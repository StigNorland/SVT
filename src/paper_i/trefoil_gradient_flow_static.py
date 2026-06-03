"""#77 Track 2: imaginary-time gradient flow with topology guard.

Replaces GMRES with pure steepest-descent (gradient flow):

    psi_{t+1} = psi_t - alpha * grad E[psi_t]

With an adaptive topology guard: if count_vortex_links drops by more than
topo_drop_tol after a step, the step is rejected and alpha is halved.
Small gradient-descent steps cannot cross topology-changing barriers, so
the guard fires rarely (if ever) under normal operation.

Key difference from the Krylov solver:
  - No GMRES, no implicit solve — pure explicit descent
  - Steps are O(alpha * dx^2) in Hilbert space rather than O(1)
  - Topology is preserved by step-size control, not by a penalty term
  - No geometry-forcing penalty => relaxed state is not penalty-dependent

Usage:
    python trefoil_gradient_flow_static.py \\
        --load-state path/to/initial.npz \\
        --n 48 --max-steps 2000 --alpha 1e-3 \\
        --save-state output.npz --output output.json

    # or from scratch:
    python trefoil_gradient_flow_static.py --n 48 --max-steps 2000

Pre-registered decision rule (#77 Track 2):
    PASS: n_y_per_curve_length spread < 5% across n=48 and n=72
          under gradient flow at the same alpha_init / convergence criterion.
    FAIL: spread >= 5% (geometries still resolution-dependent).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import asdict, dataclass, fields
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, ScriptMetadata
from trefoil_observables import total_energy
from trefoil_breather_static import (
    TrefoilConfig,
    apply_boundary_anchor,
    coordinate_grid,
    initial_state,
    logse_gradient,
)
from lperp_helpers import lperp_energy, lperp_gradient
from topology_helpers import count_vortex_links
from topology_penalty import (
    core_mask,
    topology_penalty_energy,
    topology_penalty_gradient,
)
from gradient_flow_numba import (
    NUMBA_AVAILABLE,
    count_links_numba,
    energy_total_numba,
    logse_gradient_numba,
)

SCRIPT_METADATA = ScriptMetadata(
    problem_type="static",
    status=OutputStatus.CANDIDATE,
    nondimensionalisation="xi = 1, rho0 = 1, c = 1",
    observables=("total_energy", "min_density", "vortex_links", "alpha"),
    diagnostics=("gradient_flow", "topology_guard"),
    issue_refs=("#77",),
    limitations=(
        "Explicit gradient descent: stable for alpha < dx^2 / kinetic_scale.",
        "No penalty term: topology relies entirely on step-size control.",
        "Convergence is O(1/alpha) steps — much slower than GMRES.",
        "Observables extracted via trefoil_breather_observables separately.",
    ),
)


# ---------------------------------------------------------------------------
# Gradient and energy
# ---------------------------------------------------------------------------

def full_gradient(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    lambda_perp: float,
    penalty_mask: np.ndarray | None = None,
    penalty_mu: float = 0.0,
    penalty_rho_target: float = 0.0,
) -> np.ndarray:
    g = logse_gradient(psi, cfg) + lperp_gradient(psi, cfg.grid.spacing, lambda_perp)
    if penalty_mu > 0.0 and penalty_mask is not None:
        g = g + topology_penalty_gradient(psi, penalty_mask, penalty_rho_target, penalty_mu)
    return g


def full_energy(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    lambda_perp: float,
    penalty_mask: np.ndarray | None = None,
    penalty_mu: float = 0.0,
    penalty_rho_target: float = 0.0,
) -> float:
    e = total_energy(psi, cfg.grid.spacing, cfg.log_pressure, cfg.density_floor)
    e += lperp_energy(psi, cfg.grid.spacing, lambda_perp)
    if penalty_mu > 0.0 and penalty_mask is not None:
        e += topology_penalty_energy(psi, penalty_mask, penalty_rho_target, penalty_mu, cfg.grid.spacing)
    return float(e)


def spectral_regrid(psi: np.ndarray, n_target: int) -> np.ndarray:
    """Upsample or downsample a 3D complex field via FFT zero-padding.

    Preserves all frequencies below min(n_src, n_target) / 2.
    This is the standard smooth interpolation for periodic/Dirichlet fields.
    """
    import numpy.fft as nf
    n_src = psi.shape[0]
    if n_src == n_target:
        return psi.copy()
    psi_k = nf.fftn(psi)
    # Shift zero-frequency to centre, crop/pad symmetrically, shift back
    psi_k = nf.fftshift(psi_k)
    half_t = n_target // 2
    half_s = n_src // 2
    out_k = np.zeros((n_target, n_target, n_target), dtype=np.complex128)
    # Copy the low-frequency block
    sl_s = slice(half_s - min(half_s, half_t), half_s + min(half_s, half_t))
    sl_t = slice(half_t - min(half_s, half_t), half_t + min(half_s, half_t))
    out_k[sl_t, sl_t, sl_t] = psi_k[sl_s, sl_s, sl_s]
    out_k = nf.ifftshift(out_k)
    # Scale to preserve RMS amplitude
    psi_out = nf.ifftn(out_k) * (n_target / n_src) ** 3
    return psi_out.astype(np.complex128)


def _nearest_curve_chunked(
    points: np.ndarray,
    curve: np.ndarray,
    n_workers: int = 4,
) -> np.ndarray:
    """Find nearest curve-sample index for each grid point, processing z-slices
    in parallel batches.

    Peak memory per batch: batch_size × S × n² × 3 × 8 bytes.
    At n=128, S=100, batch_size=8: 8 × 100 × 128² × 24 = 320 MB.
    """
    from concurrent.futures import ThreadPoolExecutor

    nx, ny, nz = points.shape[:3]
    nearest = np.empty((nx, ny, nz), dtype=np.int32)

    def process_slice(iz: int) -> None:
        pts = points[:, :, iz, :]                                         # (nx, ny, 3)
        offsets = pts[np.newaxis] - curve[:, np.newaxis, np.newaxis, :]   # (S, nx, ny, 3)
        dist_sq = np.einsum("sijk,sijk->sij", offsets, offsets)
        nearest[:, :, iz] = np.argmin(dist_sq, axis=0)

    with ThreadPoolExecutor(max_workers=n_workers) as pool:
        list(pool.map(process_slice, range(nz)))

    return nearest


def chunked_initial_state(cfg: TrefoilConfig) -> np.ndarray:
    """Memory-efficient version of trefoil_breather_static.initial_state.

    Uses _nearest_curve_chunked so peak RAM scales as O(frame_samples × n²)
    rather than O(frame_samples × n³).
    """
    from trefoil_breather_static import trefoil_curve, coordinate_grid

    x, y, z = coordinate_grid(cfg)
    points = np.stack((x, y, z), axis=-1)
    curve, _tangent, normal, binormal = trefoil_curve(
        cfg.frame_samples,
        major_radius=cfg.major_radius,
        minor_radius=cfg.minor_radius,
    )

    nearest = _nearest_curve_chunked(points, curve)

    nearest_curve    = curve[nearest]
    nearest_normal   = normal[nearest]
    nearest_binormal = binormal[nearest]
    nearest_offset   = points - nearest_curve

    radial_n  = np.sum(nearest_offset * nearest_normal,   axis=-1)
    radial_b  = np.sum(nearest_offset * nearest_binormal, axis=-1)
    distance  = np.sqrt(np.maximum(radial_n**2 + radial_b**2, 0.0))
    theta     = np.arctan2(radial_b, radial_n)

    amplitude = np.tanh(distance / (math.sqrt(2.0) * cfg.xi))
    phase     = np.exp(1j * theta)

    radius_sq = x**2 + y**2 + z**2
    seed = 1.0 - 0.25 * np.exp(-radius_sq / max(cfg.smoothing_radius**2, 1e-12))
    return (amplitude * phase * seed).astype(np.complex128)


def normalize_bulk(psi: np.ndarray, cfg: TrefoilConfig) -> np.ndarray:
    """Rescale psi so the mean density in the outer quarter-shell is rho0=1."""
    n = psi.shape[0]
    shell = max(1, n // 8)
    outer = np.zeros(psi.shape, dtype=bool)
    outer[:shell] = True; outer[-shell:] = True
    outer[:, :shell] = True; outer[:, -shell:] = True
    outer[:, :, :shell] = True; outer[:, :, -shell:] = True
    rho_bulk = float(np.mean(np.abs(psi[outer]) ** 2))
    if rho_bulk > 0:
        psi = psi / math.sqrt(rho_bulk)
    return psi


# ---------------------------------------------------------------------------
# Main gradient flow loop
# ---------------------------------------------------------------------------

@dataclass
class StepRecord:
    step: int
    energy: float
    alpha: float
    n_links: int
    rejected: bool
    elapsed_s: float


def run_gradient_flow(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    lambda_perp: float = 0.0,
    alpha_init: float = 1e-3,
    alpha_min: float = 1e-10,
    alpha_max_scale: float = 2.0,
    topo_drop_tol: int = 3,
    max_steps: int = 2000,
    energy_rtol: float = 1e-7,
    check_interval: int = 50,
    save_interval: int = 200,
    save_path: Path | None = None,
    penalty_mu: float = 0.0,
    penalty_rho_target: float = 0.05,
    use_numba: bool = True,
    verbose: bool = True,
) -> tuple[np.ndarray, list[StepRecord]]:
    """Pure gradient descent with adaptive topology guard.

    Returns (final_psi, step_records).
    """
    dx = cfg.grid.spacing

    # Safety: alpha must be below the kinetic stability limit dx^2 / pi^2
    alpha_stability = 0.9 * dx ** 2 / (math.pi ** 2)
    alpha = min(alpha_init, alpha_stability)
    alpha_max = min(alpha_init * alpha_max_scale, alpha_stability)

    if verbose:
        print(f"  n={cfg.n}  dx={dx:.4f}  alpha_init={alpha:.2e}  "
              f"alpha_stability={alpha_stability:.2e}  lambda_perp={lambda_perp}")

    penalty_mask = (
        core_mask(psi, 0.5) if penalty_mu > 0.0 else None
    )
    pen_kw = dict(
        penalty_mask=penalty_mask,
        penalty_mu=penalty_mu,
        penalty_rho_target=penalty_rho_target,
    )

    # Fast path: numba kernels for the per-step hot functions. Only valid when
    # there is no L_perp term and no penalty (the kernels implement pure LogSE).
    # Otherwise fall back to the numpy implementations.
    fast = use_numba and NUMBA_AVAILABLE and lambda_perp == 0.0 and penalty_mu == 0.0
    if fast:
        df = cfg.density_floor
        lp = cfg.log_pressure
        _count = lambda f: count_links_numba(f)
        _energy = lambda f: energy_total_numba(f, dx, lp, df)
        _grad = lambda f: logse_gradient_numba(f, dx, lp, df)
    else:
        _count = count_vortex_links
        _energy = lambda f: full_energy(f, cfg, lambda_perp, **pen_kw)
        _grad = lambda f: full_gradient(f, cfg, lambda_perp, **pen_kw)

    apply_boundary_anchor(psi, cfg)
    # Normalize once at start; NOT inside the gradient loop (would break descent)
    psi = normalize_bulk(psi, cfg)
    apply_boundary_anchor(psi, cfg)

    energy = _energy(psi)
    n_links = _count(psi)
    initial_links = n_links
    records: list[StepRecord] = []
    t0 = time.perf_counter()

    if verbose:
        backend = "numba (parallel)" if fast else "numpy"
        print(f"  initial: E={energy:.6f}  links={n_links}  [{backend}]")

    energies_window: list[float] = []
    MAX_BACKTRACK = 40   # more halvings → finer minimum step
    rejected_streak = 0

    for step in range(1, max_steps + 1):
        grad = _grad(psi)

        # Adaptive backtracking line search with warm start: try to grow the
        # step by 2x from the last accepted alpha, then halve until the step
        # both decreases energy and preserves topology. The accepted alpha is
        # carried forward (NOT reset to alpha_init each step) so the search can
        # ride a small step size through stiff regions and grow back out of
        # them — resetting to alpha_init each step stalls the descent.
        alpha_try = min(alpha * 2.0, alpha_max)
        rejected = True
        for _bt in range(MAX_BACKTRACK):
            candidate = psi - alpha_try * grad
            apply_boundary_anchor(candidate, cfg)

            n_links_candidate = _count(candidate)
            topo_ok = (n_links_candidate >= n_links - topo_drop_tol)
            e_candidate = _energy(candidate)
            energy_ok = (e_candidate < energy)

            if topo_ok and energy_ok:
                rejected = False
                break
            alpha_try /= 2.0

        if not rejected:
            psi = candidate
            energy = e_candidate
            n_links = n_links_candidate
            alpha = alpha_try
            rejected_streak = 0
        else:
            rejected_streak += 1
            if alpha_try < alpha_min:
                if verbose:
                    print(f"  step {step}: alpha below minimum ({alpha_min:.1e}), stopping.")
                break
            alpha = alpha_try

        elapsed = time.perf_counter() - t0
        records.append(StepRecord(step, energy, alpha, n_links, rejected, elapsed))
        energies_window.append(energy)
        if len(energies_window) > check_interval:
            energies_window.pop(0)

        if verbose and (step % check_interval == 0 or step <= 5):
            rej_str = f"  REJECTED x{rejected_streak}" if rejected_streak > 0 else ""
            print(f"  step {step:5d}  E={energy:.8f}  links={n_links:4d}  "
                  f"alpha={alpha:.2e}  ({elapsed:.1f}s){rej_str}")

        # Convergence check
        if len(energies_window) == check_interval:
            e_old = energies_window[0]
            rel_change = abs(e_old - energy) / max(abs(e_old), 1e-300)
            if rel_change < energy_rtol:
                if verbose:
                    print(f"  converged at step {step}: rel_change={rel_change:.2e} < {energy_rtol:.1e}")
                break

        # Checkpoint save
        if save_path and step % save_interval == 0:
            _save_state(psi, cfg, lambda_perp, records, save_path)

    if verbose:
        print(f"  final: E={energy:.8f}  links={n_links}  "
              f"(initial {initial_links})  alpha={alpha:.2e}")
        if n_links < initial_links:
            print(f"  WARNING: lost {initial_links - n_links} vortex links during relaxation")

    return psi, records


# ---------------------------------------------------------------------------
# State I/O
# ---------------------------------------------------------------------------

def load_state_npz(path: Path) -> tuple[np.ndarray, dict]:
    """Load psi and cfg dict from a saved .npz (supports both JSON-string and object-array formats)."""
    d = np.load(path, allow_pickle=True)
    psi = d["psi_real"] + 1j * d["psi_imag"]
    key = "config" if "config" in d else "cfg"
    raw = d[key]
    # JSON string format (saved by this script and the Krylov solver)
    raw_val = raw.item() if raw.ndim == 0 else str(raw)
    if isinstance(raw_val, str):
        cfg_dict = json.loads(raw_val)
    else:
        cfg_dict = dict(raw_val)
    return psi, cfg_dict


def _save_state(
    psi: np.ndarray,
    cfg: TrefoilConfig,
    lambda_perp: float,
    records: list[StepRecord],
    path: Path,
) -> None:
    x, y, z = coordinate_grid(cfg)
    cfg_dict = {
        "n": cfg.n,
        "half_width": cfg.half_width,
        "major_radius": cfg.major_radius,
        "minor_radius": cfg.minor_radius,
        "log_pressure": cfg.log_pressure,
        "lambda_perp": lambda_perp,
        "frame_samples": cfg.frame_samples,
        "density_floor": cfg.density_floor,
    }
    np.savez_compressed(
        path,
        psi_real=psi.real,
        psi_imag=psi.imag,
        x=x, y=y, z=z,
        config=json.dumps(cfg_dict),
        controls=json.dumps({}),
        lperp=json.dumps({"lambda_perp": lambda_perp}),
        summary=json.dumps({
            "steps": len(records),
            "final_energy": records[-1].energy if records else float("nan"),
            "final_links": records[-1].n_links if records else 0,
        }),
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n", type=int, default=48)
    p.add_argument("--half-width", type=float, default=6.0)
    p.add_argument("--major-radius", type=float, default=2.8)
    p.add_argument("--minor-radius", type=float, default=0.85)
    p.add_argument("--log-pressure", type=float, default=0.5)
    p.add_argument("--lambda-perp", type=float, default=0.0)
    p.add_argument("--load-state", type=Path, default=None,
                   help="Warm-start from a saved .npz state (overrides --n geometry)")
    p.add_argument("--alpha", type=float, default=1e-3,
                   help="Initial gradient descent step size")
    p.add_argument("--alpha-min", type=float, default=1e-10)
    p.add_argument("--topo-drop-tol", type=int, default=3,
                   help="Max allowed link drop per step before rejection")
    p.add_argument("--max-steps", type=int, default=2000)
    p.add_argument("--energy-rtol", type=float, default=1e-7,
                   help="Relative energy change convergence criterion")
    p.add_argument("--check-interval", type=int, default=50)
    p.add_argument("--save-interval", type=int, default=500)
    p.add_argument("--penalty-mu", type=float, default=0.0)
    p.add_argument("--penalty-rho-target", type=float, default=0.05)
    p.add_argument("--save-state", type=Path, default=None)
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--frame-samples", type=int, default=None,
                   help="Curve sample count for initial_state (default: auto, 100 for n>=96)")
    p.add_argument("--regrid-from", type=Path, default=None,
                   help="Spectrally interpolate a coarser saved .npz state to --n instead of "
                        "building a fresh trefoil.  Avoids sharp-feature artefacts at fine grids.")
    p.add_argument("--no-numba", action="store_true",
                   help="Disable numba-accelerated kernels (use pure numpy).")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # Curve sample count for the fresh initial state. The vortex curve must be
    # sampled finer than the grid (spacing < dx/2) or the initial trefoil is
    # bumpy and the relaxation stalls at high energy. With the chunked
    # nearest-point search, memory is O(frame_samples * n^2) so we can afford a
    # generous count: ~8*n gives curve spacing ~dx/2 (arc length ~39 xi, box 12 xi).
    def _frame_samples(n: int) -> int:
        if args.frame_samples is not None:
            return args.frame_samples
        return max(600, 8 * n)

    if args.regrid_from is not None:
        print(f"Regriding from {args.regrid_from.name} to n={args.n}...")
        psi_coarse, cfg_dict_coarse = load_state_npz(args.regrid_from)
        n_coarse = int(cfg_dict_coarse.get("n", psi_coarse.shape[0]))
        n = args.n
        cfg = TrefoilConfig(
            n=n,
            half_width=float(cfg_dict_coarse.get("half_width", args.half_width)),
            major_radius=float(cfg_dict_coarse.get("major_radius", args.major_radius)),
            minor_radius=float(cfg_dict_coarse.get("minor_radius", args.minor_radius)),
            log_pressure=float(cfg_dict_coarse.get("log_pressure", args.log_pressure)),
            frame_samples=_frame_samples(n),
        )
        psi = spectral_regrid(psi_coarse, n)
        del psi_coarse
        print(f"  spectral regrid: n={n_coarse} → n={n}, frame_samples={cfg.frame_samples}")

    elif args.load_state is not None:
        print(f"Loading initial state from {args.load_state.name}...")
        psi, cfg_dict = load_state_npz(args.load_state)
        n = int(cfg_dict.get("n", args.n))
        cfg = TrefoilConfig(
            n=n,
            half_width=float(cfg_dict.get("half_width", args.half_width)),
            major_radius=float(cfg_dict.get("major_radius", args.major_radius)),
            minor_radius=float(cfg_dict.get("minor_radius", args.minor_radius)),
            log_pressure=float(cfg_dict.get("log_pressure", args.log_pressure)),
            frame_samples=_frame_samples(n),
        )
        print(f"  loaded n={cfg.n}, major_radius={cfg.major_radius}, "
              f"minor_radius={cfg.minor_radius}, frame_samples={cfg.frame_samples}")
    else:
        n = args.n
        cfg = TrefoilConfig(
            n=n,
            half_width=args.half_width,
            major_radius=args.major_radius,
            minor_radius=args.minor_radius,
            log_pressure=args.log_pressure,
            frame_samples=_frame_samples(n),
        )
        psi = chunked_initial_state(cfg)
        print(f"Starting from fresh trefoil: n={cfg.n}, frame_samples={cfg.frame_samples} (chunked)")

    save_path = args.save_state
    if save_path is None:
        save_path = Path(
            f"papers/SSV-I/data/gradient-flow-n{cfg.n}-"
            f"hw{cfg.half_width:.0f}-{args.max_steps}steps.npz"
        )

    print(f"\nRunning gradient flow  n={cfg.n}  max_steps={args.max_steps}  "
          f"alpha={args.alpha:.1e}  lambda_perp={args.lambda_perp}")

    psi_final, records = run_gradient_flow(
        psi, cfg,
        lambda_perp=args.lambda_perp,
        alpha_init=args.alpha,
        alpha_min=args.alpha_min,
        topo_drop_tol=args.topo_drop_tol,
        max_steps=args.max_steps,
        energy_rtol=args.energy_rtol,
        check_interval=args.check_interval,
        save_interval=args.save_interval,
        save_path=save_path,
        penalty_mu=args.penalty_mu,
        penalty_rho_target=args.penalty_rho_target,
        use_numba=not args.no_numba,
    )

    save_path.parent.mkdir(parents=True, exist_ok=True)
    _save_state(psi_final, cfg, args.lambda_perp, records, save_path)
    print(f"\nSaved to {save_path}")

    if args.output:
        result = {
            "n": cfg.n,
            "half_width": cfg.half_width,
            "major_radius": cfg.major_radius,
            "minor_radius": cfg.minor_radius,
            "log_pressure": cfg.log_pressure,
            "lambda_perp": args.lambda_perp,
            "alpha_init": args.alpha,
            "n_steps": len(records),
            "final_energy": records[-1].energy if records else float("nan"),
            "final_links": records[-1].n_links if records else 0,
            "final_alpha": records[-1].alpha if records else float("nan"),
            "n_rejected": sum(1 for r in records if r.rejected),
            "metadata": {k: str(v) for k, v in asdict(SCRIPT_METADATA).items()},
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w") as fh:
            json.dump(result, fh, indent=2, default=str)
        print(f"Wrote summary to {args.output}")


if __name__ == "__main__":
    main()

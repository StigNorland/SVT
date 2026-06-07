"""Paper II reconnection-barrier numerical supplement.

Status: prototype
Problem type: dynamic
Nondimensionalisation: xi = 1, rho0 = 1.  The longitudinal speed is
NOT c = 1 in the canonical-conventions sense: the LogSE coupling enters
as ``log_pressure`` (default 8.0), so the effective sound speed is
``c_eff = sqrt(2 * log_pressure)`` in dimensionless units.  This is a
known convention mismatch with the static branch's c = 1 default.  Use
``--log-pressure 0.5`` for closure-grade runs compatible with the static
branch (issue #15).

Primary observables: saddle_index, saddle_excess, cap_radius, cap_volume,
                     cos_phi, energy_drift_pct, norm_drift_pct
Primary role: structural reproduction harness for the Paper II W/Z
reconnection-barrier checks.  Not a physical-scale production calculation;
the real SSV scale separation requires a petascale 3D grid (issue #15).

The implemented model:
- initializes two vortex rings with configurable topology,
- evolves a split-step LogSE/GPE path,
- includes chiral-shear stiffness spectrally as lambda_perp * k^4,
- extracts an effective depleted-cap radius,
- extracts a projected-Hessian amplitude/phase channel measure cos_phi,
- writes CSV rows for opposite and same topology sweeps.

Example:
    python instruments/paper_ii/reconnection_supplement.py --n 32 --length 18 \
        --lambda-perp 0 --lambda-perp 1 --lambda-perp 10 --lambda-perp 100 \
        --output papers/SSV-II/data/example_sweep.csv
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from shared_numerics import OutputStatus, ScriptMetadata


SCRIPT_METADATA = ScriptMetadata(
    problem_type="dynamic",
    status=OutputStatus.PROTOTYPE,
    nondimensionalisation="xi = 1, rho0 = 1, c_eff = sqrt(2*log_pressure)",
    observables=(
        "saddle_index",
        "saddle_excess",
        "cap_radius",
        "cap_volume",
        "cos_phi",
        "energy_drift_pct",
        "norm_drift_pct",
    ),
    diagnostics=(
        "split_step_energy_drift",
        "norm_drift",
        "cap_extraction_method",
    ),
    issue_refs=("#15", "#16"),
    limitations=(
        "Structural reproduction harness only; not a physical-scale production reconnection solver.",
        "Use --log-pressure 0.5 for static-branch-compatible runs (canonical c=1); default log_pressure=8.0 "
        "gives c_eff=4, a known convention mismatch (issue #15).",
        "Timestep / resolution / initial-condition sensitivity sweeps are open work under issue #16 (dynamic side).",
        "Cap radius extracted by volume-based or radial-slice method; both rely on a fixed cap_threshold cutoff.",
        "Radiated-mode spectrum is a basic radial-power-spectrum of delta_psi (first vs last snapshot), "
        "not a mode-decomposition into physical Bogoliubov branches (issue #15 task 4 partial).",
    ),
)


@dataclass(frozen=True)
class Config:
    n: int = 32
    length: float = 18.0
    xi: float = 1.0
    ring_radius: float | None = None
    core_radius: float | None = None
    separation: float | None = None
    dt: float = 0.001
    steps: int = 200
    snapshots: int = 17
    log_pressure: float = 8.0   # default kept for backwards compat; use 0.5 for c=1
    lambda_perp: float = 0.0
    cap_threshold: float = 0.25
    cap_method: str = "volume"
    saddle_window: int = 1

    @property
    def dx(self) -> float:
        return self.length / self.n

    @property
    def c_eff(self) -> float:
        return math.sqrt(2.0 * self.log_pressure)

    @property
    def effective_ring_radius(self) -> float:
        return 0.18 * self.length if self.ring_radius is None else self.ring_radius

    @property
    def effective_core_radius(self) -> float:
        return self.xi if self.core_radius is None else self.core_radius

    @property
    def effective_separation(self) -> float:
        return 0.34 * self.length if self.separation is None else self.separation


@dataclass
class AnalyseResult:
    """Full diagnostics returned by analyse().  Replaces the bare 4-tuple."""
    saddle_index: int
    saddle_excess: float
    cap_radius: float
    cap_volume: float
    cos_phi: float
    energy_drift_pct: float
    norm_drift_pct: float
    radiated_k: np.ndarray = field(default_factory=lambda: np.array([]))
    radiated_power: np.ndarray = field(default_factory=lambda: np.array([]))

    def as_tuple(self) -> tuple[int, float, float, float]:
        """Legacy 4-tuple for callers that still unpack (saddle_index, excess, radius, cos_phi)."""
        return self.saddle_index, self.saddle_excess, self.cap_radius, self.cos_phi


def stability_dt_max(cfg: Config, safety: float = 0.1) -> float:
    """Maximum accurate dt for the Strang-split chiral k^4 step.

    The Strang splitting is second-order accurate when
    lambda_perp * k_max^4 * dt << 1.  Empirically, energy_drift_pct ≈ 4–5%
    at product = 0.5 and ≈ 0.4% at product = 0.1.  Use safety = 0.1 (default)
    for accuracy-grade runs (energy drift < ~0.5%); safety = 0.5 for quick
    structural runs (energy drift ~5%).  If lambda_perp == 0, returns inf.
    """
    if cfg.lambda_perp == 0.0:
        return float("inf")
    k_max = math.pi / cfg.dx
    return safety / (cfg.lambda_perp * k_max ** 4)


def steps_for_duration(cfg: Config, duration: float) -> int:
    """Number of stable steps needed to evolve for `duration` time units.

    Uses stability_dt_max(cfg) as the step size.  If lambda_perp==0 uses cfg.dt.
    """
    dt = min(cfg.dt, stability_dt_max(cfg))
    return math.ceil(duration / dt)


def coordinate_grid(cfg: Config) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    axis = (np.arange(cfg.n) + 0.5) * cfg.dx - 0.5 * cfg.length
    return np.meshgrid(axis, axis, axis, indexing="ij")


def ring_factor(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    radius: float,
    z0: float,
    circulation: float,
    core_radius: float,
) -> np.ndarray:
    rho = np.sqrt(x * x + y * y)
    s = np.sqrt((rho - radius) ** 2 + (z - z0) ** 2)
    theta = np.arctan2(z - z0, rho - radius)
    amp = np.tanh(s / (math.sqrt(2.0) * core_radius))
    return amp * np.exp(1j * circulation * theta)


def initial_state(cfg: Config, lower_circ: float, upper_circ: float) -> np.ndarray:
    x, y, z = coordinate_grid(cfg)
    radius = cfg.effective_ring_radius
    core = cfg.effective_core_radius
    sep = cfg.effective_separation
    psi = ring_factor(x, y, z, radius, -0.5 * sep, lower_circ, core)
    psi *= ring_factor(x, y, z, radius, 0.5 * sep, upper_circ, core)
    # Phase kick drives the rings toward the midplane.
    psi *= np.exp(-1j * 0.9 * np.tanh(z / max(cfg.xi, 1.0e-12)) * z)
    return psi.astype(np.complex128)


def k_squared(cfg: Config) -> np.ndarray:
    k = 2.0 * math.pi * np.fft.fftfreq(cfg.n, d=cfg.dx)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    return kx * kx + ky * ky + kz * kz


def nonlinear_phase(psi: np.ndarray, cfg: Config, half_dt: float) -> np.ndarray:
    rho = np.maximum(np.abs(psi) ** 2, 1.0e-300)
    chemical = cfg.log_pressure * np.log(rho)
    return psi * np.exp(-1j * chemical * half_dt)


def kinetic_step(psi: np.ndarray, cfg: Config, k2: np.ndarray) -> np.ndarray:
    spectral_energy = 0.5 * k2 + cfg.lambda_perp * k2 * k2
    factor = np.exp(-1j * spectral_energy * cfg.dt)
    return np.fft.ifftn(np.fft.fftn(psi) * factor)


def evolve_path(cfg: Config, lower_circ: float, upper_circ: float,
                effective_dt: float | None = None) -> np.ndarray:
    """Evolve cfg.steps Strang steps.  If effective_dt is given, use it instead
    of cfg.dt for the split-step (but still save cfg.snapshots snapshots)."""
    psi = initial_state(cfg, lower_circ, upper_circ)
    k2 = k_squared(cfg)
    dt = effective_dt if effective_dt is not None else cfg.dt
    save_steps = set(np.linspace(0, cfg.steps, cfg.snapshots, dtype=int).tolist())
    snapshots = [psi.copy()] if 0 in save_steps else []
    spectral_factor = np.exp(-1j * (0.5 * k2 + cfg.lambda_perp * k2 * k2) * dt)
    for step in range(1, cfg.steps + 1):
        psi = nonlinear_phase(psi, cfg, 0.5 * dt)
        psi = np.fft.ifftn(np.fft.fftn(psi) * spectral_factor)
        psi = nonlinear_phase(psi, cfg, 0.5 * dt)
        if step in save_steps:
            snapshots.append(psi.copy())
    return np.stack(snapshots, axis=0)


def central_diff(field: np.ndarray, axis: int, dx: float) -> np.ndarray:
    return (np.roll(field, -1, axis=axis) - np.roll(field, 1, axis=axis)) / (2.0 * dx)


def potential_u(abs_psi_sq: np.ndarray) -> np.ndarray:
    rho = np.maximum(abs_psi_sq, 1.0e-300)
    return rho * np.log(rho) - rho + 1.0


def phase_gradient(psi: np.ndarray, dx: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    phase = np.angle(psi)
    return tuple(
        np.angle(np.exp(1j * (np.roll(phase, -1, axis=axis) - np.roll(phase, 1, axis=axis)))) / (2.0 * dx)
        for axis in range(3)
    )


def curl_components(vx: np.ndarray, vy: np.ndarray, vz: np.ndarray, dx: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return (
        central_diff(vz, 1, dx) - central_diff(vy, 2, dx),
        central_diff(vx, 2, dx) - central_diff(vz, 0, dx),
        central_diff(vy, 0, dx) - central_diff(vx, 1, dx),
    )


def energy(psi: np.ndarray, cfg: Config) -> float:
    grad_sq = sum(np.abs(central_diff(psi, axis, cfg.dx)) ** 2 for axis in range(3))
    grad = 0.5 * grad_sq
    pot = cfg.log_pressure * potential_u(np.abs(psi) ** 2)
    chiral = 0.0
    if cfg.lambda_perp != 0.0:
        curl = curl_components(*phase_gradient(psi, cfg.dx), cfg.dx)
        chiral = 0.5 * cfg.lambda_perp * sum(component * component for component in curl)
    return float(np.sum(grad + pot + chiral) * cfg.dx**3)


def norm_sq(psi: np.ndarray, cfg: Config) -> float:
    """Integrated |psi|^2 (particle number proxy)."""
    return float(np.sum(np.abs(psi) ** 2) * cfg.dx**3)


def radiated_mode_spectrum(
    psi_before: np.ndarray,
    psi_after: np.ndarray,
    cfg: Config,
    n_bins: int = 20,
) -> tuple[np.ndarray, np.ndarray]:
    """Power spectrum of the deviation emitted during a reconnection event.

    Computes the radial power spectrum of (psi_after - psi_before) in Fourier
    space, binned by |k|.  This measures which wavenumbers receive energy during
    the event — i.e. which modes are "radiated".

    Parameters
    ----------
    psi_before : ndarray (n,n,n) complex
        Field before the event (e.g. first snapshot).
    psi_after : ndarray (n,n,n) complex
        Field after the event (e.g. last snapshot or first post-saddle snapshot).
    cfg : Config
    n_bins : int
        Number of radial k bins.

    Returns
    -------
    k_centres : ndarray (n_bins,)
        Bin-centre wavenumbers (in units of 1/xi, since xi=1).
    power : ndarray (n_bins,)
        Mean |delta_psi_hat|^2 per mode in each bin, scaled by dx^3.
    """
    delta = psi_after - psi_before
    delta_hat = np.fft.fftn(delta) * cfg.dx**3
    power_3d = np.abs(delta_hat) ** 2

    k = 2.0 * math.pi * np.fft.fftfreq(cfg.n, d=cfg.dx)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    k_mag = np.sqrt(kx**2 + ky**2 + kz**2).ravel()
    power_flat = power_3d.ravel()

    k_max_grid = math.pi * cfg.n / cfg.length  # Nyquist
    k_edges = np.linspace(0.0, k_max_grid, n_bins + 1)
    k_centres = 0.5 * (k_edges[:-1] + k_edges[1:])
    power_bins = np.zeros(n_bins)
    counts = np.zeros(n_bins, dtype=int)
    for i in range(n_bins):
        mask = (k_mag >= k_edges[i]) & (k_mag < k_edges[i + 1])
        if np.any(mask):
            power_bins[i] = float(np.mean(power_flat[mask]))
            counts[i] = int(np.sum(mask))

    return k_centres, power_bins


def cap_radius_and_volume(psi: np.ndarray, cfg: Config) -> tuple[float, float]:
    """Return (cap_radius, cap_volume) for the depleted cap."""
    depleted = np.abs(psi) < cfg.cap_threshold
    volume = float(np.count_nonzero(depleted) * cfg.dx**3)
    if volume == 0.0:
        return 0.0, 0.0
    if cfg.cap_method == "radial-slice":
        axis = (np.arange(cfg.n) + 0.5) * cfg.dx - 0.5 * cfg.length
        x, y = np.meshgrid(axis, axis, indexing="ij")
        r = np.sqrt(x * x + y * y)
        z_index = int(np.argmax(np.count_nonzero(depleted, axis=(0, 1))))
        mask = depleted[:, :, z_index]
        radius = float(np.max(r[mask])) if np.any(mask) else 0.0
    else:
        radius = math.sqrt(volume / (math.pi * cfg.xi))
    return radius, volume


def cap_radius(psi: np.ndarray, cfg: Config) -> float:
    """Return cap radius only (backwards-compatible wrapper)."""
    r, _ = cap_radius_and_volume(psi, cfg)
    return r


def real_inner(a: np.ndarray, b: np.ndarray, cfg: Config) -> float:
    return float(np.sum((np.conjugate(a) * b).real) * cfg.dx**3)


def align_global_phase(reference: np.ndarray, psi: np.ndarray) -> np.ndarray:
    overlap = np.vdot(reference, psi)
    return psi if abs(overlap) <= 1.0e-300 else psi * np.exp(-1j * np.angle(overlap))


def projected_hessian_mode(path: np.ndarray, saddle_index: int, cfg: Config) -> np.ndarray:
    psi0 = path[saddle_index]
    candidates = []
    for offset in range(1, cfg.saddle_window + 1):
        for index in (saddle_index - offset, saddle_index + offset):
            if 0 <= index < len(path):
                candidates.append(align_global_phase(psi0, path[index]) - psi0)
    basis: list[np.ndarray] = []
    for candidate in candidates:
        vec = candidate.copy()
        for existing in basis:
            vec = vec - real_inner(existing, vec, cfg) * existing
        norm = math.sqrt(max(real_inner(vec, vec, cfg), 0.0))
        if norm > 1.0e-10:
            basis.append(vec / norm)
    if not basis:
        return np.zeros_like(psi0)
    h = 0.05
    e0 = energy(psi0, cfg)
    dim = len(basis)
    hessian = np.zeros((dim, dim), dtype=float)
    for i, vi in enumerate(basis):
        hessian[i, i] = (energy(psi0 + h * vi, cfg) - 2.0 * e0 + energy(psi0 - h * vi, cfg)) / (h * h)
        for j in range(i + 1, dim):
            vj = basis[j]
            hessian[i, j] = (
                energy(psi0 + h * (vi + vj), cfg)
                - energy(psi0 + h * (vi - vj), cfg)
                - energy(psi0 + h * (-vi + vj), cfg)
                + energy(psi0 - h * (vi + vj), cfg)
            ) / (4.0 * h * h)
            hessian[j, i] = hessian[i, j]
    _, eigenvectors = np.linalg.eigh(hessian)
    coeffs = eigenvectors[:, 0]
    delta = np.zeros_like(psi0)
    for coeff, vec in zip(coeffs, basis):
        delta = delta + coeff * vec
    return delta


def cos_phi(delta: np.ndarray, psi0: np.ndarray, cfg: Config) -> float:
    amp = np.abs(psi0)
    unit = np.divide(psi0, amp, out=np.ones_like(psi0), where=amp > 1.0e-12)
    rotated = np.conjugate(unit) * delta
    cell = cfg.dx**3
    amp_norm = math.sqrt(float(np.sum(rotated.real * rotated.real) * cell))
    phase_norm = math.sqrt(float(np.sum(rotated.imag * rotated.imag) * cell))
    return phase_norm / max(math.sqrt(amp_norm * amp_norm + phase_norm * phase_norm), 1.0e-300)


def analyse(path: np.ndarray, cfg: Config) -> AnalyseResult:
    """Full analysis of a reconnection path: saddle, cap, energy/norm drift, cos_phi."""
    energies = [energy(psi, cfg) for psi in path]
    norms = [norm_sq(psi, cfg) for psi in path]
    caps = [cap_radius_and_volume(psi, cfg) for psi in path]

    # Energy drift (total, not relative to baseline used for saddle detection)
    e0 = energies[0]
    energy_drift_pct = (energies[-1] - e0) / max(abs(e0), 1e-300) * 100.0

    # Norm drift (should be exactly zero for a unitary integrator, small drift = numerical error)
    n0 = norms[0]
    norm_drift_pct = (norms[-1] - n0) / max(abs(n0), 1e-300) * 100.0

    # Saddle: maximum of energy above the linear baseline connecting first and last frames
    diagnostics = []
    denom = max(len(energies) - 1, 1)
    for i, (value, (radius, volume)) in enumerate(zip(energies, caps)):
        t = i / denom
        baseline = (1.0 - t) * energies[0] + t * energies[-1]
        diagnostics.append((i, value - baseline, radius, volume))
    saddle_index, excess, radius, cap_vol = max(diagnostics[1:-1], key=lambda item: item[1])

    if saddle_index - cfg.saddle_window < 0 or saddle_index + cfg.saddle_window >= len(path):
        return AnalyseResult(
            saddle_index=saddle_index, saddle_excess=excess,
            cap_radius=radius, cap_volume=cap_vol,
            cos_phi=float("nan"),
            energy_drift_pct=energy_drift_pct, norm_drift_pct=norm_drift_pct,
        )
    mode = projected_hessian_mode(path, saddle_index, cfg)
    cp = cos_phi(mode, path[saddle_index], cfg)

    # Radiated-mode spectrum: energy deposited in k-modes from first to last snapshot
    k_bins, power_bins = radiated_mode_spectrum(path[0], path[-1], cfg)

    return AnalyseResult(
        saddle_index=saddle_index, saddle_excess=excess,
        cap_radius=radius, cap_volume=cap_vol,
        cos_phi=cp,
        energy_drift_pct=energy_drift_pct, norm_drift_pct=norm_drift_pct,
        radiated_k=k_bins, radiated_power=power_bins,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Paper II reconnection-barrier supplement.")
    parser.add_argument("--lambda-perp", type=float, action="append", required=True)
    parser.add_argument("--n", type=int, default=32)
    parser.add_argument("--length", type=float, default=18.0)
    parser.add_argument("--ring-radius", type=float)
    parser.add_argument("--core-radius", type=float)
    parser.add_argument("--separation", type=float)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--snapshots", type=int, default=17)
    parser.add_argument("--dt", type=float, default=0.001)
    parser.add_argument(
        "--log-pressure", type=float, default=8.0,
        help="LogSE log-pressure coupling (default 8.0 for backwards compat; "
             "use 0.5 for static-branch-canonical c=1 runs, issue #15).",
    )
    parser.add_argument(
        "--auto-dt", action="store_true",
        help="Auto-select dt from stability criterion lambda_perp*k_max^4*dt < 0.5. "
             "When set, ignores --dt and prints the chosen value.",
    )
    parser.add_argument("--cap-method", choices=("volume", "radial-slice"), default="volume")
    parser.add_argument("--output", type=Path, default=Path("paper_ii_reconnection_sweep.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if abs(args.log_pressure - 8.0) < 1e-9:
        warnings.warn(
            "log_pressure=8.0 (c_eff=4): not compatible with static-branch c=1. "
            "Use --log-pressure 0.5 for closure-grade runs (issue #15).",
            stacklevel=1,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cases = (("opposite", 1.0, -1.0), ("same", 1.0, 1.0))
    header = [
        "label", "lambda_perp",
        "saddle_index", "saddle_excess",
        "cap_radius", "cap_volume",
        "cos_phi",
        "energy_drift_pct", "norm_drift_pct",
        "n", "length", "log_pressure", "c_eff",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for lam in args.lambda_perp:
            for label, lower, upper in cases:
                cfg = Config(
                    n=args.n,
                    length=args.length,
                    ring_radius=args.ring_radius,
                    core_radius=args.core_radius,
                    separation=args.separation,
                    steps=args.steps,
                    snapshots=args.snapshots,
                    dt=args.dt,
                    log_pressure=args.log_pressure,
                    lambda_perp=lam,
                    cap_method=args.cap_method,
                )
                eff_dt: float | None = None
                if args.auto_dt and lam != 0.0:
                    eff_dt = stability_dt_max(cfg)
                    print(f"  auto-dt: {eff_dt:.3e} (lambda_perp*k_max^4*dt={lam*(math.pi/cfg.dx)**4*eff_dt:.3f})")
                path = evolve_path(cfg, lower, upper, effective_dt=eff_dt)
                res = analyse(path, cfg)
                writer.writerow([
                    label, f"{lam:.12g}",
                    res.saddle_index, f"{res.saddle_excess:.12g}",
                    f"{res.cap_radius:.12g}", f"{res.cap_volume:.12g}",
                    f"{res.cos_phi:.12g}",
                    f"{res.energy_drift_pct:.6g}", f"{res.norm_drift_pct:.6g}",
                    args.n, args.length, args.log_pressure, f"{cfg.c_eff:.6g}",
                ])
                print(
                    label, lam,
                    f"saddle={res.saddle_index}  excess={res.saddle_excess:.4g}  "
                    f"cap_r={res.cap_radius:.4g}  cap_vol={res.cap_volume:.4g}  "
                    f"cos_phi={res.cos_phi:.4g}  "
                    f"dE={res.energy_drift_pct:.3g}%  dN={res.norm_drift_pct:.3g}%"
                )


if __name__ == "__main__":
    main()

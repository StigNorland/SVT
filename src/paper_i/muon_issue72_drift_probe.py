"""Issue #72 Kelvin-sector drift diagnostic.

This probe is intentionally separate from the historical Stage 2/3 probes. It
tests the two immediate ambiguities left by those notes: whether the radial
window shape caused the half-width drift, and whether the reported "lowest
Kelvin mode" was actually branch swapping between Kelvin Nambu modes.
"""

from __future__ import annotations

import argparse
import math
import time
from dataclasses import dataclass

import numpy as np

from kelvin_augmented_bdg import build_bdg, build_modes
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig


LAMBDA_PERP = math.pi / 4.0
STABLE_TOL = 1.0e-5


@dataclass(frozen=True)
class ModeRow:
    omega: float
    vector: np.ndarray
    dominant_sector: str
    u_m0: float
    u_mp: float
    u_mm: float


@dataclass(frozen=True)
class SolveResult:
    label: str
    rows: list[ModeRow]
    elapsed_s: float


def parse_float_list(raw: str) -> list[float]:
    values = [float(part.strip()) for part in raw.split(",") if part.strip()]
    if not values:
        raise ValueError("expected at least one numeric value")
    return values


def parse_str_list(raw: str) -> list[str]:
    values = [part.strip() for part in raw.split(",") if part.strip()]
    if not values:
        raise ValueError("expected at least one value")
    return values


def sector_weights(vector: np.ndarray, mode_count: int, by_m: dict[int, list[int]]) -> tuple[str, float, float, float]:
    u = vector[:mode_count]
    u_m0 = float(np.sqrt(sum(abs(u[i]) ** 2 for i in by_m.get(0, []))))
    u_mp = float(np.sqrt(sum(abs(u[i]) ** 2 for i in by_m.get(+1, []))))
    u_mm = float(np.sqrt(sum(abs(u[i]) ** 2 for i in by_m.get(-1, []))))
    weights = {"m=0": u_m0**2, "m=+1": u_mp**2, "m=-1": u_mm**2}
    return max(weights, key=weights.get), u_m0, u_mp, u_mm


def solve_point(
    *,
    label: str,
    n: int,
    half_width: float,
    profile_n: int,
    window_kind: str,
    window_radius: float,
    window_taper: float,
    current_curl_model: str,
    kelvin_phi_n: int,
    kelvin_core_radius: float,
) -> SolveResult:
    t0 = time.time()
    cfg = ProjectionConfig(
        n=n,
        half_width=half_width,
        profile="numerical",
        profile_n=profile_n,
        chi_parity="sin",
        projection_window=window_kind,
        window_radius=window_radius,
        window_taper=window_taper if window_kind == "smooth" else 0.0,
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(bg, cfg, include_core_four=False, kelvin_seed="helicity")
    mode_count = len(modes)
    by_m: dict[int, list[int]] = {0: [], 1: [], -1: []}
    for i, mode in enumerate(modes):
        by_m.setdefault(mode.m_phi, []).append(i)
    h = build_bdg(
        bg,
        modes,
        cfg,
        "profile-logse",
        chiral_mix=0.0,
        bridge_model="shape",
        lambda_perp=LAMBDA_PERP,
        kelvin_dispersion="self-induction",
        kelvin_phi_n=kelvin_phi_n,
        kelvin_core_radius=kelvin_core_radius,
        current_curl_model=current_curl_model,
    )
    eigvals, eigvecs = np.linalg.eig(np.array(h, dtype=complex))
    stable_idx = sorted(
        (k for k, lam in enumerate(eigvals) if lam.real > 1.0e-5 and abs(lam.imag) <= STABLE_TOL),
        key=lambda k: eigvals[k].real,
    )
    deduped: list[int] = []
    for k in stable_idx:
        if not deduped or abs(eigvals[k].real - eigvals[deduped[-1]].real) > 1.0e-4:
            deduped.append(k)

    rows: list[ModeRow] = []
    for k in deduped:
        vector = eigvecs[:, k]
        vector = vector / np.linalg.norm(vector)
        dominant, u_m0, u_mp, u_mm = sector_weights(vector, mode_count, by_m)
        rows.append(
            ModeRow(
                omega=float(eigvals[k].real),
                vector=vector,
                dominant_sector=dominant,
                u_m0=u_m0,
                u_mp=u_mp,
                u_mm=u_mm,
            )
        )
    return SolveResult(label=label, rows=rows, elapsed_s=time.time() - t0)


def kelvin_rows(result: SolveResult) -> list[ModeRow]:
    return [row for row in result.rows if row.dominant_sector != "m=0"]


def vector_overlap(a: np.ndarray, b: np.ndarray) -> float:
    return float(abs(np.vdot(a, b)))


def track_branches(results: list[SolveResult]) -> list[tuple[ModeRow | None, ModeRow | None, float, float]]:
    tracked: list[tuple[ModeRow | None, ModeRow | None, float, float]] = []
    first = kelvin_rows(results[0])
    lower = first[0] if len(first) > 0 else None
    upper = first[1] if len(first) > 1 else None
    tracked.append((lower, upper, float("nan"), float("nan")))
    for result in results[1:]:
        candidates = kelvin_rows(result)
        next_lower, lower_ov = best_match(lower, candidates)
        remaining = [row for row in candidates if row is not next_lower]
        next_upper, upper_ov = best_match(upper, remaining)
        tracked.append((next_lower, next_upper, lower_ov, upper_ov))
        lower, upper = next_lower, next_upper
    return tracked


def best_match(previous: ModeRow | None, candidates: list[ModeRow]) -> tuple[ModeRow | None, float]:
    if previous is None or not candidates:
        return None, float("nan")
    scored = [(vector_overlap(previous.vector, candidate.vector), candidate) for candidate in candidates]
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[0][1], scored[0][0]


def print_window_table(kind: str, radii: list[float], results: list[SolveResult]) -> None:
    print(f"\n## {kind.upper()} radial window")
    print("  r_w    lower    ov_low  sec_l   upper    ov_up  sec_u   dt_s")
    for radius, result, (lower, upper, lower_ov, upper_ov) in zip(radii, results, track_branches(results)):
        lower_w = lower.omega if lower else float("nan")
        upper_w = upper.omega if upper else float("nan")
        lower_sec = lower.dominant_sector if lower else "none"
        upper_sec = upper.dominant_sector if upper else "none"
        print(
            f"  {radius:4.1f}  {lower_w:7.4f}  {lower_ov:6.3f}  {lower_sec:>5s}"
            f"  {upper_w:7.4f}  {upper_ov:6.3f}  {upper_sec:>5s}  {result.elapsed_s:5.1f}"
        )


def run_window_sweep(args: argparse.Namespace) -> None:
    radii = parse_float_list(args.window_radii)
    for kind in parse_str_list(args.window_kinds):
        results = [
            solve_point(
                label=f"{kind}-rw{radius:g}",
                n=args.n,
                half_width=args.half_width,
                profile_n=args.profile_n,
                window_kind=kind,
                window_radius=radius,
                window_taper=args.window_taper,
                current_curl_model="linear",
                kelvin_phi_n=args.kelvin_phi_n,
                kelvin_core_radius=args.kelvin_core_radius,
            )
            for radius in radii
        ]
        print_window_table(kind, radii, results)


def run_current_curl_comparison(args: argparse.Namespace) -> None:
    radii = parse_float_list(args.compare_radii)
    print("\n## LINEAR vs FULL current-curl comparison")
    print("  model   r_w    lower    upper    lowest_m0")
    for model in ("linear", "full"):
        for radius in radii:
            result = solve_point(
                label=f"{model}-rw{radius:g}",
                n=args.compare_n,
                half_width=args.compare_half_width,
                profile_n=args.profile_n,
                window_kind=args.compare_window,
                window_radius=radius,
                window_taper=args.window_taper,
                current_curl_model=model,
                kelvin_phi_n=args.kelvin_phi_n,
                kelvin_core_radius=args.kelvin_core_radius,
            )
            kelvin = kelvin_rows(result)
            m0 = [row for row in result.rows if row.dominant_sector == "m=0"]
            lower = kelvin[0].omega if len(kelvin) > 0 else float("nan")
            upper = kelvin[1].omega if len(kelvin) > 1 else float("nan")
            lowest_m0 = m0[0].omega if m0 else float("nan")
            print(f"  {model:6s}  {radius:4.1f}  {lower:7.4f}  {upper:7.4f}  {lowest_m0:9.4f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue #72 Kelvin drift diagnostic.")
    parser.add_argument("--n", type=int, default=41)
    parser.add_argument("--half-width", type=float, default=8.0)
    parser.add_argument("--profile-n", type=int, default=1600)
    parser.add_argument("--window-radii", default="1.0,1.5,2.0,2.5,3.0,3.5,4.0,5.0,6.0,8.0")
    parser.add_argument("--window-kinds", default="smooth,hard")
    parser.add_argument("--window-taper", type=float, default=0.5)
    parser.add_argument("--kelvin-phi-n", type=int, default=1024)
    parser.add_argument("--kelvin-core-radius", type=float, default=1.0)
    parser.add_argument("--compare-n", type=int, default=31)
    parser.add_argument("--compare-half-width", type=float, default=5.0)
    parser.add_argument("--compare-radii", default="1.0,2.0,4.0,8.0")
    parser.add_argument("--compare-window", choices=("none", "hard", "smooth"), default="hard")
    parser.add_argument("--skip-window-sweep", action="store_true")
    parser.add_argument("--skip-current-curl-comparison", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    t0 = time.time()
    print("=== Issue #72 Kelvin-sector drift diagnostic ===")
    print(
        f"window sweep: n={args.n}, hw={args.half_width}, profile_n={args.profile_n}, "
        "lambda_perp=pi/4, kelvin_dispersion=self-induction"
    )
    if not args.skip_window_sweep:
        run_window_sweep(args)
    if not args.skip_current_curl_comparison:
        run_current_curl_comparison(args)
    print(f"\n=== total time: {time.time() - t0:.1f}s ===")


if __name__ == "__main__":
    main()

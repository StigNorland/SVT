"""Convergence sweep for the relaxed-background correction to the thin-ring
muon helicity bridge.

What this does
--------------
For each tuple `(n, half_width, profile_n, finite_diff_step)`:

  1. Run `curved_torus_relaxation.py` to obtain (amp_coeffs, phase_coeffs).
  2. Run `thin_ring_alpha_correction.py --finite-alpha-scan` with those
     coefficients and an explicitly selected bridge profile to obtain the
     bridge ratio at the physical alpha row.
  3. Record delta_relax_chi  = chi_relative_to_first - 1
            delta_relax_R    = r_relative_to_first   - 1
     plus the linear slope in alpha and the relaxation diagnostics.

At the end, report the mean and spread of `delta_relax` across the sweep.
If `delta_relax` is stable (spread small compared to the mean), the
paper-level statement
    lambda_perp^BdG = (pi/4) * [1 + delta_relax + O(alpha^2)]
becomes a real prediction.  If the spread is large or the sign flips with
refinement, the reduced curved-background ansatz is not safe.

Usage
-----
Default sweep is a 12-point representative grid; use --grids / --half-widths
/ --profile-ns / --fd-steps to customize.

  python src/paper_i/thin_ring_delta_relax_sweep.py \\
      --output papers/SSV-I/data/delta-relax-sweep.json
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import sys
import time
from itertools import product
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RELAX_SCRIPT = REPO_ROOT / "src" / "paper_i" / "curved_torus_relaxation.py"
BRIDGE_SCRIPT = REPO_ROOT / "src" / "paper_i" / "thin_ring_alpha_correction.py"

PHYSICAL_ALPHA = 1.0 / 137.035999084

DEFAULT_GRIDS = [25, 31, 37]
DEFAULT_HALF_WIDTHS = [5, 6]
DEFAULT_PROFILE_NS = [800, 1200]
DEFAULT_FD_STEPS = [0.25]

# Regexes to parse the relaxation stdout
RE_AMP_CLI = re.compile(r"^\s*amp_coeffs_cli\s*=\s*([0-9eE\.\-,+]+)\s*$", re.MULTILINE)
RE_PHASE_CLI = re.compile(r"^\s*phase_coeffs_cli\s*=\s*([0-9eE\.\-,+]+)\s*$", re.MULTILINE)
RE_BASIS = re.compile(r"^\s*basis_count\s*=\s*(\d+)\s*$", re.MULTILINE)
RE_REL_DELTA = re.compile(r"^\s*relative_delta\s*=\s*([0-9eE\.\-+]+)\s*$", re.MULTILINE)
RE_GRAD_NORM = re.compile(r"^\s*gradient_norm\s*=\s*([0-9eE\.\-+]+)\s*$", re.MULTILINE)


def run_relaxation(n: int, hw: int, profile_n: int, fd_step: float, timeout: int) -> dict:
    """Run curved_torus_relaxation.py and parse out the CLI coefficient strings."""
    cmd = [
        sys.executable,
        str(RELAX_SCRIPT),
        "--n", str(n),
        "--half-width", str(hw),
        "--profile-n", str(profile_n),
        "--finite-diff-step", str(fd_step),
    ]
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    elapsed = time.time() - t0
    if proc.returncode != 0:
        return {"ok": False, "error": f"relaxation exit {proc.returncode}", "stderr": proc.stderr, "elapsed_s": elapsed}

    out = proc.stdout
    m_amp = RE_AMP_CLI.search(out)
    m_phase = RE_PHASE_CLI.search(out)
    m_basis = RE_BASIS.search(out)
    m_rel = RE_REL_DELTA.search(out)
    m_grad = RE_GRAD_NORM.search(out)

    if not (m_amp and m_phase):
        return {"ok": False, "error": "failed to parse coeffs from stdout", "stdout_tail": out[-1000:], "elapsed_s": elapsed}

    return {
        "ok": True,
        "amp_cli": m_amp.group(1).strip(),
        "phase_cli": m_phase.group(1).strip(),
        "basis_count": int(m_basis.group(1)) if m_basis else None,
        "relaxation_relative_delta": float(m_rel.group(1)) if m_rel else None,
        "gradient_norm": float(m_grad.group(1)) if m_grad else None,
        "elapsed_s": elapsed,
    }


def run_bridge_scan(
    amp_cli: str,
    phase_cli: str,
    scan_profile: str,
    profile_n: int,
    scan_profile_x_max: float,
    timeout: int,
) -> dict:
    """Run thin_ring_alpha_correction.py --finite-alpha-scan --json with given coeffs."""
    cmd = [
        sys.executable,
        str(BRIDGE_SCRIPT),
        "--finite-alpha-scan",
        "--scan-profile", scan_profile,
        "--scan-profile-n", str(profile_n),
        "--scan-profile-x-max", str(scan_profile_x_max),
        "--scan-curvature-coeffs", amp_cli,
        "--scan-phase-coeffs", phase_cli,
        "--json",
    ]
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    elapsed = time.time() - t0
    if proc.returncode != 0:
        return {"ok": False, "error": f"bridge exit {proc.returncode}", "stderr": proc.stderr, "elapsed_s": elapsed}

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"JSON parse: {e}", "stdout_tail": proc.stdout[-1000:], "elapsed_s": elapsed}

    curved = payload.get("curved_background_scan")
    if not curved:
        return {"ok": False, "error": "no curved_background_scan in payload", "elapsed_s": elapsed}

    # Find the physical-alpha row (closest to 1/137.036)
    rows = curved.get("rows", [])
    if not rows:
        return {"ok": False, "error": "no rows in curved_background_scan", "elapsed_s": elapsed}
    physical_row = min(rows, key=lambda r: abs(r["alpha"] - PHYSICAL_ALPHA))

    return {
        "ok": True,
        "chi_relative_at_physical_alpha": physical_row["chi_relative_to_first"],
        "r_relative_at_physical_alpha": physical_row["r_relative_to_first"],
        "chi_relative_slope": curved.get("chi_relative_slope"),
        "r_relative_slope": curved.get("r_relative_slope"),
        "physical_alpha_row": physical_row,
        "elapsed_s": elapsed,
    }


def run_one_point(
    n: int,
    hw: int,
    profile_n: int,
    fd_step: float,
    scan_profile: str,
    scan_profile_x_max: float,
    timeout: int,
) -> dict:
    """Run a single (n, hw, profile_n, fd_step) point: relaxation then bridge scan."""
    relax = run_relaxation(n, hw, profile_n, fd_step, timeout)
    point: dict = {
        "n": n,
        "half_width": hw,
        "profile_n": profile_n,
        "finite_diff_step": fd_step,
        "scan_profile": scan_profile,
        "scan_profile_x_max": scan_profile_x_max,
        "relaxation": relax,
    }
    if not relax["ok"]:
        return point

    bridge = run_bridge_scan(
        relax["amp_cli"],
        relax["phase_cli"],
        scan_profile,
        profile_n,
        scan_profile_x_max,
        timeout,
    )
    point["bridge"] = bridge
    if bridge["ok"]:
        point["delta_relax_chi"] = bridge["chi_relative_at_physical_alpha"] - 1.0
        point["delta_relax_R"] = bridge["r_relative_at_physical_alpha"] - 1.0
    return point


def summarise(points: list[dict]) -> dict:
    ok_points = [p for p in points if "delta_relax_chi" in p and "delta_relax_R" in p]
    if len(ok_points) < 2:
        return {"n_ok": len(ok_points), "warning": "too few successful points for statistics"}

    chi_values = [p["delta_relax_chi"] for p in ok_points]
    r_values = [p["delta_relax_R"] for p in ok_points]
    return {
        "n_ok": len(ok_points),
        "n_total": len(points),
        "delta_relax_chi": {
            "mean": statistics.mean(chi_values),
            "stdev": statistics.stdev(chi_values),
            "min": min(chi_values),
            "max": max(chi_values),
            "spread": max(chi_values) - min(chi_values),
        },
        "delta_relax_R": {
            "mean": statistics.mean(r_values),
            "stdev": statistics.stdev(r_values),
            "min": min(r_values),
            "max": max(r_values),
            "spread": max(r_values) - min(r_values),
        },
    }


def print_table(points: list[dict]) -> None:
    hdr = (
        f"{'n':>3s} {'hw':>3s} {'prof':>5s} {'fd':>5s} "
        f"{'rel_dE':>10s} {'|g|':>8s} "
        f"{'amp0':>8s} {'ph0':>9s} "
        f"{'d_chi_%':>8s} {'d_R_%':>8s} "
        f"{'chi_slope':>10s} {'R_slope':>10s} {'t_s':>6s}"
    )
    print(hdr)
    print("-" * len(hdr))
    for p in points:
        n, hw, pn, fd = p["n"], p["half_width"], p["profile_n"], p["finite_diff_step"]
        relax = p.get("relaxation", {})
        bridge = p.get("bridge", {})
        if not relax.get("ok"):
            print(f"{n:>3d} {hw:>3d} {pn:>5d} {fd:>5.2f}  RELAX FAILED: {relax.get('error', '?')}")
            continue
        if not bridge.get("ok"):
            print(f"{n:>3d} {hw:>3d} {pn:>5d} {fd:>5.2f}  BRIDGE FAILED: {bridge.get('error', '?')}")
            continue
        amp0 = float(relax["amp_cli"].split(",")[0])
        ph0 = float(relax["phase_cli"].split(",")[0])
        d_chi = p["delta_relax_chi"] * 100
        d_r = p["delta_relax_R"] * 100
        rel_dE = relax.get("relaxation_relative_delta", float("nan"))
        gn = relax.get("gradient_norm", float("nan"))
        chi_slope = bridge["chi_relative_slope"]
        r_slope = bridge["r_relative_slope"]
        t = relax.get("elapsed_s", 0) + bridge.get("elapsed_s", 0)
        print(
            f"{n:>3d} {hw:>3d} {pn:>5d} {fd:>5.2f} "
            f"{rel_dE:>10.2e} {gn:>8.2e} "
            f"{amp0:>8.4f} {ph0:>9.4f} "
            f"{d_chi:>+8.3f} {d_r:>+8.3f} "
            f"{chi_slope:>+10.4f} {r_slope:>+10.4f} {t:>6.1f}"
        )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--grids", type=int, nargs="+", default=DEFAULT_GRIDS)
    p.add_argument("--half-widths", type=int, nargs="+", default=DEFAULT_HALF_WIDTHS)
    p.add_argument("--profile-ns", type=int, nargs="+", default=DEFAULT_PROFILE_NS)
    p.add_argument("--fd-steps", type=float, nargs="+", default=DEFAULT_FD_STEPS)
    p.add_argument(
        "--scan-profile",
        choices=("numerical", "toy"),
        default="numerical",
        help="profile used in the finite-alpha bridge scan; default matches the BdG radial profile",
    )
    p.add_argument("--scan-profile-x-max", type=float, default=20.0)
    p.add_argument("--timeout", type=int, default=900, help="seconds per subprocess")
    p.add_argument("--output", type=Path, help="write JSON results to this file")
    p.add_argument(
        "--continue-on-error",
        action="store_true",
        default=True,
        help="(default) skip failed points; don't abort the whole sweep",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    combos = list(product(args.grids, args.half_widths, args.profile_ns, args.fd_steps))
    print(f"Sweep: {len(combos)} points "
          f"(n={args.grids}, hw={args.half_widths}, profile_n={args.profile_ns}, fd={args.fd_steps})",
          file=sys.stderr)

    points: list[dict] = []
    t_total = time.time()
    for i, (n, hw, pn, fd) in enumerate(combos, 1):
        print(f"[{i}/{len(combos)}] n={n} hw={hw} profile_n={pn} fd={fd} ...",
              file=sys.stderr)
        try:
            p = run_one_point(
                n,
                hw,
                pn,
                fd,
                args.scan_profile,
                args.scan_profile_x_max,
                args.timeout,
            )
        except subprocess.TimeoutExpired:
            p = {"n": n, "half_width": hw, "profile_n": pn, "finite_diff_step": fd,
                 "error": "timeout"}
        except Exception as e:
            p = {"n": n, "half_width": hw, "profile_n": pn, "finite_diff_step": fd,
                 "error": f"{type(e).__name__}: {e}"}
        points.append(p)

    elapsed_total = time.time() - t_total
    print(f"\nSweep complete in {elapsed_total:.1f} s\n", file=sys.stderr)

    print_table(points)

    summary = summarise(points)
    print("\n--- Summary across sweep ---")
    if summary.get("n_ok", 0) < 2:
        print(f"Only {summary.get('n_ok', 0)} successful points; insufficient for stats.")
    else:
        dchi = summary["delta_relax_chi"]
        dr = summary["delta_relax_R"]
        print(f"n_ok = {summary['n_ok']} / {summary['n_total']}")
        print(f"delta_relax_chi:  mean = {dchi['mean']*100:+.3f}%   stdev = {dchi['stdev']*100:.3f}%"
              f"   range = [{dchi['min']*100:+.3f}, {dchi['max']*100:+.3f}]%")
        print(f"delta_relax_R:    mean = {dr['mean']*100:+.3f}%   stdev = {dr['stdev']*100:.3f}%"
              f"   range = [{dr['min']*100:+.3f}, {dr['max']*100:+.3f}]%")
        verdict_chi = "STABLE" if dchi["stdev"] < 0.005 else ("DRIFTING" if dchi["stdev"] > 0.02 else "MARGINAL")
        verdict_r = "STABLE" if dr["stdev"] < 0.005 else ("DRIFTING" if dr["stdev"] > 0.02 else "MARGINAL")
        print(f"\nchi-K bridge verdict: {verdict_chi}")
        print(f"R-K   bridge verdict: {verdict_r}")

    payload = {
        "sweep_parameters": {
            "grids": args.grids,
            "half_widths": args.half_widths,
            "profile_ns": args.profile_ns,
            "fd_steps": args.fd_steps,
            "scan_profile": args.scan_profile,
            "scan_profile_x_max": args.scan_profile_x_max,
        },
        "points": points,
        "summary": summary,
        "elapsed_total_s": elapsed_total,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"\nResults written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()

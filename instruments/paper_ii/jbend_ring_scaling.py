"""Step 2: J_bend(r_max) vs r_max sweep — does the bending stiffness grow with ring radius?

If the 232x gap is explained by long-range flow (r_max → R_cap = phi/alpha ~ 222 xi),
the integral J_bend + K_bend must grow with r_max. Two candidate scalings:
  - Linear:     J+K ~ r_max          -> gap explained at R_cap = phi/alpha
  - Logarithmic: J+K ~ ln(r_max/xi)  -> LIA prediction, insufficient (ln(222) ~ 5.4)
  - Convergent: J+K -> constant       -> gap is genuinely non-local (confirmed local)

We sweep r_max = {1, 2, 3, 5, 8, 12, 20, 30, 50} xi and fit for scaling.
"""

from __future__ import annotations

import math
import sys

import numpy as np

ALPHA = 1.0 / 137.035999084
PHI   = (1.0 + math.sqrt(5.0)) / 2.0
R_CAP = PHI / ALPHA   # ~ 221.5 xi


def compute_core_integrals_to_rmax(r, f, fp, r_max):
    mask = r <= r_max
    r_m  = r[mask]
    f_m  = f[mask]
    fp_m = fp[mask]
    rs   = np.maximum(r_m, 1e-12)

    curl_j = 2.0 * f_m * fp_m / rs

    # Limit gradient computation to where curl_j is non-negligible
    # (np.gradient amplifies floating-point noise in the near-zero tail)
    thresh = max(np.max(np.abs(curl_j)) * 1e-8, 1e-15)
    active = np.abs(curl_j) > thresh
    d_curl = np.zeros_like(curl_j)
    if np.any(active):
        d_curl_full = np.gradient(curl_j, r_m)
        d_curl[active] = d_curl_full[active]

    i_curl = float(np.trapezoid(curl_j**2 * 2*math.pi*r_m, r_m))
    j_bend = float(np.trapezoid(r_m**2 * d_curl**2 * 2*math.pi*r_m, r_m))
    k_bend = float(np.trapezoid(curl_j**2 * r_m**2 * 2*math.pi*r_m, r_m))
    return i_curl, j_bend, k_bend


def vortex_rhs_b1(x: float, f: float, fp: float) -> tuple[float, float]:
    """b=1 LogSE vortex: f'' + f'/r - f/r^2 = 2f ln(f^2)."""
    safe_x = max(x, 1.0e-12)
    safe_f = max(abs(f), 1.0e-300)
    if safe_f > 1e6:
        return fp, float('nan')
    log_val = math.log(safe_f**2)
    fpp = -(fp / safe_x) + (f / (safe_x**2)) + 2.0 * f * log_val
    return fp, fpp


def rk4_step(x, f, fp, h, rhs):
    k1f, k1fp = rhs(x, f, fp)
    k2f, k2fp = rhs(x + 0.5*h, f + 0.5*h*k1f, fp + 0.5*h*k1fp)
    k3f, k3fp = rhs(x + 0.5*h, f + 0.5*h*k2f, fp + 0.5*h*k2fp)
    k4f, k4fp = rhs(x + h, f + h*k3f, fp + h*k3fp)
    return f + h/6*(k1f+2*k2f+2*k3f+k4f), fp + h/6*(k1fp+2*k2fp+2*k3fp+k4fp)


def integrate_profile(slope, x_min, x_max, n, rhs):
    h = (x_max - x_min) / (n - 1)
    xs  = [x_min + i*h for i in range(n)]
    fs  = [slope * xs[0]]
    fps = [slope]
    f, fp = slope*xs[0], slope
    for i in range(1, n):
        f, fp = rk4_step(xs[i-1], f, fp, h, rhs)
        if not (math.isfinite(f) and math.isfinite(fp)):
            f = fp = float('nan')
        fs.append(f)
        fps.append(fp)
    return np.array(xs), np.array(fs), np.array(fps)


def find_slope(x_min, x_max, n, rhs):
    """Bisect to find shooting slope that gives f(x_max) = 1."""
    def residual(slope):
        _, fs, _ = integrate_profile(slope, x_min, x_max, n, rhs)
        val = float(fs[-1])
        if not math.isfinite(val):
            return 1e30  # diverged — slope too large
        return val - 1.0

    lo, hi = 0.01, 0.01
    for _ in range(60):
        if residual(hi) >= 0:
            break
        hi *= 1.5
    for _ in range(60):
        if residual(lo) <= 0:
            break
        lo *= 0.5

    for _ in range(80):
        mid = 0.5*(lo + hi)
        if residual(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo + hi)


def main():
    n_pts    = 12000
    r_max_solve = 15.0   # b=1 LogSE has e^(2r) growing mode — numerically unstable beyond ~15 xi
    x_min    = 1e-4

    print("=" * 68)
    print("Step 2: J_bend(r_max) convergence sweep — b=1 profile")
    print("=" * 68)
    print()

    slope = find_slope(x_min, r_max_solve, n_pts, vortex_rhs_b1)
    r, f, fp = integrate_profile(slope, x_min, r_max_solve, n_pts, vortex_rhs_b1)
    print(f"  Solved b=1 profile: slope = {slope:.8f}, r_max = {r_max_solve}")
    print()

    r_max_vals = [1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 15.0]

    print(f"{'r_max/xi':>9}  {'J_bend':>10}  {'K_bend':>10}  {'(J+K)/4':>10}  "
          f"{'J+K growth':>12}")
    print("-" * 68)

    results = []
    for rm in r_max_vals:
        ic, jb, kb = compute_core_integrals_to_rmax(r, f, fp, rm)
        results.append((rm, ic, jb, kb))
        print(f"  {rm:7.1f}   {jb:10.4f}   {kb:10.4f}   {(jb+kb)/4:10.6f}   "
              f"{'(base)' if rm == r_max_vals[0] else f'{(jb+kb)/(results[0][2]+results[0][3]):.4f}x':>12}")

    print()
    # Reference values
    ic_ref, jb_ref, kb_ref = results[-2][1], results[-2][2], results[-2][3]  # r_max=12
    ic_r15, jb_r15, kb_r15 = results[-1][1], results[-1][2], results[-1][3]  # r_max=15

    print(f"  Convergence check (r=12 vs r=15):")
    print(f"    J_bend: {jb_ref:.4f} vs {jb_r15:.4f}  (change {(jb_r15/jb_ref-1)*100:+.3f}%)")
    print(f"    K_bend: {kb_ref:.4f} vs {kb_r15:.4f}  (change {(kb_r15/kb_ref-1)*100:+.3f}%)")
    print(f"    (J+K)/4: {(jb_ref+kb_ref)/4:.6f} vs {(jb_r15+kb_r15)/4:.6f}")
    print()

    # Fit: does (J+K) scale with r_max or ln(r_max) in the tail region (3-15 xi)?
    r_fit = np.array([row[0] for row in results[2:]])   # 3 to 15 xi
    jk_fit = np.array([row[2]+row[3] for row in results[2:]])

    # Linear fit: J+K = a * r_max + b
    A_lin = np.column_stack([r_fit, np.ones_like(r_fit)])
    c_lin, _, _, _ = np.linalg.lstsq(A_lin, jk_fit, rcond=None)
    jk_lin = A_lin @ c_lin
    res_lin = jk_fit - jk_lin
    r2_lin = 1 - np.var(res_lin)/np.var(jk_fit)

    # Log fit: J+K = a * ln(r_max) + b
    A_log = np.column_stack([np.log(r_fit), np.ones_like(r_fit)])
    c_log, _, _, _ = np.linalg.lstsq(A_log, jk_fit, rcond=None)
    jk_log = A_log @ c_log
    res_log = jk_fit - jk_log
    r2_log = 1 - np.var(res_log)/np.var(jk_fit)

    print(f"  Scaling fit over r_max = 5..50 xi:")
    print(f"    Linear fit:  (J+K) = {c_lin[0]:.6f} * r + {c_lin[1]:.4f}   R² = {r2_lin:.6f}")
    print(f"    Log    fit:  (J+K) = {c_log[0]:.6f} * ln(r) + {c_log[1]:.4f}   R² = {r2_log:.6f}")
    print()

    # Extrapolation to R_cap = phi/alpha
    jk_at_r15 = jb_r15 + kb_r15
    jk_lin_cap = c_lin[0] * R_CAP + c_lin[1]
    jk_log_cap = c_log[0] * math.log(R_CAP) + c_log[1]
    print(f"  Extrapolation to R_cap = phi/alpha = {R_CAP:.1f} xi:")
    print(f"    (J+K) at r_max=15:     {jk_at_r15:.4f} -> (J+K)/4 = {jk_at_r15/4:.6f}")
    print(f"    Linear extrapolation:  {jk_lin_cap:.4f} -> lambda_gap = "
          f"{PHI**2/((jk_lin_cap)/4):.4f}")
    print(f"    Log extrapolation:     {jk_log_cap:.4f} -> lambda_gap = "
          f"{PHI**2/((jk_log_cap)/4):.4f}")
    print(f"    Target (J+K)/4 = phi^2 = {PHI**2:.6f}")
    print()

    # How much would J+K need to be to close the gap?
    jk_needed = 4 * PHI**2
    print(f"  Needed (J+K) to reach phi^2: {jk_needed:.4f}")
    print(f"  Current (r_max=15):           {jk_at_r15:.4f}  "
          f"({jk_at_r15/jk_needed*100:.1f}% of target)")
    print(f"  Enhancement needed:           {jk_needed/jk_at_r15:.2f}x")
    print()

    # Lambda_bend from local vs needed
    lam_perp = 1.0 / ALPHA**2
    lam_local = lam_perp * jk_at_r15 / 4
    lam_target = PHI**3 / ALPHA**3
    print(f"  lambda_bend (r_max=15):  {lam_local:.4e}  gap = {lam_target/lam_local:.1f}x")
    print(f"  Target phi^3/alpha^3:    {lam_target:.4e}")
    print()

    print("=" * 68)
    print("CONCLUSION")
    print("=" * 68)
    if abs(r2_lin) > abs(r2_log):
        print(f"  Dominant scaling: LINEAR (R^2 = {r2_lin:.4f} > log R^2 = {r2_log:.4f})")
    else:
        print(f"  Dominant scaling: LOG (R^2 = {r2_log:.4f} > linear R^2 = {r2_lin:.4f})")

    frac_change = (jk_at_r15 - (results[3][2]+results[3][3])) / (results[3][2]+results[3][3])
    print(f"  (J+K) change from r_max=5 to r_max=50: {frac_change*100:+.2f}%")
    if abs(frac_change) < 0.02:
        print("  ** (J+K) converged to <2% over factor 10 in r_max: gap is LOCAL/UV, not IR **")
    else:
        print(f"  ** (J+K) shows non-trivial tail: {frac_change*100:.1f}% change over r=5..50 xi **")


if __name__ == "__main__":
    main()

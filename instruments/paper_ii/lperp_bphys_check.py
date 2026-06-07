"""Step 1: L_perp core integrals with the physical b=1/2 vortex profile.

The lperp_core_integral.py script used the b=1 LogSE profile:
    f'' + f'/r - f/r^2 = 2 f ln(f^2)

The physical (b=1/2) equation is:
    f'' + f'/r - f/r^2 = f ln(f^2)

This changes the vortex profile, healing length, and the core integrals J and K.
The key question: does (J+K)/4 converge toward phi^2 = 2.618 with the physical profile?

Under the rescaling f_phys(r) = f_b1(r/sqrt(2)):
    J_bend_phys = J_bend_b1 / 2
    K_bend_phys = K_bend_b1

But we should also check the RAW integrals with the b=1/2 profile, since the
healing length xi_phys = sqrt(2) xi_b1 and the physical r_max = 15 xi_phys > 15 xi_b1.
"""

from __future__ import annotations

import math
import sys

import numpy as np

ALPHA = 1.0 / 137.035999084
PHI   = (1.0 + math.sqrt(5.0)) / 2.0


# ── b=1/2 vortex ODE solver (copy of VortexProfile with b=0.5) ────────────

def vortex_rhs_bphys(x: float, f: float, fp: float) -> tuple[float, float]:
    """b=1/2 LogSE vortex: f'' + f'/r - f/r^2 = f ln(f^2)."""
    safe_x = max(x, 1.0e-12)
    safe_f = max(abs(f), 1.0e-300)
    fpp = -(fp / safe_x) + (f / (safe_x**2)) + f * math.log(safe_f**2)
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
        return float(fs[-1]) - 1.0

    lo, hi = 0.1, 0.1
    # find bracket
    while residual(hi) < 0:
        hi *= 1.5
    while residual(lo) > 0:
        lo *= 0.5

    for _ in range(80):
        mid = 0.5*(lo + hi)
        if residual(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5*(lo + hi)


def compute_core_integrals(r, f, fp, r_max):
    mask = r <= r_max
    r_m  = r[mask]
    f_m  = f[mask]
    fp_m = fp[mask]
    rs   = np.maximum(r_m, 1e-12)

    curl_j = 2.0 * f_m * fp_m / rs
    d_curl  = np.gradient(curl_j, r_m)

    i_curl = float(np.trapezoid(curl_j**2 * 2*math.pi*r_m, r_m))
    j_bend = float(np.trapezoid(r_m**2 * d_curl**2 * 2*math.pi*r_m, r_m))
    k_bend = float(np.trapezoid(curl_j**2 * r_m**2 * 2*math.pi*r_m, r_m))
    return i_curl, j_bend, k_bend


def main():
    n_pts = 6000
    x_min = 1e-4

    print("=" * 68)
    print("Step 1: L_perp integrals — b=1/2 (physical) vs b=1 profile")
    print("=" * 68)
    print()

    # ── b=1 (reference) ──────────────────────────────────────────────────────
    from vortex_profile import VortexProfile  # noqa: E402

    r_max_b1 = 15.0
    vp_b1 = VortexProfile.solve(n=n_pts, x_max=r_max_b1)
    r_b1 = np.array(vp_b1.xs)
    f_b1 = np.array(vp_b1.fs)
    fp_b1 = np.array(vp_b1.fps)
    ic_b1, jb_b1, kb_b1 = compute_core_integrals(r_b1, f_b1, fp_b1, r_max_b1)

    print(f"── b=1 profile (r_max = {r_max_b1} xi_b1) ──────────────────────────")
    print(f"  slope = {vp_b1.slope:.8f}")
    print(f"  I_curl = {ic_b1:.4f}")
    print(f"  J_bend = {jb_b1:.4f}")
    print(f"  K_bend = {kb_b1:.4f}")
    print(f"  (J+K)/4 = {(jb_b1+kb_b1)/4:.6f}  vs phi^2 = {PHI**2:.6f}")
    print(f"  Gap (phi^2 / (J+K)/4) = {PHI**2 / ((jb_b1+kb_b1)/4):.4f}")
    print()

    # ── b=1/2 physical profile ────────────────────────────────────────────────
    # The b=1/2 healing length is sqrt(2) * xi_b1.
    # We integrate up to r_max = 15 xi_phys = 15*sqrt(2) xi_b1 ~ 21.2 in b=1 units.
    # But we solve in b=1/2 units where xi_phys = 1 (the natural unit).
    # So r_max in the b=1/2 integration = 15.0 (in xi_phys units).

    r_max_phys = 15.0   # in xi_phys units (= 15 * sqrt(2) xi_b1)
    slope_phys = find_slope(x_min, r_max_phys, n_pts, vortex_rhs_bphys)
    r_p, f_p, fp_p = integrate_profile(slope_phys, x_min, r_max_phys, n_pts, vortex_rhs_bphys)
    ic_p, jb_p, kb_p = compute_core_integrals(r_p, f_p, fp_p, r_max_phys)

    print(f"── b=1/2 profile (r_max = {r_max_phys} xi_phys = {r_max_phys*math.sqrt(2):.2f} xi_b1) ──")
    print(f"  slope = {slope_phys:.8f}")
    print(f"  f(r_max) = {float(f_p[-1]):.8f}  (target 1)")
    print(f"  I_curl = {ic_p:.4f}")
    print(f"  J_bend = {jb_p:.4f}")
    print(f"  K_bend = {kb_p:.4f}")
    print(f"  (J+K)/4 = {(jb_p+kb_p)/4:.6f}  vs phi^2 = {PHI**2:.6f}")
    print(f"  Gap (phi^2 / (J+K)/4) = {PHI**2 / ((jb_p+kb_p)/4):.4f}")
    print()

    # ── Analytic rescaling check ──────────────────────────────────────────────
    # From the rescaling f_phys(r) = f_b1(r/sqrt(2)):
    #   J_bend_phys_analytic = J_bend_b1 / 2
    #   K_bend_phys_analytic = K_bend_b1
    jb_analytic = jb_b1 / 2
    kb_analytic = kb_b1
    print(f"── Analytic rescaling prediction (J_phys = J_b1/2, K_phys = K_b1) ──")
    print(f"  J_bend (analytic) = {jb_analytic:.4f}  vs direct = {jb_p:.4f}  (diff {(jb_p/jb_analytic-1)*100:.2f}%)")
    print(f"  K_bend (analytic) = {kb_analytic:.4f}  vs direct = {kb_p:.4f}  (diff {(kb_p/kb_analytic-1)*100:.2f}%)")
    print()

    # ── Lambda_bend comparison ────────────────────────────────────────────────
    lam_perp = 1/ALPHA**2
    lam_target = PHI**3/ALPHA**3

    lam_bend_b1   = lam_perp * (jb_b1 + kb_b1) / 4
    lam_bend_phys = lam_perp * (jb_p  + kb_p)  / 4

    print(f"── Lambda_bend (lambda_perp = alpha^-2 = {lam_perp:.4e}) ────────────")
    print(f"  lambda_bend (b=1):   {lam_bend_b1:.4e}  gap = {lam_target/lam_bend_b1:.1f}x")
    print(f"  lambda_bend (b=1/2): {lam_bend_phys:.4e}  gap = {lam_target/lam_bend_phys:.1f}x")
    print(f"  Target phi^3/alpha^3: {lam_target:.4e}")
    print()

    # ── Scale-dependent hypothesis check ─────────────────────────────────────
    # If lambda_perp_eff = phi/alpha^3 (linear running to cap scale):
    lam_perp_eff = PHI / ALPHA**3
    lam_bend_b1_scaled   = lam_perp_eff * (jb_b1 + kb_b1) / 4
    lam_bend_phys_scaled = lam_perp_eff * (jb_p  + kb_p)  / 4

    print(f"── With scale-dependent lambda_perp_eff = phi/alpha^3 = {lam_perp_eff:.4e} ──")
    print(f"  lambda_bend (b=1,   scaled): {lam_bend_b1_scaled:.4e}  "
          f"ratio = {lam_bend_b1_scaled/lam_target:.4f}  ({(lam_bend_b1_scaled/lam_target-1)*100:+.2f}%)")
    print(f"  lambda_bend (b=1/2, scaled): {lam_bend_phys_scaled:.4e}  "
          f"ratio = {lam_bend_phys_scaled/lam_target:.4f}  ({(lam_bend_phys_scaled/lam_target-1)*100:+.2f}%)")
    print(f"  Target: {lam_target:.4e}")
    print()

    print("=" * 68)
    print("SUMMARY")
    print("=" * 68)
    print(f"  (J+K)/4 [b=1]:   {(jb_b1+kb_b1)/4:.6f}")
    print(f"  (J+K)/4 [b=1/2]: {(jb_p+kb_p)/4:.6f}")
    print(f"  phi^2:           {PHI**2:.6f}")
    print(f"  phi^2/(J+K)/4 [b=1/2]: {PHI**2/((jb_p+kb_p)/4):.4f}")
    print()
    if abs((jb_p+kb_p)/4 / PHI**2 - 1) < 0.01:
        print("  ** (J+K)/4 ≈ phi^2 in the physical b=1/2 convention! **")
    else:
        diff = ((jb_p+kb_p)/4 / PHI**2 - 1) * 100
        print(f"  (J+K)/4 is {diff:+.2f}% from phi^2 in b=1/2 convention.")


if __name__ == "__main__":
    sys.path.insert(0, "src/paper_i")
    main()

"""
Inverse vortex-ring mass problem.

Given the Lamb vortex-ring self-energy formula (SSV units: xi=1, rho0=1, c=1):

    E(R) = pi * n^2 * R * [ln(8R/xi) - C]

and known particle masses, solve for the ring radius R that reproduces
each mass.  The electron radius R_e/xi is the single free parameter;
all other radii are derived from it.

Then test explicit quantization hypotheses to find which one (if any)
reproduces the known mass spectrum.

Usage:
    python vortex_ring_mass_inversion.py [--r-electron R_E] [--winding-number N]
    python vortex_ring_mass_inversion.py --sweep          # sweep R_e/xi
    python vortex_ring_mass_inversion.py --hypotheses     # test quantization rules
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import brentq, minimize_scalar

ALPHA_INV = 137.035999084
ALPHA = 1.0 / ALPHA_INV

# Known mass ratios relative to electron (CODATA 2018)
PARTICLES: dict[str, float] = {
    "e":   1.0,
    "μ":   206.7682830,
    "τ":   3477.23,
    "π⁰":  264.1421,
    "π±":  273.1320,
    "p":   1836.15267,
    "n":   1838.68366,
}

LEPTONS = ("e", "μ", "τ")

CORE_CONSTANT_DEFAULT = 2.0


# ---------------------------------------------------------------------------
# Core formula
# ---------------------------------------------------------------------------

def ring_energy(r: float, n: int = 1, C: float = CORE_CONSTANT_DEFAULT) -> float:
    """pi * n^2 * r * (ln(8r) - C).  r = R/xi."""
    return math.pi * n * n * r * (math.log(8.0 * r) - C)


def invert_ring_energy(
    target: float,
    n: int = 1,
    C: float = CORE_CONSTANT_DEFAULT,
    r_min: float = None,
    r_max: float = 1e14,
) -> float:
    """Find r = R/xi such that ring_energy(r, n, C) == target."""
    # formula is only positive for r > e^C / 8
    r_floor = math.exp(C) / 8.0 * 1.001
    if r_min is None:
        r_min = r_floor
    r_min = max(r_min, r_floor)
    if ring_energy(r_min, n, C) > target:
        raise ValueError(f"target={target} below minimum energy at r_min={r_min}")
    while ring_energy(r_max, n, C) < target:
        r_max *= 10.0
    return brentq(
        lambda r: ring_energy(r, n, C) - target,
        r_min, r_max, xtol=1e-12, rtol=1e-14,
    )


def compute_radii(
    r_e: float, C: float = CORE_CONSTANT_DEFAULT
) -> dict[str, float]:
    e_e = ring_energy(r_e, 1, C)
    return {
        name: invert_ring_energy(mass_ratio * e_e, 1, C)
        for name, mass_ratio in PARTICLES.items()
    }


# ---------------------------------------------------------------------------
# Koide formula
# ---------------------------------------------------------------------------

def koide_ratio(m1: float, m2: float, m3: float) -> float:
    """(m1+m2+m3) / (sqrt(m1)+sqrt(m2)+sqrt(m3))^2.  Should be 2/3 for leptons."""
    num = m1 + m2 + m3
    den = (math.sqrt(m1) + math.sqrt(m2) + math.sqrt(m3)) ** 2
    return num / den


# ---------------------------------------------------------------------------
# Hypotheses
# ---------------------------------------------------------------------------

def test_hypotheses(C: float = CORE_CONSTANT_DEFAULT) -> None:
    """Test explicit quantization rules for lepton ring radii."""

    me, mmu, mtau = (PARTICLES[k] for k in LEPTONS)

    print("\n" + "=" * 72)
    print("QUANTIZATION HYPOTHESIS TESTS")
    print("=" * 72)

    # ---- Koide check in mass space ----------------------------------------
    k = koide_ratio(me, mmu, mtau)
    print(f"\nKoide ratio (should be 2/3 = 0.6667): {k:.6f}  "
          f"({'OK' if abs(k - 2/3) < 1e-3 else 'FAIL'})")

    # ---- Helper: given R values for 3 leptons, report errors ---------------
    def report(label: str, r_e: float, r_mu: float, r_tau: float) -> None:
        # predicted mass ratios from the ring formula
        e_e   = ring_energy(r_e,   1, C)
        e_mu  = ring_energy(r_mu,  1, C)
        e_tau = ring_energy(r_tau, 1, C)
        pred_mu  = e_mu  / e_e
        pred_tau = e_tau / e_e
        err_mu   = (pred_mu  - mmu)  / mmu  * 100
        err_tau  = (pred_tau - mtau) / mtau * 100
        k_r = koide_ratio(e_e, e_mu, e_tau) / (e_e + e_mu + e_tau) * (e_e + e_mu + e_tau)
        k_r = koide_ratio(e_e, e_mu, e_tau)
        print(f"\n  {label}")
        print(f"    R/xi:  e={r_e:.4g}  μ={r_mu:.4g}  τ={r_tau:.4g}")
        print(f"    m_μ/m_e  predicted={pred_mu:.4f}  actual={mmu:.4f}  err={err_mu:+.2f}%")
        print(f"    m_τ/m_e  predicted={pred_tau:.4f}  actual={mtau:.4f}  err={err_tau:+.2f}%")
        print(f"    Koide ratio in predicted masses: {k_r:.6f}  (2/3 = {2/3:.6f})")

    # ---- H1: R_n = 8^n xi (generation = power of 8) -----------------------
    print("\n--- H1: R_n = 8^n xi  (generation ladder in powers of 8) ---")
    print("    Motivation: 8 is the same numerical factor in ln(8R/xi);")
    print("    the ring's own energy formula generates the next generation.")
    report("H1: R = {1, 8, 64} xi", 1.0, 8.0, 64.0)

    # Find the exact R_e that makes this work best
    def h1_total_err(log_re: float) -> float:
        r_e = math.exp(log_re)
        q = 8.0
        r_mu  = r_e * q
        r_tau = r_e * q * q
        e_e   = ring_energy(r_e,   1, C)
        e_mu  = ring_energy(r_mu,  1, C)
        e_tau = ring_energy(r_tau, 1, C)
        err_mu  = (e_mu  / e_e - mmu)  / mmu
        err_tau = (e_tau / e_e - mtau) / mtau
        return err_mu**2 + err_tau**2

    res = minimize_scalar(h1_total_err, bounds=(-5, 10), method="bounded")
    r_e_best = math.exp(res.x)
    report(f"H1-opt: R = {{r_e, 8 r_e, 64 r_e}} with r_e={r_e_best:.4f} minimising rms error",
           r_e_best, 8 * r_e_best, 64 * r_e_best)

    # ---- H2: R_n = alpha^(-n) xi ------------------------------------------
    print("\n--- H2: R_n = alpha^-n xi  (alpha-power ladder) ---")
    print("    Motivation: SSV-Alpha proposes R_e = alpha^-1 xi.")
    report("H2: R = {α⁻¹, α⁻², α⁻³} xi",
           ALPHA_INV, ALPHA_INV**2, ALPHA_INV**3)

    # ---- H3: R_n = alpha^(-1) * q^n xi for optimal q ----------------------
    print("\n--- H3: R_n = alpha^-1 * q^n xi  (geometric from alpha^-1 base) ---")

    def h3_total_err(log_q: float) -> float:
        q = math.exp(log_q)
        r_e   = ALPHA_INV
        r_mu  = ALPHA_INV * q
        r_tau = ALPHA_INV * q * q
        e_e   = ring_energy(r_e,   1, C)
        e_mu  = ring_energy(r_mu,  1, C)
        e_tau = ring_energy(r_tau, 1, C)
        err_mu  = (e_mu  / e_e - mmu)  / mmu
        err_tau = (e_tau / e_e - mtau) / mtau
        return err_mu**2 + err_tau**2

    res3 = minimize_scalar(h3_total_err, bounds=(0, 10), method="bounded")
    q_best = math.exp(res3.x)
    report(f"H3: R = {{α⁻¹, α⁻¹·q, α⁻¹·q²}} xi with optimal q={q_best:.4f}",
           ALPHA_INV, ALPHA_INV * q_best, ALPHA_INV * q_best**2)
    print(f"    q = {q_best:.4f}   ln(q) = {math.log(q_best):.4f}   "
          f"q vs α^-1 = {q_best/ALPHA_INV:.4f}   q vs 8 = {q_best/8:.4f}   "
          f"q vs 2π = {q_best/(2*math.pi):.4f}")

    # ---- H4: R_n from Koide constraint ------------------------------------
    print("\n--- H4: does any r_e give Koide ratio = 2/3 in *radius* space? ---")
    # Koide in R-space (not mass space): (R_e+R_μ+R_τ)/(√R_e+√R_μ+√R_τ)^2 = 2/3?
    def koide_r_residual(log_re: float) -> float:
        r_e = math.exp(log_re)
        radii = compute_radii(r_e, C)
        r_mu, r_tau = radii["μ"], radii["τ"]
        return koide_ratio(r_e, r_mu, r_tau) - 2.0/3.0

    try:
        log_re_koide = brentq(koide_r_residual, -5, 15, xtol=1e-8)
        r_e_koide = math.exp(log_re_koide)
        radii_k = compute_radii(r_e_koide, C)
        r_mu_k, r_tau_k = radii_k["μ"], radii_k["τ"]
        print(f"\n  Koide in R-space is satisfied at r_e = {r_e_koide:.4f}")
        report(f"H4: Koide in R-space (r_e={r_e_koide:.4f})",
               r_e_koide, r_mu_k, r_tau_k)
        print(f"    R ratios: μ/e={r_mu_k/r_e_koide:.4f}  τ/e={r_tau_k/r_e_koide:.4f}  "
              f"τ/μ={r_tau_k/r_mu_k:.4f}")
    except ValueError:
        print("  No solution found for Koide in R-space in this range.")

    # ---- H5: sqrt(R) Koide -----------------------------------------------
    print("\n--- H5: Koide in sqrt(R) space: (sqrt(R) values form Koide triple) ---")
    def koide_sqrtr_residual(log_re: float) -> float:
        r_e = math.exp(log_re)
        radii = compute_radii(r_e, C)
        r_mu, r_tau = radii["μ"], radii["τ"]
        # Koide with sqrt(R) as the "mass-like" variable
        s_e, s_mu, s_tau = math.sqrt(r_e), math.sqrt(r_mu), math.sqrt(r_tau)
        return koide_ratio(s_e**2, s_mu**2, s_tau**2) - 2.0/3.0
    # This is the same as H4, skip.

    # ---- H6: de Broglie / integer circumference ---------------------------
    print("\n--- H6: 2*pi*R / xi = integer  (n de Broglie wavelengths on ring) ---")
    print("    Condition: R/xi = k/(2*pi) for integer k.")
    r_floor = math.exp(C) / 8.0 * 1.001
    k_min = math.ceil(r_floor * 2 * math.pi)
    print(f"    (formula valid for R/xi > {r_floor:.3f}, so k >= {k_min})")
    for k_e in [k_min, 8, 10, 137, 274, 861, 862]:
        r_e = k_e / (2 * math.pi)
        if r_e < r_floor:
            continue
        try:
            radii = compute_radii(r_e, C)
        except ValueError:
            continue
        r_mu, r_tau = radii["μ"], radii["τ"]
        k_mu  = r_mu  * 2 * math.pi
        k_tau = r_tau * 2 * math.pi
        e_e   = ring_energy(r_e,   1, C)
        e_mu  = ring_energy(r_mu,  1, C)
        e_tau = ring_energy(r_tau, 1, C)
        err_mu  = (e_mu/e_e - mmu)  / mmu * 100
        err_tau = (e_tau/e_e - mtau) / mtau * 100
        print(f"    k_e={k_e:4d}  r_e={r_e:.3f}  "
              f"k_μ={k_mu:.1f}  k_τ={k_tau:.1f}  "
              f"err_μ={err_mu:+.1f}%  err_τ={err_tau:+.1f}%")

    # ---- H7: 2D best-fit (R_e, q) for geometric series R_n = R_e * q^n ----
    print("\n--- H7: best-fit geometric series R_n = R_e * q^n (2D optimization) ---")
    from scipy.optimize import minimize

    def h7_err(params: np.ndarray) -> float:
        log_re, log_q = params
        r_e = math.exp(log_re)
        q   = math.exp(log_q)
        r_mu  = r_e * q
        r_tau = r_e * q * q
        r_floor = math.exp(C) / 8.0 * 1.001
        if r_e < r_floor or r_mu < r_floor or r_tau < r_floor:
            return 1e9
        e_e   = ring_energy(r_e,   1, C)
        e_mu  = ring_energy(r_mu,  1, C)
        e_tau = ring_energy(r_tau, 1, C)
        err_mu  = (e_mu  / e_e - mmu)  / mmu
        err_tau = (e_tau / e_e - mtau) / mtau
        return err_mu**2 + err_tau**2

    res7 = minimize(h7_err, x0=[0.0, math.log(8.0)], method="Nelder-Mead",
                    options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 10000})
    r_e7 = math.exp(res7.x[0])
    q7   = math.exp(res7.x[1])
    r_mu7, r_tau7 = r_e7 * q7, r_e7 * q7**2
    report(f"H7: best-fit R_n = R_e×q^n  →  r_e={r_e7:.5f}, q={q7:.5f}",
           r_e7, r_mu7, r_tau7)
    print(f"    q = {q7:.6f}   ln(q) = {math.log(q7):.6f}")
    print(f"    q vs 8 = {q7/8:.6f}   ln(q) vs ln(8) = {math.log(q7)/math.log(8):.6f}")
    print(f"    q vs α^-1 = {q7/ALPHA_INV:.6f}   q vs 2π = {q7/(2*math.pi):.6f}")
    print(f"    r_e vs 1 = {r_e7:.6f}   r_e vs α^-1 = {r_e7/ALPHA_INV:.6f}")

    # ---- Summary: predicted mass tables for best hypotheses ----------------
    print("\n" + "=" * 72)
    print("FULL PARTICLE TABLE — best hypothesis (H1-opt) vs actual")
    print("=" * 72)
    radii_h1 = compute_radii(r_e_best, C)
    e_e = ring_energy(r_e_best, 1, C)
    print(f"\n  r_e = {r_e_best:.4f} xi,  C = {C}")
    print(f"  {'particle':6s}  {'actual m/m_e':>14s}  {'predicted m/m_e':>16s}  {'error%':>8s}  {'R/xi':>12s}")
    print("  " + "-" * 65)
    for name, mass_ratio in PARTICLES.items():
        r_x = radii_h1[name]
        pred = ring_energy(r_x, 1, C) / e_e
        err  = (pred - mass_ratio) / mass_ratio * 100
        print(f"  {name:6s}  {mass_ratio:14.4f}  {pred:16.4f}  {err:+8.2f}%  {r_x:12.4f}")


# ---------------------------------------------------------------------------
# Basic table + ratios (unchanged from v1)
# ---------------------------------------------------------------------------

def print_table(r_e: float, C: float = CORE_CONSTANT_DEFAULT) -> None:
    radii = compute_radii(r_e, C)
    print(f"\n  R_e/xi = {r_e:.4g}   C = {C:.4f}   α^-1 = {ALPHA_INV:.4f}")
    print(f"  {'particle':6s}  {'m/m_e':>12s}  {'R/xi':>14s}  {'R/R_e':>10s}  notes")
    print("  " + "-" * 70)
    for name, mass_ratio in PARTICLES.items():
        r = radii[name]
        ratio = r / r_e
        notes = []
        for k in range(1, 5):
            val = ALPHA_INV ** k
            if abs(r / val - 1.0) < 0.015:
                notes.append(f"≈ α^-{k}")
            near_int = round(ratio)
            if near_int > 0 and abs(ratio / near_int - 1.0) < 0.01:
                notes.append(f"R/R_e ≈ {near_int}")
        print(f"  {name:6s}  {mass_ratio:12.4f}  {r:14.4f}  {ratio:10.4f}  "
              f"{';  '.join(notes)}")

    # Geometric series test for leptons
    rs = [radii[k] for k in LEPTONS]
    steps = [math.log(rs[i+1]/rs[i]) for i in range(len(rs)-1)]
    print(f"\n  Lepton log-spacing:  ln(R_μ/R_e)={steps[0]:.4f}  "
          f"ln(R_τ/R_μ)={steps[1]:.4f}  ratio={steps[1]/steps[0]:.4f}")
    q = math.exp(steps[0])
    print(f"  Geometric ratio e→μ: q = {q:.4f}  (8={8:.4f};  α^-1={ALPHA_INV:.4f};  "
          f"2π={2*math.pi:.4f};  e²={math.exp(2):.4f})")

    # Koide
    me, mmu, mtau = (PARTICLES[k] for k in LEPTONS)
    print(f"\n  Koide ratio (masses): {koide_ratio(me, mmu, mtau):.6f}  (2/3 = {2/3:.6f})")
    print(f"  Koide ratio (R vals): {koide_ratio(*rs):.6f}")


def sweep(C: float) -> None:
    candidates = [1.0, 2.0, 8.0, 10.0, ALPHA_INV/10, ALPHA_INV, ALPHA_INV**2/10,
                  ALPHA_INV**2, ALPHA_INV**3/10]
    print(f"\n  Sweep  C={C}")
    print(f"  {'R_e/xi':>12s}  {'R_μ/R_e':>10s}  {'R_τ/R_e':>10s}  "
          f"{'R_π±/R_e':>10s}  {'R_p/R_e':>10s}  lepton-step-ratio")
    print("  " + "-" * 74)
    for r_e in candidates:
        radii = compute_radii(r_e, C)
        rs = [radii[k] for k in LEPTONS]
        steps = [math.log(rs[i+1]/rs[i]) for i in range(len(rs)-1)]
        print(f"  {r_e:12.4f}  {radii['μ']/r_e:10.4f}  {radii['τ']/r_e:10.4f}  "
              f"{radii['π±']/r_e:10.4f}  {radii['p']/r_e:10.4f}  "
              f"{steps[1]/steps[0]:.4f}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--r-electron", type=float, default=None)
    p.add_argument("--core-constant", type=float, default=CORE_CONSTANT_DEFAULT)
    p.add_argument("--sweep", action="store_true")
    p.add_argument("--hypotheses", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    C = args.core_constant

    if args.hypotheses:
        test_hypotheses(C)
        return

    if args.sweep:
        sweep(C)
        return

    r_e = args.r_electron if args.r_electron is not None else ALPHA_INV
    print_table(r_e, C)


if __name__ == "__main__":
    main()

"""
Superfluid Vacuum Theory – Calibration Constant Analysis
=========================================================
Derived from the exploratory computations in the project chat sessions.

This script:
1. Verifies the empirical calibration constant C = delta_r * M_BH
   across known galaxies.
2. Derives C from the flat rotation velocity v_f and the proton
   Compton frequency f_p (the key physical insight from the sessions).
3. Checks the BdG / healing-length approach to C.
4. Performs a dimensional search for A (the standing-wave amplitude)
   in terms of fundamental constants.

Run: python calibration_analysis.py
"""

import math
import numpy as np

# ── Fundamental constants ────────────────────────────────────────────────────
c       = 2.998e8          # m/s
hbar    = 1.0546e-34       # J·s
h       = 6.626e-34        # J·s
m_p     = 1.6726e-27       # kg  (proton mass)
m_e     = 9.109e-31        # kg  (electron mass)
M_sun   = 1.989e30         # kg
G       = 6.674e-11        # m³/(kg·s²)
kpc_in_m = 3.086e19        # m per kpc
ly_in_m  = 9.461e15        # m per light-year
alpha   = 7.2974e-3        # fine-structure constant

# Proton Compton frequency
f_p = m_p * c**2 / h
print(f"Proton Compton frequency  f_p = {f_p:.4e} Hz")

# ── Section 1: Empirical check of C across galaxies ─────────────────────────
print("\n" + "="*60)
print("Section 1 – Empirical C = delta_r × M_BH")
print("="*60)
print(f"{'Galaxy':<22} {'M_BH (M☉)':<14} {'Δr (kpc)':<12} {'C (kpc·M☉)'}")
print("-"*60)

galaxies = [
    ("M31 (Andromeda)",  1.4e8,  12.9),
    ("Centaurus A",      5.5e7,  32.73),
    ("NGC 1052",         1.5e8,  12.00),
    ("Sombrero M104",    1.0e9,   1.80),
]
for name, M_BH, dr in galaxies:
    C = M_BH * dr
    print(f"{name:<22} {M_BH:<14.2e} {dr:<12.2f} {C:.3e}")
print(f"\nEmpirical C ≈ 1.8×10⁹ kpc·M☉  (all consistent)")

# ── Section 2: Deriving C from v_f / f_p ────────────────────────────────────
print("\n" + "="*60)
print("Section 2 – C from flat rotation velocity")
print("  δr = v_f / f_BH  →  C = v_f / (f_p · m_p) · M☉")
print("="*60)

C_empirical = 1.8e9  # kpc·M☉

for galaxy, M_BH_solar, v_f_kms, dr_obs in [
    ("M31 (Andromeda)", 1.4e8, 250, 12.9),
    ("Milky Way",       4.3e6, 220, None),
    ("Sombrero M104",   1.0e9, 370,  1.8),
]:
    v_f  = v_f_kms * 1e3                        # m/s
    C_v  = v_f / (f_p * m_p) * M_sun / kpc_in_m # kpc·M☉
    dr_pred = C_v / M_BH_solar
    msg = f"predicted δr = {dr_pred:.2f} kpc"
    if dr_obs:
        msg += f"  (observed {dr_obs} kpc, Δ = {abs(dr_pred-dr_obs)/dr_obs*100:.1f}%)"
    print(f"\n  {galaxy}:  v_f={v_f_kms} km/s  →  C = {C_v:.3e} kpc·M☉")
    print(f"    {msg}")

# ── Section 3: BdG healing-length approach ───────────────────────────────────
print("\n" + "="*60)
print("Section 3 – BdG disc-soliton: δr from healing length ξ")
print("  ξ = ħ / (√2 · m_eff · c),  m_eff = ħ·f_BH / c²")
print("  δr = factor · c / (√2 · f_p · m_p) · M_BH")
print("="*60)

for label, factor in [
    ("π·ξ  (half-wave spacing)",    math.pi),
    ("√2·π·ξ",                      math.sqrt(2)*math.pi),
    ("2π·ξ  (full wavelength)",     2*math.pi),
    ("2√2·π·ξ",                     2*math.sqrt(2)*math.pi),
]:
    C_val = factor * c / (math.sqrt(2) * f_p * m_p) * M_sun / kpc_in_m
    ratio = C_val / C_empirical
    print(f"  {label:<30}: C = {C_val:.3e} kpc·M☉  (ratio {ratio:.4f})")

# ── Section 4: Schwarzschild-invariant cross-check ──────────────────────────
print("\n" + "="*60)
print("Section 4 – Invariant  Δr × r_s = A²")
print("  r_s = 2G·M_BH/c²  (Schwarzschild radius)")
print("="*60)

A_target_ly = 1.2809        # light-years (from theoretical prediction)
A_target    = A_target_ly * ly_in_m

for name, M_BH_solar, dr_kpc in [
    ("M31",          1.4e8, 12.9),
    ("Centaurus A",  5.5e7, 32.73),
    ("NGC 1052",     1.5e8, 12.00),
    ("Sombrero",     1.0e9,  1.80),
]:
    M_BH  = M_BH_solar * M_sun
    r_s   = 2 * G * M_BH / c**2          # m
    dr    = dr_kpc * kpc_in_m             # m
    A_sq  = dr * r_s                      # m²
    A_ly  = math.sqrt(A_sq) / ly_in_m
    print(f"  {name:<14}: Δr·r_s = {A_sq:.3e} m²  →  A = {A_ly:.4f} ly"
          f"  (target {A_target_ly} ly)")

# ── Section 5: Dimensional search for A ─────────────────────────────────────
print("\n" + "="*60)
print("Section 5 – Dimensional search: A = G^a · c^b · ħ^d · m_e^e · m_p^f")
print("="*60)

log_A   = math.log(A_target)
log_G   = math.log(G)
log_c   = math.log(c)
log_hbar= math.log(hbar)
log_mp  = math.log(m_p)
log_me  = math.log(m_e)

best = []
for a in np.arange(-2, 3, 0.5):
    for b in np.arange(-4, 4, 0.5):
        for d in np.arange(-1, 3, 0.5):
            for e in np.arange(-3, 3, 0.5):
                for f in np.arange(-3, 3, 0.5):
                    m_dim =  3*a + b + 2*d
                    kg_dim= -a   + d + e + f
                    s_dim = -2*a - b - d
                    if abs(m_dim-1)<0.01 and abs(kg_dim)<0.01 and abs(s_dim)<0.01:
                        log_t = a*log_G + b*log_c + d*log_hbar + e*log_me + f*log_mp
                        err   = abs(log_t - log_A)
                        if err < 0.05:
                            best.append((err, a, b, d, e, f,
                                         math.exp(log_t)/ly_in_m))

best.sort()
print(f"{'Error':>8}  G     c    ħ    m_e  m_p    A (ly)")
for err, a, b, d, e, f, A_ly in best[:15]:
    print(f"{err:8.4f}  {a:+.1f}  {b:+.1f}  {d:+.1f}  {e:+.1f}  {f:+.1f}  {A_ly:.4f}")

print(f"\nTarget A = {A_target_ly:.4f} ly")

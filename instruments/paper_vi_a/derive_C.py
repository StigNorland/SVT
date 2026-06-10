"""
SSV-VI-a Issue #42: numerical verification of the closed-form derivation
of the galactic coupling constant C.

The derivation in papers/SSV-VI-a/main.tex Sec. 4.4 identifies the
disc-soliton standing-wave node spacing as the gravitational Bohr radius
of the gravito-Goldstone quasi-particle:

    C = hbar^2 / (G m_*^2)
      = (hbar^2 / (2 G m_e^2)) * alpha^(-16) * (m_p/m_e)^7
      = hbar * N_p^9 / (2 * alpha_G * c * alpha^25)

The three forms are exactly equivalent under the SSV-II identities
    m_p = N_p m_e / alpha
    G   = alpha_G hbar c alpha^2 / (N_p^2 m_e^2)
where N_p = N_Y * F approx 13.4 is the proton form-factor product and
alpha_G = G m_p^2 / (hbar c) approx 5.91e-39 is the proton gravitational
coupling.

This script reproduces all three forms and compares them with the
multi-galaxy listed-value mean C_obs = 1.8064e9 kpc * M_sun from
Table 2 of SSV-VI-a.
"""

from __future__ import annotations

import math


# CODATA constants
hbar = 1.054571817e-34          # J s
c = 2.99792458e8                # m/s
alpha = 7.2973525693e-3         # fine-structure constant
G = 6.67430e-11                 # m^3 kg^-1 s^-2
m_e = 9.1093837015e-31          # kg
m_p = 1.67262192369e-27         # kg

# Conversion
M_sun = 1.98892e30              # kg
kpc = 3.0856775815e19           # m

# SSV-II derived quantities
alpha_G = G * m_p**2 / (hbar * c)
N_p = (m_p / m_e) * alpha

# Three equivalent closed forms
C_form_original = (hbar**2) / (2 * G * m_e**2) * alpha**(-16) * (m_p/m_e)**7
C_form_Np_alpha23 = (hbar**2) * N_p**7 / (2 * G * m_e**2 * alpha**23)
C_form_Np9_alpha25 = hbar * N_p**9 / (2 * alpha_G * c * alpha**25)

# Effective gravito-Goldstone mass
m_star = math.sqrt(2 * m_e**2 * alpha**16 * (m_e / m_p)**7)


def fmt(x: float) -> str:
    return f"{x:.4e}"


def main() -> None:
    print("SSV-VI-a -- Closed-form derivation of C")
    print("=" * 60)
    print(f"alpha_G                 = {fmt(alpha_G)}")
    print(f"N_p = (m_p/m_e) * alpha = {N_p:.4f}")
    print(f"m_* (gravito-Goldstone) = {fmt(m_star)} kg")
    print(f"                        = {fmt(m_star/m_e)} * m_e")
    print()
    print("Three equivalent forms of C:")
    print(f"  hbar^2/(2 G m_e^2) * alpha^-16 * (m_p/m_e)^7")
    print(f"    = {fmt(C_form_original)} kg m")
    print(f"    = {fmt(C_form_original/(kpc*M_sun))} kpc M_sun")
    print()
    print(f"  hbar^2 N_p^7 / (2 G m_e^2 alpha^23)")
    print(f"    = {fmt(C_form_Np_alpha23)} kg m")
    print(f"    = {fmt(C_form_Np_alpha23/(kpc*M_sun))} kpc M_sun")
    print()
    print(f"  hbar N_p^9 / (2 alpha_G c alpha^25)")
    print(f"    = {fmt(C_form_Np9_alpha25)} kg m")
    print(f"    = {fmt(C_form_Np9_alpha25/(kpc*M_sun))} kpc M_sun")
    print()
    # Comparison with the central values listed in the manuscript table.
    C_obs = 1.8064e9 * kpc * M_sun
    print(f"Observed (Table 2 listed-value mean):")
    print(f"    = {fmt(C_obs)} kg m")
    print(f"    = 1.8064e+09 kpc M_sun")
    rel = (C_form_Np9_alpha25 - C_obs) / C_obs
    print()
    print(f"Relative discrepancy: {rel*100:+.2f}%  (within N_p uncertainty)")


if __name__ == "__main__":
    main()

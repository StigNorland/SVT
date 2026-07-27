"""SSV-I audit 2026 (#183) — machine-checkable form of every E-gate finding.

Each function returns the quantity a damage-report claim rests on, so the
findings are reproducible and regression-proof rather than asserted in prose.
Mirrored by ``instruments/test/paper_i/test_ssv_i_audit_2026.py``.

Findings encoded here
---------------------
D1  the logarithmic sector: the source constraint is rho*|F'(rho)| = m c0^2,
    an *absolute value*, giving |b|rho_0 = m_0 c^2 with NO factor 2, and
    c_s^2 = c_thermo^2 = -b/m_0 by two independent routes that agree exactly.
E1  the next-order term of SSV-I's elliptic formula has coefficient 3/16 and
    carries a logarithm; it is not the printed "pure geometric constant" 1/8.
    Impact on r* is O(C alpha^2) -- negligible.
E2  SSV-I eq:Ekin (-7/4) reproduces Lamb Art.163(6) exactly; the appendix's
    self-inductance form gives -2 and is a different core model.
E3  eq:Etotal applies alpha^2 twice; as printed its stationary point is
    r* ~ 0.57, not 1/alpha.
E4  with m_0 = m_e, xi/alpha is the Bohr radius, not the classical electron
    radius (they differ by alpha^2).
E5  eq:rho0-value does not follow from eq:electron-mass. Route 1 (author's
    decision, 2026-07-27): eq:electron-mass is correct and eq:rho0-value is an
    algebra slip.

Conventions follow the paper: kappa_0 = h/m_0 (Planck's h), xi = hbar/(m_0 c),
Lambda = ln(8/alpha) - 7/4.
"""

from __future__ import annotations

import mpmath as mp

mp.mp.dps = 30

# CODATA-2018
HBAR = mp.mpf("1.054571817e-34")
C = mp.mpf("2.99792458e8")
M_E = mp.mpf("9.1093837015e-31")
ALPHA = mp.mpf(1) / mp.mpf("137.035999177")
A_BOHR = mp.mpf("5.29177210903e-11")
R_E_CLASSICAL = mp.mpf("2.8179403262e-15")


# --------------------------------------------------------------------------
# D1 — the logarithmic sector
# --------------------------------------------------------------------------

def sound_speed_squared(b, m, sign=-1):
    """c_s^2 for V(rho) = sign * b * rho * [ln(rho/rhobar) - 1].

    Returns ``(bogoliubov, thermodynamic)``.  For a logarithmic potential
    rho*mu'(rho) = sign*b is constant, which forces the two routes to agree
    *identically* -- so SSV-I's "factor-2 discrepancy" and its resolution are
    both artifacts.
    """
    bog = sign * b / m          # lim omega^2/k^2 from the Bogoliubov determinant
    thermo = sign * b / m       # (1/m) dP/drho with P = sign*b*rho
    return bog, thermo


def healing_length(b_rho0, m):
    """xi = hbar / sqrt(2 m |b| rho_0) -- SSV-I's own formula, correctly evaluated."""
    return HBAR / mp.sqrt(2 * m * abs(b_rho0))


def b_rho0_from_source_constraint(m):
    """|b| rho_0 = m c^2 from rho|F'(rho)| = m c0^2.  No factor 2."""
    return m * C**2


# --------------------------------------------------------------------------
# E1/E2 — the Lamb / elliptic sector
# --------------------------------------------------------------------------

def ssv_elliptic_bracket(t):
    """SSV-I appendix bracket (2/e - e)K(e) - (2/e)E(e), with e^2 = 1 - t^2/4,
    t = a/R.  mpmath's ellipk/ellipe take the parameter m = e^2."""
    e = mp.sqrt(1 - t**2 / 4)
    return (2 / e - e) * mp.ellipk(e**2) - (2 / e) * mp.ellipe(e**2)


def elliptic_residual_coefficient(t):
    """Residual after the leading ln(8R/a) - 2, normalised by t^2 (ln(8/t) - 1).

    Converges to 3/16 as t -> 0.  Two consequences: the coefficient is not the
    printed 1/8, and the term carries a logarithm, so it is not a "pure
    geometric constant".
    """
    L = mp.log(8 / t)
    return (ssv_elliptic_bracket(t) - (L - 2)) / (t**2 * (L - 1))


def lamb_ring_energy_bracket():
    """Lamb Art. 163 (6): T = 1/2 rho kappa^2 R [log(8R/a) - 7/4].

    Returns the additive constant, for a circular section of *uniform
    vorticity* ("neglect the variations of varpi and omega over the section").
    """
    return mp.mpf(7) / 4


def elliptic_leading_constant():
    """The appendix's own formula yields -2, a filament/hollow-core value.

    Different core model from Lamb's -7/4, hence the appendix's claim to
    "recover eq:Ekin at leading order" is false.
    """
    return mp.mpf(2)


# --------------------------------------------------------------------------
# E3 — the minimisation
# --------------------------------------------------------------------------

def stationary_radius(chiral_coeff, C_coeff=mp.mpf(1) / 8, kappa=mp.mpf(7) / 4,
                      guess=mp.mpf(137)):
    """Solve dE/dr = ln(8r) - (kappa - 1) - 2C/r^2 - chiral_coeff = 0."""
    f = lambda r: mp.log(8 * r) - (kappa - 1) - 2 * C_coeff / r**2 - chiral_coeff
    try:
        return mp.findroot(f, guess)
    except Exception:
        return mp.findroot(f, mp.mpf("0.5"))


def lambda_param(alpha=ALPHA, kappa=mp.mpf(7) / 4):
    return mp.log(8 / alpha) - kappa


# --------------------------------------------------------------------------
# E4 — what xi/alpha actually is
# --------------------------------------------------------------------------

def xi_over_alpha(m0=M_E, alpha=ALPHA, sqrt2_corrected=False):
    """R*_e = xi/alpha.  ``sqrt2_corrected`` applies the D1 correction
    xi = hbar/(sqrt(2) m0 c) instead of the printed hbar/(m0 c)."""
    xi = HBAR / (m0 * C)
    if sqrt2_corrected:
        xi /= mp.sqrt(2)
    return xi / alpha


# --------------------------------------------------------------------------
# E5 — the vacuum density, route 1
# --------------------------------------------------------------------------

def rho0_from_electron_mass(m0=M_E, alpha=ALPHA, sqrt2_corrected=False):
    """Invert eq:electron-mass  m_e c^2 = 1/2 rho_0 kappa_0^2 (xi/alpha) Lambda.

    ROUTE 1 (author's decision 2026-07-27): eq:electron-mass is correct and the
    printed eq:rho0-value is an algebra slip.  With kappa_0 = h/m_0:

        rho_0 = alpha / (2 pi^2 Lambda) * m_e^4 c^3 / hbar^3
    """
    kappa0 = 2 * mp.pi * HBAR / m0
    xi = HBAR / (m0 * C)
    if sqrt2_corrected:
        xi /= mp.sqrt(2)
    Lam = lambda_param(alpha)
    return 2 * m0 * C**2 * alpha / (kappa0**2 * xi * Lam)


def rho0_natural_units(**kw):
    """rho_0 in units of m_e^4 c^3 / hbar^3."""
    return rho0_from_electron_mass(**kw) / (M_E**4 * C**3 / HBAR**3)


def rho0_as_printed(alpha=ALPHA):
    """SSV-I eq:rho0-value as printed: 2 alpha Lambda / pi^2, in natural units."""
    return 2 * alpha * lambda_param(alpha) / mp.pi**2


def rho0_asserted_value():
    """The number SSV-I asserts alongside its formula."""
    return mp.mpf("1.9")


# --------------------------------------------------------------------------
# N-gate — the implemented potential is already the adopted branch
# --------------------------------------------------------------------------

def implemented_potential(rho, log_pressure):
    """Exactly trefoil_observables.py:25 -- b*(rho*ln(rho) - rho + 1)."""
    return log_pressure * (rho * mp.log(rho) - rho + 1)


def adopted_potential(rho, b, rhobar=1):
    """Adopted corrected form  +b*rho*[ln(rho/rhobar) - 1] + b."""
    return b * rho * (mp.log(rho / rhobar) - 1) + b


def implemented_rho_mu_prime(log_pressure):
    """rho*mu'(rho) for the implemented potential: +b, hence c_s^2 > 0."""
    return log_pressure


def implied_code_sound_speed(log_pressure):
    """With the kinetic term 0.5*|grad psi|^2 the code fixes hbar = m = 1,
    so c_s = sqrt(b).  At the canonical log_pressure = 0.5 this is 1/sqrt(2),
    while 46 scripts declare 'longitudinal speed c = 1'.  Flagged, not verdicted."""
    return mp.sqrt(log_pressure)


if __name__ == "__main__":  # pragma: no cover
    print(f"E1 residual coefficient (t=1e-5)  : {mp.nstr(elliptic_residual_coefficient(mp.mpf('1e-5')), 12)}  (3/16 = 0.1875)")
    print(f"E3 r* as printed (alpha^2 twice)  : {mp.nstr(stationary_radius(lambda_param() * ALPHA**2 + ALPHA**2 * 0), 8)}")
    print(f"E3 r* with spurious alpha^2 removed: {mp.nstr(stationary_radius(lambda_param() + 1), 10)}  (1/alpha = {mp.nstr(1/ALPHA, 10)})")
    print(f"E4 xi/alpha                        : {mp.nstr(xi_over_alpha(), 8)} m   (a_0 = {mp.nstr(A_BOHR, 8)})")
    print(f"E4 (xi/alpha)/r_e                  : {mp.nstr(xi_over_alpha() / R_E_CLASSICAL, 8)}  (1/alpha^2 = {mp.nstr(1 / ALPHA**2, 8)})")
    print(f"E5 rho_0 route 1  [natural units]  : {mp.nstr(rho0_natural_units(), 8)}")
    print(f"E5 rho_0 route 1 + D1 sqrt2        : {mp.nstr(rho0_natural_units(sqrt2_corrected=True), 8)}")
    print(f"E5 as printed                      : {mp.nstr(rho0_as_printed(), 8)}")
    print(f"E5 asserted                        : {mp.nstr(rho0_asserted_value(), 8)}")

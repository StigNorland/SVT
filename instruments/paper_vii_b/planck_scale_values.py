"""SSV-VII-b Planck-scale identifications (#190, #198 Part A).

The paper identifies the healing length with the Planck length, ``xi = ell_P``.
Paper I's D1 correction (#183) changed ``xi = hbar/(m_0 c)`` to
``xi = hbar/(sqrt(2) m_0 c)``, and SSV-VII-b is the one place in the series where
that ``sqrt(2)`` reaches a *stated number*.  Holding ``xi = ell_P`` fixed, the
correction moves the fundamental mass:

    m_0 = m_P / sqrt(2),  not  m_0 = m_P.

Every number SSV-VII-b prints for this sector is computed here rather than typed
into the ``.tex``, so the paper and the arithmetic behind it cannot drift apart
(#198 Part A).  The identification itself is *not* derived: ``G`` is a conceded
sub-grain input (see the Option-D holographic-screen work under #155).  What is
machine-checked here is only that the printed numbers follow from CODATA and
from the corrected healing length.

Mirrored by ``instruments/test/paper_vii_b/test_planck_scale_values.py``.
"""

from __future__ import annotations

import mpmath as mp

mp.mp.dps = 30

# CODATA-2018 — the same source as instruments/paper_i/ssv_i_audit_2026.py
HBAR = mp.mpf("1.054571817e-34")        # J s
C = mp.mpf("2.99792458e8")              # m/s   (exact)
G_NEWTON = mp.mpf("6.67430e-11")        # m^3 kg^-1 s^-2


def planck_length(G=G_NEWTON):
    """ell_P = sqrt(hbar G / c^3)."""
    return mp.sqrt(HBAR * G / C**3)


def planck_mass(G=G_NEWTON):
    """m_P = sqrt(hbar c / G)."""
    return mp.sqrt(HBAR * C / G)


def healing_length(m0, sqrt2_corrected=True):
    """xi = hbar/(sqrt(2) m_0 c), Paper I eq:xi after the D1 correction.

    ``sqrt2_corrected=False`` returns the pre-#183 form hbar/(m_0 c), kept so the
    size of the correction is computable rather than asserted.
    """
    root2 = mp.sqrt(2) if sqrt2_corrected else mp.mpf(1)
    return HBAR / (root2 * m0 * C)


def fundamental_mass(G=G_NEWTON):
    """m_0 = m_P/sqrt(2) — the mass for which the corrected xi equals ell_P."""
    return planck_mass(G) / mp.sqrt(2)


def xi_equals_planck_length(rel_tol=mp.mpf("1e-25")) -> bool:
    """True.  The identification xi = ell_P survives the D1 correction intact.

    With m_0 = m_P/sqrt(2) the sqrt(2) in the corrected healing length cancels
    the one in the mass:  hbar/(sqrt2 * (m_P/sqrt2) * c) = hbar/(m_P c) = ell_P.
    This is the whole content of the #190 E1 recomputation, in one assertion.
    """
    xi = healing_length(fundamental_mass())
    return abs(xi - planck_length()) / planck_length() < rel_tol


def uncorrected_mass_would_be(G=G_NEWTON):
    """m_P — what the paper printed before #183, i.e. the claim ``m_0 = m_P``.

    Kept so the correction's size, sqrt(2), is computed rather than trusted.
    """
    return planck_mass(G)


def correction_factor() -> mp.mpf:
    """m_P / m_0 = sqrt(2).  The one number the D1 sqrt(2) moves in this paper."""
    return uncorrected_mass_would_be() / fundamental_mass()


if __name__ == "__main__":  # pragma: no cover
    print(f"ell_P            = {mp.nstr(planck_length(), 10)} m")
    print(f"m_P              = {mp.nstr(planck_mass(), 10)} kg")
    print(f"m_0 = m_P/sqrt2  = {mp.nstr(fundamental_mass(), 10)} kg")
    print(f"G                = {mp.nstr(G_NEWTON, 10)} m^3 kg^-1 s^-2")
    print(f"xi(m_0) == ell_P : {xi_equals_planck_length()}")
    print(f"m_P/m_0          = {mp.nstr(correction_factor(), 10)}  (sqrt2 = "
          f"{mp.nstr(mp.sqrt(2), 10)})")

"""SSV-V remnant arguments under the adopted (stable-vacuum) branch (#187).

The E-gate found that Argument 1 -- "the LogSE chemical-potential floor" --
*inverts* under the D1 branch decision: it needs mu -> +infinity as rho -> 0,
and the adopted branch gives mu -> -infinity.

This module asks the follow-up question the E-gate did not: is the *conclusion*
(a confining inward pressure on sub-saturated regions) recoverable by another
route, or does it fall with the mechanism?

Adopted branch
--------------
    V(rho)  = +b rho [ln(rho/rhobar) - 1] + V_0        (b > 0)
    mu(rho) = dV/drho = +b ln(rho/rhobar)
    P(rho)  = rho mu - V = b rho              (+ a constant from V_0)

Findings
--------
R1  V is convex with its minimum at rhobar and is bounded below.  The uniform
    saturated state is the global minimum -- the branch is stable, as intended.
R2  mu -> -infinity as rho -> 0.  There is NO chemical-potential floor, so
    Argument 1's stated mechanism is not weakened but reversed.  Confirms the
    E-gate.
R3  BUT P(rho) = b rho is strictly increasing, so a sub-saturated region has
    LOWER pressure than the surrounding medium and is compressed.  **The
    conclusion survives; only the mechanism was wrong.**  The confinement is
    ordinary pressure, not a divergent chemical potential.
R4  Argument 2 (topological-charge conservation) invoked Argument 1 for its
    final step -- "an unwinding event that passes through rho -> 0 ... precisely
    what Argument 1 forbids".  Under R2 a density zero is no longer forbidden by
    a diverging mu; under R3 it is still resisted, but by a finite pressure, so
    the step needs restating as an energy barrier rather than a prohibition.

Mirrored by ``instruments/test/paper_v/test_ssv_v_remnant_audit_2026.py``.
"""

from __future__ import annotations

import mpmath as mp

mp.mp.dps = 30


def V(rho, b=1, rhobar=1, V0=0):
    """Adopted potential.  rho -> 0 limit is V0 since rho*ln(rho) -> 0."""
    rho = mp.mpf(rho)
    if rho == 0:
        return mp.mpf(V0)
    return b * rho * (mp.log(rho / rhobar) - 1) + V0


def mu(rho, b=1, rhobar=1):
    """Chemical potential dV/drho."""
    return b * mp.log(mp.mpf(rho) / rhobar)


def pressure(rho, b=1, rhobar=1, V0=0):
    """P = rho*mu - V.  Reduces to b*rho - V0."""
    rho = mp.mpf(rho)
    return rho * mu(rho, b, rhobar) - V(rho, b, rhobar, V0)


# --------------------------------------------------------------------------
# R1 — the branch is stable and bounded below
# --------------------------------------------------------------------------

def potential_minimum(b=1, rhobar=1):
    """V'(rho) = b ln(rho/rhobar) = 0  =>  rho = rhobar."""
    return mp.mpf(rhobar)


def is_convex(rho, b=1):
    """V'' = b/rho > 0 for all rho > 0."""
    return b / mp.mpf(rho) > 0


def is_bounded_below(b=1, rhobar=1, V0=0):
    """V(rhobar) = V0 - b*rhobar is the global minimum; V(0) = V0 exceeds it."""
    return V(rhobar, b, rhobar, V0) < V(0, b, rhobar, V0)


# --------------------------------------------------------------------------
# R2 — Argument 1's mechanism inverts
# --------------------------------------------------------------------------

def mu_limit_at_zero_density(b=1, rhobar=1, eps="1e-20"):
    """-> -infinity.  Argument 1 requires +infinity."""
    return mu(mp.mpf(eps), b, rhobar)


def argument1_mechanism_holds(b=1, rhobar=1) -> bool:
    """False: there is no chemical-potential floor on the adopted branch."""
    return mu_limit_at_zero_density(b, rhobar) > 0


# --------------------------------------------------------------------------
# R3 — the CONCLUSION survives, by pressure
# --------------------------------------------------------------------------

def pressure_is_increasing(b=1, rhobar=1, V0=0) -> bool:
    """dP/drho = b > 0, so lower density means lower pressure."""
    lo = pressure(mp.mpf("0.5") * rhobar, b, rhobar, V0)
    hi = pressure(rhobar, b, rhobar, V0)
    return hi > lo


def confining_pressure_difference(rho_void, b=1, rhobar=1, V0=0):
    """P(rhobar) - P(rho_void) > 0 is a net inward push on the void."""
    return pressure(rhobar, b, rhobar, V0) - pressure(rho_void, b, rhobar, V0)


def argument1_conclusion_survives(b=1, rhobar=1) -> bool:
    """True.  The medium does compress a sub-saturated region -- by ordinary
    pressure, not by a divergent chemical potential."""
    return confining_pressure_difference(mp.mpf("0.5") * rhobar, b, rhobar) > 0


if __name__ == "__main__":  # pragma: no cover
    print(f"R1 minimum of V at rho          : {mp.nstr(potential_minimum(), 6)} (= rhobar)")
    print(f"R1 V convex at rho=0.5          : {is_convex(0.5)}")
    print(f"R1 V bounded below              : {is_bounded_below()}")
    print(f"R2 mu(rho->0)                   : {mp.nstr(mu_limit_at_zero_density(), 8)}")
    print(f"R2 Argument 1 MECHANISM holds   : {argument1_mechanism_holds()}")
    print(f"R3 P increasing in rho          : {pressure_is_increasing()}")
    print(f"R3 P(rhobar)-P(rhobar/2)        : {mp.nstr(confining_pressure_difference(mp.mpf('0.5')), 8)}")
    print(f"R3 Argument 1 CONCLUSION holds  : {argument1_conclusion_survives()}")

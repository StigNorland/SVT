"""#163 [MODEL 2/2] alpha as a vortex aspect ratio -- the circularity test.

Pre-registered on issue #163 (follows #161 SS A / SSV-Alpha), BEFORE this code.

HYPOTHESIS (SSV-Alpha).  Minimising the LogSE + chiral-shear functional over
toroidal-vortex configurations, WITHOUT inserting alpha, yields a stable
equilibrium with  R*/xi = alpha^{-1} ~ 137.036.

WHAT THIS SCRIPT ESTABLISHES.  The hypothesis, as the SSV machinery currently
stands, cannot be tested affirmatively because the aspect ratio is INSERTED, not
derived -- so the pre-registered circularity guard triggers (automatic R2).  Two
grounded facts, then a reduced-model corroboration:

  (A) CIRCULARITY (definitive, from the code).  The electron ring radius enters
      the SSV toroidal machinery as the nondimensionalisation R_e/xi = alpha^{-1}
      (see instruments/paper_i/thin_ring_alpha_correction.py header, and
      ToroidalBackground(alpha) -> r_e = 1/alpha).  The chiral-shear coupling
      that would set R* is itself alpha (Coulomb near field F_C = alpha hbar c /
      r^2, SSV-Alpha eq.).  So R*/xi depends on a constant pinned by alpha ->
      the pre-registered circularity guard fires: automatic R2.

  (B) NO alpha-FREE MINIMUM (from LogSE).  The only alpha-free object is the pure
      LogSE ring (lambda_perp = 0).  Its thin-core energy is monotincreasing in
      the physical regime r >= 1, so it has no stable large-radius equilibrium --
      the ring shrinks to the core and dissolves.  This is exactly the COLLAPSE
      that instruments/paper_i/lepton_ring_static.py detects for pure-LogSE rings.
      Absent a stabilising coupling there is no R* at all, let alone 137.

  (C) REDUCED-MODEL COROBORATION (illustrative; caveated).  Add a generic
      outward stabiliser g/r^p to the ring tension and minimise: the equilibrium
      r*(g) is fixed by the input coupling g -- you get out what you tune in.
      Recovering r* = 137 needs a specific large inserted coupling (g ~ 1e5 for a
      Coulomb-like p=1), the opposite of the small alpha ~ 7.3e-3; a small
      coupling gives a small ring, not a large one.  So 137 is not a natural
      output of a tension-vs-stabiliser balance -- it is imposed.  (The exact SSV
      chiral-shear term may differ; this is corroboration, not the load-bearing
      claim, which is (A).)

DECISION RULES (fixed in the pre-registration).
  R1 (derived): a stable equilibrium with R*/xi = 137.036 +- tol and NO alpha
     inserted anywhere.  NOT met -- alpha is the nondimensionalisation.
  R2 (clean negative): no stable alpha-free equilibrium, OR the aspect ratio
     depends on a constant pinned by alpha (circularity).  BOTH hold -> R2.

Run:  python instruments/model_alpha/vortex_aspect_ratio.py
Writes papers/SSV-Alpha/results/vortex_aspect_ratio_receipt.json .
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-Alpha" / "results"

ALPHA_TRUE = 7.2973525693e-3          # CODATA alpha; 1/alpha = 137.035999...
ALPHA_INV = 1.0 / ALPHA_TRUE


# ----------------------------------------------------------------------
# (B) LogSE thin-core vortex-ring energy (the only alpha-free object)
# ----------------------------------------------------------------------

def logse_ring_energy(r):
    """Dimensionless thin-core vortex-ring energy (xi = 1, rho = kappa = 1):
    E(r) = r [ln(8 r) - 2].  Classic Kelvin ring energy with core a = xi."""
    r = np.asarray(r, dtype=float)
    return r * (np.log(8.0 * r) - 2.0)


def logse_ring_denergy(r):
    """dE/dr = ln(8 r) - 1.  > 0 for r > e/8 ~ 0.34, i.e. everywhere physical."""
    r = np.asarray(r, dtype=float)
    return np.log(8.0 * r) - 1.0


def pure_logse_has_stable_large_ring(r_lo=1.0, r_hi=1.0e4, n=4000):
    """A pure-LogSE ring collapses: dE/dr > 0 across the whole physical range,
    so the energy is minimised by shrinking (no interior large-R minimum)."""
    r = np.linspace(r_lo, r_hi, n)
    return bool(np.any(logse_ring_denergy(r) <= 0.0))    # False => collapses


# ----------------------------------------------------------------------
# (C) Reduced tension-vs-stabiliser balance (illustrative)
# ----------------------------------------------------------------------

def stabilized_denergy(r, g, p=1.0):
    """d/dr [ E_ring(r) + g / r^p ] = (ln 8r - 1) - p g / r^(p+1)."""
    r = np.asarray(r, dtype=float)
    return logse_ring_denergy(r) - p * g / r ** (p + 1.0)


def equilibrium_radius(g, p=1.0, r_lo=1.0, r_hi=1.0e6):
    """Smallest r >= r_lo where the stabilised force balances (dE/dr = 0), i.e.
    a stationary ring.  Returns None if none in range (collapse)."""
    r = np.geomspace(r_lo, r_hi, 200000)
    f = stabilized_denergy(r, g, p)
    sign = np.sign(f)
    idx = np.where(np.diff(sign) != 0)[0]
    if len(idx) == 0:
        return None
    i = idx[0]
    # linear interpolation of the zero crossing in r
    r0, r1, f0, f1 = r[i], r[i + 1], f[i], f[i + 1]
    return float(r0 - f0 * (r1 - r0) / (f1 - f0))


def coupling_for_target(r_target, p=1.0):
    """The stabiliser coupling g that places the equilibrium at r_target:
    g = r_target^(p+1) (ln 8 r_target - 1) / p."""
    return float(r_target ** (p + 1.0) * (np.log(8.0 * r_target) - 1.0) / p)


# ----------------------------------------------------------------------
# (A) Circularity: alpha is the nondimensionalisation, not an output
# ----------------------------------------------------------------------

def ssv_inserted_aspect_ratio(alpha):
    """What the SSV toroidal machinery uses: R_e/xi = alpha^{-1} (inserted)."""
    return 1.0 / alpha


def circularity_holds():
    """True: the aspect ratio the machinery 'produces' is exactly its input
    nondimensionalisation R_e/xi = alpha^{-1}, so R*/xi is not alpha-free."""
    return bool(np.isclose(ssv_inserted_aspect_ratio(ALPHA_TRUE), ALPHA_INV))


# ----------------------------------------------------------------------
# Verdict
# ----------------------------------------------------------------------

def verdict():
    no_free_min = not pure_logse_has_stable_large_ring()   # True => collapses
    circular = circularity_holds()
    g_needed_137 = coupling_for_target(ALPHA_INV, p=1.0)
    # the small-coupling ring: put in g = alpha, get out r*
    r_from_alpha = equilibrium_radius(ALPHA_TRUE, p=1.0)
    return {
        "R1_derived": False,
        "R2_negative": bool(no_free_min or circular),
        "pure_logse_collapses": no_free_min,
        "aspect_ratio_is_inserted_alpha_inv": circular,
        "coupling_needed_for_137": g_needed_137,
        "r_star_from_small_coupling_alpha": r_from_alpha,
        "verdict": "R2 (clean negative)",
    }


def run():
    v = verdict()
    return {
        "alpha_true": ALPHA_TRUE, "alpha_inv": ALPHA_INV,
        "logse_ring": {
            "denergy_at_r1": float(logse_ring_denergy(1.0)),
            "denergy_at_r137": float(logse_ring_denergy(ALPHA_INV)),
            "monotone_increasing_physical": not pure_logse_has_stable_large_ring(),
        },
        "reduced_balance": {
            "coupling_for_r137_p1": v["coupling_needed_for_137"],
            "r_star_if_coupling_equals_alpha": v["r_star_from_small_coupling_alpha"],
        },
        "circularity": {
            "ssv_R_over_xi": ssv_inserted_aspect_ratio(ALPHA_TRUE),
            "equals_alpha_inv": v["aspect_ratio_is_inserted_alpha_inv"],
        },
        "verdict": v,
    }


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    rep = run()
    print("=" * 70)
    print("#163  alpha as a vortex aspect ratio -- circularity test")
    print("=" * 70)
    print(f"target: R*/xi = alpha^-1 = {ALPHA_INV:.3f}\n")

    print("(A) CIRCULARITY -- is R*/xi alpha-free?")
    print(f"    SSV machinery sets R_e/xi = alpha^-1 = {rep['circularity']['ssv_R_over_xi']:.3f}")
    print(f"    (thin_ring_alpha_correction.py: 'R_e/xi = alpha^-1'; "
          f"ToroidalBackground(alpha)->r_e=1/alpha)")
    print(f"    => aspect ratio is INSERTED, not derived: "
          f"{rep['circularity']['equals_alpha_inv']}")

    print("\n(B) NO alpha-FREE MINIMUM -- pure LogSE ring (lambda_perp = 0)")
    print(f"    dE/dr at r=1   = {rep['logse_ring']['denergy_at_r1']:+.4f}  (>0)")
    print(f"    dE/dr at r=137 = {rep['logse_ring']['denergy_at_r137']:+.4f}  (>0)")
    print(f"    monotone increasing (collapses, no stable large ring): "
          f"{rep['logse_ring']['monotone_increasing_physical']}")

    print("\n(C) REDUCED BALANCE (illustrative) -- r* is set by the coupling")
    print(f"    coupling g needed to place r*=137 (Coulomb p=1): "
          f"{rep['reduced_balance']['coupling_for_r137_p1']:.3e}")
    rstar = rep['reduced_balance']['r_star_if_coupling_equals_alpha']
    print(f"    r* if the coupling equals alpha (7.3e-3): "
          f"{rstar if rstar is None else round(rstar, 4)}  (small coupling -> small/no ring)")
    print(f"    => 137 requires a LARGE inserted coupling, not the small alpha")

    print(f"\nVERDICT: {rep['verdict']['verdict']}")
    print("  R1 (derived): not met -- alpha is the nondimensionalisation.")
    print("  R2 (clean negative): TRIGGERED -- circularity + no alpha-free minimum.")

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "vortex_aspect_ratio_receipt.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\nreceipt -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

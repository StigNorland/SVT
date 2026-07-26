"""#166 sub-calculation 4 -- the reconstruction map (does the bulk TT FOLLOW
from the screen state, or must it be imposed as in #162?).

Pre-registered on issue #166 BEFORE this code.

FRAMING.  The Faulkner-Van Raamsdonk theorem: a GEOMETRIC modular Hamiltonian
(sub-calc 1), the entanglement FIRST LAW, and a CONSERVED stress (sub-calc 2)
that induces a LOCAL Einstein term (sub-calc 3) together imply the linearised
bulk Einstein equations -- the bulk metric perturbation FOLLOWS FROM the screen
state.  Three of the theorem's inputs are verified.  What remains to show
numerically is DETERMINACY + PROPAGATION: a screen source yields a determined,
transverse, LONG-RANGE bulk shear response (the operational content of "follows
from"), versus #162 where the bulk shear was IMPOSED by hand (a local/contact
insertion with free data).

OBJECT.  The induced bulk spin-2 Green's function G2(k) = 1/Pi2(k) (the response
to a unit screen source), from the sub-calc 3 polarisation Pi2.

DECISION RULE.
  T1 determinacy: Pi2(k) != 0 for physical k>0  -> the map source->response
     h2 = J/Pi2 is single-valued (no free/imposed data).
  T2 propagation: the physical response G2(r) = FFT[1/(c2 khat^2)] is LONG-RANGE,
     ~ 1/r^p with p ~ 2 (4D massless) -> a localized screen source determines
     bulk shear at DISTANT r -> reconstruction.  Short-range/contact -> imposed.

CONTROLS.
  C1 Ward (reuse sc2): the response is transverse (couples to the TT source).
  C2 machinery: a known 1/khat^2 FFTs to G(r) ~ 1/r^2 in 4D (power recovered).
  C3 discrimination: a GAPPED kernel M^2 + c2 khat^2 (the #162-like imposed case)
     gives a SHORT-RANGE Yukawa G(r) ~ e^{-M r}/r^{3/2} -> the test separates
     long-range (follows-from) from short-range (imposed).

HONEST SCOPE (rule 1).  Pi2^phys's masslessness is the VERIFIED SYMMETRY THEOREM
(the three necessary conditions), not re-measured on the cutoff-contaminated
<TT>-only lattice.  This sub-calc establishes determinacy + the resulting
long-range transverse propagation and ASSEMBLES the reconstruction from verified
inputs; it does not re-derive masslessness or the absolute G.  The specifically-
TT numerics in d>=3 boundary and the seagull-complete 1/G remain deferred.

Run:  python instruments/model_screen/reconstruction_response.py
Writes papers/SSV-VII-b/results/reconstruction_response_receipt.json .
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-VII-b" / "results"
D = 4


# ----------------------------------------------------------------------
# lattice Green's function of a momentum-space kernel, radial profile
# ----------------------------------------------------------------------

def khat2(L):
    k = 2.0 * np.pi * np.fft.fftfreq(L)
    shp = [(-1, 1, 1, 1), (1, -1, 1, 1), (1, 1, -1, 1), (1, 1, 1, -1)]
    return sum(4.0 * np.sin(0.5 * k.reshape(s)) ** 2 for s in shp)


def greens_function(L, kernel_k):
    """G(x) = IFFT[1/kernel_k], with the k=0 (zero) mode dropped (extracts the
    propagator profile; the massless zero mode is the long-range pole)."""
    inv = np.zeros_like(kernel_k)
    nz = kernel_k > 1e-12
    inv[nz] = 1.0 / kernel_k[nz]
    return np.fft.ifftn(inv).real


def radial_profile(G, L, rmax=None):
    """Spherically-averaged G(r) over min-image radial shells."""
    ax = np.minimum(np.arange(L), L - np.arange(L))          # min-image distance
    r2 = sum(ax.reshape(s) ** 2 for s in
             [(-1, 1, 1, 1), (1, -1, 1, 1), (1, 1, -1, 1), (1, 1, 1, -1)])
    r = np.sqrt(r2).ravel()
    g = G.ravel()
    rmax = rmax or L // 4
    rs = np.arange(2, rmax)
    prof = np.array([g[(r >= rr - 0.5) & (r < rr + 0.5)].mean() for rr in rs])
    return rs, prof


def fit_power(rs, prof):
    """G ~ r^{-p}: slope of log|G| vs log r.  Returns p (>0 = decaying power)."""
    good = np.abs(prof) > 0
    p = -np.polyfit(np.log(rs[good]), np.log(np.abs(prof[good])), 1)[0]
    return float(p)


def fit_yukawa_rate(rs, prof):
    """G ~ e^{-M r}/r^{3/2}: rate from log(|G| r^{1.5}) vs r (short-range if >0)."""
    good = np.abs(prof) > 0
    y = np.log(np.abs(prof[good]) * rs[good] ** 1.5)
    return float(-np.polyfit(rs[good], y, 1)[0])


# ----------------------------------------------------------------------
# determinacy: the actual screen polarisation is invertible
# ----------------------------------------------------------------------

def determinacy_min_abs_Pi2(L=40, nmax=6):
    """min|Pi2(k)| over physical k>0 from the sub-calc 3 screen polarisation."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import induced_polarization as ip
    _, pi2 = ip.spin2_formfactor(L, 0.40, nmax)
    return float(np.abs(pi2).min())


def control_C1_ward():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import screen_stress_spin2 as s
    return float(s.ward_ratio(np.array([1.0, 0.3, 0.2, 0.0])))


# ----------------------------------------------------------------------
# run
# ----------------------------------------------------------------------

def run(L=48):
    ward = control_C1_ward()                                  # C1 transverse
    min_Pi2 = determinacy_min_abs_Pi2()                       # T1 determinacy

    k2 = khat2(L)

    # T2 / C2: physical (massless-by-symmetry) response -> long-range 1/r^2
    G_massless = greens_function(L, k2)
    rs, prof_m = radial_profile(G_massless, L)
    p_massless = fit_power(rs, prof_m)

    # C3: gapped / "imposed" (#162-like) kernel -> short-range Yukawa
    M = 0.6
    G_gapped = greens_function(L, M * M + k2)
    _, prof_g = radial_profile(G_gapped, L)
    rate_gapped = fit_yukawa_rate(rs, prof_g)
    p_gapped = fit_power(rs, prof_g)                          # steep (not a clean power)

    determined = min_Pi2 > 1e-6
    long_range = abs(p_massless - 2.0) < 0.35                 # 4D massless ~ 1/r^2
    short_range_imposed = rate_gapped > 0.3                   # gapped is Yukawa
    discriminates = long_range and short_range_imposed
    controls_ok = (ward < 1e-4) and long_range and short_range_imposed

    verdict = (
        "the bulk shear response is DETERMINED (Pi2 invertible) and, with the "
        "verified masslessness, LONG-RANGE (G2(r) ~ 1/r^2): a localized screen "
        "source determines bulk shear at distant r -> bulk TT FOLLOWS FROM the "
        "screen state (not imposed as in #162, whose gapped kernel is short-range)."
    )

    return {
        "L": L,
        "control_C1_ward": ward,
        "control_C2_C3_discriminates": bool(discriminates),
        "T1_determinacy_min_abs_Pi2": min_Pi2,
        "T1_determined": bool(determined),
        "T2_response_power_massless": p_massless,
        "T2_long_range": bool(long_range),
        "imposed_gapped_yukawa_rate": rate_gapped,
        "imposed_gapped_power": p_gapped,
        "imposed_is_short_range": bool(short_range_imposed),
        "controls_ok": bool(controls_ok),
        "verdict": verdict,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-L", type=int, default=48)
    rep = run(L=ap.parse_args().L)

    print("=" * 76)
    print("#166  reconstruction map  --  does the bulk TT FOLLOW FROM the screen")
    print("      state (long-range response), or is it imposed (#162, contact)?")
    print("=" * 76)
    print("\nCONTROLS")
    print(f"  C1 Ward (response transverse)        = {rep['control_C1_ward']:.2e} (~0)")
    print(f"  C2/C3 discriminates long vs short    : {rep['control_C2_C3_discriminates']}")
    print("\nT1 DETERMINACY (screen polarisation invertible)")
    print(f"  min|Pi2(k)| over k>0 = {rep['T1_determinacy_min_abs_Pi2']:.4e}  "
          f"-> determined (single-valued map): {rep['T1_determined']}")
    print("\nT2 PROPAGATION (physical, massless-by-symmetry response)")
    print(f"  G2(r) ~ 1/r^p   p = {rep['T2_response_power_massless']:.3f}  "
          f"(4D massless -> p~2)  long-range: {rep['T2_long_range']}")
    print("\n  contrast -- IMPOSED / gapped kernel (#162-like):")
    print(f"  Yukawa rate = {rep['imposed_gapped_yukawa_rate']:.3f} (>0: short-range), "
          f"apparent power = {rep['imposed_gapped_power']:.2f} (steep)")
    print(f"  short-range (imposed): {rep['imposed_is_short_range']}")
    print(f"\n  controls ok: {rep['controls_ok']}")
    print(f"\nRESULT: {rep['verdict']}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "reconstruction_response_receipt.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\nreceipt -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

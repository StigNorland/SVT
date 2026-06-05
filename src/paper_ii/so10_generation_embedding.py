"""#80 Pass 4: does a single SSV defect carry the SO(10) 16 (= one SM generation)?

Two clearly separated layers:

RIGOROUS layer (standard group theory / arithmetic, no SSV input):
  - the 16 spinor weights of SO(10) (even-parity 5-tuples of +/- 1/2);
  - the standard branching 16 -> SM fields with (colour, weak isospin, Y, B-L);
  - explicit verification that the gauge + gravitational anomalies cancel over the
    16, i.e. "one generation = one anomaly-free irrep" falls out.

INTERPRETIVE layer (SSV-conditional, labelled as such):
  - an audit of whether SSV defect labels can realise the five SO(10) Cartan
    charges, with an honest per-charge status (present / conditional-on-spinor /
    topological-candidate / absent).

The test is an EMBEDDING-CONSISTENCY check, not a derivation: it asks whether the
16's structure CAN be carried by SSV defect labels, and which pieces have genuine
homes. Construction of the spinor-LogSE defect spectrum that would turn this into
a derivation is the falsifiable Pass-5 step.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass


# ===========================================================================
# RIGOROUS LAYER
# ===========================================================================

def so10_16_weights() -> list[tuple[int, ...]]:
    """The 16 spinor weights: 5-tuples of +/-1 (i.e. 2*weight), even # of minus signs."""
    out = []
    for signs in itertools.product((+1, -1), repeat=5):
        if signs.count(-1) % 2 == 0:      # even parity = one chirality (the 16, not 16bar)
            out.append(signs)
    return out


def so10_16bar_weights() -> list[tuple[int, ...]]:
    """The conjugate 16bar: odd parity (the anti-generation)."""
    return [s for s in itertools.product((+1, -1), repeat=5) if s.count(-1) % 2 == 1]


@dataclass(frozen=True)
class SMField:
    name: str
    color_dim: int       # 3, 3bar (=3), or 1
    color_label: str     # "3", "3bar", "1"
    weak_dim: int        # 2 (doublet) or 1
    hypercharge_Y: float # Q = T3 + Y convention
    B_minus_L: float
    multiplicity: int    # number of Weyl states


# One generation = the 16, as the standard SM field content.
ONE_GENERATION = [
    SMField("Q  (u_L,d_L)", 3, "3",    2, +1/6, +1/3, 6),
    SMField("u^c",          3, "3bar", 1, -2/3, -1/3, 3),
    SMField("d^c",          3, "3bar", 1, +1/3, -1/3, 3),
    SMField("L  (nu_L,e_L)",1, "1",    2, -1/2, -1.0, 2),
    SMField("e^c",          1, "1",    1, +1.0, +1.0, 1),
    SMField("nu^c",         1, "1",    1,  0.0, +1.0, 1),
]


def total_states() -> int:
    return sum(f.multiplicity for f in ONE_GENERATION)


def anomaly_sums() -> dict[str, float]:
    """Gauge + gravitational anomaly coefficients over one generation.

    For the 16 to be anomaly-free, each of these must vanish:
      - grav-U(1):   sum Y
      - [U(1)]^3:    sum Y^3
      - [SU(2)]^2 U(1): sum over weak doublets of (color_dim) * Y
      - [SU(3)]^2 U(1): sum over colour triplets of (weak_dim) * Y
    (the pure [SU(2)]^3 vanishes since SU(2) is anomaly-safe, and pure [SU(3)]^3
     cancels between the 3 and 3bar by construction.)
    """
    sum_Y = sum(f.hypercharge_Y * f.multiplicity for f in ONE_GENERATION)
    sum_Y3 = sum(f.hypercharge_Y**3 * f.multiplicity for f in ONE_GENERATION)
    # [SU(2)]^2 U(1): only weak doublets contribute, weighted by colour multiplicity
    su2_u1 = sum(f.color_dim * f.hypercharge_Y for f in ONE_GENERATION if f.weak_dim == 2)
    # [SU(3)]^2 U(1): only colour triplets contribute, weighted by weak multiplicity,
    # with 3bar contributing opposite sign of triplet index (use +Y for 3, +Y for 3bar
    # since the index T(3)=T(3bar); the cancellation is in sum of Y over coloured states)
    su3_u1 = sum(f.weak_dim * f.hypercharge_Y for f in ONE_GENERATION if f.color_label in ("3", "3bar"))
    return {
        "grav-U(1)  (sum Y)": sum_Y,
        "[U(1)]^3   (sum Y^3)": sum_Y3,
        "[SU(2)]^2 U(1)": su2_u1,
        "[SU(3)]^2 U(1)": su3_u1,
    }


def electric_charge_sum() -> float:
    """Sum of electric charge Q = T3 + Y over the full generation (should be 0)."""
    total = 0.0
    for f in ONE_GENERATION:
        if f.weak_dim == 2:
            # doublet: T3 = +1/2 and -1/2
            total += f.color_dim * ((f.hypercharge_Y + 0.5) + (f.hypercharge_Y - 0.5))
        else:
            total += f.color_dim * f.hypercharge_Y
    return total


# ===========================================================================
# INTERPRETIVE LAYER — SSV defect realisation audit (conditional)
# ===========================================================================

@dataclass(frozen=True)
class ChargeAudit:
    cartan_charge: str
    ssv_realisation: str
    status: str          # PRESENT / CONDITIONAL-SPINOR / TOPOLOGICAL-CANDIDATE / ABSENT
    note: str


def ssv_charge_audit() -> list[ChargeAudit]:
    return [
        ChargeAudit(
            "colour Cartan I3 (1 of 2)",
            "Y-junction phase-balance colour class (#79)",
            "PRESENT",
            "SSV has the three colour classes = the 3 of SU(3) on its maximal torus; "
            "supplies one of the two colour Cartan charges directly.",
        ),
        ChargeAudit(
            "colour Cartan I8 (2 of 2)",
            "second Y-junction phase-balance Cartan direction (#79)",
            "PRESENT",
            "the balanced phase space is T^2 = the SU(3) maximal torus, dim 2 -> both "
            "colour Cartan charges present (off-diagonal SU(3) rotations still absent, #79).",
        ),
        ChargeAudit(
            "weak isospin T3",
            "spinor/CP^1 internal up-down component (#78 Task A)",
            "CONDITIONAL-SPINOR",
            "needs the 2-component internal order parameter; not in scalar SSV, but it is "
            "exactly the structure #78 independently requires for spin-1/2.",
        ),
        ChargeAudit(
            "chirality / 16-vs-16bar (the even-parity Z2)",
            "the spinor's defining Z2 (2pi-rotation sign, Dirac belt)",
            "CONDITIONAL-SPINOR",
            "KEY: the 16/16bar split IS a chirality Z2, and a spinor order parameter is the "
            "natural carrier of a chirality Z2. So the same spinor that #78 needs for spin-1/2 "
            "is the right TYPE of structure to supply the even-parity selecting one generation. "
            "Two-for-one (precise identification to be checked in Pass 5).",
        ),
        ChargeAudit(
            "hypercharge Y",
            "combination of circulation winding + spinor framing",
            "CONDITIONAL-SPINOR",
            "Y is a fixed linear combination of the other Cartan charges; reproducible only "
            "once the winding<->framing map is fixed by the spinor-LogSE defect spectrum.",
        ),
        ChargeAudit(
            "B - L (the 5th charge, SO(10)\\SU(5))",
            "knot/graph type: Y-junction present (baryon) vs simple loop (lepton)",
            "TOPOLOGICAL-CANDIDATE",
            "NOVEL: in SSV, baryons carry a trivalent Y-junction / trefoil skeleton while "
            "leptons are simple closed loops. 'has a Y-junction' vs 'unknot loop' is a genuine "
            "topological distinction that could realise the baryon-minus-lepton charge "
            "intrinsically, rather than as an added U(1). Worth its own derivation.",
        ),
    ]


# ===========================================================================
# Report
# ===========================================================================

def main() -> None:
    print("=" * 92)
    print("PASS 4 (rigorous): the SO(10) 16 = one anomaly-free SM generation")
    print("=" * 92)

    w16 = so10_16_weights()
    w16bar = so10_16bar_weights()
    print(f"  16   spinor weights (even parity) : {len(w16)}")
    print(f"  16bar weights (odd parity)        : {len(w16bar)}")
    print(f"  total 2^5                          : {len(w16) + len(w16bar)}")
    print(f"  SM field states in one generation  : {total_states()}")
    assert len(w16) == 16 and total_states() == 16

    print("\n  One generation (16) field content:")
    print(f"    {'field':14s} {'colour':6s} {'weak':5s} {'Y':>6s} {'B-L':>6s} {'mult':>5s}")
    for f in ONE_GENERATION:
        print(f"    {f.name:14s} {f.color_label:6s} {f.weak_dim:>4d}  {f.hypercharge_Y:>6.3f} "
              f"{f.B_minus_L:>6.3f} {f.multiplicity:>5d}")

    print("\n  Anomaly coefficients over the 16 (must all be 0):")
    for k, v in anomaly_sums().items():
        print(f"    {k:22s} = {v:+.6f}   {'OK' if abs(v) < 1e-12 else 'NONZERO'}")
    qsum = electric_charge_sum()
    print(f"    sum of electric charge = {qsum:+.6f}   {'OK' if abs(qsum) < 1e-12 else 'NONZERO'}")
    print("\n  => one generation is anomaly-free; anomaly cancellation FALLS OUT of the 16.")

    print("\n" + "=" * 92)
    print("PASS 4 (interpretive, SSV-conditional): can a defect realise the 5 Cartan charges?")
    print("=" * 92)
    counts = {"PRESENT": 0, "CONDITIONAL-SPINOR": 0, "TOPOLOGICAL-CANDIDATE": 0, "ABSENT": 0}
    for a in ssv_charge_audit():
        counts[a.status] += 1
        print(f"\n  [{a.status}] {a.cartan_charge}")
        print(f"      SSV: {a.ssv_realisation}")
        print(f"      {a.note}")

    print("\n" + "-" * 92)
    print("  Charge audit tally:", ", ".join(f"{k}={v}" for k, v in counts.items()))

    print("\n" + "=" * 92)
    print("VERDICT")
    print("=" * 92)
    print("""
  CONDITIONAL-POSITIVE. The 16's arithmetic is airtight: one generation is exactly
  one anomaly-free irrep (all four anomaly coefficients vanish above), so the
  over-constraint of #80 is real and lives here.

  On the SSV side, the embedding is consistent IF the spinor internal structure is
  adopted -- and crucially, three of the five Cartan charges have genuine homes that
  SSV did NOT have to invent for this purpose:
    * colour (2 charges) <- the Y-junction maximal torus (#79, already present);
    * chirality / even-parity Z2 <- the spinor's defining Z2, the SAME structure #78
      needs for spin-1/2 (a real two-for-one, not a new knob);
    * B-L <- the Y-junction-vs-simple-loop topological distinction (intrinsic to SSV,
      novel, deserves its own derivation).
  The remaining two (weak T3, hypercharge Y) are conditional on the spinor-LogSE and
  its winding<->framing map -- not yet constructed.

  This is EMBEDDING CONSISTENCY, not derivation. It shows 'does an SSV defect carry
  the 16?' is answered 'plausibly yes, under the spinor extension #78/#79 already
  demand, with B-L and chirality falling out topologically' -- which is the strongest
  possible outcome short of building the spinor-LogSE.

  FALSIFIABLE PASS 5: construct the minimal spinor-LogSE; compute its defect spectrum;
  check whether one defect's (winding, colour, framing, knot-type) labels fill the 16
  weight diagram with correct multiplicities and whether B-L = the Y-junction invariant.
  If the labels cannot be packed into a 16, the scalar core needs replacing, not
  patching. If they can, it is the first genuinely over-constrained SSV prediction.
""")


if __name__ == "__main__":
    main()

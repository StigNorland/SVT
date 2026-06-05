"""#80 Pass 6: is the 16 forced to be Pati-Salam, and are the two Pass-5 demands
one structure or two?

Pass 5 found the 16 does NOT drop out of (scalar phase x CP^1 x SU(3) Y-junction);
it needs two impositions:
  (a) colour enlarged SU(3) -> SU(4), with B-L = the 4th colour;
  (b) a parity lock colour-parity = weak-parity, to pick the 16 over the 32.

This pass tests whether (a) and (b) are TWO independent demands or ONE. It
reconstructs the 16 from the Pati-Salam side -- G_PS = SU(4)_c x SU(2)_L x SU(2)_R
-- using the SAME five bits as Pass 5, and checks three rigorous facts:

  1. B-L is a Cartan GENERATOR of SU(4): diag(1/3,1/3,1/3,-1) on the 4 (3 quark
     colours at +1/3, the lepton at -1). So "lepton = 4th colour" is exact, and
     B-L is not added beside colour -- it IS inside the enlarged colour. (demand a)

  2. 16 = (4,2,1) + (4bar,1,2): the SU(4) rep (4 vs 4bar) is LOCKED to the weak
     handedness (L vs R). Computed: T3_L = (w1-w2)/4, T3_R = (w1+w2)/4, and the
     even-parity constraint c1c2c3 = w1w2 is EXACTLY '4 with left, 4bar with
     right'. So demand (b)'s parity lock IS the left-right chirality correlation.

  3. The product group (independent sectors) gives the full 32 = the 16 PLUS the
     wrong-chirality (4,1,2)+(4bar,2,1). Only the connected G_PS keeps 16.

=> (a) and (b) are ONE structure: a single connected left-right-symmetric group
in which B-L lives inside SU(4) AND the SU(4) chirality is tied to weak handedness.
That is a sharp, falsifiable target (predicts nu_R, lepton=4th colour, LR symmetry),
NOT two free knobs. What stays open is purely dynamical: does an SSV order
parameter realise G_PS as a CONNECTED symmetry (4-valent junction + a chirality
lock = spacetime spin) rather than a product. The group theory is now pinned.

Cross-checked against Pass 5 (`cp1_logse_16_assembly`): same 16, same B-L, same Y.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from cp1_logse_16_assembly import (
    b_minus_L,
    colour_minus,
    even_parity_weights,
    field_of,
    hypercharge_Y,
    odd_parity_weights,
    weak_T3,
)


# ===========================================================================
# RIGOROUS LAYER 1 -- B-L is a Cartan generator of SU(4) (lepton = 4th colour)
# ===========================================================================

def su4_b_minus_L_generator() -> list[Fraction]:
    """The B-L direction as a diagonal SU(4) generator on the fundamental 4 =
    (3 quark colours, 1 lepton). Traceless => a genuine SU(4) Cartan element."""
    return [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(-1)]


def su4_generator_is_traceless() -> bool:
    return sum(su4_b_minus_L_generator()) == 0


def four_branches_to_su3_times_bL() -> dict[str, Fraction]:
    """4 of SU(4) -> 3_{+1/3} (quarks) + 1_{-1} (lepton): the Pati-Salam content."""
    g = su4_b_minus_L_generator()
    return {"quark colour (x3) B-L": g[0], "lepton B-L (4th colour)": g[3]}


# ===========================================================================
# RIGOROUS LAYER 2 -- the left-right structure, read off the five bits
# ===========================================================================

def weak_T3R(w: tuple[int, ...]) -> float:
    """SU(2)_R isospin: pairs (u^c,d^c) and (nu^c,e^c). T3_R = (w1+w2)/4."""
    _c1, _c2, _c3, w1, w2 = w
    return (w1 + w2) / 4


def su4_rep(w: tuple[int, ...]) -> str:
    """4 (left fields Q,L: B-L in {+1/3,-1}) vs 4bar (right fields: opposite)."""
    return "4" if colour_minus(w) in (1, 3) else "4bar"


def pati_salam_irrep(w: tuple[int, ...]) -> str:
    """Assign each weight to (SU(4), SU(2)_L, SU(2)_R)."""
    is_left = abs(weak_T3(w)) > 1e-9      # SU(2)_L doublet member
    is_right = abs(weak_T3R(w)) > 1e-9    # SU(2)_R doublet member
    su2L = "2" if is_left else "1"
    su2R = "2" if is_right else "1"
    return f"({su4_rep(w)},{su2L},{su2R})"


def pati_salam_decomposition() -> dict[str, int]:
    """Tally the 16 by Pati-Salam irrep -> should be (4,2,1):8 and (4bar,1,2):8."""
    tally: dict[str, int] = {}
    for w in even_parity_weights():
        tally[pati_salam_irrep(w)] = tally.get(pati_salam_irrep(w), 0) + 1
    return tally


def chirality_lock_is_parity() -> bool:
    """The even-parity constraint c1c2c3 = w1w2 is EXACTLY '4<->left, 4bar<->right'.

    Demand (a) [B-L in SU(4)] and demand (b) [parity lock] are the SAME fact:
    4 (left fields) all have c1c2c3 = -1 = w1w2, 4bar (right) all have +1 = +1.
    """
    for w in even_parity_weights():
        colour_parity = w[0] * w[1] * w[2]
        weak_parity = w[3] * w[4]
        in_4 = su4_rep(w) == "4"
        # 4 <=> left <=> w1w2 = -1 ;  4bar <=> right <=> w1w2 = +1
        if colour_parity != weak_parity:
            return False
        if in_4 and weak_parity != -1:
            return False
        if (not in_4) and weak_parity != +1:
            return False
    return True


# ===========================================================================
# RIGOROUS LAYER 3 -- the 32 = product vs the 16 = connected
# ===========================================================================

def full_32_irreps() -> dict[str, int]:
    """16 (even) + 16bar (odd) tallied by Pati-Salam irrep = the four LR combos."""
    tally: dict[str, int] = {}
    for w in even_parity_weights() + odd_parity_weights():
        tally[pati_salam_irrep(w)] = tally.get(pati_salam_irrep(w), 0) + 1
    return tally


def wrong_chirality_irreps() -> set[str]:
    """The (4,1,2)+(4bar,2,1) the 32 has but the 16 drops -- the cost of NOT
    locking chirality (i.e. a product / vector-like spectrum)."""
    return set(full_32_irreps()) - set(pati_salam_decomposition())


# ===========================================================================
# INTERPRETIVE LAYER -- the two Pass-5 demands, now as ONE structure
# ===========================================================================

@dataclass(frozen=True)
class Demand:
    name: str
    pass5_status: str
    pass6_finding: str


def demands() -> list[Demand]:
    return [
        Demand(
            "(a) colour SU(3) -> SU(4), B-L = 4th colour",
            "NEEDS-ENLARGEMENT (looked like a free knot U(1))",
            "B-L is a Cartan GENERATOR of SU(4): diag(1/3,1/3,1/3,-1), traceless. "
            "Not beside colour -- inside it. The lepton is literally the 4th colour. "
            "In SSV: the 3-valent Y-junction (#79, SU(3)) must become 4-fold, the "
            "simple lepton loop being the 4th strand-type.",
        ),
        Demand(
            "(b) parity lock -> 16 not 32",
            "NOT-FORCED (independent colour & weak sectors)",
            "The lock c1c2c3 = w1w2 is EXACTLY the left-right chirality correlation "
            "'4 with SU(2)_L, 4bar with SU(2)_R'. It is one ZZ2, and it is the SAME "
            "ZZ2 that distinguishes a chiral (16) from a vector-like (32) spectrum. "
            "In SSV this ZZ2 is a candidate identity with the spacetime spin-1/2 / "
            "half-quantum-vortex structure #78 already requires.",
        ),
    ]


# ===========================================================================
# Report
# ===========================================================================

def main() -> None:
    print("=" * 92)
    print("PASS 6 (RIGOROUS): the 16 reconstructed as Pati-Salam SU(4)xSU(2)_LxSU(2)_R")
    print("=" * 92)

    g = su4_b_minus_L_generator()
    print(f"\n  B-L as an SU(4) generator on the 4: diag({', '.join(str(x) for x in g)})")
    print(f"    traceless (=> valid SU(4) Cartan element): "
          f"{'YES' if su4_generator_is_traceless() else 'NO'}")
    for k, v in four_branches_to_su3_times_bL().items():
        print(f"    {k:28s}: {v}")
    print("    => 4 = 3_{+1/3} (quarks) + 1_{-1} (lepton): 'lepton = 4th colour' is EXACT.")
    assert su4_generator_is_traceless()

    print("\n  16 decomposed by Pati-Salam irrep (SU(4), SU(2)_L, SU(2)_R):")
    dec = pati_salam_decomposition()
    for irr, n in sorted(dec.items()):
        print(f"    {irr:12s} : {n} states")
    assert dec == {"(4,2,1)": 8, "(4bar,1,2)": 8}
    print("    => 16 = (4,2,1) + (4bar,1,2)  [8 left + 8 right].")

    print("\n  Per-field Pati-Salam assignment (T3_L=(w1-w2)/4, T3_R=(w1+w2)/4):")
    print(f"    {'field':6s} {'irrep':12s} {'B-L':>6s} {'T3_L':>6s} {'T3_R':>6s} {'Y':>7s}")
    seen = set()
    for w in even_parity_weights():
        f = field_of(w)
        key = (f, pati_salam_irrep(w))
        if key in seen:
            continue
        seen.add(key)
        print(f"    {f:6s} {pati_salam_irrep(w):12s} {b_minus_L(w):>6.2f} "
              f"{weak_T3(w):>6.2f} {weak_T3R(w):>6.2f} {hypercharge_Y(w):>7.3f}")

    print("\n  Chirality lock test -- is parity (c1c2c3=w1w2) the SAME as '4<->L, 4bar<->R'?")
    print(f"    {'YES -- demands (a) and (b) are ONE structure' if chirality_lock_is_parity() else 'NO'}")
    assert chirality_lock_is_parity()

    print("\n  Product (32) vs connected (16):")
    full = full_32_irreps()
    for irr, n in sorted(full.items()):
        tag = "" if irr in dec else "   <- dropped by the chirality lock"
        print(f"    {irr:12s} : {n}{tag}")
    print(f"    32 = 16 + 16bar; the lock drops {sorted(wrong_chirality_irreps())}.")
    print("    A product of INDEPENDENT colour/weak sectors keeps all four -> 32 (vector-like).")
    assert full == {"(4,2,1)": 8, "(4bar,1,2)": 8, "(4,1,2)": 8, "(4bar,2,1)": 8}
    assert wrong_chirality_irreps() == {"(4,1,2)", "(4bar,2,1)"}

    print("\n" + "=" * 92)
    print("PASS 6 (INTERPRETIVE): the two Pass-5 demands collapse to ONE")
    print("=" * 92)
    for d in demands():
        print(f"\n  {d.name}")
        print(f"    Pass 5 : {d.pass5_status}")
        print(f"    Pass 6 : {d.pass6_finding}")

    print("\n" + "=" * 92)
    print("VERDICT")
    print("=" * 92)
    print("""
  The two Pass-5 impositions are NOT two free knobs -- they are one connected
  left-right-symmetric group, Pati-Salam SU(4)_c x SU(2)_L x SU(2)_R (the maximal
  subgroup of SO(10) that the 16 lands in):

    * B-L is a Cartan GENERATOR of SU(4) -- 'lepton = 4th colour' is exact, so the
      Pass-5 demand (a) is just 'colour is SU(4), not SU(3)';
    * the Pass-5 parity lock (b) is EXACTLY the left-right chirality correlation
      '4 with SU(2)_L, 4bar with SU(2)_R' -- one ZZ2, the same one separating a
      chiral 16 from a vector-like 32.

  So the minimal LogSE that can carry one generation is FORCED into a sharp,
  falsifiable shape: left-right symmetric, SU(4) colour with the lepton as the
  4th colour, an automatic right-handed neutrino, and a single chirality ZZ2.
  Nothing here is tuned per fermion; it is one group.

  WHAT REMAINS, AND IT IS PURELY DYNAMICAL: does an SSV order parameter realise
  G_PS as a CONNECTED internal symmetry rather than a product? That needs
  (i) a 4-fold junction (lepton loop = 4th strand-type) giving SU(4), and
  (ii) the chirality ZZ2 to BE the spacetime spin-1/2 / half-quantum-vortex
  structure #78 already demands -- so that internal chirality and spacetime
  handedness are locked, as they must be for a chiral theory.

  This is the genuine target for the field-theory build: not 'a CP^1 LogSE' but
  'a left-right-symmetric SU(4) order parameter whose chirality ZZ2 is its spin
  structure.' If a minimal such LogSE forces (i)+(ii) for free, it is the first
  over-constrained SSV hit. If it cannot, the scalar core needs replacing. Either
  way the group-theoretic target is now fully pinned -- the curiosity is answered:
  the 16 is reachable, but only as ONE left-right-symmetric SU(4) object.
""")


if __name__ == "__main__":
    main()

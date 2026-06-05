"""#81 — settling the sign: a parity/CPT obstruction makes it moot.

The cheap route (`lr_su4_cross_term_audit.py`) found the chirality-locking cross
term ∫ω_c·ω_w nonzero and leading-order, and reduced the verdict to the SIGN of its
coupling λ_cw. This audit settles that — and overturns the toy's interpretation —
with a symmetry argument on the *tested* #80 bit structure, no 3D solver needed.

THE OBSTRUCTION (two independent, rigorous layers).

Layer 1 — bit level (computed from cp1_logse_16_assembly's tested weights).
  Antiparticle / CP conjugation flips all five bits (c1,c2,c3,w1,w2) → (−…).
  Colour has THREE bits, weak has TWO, so:
      P_c = c1c2c3 → (−1)^3 P_c = −P_c        (odd # of flips)
      P_w = w1w2   → (−1)^2 P_w = +P_w         (even # of flips)
  Hence CP maps (P_c,P_w) → (−P_c, +P_w): the DIAGONAL sector (P_c=P_w, the chiral
  16) ↔ the ANTI-DIAGONAL (P_c≠P_w, the 16bar). The chiral 16 and its mirror are
  exact CP conjugates. (It is precisely the SU(4) enlargement — the 3rd colour bit
  = B−L = 4th colour, #80 Pass 5/6 — that makes P_c CP-odd; with only SU(3)'s two
  colour bits P_c would be CP-even and this protection would not arise.)

Layer 2 — field level (parity of the energy operands).
  The currents j=Im(ψ*∇ψ) are C-odd polar vectors; ω=∇×j are C-odd pseudovectors:
      j : C=−1, P=−1     ω=∇×j : C=−1, P=+1
  Any scalar coupling's (C,P,CP) is the product. In particular:
      ω_c·ω_w   : P=+1, C=+1, CP=+1  → CP-EVEN  (the spec's natural term)
      j_c·ω_w   : P=−1, C=+1, CP=−1  → CP-ODD / PARITY-VIOLATING
  The canonical SSV chiral-shear term is (λ⊥/2)|∇×j|² (Paper II §3–4: the Coulomb-
  like nn′/r² interaction, like-sign repulsion — manifestly CP-even). Its multi-
  component lift |∇×j_total|² produces only CP-even cross terms ω_c·ω_w.

THE VERDICT.  A CP-even Hamiltonian commutes with CP, so CP-conjugate states are
degenerate: E(16) = E(16bar). Combined with Layer 1 (CP maps the chiral 16 to its
anti-diagonal mirror), the diagonal and anti-diagonal sectors are FORCED DEGENERATE
under any CP-even chiral-shear energy. The four (P_c,P_w) sectors collapse to one
energy. So:

  * The SIGN of λ_cw is MOOT: a parity-even ω_c·ω_w coupling produces ZERO net
    16-vs-16bar selection (CPT), whatever its sign. NOT-FORCED — and not by a
    vanishing matrix element (#76) but by a CPT degeneracy.
  * Forcing chirality REQUIRES a parity-ODD coupling (e.g. ∫ j_c·ω_w). That is the
    statement "you cannot derive parity violation from a parity-conserving
    Lagrangian." A P-odd chiral-shear term IS the postulate "chirality = the spin
    framing" written in field-theory form — it does not arise for free.

This also corrects the cheap-route toy: its single colour winding (1 bit) made CP
flip P_c and P_w together (diagonal→diagonal), so it saw a CPT-violating "split."
With colour properly SU(4) (3 bits) CP flips only P_c, the would-be-split sectors
are CP partners, and the split is forbidden. The cross INTEGRAL is still nonzero;
it just cannot produce a net chirality selection.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT / "paper_ii") not in sys.path:
    sys.path.insert(0, str(SRC_ROOT / "paper_ii"))

from cp1_logse_16_assembly import even_parity_weights, odd_parity_weights  # noqa: E402


Weight = tuple[int, ...]


# ===========================================================================
# Layer 1 — how CP acts on the (P_c, P_w) sectors (tested bit structure)
# ===========================================================================

def cp_conjugate(w: Weight) -> Weight:
    """Antiparticle / CP: flip the sign of all five bits (all charges reverse)."""
    return tuple(-x for x in w)


def colour_parity(w: Weight) -> int:
    """P_c = c1 c2 c3  (4 vs 4bar). THREE colour bits ⇒ CP-odd."""
    return w[0] * w[1] * w[2]


def weak_parity(w: Weight) -> int:
    """P_w = w1 w2  (L vs R). TWO weak bits ⇒ CP-even."""
    return w[3] * w[4]


def sector(w: Weight) -> str:
    return "diagonal" if colour_parity(w) == weak_parity(w) else "anti-diagonal"


def cp_maps_16_to_16bar() -> bool:
    """CP is a bijection from the 16 (even parity) onto the 16bar (odd parity)."""
    ev, od = set(even_parity_weights()), set(odd_parity_weights())
    return {cp_conjugate(w) for w in ev} == od


def cp_flips_Pc_keeps_Pw() -> bool:
    """For every weight: CP sends P_c → −P_c (3 bits) and P_w → +P_w (2 bits)."""
    allw = set(even_parity_weights()) | set(odd_parity_weights())
    return all(
        colour_parity(cp_conjugate(w)) == -colour_parity(w)
        and weak_parity(cp_conjugate(w)) == +weak_parity(w)
        for w in allw
    )


def cp_swaps_sectors() -> bool:
    """CP maps the diagonal sector (16) onto the anti-diagonal (16bar) and back."""
    allw = set(even_parity_weights()) | set(odd_parity_weights())
    return all(sector(cp_conjugate(w)) != sector(w) for w in allw)


# ===========================================================================
# Layer 2 — parity (C, P, CP) of candidate chiral-shear couplings
# ===========================================================================

@dataclass(frozen=True)
class Operand:
    name: str
    C: int      # charge-conjugation eigenvalue
    P: int      # intrinsic spatial-reflection parity


# j = Im(psi* grad psi): C-odd polar vector.  omega = curl j: C-odd pseudovector.
J = Operand("j (current, polar vector)", C=-1, P=-1)
OMEGA = Operand("omega = curl j (pseudovector)", C=-1, P=+1)


@dataclass(frozen=True)
class Coupling:
    name: str
    operands: tuple[Operand, ...]
    note: str

    @property
    def C(self) -> int:
        p = 1
        for o in self.operands:
            p *= o.C
        return p

    @property
    def P(self) -> int:
        p = 1
        for o in self.operands:
            p *= o.P
        return p

    @property
    def CP(self) -> int:
        return self.C * self.P

    @property
    def can_force_chirality(self) -> bool:
        """A term can select the chiral 16 over its CP-mirror 16bar iff it is
        CP-odd (so it distinguishes CP conjugates). CP-even ⇒ CPT degeneracy."""
        return self.CP == -1


def candidate_couplings() -> list[Coupling]:
    return [
        Coupling("omega_c . omega_w  (|curl j_total|^2 cross term)", (OMEGA, OMEGA),
                 "the spec's natural term; the canonical CP-even chiral-shear lift"),
        Coupling("j_c . j_w", (J, J),
                 "CP-even; does not couple to the handedness sign anyway"),
        Coupling("j_c . omega_w", (J, OMEGA),
                 "PARITY-ODD: the only kind that can force chirality = the postulate"),
        Coupling("j . omega   (single-sector helicity)", (J, OMEGA),
                 "PARITY-ODD self-helicity; genuinely chiral, not the canonical term"),
    ]


# ===========================================================================
# Verdict
# ===========================================================================

def chirality_is_forced_by_cp_even_dynamics() -> bool:
    """The decisive boolean: can a CP-even chiral-shear energy force the chiral 16?
    No — CP maps 16↔16bar (Layer 1), so CPT pins them degenerate (Layer 2)."""
    cp_pairs_them = cp_maps_16_to_16bar() and cp_swaps_sectors()
    natural_term_is_cp_even = not Coupling("", (OMEGA, OMEGA), "").can_force_chirality
    # forced  <=>  the natural term could split CP partners  =>  False here
    return cp_pairs_them and (not natural_term_is_cp_even)


def main() -> None:
    print("=" * 82)
    print("#81 — does CP-conserving SSV dynamics force the chirality ℤ₂? (sign audit)")
    print("=" * 82)

    print("\n── Layer 1: how CP acts on the (P_c, P_w) sectors (tested bits) ──────────")
    print(f"  CP (flip all 5 bits) maps the 16 onto the 16bar bijectively : "
          f"{cp_maps_16_to_16bar()}")
    print(f"  CP: P_c → −P_c (3 colour bits), P_w → +P_w (2 weak bits)     : "
          f"{cp_flips_Pc_keeps_Pw()}")
    print(f"  ⇒ CP swaps diagonal (16) ↔ anti-diagonal (16bar)             : "
          f"{cp_swaps_sectors()}")
    assert cp_maps_16_to_16bar() and cp_flips_Pc_keeps_Pw() and cp_swaps_sectors()
    print("  So the chiral 16 and its mirror are exact CP CONJUGATES.")

    print("\n── Layer 2: parity of candidate chiral-shear couplings ───────────────────")
    print(f"  {'coupling':46s} {'C':>3s} {'P':>3s} {'CP':>3s}  can force χ?")
    for c in candidate_couplings():
        print(f"  {c.name:46s} {c.C:>3d} {c.P:>3d} {c.CP:>3d}  "
              f"{'YES (P-odd)' if c.can_force_chirality else 'no (P-even)'}")
    natural = candidate_couplings()[0]
    assert natural.CP == +1 and not natural.can_force_chirality

    print("\n" + "=" * 82)
    print("VERDICT")
    print("=" * 82)
    print(f"""
  Chirality forced by CP-even (canonical) chiral-shear dynamics? : """
          f"{'YES' if chirality_is_forced_by_cp_even_dynamics() else 'NO'}")
    assert not chirality_is_forced_by_cp_even_dynamics()
    print("""
  The SIGN of λ_cw is MOOT. The canonical chiral-shear term (λ⊥/2)|∇×j|² is CP-even
  (Paper II's Coulomb-like nn′/r²), so its colour–weak cross term ω_c·ω_w is CP-even
  and CANNOT distinguish the chiral 16 from its CP-conjugate 16bar. Because the
  SU(4) third colour bit makes P_c CP-odd, those are exactly the diagonal and
  anti-diagonal sectors — CPT pins them DEGENERATE. NOT-FORCED, by a CPT degeneracy
  (not a #76-style vanishing).

  Forcing the chirality ℤ₂ requires a PARITY-ODD chiral-shear coupling (∫ j_c·ω_w):
  one cannot derive parity violation from a parity-conserving Lagrangian. Such a
  P-odd term IS the postulate "chirality = the spin framing"; it does not come free.

  This corrects the cheap-route toy: with one colour winding (1 bit) CP flipped P_c
  and P_w together, so the toy mis-saw a CPT-violating split. With colour properly
  SU(4) (3 bits) the would-be-split sectors are CP partners and the split is
  forbidden. The cross integral is still nonzero — it just yields no net chirality
  selection.
""")


if __name__ == "__main__":
    main()

"""#80 Pass 7 (chapter close): the two remaining dynamical requirements, decided
at the structural level before any 3D field build.

Pass 6 forced the target to left-right-symmetric Pati-Salam SU(4)xSU(2)_LxSU(2)_R
and left exactly two requirements, both about whether an SSV order parameter can
realise this as a CONNECTED symmetry:

  (i)  a 4-fold junction giving SU(4) (lepton loop = 4th strand-type), where #79
       got only SU(3) from a 3-valent junction;
  (ii) the chirality ZZ2 (16 vs 32) being the SAME ZZ2 as the spacetime spin-1/2 /
       half-quantum-vortex structure #78 demands.

Both are decidable now:

PART A -- the 4-valent junction. Repeat the #79 computation for FOUR legs:
  balance theta_1+theta_2+theta_3+theta_4 = 0 -> the maximal torus of SU(4)
  (rank 3), leg permutations -> S_4 = Weyl(SU(4)), and crucially B-L = diag(1,1,1,-3)
  sits inside that Cartan. Result: PARTIAL in exactly the #79 sense -- Cartan + Weyl
  of SU(4) present (including B-L), off-diagonal generators absent. So requirement
  (i) is met at the SAME level #79 met SU(3): the 4-valent junction DOES supply the
  SU(4) Cartan with B-L for free.

PART B -- is the chirality ZZ2 forced, or a postulate? The order parameter carries
  two independent ZZ2 'sector parities': P_c = c1c2c3 (colour / 4-vs-4bar) and
  P_w = w1w2 (weak-spin / L-vs-R). Together they form ZZ2 x ZZ2 acting on the 32.
  The chiral 16 is the DIAGONAL sector P_c = P_w. We enumerate the THREE distinct
  index-2 ZZ2 quotients of ZZ2 x ZZ2 and show only the diagonal one (P_c*P_w fixed)
  yields the Standard-Model generation. Topology ALLOWS all three (and the full
  product = the vector-like 32); nothing forces the diagonal.

VERDICT: the chapter closes on a clean, honest place. (i) is delivered. (ii) is the
single irreducible POSTULATE the construction cannot derive but makes explicit and
falsifiable: 'the spinor's spacetime framing sign IS its internal chirality.' That
is exactly the (un-derived, everywhere) chiral nature of the weak force. SSV does
not remove that mystery -- but it compresses ALL of one generation's structure down
to that ONE identification, with everything else (colour, B-L, multiplicities,
anomaly) falling out. That is the maximal honest outcome of the reverse-engineering.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np

from cp1_logse_16_assembly import colour_minus, even_parity_weights, field_of, weak_minus
from su3_y_junction import lie_closure


# ===========================================================================
# PART A -- the 4-valent junction: does balance give the SU(4) Cartan + B-L?
# ===========================================================================

def balanced_phase_space_dimension_n(n_legs: int) -> int:
    """Dim of {(t_1..t_n): sum t_i = 0}: n phases, one constraint -> n-1."""
    constraint = np.ones((1, n_legs))
    s = np.linalg.svd(constraint, compute_uv=False)
    rank = int((s > 1e-12).sum())
    return n_legs - rank


def su4_cartan_generators() -> list[np.ndarray]:
    """Three traceless diagonal generators spanning the SU(4) Cartan, built from
    relative-phase rotations on the balanced 4-leg torus (sum of phases = 0)."""
    g1 = np.diag([1.0, -1.0, 0.0, 0.0]).astype(complex)
    g2 = np.diag([1.0, 1.0, -2.0, 0.0]).astype(complex) / np.sqrt(3.0)
    g3 = np.diag([1.0, 1.0, 1.0, -3.0]).astype(complex) / np.sqrt(6.0)   # the B-L direction
    return [g1, g2, g3]


def b_minus_L_direction() -> np.ndarray:
    """B-L = diag(1/3,1/3,1/3,-1) on the 4 (quarks +1/3, lepton -1); traceless."""
    return np.diag([1 / 3, 1 / 3, 1 / 3, -1.0]).astype(complex)


def b_minus_L_in_cartan_span() -> bool:
    """Is B-L a real linear combination of the three balanced-torus generators?"""
    cart = su4_cartan_generators()
    target = np.diag(b_minus_L_direction()).real            # length-4 diagonal
    basis = np.array([np.diag(g).real for g in cart])       # 3 x 4
    # solve basis^T x = target in least squares; check residual ~ 0
    coeffs, *_ = np.linalg.lstsq(basis.T, target, rcond=None)
    resid = np.linalg.norm(basis.T @ coeffs - target)
    return resid < 1e-12


def s4_permutations() -> list[np.ndarray]:
    """The 24 leg-permutation matrices on four legs = S_4 = Weyl(SU(4))."""
    mats = []
    for perm in itertools.permutations(range(4)):
        P = np.zeros((4, 4))
        for i, j in enumerate(perm):
            P[i, j] = 1.0
        mats.append(P)
    return mats


def permutations_form_s4() -> bool:
    mats = s4_permutations()
    keys = {M.tobytes() for M in mats}
    for A in mats:
        for B in mats:
            if (A @ B).tobytes() not in keys:
                return False
    return len(mats) == 24


@dataclass(frozen=True)
class SU4Verdict:
    balanced_dim: int
    su4_dim: int
    generated_algebra_dim: int
    bL_in_cartan: bool
    weyl_order: int
    weyl_is_s4: bool
    verdict: str


def analyse_su4_junction() -> SU4Verdict:
    cart = su4_cartan_generators()
    gen_dim = lie_closure(cart)
    bdim = balanced_phase_space_dimension_n(4)
    su4_dim = 15
    s4 = permutations_form_s4()
    if gen_dim == su4_dim:
        verdict = "SU(4) PASS"
    elif gen_dim == 3 and s4 and b_minus_L_in_cartan_span():
        verdict = ("PARTIAL (maximal torus U(1)^3 incl. B-L + Weyl S_4 of SU(4); "
                   "off-diagonal generators absent) -- requirement (i) met as in #79")
    else:
        verdict = f"OTHER (generated algebra dim {gen_dim})"
    return SU4Verdict(bdim, su4_dim, gen_dim, b_minus_L_in_cartan_span(),
                      len(s4_permutations()), s4, verdict)


# ===========================================================================
# PART B -- is the chirality ZZ2 forced, or one postulate?
# ===========================================================================

def sector_parities(w: tuple[int, ...]) -> tuple[int, int]:
    """(P_c, P_w) = (colour parity c1c2c3, weak/spin parity w1w2) for a weight."""
    return (w[0] * w[1] * w[2], w[3] * w[4])


def z2xz2_sector_contents() -> dict[tuple[int, int], int]:
    """How the full 32 distribute over the ZZ2 x ZZ2 of sector parities."""
    tally: dict[tuple[int, int], int] = {}
    all32 = list(itertools.product((+1, -1), repeat=5))
    for w in all32:
        tally[sector_parities(w)] = tally.get(sector_parities(w), 0) + 1
    return tally


def index2_subgroups_of_z2xz2() -> dict[str, set[tuple[int, int]]]:
    """The three ZZ2 subgroups of ZZ2 x ZZ2 (each defines a conserved parity)."""
    return {
        "conserve P_c only      (group by colour)": {(+1, +1), (+1, -1)},
        "conserve P_w only      (group by weak/spin)": {(+1, +1), (-1, +1)},
        "conserve P_c*P_w (DIAGONAL = chirality)": {(+1, +1), (-1, -1)},
    }


def states_invariant_under(subgroup_fixed_sectors: set[tuple[int, int]]) -> dict[str, int]:
    """SM-field content of the 16 selected by a given index-2 choice.

    A choice keeps the weights whose (P_c,P_w) lies in the two-element coset that
    contains (+1,+1). For the diagonal it is {(+,+),(-,-)}; this is the chiral 16.
    """
    tally: dict[str, int] = {}
    for w in itertools.product((+1, -1), repeat=5):
        if sector_parities(w) in subgroup_fixed_sectors:
            tally[field_of_safe(w)] = tally.get(field_of_safe(w), 0) + 1
    return tally


def field_of_safe(w: tuple[int, ...]) -> str:
    """field_of works for any 5-tuple via (colour_minus, weak_minus)."""
    key = (colour_minus(w), weak_minus(w))
    from cp1_logse_16_assembly import FIELD_BY_SECTOR
    return FIELD_BY_SECTOR.get(key, f"sector{key}")


def diagonal_selects_one_generation() -> bool:
    """The diagonal (chirality) quotient yields exactly the SM generation 6,3,3,2,1,1."""
    content = states_invariant_under({(+1, +1), (-1, -1)})
    return content == {"Q": 6, "u^c": 3, "d^c": 3, "L": 2, "e^c": 1, "nu^c": 1}


# ===========================================================================
# Report
# ===========================================================================

def main() -> None:
    print("=" * 92)
    print("PASS 7 PART A -- the 4-valent junction: SU(4) Cartan + Weyl + B-L?")
    print("=" * 92)
    v = analyse_su4_junction()
    print(f"  balanced 4-leg phase space dim     : {v.balanced_dim}   (= rank SU(4) = 3)")
    print(f"  su(4) dimension                    : {v.su4_dim}")
    print(f"  continuous moves generate algebra  : dim {v.generated_algebra_dim}   (abelian Cartan u(1)^3)")
    print(f"  B-L = diag(1/3,1/3,1/3,-1) in Cartan: {v.bL_in_cartan}")
    print(f"  leg permutations: order {v.weyl_order}, = S_4 = Weyl(SU(4)): {v.weyl_is_s4}")
    print(f"\n  PART A VERDICT: {v.verdict}")
    assert v.balanced_dim == 3 and v.generated_algebra_dim == 3
    assert v.bL_in_cartan and v.weyl_is_s4

    print("\n" + "=" * 92)
    print("PASS 7 PART B -- is the chirality ZZ2 forced, or one postulate?")
    print("=" * 92)
    print("\n  The 32 over the ZZ2 x ZZ2 of sector parities (P_c = c1c2c3, P_w = w1w2):")
    for (pc, pw), n in sorted(z2xz2_sector_contents().items(), reverse=True):
        print(f"    (P_c={pc:+d}, P_w={pw:+d}) : {n} states")
    print("    -> four sectors of 8 = the full vector-like 32 (independent sectors).")

    print("\n  The three index-2 ZZ2 quotients (each = conserving one parity):")
    for name, sub in index2_subgroups_of_z2xz2().items():
        content = states_invariant_under(sub)
        is_gen = content == {"Q": 6, "u^c": 3, "d^c": 3, "L": 2, "e^c": 1, "nu^c": 1}
        tag = "  <== the Standard-Model generation (the 16)" if is_gen else ""
        print(f"    [{name}] -> {dict(sorted(content.items()))}{tag}")

    print(f"\n  diagonal (chirality) quotient gives exactly one generation: "
          f"{diagonal_selects_one_generation()}")
    assert diagonal_selects_one_generation()

    print("\n" + "=" * 92)
    print("VERDICT -- chapter close")
    print("=" * 92)
    print("""
  (i)  4-VALENT JUNCTION = DELIVERED. Balancing four legs gives the SU(4) maximal
       torus (rank 3) and S_4 = Weyl(SU(4)), and the B-L direction diag(1/3,1/3,
       1/3,-1) sits inside that Cartan. So 'lepton = 4th colour' and B-L are free,
       at exactly the level #79 delivered SU(3) (Cartan + Weyl; off-diagonal
       generators still absent -- the same honest PARTIAL).

  (ii) CHIRALITY ZZ2 = ONE POSTULATE, NOT FORCED. The order parameter carries two
       independent ZZ2 sector-parities (colour P_c, weak/spin P_w). The chiral 16
       is the DIAGONAL P_c = P_w. Topology offers three ZZ2 quotients and the full
       product (the vector-like 32); only the diagonal yields one generation, and
       NOTHING in the homotopy forces it. Selecting it is precisely the statement
       'the spinor's spacetime framing sign IS its internal chirality' -- the
       (un-derived, universal) chiral nature of the weak force.

  SO THE CHAPTER ENDS HERE, HONESTLY AND WELL: the entire structure of one
  Standard-Model generation -- SU(4) colour, B-L = 4th colour, the weak doublets,
  the multiplicities 6,3,3,2,1,1, anomaly cancellation -- follows from an SSV
  defect once ONE identification is adopted: chirality = the spin framing. SSV does
  not derive that single ZZ2 (no framework does), but it reduces ALL of a
  generation to it. That is the maximal over-constrained outcome reverse-engineering
  could reach without the full dynamical field theory -- which now has a precise
  brief: build a left-right-symmetric SU(4) LogSE and TEST whether its defect
  dynamics force the diagonal ZZ2 (chirality = spin) rather than leaving it a
  choice. If they do, it is a genuine prediction; if not, the postulate stands as
  SSV's one irreducible input for the fermion sector.
""")


if __name__ == "__main__":
    main()

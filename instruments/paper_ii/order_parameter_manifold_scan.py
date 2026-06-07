"""#80: reverse-engineer the SSV order-parameter manifold from the SM targets.

Two decidable passes:

Pass 1 — homotopy/symmetry triage. For each candidate order-parameter manifold M,
tabulate (pi_1, pi_2, pi_3) and the symmetry group acting, and score which
defect / gauge targets it can host. Surface the structural tensions.

Pass 2 — over-constraint test in representation theory. Hitting the full gauge
group from independent product factors is NOT over-constrained (one choice per
group). Genuine over-constraint = a unifying group whose single irrep gives one
anomaly-free SM generation. Checked by explicit cubic-anomaly arithmetic for the
canonical candidates SU(5) (5bar + 10) and SO(10) (16).

All homotopy groups used are standard textbook results (encoded, not computed);
the anomaly coefficients are computed from the standard SU(N) index formulae.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Pass 1: candidate manifolds, standard homotopy + acting symmetry
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Manifold:
    name: str
    pi1: str
    pi2: str
    pi3: str
    symmetry: str          # continuous group acting (isometry / internal symmetry)
    dim: int
    n_choices: int         # how many independent structural choices to specify M


# Standard homotopy groups (textbook): products use pi_n(A x B) = pi_n(A) (+) pi_n(B).
MANIFOLDS = [
    Manifold("S^1 = U(1)            (current scalar SSV)", "Z", "0", "0", "U(1)", 1, 1),
    Manifold("S^2 = CP^1 = SU(2)/U(1)", "0", "Z", "Z", "SU(2)", 2, 1),
    Manifold("S^3 = SU(2)", "0", "0", "Z", "SU(2)xSU(2)", 3, 1),
    Manifold("SO(3) = RP^3", "Z2", "0", "Z", "SU(2)", 3, 1),
    Manifold("CP^2 = SU(3)/U(2)", "0", "Z", "0", "SU(3)", 4, 1),
    Manifold("SU(3)", "0", "0", "Z", "SU(3)xSU(3)", 8, 1),
    Manifold("flag SU(3)/T^2", "0", "Z+Z", "0", "SU(3)", 6, 1),
    Manifold("S^1 x CP^1            (phase x weak isospin)", "Z", "Z", "Z", "U(1)xSU(2)", 3, 2),
    Manifold("S^1 x CP^2            (phase x colour)", "Z", "Z", "0", "U(1)xSU(3)", 5, 2),
    Manifold("S^1 x CP^1 x CP^2     (phase x weak x colour)", "Z", "Z+Z", "Z", "U(1)xSU(2)xSU(3)", 7, 3),
    Manifold("SO(3) x CP^2          (spin x colour)", "Z2", "Z", "Z", "SU(2)xSU(3)", 7, 2),
]


# Targets, with the decidable condition each manifold must satisfy to "host" it.
def score_targets(m: Manifold) -> dict[str, bool]:
    pi1_has_Z = "Z" in m.pi1 and "Z2" not in m.pi1.replace("Z2", "")
    pi1_is_Z = m.pi1 == "Z"
    pi1_has_Z2 = "Z2" in m.pi1
    pi2_has_Z = "Z" in m.pi2
    pi3_has_Z = "Z" in m.pi3
    sym = m.symmetry
    return {
        "U(1) gauge / EM (twist, integer winding)": pi1_is_Z or "U(1)" in sym,
        "SU(2) gauge / weak": "SU(2)" in sym,
        "SU(3) gauge / colour (off-diag generators)": "SU(3)" in sym,
        "integer winding (lepton/pion)": pi1_is_Z,
        "half-winding / spin-1/2 (muon, HQV)": pi1_has_Z2,
        "skyrmion / 2D texture (pi_2)": pi2_has_Z,
        "baryon (Skyrme, pi_3)": pi3_has_Z,
    }


# ---------------------------------------------------------------------------
# Pass 2: anomaly-cancellation over-constraint (SU(N) cubic anomaly arithmetic)
# ---------------------------------------------------------------------------

def su_n_anomaly(rep: str, N: int) -> int:
    """Cubic gauge-anomaly coefficient A(R) for low SU(N) reps, normalised A(N)=+1.

    Standard results:
      A(fundamental N)            = +1
      A(antifundamental Nbar)     = -1
      A(2-index antisymmetric)    = N - 4
      A(2-index antisym bar)      = -(N - 4)
    """
    if rep == "N":
        return 1
    if rep == "Nbar":
        return -1
    if rep == "antisym2":          # the "10" of SU(5) is the 2-index antisymmetric
        return N - 4
    if rep == "antisym2bar":
        return -(N - 4)
    raise ValueError(rep)


@dataclass
class UnifyingCandidate:
    group: str
    generation_irrep: str
    anomaly: int
    anomaly_free: bool
    contains_one_generation: bool
    by_hand: bool          # True if anomaly cancellation requires hand-tuned charges
    note: str


def check_unifying_groups() -> list[UnifyingCandidate]:
    out = []

    # SU(5): one generation = 5bar + 10 (10 = 2-index antisymmetric of SU(5))
    a_5bar = su_n_anomaly("Nbar", 5)
    a_10 = su_n_anomaly("antisym2", 5)
    total = a_5bar + a_10
    out.append(UnifyingCandidate(
        group="SU(5)",
        generation_irrep="5bar + 10",
        anomaly=total,
        anomaly_free=(total == 0),
        contains_one_generation=True,
        by_hand=False,
        note=f"A(5bar)={a_5bar}, A(10)={a_10}; sum={total}. "
             "5bar+10 = exactly one SM generation (15 Weyl fermions).",
    ))

    # SO(10): no cubic gauge anomaly for SO(N>6); 16-spinor = one generation + nu_R.
    out.append(UnifyingCandidate(
        group="SO(10)",
        generation_irrep="16 (spinor)",
        anomaly=0,
        anomaly_free=True,
        contains_one_generation=True,
        by_hand=False,
        note="SO(N) with N != 6 has identically vanishing cubic anomaly; "
             "the 16 spinor = one SM generation + right-handed neutrino, automatically anomaly-free.",
    ))

    # Counter-example: a hand-built product gauge group does NOT auto-cancel;
    # the SM U(1)xSU(2)xSU(3) needs the specific hypercharge assignment by hand.
    out.append(UnifyingCandidate(
        group="U(1)xSU(2)xSU(3) (product, no unification)",
        generation_irrep="SM fields with hypercharges put in by hand",
        anomaly=0,
        anomaly_free=True,
        contains_one_generation=True,
        by_hand=True,
        note="Anomaly-free ONLY after the hypercharges are chosen to cancel "
             "[U(1)]^3, [U(1)][SU(2)]^2, [U(1)][SU(3)]^2, grav-[U(1)]; "
             "i.e. inserted, not derived. This is the over-fitting baseline.",
    ))
    return out


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def main() -> None:
    targets = list(score_targets(MANIFOLDS[0]).keys())

    print("=" * 100)
    print("PASS 1 — homotopy / symmetry triage of candidate order-parameter manifolds")
    print("=" * 100)
    header = f"{'manifold':40s} {'pi1':>5s} {'pi2':>4s} {'pi3':>4s} {'symmetry':>16s} {'#ch':>3s} {'hits':>4s}"
    print(header)
    print("-" * 100)
    for m in MANIFOLDS:
        s = score_targets(m)
        hits = sum(s.values())
        print(f"{m.name:40s} {m.pi1:>5s} {m.pi2:>4s} {m.pi3:>4s} {m.symmetry:>16s} "
              f"{m.n_choices:>3d} {hits:>3d}/{len(targets)}")

    print("\nTarget-by-target (which manifold first supplies each):")
    for t in targets:
        hosts = [m.name.split()[0] for m in MANIFOLDS if score_targets(m)[t]]
        print(f"  - {t:48s}: {', '.join(hosts[:6])}")

    print("\nStructural tensions:")
    print("  * integer winding needs pi_1 = Z (leptons/pion); spin-1/2 & HQV need pi_1 = Z2.")
    print("    No connected IRREDUCIBLE manifold has both -> forces a PRODUCT (overall U(1) phase")
    print("    x internal SO(3)/spinor), e.g. S^1 x SO(3) x CP^2.")
    print("  * Full U(1)xSU(2)xSU(3) appears only for product manifolds with #choices = 3")
    print("    (one factor per gauge group) -> NOT over-constrained: this is the SM relabelled.")

    print("\n" + "=" * 100)
    print("PASS 2 — over-constraint test: does ONE irrep of a unifying group give")
    print("         one anomaly-free SM generation? (the real derivation/fit discriminator)")
    print("=" * 100)
    for c in check_unifying_groups():
        flag = ("OVER-CONSTRAINED" if (c.anomaly_free and c.contains_one_generation
                                       and not c.by_hand) else "fitted / by-hand")
        print(f"\n  {c.group}")
        print(f"    one generation = {c.generation_irrep}")
        print(f"    anomaly sum = {c.anomaly}  ({'cancels' if c.anomaly_free else 'does NOT cancel'})")
        print(f"    -> {flag}")
        print(f"    {c.note}")

    print("\n" + "=" * 100)
    print("PASS 3 — verdict")
    print("=" * 100)
    print("""
  Topology (Pass 1) is NECESSARY but NOT SUFFICIENT:
    - it fixes which DEFECTS exist (winding, HQV, skyrmion, baryon) and which
      continuous symmetry can act, but the full gauge group only appears for a
      hand-assembled product (one manifold factor per group = not over-constrained);
    - the integer-vs-Z2 winding tension forces a product 'overall phase x internal'
      structure, which is informative but still a CHOICE per sector.

  The genuine over-constraint (Pass 2) lives in REPRESENTATION THEORY:
    - SU(5): 5bar+10 has anomaly sum 0 -> one anomaly-free generation from a fixed
      irrep set (NOT one knob per fermion);
    - SO(10): the single 16 spinor is automatically anomaly-free and IS one
      generation + nu_R -> the maximal over-constraint (one irrep -> one generation,
      anomaly cancellation free).

  CONCLUSION FOR SSV:
    Reverse-engineering from the order-parameter MANIFOLD alone cannot over-constrain
    the answer -- it reproduces defects + gauge groups but with one structural choice
    per gauge factor. The over-constraint that separates 'derivation' from 'SM
    relabelled' is anomaly cancellation, which is a fact about the REP CONTENT of a
    UNIFYING group (SU(5)/SO(10)-type), not about the manifold's homotopy.

    So the honest target of the reverse-engineering is: an SSV internal symmetry whose
    defect/texture sectors carry a single unifying-group irrep (SO(10)-16-like) per
    generation. Until an SSV defect is shown to transform as such an irrep with the
    anomaly falling out, the multi-component order parameter remains a FIT (SM in
    superfluid notation), not a derivation. This is the decidable next test.
""")


if __name__ == "__main__":
    main()

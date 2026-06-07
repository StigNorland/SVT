"""#connected-SU(4) cheap route: are the off-diagonal SU(4) generators dynamical
symmetries (connected colour) or absent (colour = labels = product)?

Spec: papers/SSV-II/connected-su4-offdiagonal-test-spec.md. The colour-sector twin
of the spinor decision #83. #79/#80 delivered only the Cartan + Weyl of SU(4) from
the junction (`lie_closure` on the junction Cartan = 3 = u(1)^3, not 15 = su(4)).
The open question: do the 12 OFF-DIAGONAL generators (the ladder operators rotating
one colour into another, incl. quark↔lepton since lepton = 4th colour) survive as
genuine symmetries of the SSV chiral-shear dynamics?

THE TEST, made cheap.  In the multi-component realisation (z ∈ C^4, shared density
ρ = Σ|z_a|², LogSE skeleton + chiral-shear L_perp; see lr-su4-logse-spec.md), the
gradient term and the log potential already see only ρ, so they are SU(4)-invariant.
Connectivity therefore hinges ENTIRELY on what current the chiral-shear L_perp is
built from:

  TOTAL-current form :  j_total = Im(z† ∇z) = Σ_a Im(z_a* ∇z_a)      (one current)
  SECTOR-current form:  {j_a = Im(z_a* ∇z_a)}_a , E_perp = Σ_a |∇×j_a|²

KEY FACT (the whole audit).  The scalar SSV current j = Im(ψ*∇ψ) is the Noether
current of the field's overall U(1). Its UNIQUE multi-component generalisation is the
overall-U(1) Noether current j_total = Im(z† ∇z) — NOT a set of per-colour currents
(individual z_a* ∇z_a are not separately conserved; there is one condensate, one
U(1)). And j_total is EXACTLY SU(4)-invariant: under z → U z (U ∈ SU(4), constant),
z† ∇z → z† U† U ∇z = z† ∇z. So the natural chiral-shear term is SU(4)-invariant, the
off-diagonal generators are exact symmetries, and lie_closure of the realised
symmetry = 15 = su(4): CONNECTED — and for FREE (no extra term needed).

The sector-current form is invariant only under diagonal phase rotations (Cartan)
and permutations (Weyl) — lie_closure of its continuous symmetries = 3 = u(1)^3:
PRODUCT. It is the un-natural choice (per-colour currents that the scalar theory has
no analogue of).

WHAT THIS DECIDES, AND WHAT IT DOESN'T.  Connectivity reduces to a FOUNDATIONAL
choice identical in kind to #81/#83: realise colour as a genuine internal multiplet
(z ∈ C^4) or not.
  * In the JUNCTION realisation (native scalar SSV, #79/#80): there is no fundamental
    C^4; colour-i → colour-j is a reconnection (a TOPOLOGY change), not a continuous
    rotation, so the off-diagonal generator is simply absent from the continuous
    dynamics → lie_closure = 3 → PRODUCT. (Reproduces #79/#80.)
  * In the MULTIPLET realisation (the #83-type internal-orientation upgrade): the
    natural total-current L_perp is SU(4)-invariant → lie_closure = 15 → CONNECTED,
    automatically.
So: once you pay for the internal multiplet, colour connectivity is GEOMETRICALLY
FREE. This is the hopeful asymmetry vs #81: chirality needs a parity-ODD term even
after the multiplet upgrade, but colour off-diagonal symmetry does NOT — the parity-
even total-current term already delivers it.

This script proves the two lie_closure values (15 vs 3) and the SU(4)-invariance of
j_total vs the Cartan-only invariance of the sector form, using the SAME lie_closure
used for the junction in su4_junction_chirality_closure.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT / "paper_ii") not in sys.path:
    sys.path.insert(0, str(SRC_ROOT / "paper_ii"))

from su3_y_junction import lie_closure  # the same closure used for the junction


# ===========================================================================
# su(4) generators: 3 Cartan (diagonal) + 12 off-diagonal (ladder), Hermitian
# ===========================================================================

def cartan_generators() -> list[np.ndarray]:
    """Three independent traceless diagonal generators spanning the SU(4) Cartan."""
    return [
        np.diag([1.0, -1.0, 0.0, 0.0]).astype(complex),
        np.diag([0.0, 1.0, -1.0, 0.0]).astype(complex),
        np.diag([0.0, 0.0, 1.0, -1.0]).astype(complex),
    ]


def offdiagonal_generators() -> list[np.ndarray]:
    """The 12 off-diagonal su(4) generators: for each i<j, the real (E_ij+E_ji) and
    imaginary (-i(E_ij-E_ji)) ladder operators. T_{i4} mix quark colour i ↔ lepton."""
    gens: list[np.ndarray] = []
    for i in range(4):
        for j in range(i + 1, 4):
            x = np.zeros((4, 4), dtype=complex)
            x[i, j] = x[j, i] = 1.0
            y = np.zeros((4, 4), dtype=complex)
            y[i, j] = -1.0j
            y[j, i] = +1.0j
            gens.extend([x, y])
    return gens


def all_su4_generators() -> list[np.ndarray]:
    return cartan_generators() + offdiagonal_generators()


def b_minus_L_generator() -> np.ndarray:
    """B−L = diag(1,1,1,-3) direction (traceless) — a Cartan element (#80)."""
    return np.diag([1.0, 1.0, 1.0, -3.0]).astype(complex)


# ===========================================================================
# Currents and their invariance under an su(4) generator
# ===========================================================================

def _expm_iH(T: np.ndarray, eps: float) -> np.ndarray:
    """U = exp(i eps T) for Hermitian T, via eigendecomposition (exact)."""
    w, V = np.linalg.eigh(T)
    return V @ np.diag(np.exp(1j * eps * w)) @ V.conj().T


def total_current(z: np.ndarray, g: np.ndarray) -> float:
    """j_total = Im(z† g), the overall-U(1) Noether current (g stands in for any
    spatial-derivative component ∇z). The unique generalisation of Im(ψ*∇ψ)."""
    return float(np.imag(np.vdot(z, g)))


def sector_functional(z: np.ndarray, g: np.ndarray) -> float:
    """Σ_a |Im(z_a* g_a)|² — the per-colour (sector) current form's invariant."""
    j_a = np.imag(np.conj(z) * g)
    return float(np.sum(j_a**2))


def _is_symmetry(functional, T: np.ndarray, *, eps: float = 0.3,
                 n_samples: int = 64, tol: float = 1e-9, seed: int = 0) -> bool:
    """Is `functional(z, g)` invariant under z,g → U z, U g for U = exp(i eps T),
    for ALL random samples? (A constant SU(4) rotation acts identically on z and ∇z.)"""
    rng = np.random.default_rng(seed)
    U = _expm_iH(T, eps)
    for _ in range(n_samples):
        z = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        g = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        before = functional(z, g)
        after = functional(U @ z, U @ g)
        if abs(after - before) > tol * (1.0 + abs(before)):
            return False
    return True


def realised_symmetry_dim(functional) -> int:
    """lie_closure of the generators that leave `functional` invariant = dimension of
    the realised continuous colour symmetry algebra."""
    invariant = [T for T in all_su4_generators() if _is_symmetry(functional, T)]
    return lie_closure(invariant) if invariant else 0


# ===========================================================================
# Report
# ===========================================================================

def main() -> None:
    gens = all_su4_generators()
    cart = cartan_generators()
    offd = offdiagonal_generators()

    print("=" * 84)
    print("Connected-SU(4) cheap audit — do the off-diagonal generators survive?")
    print("=" * 84)

    print("\n── sanity: the generator set and lie_closure (same fn as the junction) ──")
    print(f"  # generators: {len(cart)} Cartan + {len(offd)} off-diagonal = {len(gens)}")
    print(f"  lie_closure(all 15)        = {lie_closure(gens):2d}   (su(4) = 15)")
    print(f"  lie_closure(3 Cartan only) = {lie_closure(cart):2d}   (u(1)^3 = 3, the #79/#80 junction answer)")
    assert lie_closure(gens) == 15
    assert lie_closure(cart) == 3

    print("\n── which current does the chiral-shear L_perp use? ─────────────────────")
    d_total = realised_symmetry_dim(total_current)
    d_sector = realised_symmetry_dim(sector_functional)
    print(f"  TOTAL-current  j_total = Im(z† ∇z): realised symmetry dim = {d_total:2d}  "
          f"→ {'CONNECTED su(4)' if d_total == 15 else 'NOT su(4)'}")
    print(f"  SECTOR-current Σ|Im(z_a* ∇z_a)|²  : realised symmetry dim = {d_sector:2d}  "
          f"→ {'PRODUCT u(1)^3' if d_sector == 3 else 'other'}")
    assert d_total == 15
    assert d_sector == 3

    print("\n── B−L is a Cartan element → realised in BOTH forms (consistent w/ #80) ──")
    bl = b_minus_L_generator()
    print(f"  B−L symmetry of total-current  : {_is_symmetry(total_current, bl)}")
    print(f"  B−L symmetry of sector-current : {_is_symmetry(sector_functional, bl)}")
    assert _is_symmetry(total_current, bl) and _is_symmetry(sector_functional, bl)

    print("\n" + "=" * 84)
    print("VERDICT (cheap route)")
    print("=" * 84)
    print("""
  The scalar SSV current j = Im(ψ*∇ψ) is the overall-U(1) Noether current; its UNIQUE
  multi-component generalisation is j_total = Im(z† ∇z), which is EXACTLY SU(4)-
  invariant. So the natural chiral-shear L_perp makes all 12 off-diagonal generators
  exact symmetries: lie_closure = 15 = su(4) → CONNECTED, with NO extra term.

  The per-colour (sector) current form — which the scalar theory has no analogue of —
  is invariant only under the Cartan: lie_closure = 3 = u(1)^3 → PRODUCT.

  So connectivity is NOT decided by the dynamics within a fixed realisation; it is the
  SAME foundational fork as #81/#83:
    • JUNCTION realisation (native scalar SSV, #79/#80): no fundamental C^4; colour-i
      → colour-j is a reconnection (topology change), not a continuous rotation → the
      off-diagonal generators are absent → PRODUCT (u(1)^3). Reproduces #79/#80.
    • MULTIPLET realisation (the #83-type internal-orientation upgrade): the natural
      total-current L_perp is SU(4)-invariant → CONNECTED (su(4)), automatically.

  HOPEFUL ASYMMETRY vs #81: once you pay for the internal multiplet, colour off-
  diagonal symmetry is GEOMETRICALLY FREE (the parity-EVEN total-current term already
  delivers it). Chirality (#81) still needs a parity-ODD term even after the upgrade.
  So of the two continuous structures the scalar lacks, colour connectivity comes free
  with the multiplet; handedness does not.
""")


if __name__ == "__main__":
    main()

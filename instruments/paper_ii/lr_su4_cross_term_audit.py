"""#81 cheap route: does the chirality-locking cross term vanish by a selection
rule (as the #76 L_perp Berry-phase bridge did), or is it forced nonzero?

Spec: papers/SSV-II/lr-su4-logse-spec.md. The whole chirality question reduces to
ONE term in the generalised chiral-shear energy of the LR-symmetric SU(4) LogSE:

    E_perp  ⊃  λ_cw ∫ ω_c · ω_w d^3r ,   ω_c = ∇×j_c ,  ω_w = ∇×j_w,

with j_c the SU(4) colour current and j_w = j_{w,L} − j_{w,R} the weak current.
Flipping P_c alone OR P_w alone sends ω → −ω, so the cross term flips sign;
flipping BOTH (the diagonal move, = chirality) leaves it invariant. Hence it
splits the diagonal sector (the chiral 16) from the anti-diagonal by 2λ_cw ∫ω_c·ω_w
per unit defect length. So the chirality verdict hinges on TWO facts decided here
*analytically*, before any 3D solver:

  (A) Is ∫ω_c·ω_w forced to VANISH by a selection rule?  If yes → the four sectors
      are degenerate at the L_perp level → NOT-FORCED (the #80 postulate stands),
      exactly the way #76's L_perp bridge vanished by m_a + m_b = 0.
  (B) If nonzero, how big is it relative to the diagonal self-terms?  (Sets whether
      the locking is a leading effect or a tiny correction the relaxer could wash
      out.)

THE KEY DISTINCTION FROM #76.  The #76 null was an OFF-DIAGONAL holonomy/Berry-phase
matrix element ⟨ψ_a|δL_perp|ψ_b⟩ between two *different* eigenmodes carrying e^{im_aφ}
and e^{im_bφ}; its azimuthal integral ∫e^{i(m_b−m_a)φ}(…)dφ plus the curl structure
forced m_a = m_b AND m_a + m_b = 0 ⇒ it vanished.  The chirality-locking term is a
DIAGONAL energy of one configuration: ω_c, ω_w are curls of the *real* currents
j = Im(ψ*∇ψ) = (winding)·|ψ|²/r φ̂ — the phase e^{imφ} has been differentiated out,
no residual azimuthal phase survives, the φ-integral is ∫dφ = 2π ≠ 0.  So no
selection rule can kill it; only the radial integral could, and it is positive.

This script computes that radial integral for co-located straight windings using the
Paper I LogSE vortex profile (the same f(r) and r_max=15ξ reliability bound as
lperp_core_integral.py), and shows it equals the diagonal L_perp self-energy density
I_curl exactly (when the colour and weak cores coincide) — i.e. the locking term is
the SAME order as the diagonal terms, not a small correction.

Geometry (leading order).  Co-located straight vortices along ẑ:
    z-colour component:  z = f_c(r) e^{i m_c φ}   ⇒  j_c = (m_c f_c²/r) φ̂
    weak spinor compt.:  χ = f_w(r) e^{i m_w φ}   ⇒  j_w = (m_w f_w²/r) φ̂
    ω_{·,z} = (1/r) ∂_r(r j_φ) = m (f²)'/r = 2 m f f'/r   (axial; others 0)
    ω_c · ω_w = m_c m_w (2 f_c f_c'/r)(2 f_w f_w'/r)
Cross energy per unit length:
    ε_cw = ∫ ω_c·ω_w · 2πr dr = 2π m_c m_w ∫ 4 f_c f_c' f_w f_w' / r dr ≡ m_c m_w · I_cross
With f_c = f_w = f and |m| = 1:  I_cross = 2π ∫ 4 f²f'²/r dr = I_curl (lperp_core).

Loops vs straight lines: the straight vortex is the leading-order probe of whether
the term is ALLOWED and nonzero; ring curvature shifts the magnitude (cf.
lperp_core_integral's J_bend/K_bend corrections) but cannot turn a nonzero axial
overlap into an exact zero. Spatial separation of the colour and weak cores DOES
kill it (∝ overlap) — so the locking requires colour and weak windings to share one
core, which is exactly the "one defect carries the whole generation" hypothesis.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT / "paper_i") not in sys.path:
    sys.path.insert(0, str(SRC_ROOT / "paper_i"))

from vortex_profile import VortexProfile  # noqa: E402

ALPHA = 1.0 / 137.035999084
R_MAX_RELIABLE = 15.0   # growing-mode contamination beyond this (lperp_core_integral)


def cross_integrand(r: np.ndarray, f: np.ndarray, fp: np.ndarray) -> np.ndarray:
    """ω_{c,z} ω_{w,z} · 2πr  with f_c = f_w = f, |m_c| = |m_w| = 1.

    ω_z = 2 f f' / r, so ω_z² · 2πr = (2ff'/r)² · 2πr = 4 f²f'²/r · 2π.
    Returns the per-unit-length cross-energy density integrand (in r).
    """
    r_s = np.maximum(r, 1.0e-12)
    omega_z = 2.0 * f * fp / r_s                      # = 2 f f' / r  (m = 1)
    return omega_z**2 * 2.0 * math.pi * r             # ω_z² · 2πr


def compute_cross_integral(
    r: np.ndarray, f: np.ndarray, fp: np.ndarray, r_max: float
) -> float:
    """I_cross = ∫ (2ff'/r)² · 2πr dr  up to r_max  (= I_curl when f_c=f_w)."""
    mask = r <= r_max
    return float(np.trapezoid(cross_integrand(r[mask], f[mask], fp[mask]), r[mask]))


def analytic_tail(r0: float) -> float:
    """Tail r>r0 with f ~ 1 − 1/(4r²): 2ff'/r ~ 1/r⁴ ⇒ integrand ~ 2π/r⁷,
    ∫_{r0}^∞ = 2π/(6 r0⁶). Negligible (same as lperp_core_integral's I_curl tail)."""
    return 2.0 * math.pi / (6.0 * r0**6)


def sector_cross_energy(m_c: int, m_w: int, i_cross: float) -> float:
    """Cross-energy per unit length for windings (m_c, m_w): ε_cw/λ_cw = m_c m_w I_cross."""
    return m_c * m_w * i_cross


def diagonal_vs_antidiagonal_split(i_cross: float) -> dict[str, float]:
    """The four (P_c, P_w) sectors map to sign(m_c m_w):
       diagonal  P_c=P_w  ↔ m_c m_w = +1  → +I_cross
       anti-diag P_c≠P_w  ↔ m_c m_w = −1  → −I_cross
    Splitting (anti − diag) in units of λ_cw = 2 I_cross  (so sign(λ_cw) picks
    which is the ground state: λ_cw<0 ⇒ diagonal/chiral lower)."""
    diag = sector_cross_energy(+1, +1, i_cross)       # also (−1,−1) by the ℤ₂×ℤ₂ symmetry
    anti = sector_cross_energy(+1, -1, i_cross)       # also (−1,+1)
    return {"diagonal (16)": diag, "anti-diagonal": anti, "split |anti−diag|": abs(anti - diag)}


def main() -> None:
    n_pts = 4000
    print("=" * 78)
    print("#81 cheap route — chirality-locking cross term ∫ω_c·ω_w: forced zero?")
    print("=" * 78)
    print(f"  LogSE vortex profile, n={n_pts}, reliable r < {R_MAX_RELIABLE} ξ")
    print()

    vp = VortexProfile.solve(n=n_pts, x_max=R_MAX_RELIABLE)
    r = np.array(vp.xs)
    f = np.array(vp.fs)
    fp = np.array(vp.fps)
    print(f"  core slope a (f ~ a r) = {vp.slope:.6f}   f(r_max) = {float(f[-1]):.6f} (→1)")
    print()

    i_cross = compute_cross_integral(r, f, fp, R_MAX_RELIABLE)
    tail = analytic_tail(R_MAX_RELIABLE)
    print("── (A) IS THE CROSS TERM FORCED TO VANISH? ─────────────────────────────")
    print(f"  I_cross = ∫ (2ff'/r)² · 2πr dr (r<{R_MAX_RELIABLE:.0f}ξ) = {i_cross:.6f}")
    print(f"  analytic tail r>{R_MAX_RELIABLE:.0f}ξ                       = {tail:.3e} (negligible)")
    print(f"  ⇒ NONZERO and positive. No azimuthal selection rule applies:")
    print(f"    ω is a curl of the REAL current j=|ψ|²(m/r)φ̂; the e^{{imφ}} phase is")
    print(f"    differentiated out, so ∫dφ = 2π ≠ 0 (contrast #76's off-diagonal")
    print(f"    Berry-phase bridge, killed by m_a+m_b=0). The term is ALLOWED.")
    print()

    print("── (B) HOW BIG? (vs the diagonal L_perp self-energy density) ───────────")
    print(f"  With co-located cores f_c=f_w=f and |m|=1, I_cross EQUALS the diagonal")
    print(f"  straight-vortex L_perp density I_curl of lperp_core_integral.py.")
    print(f"  ⇒ the locking term is the SAME order as the diagonal self-terms,")
    print(f"    not a small correction: |λ_cw ∫ω_c·ω_w| ~ (λ/2)∫|ω|² when λ_cw ~ λ⊥.")
    print()

    print("── SECTOR SPLITTING (per unit defect length, in units of λ_cw) ─────────")
    split = diagonal_vs_antidiagonal_split(i_cross)
    for k, v in split.items():
        print(f"    {k:22s}: {v:+.6f}")
    print(f"  diagonal (P_c=P_w, the chiral 16) vs anti-diagonal split by 2·I_cross")
    print(f"  = {2*i_cross:.4f} · λ_cw per unit length.")
    print(f"  sign(λ_cw) decides the ground state: λ_cw<0 ⇒ the chiral 16 is LOWER")
    print(f"  (a genuine prediction); λ_cw>0 ⇒ anti-diagonal (WRONG-SIGN falsification).")
    print()

    print("=" * 78)
    print("VERDICT (cheap route)")
    print("=" * 78)
    print("""
  The chirality-locking cross term is NOT forced to vanish — there is no selection
  rule analogous to the #76 null, because it is a DIAGONAL energy (one config), not
  an off-diagonal holonomy bridge. For one defect carrying both colour and weak
  windings on a shared core it is generically nonzero, positive, and the SAME order
  as the diagonal L_perp self-energy.

  So the four (P_c, P_w) sectors are NOT degenerate at the L_perp level once λ_cw≠0:
  diagonal vs anti-diagonal split by 2·I_cross·λ_cw per unit length. The chirality
  verdict therefore reduces to the SIGN of λ_cw (and survival of the gap under full
  3D relaxation), NOT to whether the term exists. NOT-FORCED-by-vanishing is ruled
  out at leading order.

  CAVEATS (honest, pre-registered): (1) straight-vortex leading order — ring
  curvature shifts the magnitude (cf. J_bend/K_bend) but cannot zero a nonzero axial
  overlap; (2) requires colour & weak cores to COINCIDE (separation kills it ∝
  overlap) — that is the 'one defect = one generation' hypothesis, now a sharp
  sub-claim; (3) the SIGN of λ_cw is the remaining open question and is what the
  minimal numerical gate (M2) must settle.
""")


if __name__ == "__main__":
    main()

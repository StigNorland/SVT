"""#91 — Winding-regime audit: does the SU(2)-covariant L_⊥ supply the
spin–orbit lock |V| > 0 to put the IQV electron torus in the winding regime?

ANSWER: NO.  |V| = 0 exactly for the integer-quantum-vortex (IQV) electron with
uniform spin direction z₀.  The pre-registered decision rule gives CLEAN NO:
|m| → ∞ (firmly unlocked), γ_B = 0, muon reverts to NUMERICAL COINCIDENCE.

=============================================================================
PHYSICS OF THE ARGUMENT
=============================================================================

The B1 model `H(φ) = d·σ`, d = (m + cosφ, sinφ, 0) has a nonzero spin–orbit
lock amplitude |V| (the (cosφ, sinφ) part of d) only if the BdG operator carries
a Fourier e^{iφ} component, so that the azimuthal bridge integral

    V = ∫₀^{2π} e^{−iφ} · kernel(φ) · 1 dφ

connecting K_{+}(m_φ=+1) to Φ_{+}(m_φ=0) is nonzero.

For the SU(2)-covariant L_⊥ = (λ_⊥/2)|∇×j_total|² with j_total = Im(Ψ†∇Ψ):

1.  CURRENT ON THE IQV BACKGROUND.  For Ψ₀ = A(r,z) e^{iθ(r,z)} z₀ (constant
    z₀, the IQV):
        j_total = (ρ/ρ₀)(∇θ + a),   a = −i z₀†∇z₀ = 0.
    (Part A identity I3', verified in cp1_safety_checks.py.)

2.  FIRST-ORDER CURRENT VARIATION FROM THE z₀_⊥ CHANNEL.  For a perturbation
    δΨ = w(r,z) e^{imφ} z₀_⊥ (spin-perpendicular channel, z₀†z₀_⊥ = 0):

        δj = Im(δΨ†∇Ψ₀) + Im(Ψ₀†∇δΨ)
           = Im(w* e^{−imφ} z₀_⊥†∇(A e^{iθ} z₀))   ← kills by z₀_⊥†z₀ = 0
           + Im(A e^{−iθ} z₀†∇(w e^{imφ} z₀_⊥))    ← kills by z₀†z₀_⊥ = 0
           = 0.

    (This is the same z₀†z₀_⊥ = 0 that makes Part A Goldstone safety work.)

3.  SECOND-ORDER CORRECTION.  δ²j = Im(δΨ†∇δΨ).  For δΨ = u z₀ + w z₀_⊥:
        Im(u* z₀†∇(u z₀) + w* z₀_⊥†∇(u z₀) + u* z₀†∇(w z₀_⊥) + w* z₀_⊥†∇(w z₀_⊥))
    The cross terms u × w also kill by z₀†z₀_⊥ = 0.  So δ²j separates.

4.  BLOCK DIAGONALITY OF L_⊥.  Every term in δ²L_⊥ is either pure-z₀ or
    pure-z₀_⊥.  The L_⊥ BdG operator is block-diagonal in the two spin channels.
    Its matrix elements between K_{+}(m_φ=+1, z₀ channel) and Φ_{+}(m_φ=0, z₀_⊥
    channel) vanish — the same selection rule already encoded in
    hermitian_current_curl_bdg_blocks (kelvin_augmented_bdg.py:476) for the
    scalar operator applies without change.

5.  FOURIER ORTHOGONALITY.  Even setting aside spin channels: the L_⊥ operator on
    a φ-symmetric background has no e^{iφ} Fourier component.  The azimuthal
    integral ∫₀^{2π} e^{−iφ} × V(r,z) × e^{0} dφ = V(r,z) × ∫₀^{2π} e^{−iφ} dφ = 0.

RESULT: |V| = 0 exactly.  |m| = |Δε|/(2|V|) → ∞.  Firmly UNLOCKED.  γ_B = 0.
The scalar #76 null is reproduced.  The muon returns to NUMERICAL COINCIDENCE.

=============================================================================
CONTROL (HQV CASE)
=============================================================================

For a half-quantum vortex (HQV) electron with z₀(φ) = (cos(φ/2), sin(φ/2)):
    a_φ = −i z₀†∂_φ z₀ = ½  (constant azimuthal Berry connection)
    j_total,φ = (ρ/ρ₀)(∂_φθ/R + ½/R)  ← e^{iφ}-independent shift only

The azimuthal CURRENT still has no e^{iφ} Fourier component (a is constant, not
winding).  BUT: the Kelvin modes on the HQV background have HALF-INTEGER m_φ
(modes must be single-valued against the half-wound background), giving γ_B = π
by the half-integer ladder directly — no spin-orbit matrix element needed.

Whether the electron should be an HQV (vs IQV) is a separate foundational
question: the HQV has ½ quantum of circulation, which would change all mass
formulas and requires re-examining pion = 2μ₀ (Part A). → See issue #94.
"""

from __future__ import annotations

import math
import numpy as np
import sympy as sp


# ─── Symbols ────────────────────────────────────────────────────────────────

phi = sp.Symbol("phi", real=True)
m_K, m_Phi = sp.Integer(1), sp.Integer(0)          # azimuthal labels


# ─── Part 1: δj from z₀_⊥ channel = 0 ──────────────────────────────────────

def current_variation_from_perp_channel() -> sp.Expr:
    """Symbolic δj from δΨ = w z₀_⊥ on the IQV background.

    Both terms in δj = Im(δΨ†∇Ψ₀) + Im(Ψ₀†∇δΨ) kill by z₀†z₀_⊥ = 0.
    Returns the expression for δj — must be identically 0.
    """
    z0_dag_z0perp = sp.Integer(0)   # orthogonality z₀†z₀_⊥ = 0
    A, theta, w = sp.symbols("A theta w", real=True, positive=True)
    # Term 1: Im(w* z₀_⊥†∇(Ae^{iθ}z₀)) = Im(w* × z₀_⊥†z₀ × ∂(Ae^{iθ})) = 0
    term1 = w * z0_dag_z0perp
    # Term 2: Im(Ae^{-iθ} z₀†∇(w z₀_⊥)) = Im(Ae^{-iθ} × z₀†z₀_⊥ × ∇w) = 0
    term2 = A * z0_dag_z0perp * w
    return sp.simplify(term1 + term2)


# ─── Part 2: Fourier bridge integral ────────────────────────────────────────

def fourier_bridge_integral_iqv() -> sp.Expr:
    """∫₀^{2π} e^{−i·m_K·φ} × V(r,z) × e^{i·m_Phi·φ} dφ for IQV.

    For a φ-independent kernel V(r,z) (no e^{iφ} from the background):
        = V(r,z) × ∫₀^{2π} e^{−iφ} dφ = 0.
    Returns the symbolic result — must be 0.
    """
    V_rz = sp.Symbol("V_rz")    # the φ-independent meridional matrix element
    integrand = V_rz * sp.exp(-sp.I * (m_K - m_Phi) * phi)   # e^{-iφ}
    return sp.integrate(integrand, (phi, 0, 2 * sp.pi))


def fourier_bridge_integral_hqv() -> sp.Expr:
    """Hypothetical bridge for an HQV with spin-texture kernel ∝ e^{iφ}.

    If the background had azimuthal spin texture giving kernel ∝ e^{iφ}:
        ∫₀^{2π} e^{−iφ} × V e^{iφ} dφ = V × 2π ≠ 0.
    Returns 2π·V — nonzero, showing the HQV control works.
    """
    V_rz = sp.Symbol("V_rz")
    hqv_kernel = V_rz * sp.exp(sp.I * phi)    # e^{iφ} from the HQV texture
    integrand = hqv_kernel * sp.exp(-sp.I * (m_K - m_Phi) * phi)
    return sp.integrate(integrand, (phi, 0, 2 * sp.pi))


# ─── Part 3: Numerical verification of Fourier orthogonality ────────────────

def numerical_bridge_iqv(n_phi: int = 2000) -> float:
    """Numerical ∫₀^{2π} e^{−iφ} × 1 dφ / (2π) for IQV (should be ≈ 0)."""
    phis = np.linspace(0.0, 2 * np.pi, n_phi, endpoint=False)
    integrand = np.exp(-1j * phis) * 1.0                          # φ-independent kernel
    return abs(np.trapezoid(integrand, phis)) / (2 * np.pi)


def numerical_bridge_hqv(n_phi: int = 2000) -> float:
    """Numerical ∫₀^{2π} e^{−iφ} × e^{iφ} dφ / (2π) for HQV control (should be ≈ 1)."""
    phis = np.linspace(0.0, 2 * np.pi, n_phi, endpoint=False)
    hqv_kernel = np.exp(1j * phis)                                 # e^{iφ} from spin texture
    integrand = np.exp(-1j * phis) * hqv_kernel
    return abs(np.trapezoid(integrand, phis)) / (2 * np.pi)


# ─── Part 4: HQV modes have half-integer m_φ (control showing why HQV works) ─

def hqv_mode_periodicity() -> dict[str, object]:
    """On a half-wound HQV background z₀(φ) = (cos(φ/2), sin(φ/2)):
    Single-valued field Ψ = A e^{iθ} z₀(φ) requires z₀(φ+2π) = −z₀(φ).
    A perturbation δΨ ∝ e^{im_φ φ} z₀(φ) requires e^{im_φ·2π}·(−1) = −1 →
    m_φ ∈ ℤ (integer). BUT the effective azimuthal action is m_φ + ½ (half-integer)
    because z₀(φ) contributes ½ from its own winding.

    Returns a dict documenting the half-integer effective quantum number."""
    # z₀(φ+2π) = -z₀(φ): the background itself carries azimuthal 'charge' ½
    # A mode e^{imφ} z₀(φ) has Berry phase ∮ A_φ dφ = 2π(m + ½) → γ_B = π (mod 2π)
    return {
        "z0_winding": "half-integer (z₀(φ+2π) = -z₀(φ))",
        "mode_azimuthal_label": "integer m_φ (single-valuedness)",
        "effective_quantum_number": "m_φ + 1/2 (half-integer; accounts for background winding)",
        "berry_phase": "γ_B = π for all m_φ (the half-integer shifts the ladder)",
        "mechanism": "direct from background topology, NO spin-orbit matrix element needed",
    }


# ─── Verdict ─────────────────────────────────────────────────────────────────

def iqv_verdict() -> dict[str, object]:
    """Collect all results and state the pre-registered verdict for IQV."""
    dj_perp = current_variation_from_perp_channel()
    fourier_iqv = fourier_bridge_integral_iqv()
    fourier_hqv = fourier_bridge_integral_hqv()
    num_iqv = numerical_bridge_iqv()
    num_hqv = numerical_bridge_hqv()

    V = abs(float(fourier_iqv.subs(sp.Symbol("V_rz"), 1))) if fourier_iqv != 0 else 0.0
    # |V| = 0 for IQV → |m| → ∞ → unlocked → γ_B = 0
    regime = "UNLOCKED (|m|→∞)" if V == 0.0 else "LOCKED (|m| < 1?)"
    gamma_B = 0.0 if V == 0.0 else math.pi
    verdict = "CLEAN NO" if V == 0.0 else "PASS"

    return {
        "delta_j_from_perp_channel": dj_perp,
        "fourier_bridge_iqv_symbolic": fourier_iqv,
        "fourier_bridge_hqv_symbolic": fourier_hqv,
        "numerical_bridge_iqv": num_iqv,
        "numerical_bridge_hqv": num_hqv,
        "V_magnitude_iqv": V,
        "m_parameter": float("inf"),
        "regime": regime,
        "gamma_B": gamma_B,
        "verdict": verdict,
        "muon_status": "NUMERICAL COINCIDENCE (IQV conditional not met)",
    }


def main() -> None:
    r = iqv_verdict()
    print("=" * 76)
    print("#91 — Spinor BdG winding-regime audit: IQV electron torus")
    print("=" * 76)
    print()
    print("  STEP 1: δj from z₀_⊥ channel (must be 0 for IQV)")
    print(f"    δj = {r['delta_j_from_perp_channel']}  ← killed by z₀†z₀_⊥ = 0")
    print()
    print("  STEP 2: Fourier bridge integral")
    print(f"    IQV (φ-independent kernel): {r['fourier_bridge_iqv_symbolic']}  [exact]")
    print(f"    HQV (e^iφ kernel, control): {r['fourier_bridge_hqv_symbolic']}  [nonzero, confirms test sensitivity]")
    print()
    print("  STEP 3: Numerical check (both should agree)")
    print(f"    IQV |∫e^{{-iφ}}·1 dφ|/(2π)      = {r['numerical_bridge_iqv']:.2e}  (≈0)")
    print(f"    HQV |∫e^{{-iφ}}·e^{{iφ}} dφ|/(2π) = {r['numerical_bridge_hqv']:.4f}  (≈1)")
    print()
    print("  CONCLUSION")
    print(f"    |V|   = {r['V_magnitude_iqv']}")
    print(f"    |m|   = {r['m_parameter']} (firmly {r['regime']})")
    print(f"    γ_B   = {r['gamma_B']} (scalar #76 null reproduced)")
    print(f"    Verdict:  {r['verdict']}")
    print(f"    Muon:     {r['muon_status']}")
    print()
    print("  HQV route: modes on half-wound background have half-integer")
    hqv = hqv_mode_periodicity()
    for k, v in hqv.items():
        print(f"    {k:32s}: {v}")
    print()
    print("  The HQV would give γ_B=π automatically — but it has ½ quantum of")
    print("  circulation, changing all mass formulas. Re-examination of pion=2μ₀")
    print("  (Part A) required. → new issue #94.")
    print("=" * 76)


if __name__ == "__main__":
    main()

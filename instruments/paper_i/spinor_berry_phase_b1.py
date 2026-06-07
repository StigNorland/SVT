"""#87 Part B / B1 — does the CP¹/spinor BdG operator produce γ_B = π (the muon
rung 3/2·μ₀), lifting the #76 scalar no-go?

BACKGROUND (the scalar no-go, papers/SSV-I/results/muon/volovik-berry-phase-
issue76-tasks1-4.md).  On the electron torus the half-integer muon rung needs an
azimuthal Berry holonomy exp(iγ_B) = −1 (γ_B = π) so that

    E_n = (n + γ_B/2π) ω₀  →  E_n = (n + ½) ω₀ ,   muon = the 3/2 rung.

The scalar LogSE BdG operator gives γ_B = 0 (integer ladder) for two reasons:
  (i)  the eigenbundle carries only INTEGER azimuthal Fourier labels e^{imφ},
       m ∈ ℤ, so the holonomy is exp(i2πm) = +1;
  (ii) the bridge ⟨K_{σ,±}|(∇×δj)†(∇×δj)|Φ_R⟩ between the Kelvin helicity modes
       (m_φ = ±1) and the breathing mode (m_φ = 0) VANISHES by the scalar
       selection rule Δm_φ = 0 (L^⊥) / m_a+m_b = 0 (M^⊥).
The note's stated cures: "eigenvectors rotating by half an angle around the
ring, or an underlying spinorial order parameter."

WHAT THE SPINOR CHANGES (analytic, the note states it; the code below proves the
holonomy half of it).
  • Selection rule.  With Ψ_a = √(ρ/ρ₀)e^{iθ}z_a the SU(2)-covariant chiral-shear
    term (the #84 total-current L_⊥) is a SPIN–ORBIT coupling: it conserves the
    TOTAL azimuthal angular momentum J_φ = m_φ + s_φ, not m_φ separately.  The
    scalar-forbidden bridge is reopened — K_{σ,±}(m_φ=±1, s_φ=∓½) connects to
    Φ_R(m_φ=0, s_φ=±½) because BOTH have J_φ = ±½ (Δm_φ=±1 is compensated by
    Δs_φ=∓1).  The #76 selection-rule no-go is lifted.
  • Holonomy.  A single spin-½ excitation on the ring has HALF-INTEGER total
    angular momentum J_φ ∈ ℤ + ½ (π₁(SO(3)) = ℤ₂: a 2π frame rotation = −1).
    When the spin–orbit lock co-rotates the internal frame once with the Kelvin
    helicity around the major circle, the Nambu eigenbundle winds and acquires
    γ_B = π.

THE PROTECTION (what makes 3/2 sharp, not a tunable 1.47).  In a BdG/Nambu
problem the azimuthal Berry phase is NOT the continuous solid-angle phase: the
particle-hole / chiral symmetry of the BdG operator pins it to a ℤ₂ invariant,
γ_B ∈ {0, π}.  It can change only by closing the BdG gap (a topological
transition), never continuously.  This module demonstrates exactly that with the
minimal chiral-symmetric two-band model of the azimuthal eigenbundle:

    H(φ) = d(φ)·σ ,   d(φ) = (m + cos φ, sin φ, 0).

σ_z is the chiral (BdG-like) symmetry: σ_z H σ_z = −H (because d_z ≡ 0).  It
quantises the Zak/Berry phase around φ:0→2π to {0, π}.  The map to SSV:
  • the winding part (cos φ, sin φ) = the spin–orbit lock co-rotating the spin
    with the Kelvin helicity frame once around the ring;
  • the constant m = the un-locked anisotropy (no spin–orbit; the scalar piece).
Then:
  • |m| < 1  (lock dominates): d winds once  ⇒  γ_B = π  ⇒  half-integer ladder,
    muon = (3/2)μ₀.
  • |m| > 1  (anisotropy dominates / scalar limit): no winding ⇒ γ_B = 0 ⇒
    integer ladder — reproduces the #76 scalar null.
  • the gap |d| closes only at |m| = 1: the jump 0↔π is a genuine topological
    transition, so γ_B = π is PROTECTED, not fine-tuned.

This is the holonomy half of B1, made falsifiable.  The selection-rule half is
analytic (above) and recorded in the result note.
"""

from __future__ import annotations

import numpy as np

# Pauli matrices
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def d_vector(phi: float, m: float) -> np.ndarray:
    """d(φ) = (m + cos φ, sin φ, 0).  d_z ≡ 0 ⇒ chiral symmetry σ_z."""
    return np.array([m + np.cos(phi), np.sin(phi), 0.0])


def hamiltonian(phi: float, m: float) -> np.ndarray:
    """H(φ) = d(φ)·σ (the azimuthal two-band / Nambu eigenbundle Hamiltonian)."""
    dx, dy, dz = d_vector(phi, m)
    return dx * SX + dy * SY + dz * SZ


def chiral_symmetry_residual(m: float, n: int = 200) -> float:
    """max‖σ_z H σ_z + H‖ over the ring — must be 0 (the ℤ₂-protecting symmetry)."""
    worst = 0.0
    for phi in np.linspace(0.0, 2 * np.pi, n, endpoint=False):
        H = hamiltonian(phi, m)
        worst = max(worst, np.max(np.abs(SZ @ H @ SZ + H)))
    return float(worst)


def gap_min(m: float, n: int = 2000) -> float:
    """Minimum spectral gap 2|d(φ)| around the ring (closes only at |m|=1)."""
    phis = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    return float(min(2.0 * np.linalg.norm(d_vector(p, m)) for p in phis))


def lower_band_vectors(m: float, n: int) -> np.ndarray:
    """Lower-band eigenvectors |u_-(φ_k)| on a φ grid (shape (n, 2))."""
    phis = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    vecs = np.empty((n, 2), dtype=complex)
    for k, phi in enumerate(phis):
        w, v = np.linalg.eigh(hamiltonian(phi, m))
        vecs[k] = v[:, 0]               # eigenvalue −|d| (lower band)
    return vecs


def berry_phase(m: float, n: int = 4000) -> float:
    """Gauge-invariant Zak/Berry phase γ_B = −Im ln ∏_k ⟨u(φ_k)|u(φ_{k+1})⟩
    (Wilson loop — independent of the per-point gauge).  Because the chiral
    symmetry σ_z pins γ_B to the ℤ₂ set {0, π}, the result is returned as its
    magnitude in [0, π]: ≈0 (trivial) or ≈π (nontrivial)."""
    vecs = lower_band_vectors(m, n)
    prod = 1.0 + 0j
    for k in range(n):
        prod *= np.vdot(vecs[k], vecs[(k + 1) % n])
    return float(abs(np.angle(prod)))    # |angle| ∈ [0, π]; ℤ₂-valued: 0 or π


def winding_number(m: float, n: int = 4000) -> int:
    """Winding of (d_x, d_y) around the origin as φ:0→2π."""
    phis = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    ang = np.array([np.arctan2(*d_vector(p, m)[1::-1]) for p in phis])  # atan2(d_y,d_x)
    dang = np.diff(np.unwrap(np.concatenate([ang, ang[:1]])))
    return int(round(np.sum(dang) / (2 * np.pi)))


def rung_offset(m: float) -> float:
    """The ladder offset γ_B/2π in E_n = (n + γ_B/2π) ω₀  (→ ½ when γ_B = π)."""
    return berry_phase(m) / (2 * np.pi)


def scalar_limit_berry_phase() -> float:
    """The #76 scalar BdG result: no internal spin ⇒ no winding part ⇒ γ_B = 0.
    Modeled as the m → ∞ (anisotropy-dominated, un-locked) limit."""
    return berry_phase(50.0)


def main() -> None:
    print("=" * 76)
    print("#87 B1 — spinor BdG azimuthal holonomy: is γ_B = π (muon = 3/2 μ₀)?")
    print("=" * 76)
    print("  H(φ) = d·σ,  d = (m + cosφ, sinφ, 0);  σ_z chiral symmetry ⇒ γ_B ∈ {0,π}")
    print()

    print("  chiral-symmetry residual ‖σ_zHσ_z + H‖ (locked m=0.3): "
          f"{chiral_symmetry_residual(0.3):.1e}")
    print()
    print(f"  {'m (un-lock)':>12} {'gap_min':>9} {'winding':>8} {'γ_B/π':>8} "
          f"{'offset γ_B/2π':>14}  regime")
    for m in (0.0, 0.3, 0.6, 0.9, 1.1, 1.5, 3.0, 50.0):
        g = berry_phase(m)
        regime = "LOCKED → muon 3/2" if winding_number(m) == 1 else "scalar/#76 null"
        print(f"  {m:12.2f} {gap_min(m):9.3f} {winding_number(m):8d} "
              f"{g/np.pi:8.3f} {g/(2*np.pi):14.3f}  {regime}")
    print()

    g_lock = berry_phase(0.3)
    g_scalar = scalar_limit_berry_phase()
    print("── VERDICT ────────────────────────────────────────────────────────────")
    print(f"  spin-orbit-locked (m<1):  γ_B = {g_lock/np.pi:.3f}·π  → E_n=(n+½)ω₀ → "
          "muon = (3/2)μ₀")
    print(f"  scalar / unlocked limit:  γ_B = {g_scalar/np.pi:.3f}·π  → E_n=n·ω₀  "
          "(reproduces #76 null)")
    print("  γ_B is ℤ₂-quantised by the BdG chiral symmetry; the 0→π jump is a")
    print("  topological transition at the gap closing |m|=1, so 3/2 is PROTECTED.")
    print("=" * 76)


if __name__ == "__main__":
    main()

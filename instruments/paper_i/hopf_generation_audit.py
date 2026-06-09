"""#115 Gate 1 + Gate 3 (first pass) — are CP¹ Hopf-charge sectors viable as
lepton generations?

Issue #115 pre-registers the hypothesis that charged-lepton generations
(e, μ, τ) are CP¹ defects distinguished by the **Hopf charge** Q = 1, 2, 3 of
the spin texture n̂ = z†σz : R³ → S² (the π₃(S²) = ℤ sector of the order
parameter adopted in #83/#87, unused by the #87 muon work).  This module runs
the two cheapest gates on fixed analytic hopfion ansätze — no field relaxation,
no 3D solver (those are gated behind a PASS here).

Construction (Hietarinta–Salo A_{n,m} form).  Map R³ → S³ stereographically,
    Z₁ = ((r²−1) + 2 i z)/(r²+1) ,   Z₂ = 2(x + i y)/(r²+1) ,   |Z|² = 1 ,
then define the target stereographic coordinate W = Z₁ⁿ / Z₂ᵐ and pull S² back
through inverse stereographic projection,
    n̂ = (2 Re W, 2 Im W, 1 − |W|²) / (1 + |W|²) .
This map has Hopf charge **Q = n·m** and → south pole (0,0,−1) at infinity, so
the texture is localised.  We use (n,m) = (1,1), (2,1), (3,1) ⇒ Q = 1, 2, 3.

GATE 1 — quantum-number preservation.
  (G1a) Hopf invariant via the Whitehead integral
            H = (1/(4π)²) ∫ a·b d³x ,   b_i = ½ ε_{ijk} n̂·(∂_j n̂ × ∂_k n̂),
            ∇×a = b  (solved spectrally in Coulomb gauge).
        The *ratios* H(Q)/H(1) ≈ 2, 3 are the claim-bearing, normalisation-free
        check that we have three DISTINCT Hopf sectors.
  (G1b) electric-charge orthogonality.  Electric charge is the winding of the
        overall U(1) phase θ in Ψ_a = A e^{iθ} z_a (a π₁(U(1)) invariant); the
        Hopf charge lives entirely in n̂ = z†σz, which is INVARIANT under
        z ↦ e^{iθ} z.  We verify max|n̂(e^{iθ}z) − n̂(z)| = 0 to machine
        precision, i.e. stacking Hopf charge cannot disturb electric charge.
  (Spin-statistics — the Finkelstein–Rubinstein part of G1 — is the decisive
   follow-up step and is NOT computed here; see the result note.)

GATE 3 — energetic hierarchy (baseline).  The observed mass steps ×207 then ×17
require E(Q) to climb like ~Q⁷.  We evaluate the canonical hopfion-stabilising
(Faddeev–Niemi) energy on the SAME ansätze,
    E = E₂ + E₄ ,  E₂ = ∫ Σ_i |∂_i n̂|²,  E₄ = ∫ Σ_{i<j} (n̂·(∂_i n̂×∂_j n̂))² ,
and report E(2)/E(1).  The rigorous Vakulenko–Kapitanskii bound E ≳ Q^{3/4}
(and Battye–Sutcliffe minimal energies ≈ 1 : 1.5 : 1.9) say the *minimum* grows
SUBLINEARLY — ~120× too flat for even the first step.  This pass establishes
the baseline numerically; the open escape hatch (does the SSV chiral-shear
functional |∇×j|² scale far steeper?) is the next gate, not this one.

All derivatives are spectral on a periodic box; the texture ≈ south pole at the
boundary so periodicity error is small and falls on the integer ratios.
"""

from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------------
# Grid + spectral helpers
# --------------------------------------------------------------------------

def make_grid(n: int, half_width: float):
    """Periodic cubic grid on [-L, L)³ with N points/side; returns coords, dx, k."""
    L = float(half_width)
    dx = 2 * L / n
    ax = -L + dx * np.arange(n)
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    k1 = 2 * np.pi * np.fft.fftfreq(n, d=dx)
    KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
    return X, Y, Z, dx, (KX, KY, KZ)


def d_spectral(field, k_i):
    """∂_i field via FFT (field real, periodic)."""
    return np.real(np.fft.ifftn(1j * k_i * np.fft.fftn(field)))


# --------------------------------------------------------------------------
# Hopfion construction (Hietarinta–Salo A_{n,m}; Hopf charge Q = n·m)
# --------------------------------------------------------------------------

def hopfion_nhat(X, Y, Z, n: int, m: int):
    """Return the unit texture n̂ (3 arrays) for the A_{n,m} hopfion, Q = n·m."""
    r2 = X * X + Y * Y + Z * Z
    denom = r2 + 1.0
    Z1 = ((r2 - 1.0) + 2j * Z) / denom
    Z2 = (2.0 * (X + 1j * Y)) / denom
    # Target stereographic coordinate W = Z1^n / Z2^m.  Guard the Z2=0 axis
    # (W → ∞ ⇒ south pole) with a tiny regulator; the result is clipped anyway.
    Z2 = np.where(np.abs(Z2) < 1e-12, 1e-12 + 0j, Z2)
    W = (Z1 ** n) / (Z2 ** m)
    w2 = np.abs(W) ** 2
    common = 1.0 / (1.0 + w2)
    nx = 2.0 * np.real(W) * common
    ny = 2.0 * np.imag(W) * common
    nz = (1.0 - w2) * common
    return nx, ny, nz


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def pullback_b(nhat, K):
    """b_i = ½ ε_{ijk} n̂·(∂_j n̂ × ∂_k n̂)  (the closed 'magnetic field' 2-form)."""
    KX, KY, KZ = K
    dn = [
        [d_spectral(nc, KX) for nc in nhat],   # ∂_x of each component
        [d_spectral(nc, KY) for nc in nhat],   # ∂_y
        [d_spectral(nc, KZ) for nc in nhat],   # ∂_z
    ]
    # F_jk = n̂·(∂_j n̂ × ∂_k n̂); b_i = ε_{ijk} F_jk summed over j<k (the ½·2).
    def F(j, k):
        dj = (dn[j][0], dn[j][1], dn[j][2])
        dk = (dn[k][0], dn[k][1], dn[k][2])
        return _dot(nhat, _cross(dj, dk))
    bx = F(1, 2)   # ε_{1jk}: (j,k)=(2,3)→(y,z)
    by = F(2, 0)   # ε_{2jk}: (j,k)=(3,1)→(z,x)
    bz = F(0, 1)   # ε_{3jk}: (j,k)=(1,2)→(x,y)
    return (bx, by, bz), dn


def hopf_invariant(bvec, K):
    """H = (1/(4π)²) ∫ a·b,  â = (i k × b̂)/k²  (Coulomb gauge, k=0 dropped)."""
    KX, KY, KZ = K
    k2 = KX * KX + KY * KY + KZ * KZ
    k2[0, 0, 0] = 1.0  # avoid /0; the k=0 mode of a is set to 0 below
    bhat = [np.fft.fftn(b) for b in bvec]
    # (i k × b̂)
    cx = 1j * (KY * bhat[2] - KZ * bhat[1])
    cy = 1j * (KZ * bhat[0] - KX * bhat[2])
    cz = 1j * (KX * bhat[1] - KY * bhat[0])
    ahat = [cx / k2, cy / k2, cz / k2]
    for a in ahat:
        a[0, 0, 0] = 0.0
    avec = [np.real(np.fft.ifftn(a)) for a in ahat]
    integrand = _dot(avec, bvec)
    return integrand


def berry_connection(zeta1, zeta2, K):
    """a_i = −i z†∂_i z for the normalised CP¹ spinor z = (ζ₁,ζ₂)/|ζ| (real)."""
    KX, KY, KZ = K
    norm = np.sqrt(np.abs(zeta1) ** 2 + np.abs(zeta2) ** 2)
    z1, z2 = zeta1 / norm, zeta2 / norm

    def dz(z, k_i):
        return np.fft.ifftn(1j * k_i * np.fft.fftn(z))

    a = []
    for k_i in (KX, KY, KZ):
        s = np.conj(z1) * dz(z1, k_i) + np.conj(z2) * dz(z2, k_i)
        a.append(np.real(-1j * s))   # z†∂z is pure imaginary ⇒ a real
    return a


def chiral_shear_density(a_vec, K):
    """|∇×a|²: the SSV chiral-shear density |∇×j|² for a pure texture (j ∝ a)."""
    KX, KY, KZ = K
    ax, ay, az = a_vec
    bx = d_spectral(az, KY) - d_spectral(ay, KZ)
    by = d_spectral(ax, KZ) - d_spectral(az, KX)
    bz = d_spectral(ay, KX) - d_spectral(ax, KY)
    return bx * bx + by * by + bz * bz


def faddeev_niemi_energy(nhat, dn):
    """E₂ = ∫ Σ_i|∂_i n̂|², E₄ = ∫ Σ_{i<j} F_ij²  (densities; caller scales by dx³)."""
    e2 = sum(_dot(dn[i], dn[i]) for i in range(3))

    def F(j, k):
        return _dot(nhat, _cross(dn[j], dn[k]))
    e4 = F(0, 1) ** 2 + F(0, 2) ** 2 + F(1, 2) ** 2
    return e2, e4


# --------------------------------------------------------------------------
# Gate runners
# --------------------------------------------------------------------------

def run_hopf_charge(n: int, m: int, grid_n: int = 96, half_width: float = 8.0):
    """G1a + G3 on one (n,m): Hopf invariant, FN energies."""
    X, Y, Z, dx, K = make_grid(grid_n, half_width)
    nhat = hopfion_nhat(X, Y, Z, n, m)
    bvec, dn = pullback_b(nhat, K)
    H = float(np.sum(hopf_invariant(bvec, K)) * dx ** 3 / (4 * np.pi) ** 2)
    e2, e4 = faddeev_niemi_energy(nhat, dn)
    # Chiral-shear energy of the bare texture, ∫|∇×a|² (j ∝ a, θ=0, ρ=ρ₀).
    r2 = X * X + Y * Y + Z * Z
    denom = r2 + 1.0
    Z1 = ((r2 - 1.0) + 2j * Z) / denom
    Z2 = (2.0 * (X + 1j * Y)) / denom
    Z2 = np.where(np.abs(Z2) < 1e-12, 1e-12 + 0j, Z2)
    a_vec = berry_connection(Z1 ** n, Z2 ** m, K)
    e_chi = float(np.sum(chiral_shear_density(a_vec, K)) * dx ** 3)
    return {
        "n": n, "m": m, "Q_target": n * m,
        "H": H,
        "E2": float(np.sum(e2) * dx ** 3),
        "E4": float(np.sum(e4) * dx ** 3),
        "E_chi": e_chi,
    }


def nhat_from_spinor(zeta1, zeta2):
    """n̂ = ζ†σζ for a normalised 2-spinor ζ = (ζ₁, ζ₂) (|ζ|² = 1)."""
    norm = np.sqrt(np.abs(zeta1) ** 2 + np.abs(zeta2) ** 2)
    z1, z2 = zeta1 / norm, zeta2 / norm
    nx = 2.0 * np.real(np.conj(z1) * z2)
    ny = 2.0 * np.imag(np.conj(z1) * z2)
    nz = np.abs(z1) ** 2 - np.abs(z2) ** 2
    return nx, ny, nz


def electric_charge_orthogonality(grid_n: int = 48, half_width: float = 6.0):
    """G1b: electric charge = winding of the overall U(1) phase θ in
    Ψ = A e^{iθ} z; the Hopf charge lives in n̂ = z†σz, which is INVARIANT under
    z ↦ e^{iθ}z.  Build the spinor explicitly, multiply by a genuine
    vortex-line phase e^{iθ(x)} (electric charge ≠ 0), rebuild n̂, and return
    max|Δn̂| — a real check, not an identity asserted in code."""
    X, Y, Z, dx, K = make_grid(grid_n, half_width)
    r2 = X * X + Y * Y + Z * Z
    denom = r2 + 1.0
    Z1 = ((r2 - 1.0) + 2j * Z) / denom
    Z2 = (2.0 * (X + 1j * Y)) / denom
    n, m = 2, 1
    zeta1, zeta2 = Z1 ** n, Z2 ** m
    base = nhat_from_spinor(zeta1, zeta2)
    theta = np.arctan2(Y, X)          # a straight vortex phase: electric charge 1
    phase = np.exp(1j * theta)
    spun = nhat_from_spinor(phase * zeta1, phase * zeta2)
    dmax = float(np.max(np.abs(np.stack([spun[i] - base[i] for i in range(3)]))))
    return dmax


def summary(grid_n: int = 96, half_width: float = 8.0):
    """Run Q=1,2,3; return rows + derived ratios and the G3 verdict numbers."""
    rows = [run_hopf_charge(n, m, grid_n, half_width)
            for (n, m) in [(1, 1), (2, 1), (3, 1)]]
    H1 = rows[0]["H"]
    Etot = [r["E2"] + r["E4"] for r in rows]
    Echi = [r["E_chi"] for r in rows]
    out = {
        "rows": rows,
        "H_ratios": [r["H"] / H1 for r in rows],          # expect ≈ 1, 2, 3
        "Etot": Etot,
        "E_ratio_2_1": Etot[1] / Etot[0],                 # observed needs 207
        "E_ratio_3_2": Etot[2] / Etot[1],                 # observed needs 17
        # Chiral-shear (= SSV |∇×j|² on a bare texture).
        "Echi": Echi,
        "Echi_ratio_2_1": Echi[1] / Echi[0],              # observed needs 207
        "Echi_ratio_3_2": Echi[2] / Echi[1],              # observed needs 17
        # If chiral-shear and Skyrme are the same structure, this ratio is
        # Q-independent (a constant), confirming j ∝ a ⇒ |∇×j|² ∝ |b|².
        "chi_over_E4": [r["E_chi"] / r["E4"] for r in rows],
        "required_mu_over_e": 206.768,
        "required_tau_over_mu": 16.817,
        "charge_orthogonality_dmax": electric_charge_orthogonality(),
    }
    return out


if __name__ == "__main__":
    s = summary()
    print("Hopf-charge generation audit (#115 Gate 1 + Gate 3)\n")
    print(f"{'(n,m)':>8} {'Q':>3} {'H':>8} {'H/H1':>7} {'E2':>10} {'E4':>10} {'Etot':>10}")
    for r, hr, et in zip(s["rows"], s["H_ratios"], s["Etot"]):
        print(f"{(r['n'], r['m'])!s:>8} {r['Q_target']:>3} {r['H']:>8.3f} "
              f"{hr:>7.3f} {r['E2']:>10.2f} {r['E4']:>10.2f} {et:>10.2f}")
    print()
    print(f"G1b electric-charge orthogonality  max|Δn̂| = "
          f"{s['charge_orthogonality_dmax']:.2e}  (expect 0)")
    print()
    print("G3 energy scaling (Faddeev–Niemi baseline):")
    print(f"  E(Q2)/E(Q1) = {s['E_ratio_2_1']:.3f}   "
          f"vs required m_μ/m_e = {s['required_mu_over_e']:.1f}")
    print(f"  E(Q3)/E(Q2) = {s['E_ratio_3_2']:.3f}   "
          f"vs required m_τ/m_μ = {s['required_tau_over_mu']:.1f}")
    print()
    print("G3 chiral-shear ∫|∇×a|²  (SSV |∇×j|² on a bare texture):")
    print(f"  Echi(Q2)/Echi(Q1) = {s['Echi_ratio_2_1']:.3f}   "
          f"vs required {s['required_mu_over_e']:.1f}")
    print(f"  Echi(Q3)/Echi(Q2) = {s['Echi_ratio_3_2']:.3f}   "
          f"vs required {s['required_tau_over_mu']:.1f}")
    cr = s["chi_over_E4"]
    print(f"  ∫|∇×a|² / E4 = {cr[0]:.4f}, {cr[1]:.4f}, {cr[2]:.4f}  "
          f"(Q-independent ⇒ chiral-shear ≡ Skyrme structure)")

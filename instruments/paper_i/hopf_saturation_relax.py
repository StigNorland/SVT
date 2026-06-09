"""#115 Gate G3′ — the saturation / log-potential sector.

The texture-energy gates (E₂ gradient, E₄ Skyrme, chiral-shear ∫|∇×a|²) all
failed: none scales steeper than ~Q^{1.6} against the ~Q⁷ the lepton masses
demand (see hopf_generation_audit.py + result note).  The one surviving route —
and the original physical picture ("load energy into a confined core; the
saturated vacuum resists") — is the LogSE saturation term.

G3′ asks: when the amplitude A = |Ψ| is allowed to relax (not pinned at ρ₀) for
a FIXED Hopf texture z of charge Q, does the resulting LogSE energy scale steeply
enough to span the ×207 / ×17 mass steps?

Setup.  Write the CP¹ field Ψ_a = A(x)·z_a(x), z†z = 1 (θ = 0, pure texture).
With log_pressure = 0.5 (canonical, matching energy_total_numba) the LogSE energy
is, using |∇Ψ|² = (∇A)² + A²|∂z|² (the #87 I2 decomposition, Berry/phase terms
absent at θ = 0),

    E[A; z] = ∫ { ½[(∇A)² + A²·G(x)] + ½(A² ln A² − A² + 1) } d³x ,
    G(x) ≡ Σ_i |∂_i z|²   (the fixed texture-gradient "centrifugal" potential).

The texture forces A down where G is large (core depletion); the depletion costs
log-potential energy.  We relax A by semi-implicit imaginary-time flow
(Euler–Lagrange −∇²A + G·A + A ln A² = 0; vacuum A = 1 is the attractor where
G → 0) and read off E(Q) for Q = 1, 2, 3.

Decision rule (pre-registered in the result note): step ≳ ×50 and grid-stable →
the saturation route is viable; step stays O(1) → the hierarchy is unreachable
and #115 closes negative.

The electric-charge vortex (a θ winding for charge −1) would add a Q-INDEPENDENT
depletion offset (same charge every generation); it is omitted here because it
cannot affect the Q-scaling, which is the whole question.
"""

from __future__ import annotations

import numpy as np

from hopf_generation_audit import make_grid, berry_connection

LOG_PRESSURE = 0.5
FLOOR = 1e-12


def texture_gradient_potential(X, Y, Z, n, m, K):
    """G(x) = Σ_i |∂_i z|² for the normalised A_{n,m} spinor z = (Z₁ⁿ, Z₂ᵐ)/|·|."""
    r2 = X * X + Y * Y + Z * Z
    denom = r2 + 1.0
    Z1 = ((r2 - 1.0) + 2j * Z) / denom
    Z2 = (2.0 * (X + 1j * Y)) / denom
    Z2 = np.where(np.abs(Z2) < 1e-12, 1e-12 + 0j, Z2)
    zeta1, zeta2 = Z1 ** n, Z2 ** m
    norm = np.sqrt(np.abs(zeta1) ** 2 + np.abs(zeta2) ** 2)
    z1, z2 = zeta1 / norm, zeta2 / norm
    KX, KY, KZ = K

    def d(z, k_i):
        return np.fft.ifftn(1j * k_i * np.fft.fftn(z))

    G = np.zeros(X.shape)
    for k_i in (KX, KY, KZ):
        d1, d2 = d(z1, k_i), d(z2, k_i)
        G += np.abs(d1) ** 2 + np.abs(d2) ** 2
    return np.real(G)


def relax_amplitude(G, K, dt=0.1, max_steps=4000, tol=1e-8):
    """Semi-implicit imaginary-time relaxation of A for fixed texture potential G.

    Flow: A ← (A − dt·N)/(1 + dt·k²) in Fourier, N = G·A + A·ln(A²)  (real space).
    Returns the relaxed amplitude A (≈ 1 in the bulk, depleted where G is large).
    """
    KX, KY, KZ = K
    k2 = KX * KX + KY * KY + KZ * KZ
    A = np.ones(G.shape)
    denom = 1.0 + dt * k2
    prev = None
    for step in range(max_steps):
        rho = np.maximum(A * A, FLOOR)
        N = G * A + A * np.log(rho)
        A_hat = (np.fft.fftn(A) - dt * np.fft.fftn(N)) / denom
        A = np.real(np.fft.ifftn(A_hat))
        if step % 50 == 0:
            cur = float(np.sum(A))
            if prev is not None and abs(cur - prev) < tol * abs(prev):
                break
            prev = cur
    return A


def energy_components(A, G, K, dx):
    """Return (E_grad, E_tex, E_pot, E_total) for the relaxed amplitude."""
    KX, KY, KZ = K

    def d(f, k_i):
        return np.real(np.fft.ifftn(1j * k_i * np.fft.fftn(f)))

    gradA2 = d(A, KX) ** 2 + d(A, KY) ** 2 + d(A, KZ) ** 2
    rho = np.maximum(A * A, FLOOR)
    e_grad = 0.5 * float(np.sum(gradA2)) * dx ** 3
    e_tex = 0.5 * float(np.sum(A * A * G)) * dx ** 3
    e_pot = LOG_PRESSURE * float(np.sum(rho * np.log(rho) - rho + 1.0)) * dx ** 3
    return e_grad, e_tex, e_pot, e_grad + e_tex + e_pot


def coupled_chiral_shear(A, n, m, X, Y, Z, K, dx):
    """∫|∇×j|² with the FULL current j = ρ·a (ρ = A², a = Berry connection),
    i.e. the chiral-shear term evaluated *with* the relaxed amplitude — the
    combined (not separate) test.  Returns (E_coupled, E_bare) where E_bare uses
    ρ = 1 (the separate chiral-shear of hopf_generation_audit)."""
    KX, KY, KZ = K
    r2 = X * X + Y * Y + Z * Z
    denom = r2 + 1.0
    Z1 = ((r2 - 1.0) + 2j * Z) / denom
    Z2 = (2.0 * (X + 1j * Y)) / denom
    Z2 = np.where(np.abs(Z2) < 1e-12, 1e-12 + 0j, Z2)
    a = berry_connection(Z1 ** n, Z2 ** m, K)

    def d(f, k_i):
        return np.real(np.fft.ifftn(1j * k_i * np.fft.fftn(f)))

    def curl_sq(vec):
        vx, vy, vz = vec
        bx = d(vz, KY) - d(vy, KZ)
        by = d(vx, KZ) - d(vz, KX)
        bz = d(vy, KX) - d(vx, KY)
        return float(np.sum(bx * bx + by * by + bz * bz)) * dx ** 3

    rho = A * A
    e_coupled = curl_sq([rho * a[i] for i in range(3)])
    e_bare = curl_sq(a)
    return e_coupled, e_bare


def run_saturation(n, m, grid_n=96, half_width=8.0):
    X, Y, Z, dx, K = make_grid(grid_n, half_width)
    G = texture_gradient_potential(X, Y, Z, n, m, K)
    A = relax_amplitude(G, K)
    e_grad, e_tex, e_pot, e_tot = energy_components(A, G, K, dx)
    e_chi_coupled, e_chi_bare = coupled_chiral_shear(A, n, m, X, Y, Z, K, dx)
    return {
        "n": n, "m": m, "Q": n * m,
        "A_min": float(A.min()), "A_max": float(A.max()),
        "E_grad": e_grad, "E_tex": e_tex, "E_pot": e_pot, "E_total": e_tot,
        "E_chi_coupled": e_chi_coupled, "E_chi_bare": e_chi_bare,
    }


def summary(grid_n=96, half_width=8.0):
    rows = [run_saturation(n, m, grid_n, half_width)
            for (n, m) in [(1, 1), (2, 1), (3, 1)]]
    Et = [r["E_total"] for r in rows]
    Ep = [r["E_pot"] for r in rows]
    Ecc = [r["E_chi_coupled"] for r in rows]
    return {
        "rows": rows,
        "E_total": Et,
        "E_pot": Ep,
        "Etot_ratio_2_1": Et[1] / Et[0],
        "Etot_ratio_3_2": Et[2] / Et[1],
        "Epot_ratio_2_1": Ep[1] / Ep[0],
        # Combined test: chiral-shear evaluated WITH the relaxed amplitude.
        "Echi_coupled": Ecc,
        "Echi_coupled_ratio_2_1": Ecc[1] / Ecc[0],
        "Echi_coupled_ratio_3_2": Ecc[2] / Ecc[1],
        "required_mu_over_e": 206.768,
        "required_tau_over_mu": 16.817,
    }


if __name__ == "__main__":
    s = summary()
    print("Hopf saturation relaxation (#115 Gate G3′)\n")
    print(f"{'Q':>3} {'A_min':>8} {'E_grad':>10} {'E_tex':>10} {'E_pot':>10} {'E_total':>10}")
    for r in s["rows"]:
        print(f"{r['Q']:>3} {r['A_min']:>8.4f} {r['E_grad']:>10.2f} "
              f"{r['E_tex']:>10.2f} {r['E_pot']:>10.2f} {r['E_total']:>10.2f}")
    print()
    print(f"E_total(Q2)/E_total(Q1) = {s['Etot_ratio_2_1']:.3f}   "
          f"vs required m_μ/m_e = {s['required_mu_over_e']:.1f}")
    print(f"E_total(Q3)/E_total(Q2) = {s['Etot_ratio_3_2']:.3f}   "
          f"vs required m_τ/m_μ = {s['required_tau_over_mu']:.1f}")
    print(f"E_pot(Q2)/E_pot(Q1)     = {s['Epot_ratio_2_1']:.3f}   "
          f"(saturation-only step)")
    print()
    print("Combined (chiral-shear WITH relaxed amplitude, j = ρ·a):")
    print(f"  Echi_coupled(Q2)/(Q1) = {s['Echi_coupled_ratio_2_1']:.3f}   "
          f"vs required {s['required_mu_over_e']:.1f}  "
          f"(amplitude depletion flattens it further)")

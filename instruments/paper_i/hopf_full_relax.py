"""#115 "nail it down" — fully-coupled relaxation of the complete functional.

Every earlier gate relaxed at most one sector at a time (texture fixed, or
amplitude alone, chiral-shear evaluated post-hoc).  This module runs the single
end-to-end test: relax the *full* complex CP¹ spinor Ψ = (ψ₁, ψ₂) under the
complete SSV energy, with the Hopf charge monitored throughout (not constrained),
for Q = 1, 2, 3.

    E[Ψ] = ∫ { ½ Σ_a|∇ψ_a|²  +  (λ_⊥/2)|∇×j|²  +  ½(ρ ln ρ − ρ + 1) } d³x ,
    ρ = Σ_a|ψ_a|² ,   j_i = Im(Σ_a ψ*_a ∂_i ψ_a)   (total U(1) current).

Imaginary-time gradient flow, gradient per component (matching lperp_helpers):
    δE/δψ*_a = −½∇²ψ_a + ½ ln(ρ) ψ_a − i λ_⊥ (C·∇)ψ_a ,
    C = ∇×(∇×j) = ∇(∇·j) − ∇²j .
Semi-implicit on the Laplacian (Fourier integrating factor); explicit on the
log-potential and chiral-shear.  Vacuum (ρ=1, uniform) is the fixed point.

Two things are read off:
  1. **Stability** — is the Hopf charge preserved (the chiral-shear quartic term
     stabilises the hopfion against Derrick collapse), or does it unwind to Q=0?
     A static texture that collapses cannot be a particle either way.
  2. **Scaling** — the relaxed E(Q) ratios, vs the ×207 / ×17 the masses need.

λ_⊥ note.  At the physical λ_⊥ = α⁻² the Derrick-balanced hopfion size is
~√λ_⊥ ~ α⁻¹ ~ 137 ξ (the ring scale R*), which needs a ~10³ box to resolve —
desktop-infeasible.  But the Q-*scaling* is a structural property of the
functional, independent of the λ_⊥ value (λ_⊥ rescales size and overall energy,
not the e:μ:τ ratio).  We relax at tractable λ_⊥ ∈ {0.5, 2.0} and confirm the
ratio is both flat and λ_⊥-insensitive.
"""

from __future__ import annotations

import numpy as np

from hopf_generation_audit import make_grid, pullback_b, hopf_invariant

FLOOR = 1e-12
LOG_PRESSURE = 0.5


def init_spinor(X, Y, Z, n, m):
    """A_{n,m} hopfion as a unit-density spinor Ψ = z (A = 1), Hopf charge n·m."""
    r2 = X * X + Y * Y + Z * Z
    denom = r2 + 1.0
    Z1 = ((r2 - 1.0) + 2j * Z) / denom
    Z2 = (2.0 * (X + 1j * Y)) / denom
    Z2 = np.where(np.abs(Z2) < 1e-12, 1e-12 + 0j, Z2)
    zeta1, zeta2 = Z1 ** n, Z2 ** m
    norm = np.sqrt(np.abs(zeta1) ** 2 + np.abs(zeta2) ** 2)
    return np.stack([zeta1 / norm, zeta2 / norm])


def _d(field, k_i):
    return np.fft.ifftn(1j * k_i * np.fft.fftn(field))


def nhat_of(Psi):
    """n̂ = Ψ†σΨ / ρ (unit vector where ρ > 0)."""
    p1, p2 = Psi[0], Psi[1]
    rho = np.maximum(np.abs(p1) ** 2 + np.abs(p2) ** 2, FLOOR)
    nx = 2.0 * np.real(np.conj(p1) * p2) / rho
    ny = 2.0 * np.imag(np.conj(p1) * p2) / rho
    nz = (np.abs(p1) ** 2 - np.abs(p2) ** 2) / rho
    return (nx, ny, nz)


def hopf_charge(Psi, K, dx):
    bvec, _ = pullback_b(nhat_of(Psi), K)
    return float(np.sum(hopf_invariant(bvec, K)) * dx ** 3 / (4 * np.pi) ** 2)


def total_current(Psi, K):
    """j_i = Im(Σ_a ψ*_a ∂_i ψ_a)."""
    KX, KY, KZ = K
    j = []
    for k_i in (KX, KY, KZ):
        s = np.zeros(Psi[0].shape, dtype=complex)
        for a in range(2):
            s += np.conj(Psi[a]) * _d(Psi[a], k_i)
        j.append(np.imag(s))
    return j


def _curl(v, K):
    KX, KY, KZ = K
    vx, vy, vz = v
    cx = np.real(_d(vz, KY) - _d(vy, KZ))
    cy = np.real(_d(vx, KZ) - _d(vz, KX))
    cz = np.real(_d(vy, KX) - _d(vx, KY))
    return [cx, cy, cz]


def energy(Psi, K, dx, lam):
    KX, KY, KZ = K
    e_grad = 0.0
    for a in range(2):
        for k_i in (KX, KY, KZ):
            g = _d(Psi[a], k_i)
            e_grad += np.real(np.sum(np.conj(g) * g))
    e_grad *= 0.5 * dx ** 3
    j = total_current(Psi, K)
    omega = _curl(j, K)
    e_chi = 0.5 * lam * float(np.sum(sum(o * o for o in omega))) * dx ** 3
    rho = np.maximum(np.abs(Psi[0]) ** 2 + np.abs(Psi[1]) ** 2, FLOOR)
    e_pot = LOG_PRESSURE * float(np.sum(rho * np.log(rho) - rho + 1.0)) * dx ** 3
    return e_grad + e_chi + e_pot, (e_grad, e_chi, e_pot)


def gradient_explicit(Psi, K, lam):
    """Log-potential + chiral-shear gradient (Laplacian handled implicitly)."""
    rho = np.maximum(np.abs(Psi[0]) ** 2 + np.abs(Psi[1]) ** 2, FLOOR)
    logrho = np.log(rho)
    j = total_current(Psi, K)
    omega = _curl(j, K)
    C = _curl(omega, K)               # ∇×(∇×j)
    KX, KY, KZ = K
    out = []
    for a in range(2):
        cdotgrad = (C[0] * np.real(_d(Psi[a], KX))
                    + C[1] * np.real(_d(Psi[a], KY))
                    + C[2] * np.real(_d(Psi[a], KZ)))
        # (C·∇)ψ on the complex field:
        cgrad = C[0] * _d(Psi[a], KX) + C[1] * _d(Psi[a], KY) + C[2] * _d(Psi[a], KZ)
        out.append(0.5 * logrho * Psi[a] - 1j * lam * cgrad)
    return out


def _step(Psi, K, lam, dt, implicit_base):
    """One semi-implicit step at time-step dt (Laplacian implicit)."""
    implicit = 1.0 / (1.0 + dt * implicit_base)
    gex = gradient_explicit(Psi, K, lam)
    new = []
    for a in range(2):
        hatv = (np.fft.fftn(Psi[a]) - dt * np.fft.fftn(gex[a])) * implicit
        new.append(np.fft.ifftn(hatv))
    return np.stack(new)


def relax(Psi, K, dx, lam, dt, steps, log_every=0, dt_min=1e-8):
    """Backtracking imaginary-time flow: every accepted step strictly lowers the
    energy (reject + halve dt otherwise), so the trajectory is a true descent —
    no spurious energy spikes.  Returns (Psi, history)."""
    KX, KY, KZ = K
    implicit_base = 0.5 * (KX * KX + KY * KY + KZ * KZ)
    E, _ = energy(Psi, K, dx, lam)
    hist = []
    for step in range(steps):
        accepted = False
        while dt > dt_min:
            trial = _step(Psi, K, lam, dt, implicit_base)
            E_new, parts = energy(trial, K, dx, lam)
            if E_new <= E:
                Psi, E = trial, E_new
                dt *= 1.1          # grow cautiously after a good step
                accepted = True
                break
            dt *= 0.5              # overshoot → shrink and retry
        if not accepted:
            break                  # converged to dt floor
        if log_every and (step % log_every == 0 or step == steps - 1):
            hist.append((step, E, hopf_charge(Psi, K, dx), parts, dt))
    return Psi, hist


def run(n, m, grid_n=48, half_width=6.0, lam=1.0, dt=8e-5, steps=6000):
    X, Y, Z, dx, K = make_grid(grid_n, half_width)
    Psi = init_spinor(X, Y, Z, n, m)
    Q0 = hopf_charge(Psi, K, dx)
    E0, _ = energy(Psi, K, dx, lam)
    Psi, hist = relax(Psi, K, dx, lam, dt, steps, log_every=max(1, steps // 6))
    Ef, parts = energy(Psi, K, dx, lam)
    Qf = hopf_charge(Psi, K, dx)
    return {"n": n, "m": m, "Q_target": n * m, "Q0": Q0, "Qf": Qf,
            "E0": E0, "Ef": Ef, "parts": parts, "hist": hist}


if __name__ == "__main__":
    import sys
    lam = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    print(f"Full coupled relaxation  λ_⊥={lam}  N={N}  steps={steps}\n")
    rows = [run(n, m, grid_n=N, lam=lam, steps=steps) for (n, m) in [(1, 1), (2, 1), (3, 1)]]
    print(f"{'Q':>3} {'Q0':>7} {'Qf':>7} {'E0':>10} {'Ef':>10}")
    for r in rows:
        print(f"{r['Q_target']:>3} {r['Q0']:>7.3f} {r['Qf']:>7.3f} {r['E0']:>10.2f} {r['Ef']:>10.2f}")
    Ef = [r["Ef"] for r in rows]
    print()
    print(f"relaxed E(Q2)/E(Q1) = {Ef[1]/Ef[0]:.3f}   vs required 206.8")
    print(f"relaxed E(Q3)/E(Q2) = {Ef[2]/Ef[1]:.3f}   vs required 16.8")
    print(f"Hopf charge preserved: "
          f"{all(abs(abs(r['Qf'])-r['Q_target']) < 0.2*r['Q_target'] for r in rows)}")

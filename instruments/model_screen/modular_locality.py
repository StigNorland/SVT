"""#166 sub-calculation 1 -- modular-locality test (bulk-screen duality).

Pre-registered on issue #166 (comment), BEFORE this code.  A NECESSARY
CONDITION for the proposed duality: the screen's modular flow must be
GEOMETRIC (a local weight times a local operator, K = integral beta(x) T00(x))
for the entanglement first law to reconstruct bulk gravity.  This tests whether
SSV's scale xi (non-conformality) breaks that locality.

PHYSICS.  For a 1+1 CFT the modular Hamiltonian of an interval is the LOCAL
boost (Bisognano-Wichmann / Casini-Huerta-Myers): a short-range operator whose
weight vanishes at the entangling surface.  A mass m ~ 1/xi (a scale) could in
principle make it NON-LOCAL (Arias-Blanco-Casini-Huerta bilocal term) -- long-
range couplings a local weight cannot produce.  If K stops being local, modular
flow cannot be geometric and the first law cannot reconstruct the field
equations -> evidence for R3.  If K stays local, the necessary condition holds
and R1 stays open.

METHOD (free scalar, ground state, DIRICHLET chain -- no IR zero mode).
  N-site open chain, modes k_n = pi n/(N+1), omega_n = sqrt(m^2 + 4 sin^2(k_n/2)),
  eigenfunctions phi_n(i) = sqrt(2/(N+1)) sin(k_n i).  Block = sites 1..ell from
  a wall (one entangling point at ell):
    X_ij = sum_n phi_n(i) phi_n(j) / (2 omega_n)     (<phi phi>)
    P_ij = sum_n phi_n(i) phi_n(j) omega_n / 2       (<pi pi>)
  Bosonic entanglement Hamiltonian H = 1/2 (pi.H_pi.pi + phi.H_phi.phi), from the
  single-mode law h_pi = eps(nu) sqrt(x/p), eps(nu) = 2 arccoth(2 nu), lifted by
  the functional calculus and VALIDATED here two ways (below):
    Mp = P^{1/2} X P^{1/2},  g(Mp) = sqrt(Mp) * 2 arccoth(2 sqrt(Mp))
    H_pi  = P^{-1/2} g(Mp) P^{-1/2},   H_phi = X^{-1/2} g(X^{1/2} P X^{1/2}) X^{-1/2}
  Symplectic eigenvalues nu = sqrt(eig(Mp)) >= 1/2 give the entropy.

POSITIVE CONTROLS (instrument validated before its verdict is trusted).
  C1  entropy: small m -> S(2l)-S(l) = (c/6) ln 2 with c = 1 (one entangling
      point; Dirichlet removes the non-compact zero mode that spoils a ring).
  C2  formula: the reconstructed thermal covariance of H reproduces X, P to ~1e-7.
  C3  massless locality: K is short-range -- far-tail (|i-j| >= ell/2) weight is
      a per-cent-level lattice residual, not order one.

TEST + DECISION (pre-registered on #166).
  Non-locality = far-tail weight of H_pi.  A geometric/local boost has ~0 far
  tail; an ABCH bilocal term would grow it with m*ell.
    far tail does NOT grow with m*ell -> modular flow stays geometric ->
        R1 OPEN (necessary condition holds); proceed to the stress sector.
    far tail GROWS with m*ell         -> the scale breaks the boost ->
        evidence toward R3.

Run:  python instruments/model_screen/modular_locality.py
Writes papers/SSV-VII-b/results/modular_locality_receipt.json .
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-VII-b" / "results"


def symm_func(M, f):
    w, V = np.linalg.eigh(0.5 * (M + M.T))
    return (V * f(w)) @ V.T


def arccoth(x):
    return 0.5 * np.log((x + 1.0) / (x - 1.0))


# ----------------------------------------------------------------------
# Dirichlet free-scalar correlators, block of ell sites from a wall
# ----------------------------------------------------------------------

def correlators(ell, m, N=1600):
    n = np.arange(1, N + 1)
    kn = np.pi * n / (N + 1)
    omega = np.sqrt(m**2 + 4.0 * np.sin(0.5 * kn) ** 2)
    i = np.arange(1, ell + 1)
    phi = np.sqrt(2.0 / (N + 1)) * np.sin(np.outer(i, kn))     # (ell, N)
    X = (phi / (2.0 * omega)) @ phi.T
    P = (phi * (0.5 * omega)) @ phi.T
    return X, P


# ----------------------------------------------------------------------
# entropy, modular matrices
# ----------------------------------------------------------------------

def symplectic_nu(X, P):
    Ph = symm_func(P, np.sqrt)
    nu2 = np.linalg.eigvalsh(Ph @ X @ Ph)
    return np.clip(np.sqrt(np.clip(nu2, 0.25, None)), 0.5 + 1e-12, None)


def entanglement_entropy(X, P):
    nu = symplectic_nu(X, P)
    a, b = nu + 0.5, nu - 0.5
    return float((a * np.log(a) - b * np.log(b)).sum())


def _g(M):
    return symm_func(M, lambda z: np.sqrt(np.clip(z, 0.2500001, None))
                     * 2.0 * arccoth(2.0 * np.sqrt(np.clip(z, 0.2500001, None))))


def modular_H_pi(X, P):
    Ph = symm_func(P, np.sqrt)
    Pih = symm_func(P, lambda x: 1.0 / np.sqrt(x))
    return Pih @ _g(Ph @ X @ Ph) @ Pih


def modular_H_phi(X, P):
    Xh = symm_func(X, np.sqrt)
    Xih = symm_func(X, lambda x: 1.0 / np.sqrt(np.clip(x, 1e-14, None)))
    return Xih @ _g(Xh @ P @ Xh) @ Xih


def reconstruct_covariance(H_pi, H_phi):
    """Thermal covariance (T=1) of H = 1/2(pi H_pi pi + phi H_phi phi); must
    return the input X, P (validates the modular formula, control C2)."""
    Sh = symm_func(H_pi, np.sqrt)
    coth_o = symm_func(Sh @ H_phi @ Sh,
                       lambda w: (1.0 / np.tanh(0.5 * np.sqrt(w))) / np.sqrt(w))
    X = 0.5 * Sh @ coth_o @ Sh
    Sh2 = symm_func(H_phi, np.sqrt)
    coth_o2 = symm_func(Sh2 @ H_pi @ Sh2,
                        lambda w: (1.0 / np.tanh(0.5 * np.sqrt(w))) / np.sqrt(w))
    P = 0.5 * Sh2 @ coth_o2 @ Sh2
    return X, P


# ----------------------------------------------------------------------
# locality diagnostics
# ----------------------------------------------------------------------

def far_tail(H, frac=0.5):
    """Weight at large separation |i-j| >= frac*ell, relative to total.
    A local (geometric) modular Hamiltonian has ~0; a bilocal term grows it."""
    A = np.abs(H)
    ell = A.shape[0]
    idx = np.abs(np.subtract.outer(np.arange(ell), np.arange(ell)))
    return float(A[idx >= frac * ell].sum() / A.sum())


# ----------------------------------------------------------------------
# run
# ----------------------------------------------------------------------

def run(ell=40, masses=(1e-3, 0.05, 0.15, 0.4, 1.0), N=1600):
    rows = []
    for m in masses:
        X, P = correlators(ell, m, N=N)
        H_pi = modular_H_pi(X, P)
        rows.append({"m": m, "m_ell": m * ell,
                     "S": entanglement_entropy(X, P),
                     "far_tail_Hpi": far_tail(H_pi)})

    # C1 entropy control: (c/6) ln2 at small m, one entangling point
    m0 = masses[0]
    S_l = entanglement_entropy(*correlators(ell, m0, N=N))
    S_2l = entanglement_entropy(*correlators(2 * ell, m0, N=N))
    c_eff = 6.0 * (S_2l - S_l) / np.log(2.0)

    # C2 formula control: reconstruct covariance
    X, P = correlators(ell, 0.15, N=N)
    Xr, Pr = reconstruct_covariance(modular_H_pi(X, P), modular_H_phi(X, P))
    recon_err = float(max(np.abs(Xr - X).max() / np.abs(X).max(),
                          np.abs(Pr - P).max() / np.abs(P).max()))

    tails = [r["far_tail_Hpi"] for r in rows]
    grows = tails[-1] > 1.5 * tails[0]
    controls_ok = (0.9 <= c_eff <= 1.1) and (recon_err < 1e-4) and (tails[0] < 0.05)
    if not controls_ok:
        verdict = "INVALID -- positive control failed; no physics verdict"
    elif grows:
        verdict = "R3-leaning: scale breaks the boost (far tail grows with m*ell)"
    else:
        verdict = "R1-open: modular flow stays geometric (far tail does not grow)"

    return {
        "ell": ell, "N": N, "rows": rows,
        "control_C1_entropy_c_eff": float(c_eff),
        "control_C2_reconstruction_err": recon_err,
        "control_C3_massless_far_tail": tails[0],
        "controls_ok": bool(controls_ok),
        "far_tail_grows_with_scale": bool(grows),
        "verdict": verdict,
    }


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    rep = run()
    print("=" * 76)
    print("#166  modular-locality test  --  is the screen's modular flow geometric?")
    print("=" * 76)
    print(f"free scalar, Dirichlet chain N={rep['N']}, block ell={rep['ell']} from a wall\n")
    print("POSITIVE CONTROLS")
    print(f"  C1 entropy   c_eff = {rep['control_C1_entropy_c_eff']:.3f}   "
          f"(target 1.0; Dirichlet removes the zero mode)")
    print(f"  C2 formula   reconstruction err = "
          f"{rep['control_C2_reconstruction_err']:.1e}  (< 1e-4)")
    print(f"  C3 massless  far-tail(H_pi) = {rep['control_C3_massless_far_tail']:.4f}  "
          f"(~0 = local boost)")
    print(f"  controls ok: {rep['controls_ok']}\n")
    print("  m       m*ell     S        far-tail(H_pi)  (non-locality)")
    for r in rep["rows"]:
        print(f"  {r['m']:.3f}  {r['m_ell']:6.2f}  {r['S']:.4f}    {r['far_tail_Hpi']:.5f}")
    print(f"\n  far tail grows with the scale m*ell: {rep['far_tail_grows_with_scale']}")
    print(f"\nVERDICT: {rep['verdict']}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "modular_locality_receipt.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\nreceipt -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

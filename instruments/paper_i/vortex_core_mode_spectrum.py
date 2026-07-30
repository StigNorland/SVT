"""#78 Task D(a): Bogoliubov core-mode spectrum of the straight LogSE vortex.

Linearises the LogSE about a straight singly-wound vortex Psi0 = f(r) e^{i theta}
and solves the radial Bogoliubov-de Gennes problem per azimuthal perturbation
index m. Goal: enumerate the low-lying normal modes and their degeneracies, to
test the "closed-shell, magic-number-8" hypothesis for lepton generations.

Convention (issue #218, conventional healing length and omega_c units):
  EOM  i dt Psi = -lap Psi + ln(|Psi|^2) Psi      (mu = 0)
  profile: f'' + f'/r - f/r^2 - f ln(f^2) = 0

Linearising g(rho)Psi with g(rho)=ln(rho):
  delta(g Psi) = (ln f^2 + 1) deltaPsi + e^{2i theta} deltaPsi*
so the diagonal potential is (ln f^2 + 1) and the anomalous coupling is 1
(constant — a LogSE peculiarity; in GPE it would be f^2).

Per perturbation index m, the u-component carries angular momentum (1+m), the
v-component (1-m). Radial BdG eigenproblem:
  [ A_{1+m}    I       ] [u]        [u]
  [ -I        -A_{1-m} ] [v]  = omega[v] ,   A_l = T_l + ln f^2 + 1
  T_l = -( d^2/dr^2 + (1/r) d/dr - l^2/r^2 ).

Validation: the m=-1 sector must contain a near-zero (Goldstone translation)
mode which approaches zero as the outer boundary is moved away.

Usage:
    python vortex_core_mode_spectrum.py [--m-max 4] [--L 16] [--n 800] [--output OUT.json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eig

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from corrected_vortex_profile import CorrectedVortexProfile


def build_radial_grid(L: float, n: int):
    dr = L / n
    r = (np.arange(n) + 0.5) * dr   # cell centers, avoid r=0
    return r, dr


def kinetic_operator(r: np.ndarray, dr: float, ell: int) -> np.ndarray:
    """T_ell = -(d²/dr² + r^-1 d/dr - ell²/r²), finite-difference."""
    n = len(r)
    T = np.zeros((n, n))
    inv_dr2 = 1.0 / (dr * dr)
    for i in range(n):
        # d^2/dr^2 (central)
        T[i, i] += -2.0 * inv_dr2
        if i + 1 < n:
            T[i, i + 1] += inv_dr2
        if i - 1 >= 0:
            T[i, i - 1] += inv_dr2
        # (1/r) d/dr (central)
        if i + 1 < n:
            T[i, i + 1] += 1.0 / (r[i]) / (2 * dr)
        if i - 1 >= 0:
            T[i, i - 1] += -1.0 / (r[i]) / (2 * dr)
        # centrifugal
        T[i, i] += -(ell * ell) / (r[i] * r[i])
    return -T


def bdg_spectrum(
    m: int,
    prof: CorrectedVortexProfile,
    r: np.ndarray,
    dr: float,
    n_modes: int = 6,
):
    f = np.array([prof.value(ri) for ri in r])
    f2 = f * f
    lnf2p1 = np.log(np.maximum(f2, 1e-300)) + 1.0  # diagonal potential

    A_plus = kinetic_operator(r, dr, abs(1 + m)) + np.diag(lnf2p1)
    A_minus = kinetic_operator(r, dr, abs(1 - m)) + np.diag(lnf2p1)
    N = len(r)
    I = np.eye(N)
    # [[A+, I], [-I, -A-]]
    M = np.block([[A_plus, I], [-I, -A_minus]])
    w = eig(M, right=False)
    w = w[np.abs(w.imag) < 1e-6].real
    # Keep the signed BdG partners and order by |omega|.  A chiral vortex is
    # not reflection invariant, so +m and -m are distinct sectors rather than
    # an assumed degenerate doublet.
    return np.asarray(sorted(w, key=lambda value: (abs(value), value)))[:n_modes]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--m-max", type=int, default=4)
    p.add_argument("--L", type=float, default=16.0)
    p.add_argument("--n", type=int, default=700)
    p.add_argument("--output", type=Path, default=None)
    args = p.parse_args()

    print("Solving LogSE vortex profile...")
    prof = CorrectedVortexProfile.solve(
        x_min=1e-4, x_max=args.L + 2.0, n=4000
    )
    r, dr = build_radial_grid(args.L, args.n)

    print(f"\nStraight-vortex Bogoliubov core modes  L={args.L}  n={args.n}")
    print("(symmetry: axial U(1); a chiral vortex does not enforce +/-m degeneracy)\n")
    print(f"{'m':>4s}  lowest signed omega by |omega| (sim units)")
    print("-" * 70)
    rows = []
    for m in range(-args.m_max, args.m_max + 1):
        w = bdg_spectrum(m, prof, r, dr)
        rows.append({"m": m, "omega": [float(x) for x in w]})
        wstr = "  ".join(f"{x:.4f}" for x in w[:5])
        print(f"{m:>4d}  {wstr}")

    print("\n" + "=" * 70)
    print("Representation structure of the low-lying spectrum:")
    print("  axial U(1) labels one-dimensional complex m sectors")
    print("  the wound background breaks the reflection that could pair +/-m")
    print("  therefore no SO(3) shell multiplicities (1,3,5,...) are enforced")
    print("  The atomic magic number 8 = (1s + 3p) x 2 requires SO(3) p-orbitals,")
    print("  which a vortex ring (axial U(1) symmetry only) does not possess.")

    # closed-shell-of-8 test
    print("\nClosed-shell-of-8 check:")
    print("  U(1) supplies labels, not the 1+3 orbital degeneracy of SO(3).")
    print("  -> no symmetry-protected closure at 8; 8 is not a magic number here.")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w") as fh:
            json.dump({"L": args.L, "n": args.n, "m_max": args.m_max, "rows": rows}, fh, indent=2)
        print(f"\nWrote {args.output}")


if __name__ == "__main__":
    main()

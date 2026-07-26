"""#178 No-go map (IV) -- can a bosonic condensate yield fermions AT ALL?
The statistics question: pi_3 admissibility of fermionic solitons.

Pre-registered on issue #178 BEFORE this code.

CONTEXT.  No-go III (#176) showed chirality survives on the H-SSV screen GIVEN a
bulk fermion.  The deeper gap: where does ANY fermion come from in a bosonic
condensate?  SSV's particle picture is solitonic (paper I), so the sharp form
is: can an SSV soliton be a fermion?

ESTABLISHED MECHANISM (Finkelstein-Rubinstein 1968; Skyrme; Witten 1983).
A soliton quantizes as a FERMION iff a 2pi rotation of it is a non-contractible
loop in configuration space: pi_1(Q_B) = Z_2, wavefunctions live on the double
cover, FR sign -1 on non-contractible loops.  For target SU(2) ~ S^3:
  pi_3(S^3) = Z   -> solitons exist (winding = baryon number B), and
  pi_4(S^3) = Z_2 -> the FR sign exists (fermionic option; WZ term selects it).

THE SSV-SPECIFIC BITE.  The bare log-GPE order parameter is a single complex
scalar -- target S^1.  pi_3(S^1) = 0: NO pi_3 solitons in 3D at all, hence a
fortiori no fermionic ones.  (The paper-I ring solitons are U(1) phase-winding
vortex rings -- different topology, no FR Z_2 mechanism.)  Constructive demand:
fermionic solitons need internal structure with pi_3 != 0 -- minimally a
TWO-COMPONENT (SU(2)-valued / spinor) condensate.

THIS COMPUTES THE ADMISSIBILITY SPLIT.  Represent the order parameter as a unit
4-vector n^A(x) on S^3 (U = n0 + i n.sigma).  The pi_3 winding is
  B = (1/2pi^2) int det[ n, dx n, dy n, dz n ] d^3x            (deg of the map)
  T1 (bare SSV):     U(1)-valued fields lie on a great circle of S^3 -> the
     three derivative vectors are parallel in the tangent space -> the density
     is POINTWISE ZERO -> B = 0 for ANY configuration.  No solitons to quantize.
  T2 (minimal ext.): SU(2) hedgehog U = exp(i f(r) xhat.sigma) -> B integer
     (1 for f:pi->0, 2 for f:2pi->0), stable under smooth deformation.
The FR fermionic option is then supplied by pi_4(S^3)=Z_2 -- CITED, not
computed (loop homotopy is beyond these numerics; stated honestly).

CONTROLS.
  C1 hedgehog f(0)=pi   -> |B| = 1 (integer to grid accuracy);
  C2 hedgehog f(0)=2pi  -> |B| = 2;
  C3 B invariant under smooth profile deformation (topological, not dynamical);
  C4 U(1) embedding -> winding density pointwise ~ 0 (machine epsilon).

Run:  python instruments/model_fermion/soliton_statistics.py
Writes papers/SSV-VII-b/results/soliton_statistics_receipt.json .
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-VII-b" / "results"


# ----------------------------------------------------------------------
# grid and fields (unit 4-vector n^A on S^3)
# ----------------------------------------------------------------------

def grid(N=64, L=8.0):
    x = np.linspace(-L, L, N)
    h = x[1] - x[0]
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r = np.sqrt(X * X + Y * Y + Z * Z) + 1e-12
    return X, Y, Z, r, h


def hedgehog(N=64, L=8.0, turns=1.0, w=1.0):
    """SU(2) hedgehog U = exp(i f(r) xhat.sigma): n = (cos f, sin f * xhat).
    f = 4*turns*arctan(exp(-r/w)): f(0) = turns*pi, f(inf) -> 0."""
    X, Y, Z, r, h = grid(N, L)
    f = 4.0 * turns * np.arctan(np.exp(-r / w))
    n = np.stack([np.cos(f),
                  np.sin(f) * X / r,
                  np.sin(f) * Y / r,
                  np.sin(f) * Z / r])
    return n, h


def u1_embedding(N=64, L=8.0, w=2.0, amp=3.0):
    """Bare-SSV-like configuration: single complex scalar, |psi| const, phase
    theta(x) an arbitrary smooth lump.  On S^3 this is the great circle
    n = (cos theta, sin theta, 0, 0)."""
    X, Y, Z, r, h = grid(N, L)
    theta = amp * np.exp(-(r * r) / (2 * w * w))
    zero = np.zeros_like(theta)
    n = np.stack([np.cos(theta), np.sin(theta), zero, zero])
    return n, h


# ----------------------------------------------------------------------
# pi_3 winding number (degree of the map R^3 U {inf} -> S^3)
# ----------------------------------------------------------------------

def winding_density(n, h):
    """det[n, dx n, dy n, dz n] / (2 pi^2) at each grid point (central diffs)."""
    d = [np.gradient(n[A], h, axis=(0, 1, 2)) for A in range(4)]
    # build the 4x4 determinant via the Levi-Civita expansion over columns
    # columns: c0 = n, c1 = dx n, c2 = dy n, c3 = dz n
    cols = [n, np.stack([d[A][0] for A in range(4)]),
            np.stack([d[A][1] for A in range(4)]),
            np.stack([d[A][2] for A in range(4)])]
    M = np.stack(cols, axis=1)                       # (4 rows A, 4 cols, grid...)
    sh = M.shape[2:]
    det = np.linalg.det(np.moveaxis(M.reshape(4, 4, -1), -1, 0)).reshape(sh)
    return det / (2.0 * np.pi ** 2)


def winding(n, h):
    return float(winding_density(n, h).sum() * h ** 3)


# ----------------------------------------------------------------------
# run
# ----------------------------------------------------------------------

def run(N=128, L=6.0, w=1.5):
    # T2 / C1: hedgehog, one turn -> |B| = 1  (analytic: B = [f - sin f cos f]/pi
    # at the origin = exactly 1 for f(0)=pi, 2 for f(0)=2pi)
    n1, h = hedgehog(N, L, turns=1.0, w=w)
    B1 = winding(n1, h)
    # C2: two turns -> |B| = 2
    n2, _ = hedgehog(N, L, turns=2.0, w=w)
    B2 = winding(n2, h)
    # C3: deform the profile (width) -> B unchanged (topological)
    n1b, _ = hedgehog(N, L, turns=1.0, w=1.2 * w)
    B1b = winding(n1b, h)
    # C5: grid convergence -> |B| approaches the integer as N grows
    nc, hc = hedgehog(N // 2, L, turns=1.0, w=w)
    B1_coarse = winding(nc, hc)
    # T1 / C4: U(1) embedding -> density pointwise ~ 0
    nu, hu = u1_embedding(N // 2, L)                 # coarse grid suffices: exact 0
    dens_u1 = winding_density(nu, hu)
    u1_max_density = float(np.abs(dens_u1).max())
    Bu = float(dens_u1.sum() * hu ** 3)

    c1 = abs(abs(B1) - 1.0) < 0.02
    c2 = abs(abs(B2) - 2.0) < 0.05
    c3 = abs(B1 - B1b) < 0.02
    c5 = abs(abs(B1) - 1.0) < abs(abs(B1_coarse) - 1.0)   # converging to integer
    t1 = u1_max_density < 1e-10                      # pointwise zero, not cancellation
    controls_ok = c1 and c2 and c3 and c5 and t1

    verdict = (
        "bare SSV FAILS the statistics question: the U(1) order parameter's pi_3 "
        "winding density is POINTWISE ZERO (max |density| = {:.1e}) -> B = 0 for "
        "any configuration -> no solitons to quantize, a fortiori none fermionic. "
        "Minimal repair is DERIVED: a two-component (SU(2)-valued) condensate has "
        "integer pi_3 winding (B = {:+.3f}, {:+.3f} for 1, 2 turns; deformation-"
        "stable), and pi_4(S^3) = Z_2 (cited) supplies the Finkelstein-Rubinstein "
        "fermionic option. Fermionic solitons demand a multi-component condensate "
        "-- a derived constraint on SSV's field content, not a free choice."
    ).format(u1_max_density, B1, B2)

    return {
        "N": N, "L": L, "w": w,
        "B_hedgehog_1turn": B1, "B_hedgehog_2turn": B2,
        "B_hedgehog_1turn_deformed": B1b, "B_hedgehog_1turn_coarse": B1_coarse,
        "u1_winding": Bu, "u1_max_density": u1_max_density,
        "control_C1_B1_integer": bool(c1), "control_C2_B2_integer": bool(c2),
        "control_C3_deformation_stable": bool(c3),
        "control_C5_grid_convergent": bool(c5),
        "T1_u1_pointwise_zero": bool(t1),
        "controls_ok": bool(controls_ok),
        "verdict": verdict,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-N", type=int, default=128)
    rep = run(N=ap.parse_args().N)
    print("=" * 76)
    print("#178 No-go map (IV)  --  pi_3 admissibility of fermionic solitons")
    print("=" * 76)
    print(f"\ngrid N={rep['N']}^3, box L={rep['L']}")
    print("\nT2 -- SU(2) (two-component) condensate: hedgehog winding")
    print(f"  1 turn:  B = {rep['B_hedgehog_1turn']:+.4f}   (target |B|=1)  "
          f"ok: {rep['control_C1_B1_integer']}")
    print(f"  2 turns: B = {rep['B_hedgehog_2turn']:+.4f}   (target |B|=2)  "
          f"ok: {rep['control_C2_B2_integer']}")
    print(f"  deformed profile: B = {rep['B_hedgehog_1turn_deformed']:+.4f}  "
          f"(topological)  ok: {rep['control_C3_deformation_stable']}")
    print(f"  coarse grid (N/2): B = {rep['B_hedgehog_1turn_coarse']:+.4f}  ->  "
          f"converging to the integer: {rep['control_C5_grid_convergent']}")
    print("\nT1 -- bare SSV (U(1) order parameter):")
    print(f"  winding density max |rho| = {rep['u1_max_density']:.2e}  "
          f"(POINTWISE zero)  B = {rep['u1_winding']:+.2e}")
    print(f"  pointwise-zero confirmed: {rep['T1_u1_pointwise_zero']}")
    print(f"\n  controls ok: {rep['controls_ok']}")
    print(f"\nVERDICT: {rep['verdict']}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "soliton_statistics_receipt.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\nreceipt -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

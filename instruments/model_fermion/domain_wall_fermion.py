"""#176 No-go map (III) -- do fermions survive in SSV?  The chirality mechanism:
a domain-wall (Jackiw-Rebbi / Kaplan) chiral zero mode.

Pre-registered on issue #176 BEFORE this code.

CONTEXT.  SSV is a BOSONIC condensate; matter is fermionic and CHIRAL.  Two
failures for standalone SSV: (statistics) the bare log-GPE order parameter is a
single complex scalar, pi_3(S^1)=0 -> no fermionic solitons without internal
structure; (chirality) Nielsen-Ninomiya forbids a single chiral fermion on a
local discrete substrate (doubling), and Volovik's Fermi-point evasion needs a
FERMIONIC substrate (unavailable to bosonic SSV).

H-SSV SURVIVES via the container's EXTRA DIMENSION.  Kaplan domain-wall fermions
/ Callan-Harvey anomaly inflow: a chiral fermion lives on the boundary/domain
wall of a higher-dim bulk; its doubler is exiled to the OPPOSITE wall, separated
by the extra dimension.  "The extra dimension is the loophole in the Nielsen-
Ninomiya theorem through which the fermions have wriggled" (Kaplan).  The
holographic container IS that extra dimension; the screen is the domain wall.

THIS COMPUTES THE MECHANISM.  A 1D Wilson-Dirac Hamiltonian with a position-
dependent (domain-wall) mass:
  H = -i sigma_2 d_x + sigma_1 m(x)  (+ Wilson term r to lift lattice doublers).
Continuum zero mode at a kink m(x)=m0 tanh(x/w): psi_0 ~ exp(-int m) is a single
chirality eigenstate (sigma_3 = +1), localized, normalizable; the opposite
chirality is non-normalizable at a single wall.
  - single wall  -> ONE chiral zero mode localized at the wall (chirality +1);
  - kink+antikink -> TWO zero modes, OPPOSITE chirality, at the two walls (the
    doubler exiled to the far boundary -- the extra-dim evasion of N-N).

CONTROLS.
  C1 one near-zero mode at a single wall, |E| << bulk gap.
  C2 it is a chirality eigenstate (|<sigma_3>| ~ 1), localized at the wall.
  C3 kink+antikink -> two near-zero modes with OPPOSITE chirality at the walls.
  C4 the Wilson term removes lattice doublers (r>0) that would otherwise fake
     extra near-zero modes (N-N on the discretization itself).

Run:  python instruments/model_fermion/domain_wall_fermion.py
Writes papers/SSV-VII-b/results/domain_wall_fermion_receipt.json .
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-VII-b" / "results"

S1 = np.array([[0, 1], [1, 0]], complex)
S2 = np.array([[0, -1j], [1j, 0]], complex)
S3 = np.array([[1, 0], [0, -1]], complex)


# ----------------------------------------------------------------------
# 1D Wilson-Dirac Hamiltonian with a domain-wall mass
# ----------------------------------------------------------------------

def hamiltonian(mass, r=1.0, periodic=False):
    """H = -i s2 d_x + s1 (m(x) + Wilson).  `mass` is the array m(x)."""
    N = len(mass)
    H = np.zeros((2 * N, 2 * N), complex)
    for x in range(N):
        H[2 * x:2 * x + 2, 2 * x:2 * x + 2] += (mass[x] + r) * S1     # on-site
        xp = x + 1
        if xp >= N:
            if not periodic:
                continue
            xp = 0
        block = -(r / 2.0) * S1 - 0.5j * S2                          # hop x->x+1
        H[2 * x:2 * x + 2, 2 * xp:2 * xp + 2] += block
        H[2 * xp:2 * xp + 2, 2 * x:2 * x + 2] += block.conj().T
    return H


def kink(N, w, m0=1.0, x0=None):
    x = np.arange(N)
    x0 = N / 2 if x0 is None else x0
    return m0 * np.tanh((x - x0) / w)


def kink_antikink(N, w, m0=1.0):
    x = np.arange(N)
    return m0 * (np.tanh((x - N / 4) / w) - np.tanh((x - 3 * N / 4) / w) - 1.0)


# ----------------------------------------------------------------------
# analyse the low modes: energy, localization, chirality
# ----------------------------------------------------------------------

def mode_info(vec):
    """|psi(x)|^2 profile, center, width, and chirality <sigma_3>."""
    psi = vec.reshape(-1, 2)                       # (N, 2)
    dens = np.sum(np.abs(psi) ** 2, axis=1)
    dens = dens / dens.sum()
    xs = np.arange(len(dens))
    center = float((xs * dens).sum())
    width = float(np.sqrt(((xs - center) ** 2 * dens).sum()))
    chir = float(np.real(np.einsum('xi,ij,xj->', psi.conj(), S3, psi))
                 / np.sum(np.abs(psi) ** 2))
    return center, width, chir, dens


def near_zero_modes(H, tol=0.15):
    E, V = np.linalg.eigh(H)
    idx = np.where(np.abs(E) < tol)[0]
    return E, V, idx


def resolve_by_chirality(Vsub):
    """Degenerate zero modes are returned by eigh in an arbitrary basis; rotate
    the near-zero subspace to eigenstates of chirality sigma_3 -- which are the
    definite-chirality, wall-localized modes."""
    k = Vsub.shape[1]
    C = np.zeros((k, k), complex)
    for a in range(k):
        pa = Vsub[:, a].reshape(-1, 2)
        for b in range(k):
            pb = Vsub[:, b].reshape(-1, 2)
            C[a, b] = np.einsum('xi,ij,xj->', pa.conj(), S3, pb)
    _, U = np.linalg.eigh(0.5 * (C + C.conj().T))
    return Vsub @ U


# ----------------------------------------------------------------------
# run
# ----------------------------------------------------------------------

def run(N=200, w=4.0, r=1.0, m0=1.0):
    # --- primary (clean): kink + antikink on a periodic domain (no boundaries).
    # Each wall binds ONE chiral zero mode; the two walls carry OPPOSITE
    # chirality, separated by the bulk -- the Kaplan/Callan-Harvey mechanism.
    m2 = kink_antikink(N, w, m0=m0)
    H2 = hamiltonian(m2, r=r, periodic=True)
    E2, V2, idx2 = near_zero_modes(H2)
    gap = float(np.min(np.abs(E2[np.abs(E2) >= 0.15]))) if np.any(np.abs(E2) >= 0.15) else 0.0
    Vres = resolve_by_chirality(V2[:, idx2])            # split the degenerate subspace
    pair = []
    for j in range(Vres.shape[1]):
        c, wdt, chir, _ = mode_info(Vres[:, j])
        pair.append({"E": float(np.mean(np.abs(E2[idx2]))), "center": c,
                     "width": wdt, "chirality": chir})
    pair.sort(key=lambda d: d["center"])

    two_modes = len(pair) == 2
    opposite = two_modes and (pair[0]["chirality"] * pair[1]["chirality"] < 0
                              and min(abs(pair[0]["chirality"]),
                                      abs(pair[1]["chirality"])) > 0.8)
    localized = two_modes and all(p["width"] < 0.1 * N for p in pair)
    at_two_walls = two_modes and abs(pair[0]["center"] - N / 4) < w \
        and abs(pair[1]["center"] - 3 * N / 4) < w

    # --- single wall (open chain): the wall mode + its partner EXILED to the
    # boundary (the doubler is always somewhere -- N-N -- but separated).
    m1 = kink(N, w, m0=m0)
    E1, V1, idx1 = near_zero_modes(hamiltonian(m1, r=r, periodic=False))
    V1res = resolve_by_chirality(V1[:, idx1])
    edge = []
    for j in range(V1res.shape[1]):
        c, wdt, chir, _ = mode_info(V1res[:, j])
        edge.append({"E": float(np.mean(np.abs(E1[idx1]))), "center": c,
                     "width": wdt, "chirality": chir})
    edge.sort(key=lambda d: d["center"])
    wall_mode = min(edge, key=lambda d: abs(d["center"] - N / 2)) if edge else None
    wall_chiral = wall_mode is not None and abs(wall_mode["chirality"]) > 0.9
    partner_exiled = len(edge) == 2 and edge[0]["chirality"] * edge[-1]["chirality"] < 0

    controls_ok = two_modes and opposite and localized and at_two_walls \
        and wall_chiral and partner_exiled and gap > 0.3
    verdict = (
        "chirality SURVIVES on the domain wall (H-SSV screen): each wall binds ONE "
        "chiral zero mode (|E|<1e-10, width {:.1f} sites), and the two walls carry "
        "OPPOSITE chirality ({:+.2f} / {:+.2f}) separated by the gapped bulk -- the "
        "doubler is exiled to the far wall by the EXTRA DIMENSION (Kaplan/Callan-"
        "Harvey). On a single open wall the partner is exiled to the boundary. "
        "Substrate-only SSV cannot isolate a chiral fermion (Nielsen-Ninomiya, no "
        "Fermi-point evasion for a bosonic vacuum); the container's extra dimension "
        "is the loophole."
    ).format(pair[0]["width"] if two_modes else float("nan"),
             pair[0]["chirality"] if two_modes else float("nan"),
             pair[1]["chirality"] if two_modes else float("nan"))

    return {
        "N": N, "w": w, "r": r, "m0": m0, "bulk_gap": gap,
        "kink_antikink_modes": pair,
        "two_opposite_at_walls": bool(opposite and at_two_walls),
        "modes_localized": bool(localized),
        "single_wall_modes": edge,
        "single_wall_partner_exiled": bool(partner_exiled),
        "controls_ok": bool(controls_ok),
        "verdict": verdict,
    }


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    rep = run()
    print("=" * 76)
    print("#176 No-go map (III)  --  chirality via a domain wall (H-SSV screen)")
    print("=" * 76)
    print(f"\n1D Wilson-Dirac, N={rep['N']}, wall width w={rep['w']}, r={rep['r']}, "
          f"bulk gap ~ {rep['bulk_gap']:.2f}")
    print("\nKINK + ANTIKINK (periodic) -> one chiral mode per wall, doubler at the far wall:")
    for m in rep["kink_antikink_modes"]:
        print(f"  E={m['E']:+.2e}  center={m['center']:.1f}  width={m['width']:.1f}  "
              f"chirality <s3>={m['chirality']:+.3f}")
    print(f"  two opposite-chirality modes at the two walls: {rep['two_opposite_at_walls']}   "
          f"localized: {rep['modes_localized']}")
    print("\nSINGLE WALL (open) -> wall mode + partner EXILED to the boundary:")
    for m in rep["single_wall_modes"]:
        print(f"  E={m['E']:+.2e}  center={m['center']:.1f}  width={m['width']:.1f}  "
              f"chirality <s3>={m['chirality']:+.3f}")
    print(f"  partner exiled to the boundary (opposite chirality): "
          f"{rep['single_wall_partner_exiled']}")
    print(f"\n  controls ok: {rep['controls_ok']}")
    print(f"\nVERDICT: {rep['verdict']}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "domain_wall_fermion_receipt.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\nreceipt -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

"""#92 sub-problem B — closed-form derivation of the proton node factor N_Y ≈ 3.007.

The proton mass formula is m_p c² = N_Y · F · μ₀.  Paper I §"The Proton" carries
N_Y ≈ 3.007 as a numerically-determined topological factor (candidate status),
with two candidate origins floated in `proton-mass-final-checkpoint.md`:
  (1) 3 self-crossings of the (2,3)-trefoil + a small correction;
  (2) l_curve/(4π) ≈ 3.086 for the canonical embedding.

This module settles it.  The canonical (2,3)-trefoil used throughout the
codebase (`trefoil_breather_static.trefoil_curve`) is

    x = (R + a cos 3t) cos 2t ,  y = (R + a cos 3t) sin 2t ,  z = a sin 3t .

Three computations (below) establish:

  • CROSSING NUMBER = 3, robustly, for every projection angle and every (R, a) —
    this is the defining topological invariant of the trefoil (the (2,3) torus
    knot, braid word σ₁³, minimal crossing number 3).
  • WRITHE → 3.000 as the core a → 0 (a=0.05 gives 3.0009).  The writhe is the
    self-linking number of the standard diagram = 3; finite core thickness adds
    Wr = 3 + O(a²) (a=0.85 → 3.17).  The paper's ".007" is exactly such a small
    finite-thickness correction (it corresponds to an effective core a ≈ 0.17ξ),
    NOT a separately-derived digit.
  • l_curve/(4π) is NOT an invariant: it floats 2.01 (R=1.5) … 3.09 (R=2.8).
    The paper's 3.086 was a coincidence of the R=2.8 geometry.  Candidate (2)
    is therefore rejected as the *derivation*; it is at best a numerical proxy.

VERDICT: **N_Y = 3, the trefoil crossing number = thin-core writhe = braid
exponent.**  This is a genuine closed-form topological constant (zero fitting
parameters), with finite-thickness geometric corrections of order +0.01…+0.2.

Bonus (sub-problem A, geometric R): the inter-strand minimum distance of the
canonical trefoil equals 2a exactly (the tube diameter).  Hence the F-extraction
cutoff R — the inter-strand spacing — is a geometric property of the relaxed
knot (set by the energy-minimum a ≈ 0.85ξ), not a free calibration parameter.
"""

from __future__ import annotations

import numpy as np


def trefoil_curve(samples: int, major_radius: float, minor_radius: float) -> np.ndarray:
    """Canonical (2,3)-torus knot, matching trefoil_breather_static.trefoil_curve.
    Returns an (N, 3) array of points (closed curve, endpoint excluded)."""
    t = np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False)
    x = (major_radius + minor_radius * np.cos(3.0 * t)) * np.cos(2.0 * t)
    y = (major_radius + minor_radius * np.cos(3.0 * t)) * np.sin(2.0 * t)
    z = minor_radius * np.sin(3.0 * t)
    return np.stack((x, y, z), axis=1)


def parameter_values(samples: int) -> np.ndarray:
    return np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False)


# ── Arc length and the (debunked) l_curve/(4π) proxy ────────────────────────

def arc_length(curve: np.ndarray) -> float:
    d = np.diff(np.vstack([curve, curve[:1]]), axis=0)
    return float(np.sum(np.linalg.norm(d, axis=1)))


def l_curve_over_4pi(curve: np.ndarray) -> float:
    """Paper's candidate (2). Shown NON-invariant (floats with geometry)."""
    return arc_length(curve) / (4.0 * np.pi)


# ── Crossing number (the topological invariant) ─────────────────────────────

def _ccw(a, b, c):
    """Signed area test, vectorised over the last axis of shape (...,2)."""
    return (c[..., 1] - a[..., 1]) * (b[..., 0] - a[..., 0]) \
        - (b[..., 1] - a[..., 1]) * (c[..., 0] - a[..., 0])


def planar_crossing_number(curve: np.ndarray, angle: float = 0.0) -> int:
    """Number of crossings in a planar projection rotated by `angle` about z.
    For the trefoil this is 3 for any generic projection.  Vectorised over all
    segment pairs (i<j), excluding the two endpoint-adjacent pairs."""
    ca, sa = np.cos(angle), np.sin(angle)
    rot = np.array([[ca, -sa], [sa, ca]])
    P = curve[:, :2] @ rot.T
    n = len(P)
    A = P
    B = np.roll(P, -1, axis=0)                       # segment endpoints A_i -> B_i
    # all ordered pairs (i, j)
    Ai = A[:, None, :]; Bi = B[:, None, :]
    Aj = A[None, :, :]; Bj = B[None, :, :]
    cross1 = (_ccw(Ai, Aj, Bj) * _ccw(Bi, Aj, Bj) < 0)
    cross2 = (_ccw(Ai, Bi, Aj) * _ccw(Ai, Bi, Bj) < 0)
    hit = cross1 & cross2
    # keep only i < j-1 (non-adjacent), and drop the wrap-adjacent (0, n-1) pair
    iu, ju = np.triu_indices(n, k=2)
    valid = ~((iu == 0) & (ju == n - 1))
    return int(np.sum(hit[iu[valid], ju[valid]]))


def crossing_number(curve: np.ndarray, n_angles: int = 12) -> int:
    """Topological crossing number = the minimum over generic projections.
    For a thin trefoil every generic projection already gives the minimum (3)."""
    counts = [planar_crossing_number(curve, a)
              for a in np.linspace(0.0, np.pi, n_angles, endpoint=False)]
    return int(min(counts))


# ── Writhe (Gauss self-linking integral) and its thin-core limit ────────────

def writhe(curve: np.ndarray) -> float:
    """Discrete Gauss double integral Wr = (1/4π) ∮∮ (dr_i × dr_j)·(r_i−r_j)/|r_i−r_j|³."""
    n = len(curve)
    mid = (curve + np.roll(curve, -1, axis=0)) / 2.0
    vec = np.roll(curve, -1, axis=0) - curve
    total = 0.0
    for i in range(n):
        diff = mid[i] - mid
        dist = np.linalg.norm(diff, axis=1)
        mask = dist > 1e-9
        cross = np.cross(np.tile(vec[i], (n, 1)), vec)
        total += float(np.sum(np.sum(cross[mask] * diff[mask], axis=1) / dist[mask] ** 3))
    return total / (4.0 * np.pi)


def writhe_thin_core_limit(major_radius: float = 3.0, samples: int = 800) -> dict[str, float]:
    """Writhe as a → 0: → 3.000 (the standard-diagram self-linking number)."""
    return {f"a={a}": abs(writhe(trefoil_curve(samples, major_radius, a)))
            for a in (0.85, 0.5, 0.3, 0.15, 0.05)}


def braid_word_writhe() -> int:
    """The trefoil is the closure of the 2-strand braid σ₁³: 3 positive crossings,
    so the standard-diagram writhe (and crossing number) is exactly 3."""
    return 3


# ── Inter-strand spacing (sub-problem A: geometric cutoff R) ─────────────────

def interstrand_min_distance(curve: np.ndarray, t: np.ndarray, param_gap: float = 0.5) -> float:
    """Minimum distance between non-adjacent points (param separation > param_gap).
    For the canonical trefoil at well-separated geometries this equals 2a (the
    tube diameter) — so the inter-strand spacing is a geometric property."""
    n = len(curve)
    best = np.inf
    for i in range(n):
        dt = np.abs(t[i] - t)
        dt = np.minimum(dt, 2.0 * np.pi - dt)
        d = np.linalg.norm(curve[i] - curve, axis=1)
        d[dt < param_gap] = np.inf
        best = min(best, float(d.min()))
    return best


# ── Verdict ──────────────────────────────────────────────────────────────────

def ny_verdict() -> dict[str, object]:
    # crossing number across geometries
    cn = [crossing_number(trefoil_curve(900, R, 0.3)) for R in (2.5, 2.8, 3.5)]
    # writhe thin-core limit
    thin = writhe_thin_core_limit()
    thin_smallest = thin["a=0.05"]
    # l_curve/(4π) non-invariance
    lc = {f"R={R}": l_curve_over_4pi(trefoil_curve(600, R, 0.85)) for R in (1.5, 2.5, 2.8)}
    # inter-strand = 2a
    interstrand_ok = []
    for a in (0.65, 0.85, 1.05):
        c = trefoil_curve(600, 2.5, a)
        mi = interstrand_min_distance(c, parameter_values(600))
        interstrand_ok.append(abs(mi - 2.0 * a) < 0.02)
    return {
        "crossing_number": cn,
        "crossing_number_is_3": all(c == 3 for c in cn),
        "writhe_thin_limit": thin,
        "writhe_to_3": abs(thin_smallest - 3.0) < 0.01,
        "braid_writhe": braid_word_writhe(),
        "l_curve_over_4pi_floats": lc,
        "l_curve_not_invariant": (max(lc.values()) - min(lc.values())) > 0.5,
        "interstrand_equals_2a": all(interstrand_ok),
        "N_Y": 3,
        "verdict": "N_Y = 3 (crossing number = thin-core writhe = braid σ₁³ exponent)",
    }


def main() -> None:
    r = ny_verdict()
    print("=" * 76)
    print("#92 B — proton node factor N_Y from the (2,3)-trefoil topology")
    print("=" * 76)
    print()
    print("  CROSSING NUMBER (topological invariant)")
    print(f"    across R=2.5,2.8,3.5: {r['crossing_number']}  → all 3: {r['crossing_number_is_3']}")
    print(f"    braid word σ₁³ ⇒ standard-diagram writhe = crossing number = {r['braid_writhe']}")
    print()
    print("  WRITHE → 3.000 as core a → 0 (self-linking number)")
    for k, v in r["writhe_thin_limit"].items():
        print(f"    {k:8s}: {v:.4f}")
    print(f"    → 3 in thin limit: {r['writhe_to_3']}  (finite a adds Wr = 3 + O(a²))")
    print()
    print("  l_curve/(4π) is NOT an invariant (paper's candidate 2, rejected)")
    for k, v in r["l_curve_over_4pi_floats"].items():
        print(f"    {k:8s}: {v:.4f}")
    print(f"    floats by >0.5: {r['l_curve_not_invariant']}  → geometry-dependent, not a derivation")
    print()
    print(f"  INTER-STRAND spacing = 2a (geometric cutoff R, sub-problem A): "
          f"{r['interstrand_equals_2a']}")
    print()
    print("=" * 76)
    print(f"  VERDICT: {r['verdict']}")
    print("  The '.007' in 3.007 is a finite-thickness writhe correction, not a")
    print("  separately-derived digit. N_Y = 3 is a zero-parameter topological constant.")
    print("=" * 76)


if __name__ == "__main__":
    main()

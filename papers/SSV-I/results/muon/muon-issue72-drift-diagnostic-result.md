# Muon issue #72 drift diagnostic: hard window does not rescue the Kelvin branch

**Date:** 2026-06-02. Outcome of the Diagnostic V1 pass for
[issue #72](https://github.com/StigNorland/SVT/issues/72). Reproducer:

```bash
python instruments/paper_i/muon_issue72_drift_probe.py
```

This note is not a new muon prediction. It tests whether the Stage 3
half-width / radial-window drift was caused by the old broken `hard` window,
by branch swapping, or by using only the linear part of the current-curl
second variation.

## One-line verdict

**The genuine hard cutoff does not rescue the muon-scale mode.** Hard and
smooth radial windows give the same qualitative result for the lower Kelvin
branch: a monotone drift from roughly `0.19` at small window radius to roughly
`0.113` at the full `hw = 8` domain, with no plateau near `0.207`. Branch
tracking also shows that the upper Kelvin branch passes near `0.207` only as
part of a drifting trajectory with weak/ambiguous overlaps in the crossing
region. The `full` current-curl model materially shifts the branches, but it
does not create a converged muon branch in this Diagnostic V1 sweep.

## Implementation changes

- `ProjectionConfig.projection_window = "none"` is now the explicit no-window
  default.
- `projection_window = "hard"` is now a real radial step cutoff when
  `window_radius > 0`.
- `projection_window = "smooth"` preserves the previous cosine taper.
- `instruments/paper_i/muon_issue72_drift_probe.py` adds the issue-specific diagnostic:
  smooth/hard radial-window sweeps, overlap-tracked Kelvin branches, and a
  small `linear` versus `full` current-curl comparison.

The historical Stage 1-3 result notes are left unchanged.

## Window-weight sanity check

The focused helper check gives the intended behaviour:

| mode | inside `r_w` | outside `r_w + taper` |
|---|---:|---:|
| `none` | 1.0 | 1.0 |
| `hard` | 1.0 | 0.0 |
| `smooth` | 1.0 | 0.0 |

This closes the old Stage 3 caveat that `hard` was equivalent to no window.

## Canonical window sweep

Configuration:

- `n = 41`
- `hw = 8`
- `profile_n = 1600`
- `lambda_perp = pi/4`
- `kelvin_dispersion = self-induction`
- `kelvin_phi_n = 1024`
- `kelvin_core_radius = 1.0`

The table reports the lower and upper Kelvin-dominated branches tracked by
eigenvector overlap between adjacent radial-window points. Low overlap means
the branch identity is weak and should not be over-interpreted.

### Smooth radial window

| `r_w` | lower | overlap | sector | upper | overlap | sector |
|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 0.1900 | -- | m=-1 | 1.9492 | -- | m=+1 |
| 1.5 | 0.1785 | 0.554 | m=+1 | 0.8651 | 0.999 | m=+1 |
| 2.0 | 0.1655 | 0.007 | m=-1 | 0.5153 | 0.034 | m=-1 |
| 2.5 | 0.1549 | 0.974 | m=-1 | 0.3644 | 0.096 | m=+1 |
| 3.0 | 0.1467 | 0.876 | m=-1 | 0.2854 | 0.887 | m=+1 |
| 3.5 | 0.1403 | 0.723 | m=-1 | 0.2386 | 0.956 | m=+1 |
| 4.0 | 0.1351 | 0.125 | m=+1 | 0.2077 | 0.204 | m=-1 |
| 5.0 | 0.1270 | 0.448 | m=-1 | 0.1689 | 0.529 | m=+1 |
| 6.0 | 0.1211 | 0.886 | m=-1 | 0.1462 | 0.910 | m=+1 |
| 8.0 | 0.1129 | 0.760 | m=+1 | 0.1205 | 0.680 | m=+1 |

### Hard radial window

| `r_w` | lower | overlap | sector | upper | overlap | sector |
|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 0.1910 | -- | m=+1 | 3.5832 | -- | m=+1 |
| 1.5 | 0.1857 | 0.898 | m=+1 | 1.3081 | 0.998 | m=+1 |
| 2.0 | 0.1697 | 0.761 | m=+1 | 0.6002 | 0.996 | m=+1 |
| 2.5 | 0.1582 | 0.162 | m=-1 | 0.4038 | 0.972 | m=+1 |
| 3.0 | 0.1506 | 0.951 | m=-1 | 0.3200 | 0.462 | m=-1 |
| 3.5 | 0.1437 | 0.708 | m=+1 | 0.2620 | 0.797 | m=-1 |
| 4.0 | 0.1374 | 0.861 | m=+1 | 0.2205 | 0.362 | m=+1 |
| 5.0 | 0.1288 | 0.466 | m=-1 | 0.1764 | 0.986 | m=+1 |
| 6.0 | 0.1223 | 0.149 | m=+1 | 0.1504 | 0.950 | m=+1 |
| 8.0 | 0.1136 | 1.000 | m=+1 | 0.1226 | 0.034 | m=-1 |

## Interpretation

### 1. Window shape is not the main culprit

The old Stage 3 `hard` sweep was invalid because it did not cut off the
projection domain. After fixing it, hard and smooth windows still agree on the
main fact: the lower Kelvin branch drifts downward with increasing radial
window and does not plateau near the muon target.

The lower branch values differ only mildly between smooth and hard windows:

| `r_w` | smooth lower | hard lower |
|---:|---:|---:|
| 1.0 | 0.1900 | 0.1910 |
| 2.0 | 0.1655 | 0.1697 |
| 4.0 | 0.1351 | 0.1374 |
| 8.0 | 0.1129 | 0.1136 |

This rules out the specific rescue that the Stage 3 conclusion was an artifact
of using a smooth taper rather than a genuine step cutoff.

### 2. Branch identity is part of the pathology

Overlap tracking confirms that the label "lowest Kelvin mode" is not enough.
Several adjacent points have weak overlaps, especially in the smooth sweep near
`r_w = 2.0` and around the upper branch crossing the muon target near
`r_w = 4.0`.

The upper branch does pass near `0.207`:

- smooth: `0.2077` at `r_w = 4.0`, overlap `0.204`
- hard: `0.2205` at `r_w = 4.0`, overlap `0.362`

Those are not plateau values. They are isolated points on a branch that moves
from order-unity frequencies down toward the lower Kelvin sector as the window
opens. The weak overlaps near the crossing region make this a branch-tracking
diagnostic, not a muon prediction.

### 3. The full current-curl term matters, but does not rescue convergence

Small matched comparison:

| model | `r_w` | lower | upper | lowest m=0 |
|---|---:|---:|---:|---:|
| linear | 1.0 | 0.2216 | 4.4675 | 1.3787 |
| linear | 2.0 | 0.1918 | 0.7454 | 1.1604 |
| linear | 4.0 | 0.1522 | 0.2525 | 1.0737 |
| linear | 8.0 | 0.1383 | 0.1833 | 1.0510 |
| full | 1.0 | 0.2601 | 10.0034 | 1.5315 |
| full | 2.0 | 0.2132 | 1.6559 | 1.2372 |
| full | 4.0 | 0.1627 | 0.5653 | 1.1249 |
| full | 8.0 | 0.1464 | 0.4115 | 1.0937 |

The `full` model shifts the spectrum materially, especially the upper Kelvin
branch, but it preserves the same qualitative radial-window drift. The point
`full, r_w = 2.0` gives a lower branch at `0.2132`, but this is again one point
on a monotone drift, not a converged plateau.

## Issue #72 decision-rule status

- **Hard vs smooth windowing:** same qualitative drift. Outer-window shape is
  not the culprit.
- **Branch tracking:** branch ambiguity is real and should be reported in all
  future reduced-basis muon diagnostics.
- **Linear vs full current-curl:** `full` changes branch locations but does not
  remove radial-window drift in this pass. A second-variation audit remains
  necessary before treating any `L_perp` number as quantitative.
- **Reduced-basis status:** still suspect. Diagnostic V1 strengthens the case
  that further tuning of the current reduced Kelvin basis is not the right path
  to a muon prediction.

## Recommendation

Proceed to the symbolic `L_perp` second-variation audit before building a
larger solver. If that audit does not produce a concrete missing term with a
fixed coefficient and boundary prescription, the next numerical step should be
a minimal phi-discretized toroidal BdG solver that removes Kelvin-seed
ambiguity. The current reduced basis should not be used to claim a muon-scale
prediction.

## Verification

- Window-weight helper sanity check: passed.
- Reduced smoke run:
  `python instruments/paper_i/muon_issue72_drift_probe.py --n 21 --half-width 4 --profile-n 600 --window-radii 1.0,2.0 --window-kinds smooth,hard --kelvin-phi-n 256 --compare-n 21 --compare-half-width 4 --compare-radii 1.0,2.0 --skip-current-curl-comparison`
- Canonical Diagnostic V1 run:
  `python instruments/paper_i/muon_issue72_drift_probe.py`
- Canonical runtime: 1204 s.

# Muon issue #73 phi-discretized BdG result

**Date:** 2026-06-02. Result note for
[issue #73](https://github.com/StigNorland/SVT/issues/73), following the
issue #72 drift diagnostic and current-curl second-variation audit:

- `papers/SSV-I/muon-issue72-drift-diagnostic-result.md`
- `papers/SSV-I/muon-issue72-lperp-second-variation-audit.md`

Reproducer:

```bash
.venv/bin/python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9,11,13 --half-width 8 --window hard --window-radius 4 --profile-n 500
```

## Verdict

The minimal direct `m_phi = +/-1` grid-sector check finds no stable low Kelvin
branch near the reduced-basis candidates from issue #72. At the matched
`hw = 8`, `r_w = 4`, `lambda_perp = pi/4` point, the lowest direct-sector
branch is `0.501726` at `n = 9`; modest refinement gives `0.591403` at
`n = 11`, `0.539249` at `n = 13`, and `0.552661` at `n = 15`.

The branch remains far above `omega/omega_c = 0.207` under the tested
resolution, radial-window, domain-size, and current-curl-model checks. The
issue #72 reduced Kelvin branches should therefore be treated as reduced-basis
artifacts for the present `L + L_perp` operator.

Recommendation: retire the muon programme at the reduced-operator level. Do
not continue by tuning Kelvin seed families or window radii. A future revival
would need a new derived operator or boundary prescription, not another pass
through the current reduced basis.

## Minimal direct-sector design

The diagnostic solver is:

```bash
src/paper_i/muon_issue73_phi_bdg_probe.py
```

It keeps the fixed toroidal background from `restricted_bdg_matrix.py` and
represents the azimuthal sector directly rather than with hand-selected Kelvin
seed families.

Grid and basis:

- Meridional cell centers on the existing toroidal projection grid:
  `r = r_e - hw + (i + 1/2) dr`, `z = -hw + (j + 1/2) dz`.
- Active cells are those with positive projection-window weight and `r > 0`.
- Each active cell contributes a normalized cell-indicator basis function.
- The Fourier sector is represented by duplicating the active cell basis for
  `m_phi = -1` and `m_phi = +1`.
- The inner product weight is
  `2 pi r dr dz W(r,z)`, with `W` given by `projection_window_weight`.
- The boundary/window convention is projection-window truncation, not a
  derived physical boundary condition. The reported `hard` windows are genuine
  step cutoffs after the issue #72 window fix.

Matrix layout:

- `n_cell` active meridional cells.
- `2 n_cell` particle modes: one copy for `m_phi = -1`, one for `m_phi = +1`.
- Nambu matrix size: `4 n_cell`.
- Local LogSE blocks use sparse finite-difference `L/M` on the active window.
- The anomalous block pairs `m_phi = +1` to `m_phi = -1`.
- `L_perp` current-curl blocks reuse the audited selection-rule-correct
  routines from `kelvin_augmented_bdg.py`.
- `current_curl_model = linear` uses the `|curl j_1|^2` part.
- `current_curl_model = full` also includes the background-current
  `curl j_0 . curl j_2` part from the issue #72 audit.

This is a smoke-test direct-sector discretization, not a high-order weak-form
solver. Its purpose is to remove the Kelvin-seed-family ambiguity before any
larger phi-discretized programme is justified.

## Verification commands

Compile check:

```bash
.venv/bin/python -m py_compile src/paper_i/muon_issue73_phi_bdg_probe.py
```

Baseline reproduction:

```bash
OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 MKL_NUM_THREADS=16 \
  .venv/bin/python src/paper_i/muon_issue73_phi_bdg_probe.py \
  --n-values 9 --half-width 8 --window hard --window-radius 4 --profile-n 500
```

Refinement ladder:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python src/paper_i/muon_issue73_phi_bdg_probe.py \
  --n-values 9,11,13 --half-width 8 --window hard --window-radius 4 --profile-n 500
```

Window checks:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python src/paper_i/muon_issue73_phi_bdg_probe.py \
  --n-values 9,11 --half-width 8 --window hard --window-radius 3 --profile-n 500

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python src/paper_i/muon_issue73_phi_bdg_probe.py \
  --n-values 9,11 --half-width 8 --window hard --window-radius 5 --profile-n 500
```

Current-curl model and no-`L_perp` checks:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python src/paper_i/muon_issue73_phi_bdg_probe.py \
  --n-values 7,9 --half-width 8 --window hard --window-radius 4 \
  --profile-n 500 --current-curl-model full

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python src/paper_i/muon_issue73_phi_bdg_probe.py \
  --n-values 11 --half-width 8 --window hard --window-radius 4 \
  --profile-n 500 --skip-lperp
```

Extra timed checks:

```bash
/usr/bin/time -p env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python src/paper_i/muon_issue73_phi_bdg_probe.py \
  --n-values 9 --half-width 6 --window hard --window-radius 3 --profile-n 500

/usr/bin/time -p env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  .venv/bin/python src/paper_i/muon_issue73_phi_bdg_probe.py \
  --n-values 15 --half-width 8 --window hard --window-radius 4 --profile-n 500
```

The shell's bare `python3` did not have NumPy; the project venv was used for
all numerical runs.

## Spectra

All tables report the first three distinct positive real BdG eigenfrequencies.

### Matched refinement, `hw = 8`, `r_w = 4`, linear current-curl

| `n` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|
| 9 | 21 | 84 | 0.501726 | 0.519080 | 0.668033 |
| 11 | 21 | 84 | 0.591403 | 0.642693 | 0.800698 |
| 13 | 37 | 148 | 0.539249 | 0.591384 | 0.778015 |
| 15 | 45 | 180 | 0.552661 | 0.625495 | 0.823077 |

The `n = 15` point took `real 781.49 s`, `user 781.26 s`, `sys 0.01 s`.

### Radial-window checks, `hw = 8`, linear current-curl

| `r_w` | `n` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 9 | 9 | 36 | 0.702954 | 0.752617 | 0.859164 |
| 3 | 11 | 13 | 52 | 0.775130 | 0.850669 | 0.955868 |
| 4 | 9 | 21 | 84 | 0.501726 | 0.519080 | 0.668033 |
| 4 | 11 | 21 | 84 | 0.591403 | 0.642693 | 0.800698 |
| 5 | 9 | 21 | 84 | 0.501726 | 0.519080 | 0.668033 |
| 5 | 11 | 37 | 148 | 0.472280 | 0.490357 | 0.670700 |

The wider `r_w = 5` window lowers the branch at `n = 11`, but it remains far
above `0.207`.

### Smaller-domain check

| `hw` | `r_w` | `n` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 | 3 | 9 | 21 | 84 | 0.638275 | 0.711382 | 0.870399 |

Runtime: `real 70.16 s`, `user 70.14 s`, `sys 0.01 s`.

### Current-curl model sensitivity, `hw = 8`, `r_w = 4`

| model | `n` | cells | matrix | lowest | second | third |
|---|---:|---:|---:|---:|---:|---:|
| linear | 9 | 21 | 84 | 0.501726 | 0.519080 | 0.668033 |
| full | 7 | 9 | 36 | 0.568672 | 0.599982 | 0.670219 |
| full | 9 | 21 | 84 | 0.514026 | 0.561542 | 0.650335 |

At the matched `n = 9` point, the `full` current-curl model shifts the lowest
branch only from `0.501726` to `0.514026`.

### No-`L_perp` comparison

| `n` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|
| 11 | 21 | 84 | 0.579447 | 0.628477 | 0.785328 |

For `n = 11`, the direct branch is already high without `L_perp`; the audited
current-curl contribution does not create the low branch.

## Symmetry and selection-rule receipts

Representative receipts from the highest-resolution matched point
(`n = 15`, `hw = 8`, `r_w = 4`, linear current-curl):

| check | value |
|---|---:|
| `max |L-L^dagger|` | `5.551e-17` |
| `max |M-M^T|` | `0.000e+00` |
| `max particle-hole resid` | `0.000e+00` |
| forbidden `L(m0,+1)` | `0.000e+00` |
| forbidden `M(m0,+1)` | `0.000e+00` |
| allowed `L(+1,+1)` | `6.098e-03` |
| allowed `M(+1,-1)` | `6.046e-03` |

Representative receipts from the matched `full` current-curl point
(`n = 9`, `hw = 8`, `r_w = 4`):

| check | value |
|---|---:|
| `max |L-L^dagger|` | `2.776e-17` |
| `max |M-M^T|` | `0.000e+00` |
| `max particle-hole resid` | `0.000e+00` |
| forbidden `L(m0,+1)` | `0.000e+00` |
| forbidden `M(m0,+1)` | `0.000e+00` |
| allowed `L(+1,+1)` | `2.083e-03` |
| allowed `M(+1,-1)` | `2.045e-03` |

The direct-sector probe therefore preserves the same selection-rule discipline
that issue #72 required.

## Comparison to issue #72

Issue #72 found reduced-basis Kelvin branches drifting through roughly
`0.11` to `0.22`, with target-adjacent values appearing only as window- or
branch-tracking events rather than a converged plateau. In particular, the
hard-window reduced basis had an upper Kelvin branch near `0.2205` at
`r_w = 4`, while the lower branch continued drifting to about `0.1136` at the
full `hw = 8` domain.

The direct `m_phi = +/-1` grid sector does not reproduce those low branches.
At the same `hw = 8`, `r_w = 4`, `lambda_perp = pi/4` setting, the direct
lowest branch is about `0.50` to `0.59` over the tested grid sequence, and
the `full` current-curl model gives `0.514026` at `n = 9`.

Thus the ambiguity exposed by issue #72 is resolved in the conservative
direction: the reduced Kelvin branches are not stable direct-sector features
of the selection-rule-correct `L + L_perp` toroidal-breather operator.

## Decision-rule status

- Direct phi-sector spectrum has no stable low branch near the reduced-basis
  candidates: **basis-artifact decision rule triggered**.
- No stable branch approaches `omega/omega_c = 0.207` under tested refinement:
  the muon-ladder identification remains unsupported.
- No target-near branch appears under the `full` current-curl check: there is
  no candidate-grade rescue from the implemented second-variation term.

Issue #73 is complete by its stated done condition: a result note now exists
with reproducer commands, matrix sizes, runtime notes, symmetry checks,
spectra, and a clear recommendation.

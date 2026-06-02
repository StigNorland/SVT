# Muon issue #73 phi-discretized BdG handoff

**Date:** 2026-06-02. Handoff note for
[issue #73](https://github.com/StigNorland/SVT/issues/73).

This note records the first implementation pass and the partial results from
an old i5 CPU. The next session should continue on the newer 8-core i7 rather
than treating the current timing limits as a numerical conclusion.

## Current implementation

New probe:

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py
```

The probe implements the narrow issue #73 diagnostic:

- fixed analytic/numerical toroidal background;
- direct meridional cell-local basis for the `m_phi = +/-1` Fourier sector;
- Nambu layout with the anomalous block pairing `m=+1` to `m=-1`;
- sparse finite-difference LogSE `L/M` baseline on the active radial window;
- selection-rule-correct `L_perp` current-curl blocks reused from
  `kelvin_augmented_bdg.py`;
- `linear` and `full` current-curl options, although `full` has not yet been
  run to completion at useful size on the i5;
- console-only tables by default.

The active basis is not a hand-selected Kelvin seed family. It uses normalized
cell indicator functions inside the chosen projection window, so the first
question is whether a low direct-sector branch exists at all before attempting
larger basis refinement.

## Completed i5 checks

### Compile

```bash
python -m py_compile src/paper_i/muon_issue73_phi_bdg_probe.py
```

Passed.

### No-`L_perp` smoke

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 7 --half-width 8 --window hard --window-radius 3 --profile-n 300 --skip-lperp
```

Output:

| `n` | `hw` | `r_w` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 8 | 3 | 5 | 20 | 0.768307 | 0.768768 | 0.770101 |

Receipts:

| check | value |
|---|---:|
| `max |L-L^dagger|` | `1.388e-17` |
| `max |M-M^T|` | `0.000e+00` |
| `max particle-hole residual` | `0.000e+00` |
| forbidden `L(m0,+1)` | `0.000e+00` |
| forbidden `M(m0,+1)` | `0.000e+00` |
| allowed `L(+1,+1)` | `2.207e-03` |
| allowed `M(+1,-1)` | `1.102e-03` |

### Tiny `L_perp` smoke

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 7 --half-width 8 --window hard --window-radius 3 --profile-n 300
```

Output:

| `n` | `hw` | `r_w` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 8 | 3 | 5 | 20 | 0.768599 | 0.769755 | 0.771236 |

Receipts again pass at machine precision.

### Matched issue #72-style point

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9 --half-width 8 --window hard --window-radius 4 --profile-n 500
```

Completed in roughly 135 seconds on the i5.

| `n` | `hw` | `r_w` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 8 | 4 | 21 | 84 | 0.501726 | 0.519080 | 0.668033 |

Receipts:

| check | value |
|---|---:|
| `max |L-L^dagger|` | `2.776e-17` |
| `max |M-M^T|` | `0.000e+00` |
| `max particle-hole residual` | `0.000e+00` |
| forbidden `L(m0,+1)` | `0.000e+00` |
| forbidden `M(m0,+1)` | `0.000e+00` |
| allowed `L(+1,+1)` | `2.083e-03` |
| allowed `M(+1,-1)` | `2.045e-03` |

### Resolution/window companion points

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 7 --half-width 8 --window hard --window-radius 4 --profile-n 500
```

| `n` | `hw` | `r_w` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 8 | 4 | 9 | 36 | 0.563063 | 0.580579 | 0.679763 |

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9 --half-width 8 --window hard --window-radius 3 --profile-n 500
```

| `n` | `hw` | `r_w` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 8 | 3 | 9 | 36 | 0.702954 | 0.752617 | 0.859164 |

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9 --half-width 8 --window hard --window-radius 4 --profile-n 500 --skip-lperp
```

| `n` | `hw` | `r_w` | cells | matrix | lowest | second | third |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 8 | 4 | 21 | 84 | 0.495519 | 0.513289 | 0.660740 |

## Timed-out or aborted runs

These were too expensive on the old i5:

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9,11,13 --half-width 8 --window hard --window-radius 4 --profile-n 500
```

Timed out after 5 minutes before printing results.

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9 --half-width 6 --window hard --window-radius 3 --profile-n 500
```

Timed out at 2 minutes and was later stopped.

A tiny `current_curl_model=full` run was also started but aborted before a
useful result was captured. Re-run it on the i7.

## Interim read

The direct-sector checks completed so far do **not** show a low branch near the
issue #72 reduced-basis candidates (`~0.11` to `~0.22`). The affordable direct
branch sits around `0.50` at the matched `hw=8`, `r_w=4`, `n=9` point, with or
without `L_perp`. That is only an interim diagnostic, not a final #73 verdict,
because the grid is deliberately coarse and `full` current-curl has not yet
been run.

The strongest current hypothesis is:

```text
The issue #72 low Kelvin branches are likely reduced-basis artifacts, or at
least not reproduced by the first direct m_phi=+/-1 sector discretization.
```

Do not close issue #73 from this note alone. The i7 pass should decide whether
this remains true after modest refinement.

## Recommended next-session runs on the i7

Start with the same exact commands to confirm reproducibility:

```bash
python -m py_compile src/paper_i/muon_issue73_phi_bdg_probe.py
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9 --half-width 8 --window hard --window-radius 4 --profile-n 500
```

Then run a practical refinement ladder:

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9,11,13 --half-width 8 --window hard --window-radius 4 --profile-n 500
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9,11 --half-width 8 --window hard --window-radius 3 --profile-n 500
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 9,11 --half-width 8 --window hard --window-radius 5 --profile-n 500
```

Then test the current-curl model sensitivity:

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 7,9 --half-width 8 --window hard --window-radius 4 --profile-n 500 --current-curl-model full
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 11 --half-width 8 --window hard --window-radius 4 --profile-n 500 --skip-lperp
```

If `n=13` is practical on the i7, try one higher point:

```bash
python src/paper_i/muon_issue73_phi_bdg_probe.py --n-values 15 --half-width 8 --window hard --window-radius 4 --profile-n 500
```

## Implementation cautions for the next session

- The current grid basis is intentionally minimal and cell-local. It is useful
  for a first direct-sector check, but it is not yet a high-order weak-form
  discretization.
- The `L_perp` assembly calls cell-local field functions through the audited
  current-curl routines. This is conceptually clean but slow, scaling badly as
  active cells increase.
- If the i7 runs are still too slow, the next code improvement should be
  caching cell-local derivative stencils or assembling `L_perp` directly as
  sparse local stencils instead of repeatedly calling function closures.
- If all direct-sector branches remain far above `0.207`, write the final
  issue #73 result note and recommend retiring the muon programme at the
  reduced-operator level.
- If a branch moves down toward `0.207`, do not claim success yet. Require
  window, grid, domain, and `linear/full` current-curl checks.

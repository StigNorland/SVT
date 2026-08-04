# Issue #225 — corrected cored-logarithmic versus pISO audit

## Status and evidential boundary

This is a **retrospective correction and reproducibility audit**, not a blind preregistration. The eleven-galaxy pilot, its term-ablation outcome, and the apparent importance of the published `k2` branch were viewed before this audit. Nothing here is held-out confirmation, and no H-SSV screen mechanism follows from a rotation-curve preference.

The pilot error is corrected: `cored_log` uses `H x^2/(x^2+Rc^2)`, while genuine `pISO` uses `H[1-(Rc/x) atan(x/Rc)]`. The LogSVT `k2` branch is exactly the former, not the latter.

## Fixed audit design

The audit refits the same eleven overlapping SPARC galaxies and the same fixed stellar mass-to-light scenarios: primary `(0.5, 0.7)`, light `(0.3, 0.5)`, and heavy `(0.7, 0.9)`. Candidates are all 32 hierarchical LogSVT reductions, the separately named cored-log and genuine-pISO laws, and NFW; baryons-only is one member of the 32-model lattice. Fits use weighted velocity residuals and 16 deterministic multistarts.

## Per-galaxy decisions under inherited bounds

### primary

| galaxy | best AICc model | models within ΔAICc ≤ 2 | ΔAICc pISO−cored | ΔBIC pISO−cored | k2 term necessary? | cored-log shape necessary? |
|---|---|---|---:|---:|---|---|
| `DDO154` | `k2_Q` | `k2_Q` | 12.08 | 12.08 | yes | yes |
| `NGC2403` | `C_k12_L` | `C_k2_L`, `C_k12_L` | -370.36 | -370.36 | yes | yes |
| `NGC2841` | `k2_L` | `k2_L` | 5.17 | 5.17 | yes | yes |
| `NGC2903` | `k2_L` | `k2_L` | 43.66 | 43.66 | yes | yes |
| `NGC2976` | `cored_log` | `k2`, `k2_L`, `cored_log`, `pISO` | 0.04 | 0.04 | no | no |
| `NGC3198` | `cored_log` | `k2`, `k12`, `k12_L`, `C_k2`, `cored_log` | 17.46 | 17.46 | no | yes |
| `NGC3521` | `C_L` | `C_L`, `C_k2` | -4.15 | -4.15 | no | no |
| `NGC5055` | `k2_L` | `k2_L` | 220.79 | 220.79 | yes | yes |
| `NGC6946` | `k2` | `k2`, `k2_L`, `cored_log` | 4.34 | 4.34 | no | yes |
| `NGC7331` | `k2_L` | `k2_L` | 1.55 | 1.55 | yes | yes |
| `NGC7793` | `k2_L_Q` | `k2_L_Q`, `k12_Q`, `k12_L` | -3.32 | -3.32 | yes | yes |

### light

| galaxy | best AICc model | models within ΔAICc ≤ 2 | ΔAICc pISO−cored | ΔBIC pISO−cored | k2 term necessary? | cored-log shape necessary? |
|---|---|---|---:|---:|---|---|
| `DDO154` | `k2_Q` | `k2`, `k2_Q`, `k2_L_Q`, `k12_Q`, `k12_L`, `C_k2_Q`, `cored_log` | 9.02 | 9.02 | no | yes |
| `NGC2403` | `C_k12` | `C_k12`, `C_k12_L` | -634.75 | -634.75 | yes | yes |
| `NGC2841` | `k2_L` | `k2_L` | 7.89 | 7.89 | yes | yes |
| `NGC2903` | `k2_Q` | `k2_Q`, `k2_L`, `k2_L_Q` | 36.10 | 36.10 | yes | yes |
| `NGC2976` | `cored_log` | `k2`, `k2_Q`, `cored_log`, `pISO` | 0.18 | 0.18 | no | no |
| `NGC3198` | `k2_L` | `k2_L` | 61.65 | 61.65 | yes | yes |
| `NGC3521` | `k2_L` | `k1_L`, `k2_L`, `k12` | -8.44 | -8.44 | no | no |
| `NGC5055` | `C_k2_L` | `C_k2_L` | 58.64 | 58.64 | yes | yes |
| `NGC6946` | `C_k2_L` | `C_k2_Q`, `C_k2_L` | 1.20 | 1.20 | yes | yes |
| `NGC7331` | `k2_L` | `k2_L` | -28.33 | -28.33 | yes | yes |
| `NGC7793` | `L_Q` | `L_Q`, `k2_L_Q`, `k12_Q`, `k12_L` | -9.93 | -9.93 | no | no |

### heavy

| galaxy | best AICc model | models within ΔAICc ≤ 2 | ΔAICc pISO−cored | ΔBIC pISO−cored | k2 term necessary? | cored-log shape necessary? |
|---|---|---|---:|---:|---|---|
| `DDO154` | `k2_Q` | `k2_Q` | 14.62 | 14.62 | yes | yes |
| `NGC2403` | `C_k2_L` | `C_k2_L` | -30.81 | -30.81 | yes | yes |
| `NGC2841` | `k2_L` | `k2_L` | -19.94 | -19.94 | yes | yes |
| `NGC2903` | `k2_L` | `k2_L` | 28.39 | 28.39 | yes | yes |
| `NGC2976` | `pISO` | `k2`, `k2_L`, `cored_log`, `pISO` | -0.00 | -0.00 | no | no |
| `NGC3198` | `k2` | `k2`, `C_k2`, `cored_log` | 19.22 | 19.22 | no | yes |
| `NGC3521` | `k2_L` | `k2_L` | 0.00 | 0.00 | yes | yes |
| `NGC5055` | `k2_L` | `k2_L` | 12.15 | 12.15 | yes | yes |
| `NGC6946` | `k2_L` | `k2_L`, `k12_L` | 0.38 | 0.38 | yes | yes |
| `NGC7331` | `k2_L` | `k2_L` | 0.00 | 0.00 | yes | yes |
| `NGC7793` | `k2_Q` | `k2_Q`, `k2_L_Q`, `k12_Q`, `C_k2_Q` | 1.52 | 1.52 | yes | yes |

## Aggregate correction result

- `primary`: AICc winners `k2_Q`=1, `C_k12_L`=1, `k2_L`=4, `cored_log`=2, `C_L`=1, `k2`=1, `k2_L_Q`=1; genuine pISO and cored-log are pairwise indistinguishable in 2/11; the `k2` term is confidence-set necessary in 7/11 and the broader cored-log shape class in 9/11.
- `light`: AICc winners `k2_Q`=2, `C_k12`=1, `k2_L`=4, `cored_log`=1, `C_k2_L`=2, `L_Q`=1; genuine pISO and cored-log are pairwise indistinguishable in 2/11; the `k2` term is confidence-set necessary in 7/11 and the broader cored-log shape class in 8/11.
- `heavy`: AICc winners `k2_Q`=2, `C_k2_L`=1, `k2_L`=6, `pISO`=1, `k2`=1; genuine pISO and cored-log are pairwise indistinguishable in 5/11; the `k2` term is confidence-set necessary in 9/11 and the broader cored-log shape class in 10/11.

Under primary baryons, the corrected global candidate set therefore supports a necessary cored-log shape in 9/11 galaxies, rather than the pilot's unqualified 10/11 `k2` statement. The `NGC2976` confidence set contains genuine pISO and is phenomenologically degenerate; `NGC3521` does not require the cored-log shape.

The two ‘necessary’ columns answer different questions. `k2 term necessary` requires every global ΔAICc≤2 model to be a LogSVT reduction containing `u2`. `cored-log shape necessary` also accepts the explicitly named, algebraically equivalent cored-log comparator. Neither identifies a screen source.

## Covariance, boundaries, and bound sensitivity

- `primary`: 191/374 fitted models are practically rank deficient at relative singular-value threshold `1e-8`, 283/374 have max |correlation| ≥ 0.95, and 203/374 touch an inherited bound. Expanded bounds change 1/11 winner labels but 0/11 winner shapes, 0/11 confidence sets, and 0/11 `k2`-necessity decisions. Optimizer failures after continuation: 0.
- `light`: 169/374 fitted models are practically rank deficient at relative singular-value threshold `1e-8`, 255/374 have max |correlation| ≥ 0.95, and 155/374 touch an inherited bound. Expanded bounds change 1/11 winner labels but 0/11 winner shapes, 0/11 confidence sets, and 0/11 `k2`-necessity decisions. Optimizer failures after continuation: 0.
- `heavy`: 190/374 fitted models are practically rank deficient at relative singular-value threshold `1e-8`, 301/374 have max |correlation| ≥ 0.95, and 230/374 touch an inherited bound. Expanded bounds change 1/11 winner labels but 0/11 winner shapes, 0/11 confidence sets, and 0/11 `k2`-necessity decisions. Optimizer failures after continuation: 0.

Full transformed-parameter covariance and correlation matrices, singular values, boundary flags, optimizer status, parameters, AICc, and BIC are retained in `receipt.json`. `model-selection.csv` contains every primary and expanded-bound fit; `comparison.csv` contains all requested pISO/cored-log/LogSVT pairwise deltas; `bound-sensitivity.csv` exposes every sensitivity decision.

## Interpretation boundary

If genuine pISO is within ΔAICc≤2 of cored-log, the result is phenomenological degeneracy. If cored-log wins, that is still only a compact radial description. The audit neither derives its amplitude or core radius nor promotes a universal screen claim. Negative or unstable selections are retained as the result.

## Recovered pilot provenance

The corrected instrument has no `/tmp` dependency. SHA-256 identifiers for the reviewed pilot scripts, tables, notes, and receipts are stored in the machine receipt so the mistaken inputs can be reconstructed without moving them into the durable result set.

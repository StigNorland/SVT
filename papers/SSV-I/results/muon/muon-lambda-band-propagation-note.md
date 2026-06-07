# Muon Lambda-Band Propagation Note (2026-05-20)

> **Status (2026-05-30): superseded by Path B null.** Numerical claims in this note about the muon eigenfrequency reaching $\omega/\omega_c = 0.207$, the $\delta_{\rm relax}$ calibration, the $\alpha$-harmonic ladder identification, or the $1/\sqrt{N_{\rm modes}}$ basis-truncation residual are now governed by `papers/SSV-I/path-b-eigenvalue-result.md`: that test showed the muon agreement is not basis-robust (drifts $\pm 13\%$ across 4 bases, empty window in 2 of 4) and the pion rung is absent in every basis. Structural sub-results that stand on their own (operator algebra, analytic derivations, the cubic-vertex one-loop result, dimensional setup) remain valid in isolation; what is superseded is their use as evidence for the ladder identification or as a closure path to it. Quarantined inputs: `instruments/_fitted_quarantine/`. Tracking: issue #66.

Script: `instruments/paper_i/muon_lambda_band_sweep.py`

Question: after the relaxed-background bridge correction,

```math
\lambda_\perp^{\rm code}
  = {\pi\over4}\,(1+\delta_{\rm relax}),
\qquad
\delta_{\rm relax}=+0.038\pm0.005,
```

does the reduced Kelvin-augmented BdG branch land near the target
`\omega_\mu/\omega_c = 0.207`?

## Check Run

The first propagation used the existing Kelvin branch tracker at
`n=31`, `half_width=5`, `profile_n=1200`, `kelvin_phi_n=512`,
and `kelvin_core_radius=1.0`.

Equivalent command:

```powershell
python instruments/paper_i/muon_lambda_band_sweep.py `
  --points "31,5,1200" `
  --deltas "0.0,0.033,0.038,0.043" `
  --kelvin-phi-n 512
```

## Result

| delta_relax | lambda_perp | selected omega | abs error vs 0.207 | rel error |
|-------------|-------------|----------------|--------------------|-----------|
| `0.000` | `0.785398163` | `0.198145299` | `0.008854701` | `4.278%` |
| `0.033` | `0.811316303` | `0.202730772` | `0.004269228` | `2.062%` |
| `0.038` | `0.815243294` | `0.203418905` | `0.003581095` | `1.730%` |
| `0.043` | `0.819170284` | `0.204105317` | `0.002894683` | `1.398%` |

The selected branch remains smooth across the band and has about
`4%` core weight and `96%` Kelvin weight, so this is still a Kelvin-dominated
hybrid branch rather than a clean core-mode prediction.

## Interpretation

The relaxed correction moves the reduced branch in the right direction and
cuts the target miss from about `4.3%` to `1.4%--2.1%`. It does not, by itself,
hit the draft target within the current `+0.038 +/- 0.005` relaxed band.

A local linear extrapolation from the four points gives:

```math
\delta_{\rm relax}^{\rm target} \approx +0.064,
\qquad
\lambda_\perp^{\rm target} \approx 0.836.
```

This is outside the present relaxed-background band, but close enough that the
remaining missing physics could plausibly matter: full second variation,
larger basis, half-width extrapolation, Kelvin core-radius calibration, or
the circumferential grid.

## Next Decision

The bridge result is robust, but the muon frequency is not yet a closed
prediction. The next useful fork is:

1. Run the lambda-band sweep across `n={25,31,37}` and `half_width={5,6}` to
   check whether the `1.4%--2.1%` miss is stable or a grid/box artifact.
2. Sweep `kelvin_core_radius` because the selected branch is Kelvin-dominated.
3. If those axes do not close the remaining error, the full second variation
   becomes mandatory before claiming a paper-level number.

## Follow-up: Grid/Core-Radius Probe

The broad grid/core-radius sweep was too expensive for a single PC turn, so the
probe was decomposed into smaller runs:

```powershell
python instruments/paper_i/muon_lambda_band_sweep.py `
  --points "21,4,800" `
  --deltas "0.038" `
  --kelvin-core-radius 1.0 `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-lambda-band-n21-corrected-2026-05-20.json

python instruments/paper_i/muon_lambda_band_sweep.py `
  --points "13,4,400" `
  --deltas "0.038" `
  --kelvin-core-radii "0.75,1.0,1.25" `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-lambda-band-n13-core-radius-2026-05-20.json

python instruments/paper_i/muon_lambda_band_sweep.py `
  --points "21,4,800" `
  --deltas "0.038" `
  --kelvin-core-radii "0.75,1.25" `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-lambda-band-n21-core-radius-edges-2026-05-20.json
```

| point | kelvin core radius | selected omega | rel error |
|-------|--------------------|----------------|-----------|
| `n=13`, `hw=4`, `profile_n=400` | `0.75` | `0.208710113` | `0.826%` |
| `n=13`, `hw=4`, `profile_n=400` | `1.00` | `0.208083284` | `0.523%` |
| `n=13`, `hw=4`, `profile_n=400` | `1.25` | `0.207678214` | `0.328%` |
| `n=21`, `hw=4`, `profile_n=800` | `0.75` | `0.195991839` | `5.318%` |
| `n=21`, `hw=4`, `profile_n=800` | `1.00` | `0.195416559` | `5.596%` |
| `n=21`, `hw=4`, `profile_n=800` | `1.25` | `0.195044894` | `5.775%` |

This is a sharp warning: the near-target coarse `n=13` result is not
converging toward the `n=21` and `n=31` behaviour. Kelvin-core-radius changes
shift the branch by only `O(10^{-3})`; they cannot explain the grid jump.

The next paper-safe statement is therefore not "the target is hit", but:

```text
The relaxed pi/4 bridge correction is stable. The reduced Kelvin-augmented
frequency prediction is not yet grid-stable, and the current selected branch is
Kelvin dominated. A full second-variation or larger/stabilized reduced basis is
needed before quoting the muon frequency.
```

## Follow-up: Coarse-Grid Artifact Identified

The next diagnostic recorded all hybrid branches instead of only the
nearest-to-target selected branch.

```powershell
python instruments/paper_i/muon_lambda_band_sweep.py `
  --points "13,4,400;17,4,600;21,4,800;25,4,1000;31,4,1200" `
  --deltas "0.0,0.038" `
  --kelvin-core-radius 1.0 `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-lambda-band-grid-ladder-hw4-2026-05-20.json

python instruments/paper_i/muon_lambda_band_sweep.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --deltas "0.038" `
  --kelvin-core-radius 1.0 `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-lambda-band-grid-ladder-hw5-corrected-2026-05-20.json
```

At the corrected central value `delta_relax=0.038`, the `half_width=4` ladder
gives:

| n | lower hybrid | upper hybrid | nearest-to-target branch |
|--:|-------------:|-------------:|--------------------------|
| 13 | `0.142635338` | `0.208083284` | upper |
| 17 | `0.174072827` | `0.275499900` | lower |
| 21 | `0.195416559` | `0.326200380` | lower |
| 25 | `0.210496305` | `0.351323941` | lower |
| 31 | `0.224313446` | `0.380246849` | lower |

At `half_width=5`, the same corrected coefficient gives:

| n | lower hybrid | upper hybrid | nearest-to-target branch |
|--:|-------------:|-------------:|--------------------------|
| 21 | `0.170431186` | `0.226605611` | upper |
| 25 | `0.187779884` | `0.258503939` | lower |
| 31 | `0.204101556` | `0.293951890` | lower |

This identifies the artifact. The "selected" branch was chosen by proximity to
the target `0.207`, not by physical branch identity. On coarse grids the upper
hybrid branch can sit near the target, while on finer grids the nearest branch
can switch to the lower hybrid. That makes the earlier near-hit a branch
selection artifact, not converged muon evidence.

The useful reduced-basis lesson is sharper now:

```text
Do not quote the nearest-to-target hybrid as the muon prediction. Track lower
and upper hybrid branches separately by identity, preferably using eigenvector
overlap/Krein signature across grid refinements, then decide whether either
branch converges near the physical target.
```

Current branch-identity evidence is not yet paper-safe. The lower branch drifts
strongly with `n` and `half_width`; the upper branch also drifts upward. The
stable result remains the corrected thin-ring bridge coefficient, not the final
muon frequency.

## Branch Tracking by Eigenvector/Krein Continuation

The target-proximity rule was replaced by explicit branch continuation. The new
diagnostic computes the Kelvin-augmented BdG eigenvectors, assigns the first
grid's hybrids by frequency order, and then matches each subsequent grid by
coefficient-vector overlap with a Krein-overlap/sign guard.

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "13,4,400;17,4,600;21,4,800;25,4,1000;31,4,1200" `
  --delta-relax 0.038 `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-branch-identity-hw4-2026-05-20.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-branch-identity-hw5-2026-05-20.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,6,800;25,6,1000;31,6,1200" `
  --delta-relax 0.038 `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-branch-identity-hw6-2026-05-20.json
```

The continuation is numerically unambiguous: adjacent-grid match scores are
`0.989--0.999`, Euclidean overlaps are `0.987--0.999`, and all tracked hybrids
keep positive Krein sign.

At the corrected central coefficient, the branch identities are:

| half_width | n | lower identity branch | upper identity branch |
|------------|--:|----------------------:|----------------------:|
| 4 | 13 | `0.142635` | `0.208083` |
| 4 | 17 | `0.174073` | `0.275500` |
| 4 | 21 | `0.195417` | `0.326200` |
| 4 | 25 | `0.210496` | `0.351324` |
| 4 | 31 | `0.224313` | `0.380247` |
| 5 | 21 | `0.170431` | `0.226606` |
| 5 | 25 | `0.187780` | `0.258504` |
| 5 | 31 | `0.204102` | `0.293952` |
| 6 | 21 | `0.146648` | `0.168990` |
| 6 | 25 | `0.166168` | `0.196942` |
| 6 | 31 | `0.186147` | `0.231893` |

This settles the coarse-grid artifact. The `n=13`, `half_width=4` near-hit is
the upper identity branch. That same identity branch moves rapidly upward with
grid refinement at `half_width=4`; it is not converging to the target. The
lower identity branch crosses near the target around `n=25`, but continues
upward by `n=31`. Larger boxes push both branches downward.

Paper-safe conclusion:

```text
The branch-continuation diagnostic removes the target-selection ambiguity, but
it does not produce a converged muon eigenfrequency. The reduced basis is still
too box/grid sensitive. The corrected pi/4 bridge remains robust; the frequency
claim needs a stabilized basis or the full second variation/circumferential
grid before it can be quoted.
```

## Basis-Enrichment Check

The next test was whether the target-adjacent branch is stable under reduced
basis enrichment. The branch identity tracker was extended with:

- `--core-basis two|four`
- `--kelvin-seed helicity|displacement|breathing`

All runs below use the corrected central coefficient `delta_relax=0.038`,
`half_width=5`, `kelvin_phi_n=128`, and points
`n={21,25,31}` with `profile_n={800,1000,1200}`.

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --core-basis two `
  --kelvin-seed helicity `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-identity-basis-two-helicity-hw5-2026-05-20.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed helicity `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-identity-basis-four-helicity-hw5-2026-05-20.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --core-basis two `
  --kelvin-seed displacement `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-identity-basis-two-displacement-hw5-2026-05-20.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --core-basis two `
  --kelvin-seed breathing `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-identity-basis-two-breathing-hw5-2026-05-20.json
```

The `n=31`, `half_width=5` outcomes are:

| basis | tracked branch values at `n=31` | nearest miss vs `0.207` |
|-------|---------------------------------|-------------------------|
| two-core, helicity Kelvin | `0.205511`, `0.295392` | `0.72%` low |
| four-core, helicity Kelvin | `0.196543`, `0.305117` | `5.05%` low |
| two-core, displacement Kelvin | `0.341269` | `64.9%` high |
| two-core, breathing Kelvin | `0.218028` | `5.33%` high |

The overlap/Krein continuation is still numerically clean in every case
(`~0.998--1.000` adjacent-grid scores for the helicity/core-enriched runs and
`~0.994--0.999` for the alternate Kelvin seeds). The problem is not branch
matching. The problem is that the predicted frequency changes materially when
the reduced basis is changed.

This is the strongest evidence so far that the current reduced Kelvin BdG
frequency extractor is basis-truncated. The two-core/helicity setup happens to
place a tracked branch near the target at `n=31`, but adding the conjugate core
partners moves that branch down by almost `0.009`, and changing the Kelvin seed
family changes the window structure entirely.

Updated conclusion:

```text
The muon-frequency calculation should not be pushed further by tuning
lambda_perp, Kelvin core radius, or target-nearest selection. The reduced basis
itself is not stable. The next meaningful physics calculation is the full
second variation of the current-curl term in an enriched basis, or else the full
circumferential BdG grid.
```

## Full Second-Variation Check

The previous current-curl BdG block kept the `|curl j_1|^2` piece of

```math
E_\perp = {\lambda\over2}\int |\nabla\times j|^2\,d^3x.
```

The `current_curl_model=full` option adds the missing background-vorticity term
from the quadratic expansion,

```math
\int(\nabla\times j_0)\cdot(\nabla\times j_2)\,d^3x,
```

with angular selection rules for the normal and anomalous Nambu blocks.

Commands:

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --core-basis two `
  --kelvin-seed helicity `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-two-helicity-hw5-2026-05-20.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed helicity `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-helicity-hw5-2026-05-20.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --core-basis two `
  --kelvin-seed displacement `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-two-displacement-hw5-2026-05-20.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --core-basis two `
  --kelvin-seed breathing `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-two-breathing-hw5-2026-05-20.json
```

At `n=31`, `half_width=5`, the full second-variation model gives:

| basis | tracked branch values at `n=31` | nearest miss vs `0.207` |
|-------|---------------------------------|-------------------------|
| two-core, helicity Kelvin | `0.216509`, `0.237616` | `4.59%` high |
| four-core, helicity Kelvin | `0.204752`, `0.237616` | `1.09%` low |
| two-core, displacement Kelvin | `0.104888`, `0.129835`, `0.343945` | `37.3%` low |
| two-core, breathing Kelvin | `0.280803` | `35.7%` high |

The full background-vorticity term is therefore important. It removes the
earlier four-core/helicity downward shift and puts the enriched helicity lower
branch close to the target again. But the result is still not seed-independent:
displacement and breathing Kelvin seeds give different window structures.

Interpretation:

```text
Full second variation makes the enriched helicity reduced basis promising
again, but not closure-grade. The next reduced-basis task is to combine Kelvin
seed families in one basis, instead of choosing helicity/displacement/breathing
as mutually exclusive ansatz spaces. If the combined Kelvin basis stabilizes
the lower branch near 0.207 across n and half_width, the reduced calculation is
back in play. If not, go to the full circumferential grid.
```

## Combined Kelvin Basis Check

The `combined` Kelvin basis includes breathing, radial displacement, vertical
displacement, and helicity candidates, then orthogonalizes each azimuthal sector
so the helicity candidates do not duplicate the radial/vertical span. This tests
whether the previous seed dependence was just an incomplete ansatz space.

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,5,800;25,5,1000;31,5,1200" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-combined-hw5-2026-05-21.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "21,6,800;25,6,1000;31,6,1200" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-combined-hw6-2026-05-21.json
```

At `half_width=5`, the combined full/four-core lower branch is promising:

| n | lower identity branch | pure-Kelvin identity branch | nearest miss |
|--:|----------------------:|----------------------------:|-------------:|
| 21 | `0.167837` | `0.199404` | `3.67%` low |
| 25 | `0.185857` | `0.217172` | `4.91%` high |
| 31 | `0.205374` | `0.237633` | `0.79%` low |

The branch continuation remains clean (`0.993--1.000` match scores), and the
target-adjacent branch at `n=31` is no longer an isolated helicity-only result.

However, the same combined full/four-core basis at `half_width=6` gives:

| n | lower identity branch | pure-Kelvin identity branch | nearest miss |
|--:|----------------------:|----------------------------:|-------------:|
| 21 | `0.146962` | `0.153506` | `25.8%` low |
| 25 | `0.165525` | `0.170397` | `17.7%` low |
| 31 | `0.186942` | `0.191445` | `7.51%` low |

So the combined basis improves seed stability but does not remove the dominant
box-size sensitivity. The reduced calculation is therefore not falsified, but
it is still not closure-grade.

Current best reading:

```text
Full second variation plus a combined Kelvin basis gives a coherent branch near
the muon target on hw=5 grids. The same branch remains significantly below
target at hw=6. The next reduced check is not more seed tuning; it is a
box-size/extrapolation campaign at larger n, or a boundary-condition audit. If
the hw=5/hw=6 split persists, the full circumferential grid is required.
```

## Matched-Spacing Box Audit

The earlier `half_width=5` versus `half_width=6` comparison changed both box
size and grid spacing, because the projection grid has

```math
dr = dz = {2\,{\rm half\_width}\over n}.
```

Thus `hw=5,n=31` has `dr=0.323`, while `hw=6,n=31` has the coarser
`dr=0.387`. The next audit matched spacing by running `hw=6,n=37`
(`dr=0.324`) and also checked a higher-resolution `hw=5,n=37` point.

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "25,6,1000;31,6,1200;37,6,1400" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-combined-hw6-n37-2026-05-21.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "25,5,1000;31,5,1200;37,5,1400" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-combined-hw5-n37-2026-05-21.json
```

Results:

| box/grid | `dr` | mixed lower branch | pure-Kelvin branch | nearest miss |
|----------|-----:|-------------------:|-------------------:|-------------:|
| `hw=5,n=31` | `0.323` | `0.205374` | `0.237633` | `0.79%` low |
| `hw=6,n=31` | `0.387` | `0.186942` | `0.191445` | `7.51%` low |
| `hw=6,n=37` | `0.324` | `0.202869` | `0.205317` | `0.81%` low |
| `hw=5,n=37` | `0.270` | `0.220134` | `0.247399` | `6.34%` high |

This sharpens the diagnosis. Much of the old `hw=6` deficit was actually a
coarser-grid effect. When `hw=6` is rerun at matched spacing, a coherent branch
returns near the target. But the higher-resolution `hw=5,n=37` point overshoots,
so the branch is not yet converged in `dr` or box size.

Current best reduced-basis status:

```text
The combined/full/four-core reduced model is viable enough to keep auditing.
The target-adjacent branch is not a seed artifact and not simply killed by a
larger box once spacing is matched. However, the branch still has significant
dr/box drift. The next decisive reduced audit is a constant-dr sequence across
half_width = 5, 6, 7, followed by a fixed-box refinement sequence. If those do
not settle, move to the full circumferential grid.
```

## Unattended Low-Hanging Audit

The unattended pass exhausted the cheap reduced-BdG checks that fit under the
four-hour-per-calculation limit.

### Constant-spacing box sequence

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,5,1200;37,6,1400;43,7,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-combined-constant-dr-2026-05-21.json
```

| point | `dr` | branch values | continuation status |
|-------|-----:|---------------|---------------------|
| `hw=5,n=31` | `0.323` | `0.205374`, `0.237633` | start |
| `hw=6,n=37` | `0.324` | `0.202869`, `0.205317` | clean match |
| `hw=7,n=43` | `0.326` | `0.238321`, `0.176028` | poor match / Krein flip |

The `hw=5 -> hw=6` comparison is healthy when spacing is matched, but the
`hw=7` extension breaks the identity continuation. This is a boundary/box red
flag, not a mere target-selection issue.

### Fixed-box refinement

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,5,1200;37,5,1400;43,5,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-combined-hw5-refinement-2026-05-21.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,6,1200;37,6,1400;43,6,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-combined-hw6-refinement-2026-05-21.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "37,7,1400;43,7,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-combined-hw7-refinement-2026-05-21.json
```

| fixed box | tracked values | conclusion |
|-----------|----------------|------------|
| `hw=5` | `0.205374 -> 0.220134 -> 0.231630` | monotone upward drift |
| `hw=6` | `0.186942 -> 0.202869 -> 0.215235` | monotone upward drift |
| `hw=7` | `0.174852/0.186757 -> 0.238321/0.176028` | identity instability |

The target-adjacent points at `hw=5,n=31` and `hw=6,n=37` are crossings, not
convergence plateaus. Refining the fixed box pushes the mixed lower branch
upward.

### Kelvin self-induction quadrature

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,5,1200;37,6,1400" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-branch-full-second-variation-four-combined-phi256-check-2026-05-21.json
```

Increasing `kelvin_phi_n` from `128` to `256` shifts the target-adjacent
branches downward by only about `0.0013`; it does not explain the box/refinement
drift.

## Reduced-Basis Verdict

The low-hanging reduced-BdG options are now effectively exhausted:

1. `lambda_perp` is no longer the live issue; the relaxed bridge correction is
   stable.
2. Target-nearest selection was fixed by branch continuation.
3. Kelvin seed dependence was reduced by the combined basis.
4. Full second variation is included.
5. Self-induction quadrature is not the dominant error.
6. The remaining failure mode is box/refinement sensitivity of the reduced
   ansatz itself.

The reduced model remains useful as a diagnostic, but it is not closure-grade
for the muon eigenfrequency. The next calculation with real authority is the
full circumferential BdG grid, or a deliberate boundary-condition redesign of
the reduced projection model.

## Windowed Projection Redesign

The first boundary redesign decouples the physical projection tube from the
numerical square box. The reduced projection metric now supports:

```powershell
--projection-window smooth --window-radius R --window-taper T
```

with full weight for `s <= R`, a cosine taper over `R < s < R+T`, and zero
outside. This weight is used consistently in the reduced BdG projection,
Gram-Schmidt/normalization, current-curl blocks, and full second-variation
background-vorticity blocks. New tracker runs also report Gram minimum
eigenvalue and condition number for the reduced basis.

### Smooth window, fixed physical support

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,5,1200;37,6,1400;43,7,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --projection-window smooth `
  --window-radius 4.0 `
  --window-taper 1.0 `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-window-smooth-r4-t1-constant-dr-2026-05-21.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,5,1200;37,6,1400;43,7,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --projection-window smooth `
  --window-radius 3.5 `
  --window-taper 1.0 `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-window-smooth-r3p5-t1-constant-dr-2026-05-21.json
```

| window | `hw=5,n=31` | `hw=6,n=37` | `hw=7,n=43` |
|--------|------------:|------------:|------------:|
| `R=4,T=1` | `0.207768` | `0.207505` | identity instability; new `0.194252` negative-Krein branch |
| `R=3.5,T=1` | `0.210151` | `0.209879` | identity instability; new `0.199098` negative-Krein branch |

This is the best evidence that the old `hw=5 -> hw=6` split was largely a
boundary/projection artifact: with fixed smooth support, those two boxes agree
to about `3e-4`. But extending to `hw=7` still destabilizes the reduced branch
identity and introduces a negative-Krein near-window branch.

### Smooth-window fixed-box refinement

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,5,1200;37,5,1400;43,5,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --projection-window smooth `
  --window-radius 4.0 `
  --window-taper 1.0 `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-window-smooth-r4-t1-hw5-refinement-2026-05-21.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,6,1200;37,6,1400;43,6,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --projection-window smooth `
  --window-radius 4.0 `
  --window-taper 1.0 `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-window-smooth-r4-t1-hw6-refinement-2026-05-21.json
```

| fixed box | smooth-window tracked branch | conclusion |
|-----------|------------------------------|------------|
| `hw=5` | `0.207768 -> 0.222995 -> 0.234855` | monotone upward drift |
| `hw=6` | `0.190886 -> 0.207505 -> 0.220576` | monotone upward drift |

The smooth window fixes much of the box mismatch at matched spacing, but it does
not remove fixed-box refinement drift. The target-adjacent values are still
crossings, not plateaus.

## Boundary-Redesign Verdict

The smooth projection window is a useful improvement and should stay in the
tooling. It proves that the previous `hw=5/hw=6` split was partly artificial.
But the reduced boundary/projection redesign does not close the muon frequency:

1. `hw=5` and `hw=6` agree when the same physical window and spacing are used.
2. Fixed-box refinement still drifts upward.
3. `hw=7` introduces branch-identity/Krein instability even with a compact
   physical projection window.
4. The remaining issue is not a low-hanging parameter choice in the current
   reduced ansatz.

The reduced model is now a strong diagnostic for the bridge, but not a final
muon eigenfrequency calculation. The next meaningful step is either a more
fundamental boundary-condition redesign with an explicitly self-adjoint
truncated operator, or the full circumferential BdG grid.

## Self-Adjoint Weak-Form Boundary Operator

The self-adjoint reduced-boundary prototype replaces the strong-form projected
Laplacian in the normal BdG block by the weak energy bilinear form:

```math
\langle a,Lb\rangle_W
= \int W\,2\pi r\left[
{1\over2}\left(\partial_r a^*\partial_r b
+\partial_z a^*\partial_z b
+{m^2\over r^2}a^*b\right)
+V a^*b\right]\,dr\,dz .
```

This removes artificial boundary-flux dependence from applying a strong
Laplacian inside a truncated projection region. The CLI switch is:

```powershell
--reduced-operator-form weak
```

### Weak-form matched-spacing and refinement audit

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,5,1200;37,6,1400;43,7,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --reduced-operator-form weak `
  --projection-window smooth `
  --window-radius 4.0 `
  --window-taper 1.0 `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-weak-window-r4-t1-constant-dr-2026-05-22.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,5,1200;37,5,1400;43,5,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --reduced-operator-form weak `
  --projection-window smooth `
  --window-radius 4.0 `
  --window-taper 1.0 `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-weak-window-r4-t1-hw5-refinement-2026-05-22.json

python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "31,6,1200;37,6,1400;43,6,1600" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --reduced-operator-form weak `
  --projection-window smooth `
  --window-radius 4.0 `
  --window-taper 1.0 `
  --kelvin-phi-n 128 `
  --output papers/SSV-I/data/muon-weak-window-r4-t1-hw6-refinement-2026-05-22.json
```

The weak form changes the picture substantially. The branch is now monotone
from below instead of overshooting:

| audit | tracked lower branch |
|-------|----------------------|
| `hw=5`: `n=31 -> 37 -> 43 -> 49` | `0.182721 -> 0.192618 -> 0.200600 -> 0.206278` |
| `hw=6`: `n=31 -> 37 -> 43 -> 49 -> 59` | `0.172514 -> 0.182634 -> 0.191067 -> 0.197056 -> 0.207313` |
| matched spacing: `hw=5,n=49`; `hw=6,n=59`; `hw=7,n=69` | `0.206278`, `0.207313`, `0.207762` |

The Gram diagnostics are benign throughout the high-resolution weak-form runs:
minimum Gram eigenvalues are about `0.51` and condition numbers are about `3.9`.
The branch continuation scores remain `>0.999` on the tracked lower branch.

### Kelvin quadrature check

```powershell
python instruments/paper_i/muon_branch_identity_tracking.py `
  --points "59,6,2000" `
  --delta-relax 0.038 `
  --core-basis four `
  --kelvin-seed combined `
  --current-curl-model full `
  --reduced-operator-form weak `
  --projection-window smooth `
  --window-radius 4.0 `
  --window-taper 1.0 `
  --kelvin-phi-n 256 `
  --output papers/SSV-I/data/muon-weak-window-r4-t1-hw6-n59-phi256-2026-05-22.json
```

Increasing `kelvin_phi_n` from `128` to `256` at the representative
`hw=6,n=59` point shifts the lower branch from `0.207313` to `0.206035`. The
branch remains within `0.47%` of target, so quadrature is now an uncertainty,
not a failure mode.

## Updated Reduced-Basis Verdict

The self-adjoint weak-form boundary redesign succeeds as a reduced model
prototype. It removes the strong-form overshoot, tames the fixed-box refinement
trend, restores matched-box agreement across `hw=5,6,7`, and keeps the Gram
matrix well-conditioned.

This is not yet a publication-grade final muon number, but the reduced route is
back in play. The next meaningful checks are now refinement/uncertainty
quantification, not a wholesale jump to the full circumferential grid:

1. `kelvin_phi_n` convergence at one or two high-resolution points.
2. One more matched-spacing refinement level if affordable.
3. Propagate the `delta_relax = 0.038 +/- 0.005` band through the weak-form
   high-resolution points.

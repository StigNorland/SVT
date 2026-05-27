# Paper I Numerical Prototype Summary

The Paper I codebase tests the foundational SSV particle picture:

- stable vortex-core profiles in the logarithmic Schrodinger equation,
- a toroidal electron background with major radius `R_e = xi / alpha`,
- reduced collective-coordinate routes toward the muon mode,
- chiral/Kelvin coupling diagnostics that motivate the transverse sector.
- source-vs-topology closure questions for the static proton branch.

Recent source-driven static-branch work has added a topology-facing diagnostic layer. The current repo state now says something sharper than before: the present constrained static branch can stabilize gravity-facing source observables while still losing the local branch winding that the Paper I proton text appears to require, and the unconstrained comparison branch loses that winding too. See [topological-closure-memo.md](../../papers/SSV-I/topological-closure-memo.md), [topology-winding-check-note.md](../../papers/SSV-I/topology-winding-check-note.md), and [q-p-constraint-sensitivity-note.md](../../papers/SSV-I/q-p-constraint-sensitivity-note.md).

The first topology-guard pilot now exists too. It shows that a hard winding-aware acceptance rule can keep the branch from falling below the chosen local winding floor, but the current relaxer then stalls early and leaves a larger residual and source-heavy state. A follow-up pressure scan also shows an intermediate soft-pressure regime that bends branch selection without fully reproducing the hard stop. See [topology-guard-probe-note.md](../../papers/SSV-I/topology-guard-probe-note.md).

The medium-pressure branch has now been carried into the source diagnostics too. It is not yet a resolved proton branch, but it does change the source distribution in a promising direction: compared with the baseline branch from the same fresh initial state, it shifts weight from halo into the mid region and slightly reduces the outer-interior share of the total `Q_p`. See [topology-pressure-source-note.md](../../papers/SSV-I/topology-pressure-source-note.md).

The later flow-based follow-up is now more specific too. Broad topology-flow, phase-aware flow, loop-circulation flow, and even a direct winding-error flow built from phase-increment mismatch are all smoother numerically than the hard guard or pressure branch. But in the tested `hw = 7` pilot they still leave `topology_alignment_score ~ 0.25`, so they are not yet preserving or restoring the seeded local winding. See [topology-guard-probe-note.md](../../papers/SSV-I/topology-guard-probe-note.md).

## Main Takeaways

1. The planar LogSE vortex profile is numerically well-defined and reusable as the local core profile for a toroidal defect.
2. A leading toroidal ansatz `Psi_0 = f_0(s/xi) exp(i vartheta)` gives a concrete background for projection integrals.
3. The planar amplitude channel alone does not produce the muon as a simple bound breathing mode; toroidal geometry and chiral transverse coupling are required.
4. The reduced BdG and Kelvin/chiral scripts are exploratory tools for identifying which finite-dimensional truncations carry the right mode structure.

## Validation Status of Reduced-Problem Scripts (issue #16)

The reduced-problem scripts in `src/paper_i/` are not all of the same
maturity. The table below classifies each one so the paper text and
discussion can cite them at the correct confidence level. **Prototype**
scripts are exploratory checkpoints; the numbers they print are not
predictions. **Validation** scripts are robust building blocks whose
output the paper depends on but does not directly cite as a result.
**Derived** scripts produce the actual paper numbers.

| script | status | sensitivity verdict | notes |
|---|---|---|---|
| `vortex_profile.py` | validation | profile_n>=600 stable; **shooting fails at x_max>=25** | see `validation-refinement-sweeps-2026-05-27.md` |
| `restricted_bdg_matrix.py` | **prototype** | `omega_plus` drifts ~63% in `n`, ~66% in `hw`; `omega_minus` is `nan` at every reference point | see `validation-refinement-sweeps-2026-05-27.md` |
| `curved_torus_relaxation.py` | validation | small-basis ansatz only — pre-existing module header notes this | small-basis validation asset for issue #12 |
| `kelvin_augmented_bdg.py` / `muon_branch_identity_tracking.py` | derived | matched-spacing-trio addresses hw, weak-form + lru_cache fixes in `4b869bd`; outstanding cross-m current-curl issue identified in `enrichment-attempt-findings-2026-05-27.md` | source of the muon-mass predictions actually used in Paper I |

**Headline finding from the static-branch sweep:** the restricted 2-mode
diagnostic in `restricted_bdg_matrix.py` is NOT converged in grid `n` or
box `half_width` — neither axis shows a plateau within the swept range,
and the lower BdG branch is outside the 2-mode subspace (`omega_minus` is
`nan` at every sampled point). Any historical citation of
`restricted_bdg_matrix` numbers as derived predictions must be re-framed
as diagnostic checkpoints for the projected-Hessian formulation.

## Reproduction Commands

From the repository root:

```bash
python src/paper_i/vortex_profile.py --n 400 --x-max 12
python src/paper_i/muon_mode_prototype.py
python src/paper_i/kelvin_self_induction.py --phi-n 64
```

For heavier projection checks, use the lower grid sizes first:

```bash
python src/paper_i/restricted_bdg_matrix.py --n 21 --profile numerical --profile-n 400
python src/paper_i/chiral_bridge_projection.py --n 11 --profile-n 400
```

## Interpretation

These results should be cited in Paper I as evidence that the mathematical program is computationally well-posed. They should not be overclaimed as final high-precision predictions for the muon mass.

## Smoke Results

Curated smoke-test output is stored in:

```text
papers/SSV-I/data/smoke-results.csv
```

The first saved static-trefoil refinement checkpoint is recorded in:

```text
papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06.json
papers/SSV-I/trefoil-refinement-checkpoint.md
```

The improved-controller checkpoint is recorded in:

```text
papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06b.json
papers/SSV-I/trefoil-refinement-checkpoint-2.md
```

The first far-field-enabled checkpoint is recorded in:

```text
papers/SSV-I/data/trefoil-refinement-farfield-checkpoint-2026-05-06.json
papers/SSV-I/trefoil-farfield-checkpoint.md
```

The first box-size radial-profile comparison is recorded in:

```text
papers/SSV-I/data/example-trefoil-farfield-compare-hw5-vs-hw6.json
papers/SSV-I/trefoil-farfield-compare-note.md
```

The first fixed-resolution box-size sweep is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n24-2026-05-06.json
papers/SSV-I/trefoil-boxsize-sweep-note.md
```

The longer soft-boundary box-size sweep is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-60steps-2026-05-06.json
papers/SSV-I/trefoil-boxsize-sweep-softbc-60steps-note.md
```

The `100`-step soft-boundary box-size sweep is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-100steps-2026-05-06.json
papers/SSV-I/trefoil-boxsize-sweep-softbc-100steps-note.md
```

The direct `60`-vs-`100` step comparison is recorded in:

```text
papers/SSV-I/trefoil-boxsize-sweep-softbc-60-vs-100-note.md
```

The longer `150`/`200` step runs and the doubled-resolution `n = 48` check are recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-150steps-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-100steps-2026-05-06.json
papers/SSV-I/trefoil-longrun-and-resolution-note.md
```

The first scaled-control rerun of the doubled-resolution branch is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-100steps-scaled-2026-05-06.json
papers/SSV-I/trefoil-n48-scaled-control-note.md
```

The longer scaled `n = 48` follow-up, including the `400`-step checkpoint, is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-150steps-scaled-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-200steps-scaled-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-scaled-2026-05-06.json
papers/SSV-I/trefoil-n48-400steps-note.md
```

The direct matched-resolution comparison between the `n = 24` and `n = 48` branches is recorded in:

```text
papers/SSV-I/trefoil-matched-resolution-comparison-note.md
```

The first gravity-branch bridge note is recorded in:

```text
papers/SSV-I/alpha-g-proxy-note.md
papers/SSV-I/data/alpha-g-proxy-checkpoint-2026-05-06.json
papers/SSV-I/alpha-g-mapping-note.md
papers/SSV-I/cq-geometry-note.md
papers/SSV-I/data/cq-geometry-compare-2026-05-06.json
papers/SSV-I/cq-geometry-sweep-note.md
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-geom-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-geom-2026-05-06.json
papers/SSV-I/q-p-two-factor-probe-note.md
papers/SSV-I/data/q-p-two-factor-probe-2026-05-06.json
papers/SSV-I/q-p-two-factor-scan-note.md
papers/SSV-I/data/q-p-two-factor-scan-2026-05-06.json
papers/SSV-I/q-p-two-factor-normalized-scan-note.md
papers/SSV-I/data/q-p-two-factor-normalized-scan-2026-05-06.json
papers/SSV-I/q-p-two-factor-reexpress-scan-note.md
papers/SSV-I/data/q-p-two-factor-reexpress-scan-2026-05-07.json
papers/SSV-I/q-p-two-factor-local-scale-scan-note.md
papers/SSV-I/data/q-p-two-factor-local-scale-scan-2026-05-07.json
papers/SSV-I/q-p-two-factor-pure-additive-local-scan-note.md
papers/SSV-I/data/q-p-two-factor-pure-additive-local-scan-2026-05-16.json
papers/SSV-I/y-junction-prototype-checkpoint.md
papers/SSV-I/data/y-junction-checkpoint-n24-hw6-200steps-2026-05-16.json
papers/SSV-I/data/y-junction-state-n24-hw6-200steps-2026-05-16.npz
papers/SSV-I/data/y-junction-checkpoint-n24-hw6-600steps-2026-05-16.json
papers/SSV-I/data/y-junction-state-n24-hw6-600steps-2026-05-16.npz
papers/SSV-I/y-junction-observables-checkpoint.md
papers/SSV-I/data/y-junction-observables-n24-hw6-200steps-2026-05-17.json
papers/SSV-I/data/y-junction-observables-sensitivity-n24-hw6-200steps-2026-05-17.json
papers/SSV-I/y-junction-refinement-checkpoint.md
papers/SSV-I/data/y-junction-refinement-2026-05-17.json
papers/SSV-I/data/y-junction-refinement-n48-hw8-2026-05-17.json
papers/SSV-I/data/y-junction-refinement-fixedcal-2026-05-17.json
papers/SSV-I/y-junction-closed-prototype-checkpoint.md
papers/SSV-I/data/y-junction-closed-checkpoint-n24-hw6-200steps-2026-05-17.json
papers/SSV-I/data/y-junction-closed-state-n24-hw6-200steps-2026-05-17.npz
papers/SSV-I/data/y-junction-closed-checkpoint-n24-hw6-600steps-2026-05-17.json
papers/SSV-I/data/y-junction-closed-state-n24-hw6-600steps-2026-05-17.npz
papers/SSV-I/y-junction-closed-observables-checkpoint.md
papers/SSV-I/data/y-junction-closed-observables-n24-hw6-200steps-2026-05-17.json
papers/SSV-I/trefoil-breather-observables-checkpoint.md
papers/SSV-I/data/trefoil-breather-observables-n48-hw5-400steps-2026-05-17.json
papers/SSV-I/y-junction-closed-asym-checkpoint.md
papers/SSV-I/data/y-junction-closed-asym-checkpoint-n24-hw6-200steps-2026-05-17.json
papers/SSV-I/data/y-junction-closed-asym-state-n24-hw6-200steps-2026-05-17.npz
papers/SSV-I/data/y-junction-closed-asym-checkpoint-n24-hw6-600steps-2026-05-17.json
papers/SSV-I/data/y-junction-closed-asym-state-n24-hw6-600steps-2026-05-17.npz
papers/SSV-I/data/y-junction-closed-asym-observables-n24-hw6-200steps-2026-05-17.json
papers/SSV-I/y-junction-closed-asym-refinement-checkpoint.md
papers/SSV-I/data/y-junction-closed-asym-refinement-2026-05-17.json
papers/SSV-I/trefoil-knot-dissolution-checkpoint.md
papers/SSV-I/data/trefoil-state-n48-hw5-800steps-2026-05-17.json
papers/SSV-I/data/trefoil-state-n48-hw5-800steps-2026-05-17.npz
papers/SSV-I/lperp-first-implementation-checkpoint.md
papers/SSV-I/data/y-junction-closed-asym-lperp-lambda10-n24-hw6-200steps-2026-05-17.json
papers/SSV-I/data/y-junction-closed-asym-lperp-lambda10-n24-hw6-200steps-2026-05-17.npz
papers/SSV-I/data/y-junction-closed-asym-lperp-sweep-n24-hw6-200steps-2026-05-17.json
papers/SSV-I/trefoil-lperp-dissolution-checkpoint.md
papers/SSV-I/data/trefoil-lperp-lambda10-n24-hw6-800steps-2026-05-17.json
papers/SSV-I/data/trefoil-lperp-lambda10-n24-hw6-800steps-2026-05-17.npz
papers/SSV-I/data/trefoil-lperp-dissolution-sweep-n24-hw6-2026-05-17.json
papers/SSV-I/lperp-semi-implicit-checkpoint.md
papers/SSV-I/data/trefoil-lperp-implicit-lambda2000-n24-hw6-800steps-2026-05-17.json
papers/SSV-I/data/trefoil-lperp-implicit-lambda2000-n24-hw6-800steps-2026-05-17.npz
papers/SSV-I/data/trefoil-lperp-implicit-lambda2000-observables-n24-hw6-2026-05-17.json
papers/SSV-I/lperp-krylov-checkpoint.md
papers/SSV-I/data/trefoil-lperp-krylov-lambda2000-n24-hw6-800steps-2026-05-17.json
papers/SSV-I/data/trefoil-lperp-krylov-lambda2000-n24-hw6-800steps-2026-05-17.npz
papers/SSV-I/data/trefoil-lperp-krylov-lambda2000-observables-n24-hw6-2026-05-17.json
papers/SSV-I/q-p-two-factor-local-additive-scan-note.md
papers/SSV-I/data/q-p-two-factor-local-additive-scan-2026-05-07.json
papers/SSV-I/q-p-two-factor-local-modulated-scan-note.md
papers/SSV-I/data/q-p-two-factor-local-modulated-scan-2026-05-07.json
papers/SSV-I/q-p-two-factor-eta-calibration-note.md
papers/SSV-I/data/q-p-two-factor-eta-calibration-2026-05-07.json
papers/SSV-I/data/q-p-two-factor-eta-shape-calibration-2026-05-07.json
papers/SSV-I/q-p-two-factor-calibrated-checkpoint-note.md
papers/SSV-I/data/q-p-two-factor-calibrated-checkpoint-2026-05-07.json
papers/SSV-I/q-p-convergence-and-kernel-note.md
papers/SSV-I/data/q-p-convergence-audit-2026-05-07.json
papers/SSV-I/q-p-kernel-integral-note.md
papers/SSV-I/data/q-p-kernel-integral-2026-05-07.json
papers/SSV-I/q-p-static-potential-note.md
papers/SSV-I/data/q-p-static-potential-2026-05-07.json
papers/SSV-I/logse-static-green-function-note.md
papers/SSV-I/trefoil-continuation-sweep-note.md
papers/SSV-I/data/trefoil-continuation-sweep-n48-plus100-2026-05-17.json
papers/SSV-I/data/trefoil-continuation-sweep-n48-plus200-2026-05-17.json
papers/SSV-I/data/trefoil-plateau-driven-n48-2026-05-17.json
papers/SSV-I/data/trefoil-continuation-sweep-n48-constrained-plus100-2026-05-17.json
papers/SSV-I/data/trefoil-plateau-driven-n48-constrained-2026-05-17.json
papers/SSV-I/data/trefoil-hw6-constrained-plateau-extension-2026-05-17.json
papers/SSV-I/data/trefoil-hw6-constrained-plateau-extension-2-2026-05-17.json
papers/SSV-I/data/trefoil-hw6-projected-residual-2026-05-17.json
papers/SSV-I/data/q-p-convergence-audit-2026-05-17.json
papers/SSV-I/trefoil-hw8-note.md
papers/SSV-I/data/trefoil-hw8-projected-residual-2026-05-17.json
papers/SSV-I/trefoil-hw8-resolution-note.md
papers/SSV-I/data/trefoil-hw8-n64-projected-residual-2026-05-17.json
papers/SSV-I/trefoil-boxsize-trend-6-7-8-note.md
papers/SSV-I/data/trefoil-boxsize-trend-6-7-8-2026-05-17.json
papers/SSV-I/q-p-source-mechanism-probe-note.md
papers/SSV-I/data/q-p-source-mechanism-probe-2026-05-17.json
papers/SSV-I/q-p-halo-window-scan-note.md
papers/SSV-I/data/q-p-halo-window-scan-2026-05-17.json
papers/SSV-I/q-p-preboundary-plateau-check-note.md
papers/SSV-I/data/q-p-preboundary-plateau-check-2026-05-17.json
papers/SSV-I/q-p-cumulative-curve-compare-note.md
papers/SSV-I/data/q-p-cumulative-curve-compare-2026-05-17.json
papers/SSV-I/q-p-constraint-sensitivity-note.md
papers/SSV-I/data/q-p-constraint-sensitivity-2026-05-17.json
```

The GMRES tuning pass (improved preconditioner + restarted GMRES) is recorded in:

```text
papers/SSV-I/gmres-tuning-checkpoint.md
src/paper_i/lperp_krylov_helpers.py   (k^2+k^4 preconditioner, gmres_restarted)
src/paper_i/test_lperp_krylov.py      (17 unit tests, all passing)
```

Smoke-test comparison at `(n=16, hw=5, lambda=2000, 50 steps)`:

| solver | `min_rho` | `F^int` | violations | mean GMRES iters/step |
|---|---:|---:|---:|---:|
| k^4 only, 1 cycle (old) | 2.61e-3 | 1.034 | 5 | 30.0 |
| k^2+k^4, 5 cycles (new) | 2.23e-3 | 1.094 | 8 | 130.9 |
```

The GMRES topology-loss and min_rho guard investigation is recorded in:

```text
papers/SSV-I/gmres-topology-loss-note.md
papers/SSV-I/min-rho-guard-checkpoint.md
papers/SSV-I/gmres-tuning-final-summary.md
```

The topology-penalty breakthrough (first run with preserved trefoil topology) is recorded in:

```text
papers/SSV-I/topology-penalty-checkpoint.md
src/paper_i/topology_penalty.py
src/paper_i/test_topology_penalty.py
papers/SSV-I/data/trefoil-lperp-krylov-penalty-mu1000-n24-hw6-800steps-2026-05-18.json
papers/SSV-I/data/trefoil-lperp-krylov-penalty-mu1000-n24-hw6-800steps-2026-05-18.npz
```

Headline: at `mu=1000`, the run preserves 50 vortex links (vs 0 in every
prior run), gives `F^int = 1.223` (first physically meaningful trefoil
moment), and reaches `min_rho = 1.01e-4`.  All prior Krylov "trefoil" results
should be treated as topologically trivial.

The follow-up parameter expansion (19 runs across mu, grid, box, rho_target,
mask_threshold) is recorded in `papers/SSV-I/penalty-expansion-checkpoint.md`.
Best configuration: `mu=400, rho_target=0.01, n=24 hw=6, 800 steps` -- gives
**F^int = 2.248** with **136 out of 166 vortex links preserved** (82% of
initial topology).  Topology-preserving configurations validated at hw=5
(F^int=2.13), hw=7 (with wider mask=0.8, F^int=1.92), and n=32 (F^int=2.15).
Penalty term confirmed to generalise across grids with appropriate per-grid
tuning of `mu`, `rho_target`, and `mask_threshold`.

**Paper F target hit at n=24** (but NOT grid-converged): the topology-preserving
state at n=24 hw=6 gives `F_factor_interior = 4.547` (paper target 4.47, +1.7%).
At n=48 hw=6 the same observable rises to **6.886 (+54%)** -- the n=24 match
was a coarse-grid coincidence, not a real precision claim.  See
`papers/SSV-I/f-factor-paper-target-checkpoint.md` for the n=24 result and
`papers/SSV-I/f-factor-grid-convergence-checkpoint.md` for the honest assessment.
The penalty mechanism preserves topology robustly across all tested grids;
the F observable itself is not stable enough to claim paper-level precision.

The refinement gate (grid and box convergence sweep) is recorded in:

```text
papers/SSV-I/refinement-gate-checkpoint.md
papers/SSV-I/data/refinement-krylov-n24-hw5-800steps-noguard-2026-05-18.json
papers/SSV-I/data/refinement-krylov-n24-hw7-800steps-noguard-2026-05-18.json
papers/SSV-I/data/refinement-krylov-n32-hw6-800steps-noguard-2026-05-18.json
```

Key finding: the reference (n=24, hw=6) result is **not grid/box converged**.
Any change in dx or box size dissolves the vortex topology.  Converged results
require explicit topology enforcement (winding-number, penalty, or projected gradient).

Representative values:

| check | quantity | value |
|---|---:|---:|
| vortex profile | slope | 1.140313646074 |
| vortex profile | f(1) | 0.735813385965 |
| muon ladder | prediction | 105.037877466 MeV |
| muon ladder | observed | 105.6583755 MeV |
| Kelvin self-induction | omega first-order | 9.2889e-05 |

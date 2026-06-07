# Numerical Issue Drafts

These began as ready-to-paste issue bodies for the first computation tasks on the numerical closure track.

**Bookkeeping status (2026-06-07):** the seed issues listed here have been opened
and closed in GitHub. The checkboxes below now reflect repository status rather
than pristine issue-template text. Closed issue does not always mean
closure-grade physics; see the per-section status note.

## 1. Shared Numerical Core

**Title**

`[numerics] Build the shared numerical core for \mathcal{L}+\mathcal{L}_\perp`

**Target**

Shared numerical core for static-breather and dynamic-reconnection work

**Question**

What is the minimum reusable numerical layer the repository needs so that the static 3D breather programme and the dynamic 3D reconnection programme stop duplicating conventions, parameter handling, and diagnostics?

**Inputs / scripts**

- `docs/numerical-minimisation-roadmap.md`
- `docs/numerical-conventions.md`
- `instruments/paper_i/`
- `instruments/paper_ii_reconnection_supplement.py`

**Tasks**

- [x] Identify the common conventions already being shared informally across the existing scripts
- [x] Define one canonical nondimensionalisation note for the repo
- [x] Define the minimum shared diagnostics for static and dynamic runs
- [x] Mark which existing scripts are prototypes and which should be treated as validation baselines
- [x] Decide whether the first shared layer should live as a helper module or remain a documentation-only contract for one more iteration
- [x] Summarize what later computations will import from this shared layer

Status: closed by issue #12; implemented as the thin `instruments/shared_numerics/` contract layer.

## 2. Static Trefoil-Breather Closure

**Title**

`[numerics] Close the static 3D trefoil-breather minimisation`

**Target**

Static 3D proton-breather minimisation

**Question**

Can we turn the current trefoil Y-junction blueprint into a reproducible 3D relaxation pipeline that yields stable values for `N_Y`, `F`, and the proton-scale geometry without introducing new fitted closure factors?

**Inputs / scripts**

- `docs/numerical-minimisation-roadmap.md`
- `docs/numerical-conventions.md`
- `papers/SSV-I/main.tex`
- `instruments/paper_i/toroidal_background.py`
- `instruments/paper_i/curved_torus_relaxation.py`
- `instruments/paper_i/toroidal_projection_integrals.py`

**Tasks**

- [x] Define the initial-condition family for the trefoil Y-junction breather
- [x] Choose and document the relaxation method
- [x] Specify the core observables to report: `N_Y×F`, total energy, topology/link status
- [x] Add convergence diagnostics and resolution / box-size sensitivity checks
- [x] Decide what tolerance band is required before `N_Y×F` can be treated as more than provisional
- [x] Summarize consequences for Paper I and the static branch of Paper II

Status: issue #13 was superseded by #77. #77 is closed with candidate-grade
static result `(R,a)=(2.5,0.85)ξ`, `N_Y×F=54`. Far-field gravity extraction is
not closed by this task; it remains on the `\alpha_G` branch.

## 3. Static Gravity Extraction

**Title**

`[numerics] Extract \alpha_G from the relaxed static breather`

**Target**

Static far-field gravity extraction from the proton-breather branch

**Question**

Once a converged static breather exists, what pipeline turns its far-field density / acoustic signature into a first-principles prediction for `\alpha_G` rather than a CODATA consistency check?

**Inputs / scripts**

- `docs/numerical-minimisation-roadmap.md`
- `papers/SSV-II/main.tex`
- static-breather outputs from the preceding issue

**Tasks**

- [x] Define the far-field observable to extract from the relaxed breather as a proton acoustic monopole suppression estimator, not yet as `\alpha_G`
- [x] Connect that estimator to the Paper II acoustic monopole moment `Q_p`
- [x] Make any calibration factor between the estimator and `Q_p` explicit
- [x] Measure numerical sensitivity in the extracted suppression estimator
- [x] Compare the resulting mapped `\alpha_G` with the current Paper II consistency check
- [x] Rewrite the relevant Paper II language according to the measured result

Status: issue #14 is closed as a candidate/status-cleanup branch, not as a
first-principles `\alpha_G` derivation. The `Q_p` map remains the upgrade gate
and is now tracked by follow-up issue [#98](https://github.com/StigNorland/SVT/issues/98).

## 4. Dynamic Reconnection Closure

**Title**

`[numerics] Close the dynamic 3D reconnection minimisation`

**Target**

Time-dependent 3D reconnection event in the coupled `\mathcal{L}+\mathcal{L}_\perp` theory

**Question**

Can we replace the current structural reconnection harness with a real 3D event calculation that measures barrier geometry, cap geometry, and emitted mode content directly enough to test the `\phi` ansatz and support later sector claims?

**Inputs / scripts**

- `docs/numerical-minimisation-roadmap.md`
- `docs/numerical-conventions.md`
- `instruments/paper_ii_reconnection_supplement.py`
- `papers/SSV-II/main.tex`

**Tasks**

- [x] Define the incoming defect geometry and event setup clearly enough to reproduce
- [ ] Choose the first production-grade time-evolution scheme
- [ ] Define the full event diagnostics: energy drift, norm drift, onset/completion markers
- [ ] Define the full observables: barrier height, cap radius, cap volume, emitted mode content
- [x] Add timestep and resolution sensitivity checks
- [ ] Compare measured cap geometry with the golden-ratio ansatz instead of back-solving from the observed `W` mass
- [x] Summarize which Paper II claims remain structural even after the first reconnection run

Status: issue #15 is closed as structural/prototype work. The reconnection
harness confirms a chiral-shear barrier and cap formation at physical
`lambda_perp`, but cap geometry is not grid-converged and does not support a
derived `W` mass. The cap-geometry upgrade is now tracked by follow-up issue
[#97](https://github.com/StigNorland/SVT/issues/97).

## 5. Reduced-Problem Validation

**Title**

`[numerics] Add refinement and sensitivity checks to reduced validation problems`

**Target**

Validation layer for reduced static and dynamic problems

**Question**

Before attempting closure-grade 3D runs, can the existing reduced problems reproduce their current outputs under measured refinement and domain-size checks?

**Inputs / scripts**

- `instruments/paper_i/vortex_profile.py`
- `instruments/paper_i/curved_torus_relaxation.py`
- `instruments/paper_i/restricted_bdg_matrix.py`
- `instruments/paper_ii_reconnection_supplement.py`

**Tasks**

- [x] Select one reduced problem from each branch as a validation baseline
- [x] Add grid-refinement sweeps
- [x] Add box-size or domain-size sweeps
- [x] Record which reported quantities are stable and which drift materially
- [x] Mark the affected outputs in docs as prototype or validation rather than derived

Status: issue #16 is closed; see the reduced-problem validation summaries and
status labels in `docs/numerical-conventions.md` and Paper I/II result notes.

## 6. Claim-Status Cleanup

**Title**

`[numerics] Re-label quantitative claims by computation status`

**Target**

Paper-facing claim hygiene for unresolved numerical closures

**Question**

Which quantitative statements in Papers I and II should currently be labelled as derived, structural, ansatz-backed, or speculative, given the computations the repo has actually performed?

**Inputs / scripts**

- `docs/numerical-minimisation-roadmap.md`
- `docs/numerical-conventions.md`
- `papers/SSV-I/main.tex`
- `papers/SSV-II/main.tex`

**Tasks**

- [x] Identify every claim that still depends on missing 3D closure work
- [x] Tag each claim as derived, structural, ansatz, or speculative
- [x] Remove wording that implies the number is already first-principles when it is not
- [x] Link each deferred claim to the specific computation issue that would change its status

Status: issue #17 is closed. Later updates should keep this taxonomy synchronized
with #77 and #78: proton `N_Y×F` is candidate static geometry; scalar lepton
generation routes C/D are failed, not pending. The post-#78 lepton branch
decision is tracked by [#99](https://github.com/StigNorland/SVT/issues/99).

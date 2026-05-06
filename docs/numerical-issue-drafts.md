# Numerical Issue Drafts

These are ready-to-paste issue bodies for the first computation tasks on the numerical closure track.

Use the `Computation Task` template and paste the relevant section into the body.

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
- `src/paper_i/`
- `src/paper_ii_reconnection_supplement.py`

**Tasks**

- [ ] Identify the common conventions already being shared informally across the existing scripts
- [ ] Define one canonical nondimensionalisation note for the repo
- [ ] Define the minimum shared diagnostics for static and dynamic runs
- [ ] Mark which existing scripts are prototypes and which should be treated as validation baselines
- [ ] Decide whether the first shared layer should live as a helper module or remain a documentation-only contract for one more iteration
- [ ] Summarize what later computations will import from this shared layer

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
- `src/paper_i/toroidal_background.py`
- `src/paper_i/curved_torus_relaxation.py`
- `src/paper_i/toroidal_projection_integrals.py`

**Tasks**

- [ ] Define the initial-condition family for the trefoil Y-junction breather
- [ ] Choose and document the relaxation method
- [ ] Specify the observables to report: `N_Y`, `F`, total energy, component energies, far-field depression
- [ ] Add convergence diagnostics and resolution / box-size sensitivity checks
- [ ] Decide what tolerance band is required before `N_Y` and `F` can be treated as more than provisional
- [ ] Summarize consequences for Paper I and the static branch of Paper II

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

- [ ] Define the far-field observable to extract from the relaxed breather
- [ ] Connect that observable to the structural gravity formula used in Paper II
- [ ] Measure numerical sensitivity in the extracted suppression factor
- [ ] Compare the resulting `\alpha_G` with the current Paper II consistency check
- [ ] Rewrite the relevant Paper II language according to the measured result

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
- `src/paper_ii_reconnection_supplement.py`
- `papers/SSV-II/main.tex`

**Tasks**

- [ ] Define the incoming defect geometry and event setup clearly enough to reproduce
- [ ] Choose the first production-grade time-evolution scheme
- [ ] Define the event diagnostics: energy drift, norm drift, onset/completion markers
- [ ] Define the observables: barrier height, cap radius, cap volume, emitted mode content
- [ ] Add timestep, resolution, and initial-condition sensitivity checks
- [ ] Compare measured cap geometry with the golden-ratio ansatz instead of back-solving from the observed `W` mass
- [ ] Summarize which Paper II claims remain structural even after the first reconnection run

## 5. Reduced-Problem Validation

**Title**

`[numerics] Add refinement and sensitivity checks to reduced validation problems`

**Target**

Validation layer for reduced static and dynamic problems

**Question**

Before attempting closure-grade 3D runs, can the existing reduced problems reproduce their current outputs under measured refinement and domain-size checks?

**Inputs / scripts**

- `src/paper_i/vortex_profile.py`
- `src/paper_i/curved_torus_relaxation.py`
- `src/paper_i/restricted_bdg_matrix.py`
- `src/paper_ii_reconnection_supplement.py`

**Tasks**

- [ ] Select one reduced problem from each branch as a validation baseline
- [ ] Add grid-refinement sweeps
- [ ] Add box-size or domain-size sweeps
- [ ] Record which reported quantities are stable and which drift materially
- [ ] Mark the affected outputs in docs as prototype or validation rather than derived

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

- [ ] Identify every claim that still depends on missing 3D closure work
- [ ] Tag each claim as derived, structural, ansatz, or speculative
- [ ] Remove wording that implies the number is already first-principles when it is not
- [ ] Link each deferred claim to the specific computation issue that would change its status

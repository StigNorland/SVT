# Numerical Minimisation Roadmap

This document turns the recurring "deferred to the 3D `\mathcal{L}+\mathcal{L}_\perp` minimisation" language into an actual work program.

**Bookkeeping status (2026-06-07):** Workstream 0 is implemented as the thin
`src/shared_numerics/` layer (#12). The static trefoil-breather branch has a
candidate-grade closure result via #77: `(R,a)=(2.5,0.85)ξ` and `N_Y×F=54`,
grid-converged over the tested continuation ladder and route-independent. This
upgrades the proton geometry row from "missing computation" to "candidate
static result." The static gravity extraction and dynamic reconnection branches
remain candidate/structural rather than closure-grade and are now tracked by
follow-up issues #98 and #97, respectively. The post-#78 lepton branch decision
is tracked by #99.

The main point is simple:

- there is not one open numerical problem, but two closely related ones
- many of the most important quantitative claims depend on one of these two problems
- papers should only promote a claim after the relevant computation has passed a defined validation gate

## Purpose

The roadmap is designed to answer three practical questions:

1. What is the minimum numerical core the repository still lacks?
2. Which unresolved observables depend on the static breather computation, and which depend on the dynamic reconnection computation?
3. What counts as "closed enough" to upgrade a quantity from estimate to derivation?

## Two Core Computations

### A. Static 3D breather minimisation

This is the ground-state problem for the proton-like trefoil Y-junction breather.

Primary outputs:

- relaxed 3D field configuration for the trefoil breather (#77 candidate result)
- converged node-cost factor `N_Y` folded into the reported product `N_Y×F = 54`
- converged geometric form factor `F` folded into the reported product `N_Y×F = 54`
- acoustic monopole / far-field suppression data needed for `\alpha_G`
- stable linearisation background for later BdG work

Claims that depend primarily on this computation:

- proton mass closure beyond scalar estimates
- `\alpha_G` from first principles
- robustness of the Paper I particle-scale geometry

### B. Dynamic 3D reconnection minimisation

This is the time-dependent reconnection event in the same `\mathcal{L}+\mathcal{L}_\perp` theory.

Primary outputs:

- reconnection trajectory and barrier profile
- end-cap radius and volume during reconnection
- emitted torsional / radiative mode content
- linearised mode spectrum around the event background
- chirality-biased event statistics

Claims that depend primarily on this computation:

- `W` mass and the fate of the golden-ratio end-cap ansatz
- neutrino-sector claims
- charged-lepton generation structure beyond current ladder estimates
- CP observables tied to reconnection asymmetry
- higher-order strong-sector features linked to reconnection geometry

## Decision Rule

Use the following language consistently across papers and notes:

- `derived`: a quantity reproduced by a converged computation with documented sensitivity checks
- `structural`: a quantity whose dependence on the framework is clear, but whose number is still deferred to the computation
- `ansatz`: a calibrated or geometrically motivated placeholder such as the `\phi` cap-radius guess
- `speculative`: a sector-level idea without a validated numerical path yet

No quantity should be called "derived" if it still depends on an untested scalar closure factor.

## Workstreams

### Workstream 0: Shared Numerical Core

Goal: build the numerical substrate both major computations will use.

Required pieces:

- one canonical statement of the full `\mathcal{L}+\mathcal{L}_\perp` functional
- nondimensionalisation and parameter conventions in one place
- common grid, boundary-condition, and diagnostic utilities
- energy decomposition utilities:
  - longitudinal / pressure term
  - core term
  - chiral-shear term
  - reconnection or junction-localised term
- regression tests against current Paper I prototypes

Suggested repo direction:

- keep exploratory scripts in `src/paper_i/` and `src/paper_ii/`
- add a shared numerical core only after conventions are stable enough to reuse

Exit gate:

- every later script can import one consistent parameter set and energy decomposition
- at least one 2D or reduced-basis problem reproduces an existing known result

### Workstream 1: Reduced Validation Problems

Goal: stop jumping directly from toy scripts to full 3D claims.

Validation problems to solve first:

1. 2D single-vortex LogSE profile
2. toroidal background with curvature relaxation
3. reduced-basis BdG around the toroidal background
4. reduced reconnection-barrier problem with the current Paper II supplement

This stage is not optional. It is where discretisation choices, step control, and diagnostic conventions get debugged cheaply.

Exit gate:

- reduced problems reproduce the existing prototype outputs within documented tolerance
- grid refinement and domain-size sensitivity are measured, not assumed

### Workstream 2: Static Breather Closure

Goal: turn the trefoil Y-junction breather from blueprint language into a converged 3D result.

Tasks:

1. Define the 3D initial condition family.
   - toroidal wrapping
   - Y-junction placement
   - phase winding convention
   - symmetry assumptions, if any

2. Implement relaxation.
   - imaginary-time or gradient-flow relaxation
   - energy monotonicity diagnostics
   - vortex-core tracking through the relaxation

3. Measure observables.
   - `N_Y`
   - `F`
   - total energy and component energies
   - effective size scales and far-field density depression

4. Run sensitivity checks.
   - grid resolution
   - box size
   - timestep / step size
   - initial-condition family

Exit gate:

- `N_Y` and `F` stop moving outside the chosen tolerance band under refinement
- the relaxed breather is stable under small perturbations
- the computation yields a reproducible path to the proton mass estimate without fresh fitted constants

Direct downstream targets:

- Paper I appendix cleanup
- Paper II `\alpha_G` programme
- any later claim that uses proton-scale geometry as input

### Workstream 3: Static Gravity Extraction

Goal: compute the far-field quantity needed for `\alpha_G` from the converged breather, instead of importing it from CODATA.

Tasks:

1. Extract the long-range density / acoustic field around the relaxed breather.
2. Measure a provisional estimator for the proton's sub-grain acoustic monopole suppression.
3. Map that estimator into the effective acoustic monopole moment `Q_p`.
4. Propagate that result into the structural Paper II gravity formula.
5. Compare predicted `\alpha_G` with the current consistency check.

Current bridge discipline:

- do not identify a raw far-field scalar with `\alpha_G`
- treat the static output first as an estimator for the proton acoustic monopole suppression
- keep any calibration factor between the estimator and `Q_p` explicit until the geometry fixes it

Current working template:

- static branch estimator: `\Pi_{\rm mono} \approx 1 - \rho_{\rm shell}`
- Paper II structural hook: `Q_p \sim \delta V_p (a_p / \xi)^3`
- gravity target relation: `G = \rho_0 \omega_p^2 Q_p^2/(8\pi m_p^2)` and therefore `G = \alpha_G \hbar c \alpha^2/(N_p^2 m_e^2)`

Exit gate:

- a single documented pipeline maps the relaxed breather to a predicted `\alpha_G`
- uncertainty is dominated by measured numerical sensitivity, not a hidden or guessed calibration factor

### Workstream 4: Dynamic Reconnection Closure

Goal: simulate the full reconnection event that currently carries too many deferred claims.

Tasks:

1. Define the event geometry.
   - incoming defect types
   - chirality assignments
   - relative phase and separation
   - event frame and boundary treatment

2. Implement time-dependent evolution.
   - stable integrator for the coupled functional
   - event detection for reconnection onset and completion
   - energy accounting during topology change

3. Extract event observables.
   - barrier height
   - cap radius and cap volume as functions of time
   - emitted radiative channels
   - chirality asymmetry metrics

4. Test the `\phi` ansatz.
   - compare measured cap geometry with the golden-ratio estimate
   - keep the ansatz only if the free relaxation actually lands near it

Exit gate:

- event observables are reproducible across refinement and nearby initial conditions
- the cap geometry is measured directly rather than back-solved from the observed `W` mass

### Workstream 5: Linearised Spectra on Event Backgrounds

Goal: stop speaking about neutrinos, flavour, and lepton generations as if they were scalar side effects.

Tasks:

1. Linearise around the converged toroidal and reconnection backgrounds.
2. Compute bound and radiative mode spectra.
3. Identify which observables can be read off directly:
   - harmonic mode spacing
   - degeneracy structure
   - chirality splitting
   - Berry-phase transport candidates

Exit gate:

- the repository can point to a computed operator and spectrum, not just a narrative about where the physics "should" live

## Observable Matrix

| Observable | Depends first on | Current status | Upgrade condition |
|------|------|------|------|
| Proton mass closure | Static breather | candidate static result: #77 gives `N_Y×F=54` at `(R,a)=(2.5,0.85)ξ`; residual physical shallow-minimum uncertainty remains | separate `N_Y`/`F` decomposition and final paper propagation if needed |
| `\alpha_G` | Static breather far field | CODATA consistency check + provisional monopole estimator; follow-up #98 | predicted from relaxed breather through documented `Q_p` map |
| `W` mass | Dynamic reconnection | `\phi` ansatz; cap-geometry upgrade #97 | measured cap geometry |
| Neutrino spectrum | Event-background linearisation | structural hypothesis | computed mode spectrum |
| PMNS / CP observables | Event-background linearisation + chirality statistics | speculative | reproducible asymmetry and phase extraction |
| Lepton generations | Toroidal / event spectra | scalar-SSV routes C/D failed; `8^n` is a numerical curiosity, not a first-principles degeneracy; branch decision #99 | new half-quantum-vortex or spinorial-order-parameter branch, or retirement |

## Immediate Repo Tasks

These are the next concrete steps the repository should track.

1. [x] Write down one canonical numerical conventions note.
2. [x] Mark which existing scripts are prototype-only and which are validation baselines.
3. [x] Add a computation issue for the static breather minimisation.
4. [x] Add a separate computation issue for the dynamic reconnection minimisation.
5. [x] Add a validation issue for sensitivity tests on reduced problems.
6. [x] Add a claim-status issue to replace "derived" language where the computation is still missing.

All six seed tasks have corresponding closed issues (#12, #13/#77, #15, #16,
#17). The closures do not mean every physical observable is derived:
`N_Y×F` is candidate-grade from #77, `\alpha_G` remains candidate/blocked on the
`Q_p` map, and dynamic reconnection remains structural.

## Recommended Paper Discipline

### Paper I

- keep the qualitative trefoil breather picture
- cite #77 for the candidate-grade `N_Y×F=54` proton-geometry result
- avoid promoting separate `N_Y` and `F` values beyond the diagnostics actually reported

### Paper II

- present `W`, neutrino, CP, and generation claims as downstream targets of the reconnection computation
- keep `\alpha_G` explicitly on the static-breather branch, not mixed into the reconnection branch
- keep scalar-SSV lepton generation routes C/D marked failed unless a new HQV/spinorial branch is opened

### Later Papers

- only inherit quantitative claims after the relevant workstream has passed its exit gate

## What Success Looks Like

This roadmap succeeds if the repo reaches a point where the question

"what computation would change the status of this claim?"

has a one-line answer for every major unresolved quantitative result.

# Trefoil Breather Minimisation Plan

This note is the repo-side starting specification for issue [#13](https://github.com/StigNorland/SVT/issues/13):
`[numerics] Close the static 3D trefoil-breather minimisation`.

It does not claim the problem is solved. Its purpose is to turn the current Paper I blueprint into a sequence of implementable numerical decisions.

## Goal

Construct a reproducible static 3D relaxation pipeline for the proton-like trefoil Y-junction breather that can eventually support:

- stable `N_Y`
- stable geometric factor `F`
- a defensible proton-scale energy decomposition
- the static far-field extraction later needed for `\alpha_G`

## Scope

This plan covers only the static branch.

It does not include:

- dynamic reconnection
- `W`-sector cap geometry
- neutrino or CP observables

Those belong to the dynamic branch of the numerical roadmap.

## Starting Assets Already In Repo

Closest current ingredients:

- `instruments/paper_i/vortex_profile.py`
- `instruments/paper_i/toroidal_background.py`
- `instruments/paper_i/curved_torus_relaxation.py`
- `instruments/paper_i/toroidal_projection_integrals.py`

These are enough to define a first background family, but not yet enough to claim full 3D closure.

## Initial-Condition Family

The first implementation should stay narrow.

### Background geometry

- one toroidal major radius `R`
- one core scale `\xi`
- three filament branches arranged as a trefoil-like Y-junction skeleton
- phase winding fixed consistently on each branch

### What should vary in the first sweep

- major radius `R / \xi`
- branch-placement geometry near the junction
- smoothing radius used to regularise the initial phase singularity

### What should not vary yet

- exotic topologies
- multiple competing branch families
- broad parameter scans over unrelated stiffness choices

The first task is not discovery of all possible objects. It is closure of one clearly defined candidate.

## Relaxation Strategy

Recommended first pass:

1. initialise the trefoil field on a cubic 3D grid
2. relax by imaginary-time or gradient-flow evolution
3. track energy and topology through the relaxation
4. stop only when a stationarity criterion is met, not after an arbitrary step count

Minimum controls to expose explicitly:

- grid size
- box size
- relaxation step size
- stopping tolerance
- maximum step count

## Observables

The solver should report four classes of outputs.

### A. Core observables

- total relaxed energy
- `N_Y`
- `F`

### B. Geometry observables

- branch lengths after relaxation
- junction neighbourhood size
- effective breather radius
- core-thickness diagnostics

### C. Far-field observables

- density depression profile away from the breather
- candidate monopole-suppression measure for later gravity extraction

### D. Solver diagnostics

- energy monotonicity
- residual norm / stationarity measure
- topology-preservation check
- sensitivity to refinement

## Validation Gates

The result should not be called derived unless all of the following are true.

1. `N_Y` remains within a fixed tolerance band under grid refinement.
2. `F` remains within a fixed tolerance band under box-size changes.
3. The relaxed object is recovered from more than one nearby initial condition.
4. The branch topology survives relaxation without ambiguous reconnection artefacts.
5. Reported energies are accompanied by the numerical controls that produced them.

## Suggested Milestones

### Milestone 1

Static field initialiser exists and can produce one trefoil-like configuration reproducibly.

### Milestone 2

Relaxation loop exists and decreases total energy reliably on small test grids.

### Milestone 3

Topology tracking and stationarity diagnostics exist.

### Milestone 4

First refinement sweep for `N_Y` and total energy exists.

### Milestone 5

First candidate far-field extraction exists for the later `\alpha_G` issue.

## Recommended File Direction

Likely next code additions:

- `instruments/paper_i/trefoil_breather_static.py`
- `instruments/paper_i/trefoil_observables.py`
- optional helper reuse from `instruments/shared_numerics/`

This should happen only after the script header and status conventions are in place.

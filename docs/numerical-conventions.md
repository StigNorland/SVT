# Numerical Conventions

This note is the starting point for Workstream 0 of the numerical minimisation roadmap.

Its job is modest but important:

- give the repository one shared vocabulary for the `\mathcal{L}+\mathcal{L}_\perp` calculations
- separate prototype conventions from closure-grade conventions
- make it obvious when two scripts are using different normalisations or assumptions

This is not yet a final theory note. It is a working agreement for code in the repository.

## Scope

These conventions apply first to:

- `instruments/paper_i/`
- `instruments/paper_ii_reconnection_supplement.py`
- any later static-breather or dynamic-reconnection solver

They should be updated before large production code is added, not after.

## Numerical Branches

The repo now treats two related but distinct numerical branches:

### Static branch

Used for:

- vortex profile
- toroidal background
- trefoil Y-junction breather
- proton-scale geometry
- `\alpha_G` extraction

### Dynamic branch

Used for:

- reconnection barrier
- time-dependent topology change
- cap geometry
- emitted radiative / torsional mode content

The same field theory should underlie both branches, but diagnostics and success criteria differ.

## Naming

Use these names consistently in code, docs, and issue text.

- `LogSE`: logarithmic Schr\"odinger / Gross-Pitaevskii-like longitudinal sector
- `L_perp` or `lambda_perp`: chiral-shear sector
- `static breather`: relaxed 3D trefoil Y-junction background
- `reconnection event`: time-dependent topology-changing dynamic run
- `acoustic monopole suppression estimator`: static far-field quantity used as a provisional bridge toward the gravity branch
- `Q_p`: effective proton acoustic monopole moment in the Paper II gravity sector
- `observable`: quantity reported to papers
- `diagnostic`: quantity used to judge solver health

Avoid calling a diagnostic an observable unless it is actually part of a paper-level claim.

## Parameter Conventions

Until a stricter shared module exists, scripts should document explicitly:

- whether they are dimensional or nondimensional
- what quantity sets the unit length
- what quantity sets the unit time
- what quantity sets the unit density / amplitude
- whether `lambda_perp` is physical, fitted, scanned, or placeholder

Minimum header block for any new solver script:

1. problem type: static or dynamic
2. nondimensionalisation used
3. free parameters being scanned
4. observables reported
5. known limitations

## Default Reporting Rules

Every computation note or script output should distinguish:

- inputs
- numerical controls
- diagnostics
- observables

### Inputs

Examples:

- grid size `n`
- box length
- timestep `dt`
- step count
- ring radius
- separation
- `lambda_perp`

### Numerical controls

Examples:

- integrator type
- relaxation rule
- convergence threshold
- snapshot cadence
- boundary condition

### Diagnostics

Examples:

- total energy monotonicity
- norm drift
- residual size
- vortex-core tracking stability
- refinement sensitivity

### Observables

Examples:

- `N_Y`
- `F`
- cap radius
- cap volume
- saddle excess
- far-field suppression factor
- acoustic monopole suppression estimator
- mode splitting

## Status Labels for Outputs

Each reported quantity should be tagged internally as one of:

- `prototype`
- `validation`
- `candidate`
- `closure-grade`

Meaning:

- `prototype`: exploratory, useful for intuition only
- `validation`: used to reproduce an earlier reduced result
- `candidate`: may inform draft language, but has not passed sensitivity checks
- `closure-grade`: documented under refinement and suitable to support a paper-level derived claim

Current repo state:

- most `instruments/paper_i/` outputs are `prototype`
- the #77 trefoil continuation result is `candidate`: it gives reproducible
  `N_Y×F=54` at `(R,a)=(2.5,0.85)ξ`, but does not by itself close the separate
  `Q_p` / `\alpha_G` map
- current reconnection supplement outputs are `prototype` to `validation`
- no current result should yet be treated as `closure-grade`

## Static-Branch Minimum Diagnostics

Any static breather solver should report at minimum:

- total energy per iteration or time slice
- component energies, if separated
- residual / stationarity measure
- vortex-core count and topology-tracking status
- sensitivity to grid size
- sensitivity to box size
- sensitivity to initial condition family

If the run is being used for the gravity branch, report additionally:

- which quantity is being treated as the acoustic monopole suppression estimator
- how that estimator depends on shell location or outer-region extraction choice
- whether any mapping to `Q_p` introduces an explicit calibration factor

## Dynamic-Branch Minimum Diagnostics

Any reconnection solver should report at minimum:

- total energy drift
- norm drift
- reconnection onset and completion markers
- cap-radius extraction method
- sensitivity to timestep
- sensitivity to resolution
- sensitivity to event initial conditions

## Paper Discipline

No paper should promote a quantity from estimate to derivation unless the underlying output has reached `closure-grade`.

In practice this means:

- a scalar fit or geometric guess is not enough
- agreement with the target number alone is not enough
- one grid at one parameter setting is not enough

## Near-Term Repo Tasks

1. Add status labels to the major existing scripts in `instruments/paper_i/`.
2. Mark `instruments/paper_ii/reconnection_supplement.py` as a reduced structural harness, not a production reconnection solver.
3. When the first shared solver utilities appear, move these conventions into code comments and reusable helpers.

## Shared-Layer Status (Issue #12)

The conventions above are crystallised in the `shared_numerics` Python
package under `instruments/shared_numerics/`. That package is the artifact of
issue #12 and is intentionally a thin layer: dataclasses for canonical
nondimensionalisation, grid spec, relaxation / time-step controls,
minimum diagnostics for each branch, and machine-readable script
metadata with status labels. It is not yet a production solver layer.

### Contract for closure-grade runs

Closure-grade workstreams (`#13` static breather minimisation, `#15`
dynamic reconnection minimisation) should import the following from
`shared_numerics`:

| Import                  | Use                                                              |
|-------------------------|------------------------------------------------------------------|
| `Nondimensionalisation` | Declare the run's unit system; catch mismatches between scripts. |
| `GridSpec`              | Cartesian grid description shared with `instruments/paper_i/` prototypes.|
| `RelaxationControls`    | Static gradient-flow controls including topology-preservation knobs.|
| `TimeStepControls`      | Split-step time-integration controls.                            |
| `StaticDiagnostics`     | Advertise which minimum static checks were run.                  |
| `DynamicDiagnostics`    | Advertise which minimum dynamic checks were run.                 |
| `DynamicObservables`    | Standard reconnection observables (saddle, cap, channel cosine). |
| `OutputStatus`          | `prototype` / `validation` / `candidate` / `closure-grade` enum. |
| `ScriptMetadata`        | Top-of-script machine-readable status block.                     |

New scripts on either branch should import these instead of redefining
equivalents. The longer-form contract and rationale live in the
`shared_numerics` package docstring (`instruments/shared_numerics/__init__.py`).

### Known convention mismatch (dynamic branch)

`instruments/paper_ii/reconnection_supplement.py` uses
`c_eff = sqrt(2 * log_pressure)` (with `log_pressure = 8` by default)
where the canonical static-branch convention is `c = 1`. The mismatch
is flagged in that script's `SCRIPT_METADATA.limitations`. Closure-grade
dynamic runs under issue #15 should reconcile this with the canonical
unit system before being treated as derived predictions.

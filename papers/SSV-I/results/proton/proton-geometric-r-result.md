# Proton geometric-R diagnostic result: FAIL

**Date:** 2026-05-30. Outcome of the pre-registered test in
`papers/SSV-I/proton-geometric-r-prereg.md`. Reproducer:
`python instruments/paper_i/proton_geometric_r_probe.py`.

## One-line verdict

**FAIL by the pre-registered rule.** Both candidate $R_{\rm geom}$
definitions give spreads $> 10\%$ across the three grid resolutions
$n = 24, 48, 72$ at $hw = 6\,\xi$. The deficit-weighted RMS minor radius
$R_{\rm profile}$ spreads 14%; the centerline half-spacing
$R_{\rm centerline}$ spreads 71%; neither produces an $F(R_{\rm geom})$
that agrees better than the existing 24% paper-cutoff spread.
Additionally, the relaxed configuration's effective minor radius
$\approx 3.8\,\xi$ does NOT match the seed value $0.85\,\xi$ that the
paper's $R = 1.18\,\xi$ derivation assumed.

## The data

| state         | $n$ | $R_{\rm profile}/\xi$ | $R_{\rm centerline}/\xi$ | $F(R = 1.18)$ | $F(R_{\rm profile})$ | $F(R_{\rm centerline})$ |
|---------------|-----|----------------------:|-------------------------:|--------------:|---------------------:|------------------------:|
| penalty-mu400 | 24  | 3.345                 | 0.363                    | 5.606         | 2.701                | 26.646                  |
| penalty-best  | 48  | 3.760                 | 0.415                    | 4.528         | 2.055                | 17.350                  |
| penalty-n72   | 72  | 3.845                 | 0.200                    | 4.417         | 1.983                | 59.962                  |

Cross-grid spread:
- $R_{\rm profile}$: 14% (FAIL the 5% threshold)
- $R_{\rm centerline}$: 71% (catastrophic FAIL)
- $F(R = 1.18)$ (imposed paper cutoff): 24% across all three, but only 2.5%
  between the two fine grids ($n = 48, 72$).
- $F(R_{\rm profile})$: 32% across all three, 3.6% between fine grids.
- $F(R_{\rm centerline})$: 123% across all three, FAIL.

Per the pre-registered decision rule:
$R_{\rm profile}$ FAIL on $R_{\rm geom}$ convergence (14% > 10%);
$R_{\rm centerline}$ FAIL on both axes.
**Overall: FAIL.**

## What went structurally wrong

Two distinct issues, both worth recording:

**1. The relaxed minor radius is $\sim 3.8\,\xi$, not $0.85\,\xi$.** The seed
configuration uses $r_{\rm minor} = 0.85$, and the paper's geometric
derivation of $R = 1.18 = 1.388 \times 0.85$ assumes the relaxed state
preserves this minor radius. The deficit-weighted RMS measurement shows
the relaxed deficit spreads over a region $\sim 4\times$ broader than the
seed, so the geometric-ratio extrapolation $R/r_{\rm minor} = 1.388$
applied to the seed value $0.85$ has no foothold in the actual relaxed
configuration. Using the relaxed-state minor radius would give
$R_{\rm geom} \approx 3.8 \times 1.388 = 5.3\,\xi$, and $F$ there is
$\sim 1.7$, giving an implied $m_p \sim 3.0 \times 1.7 \times 70 \approx
360\,$ MeV -- nowhere near CODATA.

**2. The centerline-minimum algorithm fails at high resolution.** The
$n = 72$ grid has spacing $\Delta x = 0.167\,\xi$; the algorithm's
"nearest density-minima" search picks up adjacent grid cells in the same
vortex strand (intra-strand distances $\sim \Delta x$) rather than
distinct strand cores. The $n = 72$ result $R_{\rm centerline} = 0.20$
is an algorithmic artifact, not a physical measurement. A meaningful
centerline R_geom needs actual 3D vortex centerline tracing (Newton solve
for nodal curves of $\Psi = 0$, then minimum-distance computation across
genuinely distinct strands), which is significant new infrastructure
not in scope for this pre-registration.

## What this finding actually rules out

The simple "deficit-weighted RMS minor radius" definition of $R_{\rm geom}$
is ruled out as a geometric closure for the proton form factor: the relaxed
configuration is too broad relative to the seed for this scale to play the
role $R = 1.18\,\xi$ does in the paper's mass formula.

The simple "nearest-minimum strand half-spacing" definition is ruled out by
algorithmic instability at high resolution.

What is NOT ruled out:
- A proper 3D centerline-tracing algorithm might give a clean grid-stable
  inter-strand half-spacing.
- A different physical observable (e.g. derived from the curvature radius
  at the Y-junction, or from a topological invariant) could plausibly
  define $R_{\rm geom}$.

## What does survive: fine-grid F(R=1.18) is stable

A side observation, not part of the pre-registered test: at the paper
cutoff $R = 1.18\,\xi$, the two fine grids $n = 48, 72$ give
$F = 4.53, 4.42$, agreeing to 2.5%. This is consistent with the closure
status memo's existing statement that the $F$ at imposed $R = 1.18\,\xi$
is grid-converged at the $\sim 6\%$ level. The cutoff itself is the
unresolved question, not the value of $F$ at it.

## Per the closure status memo's three gates

The diagnostic addressed gate (ii): geometric derivation of $R = 1.18\,\xi$.
Result: FAIL with the simple extractors tried. Gates (i) (dedicated $N_Y$
cross-grid sweep at fixed penalty config) and (iii) (recovery from
non-trefoil initial conditions) are untouched. The §Proton gapbox in
SSV-I main.tex stands as written: $F$ remains a cutoff-dependent
calibration; the only way to promote the proton mass formula from
candidate to derived is one of (a) a more sophisticated centerline R_geom
extraction, (b) gate (iii) showing topological convergence from independent
initial conditions, or (c) showing $N_Y \cdot F$ is cutoff-invariant
(itself flagged as "falsified by prior runs" per the closure memo).

## Files

- Pre-registration: `papers/SSV-I/proton-geometric-r-prereg.md`
- Probe: `instruments/paper_i/proton_geometric_r_probe.py` (reproducible in seconds)
- State files used (all topology-preserving at hw=6 per closure memo):
  - `penalty-mu400-rho0p01-n24-hw6-1600steps-2026-05-18.npz`
  - `penalty-best-n48-hw6-800steps-2026-05-19.npz`
  - `penalty-n72-mu2000-rho0p05-2026-05-19.npz`

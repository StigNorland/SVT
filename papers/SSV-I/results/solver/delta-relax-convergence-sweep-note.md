# delta_relax Convergence Sweep: Numerical-Profile Bridge Check (2026-05-20)

> **Status (2026-05-30): superseded by Path B null.** Numerical claims in this note about the muon eigenfrequency reaching $\omega/\omega_c = 0.207$, the $\delta_{\rm relax}$ calibration, the $\alpha$-harmonic ladder identification, or the $1/\sqrt{N_{\rm modes}}$ basis-truncation residual are now governed by `papers/SSV-I/path-b-eigenvalue-result.md`: that test showed the muon agreement is not basis-robust (drifts $\pm 13\%$ across 4 bases, empty window in 2 of 4) and the pion rung is absent in every basis. Structural sub-results that stand on their own (operator algebra, analytic derivations, the cubic-vertex one-loop result, dimensional setup) remain valid in isolation; what is superseded is their use as evidence for the ladder identification or as a closure path to it. Quarantined inputs: `src/_fitted_quarantine/`. Tracking: issue #66.

Script: `src/paper_i/thin_ring_delta_relax_sweep.py`

Data:

- `papers/SSV-I/data/delta-relax-sweep-numerical-profile-smoke-2026-05-20.json`
- `papers/SSV-I/data/delta-relax-sweep-numerical-profile-fd-profile-2026-05-20.json`
- `papers/SSV-I/data/delta-relax-sweep-numerical-profile-n37-2026-05-20.json`

## One-line result

The relaxed-background correction is positive, stable in sign, and remains at a
few-percent scale when the finite-alpha bridge uses the numerical BdG radial
profile consistently:

```math
\lambda_\perp^{\rm BdG}
  = {\pi\over4}\,[1+\delta_{\rm relax}+c_2\alpha^2+\cdots],
\qquad
\delta_{\rm relax}=+0.038\pm0.005.
```

The older toy-profile sweep gave a negative correction around `-0.030`. That
result is now superseded for paper-facing interpretation because it mixed the
relaxed coefficients with the toy straight-core bridge profile.

## Sweep Results

| sweep slice | successful points | delta_relax_chi | delta_relax_R | verdict |
|-------------|-------------------|-----------------|---------------|---------|
| `n={25,31}`, `hw={5,6}`, `profile_n=800`, `fd=0.25` | 4/4 | `+4.210% +/- 0.615%` | `+0.210% +/- 0.035%` | sign/scale stable |
| `n=31`, `hw={5,6}`, `profile_n={800,1200}`, `fd={0.20,0.25,0.30}` | 12/12 | `+3.999% +/- 0.455%` | `+0.199% +/- 0.026%` | profile and fd stable |
| `n=37`, `hw={5,6}`, `profile_n=800`, `fd=0.25` | 2/2 | `+3.791% +/- 0.545%` | `+0.184% +/- 0.031%` | finest grid tested |

## Structural Observations

1. `profile_n` is not a live uncertainty at the tested precision. Moving from
   `800` to `1200` changes `delta_relax_chi` by only a few `1e-5`.
2. `finite_diff_step` is also benign over `0.20, 0.25, 0.30`; the fitted
   coefficients move slightly, but the bridge ratio is stable.
3. The dominant residual systematic is `half_width`. At `n=37`, `hw=5` gives
   `delta_relax_chi = +3.405%`, while `hw=6` gives `+4.176%`.
4. Increasing `n` from 25 to 37 gently lowers the central correction, but does
   not make it grow, flip sign, or wander unpredictably.
5. The `R-K` bridge correction is tiny, about `+0.18%` to `+0.21%`, and is not
   the relevant muon-channel uncertainty.

## Paper-Level Interpretation

The thin-ring bridge survives this check. The corrected coefficient should be
carried as:

```math
\lambda_\perp^{\rm BdG}
  = {\pi\over4}\,[1+0.038(5)+c_2\alpha^2+\cdots].
```

This is not yet a full closure theorem, because the complete second variation
has not been inserted. But the reduced curved-background ansatz is no longer
showing the failure mode that would force an immediate full 3D circumferential
grid: no sign chaos, no refinement growth, and no finite-difference/profile
instability.

## Next Step

Propagate `lambda_perp^code = (pi/4) * (1 + delta_relax)` through the reduced
BdG eigenproblem over `delta_relax in [0.033, 0.043]`. If the muon eigenfrequency
remains close to the target across that band, the leading-order thin-ring bridge
becomes a quoted prediction with an explicit numerical uncertainty.

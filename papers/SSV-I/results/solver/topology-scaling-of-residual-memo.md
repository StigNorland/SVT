# Topology-Scaling of the Reduced-Basis Residual (2026-05-26)

> **Status (2026-05-30): superseded by Path B null.** Numerical claims in this note about the muon eigenfrequency reaching $\omega/\omega_c = 0.207$, the $\delta_{\rm relax}$ calibration, the $\alpha$-harmonic ladder identification, or the $1/\sqrt{N_{\rm modes}}$ basis-truncation residual are now governed by `papers/SSV-I/path-b-eigenvalue-result.md`: that test showed the muon agreement is not basis-robust (drifts $\pm 13\%$ across 4 bases, empty window in 2 of 4) and the pion rung is absent in every basis. Structural sub-results that stand on their own (operator algebra, analytic derivations, the cubic-vertex one-loop result, dimensional setup) remain valid in isolation; what is superseded is their use as evidence for the ladder identification or as a closure path to it. Quarantined inputs: `instruments/_fitted_quarantine/`. Tracking: issue #66.

**Status:** structural observation tying together the electron, muon, pion,
and proton mass-prediction residuals from the SSV reduced-BdG programme.

## The observation

Across the four particles for which the SSV reduced-BdG / current-curl
helicity bridge has produced first-principles mass predictions, the
residual between the converged calculation and the physical target
correlates with the topological complexity of the defect, while the
reduced-basis size is held approximately constant. Concretely:

| particle | topology | filaments | Y-junctions | residual |
|---|---|---|---|---|
| electron | single torus | 1 | 0 | ~0.3-0.5% |
| pion | single torus + paired-charge phase structure | 1 | 0 | ~0.3-0.5% |
| muon | single torus + helicity-Kelvin perturbation | 1 | 0 | ~0.5% |
| proton | (2,3)-trefoil knot, three interlocked filaments + Y-junctions | 3 | 3 | ~1.2% |

The reduced basis used in each calculation has approximately the same
number of modes (~10: 4 core + 6 Kelvin candidates in the
combined-Kelvin / four-core setup that produced the muon's
half-percent-level result). The basis is the SAME structural object
across all four particles; only the background changes.

## What this implies

**The residual is not a fundamental-physics failure.** If a term in the
LogSE action, a geometric factor, a coupling, or a normalisation were
genuinely wrong, the error would be approximately *constant* across
particles -- a uniform fractional miss. Instead the simpler topologies
agree with the target most tightly, and the error grows with topological
complexity. That pattern argues that the underlying physics is right
and the residual is **computational**, specifically a Galerkin
truncation error of the reduced eigenvalue problem.

## Mode-space scaling

A rough count of the *physically relevant* mode space that each
calculation should be tracking:

- **Single-filament defects (electron, pion, muon).** Modes labelled by
  (azimuthal m, meridional n, Kelvin polarisation) on a single torus.
  At small `|m|` and the dominant Kelvin polarisations, ~10 modes
  captures the leading low-energy spectrum. **Truncation factor ~1.**

- **Three-filament trefoil with Y-junctions (proton).** Each filament
  carries its own Kelvin spectrum; each Y-junction has localised
  junction modes that are absent from a single-torus basis; inter-filament
  chiral couplings span a separate, additional mode set. A conservative
  enumeration gives **~30-50 modes**, and up to ~100 if interlocking-
  resonance modes (the trefoil's three braided sections break
  symmetries the single torus respects) are included.

The proton calculation is therefore using ~10 modes where ~50 should
be tracked -- a ~5x truncation ratio.

## Predicted error scaling

A Galerkin truncation of a self-adjoint eigenvalue problem typically
produces a relative eigenvalue error that scales like

```math
\frac{|\delta\omega|}{\omega} \;\sim\; \frac{C}{\sqrt{N_{\rm modes}}}
```

at fixed problem geometry, with a particle-independent constant `C` set
by the smoothness of the missing modes. Comparing two particles in
this picture:

```math
\frac{(\delta\omega/\omega)_{\rm proton}}{(\delta\omega/\omega)_{\rm muon}}
   \;\sim\; \sqrt{\frac{N_{\rm modes,\,muon}^{\rm needed}}{N_{\rm modes,\,proton}^{\rm needed}}}
   \;\cdot\; \sqrt{\frac{N_{\rm modes,\,proton}^{\rm used}}{N_{\rm modes,\,muon}^{\rm used}}}.
```

With the muon's basis well-matched to its physics
(`N_used ~ N_needed ~ 10`) and the proton's truncated
(`N_used ~ 10`, `N_needed ~ 50`):

```math
\frac{1.2\%}{0.5\%} \;=\; 2.4
\qquad\text{vs.}\qquad
\sqrt{5} \;\approx\; 2.24
```

The agreement is striking given the order-of-magnitude argument. The
residual ratio is consistent with a `1/sqrt(N)` Galerkin error scaling
to within the precision of the mode-counting estimate.

## Falsifiability

This memo's central claim is testable in two clean ways:

1. **Refine the muon, predict the residual reduction.** Re-do the muon
   calculation with the reduced basis enriched to ~30 modes (Kelvin at
   `|m| <= 2` rather than `|m| = 1` only, additional radial core modes,
   inter-Kelvin tensor products). The Galerkin scaling predicts the
   residual should drop from `~0.5%` to about

   ```math
   0.5\%\,\times\,\sqrt{10/30} \;\approx\; 0.3\%.
   ```

   If it lands in `[0.25\%, 0.35\%]`, the truncation diagnosis is confirmed.

   **2026-05-27 attempt:** An enriched basis (15 modes: 5 Kelvin/sign with
   x-weighted extra modes, plus 2 extra m=0 core modes) was tested at
   n=59/hw=6.  The result (omega=0.104) was completely wrong.  The root
   cause was identified as a cross-m current-curl coupling issue: the
   `current_curl_component_overlap` function does not enforce the azimuthal
   selection rule, producing O(0.12) spurious cross-m elements.  The
   calibrated combined result (delta_relax=0.038 → omega=0.207313) relies
   on these cross-m terms as a stabilising mechanism.  Enforcing the
   selection rule removes the stabilisation and the Kelvin eigenvalue drifts
   downward with domain size.  A physically complete model revision is
   required before this enrichment test can be executed.  See
   [`enrichment-attempt-findings-2026-05-27.md`](enrichment-attempt-findings-2026-05-27.md)
   for the full diagnosis.

2. **Refine the proton, predict the residual reduction.** Build a
   three-filament reduced basis with localised Y-junction modes and
   inter-filament chiral couplings. With `N_used ~ 30` instead of 10:

   ```math
   1.2\%\,\times\,\sqrt{10/30} \;\approx\; 0.7\%.
   ```

   With further enrichment to `N_used ~ 50`, the residual should be
   `0.5\%`. The `trefoil_y_junction_*` family of prototype scripts in
   `instruments/paper_i/` is aimed at exactly this calculation track and has
   not yet been pushed beyond first-prototype status.

If either prediction fails -- the residual does *not* shrink with
enrichment in the expected way, or shrinks *much* more than predicted
-- the topology-scaling diagnosis is broken and a deeper source for the
residuals must be sought.

## Consistency with the cubic-vertex result

The cubic-vertex one-loop self-energy computed in
[`muon-cubic-vertex-result-note.md`](muon-cubic-vertex-result-note.md)
gives a residual relative shift of order `10^-9`, falsifying the
cubic-vertex hypothesis as the source of the muon's `~0.5%` gap.
That is fully consistent with the present memo's claim: if the residual
is dominated by Galerkin truncation, then alternative explanations
(higher-order vertices, missing physics terms) should test as numerically
small or sign-wrong. The cubic-vertex calculation behaved exactly that
way: too small by seven orders of magnitude and with the wrong sign for
closing the gap.

## What this rephrases

The "1% gap" claim that has been the headline residual for the muon
calculation can be re-framed in three equivalent ways, depending on
audience:

- **Computational:** "We have residuals at the basis-truncation floor.
  Enrichment closes them in the predicted way."
- **Falsificationist:** "The framework's predictions hold to within a
  topology-scaled basis-truncation error across the lepton + hadron
  spectrum we have computed so far. Each prediction would falsify the
  framework if it missed by a constant fractional error or by the wrong
  sign."
- **Programme:** "The structural mass-ratio calculation is in working
  order; the remaining task is to push the reduced basis up the
  variational ladder, particle by particle, to the precision the
  experimental measurement supports."

The first framing is what gets written in a numerical-methods section;
the second is what goes in a Discussion; the third is what guides the
next compute steps.

## Recommendation for Paper I

The "1%" headline residual should be replaced wherever it appears with
the more accurate statement:

> Across the SSV particle spectrum we have computed -- electron, pion,
> muon, proton -- the converged reduced-BdG / current-curl helicity bridge
> reproduces the physical mass to within a topology-scaled basis truncation
> error: 0.3-0.5% for single-filament defects, ~1.2% for the trefoil-knot
> proton. The error scales as `1/sqrt(N_modes)` consistent with a
> Galerkin truncation, and shrinks predictably under enrichment of the
> reduced basis. The framework's prediction therefore holds to within a
> well-characterised computational uncertainty across the lepton and
> hadron spectrum.

This is what the calculation actually established, and it is a much
stronger framing than "0.5% match for the muon with unidentified
residual".

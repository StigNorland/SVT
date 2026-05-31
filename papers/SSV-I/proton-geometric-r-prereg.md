# Proton geometric-R pre-registration

**Date:** 2026-05-30. Written BEFORE running any extraction, so the decision
rule cannot be tuned to the result. Branched off main after PR #67 (cleanup)
merged. Picks up the proton task left open in PR #67 and named explicitly
in `papers/SSV-I/static-3d-closure-status-2026-05-28.md` §2 as one of three
remaining gates for closure: "the geometric derivation of the cutoff
$R = 1.18\,\xi$ that fixes the $F$ scale."

## Background

The SSV-I §Proton gapbox (added in PR #67) records:
$$m_p\,c^2 = N_Y \cdot F \cdot \mu_0$$
with $N_Y \approx 3.007$ (topological, candidate grade) and $F \approx 4.47$
extracted at the canonical cutoff $R \approx 1.18\,\xi$. The cutoff
dependence is steep: $\mathrm{d}\ln F/\mathrm{d}\ln R \approx -0.94$, a 19%
variation between $R = 1.18\,\xi$ and $R = 1.5\,\xi$. The §Proton gapbox
states the only two paths to promote this from calibration to derivation:

  (a) Derive $R$ geometrically from the relaxed breather itself.
  (b) Show $N_Y \cdot F$ is itself cutoff-invariant.

The SSV-I main text says $R = 1.18\,\xi$ is "the inter-strand half-spacing
of the trefoil with minor radius $0.85\,\xi$", suggesting $R$ is meant to
be an emergent geometric property of the relaxed configuration. This
pre-registration tests path (a): extract an emergent geometric $R$ from
each saved state, then check whether using that per-state $R_{\rm geom}$
gives a $N_Y \cdot F$ product that is cross-grid stable.

## What "geometric $R$" will mean

Two candidate definitions, both pre-registered (we report both regardless of
which gives nicer numbers):

  **R_geom_centerline.** The minimum distance between the three vortex
  centerlines of the relaxed trefoil, measured at multiple azimuthal angles
  $\varphi$ around the major ring and averaged. This is the literal
  "inter-strand half-spacing" of the paper's language.

  **R_geom_profile.** The characteristic transverse scale of the density
  profile around a single strand: defined as the radius $r_{1/2}$ at which
  $|\Psi|^2 / \rho_0$ recovers to half its asymptotic-saturation deficit.
  This is the natural scale at which the vortex-core healing meets the
  background.

No additional tuning: $R_{\rm geom}$ is determined per-state by the
extraction algorithms above, with no free parameters.

## States to use

All saved topology-preserving trefoil-breather states under
`papers/SSV-I/data/`. The closure status memo identifies three grid
resolutions that meet the topology-preservation gate at half-width
$6\,\xi$: $n^3 = 24^3, 48^3, 72^3$. The exact files in scope:

  - `penalty-mu400-rho0p01-n24-hw6-1600steps-2026-05-18.npz` (n=24, hw=6)
  - `penalty-best-n48-hw6-800steps-2026-05-19.npz` (n=48, hw=6)
  - `penalty-n72-mu2000-rho0p05-2026-05-19.npz` (n=72, hw=6)

Plus the cross-grid variants `penalty-cross-grid-hw5-2026-05-19.npz` and
`penalty-cross-grid-hw7-2026-05-19.npz` to also vary $hw$ at fixed grid
spacing. If those files don't have the same physical configuration just
at different $hw$, we report this as a limitation; we don't add a parameter
sweep.

## The decision rule, fixed in advance

For each state:
1. Extract $R_{\rm geom\_centerline}$ and $R_{\rm geom\_profile}$ from
   the saved 3D field.
2. Compute $F(R_{\rm geom})$ using the existing
   `trefoil_breather_observables.extract(...)` with
   `straight_vortex_r_max = R_{\rm geom}`.
3. Compute $N_Y(R_{\rm geom})$ from the same extraction
   (`s.n_y_straight`).
4. Compute the product $(N_Y \cdot F)(R_{\rm geom})$ from
   `s.n_y_times_f_straight` (this is the structural quantity that gives
   $m_p / \mu_0$).

Across the three grid resolutions:

  **PASS (geometric $R$ rescues cutoff invariance)** iff:
  - $R_{\rm geom}$ itself converges across grids to within 5% (i.e. the
    geometric definition is itself a stable observable of the breather),
    AND
  - $(N_Y \cdot F)(R_{\rm geom})$ agrees across grids to within 3% (a
    meaningful improvement on the existing 6% spread at the imposed
    $R = 1.18\,\xi$).

  **FAIL (geometric $R$ does not rescue)** iff:
  - $R_{\rm geom}$ does not converge across grids (spread > 10%), OR
  - $(N_Y \cdot F)(R_{\rm geom})$ has spread > 10% across grids.

  **AMBIGUOUS (modest improvement, not decisive)** otherwise: any case
  where the spread is in 3-10% and falls short of PASS but doesn't trigger
  FAIL. Report and propose follow-ups; do not pick a narrative.

If two definitions of $R_{\rm geom}$ give different verdicts, that itself
is informative and gets reported as a finding.

## What this does NOT settle

- The cross-grid $N_Y$ sweep flagged in `static-3d-closure-status-2026-05-28.md`
  as task (i): the dedicated $N_Y$ sweep at $n^3 \in \{48, 72, 96\}$ at a
  single penalty configuration was never run; we work with what's saved.
- The "recovered from non-trefoil initial conditions" gate (task iii in
  the closure status memo). Out of scope.
- The $N_Y$ value's own candidate status (it's still $\sim 3.007$ from the
  topological argument plus reproduction at a single grid family).
- Whether the resulting $m_p$ matches CODATA at sub-percent. We're testing
  cutoff invariance, not absolute agreement.

## Outcome commitment

Whatever the extraction reveals goes into the result note verbatim, with
the per-state per-definition $R_{\rm geom}$ values, the $N_Y \cdot F$ table,
and the PASS/FAIL/AMBIGUOUS verdict applied without adjustment. If PASS, the
SSV-I §Proton gapbox can be revised to drop "cutoff-dependent calibration"
in favour of "cutoff fixed by the emergent geometry $R_{\rm geom\_def}$";
the proton-mass agreement is then promoted from candidate to derived. If
FAIL, the SSV-I §Proton gapbox stands as written and the next step under
the closure status memo would be path (b) (showing $N_Y \cdot F$ is itself
cutoff-invariant, which the same memo notes was already "falsified" by
prior runs in `static-3d-closure-runs-findings-2026-05-28.md`).

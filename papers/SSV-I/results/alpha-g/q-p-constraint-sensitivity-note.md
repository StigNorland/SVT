# `Q_p` Constraint Sensitivity Note

This note records the first direct branch-sensitivity test using the same saved trefoil states as common starting points.

Artifacts:

- `papers/SSV-I/data/q-p-constraint-sensitivity-2026-05-17.json`
- `papers/SSV-I/data/q-p-constraint-topology-sensitivity-2026-05-17.json`

Inputs:

- `trefoil-state-n48-hw7-400steps-2026-05-06.npz`
- `trefoil-state-n64-hw8-400steps-2026-05-17.npz`

For each state, two `+100` continuation branches were run:

- constrained: interior `L2`-norm-conserving continuation
- unconstrained: same relaxer, same step schedule, but without the `L2` constraint

## Main Result

The constraint choice alone changes the gravity-facing source by about `45%` from the same starting state.

For `half_width = 7`:

- constrained: `delta V_p ~ 61.52`, `Q_p^eff ~ 60.69`
- unconstrained: `delta V_p ~ 32.97`, `Q_p^eff ~ 32.50`
- relative difference in `Q_p^eff`: about `0.464`

For `half_width = 8`:

- constrained: `delta V_p ~ 249.69`, `Q_p^eff ~ 244.42`
- unconstrained: `delta V_p ~ 138.20`, `Q_p^eff ~ 135.43`
- relative difference in `Q_p^eff`: about `0.446`

So the branch-selection effect is not a small correction. It is one of the dominant influences on the extracted source.

## Topology Retention Result

The topology-facing extension of the same test adds an equally important negative result.

For both `half_width = 7` and `half_width = 8`, after the `+100` continuation:

- constrained: `topology_mean_winding = 0.0`, `topology_unit_fraction = 0.0`
- unconstrained: `topology_mean_winding = 0.0`, `topology_unit_fraction = 0.0`

So the constraint choice changes the gravity-facing source strongly, but it does **not** rescue the local unit winding structure. By the time these source branches are being compared, both variants have already lost the topology-facing feature the Paper I proton text appears to rely on.

## Interior Curve Sensitivity

The same conclusion appears in the interior cumulative samples.

For `half_width = 7`:

- at `r = 4`: constrained `~ 15.85`, unconstrained `~ 11.58`
- at `r = 6`: constrained `~ 38.51`, unconstrained `~ 24.07`
- at `r = 8`: constrained `~ 57.41`, unconstrained `~ 31.88`

For `half_width = 8`:

- at `r = 4`: constrained `~ 49.34`, unconstrained `~ 39.90`
- at `r = 6`: constrained `~ 110.99`, unconstrained `~ 77.05`
- at `r = 8`: constrained `~ 196.12`, unconstrained `~ 119.27`

The normalized cumulative fractions also shift:

- unconstrained branches put a larger fraction of their smaller total source inside a given radius
- constrained branches preserve a much larger total source and maintain a stronger extended contribution

So the current static source family is genuinely constraint-sensitive, not just normalization-sensitive.

## Interpretation

This is the strongest shortcut-sensitivity result in the repo so far.

Earlier probes showed that:

- the halo is real
- the source settles before the boundary blend layer
- the interior cumulative curves disagree across `half_width`

This new check shows that the global interior `L2` constraint is itself a major branch selector for source strength, but not a topology-preserving closure rule.

That means the next closure question is not only "what radius cutoff should be used?" It is also:

- is global interior `L2` conservation the right physical constraint for a proton breather?

At present, the answer is still open. What is no longer open is that both current variants are inadequate as topology-faithful proton branches.

## Consequence

The next best sensitivity test should now move one level earlier than source comparison:

- compare global `L2` conservation against a more local or geometry-tied conserved measure
- reject branch variants that do not retain local winding around the seeded trefoil centerline
- only then re-run the interior cumulative-curve comparison and gravity-facing source extraction

That is the cleanest way to test whether the current halo-heavy branch is a physical feature or a consequence of the present continuation manifold.

# Topology Winding Check Note

This note records the first topology-facing diagnostic added to the static trefoil prototype.

## Added Diagnostic

[trefoil_breather_static.py](../../src/paper_i/trefoil_breather_static.py) now measures local winding retention around the seeded trefoil centerline.

For a small set of sample locations along the trefoil curve, the script:

- constructs a small loop in the local normal-binormal plane
- samples the complex field on that loop
- unwraps the phase
- measures the circulation winding number

This is not a full knot invariant. It is a first check that the solver still carries the unit filament winding the Paper I proton picture relies on.

## Test Artifacts

- plateaued constrained state check:
  [trefoil-topology-check-hw7-2026-05-17.json](../../papers/SSV-I/data/trefoil-topology-check-hw7-2026-05-17.json)
- near-initial-state check:
  [trefoil-topology-check-initial-like-2026-05-17.json](../../papers/SSV-I/data/trefoil-topology-check-initial-like-2026-05-17.json)

## Result

The result is striking.

For the near-initial state:

- `topology_mean_winding = 0.833`
- `topology_unit_fraction = 0.833`
- `topology_max_winding = 1.0`

So the seeded prototype does mostly carry the intended unit winding around the filament.

For the plateaued constrained `half_width = 7` state:

- `topology_mean_winding = 0.0`
- `topology_unit_fraction = 0.0`

So the current relaxation path reaches a state with gravity-facing source observables that look numerically stable, but without retaining the local winding structure that the Paper I proton story appears to require.

## Interpretation

This does not by itself prove the final relaxed object is unphysical. The present prototype is still a simplified single-filament trefoil background rather than the full trefoil `Y`-junction solver.

But it does prove something important:

- the current static branch can look numerically well-behaved while erasing the topology-facing feature the source text leans on
- therefore topology preservation must become a first-class acceptance criterion, not an optional side diagnostic
- the current global interior `L2` constraint is not enough, because it can stabilize a source branch without preserving the intended branch winding

## Consequence

The next branch-selection tests should compare:

- unconstrained flow
- current global `L2`-constrained flow
- future topology-aware closure conditions

and they should reject branches that lose the local winding structure, even if their residual and source observables look cleaner.

# Trefoil Far-Field Comparison Note

This note records the first box-size comparison of saved radial far-field profiles for the static trefoil prototype.

Artifacts:

- smaller-box profile: [papers/SSV-I/data/example-trefoil-farfield-profile.json](../../papers/SSV-I/data/example-trefoil-farfield-profile.json)
- larger-box profile: [papers/SSV-I/data/example-trefoil-farfield-profile-hw6.json](../../papers/SSV-I/data/example-trefoil-farfield-profile-hw6.json)
- comparison: [papers/SSV-I/data/example-trefoil-farfield-compare-hw5-vs-hw6.json](../../papers/SSV-I/data/example-trefoil-farfield-compare-hw5-vs-hw6.json)

Command used:

```bash
python src/paper_i/trefoil_farfield_compare.py \
  papers/SSV-I/data/example-trefoil-farfield-profile.json \
  papers/SSV-I/data/example-trefoil-farfield-profile-hw6.json \
  --output papers/SSV-I/data/example-trefoil-farfield-compare-hw5-vs-hw6.json
```

## Comparison Rule

The comparison is done by matching bin index and normalised radial position, not by requiring the two profiles to live on the same absolute radius grid.

That is the right choice for box-size studies:

- absolute radii differ because the boxes differ
- relative radial position is what lets us compare the shape of the recovery curve

## Main Readout

From the saved comparison:

- max absolute density difference: about `0.181`
- mean absolute density difference: about `0.052`
- max absolute deficit difference: about `0.181`
- mean absolute deficit difference: about `0.052`

## Interpretation

Three things stand out.

1. The outermost bins are stable.
   The last bins are effectively identical and anchored to density `1`, which is reassuring for the boundary treatment.

2. The mid-to-outer shells still move materially with box size.
   The largest density differences occur in the recovery region rather than at the very centre or the very edge.

3. The box-size effect is now visible in a more physical way than a single scalar can show.
   The scalar shell-density summary said box size mattered; the radial comparison shows where it matters.

## What This Means For #13

This comparison strengthens the current interpretation of the static branch:

- the prototype is numerically healthier than before
- resolution sensitivity is improving
- box-size sensitivity is still one of the main open issues

## Best Next Step

The most useful continuation is a larger far-field sweep that keeps `n` fixed and varies only box size, so the recovery profile can be tracked more cleanly without mixing resolution and domain effects.

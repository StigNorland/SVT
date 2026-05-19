# Trefoil Far-Field Profile Note

This note records the first saved radial far-field profile for the static trefoil prototype.

Artifacts:

- state: [papers/SSV-I/data/example-trefoil-state.npz](papers/SSV-I/data/example-trefoil-state.npz)
- profile: [papers/SSV-I/data/example-trefoil-farfield-profile.json](papers/SSV-I/data/example-trefoil-farfield-profile.json)

Commands used:

```bash
python src/paper_i/trefoil_breather_static.py \
  --n 20 \
  --half-width 5 \
  --max-steps 20 \
  --step-size 0.005 \
  --save-state papers/SSV-I/data/example-trefoil-state.npz

python src/paper_i/trefoil_farfield_profile.py \
  papers/SSV-I/data/example-trefoil-state.npz \
  --bins 12 \
  --output papers/SSV-I/data/example-trefoil-farfield-profile.json
```

## What The Profile Shows

The radial shell averages show the expected qualitative recovery toward the background state:

- inner-to-mid shells carry a large density deficit
- outer shells recover steadily toward density `1`
- the last few bins are effectively anchored to the background

This is still a prototype state, so the profile should not be interpreted as a final physical prediction. But it is already more informative than a single outer-shell average.

## Why This Matters

For the static branch, the important transition is:

- from one-number summaries of the outer region
- to a radial picture of how the density deficit decays

That radial picture is what later gravity-proxy work will need.

## Current Use

At this stage the radial profile is best used for:

1. checking whether outer density recovery is qualitatively sensible
2. comparing box-size effects
3. deciding which far-field scalar summaries are worth trusting

## Best Next Step

Compare profiles across two saved box sizes using the new comparison tool before promoting any outer-region quantity into an `\alpha_G`-facing proxy.

# Paper I Numerical Prototype Summary

The Paper I codebase tests the foundational SSV particle picture:

- stable vortex-core profiles in the logarithmic Schrodinger equation,
- a toroidal electron background with major radius `R_e = xi / alpha`,
- reduced collective-coordinate routes toward the muon mode,
- chiral/Kelvin coupling diagnostics that motivate the transverse sector.

## Main Takeaways

1. The planar LogSE vortex profile is numerically well-defined and reusable as the local core profile for a toroidal defect.
2. A leading toroidal ansatz `Psi_0 = f_0(s/xi) exp(i vartheta)` gives a concrete background for projection integrals.
3. The planar amplitude channel alone does not produce the muon as a simple bound breathing mode; toroidal geometry and chiral transverse coupling are required.
4. The reduced BdG and Kelvin/chiral scripts are exploratory tools for identifying which finite-dimensional truncations carry the right mode structure.

## Reproduction Commands

From the repository root:

```bash
python src/paper_i/vortex_profile.py --n 400 --x-max 12
python src/paper_i/muon_mode_prototype.py
python src/paper_i/kelvin_self_induction.py --phi-n 64
```

For heavier projection checks, use the lower grid sizes first:

```bash
python src/paper_i/restricted_bdg_matrix.py --n 21 --profile numerical --profile-n 400
python src/paper_i/chiral_bridge_projection.py --n 11 --profile-n 400
```

## Interpretation

These results should be cited in Paper I as evidence that the mathematical program is computationally well-posed. They should not be overclaimed as final high-precision predictions for the muon mass.

## Smoke Results

Curated smoke-test output is stored in:

```text
papers/SSV-I/data/smoke-results.csv
```

The first saved static-trefoil refinement checkpoint is recorded in:

```text
papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06.json
papers/SSV-I/trefoil-refinement-checkpoint.md
```

The improved-controller checkpoint is recorded in:

```text
papers/SSV-I/data/trefoil-refinement-checkpoint-2026-05-06b.json
papers/SSV-I/trefoil-refinement-checkpoint-2.md
```

The first far-field-enabled checkpoint is recorded in:

```text
papers/SSV-I/data/trefoil-refinement-farfield-checkpoint-2026-05-06.json
papers/SSV-I/trefoil-farfield-checkpoint.md
```

The first box-size radial-profile comparison is recorded in:

```text
papers/SSV-I/data/example-trefoil-farfield-compare-hw5-vs-hw6.json
papers/SSV-I/trefoil-farfield-compare-note.md
```

The first fixed-resolution box-size sweep is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n24-2026-05-06.json
papers/SSV-I/trefoil-boxsize-sweep-note.md
```

The longer soft-boundary box-size sweep is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-60steps-2026-05-06.json
papers/SSV-I/trefoil-boxsize-sweep-softbc-60steps-note.md
```

The `100`-step soft-boundary box-size sweep is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-100steps-2026-05-06.json
papers/SSV-I/trefoil-boxsize-sweep-softbc-100steps-note.md
```

The direct `60`-vs-`100` step comparison is recorded in:

```text
papers/SSV-I/trefoil-boxsize-sweep-softbc-60-vs-100-note.md
```

The longer `150`/`200` step runs and the doubled-resolution `n = 48` check are recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-150steps-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-100steps-2026-05-06.json
papers/SSV-I/trefoil-longrun-and-resolution-note.md
```

The first scaled-control rerun of the doubled-resolution branch is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-100steps-scaled-2026-05-06.json
papers/SSV-I/trefoil-n48-scaled-control-note.md
```

The longer scaled `n = 48` follow-up, including the `400`-step checkpoint, is recorded in:

```text
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-150steps-scaled-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-200steps-scaled-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-scaled-2026-05-06.json
papers/SSV-I/trefoil-n48-400steps-note.md
```

The direct matched-resolution comparison between the `n = 24` and `n = 48` branches is recorded in:

```text
papers/SSV-I/trefoil-matched-resolution-comparison-note.md
```

The first gravity-branch bridge note is recorded in:

```text
papers/SSV-I/alpha-g-proxy-note.md
papers/SSV-I/data/alpha-g-proxy-checkpoint-2026-05-06.json
papers/SSV-I/alpha-g-mapping-note.md
papers/SSV-I/cq-geometry-note.md
papers/SSV-I/data/cq-geometry-compare-2026-05-06.json
papers/SSV-I/cq-geometry-sweep-note.md
papers/SSV-I/data/trefoil-boxsize-sweep-n24-softbc-200steps-geom-2026-05-06.json
papers/SSV-I/data/trefoil-boxsize-sweep-n48-softbc-400steps-geom-2026-05-06.json
papers/SSV-I/q-p-two-factor-probe-note.md
papers/SSV-I/data/q-p-two-factor-probe-2026-05-06.json
papers/SSV-I/q-p-two-factor-scan-note.md
papers/SSV-I/data/q-p-two-factor-scan-2026-05-06.json
papers/SSV-I/q-p-two-factor-normalized-scan-note.md
papers/SSV-I/data/q-p-two-factor-normalized-scan-2026-05-06.json
```

Representative values:

| check | quantity | value |
|---|---:|---:|
| vortex profile | slope | 1.140313646074 |
| vortex profile | f(1) | 0.735813385965 |
| muon ladder | prediction | 105.037877466 MeV |
| muon ladder | observed | 105.6583755 MeV |
| Kelvin self-induction | omega first-order | 9.2889e-05 |

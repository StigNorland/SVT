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

Representative values:

| check | quantity | value |
|---|---:|---:|
| vortex profile | slope | 1.140313646074 |
| vortex profile | f(1) | 0.735813385965 |
| muon ladder | prediction | 105.037877466 MeV |
| muon ladder | observed | 105.6583755 MeV |
| Kelvin self-induction | omega first-order | 9.2889e-05 |

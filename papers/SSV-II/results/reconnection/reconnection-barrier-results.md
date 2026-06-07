# Paper II Reconnection-Barrier Numerical Supplement

This note records the current 3D LogSE/GPE reconnection-barrier checks for Paper II.

## Code

The reproducible supplement script is:

```bash
python instruments/paper_ii_reconnection_supplement.py --lambda-perp 0 --lambda-perp 1 --lambda-perp 10 --lambda-perp 100 --output papers/SSV-II/data/example_sweep.csv
```

It generates opposite-topology and same-topology vortex-ring reconnection paths, evolves them with a split-step LogSE/GPE solver, includes the chiral-shear stiffness as a spectral `lambda_perp * k^4` term, and extracts:

- effective depleted-cap radius `R_cap`,
- projected-Hessian amplitude/phase channel weight `cos_phi`.

## Main Numerical Findings

The spectral chiral term is geometrically active: increasing `lambda_perp` inflates the effective cap scale. This fixed the earlier inert-geometry failure of force-like chiral implementations.

On the current coarse grids, however, the golden-ratio cap relation is not confirmed. The ratio `R_cap(opposite)/R_cap(same)` is not monotone and does not converge cleanly to `phi = 1.618`.

Run A, `n=64`, `length=40`, constant core:

| lambda | R_cap opposite | R_cap same | opposite/same |
|---:|---:|---:|---:|
| 1 | 3.526 | 3.203 | 1.101 |
| 10 | 8.745 | 18.135 | 0.482 |
| 100 | 27.211 | 35.665 | 0.763 |
| 2000 | 47.558 | 36.679 | 1.297 |

The `cos_phi` extraction is structurally sensitive to topology and chiral stiffness. On `n=32`, the same/opposite ratio descended toward the Weinberg reference through `lambda=100`, but inverted at `lambda=2000`, which is interpreted as a finite-size artifact.

Run B, `n=32`, constant core:

| lambda | cos_phi opposite | cos_phi same | same/opposite |
|---:|---:|---:|---:|
| 0 | 0.953 | 0.943 | 0.990 |
| 1 | 0.823 | 0.762 | 0.926 |
| 10 | 0.802 | 0.735 | 0.917 |
| 100 | 0.680 | 0.594 | 0.874 |
| 2000 | 0.709 | 0.757 | 1.068 |

The `lambda=100` value, `same/opposite = 0.874`, is close to `cos(theta_W) = 0.8769`, but the `lambda=2000` inversion and disagreement with larger-grid behavior mean this should be presented as suggestive only, not as a confirmed Weinberg-angle derivation.

## Physical-Ratio Stress Test

A targeted stress test used `n=64`, `length=40`, `R_ring=12`, `core=12/137`, `lambda=100`. The core is below the grid spacing, so this tests topological channel separation rather than a resolved physical vortex core.

Radial-slice extraction:

| channel | R_cap | cos_phi |
|---|---:|---:|
| opposite | 27.842 | 0.6669 |
| same | 23.836 | 0.6476 |

Derived ratios:

- `R_cap(opposite)/R_cap(same) = 1.168`
- `cos_phi(same)/cos_phi(opposite) = 0.971`

The ordering is physically sensible, but the separation is small because the core is unresolved.

## Scale-Separation Conclusion

The physical SSV hierarchy is approximately:

```text
xi : xi/alpha : xi/alpha^2 = 1 : 137 : 18769
```

Resolving a box large enough to contain `R_ring ~ xi/alpha` while also resolving the core at `dx << xi` requires thousands of cells per side. A direct physical-scale 3D simulation is therefore a petascale calculation, not a desktop calculation.

For Paper II, the numerical result should be framed conservatively:

- The code verifies that reconnection saddles exist.
- Topology changes the amplitude/phase channel structure.
- Spectral chiral stiffness inflates cap-scale geometry.
- The direct physical-scale golden-ratio cap relation remains an analytic conjecture requiring either multiscale reduction or petascale simulation for direct numerical confirmation.

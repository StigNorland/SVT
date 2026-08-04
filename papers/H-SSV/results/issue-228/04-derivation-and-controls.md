# Issue #228 — derivation and executable controls

Status: **complete**

## Candidate results

| candidate | invariant redshift | time stretch | optical area/duality | outcome |
|---|---:|---:|---:|---|
| R0 lapse only | no (`1+z=1`) | no | no | removable coordinate lapse |
| R1 energy-only | conditional | `1` | `eta=y^-3/2` | fails transient clock |
| R2 coherent temporal dilation | conditional | `y` | `eta=y^-1` | requires spatial completion |
| R3 optical/spatial completion | `y=S_o/S_e` | `y` | `eta=1` | wake/geometry rank one |
| R4 information-area expansion | `y=sqrt(N_o/N_e)` | `y` | metric form | record/area dynamics underived; pure deceleration sign challenged |

Here `y=1+z` and `eta=D_L/(y^2D_A)`. The respective bolometric
surface-brightness exponents for R1, R2, and metric R3/R4 are `-1`, `-2`, and
`-4`.

## Machine controls

The focused instrument verifies:

- arbitrary positive lapse endpoints leave the lapse-only redshift at zero;
- at `y=2`, R1 has duration factor one and `eta=2^-3/2`;
- at `y=2`, R2 has duration factor two, a normalized packet, and `eta=1/2`;
- a scalar photon/screen energy transfer closes numerically while correctly
  refusing to mark the interaction Hamiltonian as derived;
- metric `B_o/B_e` fixes redshift independently of lapse endpoints;
- `B W` is invariant under reciprocal functional redefinitions and the
  geometry/wake Jacobian has rank one for two components;
- redshift drift is unchanged under decompositions with the same effective
  endpoint rates;
- R4 gives `q=1` for constant record production, coasting for `N proportional
  t^2`, and acceleration only for growth faster than `t^2`.

The dimensional control also distinguishes `u c`, an energy flux, from an
update rate. Although `sqrt(G u/c^2)` has rate dimensions, dimensional
availability neither establishes a physical law nor fixes a coefficient.

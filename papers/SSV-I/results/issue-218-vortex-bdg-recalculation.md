# Issue #218 — corrected vortex/BdG dependency and recalculation record

Status: **focused recalculation complete**. No new 3D relaxation was run.

Parent: issue #216. The fixed convention is
\[
c_s^2=b=c^2,\qquad
\xi=\frac{\hbar}{\sqrt2\,m_0c},\qquad
\omega^2=c^2k^2\left(1+\frac{\xi^2k^2}{2}\right).
\]

## Dependency audit

The coefficient-two `vortex_profile.py` is a direct dependency of the
following active Paper I instruments:

| direct consumer | downstream role | #218 classification |
|---|---|---|
| `vortex_ring_core_constant.py` | smooth-core Lamb constant and route-D control | exact scale transformation plus focused recomputation |
| `trefoil_breather_observables.py` | straight-vortex denominator in \(F\) and \(N_YF\) | recompute denominator; saved trefoil state is not regenerated merely for this dependency |
| `static_closure_self_consistent_r.py` | half-density cutoff \(R_{\rm sc}\) | exact scale transformation plus focused recomputation |
| `peierls_nabarro_test.py` | lattice translation-barrier control | corrected profile required; energy functional already uses log pressure \(1/2\) |
| `toroidal_projection_integrals.py` | reduced stiffness/norm blocks | operator repair and recomputation required |
| `restricted_bdg_matrix.py` | two-mode projected diagnostic | transitive operator-dependent recomputation |
| `direct_bdg_projection.py` | direct \(L/M\) projection | operator repair and recomputation required |
| `vortex_core_mode_spectrum.py` | straight-core BdG spectrum | operator repair and recomputation required |
| `curved_torus_relaxation.py` | reduced curvature relaxation | coordinate/energy normalization repair required |
| `thin_ring_alpha_correction.py` | finite-\(\alpha\) bridge diagnostic | transitive profile/projection recomputation |

Active transitive consumers include `restricted_bdg_three_mode.py`,
`kelvin_augmented_bdg.py`, `chiral_bridge_projection.py`,
`path_b_spectrum_probe.py`, the issue-72/73 and stage-1/2/3 probes,
`proton_gate_iii_probe.py`, `proton_geometric_r_probe.py`,
`f_vs_r_cutoff_scan.py`, and the static-closure/cutoff sweeps. Fitted
quarantine consumers remain quarantined and are not rerun.

Five Paper II instruments also import the legacy profile. They are recorded as
a cross-paper consequence, not silently changed under this Paper I issue.

## Exact scale relation

Let \(f_2(y)\) solve the legacy equation
\[
f_2''+\frac{f_2'}y-\frac{f_2}{y^2}-2f_2\ln(f_2^2)=0.
\]
Then
\[
f_1(x)=f_2(x/\sqrt2)
\]
solves the corrected conventional-healing-length equation
\[
f_1''+\frac{f_1'}x-\frac{f_1}{x^2}-f_1\ln(f_1^2)=0.
\]
The issue #218 solver integrates both equations independently; the rescaling
identity is a numerical control, not an assumed implementation.

For the asymptotic straight-vortex constant
\[
A=\lim_{R\to\infty}\left[\int_0^R\frac{f^2(r)}r\,dr-\ln R\right],
\qquad C=2-A,
\]
the coordinate change predicts
\[
A_1=A_2-\ln\sqrt2,\qquad C_1=C_2+\ln\sqrt2.
\]

## Additional operator defects exposed by the dependency audit

The recalculation is not reducible to swapping profiles:

1. `toroidal_projection_integrals.py` uses
   `v_second = -b/rho`. The stable action has
   \(V''(\rho)=+b/\rho\).
2. `direct_bdg_projection.py` and `vortex_core_mode_spectrum.py` use a
   coefficient-two profile with a mixed operator normalization. In
   \(x=r/\xi\) and \(\omega_c=m_0c^2/\hbar\) units, the corrected blocks are
   \[
   L=-\nabla_x^2+\ln(f_1^2)+1,\qquad M=e^{2i\theta}.
   \]
3. The toroidal geometry fixes \(R_e/\xi=1/\alpha\). A coordinate rescaling of
   the core without consistently restoring this ratio changes the physical
   background, so toroidal eigenvalues are not declared invariant by the
   planar identity alone.

These findings make the prior scalar and reduced numerical frequencies
results for their implemented legacy operators. Each current-physics use must
be recomputed or remain explicitly open.

## Corrected profile and core constant

Independent coefficient-one shooting gives

| observable | historical coefficient two | corrected coefficient one |
|---|---:|---:|
| origin slope \(f'(0)\) | 1.140688 | 0.806588 |
| half-density radius \(R_{\rm sc}/\xi\) | 0.923141 | 1.305516 |
| ring core constant \(C\) | 1.879670 | 2.226289 |

The half-density-radius ratio is \(1.414211\). The independently integrated
core constant differs from the exact transformed value
\(C_2+\ln\sqrt2\) by \(4.6\times10^{-5}\).

The lepton route-D fit remains negative: the best-fit generation ratio is
\(q=8.58682\), independent of \(C\), while the fitted radius moves to
\(R_e/\xi=1.27127\). The fixed \(R/\xi=(1,8,64)\) control is no longer
admissible because its \(R=\xi\) reference has \(\ln8-C<0\).

## Saved-state proton recalculation

The saved trefoil fields and their energies are unchanged. Only their
straight-vortex calibration was recomputed.

At the paper cutoff \(R=1.18\,\xi\):

| state | \(n\) | corrected \(F\) | corrected \(N_Y\) | \(N_YF\) |
|---|---:|---:|---:|---:|
| penalty-mu400 | 24 | 6.558734 | 55.9591 | 367.021 |
| penalty-best | 48 | 5.298115 | 84.6842 | 448.667 |
| penalty-n72 | 72 | 5.167662 | 82.3353 | 425.481 |

The two fine-grid \(F\) values still differ by \(2.49\%\). With the paper's
\(N_Y=3.007\) and \(E_\star=70.025\) MeV they instead imply
\[
3.007F E_\star=1088\text{--}1116\ {\rm MeV},
\]
which is \(16.0\%\)--\(18.9\%\) above the observed proton mass. The former
near-CODATA band is therefore a normalization artifact, not a surviving
prediction.

For results in which both \(N_Y\) and \(F\) used the same \(R=1.18\,\xi\)
straight-vortex denominator, the tension ratio is
\[
\mu_{\rm legacy}/\mu_{\rm corrected}=1.169958,
\]
so \(F\) scales by \(1.169958\) and \(N_YF\) by \(1.368801\). The issue-77
resolution ladder therefore becomes
\[
N_YF=(71.920,73.659,73.225,74.956)
\]
for \(n=(96,128,160,192)\). Its relative convergence survives, but the
reported anchor is approximately \(74\), not \(54\).

At the corrected self-consistent cutoff \(R_{\rm sc}=1.305516\,\xi\), saved
states give

| state | \(N_Y\) | \(F\) | \(N_YF\) |
|---|---:|---:|---:|
| n24 | 50.1186 | 5.8742 | 294.4 |
| n48 best | 75.8712 | 11.1551 | 846.3 |
| n48, \(\mu=1000\) | 59.7519 | 10.6059 | 633.7 |
| n48, \(\mu=2500\) | 71.3522 | 10.9858 | 783.9 |
| n72 | 73.7725 | 15.6086 | 1151.5 |
| n96 | 108.005 | 23.2092 | 2506.7 |

The \(n\ge48\) spread is \(158.1\%\), so the pre-registered \(<5\%\) closure
gate remains **FAIL** and is strengthened.

## Corrected BdG and reduced-operator checks

The direct profile-matched two-mode projection, without the unrederived chiral
block, gives:

| grid \(n\) | \(\lvert\omega_-\rvert\) | \(\lvert\omega_+\rvert\) |
|---:|---:|---:|
| 21 | 0.86649 | 4.64585 |
| 31 | 0.87762 | 5.02921 |
| 41 | 0.88323 | 5.23776 |

The low branch changes by \(0.64\%\) from \(n=31\) to \(41\); the high branch
still changes by \(4.15\%\). These are restricted-basis diagnostics, not
particle predictions.

The quadrature-Hessian diagnostic gives
\(\omega_-=(1.1307,1.1762,1.1977)\) on the same grids. It remains explicitly
provisional because its chiral-shear normalization has not been independently
rederived. The chiral block is not used to promote any Paper I claim here.

For the straight-core radial BdG solve, the translation partners occur at
\(\omega=\pm0.0133\) for \(L=12\,\xi,n=300\), falling to
\(\lvert\omega\rvert=0.0071\) for \(L=16\,\xi,n=400\). This passes the
finite-box Goldstone control. The audit also removes the old assumption that
axial \(U(1)\) enforces a \(+m/-m\) doublet on a chiral vortex. It does not;
the earlier no-magic-8 verdict survives because \(U(1)\) supplies no
three-fold \(p\)-shell degeneracy.

## Other focused controls

- The corrected \(n=64,128\) Peierls--Nabarro barrier falls
  \(6.98\times10^{-2}\to3.42\times10^{-2}\) when the grid spacing halves.
  The lattice-artifact verdict survives.
- The exact thin-ring angular-parity result remains \(\pi/4\), with all tested
  \(O(\alpha)\) angular projections vanishing.
- A small \(n=21\) curved-background relaxation lowered the reduced energy by
  \(1.42\times10^{-4}\) fractionally but retained gradient norm \(3.55\).
  It is recorded only as a non-converged diagnostic.

## Focused validation

The controls cover the coefficient distinction, exact coordinate rescaling,
core-constant shift, corrected H7 optimizer domain, BdG kinetic coefficient,
longitudinal Hessian sign, and signed translation Goldstone partner. The
repository-wide calculation-heavy suite is deliberately out of scope.

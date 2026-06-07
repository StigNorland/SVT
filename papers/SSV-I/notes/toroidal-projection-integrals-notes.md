# First Toroidal Projection-Integral Results

> **Status (2026-05-30): superseded by Path B null.** Numerical claims in this note about the muon eigenfrequency reaching $\omega/\omega_c = 0.207$, the $\delta_{\rm relax}$ calibration, the $\alpha$-harmonic ladder identification, or the $1/\sqrt{N_{\rm modes}}$ basis-truncation residual are now governed by `papers/SSV-I/path-b-eigenvalue-result.md`: that test showed the muon agreement is not basis-robust (drifts $\pm 13\%$ across 4 bases, empty window in 2 of 4) and the pion rung is absent in every basis. Structural sub-results that stand on their own (operator algebra, analytic derivations, the cubic-vertex one-loop result, dimensional setup) remain valid in isolation; what is superseded is their use as evidence for the ladder identification or as a closure path to it. Quarantined inputs: `instruments/_fitted_quarantine/`. Tracking: issue #66.

This note records the first numerical projection-integral prototype built on the toroidal
background ansatz.

## 1. Files

- `toroidal_background.py` defines the background field \(\Psi_0\), the breathing seed
  \(\Phi_R\), and the chiral seeds \(\Phi_\chi^{(\cos)}\), \(\Phi_\chi^{(\sin)}\).
- `toroidal_projection_integrals.py` evaluates first stiffness and norm integrals on a 2D
  meridional \((r,z)\) grid using the cylindrical volume element \(2\pi r\,dr\,dz\).

The current code works in natural units:
\[
\xi=\hbar=m_0=\rho_0=c=1,
\qquad
b=\frac12,
\qquad
R_e=\frac{1}{\alpha}.
\]

## 2. Integral definitions implemented

The LogSE Hessian estimate is
\[
K^{(0)}_{ab}
=
\int d^3x
\left[
\frac12 \Re(\nabla\Phi_a^\ast\cdot\nabla\Phi_b)
+\frac12 V''(|\Psi_0|^2)\,\delta\rho_a\delta\rho_b
\right],
\]
with
\[
V''(\rho)=-\frac{b}{\rho}.
\]

The chiral contribution is
\[
K^{(\perp)}_{ab}
=
\lambda
\int d^3x\,
(\nabla\times\delta j_a)\cdot(\nabla\times\delta j_b),
\]
up to the natural-unit prefactor. In axisymmetry the only curl component is
\[
(\nabla\times\delta j)_\varphi
=
\partial_z \delta j_r-\partial_r\delta j_z.
\]

The norm matrix is also computed:
\[
N_{ab}=\int d^3x\,\Re(\Phi_a^\ast\Phi_b).
\]

## 3. Important parity result

The cosine chiral seed is orthogonal to the breathing seed on the symmetric leading torus:
\[
K_{R\chi}^{(\cos)}\approx 0.
\]

The sine chiral seed gives a nonzero coupling:
\[
K_{R\chi}^{(\sin)}\ne 0.
\]

Therefore the first coupled ring-chiral channel to keep is
\[
\Phi_\chi^{(\sin)}
=
i\,g_\chi(\tilde s)\sin\vartheta\,e^{i\vartheta}.
\]

This is a useful correction to the first paper-ready wording, which named the cosine seed as
the most obvious curvature partner. The numerical projection says the sine-parity partner is
the one that actually overlaps with the current breathing seed.

## 4. Representative run

Command:

```powershell
python .\toroidal_projection_integrals.py --n 51 --half-width 5 --chi-parity sin
```

Output summary:

```text
K_RR        = 1.274003596e+06
K_Rchi      = 5.591286930e+04
K_chichi    = 4.217084402e+02
N_RR        = 9.509261022e+07
N_Rchi      = -1.395736859e-09
N_chichi    = 2.581692858e+02
Khat_RR     = 1.339750369e-02
Khat_Rchi   = 3.568503349e-01
Khat_chichi = 1.633457050e+00
```

Here the chiral seed has been Gram-Schmidt orthogonalized against \(\Phi_R\), so
\[
N_{R\chi}\approx 0.
\]

The normalized stiffness coupling remains nonzero:
\[
\hat K_{R\chi}\approx 0.36.
\]

## 5. Interpretation

This is not yet a physical eigenfrequency calculation. It is a projection diagnostic. It shows:

1. the leading toroidal ansatz produces a large geometric breathing stiffness;
2. the cosine chiral seed is parity-forbidden at leading order;
3. the sine chiral seed couples strongly to the breathing mode;
4. the coupling survives Gram-Schmidt removal of direct norm overlap.

The stiffness matrix is not yet guaranteed positive because the background is not a fully relaxed
solution of the full LogSE plus chiral-shear energy. That is expected: the ansatz is a seed, not
the final stationary torus.

## 6. Next step

The previous next step was to replace the toy profile
\[
f_0(\tilde s)=\tanh(\tilde s/\sqrt2)
\]
with a numerical solution of the planar vortex equation from Appendix C:
\[
-\left(\partial_{\tilde s}^2+\frac1{\tilde s}\partial_{\tilde s}-\frac1{\tilde s^2}\right)f_0
-2f_0\ln f_0^2=0,
\]
then rerun the projection integrals. This has now been implemented in `vortex_profile.py` and
enabled with:

```powershell
python .\toroidal_projection_integrals.py --profile numerical
```

## 7. Numerical profile result

The numerical shooting solution uses the sign convention
\[
f_0''+\frac1{\tilde s}f_0'-\frac1{\tilde s^2}f_0-2f_0\ln f_0^2=0,
\]
which gives a monotone \(0\le f_0\le1\) profile and matches the Appendix C checks:

```text
f(1)    ≈ 0.735855
Veff(1) ≈ 1.83407
f(5)    ≈ 0.989555
Veff(5) ≈ 0.08313
```

A representative 4-worker projection run is:

```powershell
python .\toroidal_projection_integrals.py --n 51 --half-width 5 --chi-parity sin --profile numerical --profile-n 2000 --workers 4
```

Output summary:

```text
K_RR        = 2.102488437e+07
K_Rchi      = 4.089024694e+04
K_chichi    = 3.647041245e+02
N_RR        = 1.058653520e+08
N_Rchi      ≈ 0
N_chichi    = 2.159754480e+02
Khat_RR     = 1.986002405e-01
Khat_Rchi   = 2.704211271e-01
Khat_chichi = 1.688636963e+00
```

A denser check with `n=61`, `profile-n=2400` gives:

```text
Khat_RR     = 2.063325238e-01
Khat_Rchi   = 2.645937085e-01
Khat_chichi = 1.770011832e+00
```

So the numerical-profile projection currently suggests a normalized ring-chiral stiffness
coupling of order
\[
\hat K_{R\chi}\sim 0.26\text{--}0.27
\]
in the present natural-unit normalization.

Additional convergence checks:

```text
n=81, half-width=5, profile-n=3000:
Khat_RR     = 2.156692670e-01
Khat_Rchi   = 2.565010272e-01
Khat_chichi = 1.870845006e+00

n=81, half-width=6, profile-n=3000:
Khat_RR     = 1.965547929e-01
Khat_Rchi   = 2.514559764e-01
Khat_chichi = 1.604819539e+00

n=101, half-width=6, profile-n=4000:
Khat_RR     = 2.026955269e-01
Khat_Rchi   = 2.469014501e-01
Khat_chichi = 1.667357305e+00
```

The coupling estimate is therefore converging toward
\[
\hat K_{R\chi}\approx 0.25
\]
for the current leading toroidal ansatz and sine-parity chiral seed. The diagonal chiral term
is more sensitive to domain and resolution, but remains order unity in this normalization.

## 8. Parallel execution

No NumPy/SciPy/joblib/numba installation is available in the current environment. The code
therefore uses Python's standard-library `multiprocessing.Pool` when `--workers` is greater
than one. On Windows this requires permission to create worker-process pipes; inside the
sandbox the worker pool can fail with `PermissionError: [WinError 5] Access is denied`.

Once allowed, the 4-worker run completes and agrees with the sequential result on smaller test
grids.

## 9. Next step

The remaining missing ingredient is the effective mass/norm appropriate to the BdG symplectic
problem, not just the real \(L^2\) norm. The next technical step is to build the projected
generalized BdG matrix
\[
\mathsf H X = \hbar\omega\,\mathsf N X
\]
for the \((\Phi_R,\Phi_\chi^{(\sin)})\) basis, using the numerical \(f_0\), and compare the
resulting two-mode eigenvalues with the target \(\omega_\mu\approx0.207\,\omega_c\).

## 10. Provisional two-mode eigenvalue diagnostic

The real-norm generalized eigenvalue diagnostic is implemented in:

```powershell
python .\projected_two_mode_eigen.py --n 101 --half-width 6 --profile numerical --profile-n 4000 --workers 4
```

It solves
\[
KX=\omega^2NX
\]
using the projected real \(L^2\) norm as \(N\). With the converged projection settings, the raw
matrices are:

```text
K = [[2.341162888e+07, 4.247118029e+04],
     [4.247118029e+04, 4.271521431e+02]]

N = [[1.155014580e+08, ~0],
     [~0,              2.561851271e+02]]
```

The normalized stiffness matrix is:

```text
Khat_RR     = 2.026955269e-01
Khat_Rchi   = 2.469014501e-01
Khat_chichi = 1.667357305e+00
```

The provisional eigenvalues are:

```text
omega_minus = 4.027340346e-01
omega_plus  = 1.306850462e+00
```

Compared with the draft target
\[
\omega_\mu/\omega_c\approx0.207,
\]
the lower real-norm branch is
\[
\frac{\omega_-}{\omega_\mu}\approx1.95.
\]

This should not yet be read as a failed muon prediction, because this matrix uses the ordinary
real \(L^2\) norm. The physical BdG problem uses a first-order symplectic structure and a
\((u,v)\) fluctuation basis. The result does, however, show that the current projected stiffness
scale is not wildly far from the muon target: it is high by a factor of order two in this
provisional normalization.

## 11. Updated next step

Build the actual restricted BdG basis
\[
\Xi_R=(\Phi_R,\Phi_R^\ast)^T,\qquad
\Xi_\chi=(\Phi_\chi,\Phi_\chi^\ast)^T,
\]
then project the BdG operator and symplectic metric:

\[
H_{ab}=\langle \Xi_a,\hat{\mathcal H}_{\rm BdG}\Xi_b\rangle,
\qquad
S_{ab}=\langle \Xi_a,\sigma_3\Xi_b\rangle.
\]

The physical diagnostic is then
\[
HX=\hbar\omega\,SX,
\]
not \(KX=\omega^2NX\). This is the next refinement needed before deciding whether a full 3D
calculation is justified.

## 12. Restricted BdG diagnostic from quadrature Hessians

The first restricted BdG diagnostic is implemented in:

```powershell
python .\restricted_bdg_matrix.py --n 51 --half-width 5 --profile numerical --profile-n 2000
```

This script computes separate normalized Hessians for real-amplitude and phase-quadrature
perturbations:

\[
K_{xx}: \delta\Psi = x_R\Phi_R+x_\chi\Phi_\chi,
\qquad
K_{yy}: \delta\Psi = i y_R\Phi_R+i y_\chi\Phi_\chi.
\]

It then forms the minimal restricted BdG split
\[
A=\frac12(K_{xx}+K_{yy}),\qquad
B=\frac12(K_{xx}-K_{yy}),
\]
and solves the two-mode bosonic BdG diagnostic
\[
\omega^2\in {\rm eig}\left[(A-B)(A+B)\right].
\]

Representative `n=51` result:

```text
Kxx_RR     =  1.986002405e-01
Kxx_Rchi   =  2.704211271e-01
Kxx_chichi =  1.688636963e+00

Kyy_RR     = -5.660986501e-01
Kyy_Rchi   = -1.804743390e-01
Kyy_chichi =  1.552953867e+00

A_RR       = -1.837492048e-01
A_Rchi     =  4.497339405e-02
A_chichi   =  1.620795415e+00

B_RR       =  3.823494453e-01
B_Rchi     =  2.254477331e-01
B_chichi   =  6.784154813e-02

omega_minus_sq = -9.533901947e-02
omega_plus_sq  =  2.507678844e+00
```

The lower branch is non-real in this restricted diagnostic. This should not be interpreted as a
physical instability of the theory. It means the current leading toroidal ansatz is not yet a
stationary solution of the full energy functional. A BdG calculation assumes expansion about a
stationary background; using an unrelaxed ansatz leaves spurious negative curvature in the
phase/ring quadrature.

The result changes the priority:

1. The ring-chiral stiffness overlap is real and robust.
2. But a physical restricted BdG matrix requires a relaxed toroidal background, or at minimum
   an ansatz with its first variations projected out.
3. The next calculation should therefore be torus relaxation in the \((f_0+\alpha f_1\cos\vartheta)\)
   family, not full 3D yet.

## 13. Curved ansatz relaxation

The first curved-family relaxation is implemented in:

```powershell
python .\curved_torus_relaxation.py --n 41 --half-width 5 --profile-n 1600 --finite-diff-step 0.25
```

The ansatz is
\[
\Psi_0^{\rm curved}
=
\left[
f_0(\tilde s)+\alpha f_1(\tilde s)\cos\vartheta
\right]e^{i\vartheta},
\]
with
\[
f_1(\tilde s)=\sum_k c_k\,\tilde s^2 e^{-\tilde s/L_k},
\qquad
L_k\in\{1,2,4\}.
\]

The \(\tilde s^2\) factor keeps the curvature correction regular at the vortex core.

For `n=41`, `half-width=5`, the relaxed coefficients are:

```text
c[0] =  1.311633842587e-01
c[1] = -3.732604652694e-02
c[2] =  6.918555747661e-03
```

The energy decreases only slightly:

```text
E_unrelaxed    = 6.971348174918e+03
E_relaxed      = 6.971346805925e+03
Delta_E        = -1.368992524476e-03
relative_delta = -1.963741431538e-07
```

The projection scripts now accept these coefficients:

```powershell
python .\toroidal_projection_integrals.py --n 41 --half-width 5 --chi-parity sin --profile numerical --profile-n 1600 --curvature-coeffs "0.1311633842587,-0.03732604652694,0.006918555747661"
```

The curved-background projection gives:

```text
Khat_RR     = 1.712008859e-01
Khat_Rchi   = 2.999234242e-01
Khat_chichi = 1.467307942e+00
```

The restricted BdG diagnostic with the same coefficients gives:

```text
omega_minus_sq = -7.099226708e-02
omega_plus_sq  =  1.814720083e+00
```

This is an improvement over the corresponding unrelaxed `n=41` lower branch:

```text
unrelaxed omega_minus_sq ≈ -8.736216302e-02
relaxed   omega_minus_sq ≈ -7.099226708e-02
```

So the curved correction moves the restricted BdG diagnostic in the right direction, but it does
not yet fully stabilize the lower branch. The current three-basis \(f_1\) family is too small, or
the finite-dimensional energy relaxation must also include a phase/flow correction rather than
amplitude curvature alone.

## 14. Joint amplitude plus phase/flow relaxation

The curved relaxation was extended to include a phase/flow correction:

\[
\Psi_0^{\rm curved}
=
\left[
f_0(\tilde s)+\alpha f_1(\tilde s)\cos\vartheta
\right]
\exp\left\{
i\left[\vartheta+\alpha g_1(\tilde s)\sin\vartheta\right]
\right\},
\]

with
\[
g_1(\tilde s)=\sum_k d_k\,\tilde s^2 e^{-\tilde s/L_k}.
\]

The sine angular dependence is the natural reflection-odd flow correction paired with the
reflection-even amplitude correction.

Command:

```powershell
python .\curved_torus_relaxation.py --n 41 --half-width 5 --profile-n 1600 --finite-diff-step 0.25
```

Output coefficients:

```text
amp_coeffs_cli   = 1.20855403928,-0.295774109337,0.063309785463
phase_coeffs_cli = -4.37241166392,0.372671765463,-0.475758295289
```

The energy improvement is much larger than amplitude-only:

```text
E_unrelaxed    = 6.971348174918e+03
E_relaxed      = 6.970376192301e+03
Delta_E        = -9.719826169876e-01
relative_delta = -1.394253439363e-04
```

So the phase/flow correction is definitely part of the stationary torus structure.

However, feeding these coefficients back into the current two-mode projection gives nearly the
same restricted BdG lower branch as the amplitude-only relaxed background:

```text
Khat_RR     = 1.712663020e-01
Khat_Rchi   = 2.996093212e-01
Khat_chichi = 1.465430235e+00

omega_minus_sq = -7.105765236e-02
omega_plus_sq  =  1.811485049e+00
```

The phase/flow correction strongly lowers the static energy, but does not by itself stabilize the
restricted \((\Phi_R,\Phi_\chi)\) BdG diagnostic. This suggests the remaining negative branch is
not just an amplitude/flow curvature defect in the background. More likely, the restricted BdG
basis is missing at least one zero/near-zero stationarity direction, such as:

1. centerline displacement/Kelvin \(m=1\) deformation,
2. a separate phase mode conjugate to \(R\),
3. a change in the ring radius \(R\) itself during relaxation,
4. direct projection of the differential \(L/M\) BdG operator instead of reconstruction from
   quadrature Hessians.

## 15. Inner/outer breathing resistance term

An explicit localized inner/outer breathing-resistance term was added to the projection code as
an optional \(K_{RR}\) contribution:

\[
K^{\rm io}_{RR}
=
\kappa_{\rm io}
\int d^3x\,
\left(1-|\Psi_0|^2\right)^2\cos^2\vartheta.
\]

The factor \((1-|\Psi_0|^2)^2\) localizes the modulus to the vortex core, avoiding a divergent
bulk-vacuum contribution. The \(\cos^2\vartheta\) factor is the lowest even inner/outer strain
shape: the inner and outer sides of the torus have opposite signs of \(\cos\vartheta\), but strain
energy is even.

The term is exposed as:

```powershell
--inner-outer-stiffness <kappa_io>
```

Example:

```powershell
python .\toroidal_projection_integrals.py --n 21 --half-width 4 --profile numerical --profile-n 800 --chi-parity sin --inner-outer-stiffness 1
```

For `kappa_io = 1`, the small-grid diagnostic gives:

```text
Kio_RR  = 1.072694701e+03
Khat_RR = 1.679082522e-01
```

The restricted BdG diagnostic adds this same \(K^{\rm io}_{RR}\) to both amplitude and
phase-quadrature blocks so it behaves as a shared elastic resistance, not as an artificial
particle-hole splitting.

Sweeping the coefficient on a small grid gives:

```text
kappa_io = 0:    omega_minus_sq = -6.654635890e-02
kappa_io = 1:    omega_minus_sq = -6.655285873e-02
kappa_io = 10:   omega_minus_sq = -6.661134361e-02
kappa_io = 100:  omega_minus_sq = -6.719484831e-02
kappa_io = 1000: omega_minus_sq = -7.289563938e-02
```

So this particular localized \(K_{RR}\) resistance is physically sensible and now modelled, but
it does not stabilize the current restricted lower BdG branch. The negative branch is therefore
not simply missing scalar breathing stiffness. The missing piece is more likely canonical:
ring-breathing needs its conjugate flow/momentum mode, or the BdG operator must be projected
directly in a \((u,v)\) basis rather than reconstructed from quadrature Hessians.

## 16. Conjugate flow/momentum mode

A distinct conjugate flow seed was added to `toroidal_background.py`:

\[
\Phi_P
=
i\,p(\tilde s)\cos\vartheta\,\Psi_0,
\qquad
p(\tilde s)=\tilde s e^{-\tilde s}.
\]

This is not the same as \(i\Phi_R\). It is a localized phase/flow deformation with the same
inner/outer angular shape as a major-radius breathing velocity field.

The three-mode diagnostic is implemented in:

```powershell
python .\restricted_bdg_three_mode.py --n 31 --half-width 4 --profile numerical --profile-n 1200
```

For the basis \((R,\chi,P)\), the Hessian blocks show that \(\Phi_P\) is nearly
stiffness-orthogonal to \(\Phi_R\) and \(\Phi_\chi\):

```text
K_xx R-P   ≈ 3.08e-18
K_xx chi-P ≈ 3.77e-17
```

That does not make the mode irrelevant. It means the mode is genuinely canonical. Its main
coupling appears in the first-order symplectic/time-derivative matrix

\[
S_{ij}=2\,{\rm Im}\langle \Phi_i|\Phi_j\rangle.
\]

The normalized symplectic matrix is:

```text
S =
  ~0        ~0        -4.205648407e-01
  ~0        ~0         8.805376511e-01
   4.205648407e-01 -8.805376511e-01 ~0
```

So the new \(P\) mode couples strongly to \(R\) and \(\chi\) through the canonical structure,
not through static stiffness.

The three-mode Hessian-only BdG reconstruction still has non-real lower branches. This is now
expected: an odd-dimensional antisymmetric symplectic matrix is singular. The physical reduced
dynamics should be formulated as

\[
S\dot q=Kq,
\]

or in an even-dimensional canonical basis. The immediate next step is therefore to add the
conjugate partner for \(\chi\) as well, or reduce the \((R,\chi,P)\) system onto the rank-two
symplectic subspace before extracting frequencies.

## 17. Four-mode canonical diagnostic

A fourth canonical seed was added using the phase partner of the chiral mode:

\[
P_\chi \sim i\Phi_\chi.
\]

The four-mode diagnostic is implemented in:

```powershell
python .\canonical_four_mode.py --n 21 --half-width 4 --profile numerical --profile-n 800
```

The basis is

\[
(R,\chi,P_R,P_\chi).
\]

The symplectic matrix is now invertible, so the first-order reduced system can be formed:

\[
S\dot q=Kq,
\qquad
\dot q=S^{-1}Kq.
\]

For the unrelaxed numerical background, the generator eigenvalues are real pairs:

```text
lambda = ±2.043061236e-01
lambda = ±1.322282599e-01
```

For the amplitude-plus-phase relaxed background, using:

```powershell
--curvature-coeffs "1.20855403928,-0.295774109337,0.063309785463"
--phase-coeffs "-4.37241166392,0.372671765463,-0.475758295289"
```

the generator eigenvalues are again real pairs:

```text
lambda = ±1.337376619e-01
lambda = ±1.422529513e-01
```

For a stable oscillator these eigenvalues should be imaginary pairs \(\lambda=\pm i\omega\).
Real pairs indicate saddle directions in the current reduced stiffness matrix. The conjugate
partner therefore fixes the odd-dimensional symplectic problem, but it has not yet produced a
stable muon-like oscillator.

The next likely bottleneck is the projected stiffness itself: the \(P_\chi\) phase-partner block
contains a negative curvature in the current Hessian reconstruction. This points again toward
direct projection of the differential BdG \(L/M\) operator, or a larger relaxation basis that
removes the remaining saddle before frequency extraction.

## 18. Direct restricted BdG \(L/M\) projection

A direct \(L/M\)-block projection was added in:

```powershell
python .\direct_bdg_projection.py --n 31 --half-width 4 --profile numerical --profile-n 1200
```

Unlike the quadrature-Hessian reconstruction, this script directly assembles a restricted BdG
matrix of the form

\[
\begin{pmatrix}
L & M\\
-M^\ast & -L^\ast
\end{pmatrix}
\]

on the restricted \((R,\chi)\) basis.

The current implementation uses a finite-difference cylindrical Laplacian and an approximate
LogSE local curvature model:

\[
L\phi\simeq -\frac12\nabla^2\phi+2(1-|\Psi_0|^2)\phi,
\]

\[
M\phi\simeq -2(1-|\Psi_0|^2)e^{2i\Theta}\phi.
\]

This is not yet the final analytic LogSE \(L/M\) operator, but it is a direct operator projection
rather than a reconstruction from separate real/phase Hessians.

Small-grid result:

```text
n=21:
eigenvalues = ±1.023439071, ±3.352100178

n=31:
eigenvalues = ±1.065591163, ±3.769735612
```

This is qualitatively better than the Hessian-reconstructed restricted BdG diagnostic: the
eigenvalues are real particle-hole pairs instead of non-real saddle branches. However, the
lowest restricted positive eigenvalue is still of order unity in the present normalization, not
near the muon target \(\omega_\mu/\omega_c\approx0.207\).

The next improvements are:

1. derive and implement the exact LogSE \(L/M\) local coefficients instead of the provisional
   \(2(1-|\Psi_0|^2)\) model;
2. add the chiral-shear operator contribution directly to \(L/M\), not only as an energy
   correction;
3. extend the projected basis beyond \((R,\chi)\), probably including \(P_R,P_\chi\) as genuine
   \(u/v\) basis directions rather than only canonical diagnostics.

## 19. Ordered direct-BdG refinements

The direct BdG script now supports:

```powershell
--operator-model profile-logse
--include-projected-chiral
--basis two|four
```

The `profile-logse` operator is derived from the same stationary equation solved by the
numerical profile:

\[
-\frac12\nabla^2\Psi+\log(|\Psi|^2)\Psi=0.
\]

Thus, for \(g(n)=\log n\),

\[
L\phi=-\frac12\nabla^2\phi+\left[\log n+1\right]\phi,
\qquad
M\phi=e^{2i\Theta}\phi.
\]

This replaces the provisional local model. On the same small grid:

```text
provisional lowest positive eigenvalue: 1.023439071
profile-logse lowest positive eigenvalue: 0.849373721
```

At `n=31`, `profile-logse` gives:

```text
lowest positive eigenvalue: 0.863367405
```

Adding the projected chiral-shear Hessian to the \(L\) block changes the spectrum only very
slightly at the natural \(\lambda=\alpha^2\):

```text
without projected chiral: 0.863367405
with projected chiral:    0.863421548
```

Extending the direct \(u/v\) basis to four modes,

\[
(R,\chi,P_R,P_\chi),
\]

produces near-zero symmetry/canonical modes and the lowest nonzero positive branch:

```text
n=21, basis=four:
eigenvalues ≈ 0, 0, ±0.922372600, ±1.317743829, ±4.039763520
```

With projected chiral included:

```text
n=21, basis=four:
eigenvalues ≈ ±9.3e-6, ±0.922391620, ±1.317783309, ±4.039803394
```

So the ordered refinements improved the restricted direct-BdG calculation and removed the
earlier saddle artifacts, but the lowest nonzero branch is still well above the muon target
\(\omega_\mu/\omega_c\approx0.207\). The remaining missing effect is not a small perturbative
chiral stiffness at \(\lambda=\alpha^2\); it must be either a stronger nonlocal chiral operator,
a better relaxed toroidal background, or a larger basis containing actual ring-shape/Kelvin
degrees of freedom.

## 20. Minimal Kelvin \(m_\varphi=\pm1\) seed extension

The direct BdG projection was extended with azimuthal mode labels in:

```powershell
python .\kelvin_augmented_bdg.py --n 21 --half-width 4 --profile numerical --profile-n 800 --core-basis four
```

The Kelvin seeds are

\[
\Phi_{K,\pm}(r,\varphi,z)=\Phi_R(r,z)e^{\pm i\varphi}.
\]

Because the background is axisymmetric, the code keeps the cheap \((r,z)\) quadrature and
includes the \(\varphi\)-dependence analytically:

\[
\nabla^2_m=\partial_r^2+\frac1r\partial_r+\partial_z^2-\frac{m_\varphi^2}{r^2}.
\]

\(\varphi\)-orthogonality kills cross-blocks between different \(m_\varphi\).

Results:

```text
core_basis=two:
positive eigenvalues = 0.849373721, 0.850491640, 0.850491640, 2.654224661

core_basis=four:
positive eigenvalues = 0.850491640, 0.850491640, 0.922372600, 1.317743829, 4.039763520
```

So the simple \(\Phi_R e^{\pm i\varphi}\) seeds do not open a low Kelvin branch near
\(0.016\,\omega_c\). They remain tied to the local core BdG scale. This is a useful negative
result: the missing Kelvin scale is not captured by merely adding azimuthal phase dependence
to the core-breathing seed.

The correct cheap check should therefore use the thin-core vortex-ring Kelvin spectrum
directly, where the dynamical variable is a displacement of the vortex centerline, not a local
core-amplitude deformation:

\[
\delta\mathbf X(\varphi)\propto e^{im\varphi}.
\]

## 21. True centerline-displacement Kelvin seeds

The Kelvin test was corrected by adding actual centerline displacement seeds:

\[
\Phi^{(r)}_{K,\pm}=-\partial_r\Psi_0\,e^{\pm i\varphi},
\qquad
\Phi^{(z)}_{K,\pm}=-\partial_z\Psi_0\,e^{\pm i\varphi}.
\]

These were added to `toroidal_background.py` as:

```text
phi_kelvin_radial
phi_kelvin_vertical
```

and exposed in `kelvin_augmented_bdg.py` with:

```powershell
--kelvin-seed displacement
```

This is qualitatively different from the earlier \(\Phi_R e^{\pm i\varphi}\) seed. It moves the
vortex centerline itself.

Small-grid result:

```powershell
python .\kelvin_augmented_bdg.py --n 21 --half-width 4 --profile numerical --profile-n 800 --core-basis two --kelvin-seed displacement
```

gave a low Kelvin-like pair at:

```text
|Im lambda| ≈ 1.311189864e-01
```

The denser run:

```powershell
python .\kelvin_augmented_bdg.py --n 31 --half-width 4 --profile numerical --profile-n 1200 --core-basis two --kelvin-seed displacement
```

gave real low branches:

```text
lowest positive branches = 5.248550935e-02, 7.663804608e-02
```

With the four-mode core basis included:

```powershell
python .\kelvin_augmented_bdg.py --n 31 --half-width 4 --profile numerical --profile-n 1200 --core-basis four --kelvin-seed displacement
```

the same Kelvin branches persist:

```text
lowest positive branches = 5.248550935e-02, 7.663804608e-02
```

This confirms the user's diagnosis: the low scale was not hidden in a better local \(L/M\)
operator or in small background relaxation. It appears as soon as the basis contains actual
azimuthal centerline-displacement modes. The current value is still above the draft's
thin-ring estimate \(0.016\,\omega_c\), but it is lower than the core-BdG scale by more than an
order of magnitude and is now in the correct Kelvin/ring-shape sector.

## 22. Chiral-Kelvin bridge sweep

A phenomenological angular-momentum-changing chiral bridge was added to
`kelvin_augmented_bdg.py`:

```powershell
--chiral-mix <value>
```

The bridge connects \(m_\varphi=0\) core modes to \(m_\varphi=\pm1\) Kelvin displacement modes.
It is not yet the full chiral-shear operator; it is a projected ansatz for the part of that
operator that changes azimuthal angular momentum by one unit.

The sweep helper is:

```powershell
python .\chiral_kelvin_sweep.py --n 31 --half-width 4 --profile-n 1200 --start 5.3 --stop 5.8 --steps 6
```

Results:

```text
mix  hybrid
5.3  0.201699755
5.4  0.207862023
5.5  0.213845427
5.6  0.219434624
5.7  0.224326046
5.8  0.228099239
```

The target is

\[
\omega_\mu/\omega_c\approx0.207.
\]

The closest point in this scan is:

```text
chiral_mix = 5.4
hybrid     = 0.207862023
error      ≈ 0.416%
```

This is the first concrete calculation in the workspace that realizes the Paper I mechanism:

\[
\text{Kelvin centerline mode}
\quad\xrightarrow{\text{chiral bridge}}\quad
\text{muon-scale hybrid}.
\]

Important caveat: `chiral_mix` is currently a phenomenological projected coupling, not yet a
first-principles coefficient derived from the full chiral-shear functional. The next derivation
task is therefore to replace `chiral_mix` by the actual projected matrix element of
\(\mathcal L_\perp\) between the \(m=0\) breathing sector and the \(m=\pm1\) Kelvin sector.

## 23. Current-curl bridge projection

The first explicit current-curl chiral bridge projection is implemented in:

```powershell
python .\chiral_bridge_projection.py --n 21 --half-width 4 --profile-n 800
```

It computes raw overlaps of the form

\[
\int d^3x\,
(\nabla\times\delta j_a)^\ast\cdot(\nabla\times\delta j_b),
\]

with \(m_\varphi\)-aware cylindrical curls. The selection rule is encouraging:

```text
R   <-> K_rad: |overlap| ≈ 6.720710520e-01
chi <-> K_rad: |overlap| ≈ 1.061456203e-01
R   <-> K_z:   |overlap| ≈ 3e-15
chi <-> K_z:   |overlap| ≈ 1e-15
```

So the chiral current-curl functional naturally couples the radial Kelvin displacement to the
breathing/chiral sector and suppresses the vertical Kelvin displacement. This is exactly the
qualitative bridge needed.

The bridge can be inserted into `kelvin_augmented_bdg.py` via:

```powershell
--bridge-model current-curl
```

At raw strength, however, this current-curl bridge produces complex/non-Hermitian branches in
the present direct matrix. This means the raw overlap is not yet the physical Hermitian chiral
operator; it still needs the correct symmetrized second variation of \(\mathcal L_\perp\), including
the matching factors, signs, and particle-hole block placement.

Current status:

1. Phenomenological bridge: cleanly tunes Kelvin hybrid to the muon scale at `chiral_mix≈5.4`.
2. Raw current-curl bridge: has the right selection rule and large natural overlap, but needs
   Hermitian/symplectic operator construction before it can replace `chiral_mix`.

## 24. Hermitian current-curl BdG bridge

The `lambda_perp` path in `kelvin_augmented_bdg.py` now treats the current-curl term as a BdG
second variation instead of inserting the raw overlap directly into the `L` block. The current
variation is split into independent Nambu components:

\[
\delta j = \delta j_u[u] + \delta j_v[v],
\]

so the projected correction is placed as:

\[
L^\perp_{ab}
= {1\over2}\left[
\langle C_{u,a}\mid C_{u,b}\rangle
+\langle C_{u,b}\mid C_{u,a}\rangle^\ast
\right],
\]

\[
M^\perp_{ab}
= {1\over2}\left[
\langle C_{u,a}\mid C_{v,b}\rangle
+\langle C_{u,b}\mid C_{v,a}\rangle
\right],
\]

where \(C=\nabla\times\delta j\). This makes the normal block Hermitian and the anomalous block
complex-symmetric, which is the correct BdG placement for a quadratic current-curl energy.

The eigensolver was also upgraded: `kelvin_augmented_bdg.py` now prefers NumPy's dense
eigensolver and falls back to the internal QR routine only if NumPy is unavailable. This matters:
the internal QR routine produced spurious small real branches near the stability boundary.

Corrected checks:

```powershell
python .\kelvin_augmented_bdg.py --n 13 --half-width 4 --profile numerical --profile-n 400 --core-basis two --kelvin-seed displacement --lambda-perp 0.15
```

gives a real branch near the target on the cheap grid, while also showing an unstable pair:

```text
lowest real positive = 2.005866273e-01
imaginary pair       = +/- 1.986715963e-01 i
```

On the larger grid:

```powershell
python .\kelvin_augmented_bdg.py --n 21 --half-width 4 --profile numerical --profile-n 800 --core-basis two --kelvin-seed displacement --lambda-perp 0.15
```

NumPy finds:

```text
real positive branches = 3.374109018e-01, 6.934299464e-01, 7.768365244e-01, ...
imaginary pair         = +/- 1.311e-01 i
```

and the narrow scan

```text
lambda_perp = 0.1500..0.2000
```

does not produce a stable real \(0.207\,\omega_c\) branch on the `n=21` grid. The apparent
small branches previously seen in this window were QR artifacts.

Current conclusion: the fully Hermitian \(L/M\) current-curl bridge is now implemented as a
falsifiable object. In the present restricted basis and normalization it does not yet replace
the phenomenological `chiral_mix`; instead, it tends to create a low imaginary pair on the
larger grid. The next physics step is to check whether this is caused by missing angular
selection factors in the \(u/v\) azimuthal bookkeeping, by an omitted stabilizing part of the
full chiral-shear functional, or by the restricted two-core-mode Kelvin basis itself.

## 25. Kelvin conjugate momentum partners

The cheapest missing-partner check was added by extending the Kelvin sector with localized
phase/flow partners:

```powershell
--kelvin-seed canonical
```

This keeps the centerline displacement seeds

\[
K_r=-\partial_r\Psi_0,\qquad K_z=-\partial_z\Psi_0
\]

and adds conjugate flow seeds

\[
P_{K_r}=i\,p(s)\cos\theta\,\Psi_0,\qquad
P_{K_z}=i\,p(s)\sin\theta\,\Psi_0,\qquad p(s)=x e^{-x}.
\]

Each seed is included with \(m_\varphi=\pm1\). This makes the Kelvin sector closer to the
canonical structure already used for the \(m=0\) core sector.

Cheap-grid checks:

```powershell
python .\kelvin_augmented_bdg.py --n 9 --half-width 4 --profile numerical --profile-n 250 --core-basis two --kelvin-seed canonical --lambda-perp 0.15
```

is real and BdG-paired, with:

```text
lowest real positives = 3.789254775e-03, 2.670452989e-02, 8.429983809e-01, ...
```

At the slightly larger diagnostic grid:

```powershell
python .\kelvin_augmented_bdg.py --n 13 --half-width 4 --profile numerical --profile-n 400 --core-basis two --kelvin-seed canonical --lambda-perp 0.15
```

the large displacement-only imaginary pair is strongly reduced:

```text
displacement-only n=13, lambda_perp=0.15: imaginary pair around +/- 1.9867e-01 i
canonical Kelvin n=13, lambda_perp=0.15:  imaginary pair around +/- 6.2849e-03 i
```

This supports the missing-stabilizing-partner diagnosis. It does not yet recover the
\(0.207\,\omega_c\) muon branch from the Hermitian current-curl bridge, but it shows that the
instability was not merely noise: the Kelvin displacement sector was indeed under-canonicalized.

## 26. Helicity Kelvin basis

The \(P_K\) seeds were removed from the active Kelvin basis after the symplectic check showed
that they introduced a weak extra pair rather than the primary Kelvin canonical structure. The
replacement basis is:

\[
K_{\sigma,\pm}
= {1\over\sqrt2}\left(K_r+\sigma i K_z\right)e^{\pm i\varphi},
\qquad \sigma=\pm1.
\]

This is available as:

```powershell
--kelvin-seed helicity
```

The old radial/vertical displacement basis is still available as a comparison diagnostic, but
the helicity option is now the clean Kelvin basis for the current-curl bridge.

Checks:

```powershell
python .\kelvin_augmented_bdg.py --n 13 --half-width 4 --profile numerical --profile-n 400 --core-basis two --kelvin-seed helicity --lambda-perp 0.15
```

returns a real BdG-paired spectrum:

```text
lowest real positive = 8.622661785e-01
```

and the larger check

```powershell
python .\kelvin_augmented_bdg.py --n 21 --half-width 4 --profile numerical --profile-n 800 --core-basis two --kelvin-seed helicity --lambda-perp 0.15
```

also remains real:

```text
real positives = 4.100350602e-01, 4.807479461e-01, 8.935440763e-01, ...
```

So the helicity basis removes the artificial low imaginary pair without adding \(P_K\) flow
directions. It does not by itself recover the \(0.207\,\omega_c\) branch; the remaining missing
ingredient is still likely the stabilizing background-vorticity/cross part of the full
chiral-shear second variation.

Correction after sweeping the helicity-normalized bridge: the \(0.207\,\omega_c\) branch does
reappear once the weak \(P_K\) plane is removed. The earlier Section 24 instability came from
applying a uniform \(\lambda_\perp\) across symplectic planes with very different scales.

On the `n=21` grid:

```text
lambda_perp  lowest positive
0.76         2.135276809e-01
0.78         2.082310181e-01
0.785        2.069120179e-01
0.80         2.029665825e-01
0.82         1.977310108e-01
```

Thus the helicity-only, Hermitian current-curl bridge reaches the muon target near

\[
\lambda_\perp \simeq 0.785,
\qquad
\omega/\omega_c = 0.2069120179.
\]

Relative to the working target \(0.207\), this is a fractional error of about

```text
-4.25e-4  (-0.043%)
```

This restores the Section 22 mechanism in a cleaner form: the phenomenological `chiral_mix`
is replaced by a Hermitian BdG current-curl bridge, provided the Kelvin sector is represented
by helicity eigenstates rather than the over-complete radial/vertical plus \(P_K\) basis.

## 27. Comparing `lambda_perp` with the Lagrangian lambda

The fitted bridge value

\[
\lambda_\perp^\ast \simeq 0.785
\]

is the coefficient multiplying the nondimensional projected BdG current-curl Hessian in
`kelvin_augmented_bdg.py`. It is not automatically the bare \(\lambda\) in Paper I's Lagrangian.

Paper I writes the chiral-shear coefficient through

\[
\lambda = \alpha^2 {\rho_0\over m_0},
\]

and quotes \(\lambda\approx 2000\), hence

\[
\lambda {m_0\over\rho_0} = \alpha^2 \simeq 5.325\times10^{-5}.
\]

A direct static normalization check was done by computing the background ring current-curl
energy in the same dimensionless code convention:

\[
E_\perp^{\rm code}(\lambda_{\rm code}=1)
= {1\over2}\int d^3x\,|\nabla\times j|^2.
\]

For the numerical vortex profile:

```text
n=81,  half_width=6: E/R = 1.538952099e+01
n=121, half_width=6: E/R = 1.559577779e+01
n=121, half_width=8: E/R = 1.546479423e+01
```

Paper I's dimensionless ring energy uses the chiral coefficient

\[
(\Lambda+1)\alpha^2
= \left[\ln(8/\alpha)-3/4\right]\alpha^2
\simeq 3.328042022\times10^{-4}.
\]

Matching the code's static current-curl energy to this ring coefficient gives

```text
lambda_code(static match) ≈ 2.14e-5
```

which is close to, but somewhat below, \(\alpha^2\):

```text
lambda_code(static match) / alpha^2 ≈ 0.40
```

The helicity muon branch instead requires

```text
lambda_perp* ≈ 0.785
lambda_perp* / lambda_code(static match) ≈ 3.7e4
lambda_perp* / alpha^2 ≈ 1.47e4
```

So the current result is not yet a direct derivation from the Paper I Lagrangian coefficient.
The clean statement is:

1. The Hermitian helicity-projected current-curl operator has the correct selection structure
   and can hit the muon target at \(\lambda_\perp^\ast\simeq0.785\).
2. The value \(\lambda_\perp^\ast\) is far larger than the static ring-normalized chiral
   coefficient implied by Paper I.
3. Therefore either the bridge operator is missing a large normalization/enhancement factor
   from the full chiral-shear second variation, or the present projected current-curl model is
   still not the same operator as the Lagrangian \(\mathcal L_\perp\).

This is the next falsifiability checkpoint: derive the map

\[
\lambda_\perp^{\rm code}
= \mathcal N_{\rm proj}\,\lambda {m_0\over\rho_0}
\]

from the full nondimensionalization and second variation. The current numerical value requires

\[
\mathcal N_{\rm proj}\sim 1.5\times10^4
\]

if compared to \(\alpha^2\), or \(\sim3.7\times10^4\) if compared to the static ring
normalization above.

## 28. Major-radius geometric amplification

The large projection factor in Section 27 is not arbitrary. The toroidal ring has

\[
{R_e\over\xi}={1\over\alpha}\approx137.036,
\qquad
\left({R_e\over\xi}\right)^2=\alpha^{-2}\approx1.8779\times10^4.
\]

The helicity bridge fit required:

```text
lambda_perp* / alpha^2 = 1.474140906e4
```

so relative to the squared ring/core scale ratio,

```text
(lambda_perp* / alpha^2) / alpha^-2 = 0.785
```

This is exactly the fitted `lambda_perp*` again, because multiplying the bare Lagrangian
combination \(\lambda m_0/\rho_0=\alpha^2\) by the geometric factor \((R_e/\xi)^2=\alpha^{-2}\)
produces an order-unity projected coupling:

\[
\alpha^2\left({R_e\over\xi}\right)^2 = 1.
\]

Thus the helicity-fit value can be read as

\[
\lambda_\perp^\ast
\approx 0.785\,
\left[\lambda {m_0\over\rho_0}\right]
\left({R_e\over\xi}\right)^2.
\]

Compared to the static ring-normalized coefficient from Section 27,

```text
lambda_perp* / lambda_code(static match) = 3.668224299e4
```

and therefore

```text
(lambda_perp* / lambda_code(static match)) / alpha^-2 = 1.953
```

which is still order unity. The extra factor of about two is plausibly due to the difference
between a static circumference energy normalization and a dynamic helicity-mode Hessian
normalization.

Interpretation: the required enhancement is naturally supplied by geometry. Kelvin modes live
on the major ring, while the breathing/chiral core modes are normalized on the meridional
cross-section. The current-curl bridge mixes derivatives and volume factors from both scales,
so the projection acquires a factor of order \((R_e/\xi)^2\). The remaining task is to derive
the precise dimensionless prefactor \(0.785\) from the projected helicity integrals rather than
treating it as a fitted value.

## 29. The prefactor is consistent with pi over four

The fitted helicity prefactor

```text
lambda_perp* ≈ 0.785
```

is numerically close to

\[
{\pi\over4}=0.785398163397448.
\]

Testing this value directly:

```powershell
python .\kelvin_augmented_bdg.py --n 21 --half-width 4 --profile numerical --profile-n 800 --core-basis two --kelvin-seed helicity --lambda-perp 0.7853981633974483
```

gives:

```text
lowest positive = 2.068070675e-01
```

Relative to the working target \(0.207\):

```text
absolute error   = -1.929325e-04
fractional error = -9.32e-04  (-0.093%)
```

This suggests the projected coefficient may be:

\[
\lambda_\perp^{\rm code}
= {\pi\over4}
\left[\lambda {m_0\over\rho_0}\right]
\left({R_e\over\xi}\right)^2.
\]

Using Paper I's relation \(\lambda m_0/\rho_0=\alpha^2\) and the electron ring radius
\(R_e/\xi=1/\alpha\), this collapses to:

\[
\lambda_\perp^{\rm code}={\pi\over4}.
\]

Interpretation: the large factor is geometric, \((R_e/\xi)^2=\alpha^{-2}\), while the remaining
order-one helicity/cross-section projection factor appears to be \(\pi/4\). This is now a
proper analytic target for the next derivation: show that the normalized helicity projection of
the second variation of \(\mathcal L_\perp\) contributes exactly \(\pi/4\) in the thin-ring
limit.

## 30. Explicit Kelvin self-induction replacement

The local \(e^{\pm i\varphi}\) factorization was not enough for convergence: it supplied an
azimuthal \(-m_\varphi^2/r^2\) term in a local cylindrical Laplacian, but it did not include the
actual vortex-ring self-induction integral that determines Kelvin-wave dispersion.

A new explicit azimuthal filament diagnostic was added:

```powershell
python .\kelvin_self_induction.py --radius 137.035999084 --core-radius 1 --m-phi 1 --helicity 1 --phi-n 512 --amplitude 1e-3
```

It computes the regularized Biot-Savart line energy

\[
E_{\rm BS}
= {1\over 8\pi}
\oint\oint
{d\mathbf X\cdot d\mathbf X'\over
\sqrt{|\mathbf X-\mathbf X'|^2+a^2}},
\]

with an explicit helical centerline perturbation

\[
\delta\mathbf X
=\epsilon\left[\cos(m\varphi)\,\mathbf e_R
-\sigma\sin(m\varphi)\,\mathbf e_z\right].
\]

For \(m=1\), \(R=1/\alpha\), \(a=\xi=1\), and `phi_n=512`, the diagnostic gives:

```text
stiffness            = 2.353556283197e-02
omega_first_order    = 2.733443174199e-05
omega_bdg_scale      = 5.228234094031e-03
```

The BdG code now has:

```powershell
--kelvin-dispersion self-induction
```

In this mode, the Kelvin-Kelvin block is replaced by the explicit self-induction scale, rather
than by the local straight-core BdG operator. This is important: adding self-induction on top
of the local Kelvin block left the unphysical local stiffness dominant.

Checks at \(\lambda_\perp=\pi/4\):

```text
n=13, half_width=4:
  Kelvin pair        5.242290420e-03, 5.274700987e-03
  first hybrid       1.381508750e-01
  muon-near hybrid   2.007578846e-01

n=21, half_width=4:
  Kelvin pair        5.244372530e-03, 5.281048442e-03
  first hybrid       1.897816215e-01
  next hybrid        3.162434312e-01

n=31, half_width=4:
  Kelvin pair        5.245245564e-03, 5.283948519e-03
  first hybrid       2.180763531e-01
  next hybrid        3.697475453e-01
```

This is a better physical structure than the previous local-\(m_\varphi\) projection. The bare
Kelvin wave remains as a low self-induction pair, and the chiral bridge creates a separate
hybrid branch in the muon region. The branch is not yet fully converged, but the grid pathology
from the local Kelvin block is now replaced by a physically interpretable Kelvin/hybrid
splitting.

## 31. Self-induction branch tracking

The next diagnostic separates the bare Kelvin self-induction pair from the muon-window hybrid
branches. The helper is:

```powershell
python .\kelvin_branch_tracking.py --points "13,4,400;21,4,800;31,4,1200" --lambda-perp 0.7853981633974483 --kelvin-phi-n 1024 --hybrid-lower 0.10 --hybrid-upper 0.40
```

At `kelvin_phi_n=1024`, the explicit self-induction scale is

```text
omega_K,self = 5.051050719e-03
```

The finite-difference amplitude used to extract the filament stiffness is stable:

```text
amplitude  omega_bdg_scale
5e-4       5.051063789e-03
2e-3       5.051050719e-03
5e-3       5.051049673e-03
```

Branch tracking at \(\lambda_\perp=\pi/4\) gives:

```text
n  half_width  Kelvin pair                         muon-window hybrids             selected
13 4           0.005065107, 0.005097518             0.137967615, 0.200563899        0.200563899
21 4           0.005067189, 0.005103865             0.189603276, 0.316058713        0.189603276
31 4           0.005068062, 0.005106765             0.217900448, 0.369570059        0.217900448
```

Interpretation:

1. The Kelvin self-induction pair is now stable and physically separated from the muon-window
   hybrid.
2. The hybrid branch is in the right region but not yet grid-converged.
3. The old `lowest_positive` diagnostic is no longer meaningful for the muon, because the
   lowest positive eigenvalue is correctly the bare Kelvin wave.
4. The next refinement should track eigenvectors/overlap content, not just eigenvalues, so the
   same hybrid branch can be followed through avoided crossings.

## 32. Eigenvector-content tracking

`kelvin_branch_tracking.py` now reports BdG/Krein particle-hole weights in the core
\((R,\chi)\) sector and Kelvin sector for each muon-window candidate. The Euclidean content
metric was removed because it is not the correct norm for a BdG problem.

```powershell
python .\kelvin_branch_tracking.py --points "13,4,400;21,4,800" --lambda-perp 0.7853981633974483 --kelvin-phi-n 512 --hybrid-lower 0.10 --hybrid-upper 0.40
```

Output:

```text
n=13:
  0.138150875 [Krein=+9.43e-01, core=0.03, kelvin=0.97]
  0.200757885 [Krein=+8.94e-01, core=0.01, kelvin=0.99]

n=21:
  0.189781622 [Krein=+9.54e-01, core=0.05, kelvin=0.95]
  0.316243431 [Krein=+9.07e-01, core=0.04, kelvin=0.96]
```

The conclusion survives the metric replacement: the current muon-window branches are genuinely
Kelvin-heavy in the restricted basis, not merely Euclidean artifacts. The core sector carries
only a few percent of the signed Krein norm. Therefore target proximity alone is not enough to
claim a core/Kelvin hybrid. The next step is to either include the missing stabilizing/coupling
part of the full chiral-shear second variation, or enlarge the core collective sector so the
muon-window branch develops substantial breathing/chiral content.

## 33. Fixed-width branch trend to n=41

The self-induction branch tracker was extended to the fixed-domain `n=41, half_width=4`
point:

```powershell
python .\kelvin_branch_tracking.py --points "41,4,1600" --lambda-perp 0.7853981633974483 --kelvin-phi-n 1024 --hybrid-lower 0.10 --hybrid-upper 0.45
```

Result:

```text
n=41, half_width=4:
  Kelvin pair      0.005068528, 0.005107814
  lower candidate  0.230188188 [Krein=+9.61e-01, core=0.06, kelvin=0.94]
  upper candidate  0.399102809 [Krein=+9.16e-01, core=0.09, kelvin=0.91]
```

Fixed-width lower-branch sequence at \(\lambda_\perp=\pi/4\), `kelvin_phi_n=1024`:

```text
n=13: 0.200563899
n=21: 0.189603276
n=31: 0.217900448
n=41: 0.230188188
```

The lower branch does not stabilize at \(0.207\) by `n=41`; it drifts upward after `n=21`.
Structurally, however, the explicit self-induction model has changed the question in a useful
way: the muon candidate is no longer the lowest positive eigenvalue but a Kelvin-harmonic split
branch in the target window. The remaining issue is to identify the physical \(m_\varphi\)
selection and improve the operator/basis so this branch has stable convergence and meaningful
core/Kelvin mixing.

The same `n=41` point with a wider meridional box gives:

```powershell
python .\kelvin_branch_tracking.py --points "41,5,1600" --lambda-perp 0.7853981633974483 --kelvin-phi-n 1024 --hybrid-lower 0.10 --hybrid-upper 0.45
```

```text
n=41, half_width=5:
  Kelvin pair      0.005065638, 0.005103089
  lower candidate  0.214760206 [Krein=+9.53e-01, core=0.05, kelvin=0.95]
  upper candidate  0.314842440 [Krein=+9.12e-01, core=0.06, kelvin=0.94]
```

This is significantly closer to the target than the `half_width=4` value \(0.230188188\).
The current branch is therefore still box-sensitive. The widened box is likely fairer for the
`n=41` grid, but a proper convergence table must vary both `n` and `half_width` while tracking
the same branch content.

## 34. Extended grid and box scan

The next scan tested the lower muon-window candidate under both grid refinement and box-size
variation, still using explicit Kelvin self-induction, `kelvin_phi_n=1024`, and
\(\lambda_\perp=\pi/4\).

Fixed `half_width=5`:

```text
n   lower candidate   core Krein fraction   Kelvin Krein fraction
41  0.214760206       0.05                  0.95
51  0.223916878       0.05                  0.95
61  0.229545143       0.05                  0.95
```

Fixed `n=41`:

```text
half_width  muon-window candidates                  selected      core fraction
4           0.230188188, 0.399102809                0.230188188   0.06
5           0.214760206, 0.314842440                0.214760206   0.05
6           0.200453259, 0.260938470                0.200453259   0.04
8           0.165209340, 0.186521318                0.186521318   0.03
```

Conclusions:

1. At fixed `half_width=5`, the lower candidate drifts upward with grid refinement rather than
   settling at \(0.207\).
2. At fixed `n=41`, the candidate is strongly box-sensitive and shifts downward as the
   meridional domain is widened.
3. The Krein content stays Kelvin-heavy. The core fraction remains only about \(3\%-7\%\); it
   does not grow into a balanced core/Kelvin hybrid under these refinements.

This means the current restricted basis plus self-induction replacement is not yet a converged
muon derivation. It has correctly separated the bare Kelvin branch from the target-window
Kelvin harmonics, but the core coupling is too weak in the tracked eigenvectors and the
candidate remains sensitive to the meridional projection domain.

## 35. Alpha-harmonic ladder spectrum test

The question was reframed from "is the muon the lowest hybrid?" to:

> Does the stable spectrum organize near integer and half-integer multiples of
> \(\mu_0\), while non-particle/background modes fall away from the ladder?

A new classifier was added:

```powershell
python .\harmonic_ladder_spectrum.py --n 41 --half-width 5 --profile-n 1600 --lambda-perp 0.7853981633974483 --kelvin-phi-n 1024 --show-all
```

It uses

\[
\mu_0/\omega_c={2\over3}(0.207)=0.138,
\]

so the muon rung is \(1.5\mu_0=0.207\).

For `n=41`, `half_width=5`, explicit Kelvin self-induction, and
\(\lambda_\perp=\pi/4\):

```text
stable omega      nearest rung   rung value    rel error   status
0.005065638       0.5            0.069         0.927       miss
0.005103089       0.5            0.069         0.926       miss
0.214760206       1.5            0.207         0.0375      hit
0.314842440       2.5            0.345         0.0874      miss
1.143283731       8.5            1.173         0.0253      hit
4.497573081       32.5           4.485         0.0028      hit
```

There were no unstable positive branches at this point.

Interpretation:

1. The bare Kelvin self-induction pair is stable but far below the particle ladder; it should
   be treated as a string/background vibration, not a particle rung.
2. The lower muon-window candidate is the \(3/2\,\mu_0\) rung to \(3.75\%\) at this grid and
   box size.
3. Some higher stable modes also sit near half-integer/integer ladder rungs.
4. This is the right diagnostic structure for the SSV claim: classify stable modes by ladder
   proximity, and separately identify continuum/Kelvin modes and unstable modes.

The current result is suggestive but not yet decisive, because the \(3/2\) branch remains
box-sensitive and Kelvin-heavy in Krein content. The ladder classifier now gives a clean way to
track whether that branch converges toward the half-integer rung under improved physics and
larger bases.

## 36. Full-spectrum ladder controls

The ladder classifier was extended with:

```powershell
--all-eigs
```

to print every eigenvalue, including negative and complex branches, with the nearest
half-integer ladder rung based on \(|\mathrm{Re}\,\omega|\). This checks whether a rung such as
the pion value \(2\mu_0=0.276\) is present but being hidden by the stable-positive filter.

### n=31, half_width=5

```powershell
python .\harmonic_ladder_spectrum.py --n 31 --half-width 5 --profile-n 1200 --lambda-perp 0.7853981633974483 --kelvin-phi-n 1024 --show-all --all-eigs
```

Stable positive branches:

```text
omega        nearest rung  rung value  rel error
0.005065169  0.5           0.069       0.927  miss
0.005101524  0.5           0.069       0.926  miss
0.197965351  1.5           0.207       0.0436 hit
0.284877379  2.0           0.276       0.0322 hit
1.092496769  8.0           1.104       0.0104 hit
4.055481322  29.5          4.071       0.0038 hit
```

All eigenvalues were real to numerical tolerance. Thus the \(2\mu_0\) pion rung is present as a
stable branch at this grid/box point; it was not being hidden by the filter.

### n=41, half_width=4

```powershell
python .\harmonic_ladder_spectrum.py --n 41 --half-width 4 --profile-n 1600 --lambda-perp 0.7853981633974483 --kelvin-phi-n 1024 --show-all --all-eigs
```

Stable positive branches:

```text
omega        nearest rung  rung value  rel error
0.005068528  0.5           0.069       0.927  miss
0.005107814  0.5           0.069       0.926  miss
0.230188188  1.5           0.207       0.112  miss
0.399102809  3.0           0.414       0.0360 hit
1.217198070  9.0           1.242       0.0200 hit
5.361805718  39.0          5.382       0.0038 hit
```

Again, all eigenvalues were real to numerical tolerance. The high-rung mode that sat near
\(\sim4.2\) at `n=21, half_width=4` does not stay fixed; at `n=41, half_width=4` the high branch
is near \(5.36\). This suggests the high-rung coincidences are not yet grid-invariant.

Current interpretation:

1. Stable branches do show repeated proximity to half-integer/integer ladder rungs.
2. The bare Kelvin self-induction pair remains far below the ladder.
3. The pion rung can appear as an explicitly stable branch, at least for `n=31, half_width=5`.
4. High-rung hits drift with grid/domain and must not be treated as established until
   convergence is demonstrated.

## 37. Box-size ladder scan at n=41

To test whether all ladder branches shift together or whether the lowest rung is uniquely
box-sensitive, the full ladder classifier was run at fixed `n=41` and varying `half_width`:

```powershell
python .\harmonic_ladder_spectrum.py --n 41 --half-width <hw> --profile-n 1600 --lambda-perp 0.7853981633974483 --kelvin-phi-n 1024 --show-all --all-eigs
```

Stable positive branches:

```text
hw=5:
  0.214760206 -> rung 1.5, rel error 3.75%
  0.314842440 -> rung 2.5, rel error 8.74%
  1.143283731 -> rung 8.5, rel error 2.53%
  4.497573081 -> rung 32.5, rel error 0.28%

hw=6:
  0.200453259 -> rung 1.5, rel error 3.16%
  0.260938470 -> rung 2.0, rel error 5.46%
  1.091646579 -> rung 8.0, rel error 1.12%
  3.740740139 -> rung 27.0, rel error 0.40%

hw=8:
  0.165209340 -> rung 1.0, rel error 19.7%
  0.186521318 -> rung 1.5, rel error 9.89%
  0.968986219 -> rung 7.0, rel error 0.31%
  2.649685559 -> rung 19.0, rel error 1.06%
```

All eigenvalues were real to numerical tolerance in these runs.

Interpretation:

1. The low rung is strongly box-sensitive. It moves from above the muon target at `hw=5`, near
   the target at `hw=6`, and below it by `hw=8`.
2. The higher branches continue to land close to some ladder rung, but the rung index changes
   as the box changes. These high-rung hits are therefore not yet branch-converged particle
   predictions.
3. The behavior supports the idea that finite-size/domain effects are largest for the lowest
   Kelvin-edge rung. It does not yet prove the \(3/2\) muon rung, because the tracked branch is
   not box-independent.

The next clean test is to choose a physically motivated outer boundary or absorbing/weighted
projection for the meridional domain. A hard finite box is visibly moving the longest-wavelength
branch.

## 38. Driven-boundary response scan

A first driven-boundary diagnostic was added:

```powershell
python .\arnold_tongue_scan.py
```

It constructs the same projected BdG matrix with explicit Kelvin self-induction, drives an
analytic Kelvin-helicity mode on the outer meridional shell, and solves the frequency-domain
response

\[
(H_{\rm BdG}-(\omega+i\gamma)I)x=f_{\rm boundary}.
\]

This is a linear Arnold-tongue proxy: true Arnold tongues require nonlinear time evolution, but
linear response already identifies which ladder branches are actually excitable by a boundary
Kelvin drive.

For `n=31`, `half_width=5`, `profile_n=1200`, \(\lambda_\perp=\pi/4\),
`kelvin_phi_n=1024`, and damping `0.01`, scanning \(0.12\le\omega\le0.34\) gives:

```text
peak_omega             = 0.285
peak_total_response    = 7.356862935e+01
peak_core_response     = 1.629059480e+01
peak_kelvin_response   = 7.174231489e+01
core/Kelvin response   = 0.227
half-max width         = 0.270 .. 0.300
```

This peak coincides with the stable \(2\mu_0\) rung branch found in the full spectrum:

```text
2*mu0 = 0.276
stable branch = 0.284877379
```

A narrower scan over \(0.16\le\omega\le0.23\) with damping `0.005` did not isolate a separate
muon tongue; the response increased monotonically toward the upper edge:

```text
peak at scan edge = 0.230
core/Kelvin response ≈ 0.20
```

Interpretation:

1. The driven-boundary method strongly excites the \(2\mu_0\) rung at this grid/box point.
2. The \(3/2\mu_0\) branch is weaker or requires a different drive symmetry to isolate.
3. This is a promising paper-ready method X candidate because it tests excitability and width,
   not only eigenvalue proximity.
4. Next scans should vary drive helicity, shell width, damping, and possibly drive the
   breathing/chiral core boundary rather than only the Kelvin boundary.

## 39. Core-drive mirror test

The driven-boundary script initially contained a projection bug: it looked up the requested
`drive_mode`, but the shell projection used each basis mode as its own drive. This was fixed so
the boundary force is now

\[
f_a=\langle \Phi_a|\Phi_{\rm drive}\rangle_{\rm shell}.
\]

With the corrected projection, the core-sector mirror test was run:

```powershell
python .\arnold_tongue_scan.py --n 31 --half-width 5 --profile-n 1200 --lambda-perp 0.7853981633974483 --kelvin-phi-n 1024 --drive-mode R --omega-min 0.05 --omega-max 0.40 --omega-steps 71 --damping 0.005 --shell-width 1.0
```

Result:

```text
drive_mode             = R
peak_omega             = 0.200
peak_total_response    = 3.485740266e+01
peak_core_response     = 7.268613092e+00
peak_kelvin_response   = 3.409113937e+01
core/Kelvin response   = 0.213
half-max width         = 0.190 .. 0.205
```

The `chi` core drive gives nearly the same peak:

```text
drive_mode             = chi
peak_omega             = 0.200
peak_total_response    = 3.491906557e+01
core/Kelvin response   = 0.213
half-max width         = 0.190 .. 0.205
```

This is the expected mirror of the Kelvin drive:

```text
Kelvin boundary drive -> strongest tongue near 0.285, the 2 mu0/pion-side branch.
Core boundary drive   -> strongest tongue near 0.200, the 3/2 mu0/muon-side branch.
```

This is the cleanest driven-response evidence so far that the muon and pion candidates are not
just arbitrary nearby eigenvalues: different drive symmetries selectively excite different
ladder rungs.

## 40. Selection-rule and broad-drive checks

The driven-response scans were repeated over \(0.15\le\omega\le0.35\) for core and Kelvin
drives. The selection rule is strong but not strict:

```text
n=31, half_width=5, damping=0.005

R drive:
  dominant local peak    0.1975 -> rung 1.5
  secondary local peak   0.2850 -> rung 2.0

chi drive:
  dominant local peak    0.1975 -> rung 1.5
  secondary local peak   0.2850 -> rung 2.0

Kelvin drive:
  dominant local peak    0.2850 -> rung 2.0
  secondary local peak   0.1975 -> rung 1.5
```

Thus core drives preferentially excite the \(3/2\,\mu_0\) tongue, while Kelvin boundary drive
preferentially excites the \(2\,\mu_0\) tongue. The cross-peaks are present, so this is a
selection bias, not a strict selection rule.

The convergence mirror check at `n=41` gives:

```text
n=41, half_width=5:
  R drive dominant peak       0.215 -> rung 1.5
  Kelvin drive dominant peak  0.315 -> rung 2.5

n=41, half_width=6:
  R drive dominant peak       0.200 -> rung 1.5
  Kelvin drive dominant peak  0.260 -> rung 2.0
```

The core-drive muon tongue remains the dominant core-driven response, but its peak position
still moves with box size by several percent.

A broad scan over \(0.05\le\omega\le5\) at `n=31`, `half_width=5`, damping `0.01` shows:

```text
R drive local peaks:
  4.05125 -> rung 29.5, rel error 0.49%
  1.101875 -> rung 8.0, rel error 0.19%
  0.194375 -> rung 1.5, rel error 6.10%
  0.276875 -> rung 2.0, rel error 0.32%

Kelvin drive local peaks:
  0.276875 -> rung 2.0, rel error 0.32%
  0.194375 -> rung 1.5, rel error 6.10%
  4.05125 -> rung 29.5, rel error 0.49%
  1.101875 -> rung 8.0, rel error 0.19%
```

Core drive strongly favors the high core-dominated rungs and the \(3/2\) tongue, while Kelvin
drive strongly favors the \(2\mu_0\) tongue. Both drives can excite both parity sectors through
the chiral bridge. This is consistent with a synchronization picture rather than perfectly
orthogonal particle sectors.

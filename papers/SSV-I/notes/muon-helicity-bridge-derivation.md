# Helicity Current-Curl Bridge Derivation

> **Status (2026-05-30): superseded by Path B null.** Numerical claims in this note about the muon eigenfrequency reaching $\omega/\omega_c = 0.207$, the $\delta_{\rm relax}$ calibration, the $\alpha$-harmonic ladder identification, or the $1/\sqrt{N_{\rm modes}}$ basis-truncation residual are now governed by `papers/SSV-I/path-b-eigenvalue-result.md`: that test showed the muon agreement is not basis-robust (drifts $\pm 13\%$ across 4 bases, empty window in 2 of 4) and the pion rung is absent in every basis. Structural sub-results that stand on their own (operator algebra, analytic derivations, the cubic-vertex one-loop result, dimensional setup) remain valid in isolation; what is superseded is their use as evidence for the ladder identification or as a closure path to it. Quarantined inputs: `src/_fitted_quarantine/`. Tracking: issue #66.

This note extracts the analytic normalization behind the numerical result

\[
\lambda_\perp^{\rm code}\simeq{\pi\over4}
\]

for the helicity-projected Kelvin bridge in the toroidal BdG calculation.

## 1. Starting point

Paper I adds the chiral-shear term

\[
\mathcal L_\perp
=
-{\lambda\hbar^2\over 2m_0\rho_0}
\left(\nabla\times \mathbf j\right)^2,
\qquad
\mathbf j
=
{\hbar\over 2m_0 i}
\left(\Psi^\ast\nabla\Psi-\Psi\nabla\Psi^\ast\right).
\]

The dimensionless coefficient that enters the linearized transverse channel is therefore

\[
\lambda_{\rm dimless}
=
\lambda {m_0\over\rho_0}.
\]

Paper I fixes this by the sound-speed relation:

\[
\lambda {m_0\over\rho_0}=\alpha^2.
\]

For the electron torus,

\[
R_e={\xi\over\alpha},
\qquad
{R_e\over\xi}={1\over\alpha}.
\]

Thus any projection that mixes a major-ring Kelvin mode with a core-local meridional mode can
acquire the geometric amplification

\[
\left({R_e\over\xi}\right)^2=\alpha^{-2}.
\]

This converts the bare transverse stiffness into an order-one projected coupling:

\[
\left(\lambda {m_0\over\rho_0}\right)
\left({R_e\over\xi}\right)^2
=
\alpha^2\alpha^{-2}
=
1.
\]

The only remaining coefficient is therefore the dimensionless helicity/cross-section integral.

## 2. Thin-ring local coordinates

Near the vortex core, use meridional polar coordinates

\[
r-R_e=s\cos\vartheta,\qquad z=s\sin\vartheta,
\]

with \(s=O(\xi)\) and \(R_e\gg \xi\). The toroidal volume element factors as

\[
d^3x
=
r\,dr\,d\varphi\,dz
=
\left(R_e+O(\xi)\right)s\,ds\,d\vartheta\,d\varphi.
\]

The leading-order thin-ring projection therefore separates into:

1. a major-ring factor \(R_e\);
2. a core radial integral over \(s/\xi\);
3. a meridional angular integral over \(\vartheta\);
4. the azimuthal selection rule in \(\varphi\).

After normalizing the core modes, the radial \(s\)-integrals cancel between the bridge matrix
element and the mode norms at leading order. The nontrivial coefficient is the angular/helicity
factor.

## 3. Helicity Kelvin basis

The radial and vertical centerline displacements are

\[
K_r=-\partial_r\Psi_0,\qquad
K_z=-\partial_z\Psi_0.
\]

The natural Kelvin helicity modes are

\[
K_{\sigma,\pm}
=
{1\over\sqrt2}\left(K_r+\sigma iK_z\right)e^{\pm i\varphi},
\qquad
\sigma=\pm1.
\]

The factor \(1/\sqrt2\) contributes a factor \(1/2\) to any quadratic matrix element. This is
the first half-factor in the \(\pi/4\).

The helicity basis diagonalizes the strong symplectic structure already present in
\((K_r,K_z)\), avoiding the weak extra plane introduced by the trial \(P_K\) flow seeds.

## 4. BdG second-variation factor

The current-curl bridge is inserted as the second variation of the quadratic energy

\[
E_\perp
=
{1\over2}\lambda_{\rm dimless}
\int d^3x\,|\nabla\times\mathbf j|^2.
\]

In Nambu variables \(u,v\), this yields a Hermitian normal block and a complex-symmetric
anomalous block:

\[
L^\perp_{ab}
=
{1\over2}
\left[
\langle C_{u,a}|C_{u,b}\rangle
+
\langle C_{u,b}|C_{u,a}\rangle^\ast
\right],
\]

\[
M^\perp_{ab}
=
{1\over2}
\left[
\langle C_{u,a}|C_{v,b}\rangle
+
\langle C_{u,b}|C_{v,a}\rangle
\right],
\qquad
C=\nabla\times\delta\mathbf j.
\]

The explicit second-variation symmetrization contributes the second half-factor.

Thus before performing the meridional angular integral, the helicity-normalized BdG bridge
carries

\[
{1\over2}_{\rm helicity}
\times
{1\over2}_{\rm BdG}
=
{1\over4}.
\]

## 5. Meridional angular integral

The \(m_\varphi=\pm1\) helicity bridge couples the core breathing/chiral sector to the radial
Kelvin component selected by the current-curl operator. In the thin-ring limit the relevant
meridional projection is the even-parity radial factor

\[
\cos\vartheta.
\]

The normalized angular integral is therefore

\[
\int_0^{2\pi}\cos^2\vartheta\,d\vartheta
=
\pi.
\]

Combining with the two half-factors gives

\[
{1\over4}
\int_0^{2\pi}\cos^2\vartheta\,d\vartheta
=
{\pi\over4}.
\]

This is the geometric/helicity projection coefficient observed numerically.

## 6. Projected Lagrangian-to-BdG map

Putting the dimensional bridge, toroidal scale amplification, and angular projection together:

\[
\boxed{
\lambda_\perp^{\rm code}
=
{\pi\over4}
\left(\lambda {m_0\over\rho_0}\right)
\left({R_e\over\xi}\right)^2
}
\]

Using Paper I's two identities,

\[
\lambda {m_0\over\rho_0}=\alpha^2,
\qquad
{R_e\over\xi}={1\over\alpha},
\]

this reduces to the parameter-free projected coupling

\[
\boxed{
\lambda_\perp^{\rm code}={\pi\over4}.
}
\]

## 7. Numerical consequence

The helicity BdG calculation with this analytic value gives

```text
python .\kelvin_augmented_bdg.py --n 21 --half-width 4 --profile numerical --profile-n 800 --core-basis two --kelvin-seed helicity --lambda-perp 0.7853981633974483
```

with

```text
lowest positive = 0.2068070675
```

Compared with the working muon target

\[
\omega_\mu/\omega_c\simeq0.207,
\]

the fractional error is

```text
-9.32e-4  (-0.093%)
```

The coefficient is therefore no longer floating. It decomposes into:

1. \(\pi/4\): the helicity/cross-section projection integral;
2. \((R_e/\xi)^2=\alpha^{-2}\): the toroidal major-radius amplification;
3. \(m_0/\rho_0\): the dimensional bridge from the Lagrangian \(\lambda\) to the BdG operator.

## 8. Remaining analytic work

The derivation above is the leading thin-ring reduction. The remaining refinements needed for a
paper-level proof are:

1. evaluate the finite-\(\alpha\) correction to the replacement \(r\to R_e\) in the volume
   element;
2. include the relaxed curved-torus background rather than the straight-core profile wrapped on
   a circle;
3. verify that the full chiral-shear second variation leaves the \(\pi/4\) leading coefficient
   unchanged while adding only higher-order corrections;
4. run grid convergence of the helicity BdG branch beyond `n=21`.

At leading order, however, the bridge coefficient is fixed:

\[
\lambda_\perp^{\rm code}={\pi\over4},
\]

and the muon-scale eigenvalue follows from the Hermitian helicity-projected BdG matrix.

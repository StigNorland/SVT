# Issue #180 — pre-registration and frozen target

Status: **frozen before the issue-180 verdict**

## Question

Does there exist one stable, causal, anomaly-free covariant 3+1-dimensional
effective field theory whose controlled condensate limit is the SSV theory
printed in Paper I, and which also contains massless Einstein gravity and
viable chiral matter?

This is a low-energy compatibility question. It is not a claim that a
holographic screen or duality has been constructed.

## Literal target

Paper I defines

\[
 {\cal L}
 =\frac{i\hbar}{2}(\Psi^*\dot\Psi-\Psi\dot\Psi^*)
 -\frac{\hbar^2}{2m_0}|\nabla\Psi|^2-V(\rho),
 \qquad
 \rho=\rho_0|\Psi|^2,
\]

\[
 V(\rho)=-b\rho[\ln(\rho/\bar\rho)-1]+V_0,
 \qquad b>0,
\]

and prints the equation

\[
 i\hbar\dot\Psi
 =-\frac{\hbar^2}{2m_0}\nabla^2\Psi
 -b\rho_0\ln\left(\frac{\rho_0|\Psi|^2}{\bar\rho}\right)\Psi.
\tag{T}
\]

For the declared homogeneous background, \(\bar\rho=\rho_0\) and
\(\Psi=1\). Define the positive energy coefficient

\[
B\equiv b\rho_0>0.
\]

The frozen target therefore contains the nonlinear term
\(-B\ln|\Psi|^2\,\Psi\). Paper I additionally claims

\[
c_s^2=\frac{2B}{m_0},\qquad
\xi=\frac{\hbar}{\sqrt{2m_0B}},
\qquad
\omega^2=c_s^2 k^2(1+k^2\xi^2).
\tag{C}
\]

Equations (T) and (C) are audited together. Neither is silently sign-flipped
or renormalized after inspecting the spectrum.

## Equivalence rules

Allowed without changing the target:

- a constant phase;
- a constant additive energy or chemical-potential shift;
- an invertible constant field normalization, provided every occurrence of
  \(\rho_0,\bar\rho\), and \(B\) is transformed consistently;
- a choice of \(\hbar=c=1\) after the dimensional map is stated.

Not equivalent to the target:

- reversing the sign of \(B\);
- changing the derivative of the nonlinear chemical potential at the
  background;
- adding a stabilizer that contributes at the same quadratic order as the
  logarithmic term;
- supplying new propagating fields and calling them modes of \(\Psi\).

## Pre-registered relativistic branches

1. **R0:** canonical complex Lorentz scalar with the unique logarithmic
   interaction whose nonrelativistic envelope has coefficient \(-B\).
2. **R1:** a minimal bounded saturation completion, tested only if it preserves
   (T) in a controlled nonempty domain.
3. Higher-derivative kinetic terms or additional stabilizing fields are outside
   this issue and require a new pre-registration.

## Pass conditions

- Coefficient and sign matching are symbolic.
- A claimed \(O(\epsilon^2)\) remainder must show convergence slope at least
  1.8 under successive halvings, unless an exact analytic remainder is given.
- Stability must hold on an open parameter region, not at a fitted point.
- The kinetic matrix must have the correct exact sign.
- Numerical roots must reproduce analytic roots to relative error \(10^{-8}\)
  away from degeneracies.
- A scalar Goldstone counts as one spin-0 mode. It is not counted as two photon
  helicities without a representation-level derivation.
- An upstream failure is not overridden by adding a healthy decoupled sector.

## Instruments

- `instruments/model_hssv/ssv_target_audit.py`
- `instruments/model_hssv/relativistic_logse_bridge.py`
- `instruments/model_hssv/shared_eft_audit.py`
- `instruments/model_hssv/run_issue180.py`
- mirrored tests in `instruments/test/model_hssv/`

## Decision categories

- **K1:** the literal target passes in one shared theory without independently
  supplying its missing sectors.
- **K2:** compatibility requires independent fields or structural additions,
  but the frozen SSV limit itself remains controlled and stable.
- **K3:** the frozen SSV target is already unstable/inconsistent, or the
  required sectors cannot coexist under the declared assumptions.

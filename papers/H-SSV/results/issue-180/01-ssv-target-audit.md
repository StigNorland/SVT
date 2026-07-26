# Issue #180 — literal SSV target audit

Status: **closure-grade negative result**

Gate: **P0 FAIL**

## Result

The homogeneous state of the literal Paper-I equation is modulationally
unstable for the declared \(B=b\rho_0>0\). The equation does not produce the
positive sound cone printed in the paper.

This result follows from the equation itself and is independent of the
normalization ambiguity in the displayed Lagrangian.

## Direct linearization

Write the target in the homogeneous convention \(\bar\rho=\rho_0\):

\[
i\hbar\dot\Psi=-\frac{\hbar^2}{2m}\nabla^2\Psi
-B\ln|\Psi|^2\Psi,\qquad B>0.
\]

Perturb

\[
\Psi=1+u+iv,\qquad |u|,|v|\ll1,
\]

so \(\ln|\Psi|^2=2u+O(u^2,v^2)\). With
\(K=\hbar^2/(2m)\), the real linear system is

\[
-\hbar\dot v=-K\nabla^2u-2Bu,
\qquad
\hbar\dot u=-K\nabla^2v.
\]

For \(u,v\propto e^{i(\mathbf k\cdot\mathbf x-\omega t)}\), its determinant
gives

\[
\hbar^2\omega^2
=\epsilon_k(\epsilon_k-2B),
\qquad
\epsilon_k=\frac{\hbar^2k^2}{2m}.
\tag{1}
\]

Consequently

\[
\omega^2<0
\quad\text{for}\quad
0<k<\frac{2\sqrt{mB}}{\hbar},
\]

and

\[
\lim_{k\to0}\frac{\omega^2}{k^2}=-\frac{B}{m}.
\tag{2}
\]

Paper I instead claims \(c_s^2=2B/m>0\). The signs are opposite and the
magnitudes differ by a factor of two. This is not a convention change:
changing it requires changing the curvature of the nonlinear term at the
background.

The printed high-\(k\) expression is inconsistent as well. Substituting the
paper's \(c_s\) and \(\xi\) into
\(c_s^2k^2(1+k^2\xi^2)\) gives an ultraviolet \(k^4\) coefficient four times
the free Schrödinger coefficient in (1).

## Thermodynamic cross-check

For the printed

\[
V(\rho)=-b\rho[\ln(\rho/\bar\rho)-1]+V_0,
\]

the standard barotropic combination is

\[
P=\rho V'(\rho)-V(\rho)=-b\rho-V_0,
\qquad
\frac{dP}{d\rho}=-b.
\tag{3}
\]

Thus the compressibility sign obtained independently from the potential
agrees with the negative \(k^2\) term in (2), not with the positive pressure
and sound speed printed in Paper I.

## Conserved current and Madelung check

The global phase symmetry still gives the usual LogSE norm current,

\[
n=|\Psi|^2,\qquad
\mathbf j=\frac{\hbar}{m}\operatorname{Im}(\Psi^*\nabla\Psi),
\qquad
\dot n+\nabla\cdot\mathbf j=0.
\]

Writing \(\Psi=\sqrt n e^{i\theta}\) and
\(\mathbf v=(\hbar/m)\nabla\theta\) reproduces continuity and the Euler
equation with the quantum-pressure term. The nonlinear chemical potential is
\(\mu(n)=-B\ln(n/n_0)\), so
\[
\mu'(n_0)=-\frac{B}{n_0}<0.
\]
The hydrodynamic derivation therefore gives the same negative compressibility
as the direct Bogoliubov determinant. Conservation of norm does not imply
stability.

## Normalization audit

Because \(\Psi\) is declared dimensionless and \(B=b\rho_0\) has energy units,
the displayed terms can be read consistently as energies per reference
element. The paper does not uniquely specify the additional normalization
needed to regard the expression as a physical action density integrated over
\(d^3x\). This is an under-specification, but it is not used to obtain the
failure: multiplying the entire action by a positive common factor cannot
change (1).

## Controls

`ssv_target_audit.py` independently records:

- the exact symbolic determinant
  \(\epsilon_k(\epsilon_k-2B)\);
- the analytic instability boundary;
- negative numerical \(\omega^2\) at four preregistered points inside the band;
- positive values from the paper's claimed formula at the same points;
- \(dP/d\rho=-b\);
- the action-normalization ledger.

The mirrored tests reproduce all of these statements.

## Gate decision

P0 required a well-defined stable stationary background. The literal uniform
SSV state fails that requirement. This is already **K3 for literal SSV**.

A neighboring sign-reversed logarithmic theory is retained only as a blind
control in the next stage. It is not relabelled as SSV.

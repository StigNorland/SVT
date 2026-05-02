# Symbolic Two-Mode Reduction for the Muon in SSV

This note derives the reduced two-mode model for the muon directly from the SSV Lagrangian, up to explicit background-dependent projection integrals.

## 1. Starting point

Take the action
\[
S = \int dt\, d^3x \left( \mathcal L_0 + \mathcal L_\perp \right),
\]
with
\[
\mathcal L_0
=
\frac{i\hbar}{2}\left(\Psi^\ast \partial_t \Psi-\Psi \partial_t \Psi^\ast\right)
-\frac{\hbar^2}{2m_0}|\nabla\Psi|^2
-V(\rho),
\]
\[
V(\rho)=-b\,\rho\ln(\rho/\bar\rho)-1+V_0,
\qquad
\rho=\rho_0 |\Psi|^2,
\]
and
\[
\mathcal L_\perp
=
-\frac{\lambda\hbar^2}{2m_0\rho_0}\,(\nabla\times j)^2,
\qquad
j=\frac{\hbar}{2m_0 i}\left(\Psi^\ast \nabla\Psi-\Psi\nabla\Psi^\ast\right).
\]

Let \(\Psi_0(\mathbf x;R_e)\) be the static equilibrium toroidal solution at major radius \(R_e\).

## 2. Collective-coordinate ansatz

Introduce two soft coordinates:

- \(q(t)\): fractional major-radius breathing,
- \(\chi(t)\): amplitude of the lowest chiral transverse fluctuation.

Define
\[
R(t)=R_e[1+q(t)].
\]

The fluctuation ansatz is
\[
\Psi(\mathbf x,t)
=
e^{-i\mu_{\rm chem} t/\hbar}
\Big[
\Psi_0(\mathbf x;R_e)
+q(t)\,\Phi_R(\mathbf x)
+\chi(t)\,\Phi_\chi(\mathbf x)
\Big],
\]
where
\[
\Phi_R(\mathbf x)\equiv R_e\,\partial_R \Psi_0(\mathbf x;R)\big|_{R=R_e}
\]
is the tangent vector to toroidal breathing, and \(\Phi_\chi\) is the lowest localized chiral mode.

For a real reduced action it is useful to keep the mode pair closed under conjugation. One may
equivalently regard the ansatz as a restricted BdG basis
\[
\delta\Psi = q\,\Phi_R + \chi\,\Phi_\chi,
\qquad
\delta\Psi^\ast = q\,\Phi_R^\ast + \chi\,\Phi_\chi^\ast,
\]
with \(q,\chi\in\mathbb R\).

## 3. Quadratic expansion: general structure

Because \(\Psi_0\) satisfies the static Euler-Lagrange equation, the linear term vanishes. The
effective action begins at quadratic order:
\[
S^{(2)}=\frac12 \int dt \left[
\sum_{a,b\in\{R,\chi\}}
\mathcal M_{ab}\,\dot Q_a \dot Q_b
-\mathcal K_{ab}\,Q_a Q_b
\right],
\]
where
\[
Q_R=q,\qquad Q_\chi=\chi.
\]

If the basis is chosen parity-adapted, the off-diagonal kinetic term can be made to vanish at
leading order, leaving
\[
S^{(2)}=\frac12 \int dt \left[
M_R \dot q^2 + M_\chi \dot\chi^2 - K_R q^2 - K_\chi \chi^2 - 2G q\chi
\right].
\]

The task is therefore to identify \(M_R, M_\chi, K_R, K_\chi, G\) as projection integrals over
the background torus.

## 4. Symplectic/time-derivative sector

The first-order Schrödinger term does not itself produce a standard positive kinetic energy.
To obtain a second-order oscillator form one integrates out the fast phase-conjugate sector, or
equivalently works in the restricted BdG basis and projects the generalized eigenvalue problem.

The reduced matrices are therefore best defined by
\[
\mathsf H_{ab} = \langle \Phi_a, \hat{\mathcal H}_{\rm BdG}\,\Phi_b\rangle_B,
\qquad
\mathsf N_{ab} = \langle \Phi_a,\Phi_b\rangle_B,
\]
where \(\hat{\mathcal H}_{\rm BdG}\) is the full quadratic BdG operator from \(\mathcal L_0+\mathcal L_\perp\),
and \(\langle\cdot,\cdot\rangle_B\) is the BdG symplectic inner product.

The reduced eigenproblem is
\[
\mathsf H X = \hbar\omega\,\mathsf N X.
\]

Near a nonrelativistic normal-mode regime this generalized eigenproblem can be rewritten in
oscillator form
\[
\mathsf K X = \omega^2 \mathsf M X,
\]
which defines the reduced mass and stiffness matrices.

## 5. LogSE contribution to the stiffness matrix

Write the static energy functional
\[
E[\Psi]
=
\int d^3x
\left[
\frac{\hbar^2}{2m_0}|\nabla\Psi|^2 + V(\rho)
\right].
\]

Then the LogSE contribution to the quadratic stiffness is the Hessian of \(E\) at \(\Psi_0\):
\[
K^{(0)}_{ab}
=
\left.
\frac{\partial^2 E[\Psi_0 + Q_R\Phi_R + Q_\chi\Phi_\chi]}
{\partial Q_a\,\partial Q_b}
\right|_{Q=0}.
\]

Equivalently,
\[
K^{(0)}_{ab}
=
\int d^3x\,
\begin{pmatrix}
\Phi_a^\ast & \Phi_a
\end{pmatrix}
\begin{pmatrix}
\hat L_0 & \hat M_0 \\
\hat M_0^\ast & \hat L_0^\ast
\end{pmatrix}
\begin{pmatrix}
\Phi_b \\
\Phi_b^\ast
\end{pmatrix}.
\]

Thus
\[
K_R = K^{(0)}_{RR}+K^{(\perp)}_{RR},\qquad
K_\chi = K^{(0)}_{\chi\chi}+K^{(\perp)}_{\chi\chi},\qquad
G = K^{(0)}_{R\chi}+K^{(\perp)}_{R\chi}.
\]

## 6. Explicit LogSE Hessian pieces

For \(\delta\Psi = Q_a \Phi_a\), the density variation is
\[
\delta\rho = \rho_0\left(\Psi_0^\ast \delta\Psi + \Psi_0 \delta\Psi^\ast\right),
\]
and at quadratic order
\[
\delta^2 E_0
=
\int d^3x
\left[
\frac{\hbar^2}{2m_0} |\nabla\delta\Psi|^2
+\frac12 V''(\rho_0 |\Psi_0|^2)\,(\delta\rho)^2
\right],
\]
with
\[
V''(\rho) = -\frac{b}{\rho}.
\]

Therefore the LogSE contributions are
\[
K^{(0)}_{ab}
=
\int d^3x
\left[
\frac{\hbar^2}{2m_0}\,\Re\big(\nabla\Phi_a^\ast\!\cdot\nabla\Phi_b\big)
+\frac12 V''(\rho_0|\Psi_0|^2)\,\delta\rho_a\,\delta\rho_b
\right],
\]
where
\[
\delta\rho_a=\rho_0\left(\Psi_0^\ast \Phi_a + \Psi_0 \Phi_a^\ast\right).
\]

This gives directly
\[
K^{(0)}_{RR},\quad K^{(0)}_{\chi\chi},\quad K^{(0)}_{R\chi}.
\]

## 7. Chiral-shear contribution

Define the background current
\[
j_0=\frac{\hbar}{2m_0 i}\left(\Psi_0^\ast \nabla\Psi_0-\Psi_0\nabla\Psi_0^\ast\right),
\]
and first-order current variation
\[
\delta j_a
=
\frac{\hbar}{2m_0 i}
\left(
\Phi_a^\ast \nabla\Psi_0
+\Psi_0^\ast \nabla\Phi_a
-\Phi_a \nabla\Psi_0^\ast
-\Psi_0 \nabla\Phi_a^\ast
\right).
\]

Since
\[
E_\perp[\Psi]
=
\int d^3x\,
\frac{\lambda\hbar^2}{2m_0\rho_0}(\nabla\times j)^2,
\]
the quadratic contribution is
\[
K^{(\perp)}_{ab}
=
\frac{\lambda\hbar^2}{m_0\rho_0}
\int d^3x\,
(\nabla\times \delta j_a)\cdot(\nabla\times \delta j_b).
\]

Hence the ring-chiral coupling is explicitly
\[
G
=
K_{R\chi}
=
K^{(0)}_{R\chi}
+\frac{\lambda\hbar^2}{m_0\rho_0}
\int d^3x\,
(\nabla\times \delta j_R)\cdot(\nabla\times \delta j_\chi).
\]

This is the main structural result: the muon-relevant mixing is an overlap between the
vorticity content of the breathing deformation and the localized chiral fluctuation.

## 8. Reduced mass matrix

The effective mass matrix comes from the dynamical BdG norm after projection. In practice,
for a mode basis \(\Xi_a=(\Phi_a,\Phi_a^\ast)^T\),
\[
N_{ab} = \langle \Xi_a,\sigma_3 \Xi_b\rangle
=
\int d^3x \left(\Phi_a^\ast \Phi_b - \Phi_a \Phi_b^\ast\right),
\]
and the reduced second-order mass matrix may be defined from the low-frequency expansion of
the projected generalized eigenproblem.

Operationally one computes
\[
\mathsf H(\omega) X = \hbar\omega\, \mathsf N X
\]
and expands near the target mode. This yields
\[
M_{ab}
=
\left.
\frac{1}{2\omega}
\frac{\partial}{\partial\omega}
\det\!\big(\mathsf H-\hbar\omega \mathsf N\big)
\right|_{\omega=\omega_\star}
\times
\text{projection factors}.
\]

For the reduced phenomenological model one usually chooses a normalization such that
\[
M_R = \int d^3x\, \mathfrak m_R(\mathbf x),\qquad
M_\chi = \int d^3x\, \mathfrak m_\chi(\mathbf x),
\]
with cross term removed by orthogonalization of the basis. To leading order this is equivalent
to Gram-Schmidt orthogonalization in the projected BdG metric.

## 9. Final reduced equations

After orthogonalization, the effective equations are
\[
M_R \ddot q + K_R q + G\chi = 0,
\]
\[
M_\chi \ddot\chi + K_\chi \chi + G q = 0.
\]

Therefore
\[
\begin{pmatrix}
K_R-\omega^2 M_R & G\\
G & K_\chi-\omega^2 M_\chi
\end{pmatrix}
\begin{pmatrix}
q\\
\chi
\end{pmatrix}
=0,
\]
and
\[
(K_R-\omega^2 M_R)(K_\chi-\omega^2 M_\chi)-G^2=0.
\]

The lower root is
\[
\omega_-^2
=
\frac12\left(
\frac{K_R}{M_R}+\frac{K_\chi}{M_\chi}
\right)
-\frac12
\sqrt{
\left(
\frac{K_R}{M_R}-\frac{K_\chi}{M_\chi}
\right)^2
+4\frac{G^2}{M_R M_\chi}
}.
\]

## 10. Interpretation

The muon derivation problem is now reduced to five background-dependent quantities:

- \(M_R\): inertia of toroidal breathing,
- \(K_R\): restoring stiffness of ring expansion/compression,
- \(M_\chi\): inertia of the localized chiral mode,
- \(K_\chi\): intrinsic chiral stiffness,
- \(G\): overlap coupling between toroidal breathing and chiral vorticity.

The observed muon mass is obtained if the lowest projected eigenfrequency satisfies
\[
\hbar\omega_- = m_\mu c^2.
\]

So the symbolic result is:

\[
\boxed{
G =
\int d^3x\,
\left[
\frac{\hbar^2}{2m_0}\,\Re(\nabla\Phi_R^\ast\!\cdot\nabla\Phi_\chi)
+\frac12 V''(\rho_0|\Psi_0|^2)\,\delta\rho_R\,\delta\rho_\chi
+\frac{\lambda\hbar^2}{m_0\rho_0}
(\nabla\times \delta j_R)\!\cdot\!(\nabla\times \delta j_\chi)
\right]
}
\]

up to the basis normalization conventions. This is the explicit coefficient that must become
large enough to lift the bare ring mode to the muon scale.

# Issue #76 Tasks 1--4: SSV BdG Berry-phase quantization audit

**Date:** 2026-06-02. Analytic note for
[issue #76](https://github.com/StigNorland/SVT/issues/76).

This note completes Tasks 1--4 as an analytic calculation. The result is not
the hoped-for Berry-phase rescue of the muon rung. Tasks 1, 2, and 4 give
well-defined formulas, but Task 3 gives a no-go result for the
selection-rule-correct SSV operator: the current-curl block does not contribute
a topological holonomy of \(-1\) to the scalar LogSE BdG pair.

The calculation should therefore be read together with:

- `papers/SSV-I/path-b-eigenvalue-result.md`
- `papers/SSV-I/muon-issue72-drift-diagnostic-result.md`
- `papers/SSV-I/muon-issue72-lperp-second-variation-audit.md`
- `papers/SSV-I/muon-issue73-phi-bdg-result.md`

Bibliographic note: issue #76 cites `arXiv:cond-mat/9812131` as Volovik's
"Bound States in the Vortex Core", but that arXiv record is by Knezevic and
Radovic. The Volovik preprint whose abstract matches the Berry-phase
integer/half-integer vortex-core statement is `arXiv:cond-mat/9709159`,
"Fermions in the vortex core in chiral superconductors".

## Summary verdict

Volovik's framework is the right diagnostic question: equal CdGM-like spacing
must come from holonomy/topology, not from a generic potential-well eigenvalue
problem. In the present SSV scalar BdG operator, however, the azimuthal
holonomy around the electron torus is trivial in the pure LogSE sector, and
the implemented \(\mathcal L_\perp\) current-curl second variation does not
change it to \(-1\).

The requested Task 3 matrix element

\[
\langle K_{L,\pm}|(\nabla\times\delta j)^\dagger
(\nabla\times\delta j)|\Phi_R\rangle
\]

vanishes in the selection-rule-correct theory: \(\Phi_R\) carries
\(m_\varphi=0\), while \(K_{L,\pm}\) carries \(m_\varphi=\pm1\). The normal
\(L^\perp\) block requires \(m_a=m_b\), and the anomalous \(M^\perp\) block
requires \(m_a+m_b=0\). Neither condition is satisfied by a direct
core-breathing to Kelvin-helicity bridge.

Thus the calculation completes Tasks 1--4 in the conservative direction:

| task | result |
|---|---|
| Task 1 | SSV BdG quantization condition stated below. |
| Task 2 | Pure LogSE azimuthal holonomy is trivial; integer sector only. |
| Task 3 | No \(\pi\) Berry phase from the implemented \(\mathcal L_\perp\) block; requested bridge matrix element is zero. |
| Task 4 | Volovik spacing formula gives \(\mu_0=m_ec^2/\alpha\) as a conditional scale cross-check, not as a rung derivation. |

## Task 1: Quantization condition for the SSV BdG pair

Near the electron torus, write the fixed background in thin-ring coordinates

\[
  r-R_e = s\cos\vartheta,\qquad z=s\sin\vartheta,
  \qquad R_e={\xi\over\alpha}\gg \xi ,
\]

with scalar vortex phase

\[
  \Psi_0(s,\vartheta)=f_0(s/\xi)e^{ik\vartheta},
  \qquad k=1.
\]

The phase winding of the electron torus is meridional, in
\(\vartheta\), not azimuthal in \(\varphi\). The \(\varphi\)-direction is the
large circle of the torus.

For an azimuthal Fourier sector \(m\in{\mathbb Z}\), write a BdG perturbation
as a Nambu pair

\[
  \delta\Psi(t,s,\vartheta,\varphi)
  =
  u_m(s,\vartheta)e^{im\varphi}e^{-i\omega t}
  +v_m^\ast(s,\vartheta)e^{-im\varphi}e^{i\omega t}.
\]

Equivalently, introduce the Nambu spinor

\[
  \Xi_m(\varphi)
  =
  \begin{pmatrix}
    u_m(s,\vartheta)e^{im\varphi}\\
    v_m(s,\vartheta)e^{-im\varphi}
  \end{pmatrix}.
\]

The BdG inner product is the Krein, or \(SU(1,1)\), product

\[
  \langle \Xi,\Eta\rangle_K
  =
  \int_\Sigma
  \left(u_\Xi^\ast u_\Eta-v_\Xi^\ast v_\Eta\right)
  R_e\,s\,ds\,d\vartheta ,
\]

where \(\Sigma\) is a meridional cross-section of the projection tube. For a
normalized positive-Krein mode, \(\langle\Xi,\Xi\rangle_K=1\), the Berry
connection around the azimuthal circle is

\[
  \mathcal A_\varphi
  =
  -i\,\langle \Xi_m,\partial_\varphi\Xi_m\rangle_K.
\]

The SSV analog of the Volovik semiclassical quantization condition is

\[
  \boxed{
  \oint_0^{2\pi}
  \left(p_\varphi+\mathcal A_\varphi\right)d\varphi
  =
  2\pi n ,
  }
  \tag{1}
\]

or, after isolating the geometric part,

\[
  \boxed{
  E_n =
  \left(n+{\gamma_B\over2\pi}\right)\omega_0,
  \qquad
  \gamma_B=\oint_0^{2\pi}\mathcal A_\varphi\,d\varphi
  \pmod{2\pi}.
  }
  \tag{2}
\]

Here \(\omega_0\) is the microscopic level spacing scale. The only way to
obtain a protected half-integer ladder from Eq. (2) is to show

\[
  \exp(i\gamma_B)=-1,\qquad \gamma_B=\pi\pmod{2\pi}.
\]

Because the SSV order parameter is scalar, not a fermionic spinor, such a
minus sign cannot be assumed. It must be produced by a genuine winding of the
BdG eigenbundle or by an explicit half-winding in the off-diagonal Nambu
coupling.

## Task 2: Pure LogSE vortex gives trivial azimuthal Berry phase

With \(\mathcal L_\perp=0\), the LogSE BdG operator on the toroidal background
is invariant under \(\varphi\)-translations and diagonal in integer
\(m_\varphi\). The azimuthal dependence of a mode is exhausted by the integer
Fourier factors \(e^{\pm im\varphi}\).

For the spinor \(\Xi_m\) above,

\[
  \partial_\varphi\Xi_m
  =
  i m
  \begin{pmatrix}
    u_m e^{im\varphi}\\
    -v_m e^{-im\varphi}
  \end{pmatrix}.
\]

Thus

\[
  \mathcal A_\varphi
  =
  m
  \int_\Sigma
  \left(|u_m|^2+|v_m|^2\right)R_e\,s\,ds\,d\vartheta ,
\]

up to the conventional normalization of the canonical action variable. This
term is the ordinary integer azimuthal action, not an additional topological
Berry phase. It may be absorbed into \(p_\varphi\) in Eq. (1). The remaining
geometric holonomy is

\[
  U_B^{\rm LogSE}
  =
  \exp(i\gamma_B^{\rm LogSE})
  =
  \exp(i2\pi m)
  =
  1 ,
  \qquad m\in{\mathbb Z}.
\]

Equivalently,

\[
  \boxed{\gamma_B^{\rm LogSE}=0\pmod{2\pi}.}
\]

This is the integer sector:

\[
  \boxed{E_n=n\,\omega_0.}
\]

The result is consistent with the electron torus winding \(k=1\): that winding
lives around the meridional core angle \(\vartheta\). It does not by itself
produce a spinorial sign change when a scalar BdG pair is carried once around
the azimuthal circle \(\varphi:0\to2\pi\).

**Lemma.** For the pure scalar LogSE BdG operator on the \(k=1\) electron
torus, every integer-\(m_\varphi\) azimuthal mode has trivial Berry holonomy
around the major ring. The pure sector can support integer rungs only.

This gives an integer-sector consistency check for any pion-style
two-winding/topological-boundary argument, but it does not derive a
half-integer muon rung.

## Task 3: Current-curl block does not give \(\gamma_B=\pi\)

The \(\mathcal L_\perp\) energy used in the repo is

\[
  E_\perp[\Psi]
  =
  {\lambda\over2}\int |\nabla\times j[\Psi]|^2\,d^3x,
  \qquad
  j={1\over2i}(\Psi^\ast\nabla\Psi-\Psi\nabla\Psi^\ast).
\]

The issue #72 audit decomposes the second variation as

\[
  j=j_0+\epsilon j_1+\epsilon^2 j_2+O(\epsilon^3),
\]

so the quadratic current-curl form is

\[
  {1\over2}\int |\nabla\times j_1|^2\,d^3x
  +
  \int (\nabla\times j_0)\cdot(\nabla\times j_2)\,d^3x .
\]

In BdG block form this gives

\[
  H_{\rm BdG}
  =
  \begin{pmatrix}
    L & M\\
    -M^\ast & -L^\ast
  \end{pmatrix},
  \qquad
  L=L^{\rm LogSE}+\lambda_\perp L^\perp,\quad
  M=M^{\rm LogSE}+\lambda_\perp M^\perp.
\]

Azimuthal integration enforces the selection rules

\[
  \boxed{L^\perp_{ab}\neq0\Rightarrow m_a=m_b,}
  \qquad
  \boxed{M^\perp_{ab}\neq0\Rightarrow m_a+m_b=0.}
\]

These are exactly the rules implemented in `kelvin_augmented_bdg.py` and
verified in issues #72 and #73.

Let the ring-breathing mode be

\[
  \Phi_R=R_e\,\partial_R\Psi_0,\qquad m_\varphi(\Phi_R)=0,
\]

and let a Kelvin helicity mode be

\[
  K_{\sigma,\pm}
  =
  {1\over\sqrt2}(K_r+\sigma iK_z)e^{\pm i\varphi},
  \qquad m_\varphi(K_{\sigma,\pm})=\pm1.
\]

The requested Task 3 bridge matrix element is therefore forbidden:

\[
  L^\perp_{K_{\sigma,\pm},\Phi_R}=0
  \quad\hbox{because}\quad
  \pm1\neq0,
\]

and

\[
  M^\perp_{K_{\sigma,\pm},\Phi_R}=0
  \quad\hbox{because}\quad
  \pm1+0\neq0.
\]

Equivalently,

\[
  \boxed{
  \langle K_{\sigma,\pm}|(\nabla\times\delta j)^\dagger
  (\nabla\times\delta j)|\Phi_R\rangle=0
  }
  \tag{3}
\]

for the selection-rule-correct scalar current-curl operator.

Inside the direct \(m_\varphi=\pm1\) sector, \(\mathcal L_\perp\) can still
modify \(L_{+,+}\), \(L_{-,-}\), and the anomalous pairing \(M_{+,-}\). But
the coefficients are independent of \(\varphi\) in the thin-ring background.
The local Nambu block has the schematic form

\[
  H_m^\perp
  =
  \begin{pmatrix}
    a_m & b_m\\
    -b_m^\ast & -a_m^\ast
  \end{pmatrix},
  \qquad
  \partial_\varphi a_m=\partial_\varphi b_m=0.
\]

A \(\varphi\)-independent off-diagonal Nambu mass can change eigenvalues and
Krein signatures, but it does not create a Berry-phase sign. Its normalized
eigenvectors can be chosen independent of \(\varphi\), apart from the integer
Fourier factors already accounted for in Task 2. Therefore

\[
  \gamma_B^{\rm LogSE+\mathcal L_\perp}
  =
  \gamma_B^{\rm LogSE}
  =
  0\pmod{2\pi}
\]

for the implemented scalar current-curl block.

To obtain \(\gamma_B=\pi\), the Nambu eigenbundle would need a genuine
half-winding, for example an off-diagonal phase of the form

\[
  b(\varphi)=|b|e^{i\varphi}
\]

with eigenvectors rotating by half an angle around the ring, or an underlying
fermionic/spinorial order parameter. The SSV scalar LogSE BdG pair and the
audited \(\mathcal L_\perp\) current-curl block contain neither ingredient.

**Task 3 conclusion.** The key calculation does not close in the direction
proposed by issue #76. The implemented \(\mathcal L_\perp\) term does not
convert the integer scalar BdG sector into a half-integer sector. The muon
identification

\[
  m_{\mu^\pm}={3\over2}\mu_0
\]

is not analytically derived by Volovik-style Berry holonomy for the current
SSV operator.

## Task 4: Conditional \(\mu_0\) scale from Volovik's spacing formula

Volovik's CdGM scale has the form

\[
  \omega_0\sim{\Delta^2\over E_F}.
\]

As a dimensional SSV cross-check, identify

\[
  \Delta_{\rm SSV}=m_ec^2,
\]

the lightest stable defect energy fixed by the Lamb-formula electron
construction, and identify the chiral-shear microscopic scale

\[
  E_{\rm shear}
  =
  {\hbar c_\perp\over\xi}
  =
  \alpha\,{\hbar c\over\xi}
  =
  \alpha\,m_ec^2 ,
\]

using \(c_\perp=\alpha c\) and \(\xi=\hbar/(m_ec)\). If this shear scale is
used as the \(E_F\)-analog in the Volovik spacing estimate, then

\[
  \boxed{
  \omega_0^{\rm SSV}
  =
  {\Delta_{\rm SSV}^2\over E_{\rm shear}}
  =
  {(m_ec^2)^2\over \alpha m_ec^2}
  =
  {m_ec^2\over\alpha}
  \equiv \mu_0 .
  }
\]

This is a useful independent dimensional recovery of the base ladder scale
\(\mu_0\). It is not, by itself, a derivation of either integer or
half-integer rungs. The rung offset is controlled by the Berry holonomy in
Eq. (2), and Tasks 2--3 show that the current SSV scalar BdG operator gives
trivial azimuthal holonomy.

Thus Task 4 should be cited as a scale cross-check of the Lamb-formula route:
the same combination \(m_ec^2/\alpha\) emerges from SSV vacuum scales, but the
half-integer muon rung remains unsupported.

## Consequence for issue #76

Tasks 1--4 are complete as calculations, but the result is a falsification of
the proposed analytic closure:

\[
  \boxed{
  \hbox{current SSV scalar BdG + }\mathcal L_\perp
  \hbox{ does not produce } \gamma_B=\pi .
  }
\]

The correct Task 5 action is therefore not to promote the muon and pion rungs
to "derived" in Paper I. Instead, Paper I should keep the Path B, issue #73,
and present Berry-holonomy audit as a coherent null result:

1. potential-well BdG equal spacing fails;
2. reduced Kelvin branches are not direct-sector features;
3. the current scalar current-curl operator does not supply the missing
   half-integer Berry phase.

A future positive Berry-phase ladder would require a changed microscopic
structure, such as a spinorial order parameter, a derived half-winding Nambu
mass, or a new boundary condition that explicitly changes the eigenbundle
holonomy. Those ingredients are not present in the current SSV operator.

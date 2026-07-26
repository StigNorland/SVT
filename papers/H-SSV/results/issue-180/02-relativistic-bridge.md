# Issue #180 — minimal relativistic bridge

Status: **exact formal map; physical parent fails**

Gates:

- **P1 FAIL** for the exact target parent
- **P2 PASS FORMALLY**
- **P3 FAIL**

## R0 action

Use natural units \(\hbar=c=1\), metric signature \((+---)\),
\(q=|\Phi|^2\), and the canonical action

\[
{\cal L}_{R0}
=\partial_\mu\Phi^*\partial^\mu\Phi-m^2q-W(q),
\]

\[
W(q)=-2mBq[\ln(q/q_0)-1].
\tag{4}
\]

Its field equation is

\[
(\Box+m^2)\Phi+W'(q)\Phi=0,
\qquad
W'(q)=-2mB\ln(q/q_0).
\]

The conserved \(U(1)\) current and Hamiltonian density are

\[
j^\mu=i(\Phi^*\partial^\mu\Phi-\Phi\partial^\mu\Phi^*),
\]

\[
{\cal H}=|\dot\Phi|^2+|\nabla\Phi|^2+m^2q+W(q).
\]

## Controlled envelope reduction

Set

\[
\Phi=\frac{e^{-imt}}{\sqrt{2m}}\psi,
\qquad q_0=\frac{n_0}{2m}.
\]

Without discarding anything, the covariant equation becomes

\[
i\dot\psi
=-\frac{\nabla^2}{2m}\psi
-B\ln(|\psi|^2/n_0)\psi
+\frac{\ddot\psi}{2m}.
\tag{5}
\]

For envelope energy \(E_{\rm nr}\), the last term relative to the first-order
time term is \(|E_{\rm nr}|/(2m)\). It therefore vanishes in the controlled
nonrelativistic regime. Equation (5) supplies an exact symbolic coefficient
map and a known remainder; P2 passes as a formal asymptotic derivation.

The complete slow-field split may be written

\[
\Phi=\frac{1}{\sqrt{2m}}\left(e^{-imt}\psi_+
+e^{+imt}\psi_-^*\right).
\]

R0 tests the positive-charge, well-prepared sector
\(\psi_-=O(E_{\rm nr}/m)\). Equation (5) is the exact equation obtained when
the negative-frequency slow amplitude is absent; the charge-conjugate branch
obeys the corresponding conjugate equation. If both slow amplitudes are
populated, the logarithm contains fast interference terms and a single-field
SSV equation is not the leading closed description. Thus suppressing the
antiparticle amplitude is an explicit approximation condition, not an
unmentioned deletion.

The parameter map is:

| Covariant quantity | SSV quantity |
|---|---|
| \(m\) | \(m_0\) |
| \(B\) | \(b\rho_0\) |
| \(q_0\) | \(n_0/(2m)\) |
| \(n_0\) | \(\bar\rho/\rho_0\) in the Paper-I field normalization |
| \(e^{-imt}\) | removed rest-energy phase |
| \(\ddot\psi/(2m)\) | leading relativistic correction |

The existence of a formal parent is not yet physical compatibility.

## R0 boundedness

For \(B>0\),

\[
W(q)\sim-2mBq\ln q\longrightarrow-\infty
\quad(q\to\infty).
\]

The exact parent is unbounded below. P1 therefore fails.

## Exact rotating-background spectrum

The envelope background \(\psi=\sqrt{n_0}\) corresponds to the exact rotating
solution \(\Phi=\sqrt{q_0}e^{-imt}\). Linearizing the full relativistic
equation gives the determinant

\[
(k^2-\omega^2)(k^2-\omega^2-4mB)-4m^2\omega^2=0.
\tag{6}
\]

At \(k=0\), the branches have

\[
\omega_G^2=0,\qquad
\omega_H^2=4m(m-B).
\]

The gapless branch has

\[
\omega_G^2=
-\frac{B}{m-B}k^2+O(k^4).
\tag{7}
\]

For \(0<B<m\), the massive mode is healthy but the Goldstone has negative
sound-speed squared. For \(B\ge m\), the massive branch is non-positive as
well. There is no positive-\(B\) stable region.

Thus the covariant parent faithfully preserves rather than cures the
nonrelativistic instability.

## Why a small stabilizer cannot preserve the target

The long-wavelength sign is fixed by the derivative of the nonlinear chemical
potential at the background, equivalently by the quadratic curvature of the
potential along the density direction. A stabilizer capable of changing
(2) or (7) from negative to positive must contribute at the same quadratic
order as the logarithmic term. It is therefore not a parametrically small
correction in the regime whose spectrum defines SSV.

More explicitly, write a proposed R1 envelope chemical potential as

\[
\mu_{\rm R1}(n)=-B\ln(n/n_0)+\delta\mu(n).
\]

Preserving the literal quadratic SSV limit requires
\(\delta\mu'(n_0)=0\). Stability requires

\[
\mu_{\rm R1}'(n_0)
=-\frac{B}{n_0}+\delta\mu'(n_0)>0.
\]

For \(B>0\), these conditions are mutually exclusive. A saturation term may
bound the potential at large amplitude, but unless it changes the derivative
at \(n_0\) it cannot cure the infrared mode. If it does change that derivative
enough to stabilize the mode, it changes the frozen SSV limit at leading
quadratic order. This rules out the entire R1 class defined in the
pre-registration, rather than only one guessed polynomial.

Such a completion may define a useful neighboring theory, but it does not
retain the frozen target required by G1 and G6.

## Sign-reversed blind control

The same calculation was run with \(B<0\), without calling it SSV. Then

\[
W(q)\to+\infty,\qquad
c_G^2=\frac{|B|}{m+|B|}>0,\qquad
\omega_H^2=4m(m+|B|)>0.
\]

This control demonstrates that the instrument recognizes a stable
logarithmic relativistic scalar when the sign permits one. It also reveals a
second incompatibility:

\[
0<c_G^2<1
\]

for every finite coupling. The Goldstone reaches the metric light cone only
in the singular \(|B|/m\to\infty\) limit, whereas a controlled
nonrelativistic reduction requires characteristic envelope energies,
including the nonlinear scale, to be small relative to \(m\).

## Decision

The exact target has a controlled formal covariant map, but no stable canonical
parent. The sign-reversed stable control is not the SSV limit. P1 and P3 fail.

Primary mathematical context for nonlinear Klein–Gordon to Schrödinger limits:
[Machihara, Nakanishi & Ozawa (2002)](https://doi.org/10.1007/s002080200008).
The issue-180 coefficient map is derived explicitly above and does not rely on
that paper for its sign.

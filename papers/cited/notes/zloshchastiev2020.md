# zloshchastiev2020 — paragraph-level citation evidence

K. G. Zloshchastiev, *Superfluid vacuum theory and deformed dispersion
relations*, International Journal of Modern Physics A **35**, 2040032 (2020),
DOI `10.1142/S0217751X20400321`, arXiv:2011.11897.

Primary source: <https://arxiv.org/abs/2011.11897> · local PDF
`papers/cited/pdf/zloshchastiev2020.pdf` · SHA-256
`8aff20eb75784f6db483cb3a4ec03d715441f77d2ac544cd6aeecab362818e92`.
The repository retrieval pin is the matching prefix `8aff20eb75784f6d`.

## SSV-I sites checked

Paper I uses this source at four load-bearing sites:

- the lineage statement preceding `eq:Lag`, where the logarithmic
  nonlinearity is described as the form used in superfluid-vacuum theory;
- `eq:LogSE`, with the explicit convention map
  \(B=-\hbar b_{\rm src}=m_0b>0\);
- `eq:cs-routes-agree` through `eq:xi`, where Paper I derives
  \(b=c_s^2=c^2\) and
  \(\xi=\hbar/(\sqrt2\,m_0c)\);
- the claim-status table, which classifies the stable LogSE branch as an
  adopted postulate rather than a result proved by the citation.

The source is not cited for Paper I's pressure law, exact Bogoliubov
dispersion, healing-length normalization, or stability choice. Those are
derived from Paper I's dimensionally complete action.

## Relied-on source paragraph — logarithmic constraint and Eq. (1), p. 1

The complete paragraph containing the relied-on result reads:

> SVT assumes that physical vacuum is described by a similar equation, while
> photon-like excitations are analogous to acoustic waves in superfluid which
> propagate with the velocity \(c_s\propto\sqrt{p'(\rho)}\), where prime
> denotes a derivative. The correspondence principle requires that in
> low-momenta limit, SVT must recover Einstein's theory of relativity. One of
> postulates of the latter implies that the speed of photon-like excitations
> of vacuum should not depend on density, at least in a leading order with
> respect to \(\hbar\). At low momenta, \(c_s\) tends to \(c_0\approx c\).
> As shown in Ref. 5, this results in the following equation
> \(\rho|F'(\rho)|=mc_s^2/\hbar\approx\operatorname{const}(\rho)\).
> The solution of this differential equation is a logarithmic function:
> \(F(\rho)=b\ln(\rho/\bar\rho)\), where \(b\) and \(\bar\rho\) are real
> parameters. The wave equation thus becomes
> \(i\partial_t\Psi=[-\hbar\nabla^2/(2m)+V_{\rm ext}
> -b\ln(|\Psi|^2/\bar\rho)]\Psi\). (1)

This paragraph establishes the lineage of the logarithmic wave equation. In
the source equation the coefficient \(b_{\rm src}\) has dimensions of
frequency because the equation is divided by \(\hbar\). Applying the same
paragraph's constraint to
\(F=b_{\rm src}\ln(\rho/\bar\rho)\) gives
\[
  |b_{\rm src}|=\frac{m c_s^2}{\hbar},
\]
with no factor of \(\rho_0\). Paper I's stable-branch map
\(-\hbar b_{\rm src}=m_0b\), where \(b\) is mass-specific energy, therefore
gives \(b=c_s^2\).

**Verdict for lineage and coefficient map: `OK`.** The source supports the
logarithmic nonlinearity and the magnitude relation after dimensions and sign
conventions are made explicit. It does not choose Paper I's stable sign: the
absolute value leaves that choice open.

## Governing-equation and normalization context, p. 1

The immediately preceding paragraph defines a condensate wavefunction obeying
\[
 i\partial_t\Psi
 =[-\hbar\nabla^2/(2m)+V_{\rm ext}-F(|\Psi|^2)]\Psi
\]
and normalizes \(\int_V|\Psi|^2\,dV=M>0\). This is consistent with treating
the nonlinear term in Eq. (1) as a wave-equation frequency. It does not
identify \(F\) as a pressure or supply Paper I's energy-density action.

**Verdict for a pressure attribution: `NOT SUPPORTED`.** Paper I must obtain
\(P=\rho\mu-V=b\rho\) from its own energy density; the citation cannot be used
as a pressure equation of state.

## Positive-source-\(b\) solution, p. 1

The paragraph following Eq. (1) says the known ground state for positive
source \(b\) is a Gaussian wave packet (a radial Gaussian in the rotationally
symmetric three-dimensional case), citing Rosen and
Bialynicki-Birula–Mycielski. Because Eq. (1) contains \(-b_{\rm src}\ln\),
that source-positive branch is the attractive Gausson branch. Under Paper I's
map it corresponds to negative mass-specific \(b\), not to the stable
homogeneous branch adopted in Paper I.

**Verdict for simultaneous Gausson and stable vacuum: `CONTRADICTED`.** The
pure one-component logarithmic model cannot provide both signs at once.

## Printed natural scale below Eq. (2), p. 2

The source defines the de Broglie momentum using

> \(p_a=2\hbar/a\), corresponding to the length scale
> \(a=\hbar/\sqrt{2m|b|}\).

As printed, this is dimensionally inconsistent with the frequency dimension
of \(b_{\rm src}\) in Eq. (1): \(\hbar/\sqrt{m b_{\rm src}}\) is not a length.
The dimensionally homogeneous source-convention expression would contain
\(\sqrt{\hbar}\) in the numerator. Paper I therefore does not use this line
to normalize its core scale. From its own action it obtains
\[
  \xi=\frac{\hbar}{\sqrt{2m_0(m_0b)}}
     =\frac{\hbar}{\sqrt2\,m_0c_s}.
\]

**Verdict for the printed natural-length formula: `MISDERIVED`.** It cannot
support Paper I's healing length as written; the corrected Paper I expression
is an independent derivation.

## Overall use verdict

**`OK` with explicit scope.** Zloshchastiev 2020 is the correct primary source
for the superfluid-vacuum use of a logarithmic wave equation. It supports
neither the retired \(\rho_0\)-dependent coefficient nor a factor of two, and
its printed natural-length formula is not dimensionally usable under its own
Eq. (1) convention.

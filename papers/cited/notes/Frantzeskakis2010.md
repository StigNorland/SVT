# Frantzeskakis2010 — citation evidence

D. J. Frantzeskakis, *Dark solitons in atomic Bose–Einstein condensates: from
theory to experiments*, J. Phys. A: Math. Theor. **43**, 213001 (2010).

Primary source: arXiv:1004.4071 · DOI:
10.1088/1751-8113/43/21/213001 · local PDF sha256 `2c02ff45215594c8`.

## SSV usage

SSV-III `main.tex:929–941` cites the review for an exponentially screened
Gross–Pitaevskii dark-soliton pair potential
`U(r)≈U₀ exp(-2r/ξ)`, then derives a finite virial coefficient from that
asymptotic form.

## Source result and explanation

Section 3.6.2, printed pp. 26–27, treats extremely slow, well-separated dark
solitons. After Eq. (76), it states:

> If the separation between the dark solitons is sufficiently large (i.e.,
> \(2z_0\gg1\)) then the hyperbolic sinh function in Eq. (76) can be
> approximated by its exponential asymptote, and the potential in Eq. (76) can
> be simplified as \(V_{\rm int}(z_0)\approx
> 2n_0B^2\exp(-4\sqrt{n_0}Bz_0)\).

Writing the full centre-to-centre separation as `r=2z₀`, taking a nearly black
soliton `B≈1`, and identifying the dimensionless healing scale as
`ξ=1/√n₀` gives the SSV exponential `exp(-2r/ξ)`.

**Verdict: `OK`.** The cited asymptotic screening is supported under the
source's slow, well-separated, nearly black one-dimensional soliton
assumptions. The stated `B₂` magnitude and logarithmic temperature dependence
are SSV's subsequent approximation, not results quoted from this review.

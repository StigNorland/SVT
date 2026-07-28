# Barenghi2014 — citation evidence

C. F. Barenghi, L. Skrbek, and K. R. Sreenivasan, *Introduction to
quantum turbulence*, PNAS **111**, 4647–4652 (2014).

Primary source: arXiv:1404.1909 · DOI: 10.1073/pnas.1400033111 · local PDF
sha256 `1d2967503ac87030`.

## SSV usage

SSV-III `main.tex:1112–1118` says that dimensional analysis using circulation
`κ` and vortex-line density `L` gives

```tex
\dot N_{\rm rec}=c_{\rm rec}\,\kappa\,\mathcal L^{5/2}.
```

## Source evidence

The paper defines quantized circulation on p. 2 as `κ=h/m` and gives the
azimuthal vortex velocity `v_s=κ/(2πr)`. It then defines the other dimensional
input on p. 3:

> measurement tool in 4 He, revealing the vortex line density L – the total
> length of the quantized vortex line in a unit volume.

The complete 7,278-word extracted text contains no `5/2` exponent and does not
state a reconnection-rate law. That is consistent with SSV's wording: the
formula is presented as its own dimensional inference, while the citation
supplies the physical meanings and dimensions `[κ]=L²/T` and
`[\mathcal L]=L⁻²`. Those dimensions uniquely give
`[κ\mathcal L^{5/2}]=L⁻³T⁻¹`, a rate per volume.

**Verdict: `OK`.** The cited review supports the two quantities used. The
reconnection-rate equation is not attributed to the review and should continue
to be described as a dimensional estimate with an undetermined coefficient.

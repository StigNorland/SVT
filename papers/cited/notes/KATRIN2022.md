# KATRIN2022 — citation evidence

M. Aker et al. (KATRIN Collaboration), *First direct neutrino-mass
measurement with sub-eV sensitivity*, arXiv:2105.08533; published as *Direct
neutrino-mass measurement with sub-electronvolt sensitivity*, Nature Physics
**18**, 160–166 (2022).

Primary source: arXiv:2105.08533 · DOI: 10.1038/s41567-021-01463-1 · local PDF
sha256 `e7a8377bfa12b4a4`.

## SSV usage

SSV-II `main.tex:2081–2087` cites KATRIN for a present
`\sum m_\nu < 0.45 eV` bound and describes a future KATRIN measurement
`\sum m_\nu \gtrsim 1 eV` as a falsifier.

## Source result and explanation

The introduction, printed p. 2, defines KATRIN's observable as the effective
electron-antineutrino mass squared,
`m_\nu^2=\sum_i |U_{ei}|^2m_i^2`. This is not the unweighted cosmological mass
sum `\sum_i m_i`. The abstract, printed p. 1, reports:

> The best fit to the spectral data yields \(m_\nu^2=(0.26\pm0.34)\)
> eV²/c⁴, resulting in an upper limit of \(m_\nu<0.9\) eV/c² (90% CL).
> By combining this result with the first neutrino mass campaign, we find an
> upper limit of \(m_\nu<0.8\) eV/c² (90% CL).

The paper mentions `\sum_i m_i<0.12 eV` only as a cosmological constraint from
other references. It neither reports `\sum m_\nu<0.45 eV` nor directly measures
the mass sum.

**Verdict: `MISREAD`.** The citation conflates KATRIN's
`m_\beta=\sqrt{\sum_i|U_{ei}|^2m_i^2}` with `\sum_i m_i` and assigns this paper
a numerical bound it does not contain. SSV must use the effective-mass
observable and the cited paper's `0.8 eV` limit, or separately derive a
mass-sum conversion under explicit ordering and spectrum assumptions.

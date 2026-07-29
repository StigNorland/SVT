# lelli2016 — citation evidence

F. Lelli, S. S. McGaugh, and J. M. Schombert, *SPARC: Mass Models for 175
Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves*,
Astron. J. **152**, 157 (2016).

Primary source: arXiv:1606.09251 · DOI:
10.3847/0004-6256/152/6/157 · local PDF sha256 `d089215877213661`.

## SSV usage

SSV-VI `main.tex:453–462` says SPARC provides 175 galaxies with observed
rotation curves and baryonic decompositions at each sampled radius.

## Source data and explanation

The abstract defines the sample:

> We introduce SPARC: a sample of 175 nearby galaxies with new surface
> photometry at 3.6 μm and high-quality rotation curves from previous H I/Hα
> studies.

Section 3.3 constructs the baryonic mass models. The circular contributions are
tabulated as gas, stellar disk, and bulge components; the total baryonic curve
is

```tex
V_{\rm bar}^2
 = |V_{\rm gas}|V_{\rm gas}
 + \Upsilon_{\rm disk}V_{\rm disk}^2
 + \Upsilon_{\rm bulge}V_{\rm bulge}^2.
```

The paper also states that the complete photometric, rotation-curve, and
mass-model data are publicly available.

**Verdict: `OK`.** The source supports the sample size and the resolved
`V_gas`, `V_disk`, and `V_bul` inputs described by SSV-VI.

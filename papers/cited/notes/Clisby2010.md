# Clisby2010 — evidence

N. Clisby, *Accurate estimate of the critical exponent $\nu$ for self-avoiding
walks via a fast implementation of the pivot algorithm*,
Phys. Rev. Lett. **104**, 055702 (2010) · arXiv:1002.0494 · sha256 `cca34bb00b44c599`

Cited by SSV-III `main.tex:901`.

## Why the first fetch failed

The bulk fetch mis-resolved this to Clisby's *J. Stat. Phys.* companion (the
four-dimensional SAW study). That file was **kept but renamed**
`Clisby2010_pivot_implementation_SIBLING.pdf` so it could not masquerade as the
cited work. Resolved by pinning **arXiv:1002.0494** explicitly; the correct
paper is now stored as `Clisby2010.pdf`.

## Q. Does it support SSV-III's number?

SSV-III `main.tex:901`:

> $\nu \approx 0.587597$ the self-avoiding-walk correlation-length
> exponent~\cite{Clisby2010}

**Abstract** (p. 1):

> The critical exponent $\nu$ for three-dimensional self-avoiding walks is
> determined to great accuracy; the final estimate is **$\nu = 0.587\,597(7)$**.

Reproduced in the results table (p. 5): `0.587597(7)`.

**Verdict `OK`.** Exact match, correct paper, correct journal reference. SSV-III
quotes the central value and does not misuse the uncertainty.

Downstream in SSV-III this feeds $\theta = -(1+3\nu) \approx -2.76$, which the
paper correctly describes as universal via hyperscaling $\alpha = 2 - d\nu$ at
$d=3$. Checked in the SSV-III E-gate; unaffected by D1.

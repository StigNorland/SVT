# Srednicki1993 — citation evidence

M. Srednicki, *Entropy and Area*, Phys. Rev. Lett. **71**, 666–669 (1993).

Primary source: arXiv:hep-th/9303048v2 · DOI:
10.1103/PhysRevLett.71.666 · local PDF sha256 `aed88ccf9e75cfb2`.

## SSV usage

SSV-V `main.tex:463–471` cites Srednicki for the area-law entanglement entropy
of a short-range-correlated ground state with a UV cutoff, as conceptual
support for its numerical Bogoliubov-vacuum calculation.

## Source result and explanation

The abstract, PDF p. 1, states the calculation and scaling:

> The ground state density matrix for a massless free field is traced over the
> degrees of freedom residing inside an imaginary sphere; the resulting
> entropy is shown to be proportional to the area (and not the volume) of the
> sphere.

The calculation discretizes a free massless scalar field radially with UV
cutoff `M=a^{-1}`. Equation (22), printed p. 5, gives
`S=0.30 M^2R^2`; the conclusion, printed p. 6, describes this as entropy
proportional to the inaccessible region's surface area.

**Verdict: `OK`.** The source directly establishes an area law for the
vacuum entanglement entropy in the stated free-field spherical-cut setup. It
does not establish SSV's numerical coefficient, inhomogeneous acoustic metric,
or claim of universality to five percent; those remain results of SSV's own
calculation rather than facts supplied by this citation.

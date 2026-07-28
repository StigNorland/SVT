# Lindblad1975 — citation evidence

G. Lindblad, *Completely positive maps and entropy inequalities*,
Commun. Math. Phys. **40**, 147–151 (1975).

Primary source page: DOI 10.1007/BF01609396. This pre-arXiv article's full
text was paywalled when checked on 2026-07-28; its official bibliographic
record and abstract remain accessible.

## SSV usage

SSV-III `main.tex:999–1023` invokes monotonicity of quantum relative entropy
under a completely positive trace-preserving map. It applies that result to a
proposed block transformation \(\mathcal R_b\), a fixed local-equilibrium
reference \(\sigma\), and an entropy-production functional.

## Accessible primary-source evidence

The publisher/INSPIRE abstract states:

> It is proved that the relative entropy for a quantum system is
> non-increasing under a trace-preserving completely positive map. The proof
> is based on the strong sub-additivity property of the entropy.

That is precisely the data-processing theorem cited in the first step. The
inaccessible full text prevents paragraph-level local checking, so this
record waives the full-paragraph requirement under the explicit
`paywalled-primary` exception.

**Verdict: `OK`.** Lindblad supports
\(D(\mathcal R_b\rho\Vert\mathcal R_b\sigma)\leq D(\rho\Vert\sigma)\).
Using \(\mathcal R_b\sigma=\sigma\) then gives monotonic decrease relative to
that reference. The citation does not itself establish that SSV's proposed
block transformation is CPTP, that its chosen \(\sigma\) is a fixed point, or
that the paper's separately defined \(dS/d\ln b\) is exactly the decrease of
relative entropy; those premises and the sign convention must be supplied by
SSV.

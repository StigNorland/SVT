# toomre1964 — citation evidence

A. Toomre, *On the gravitational stability of a disk of stars*, Astrophys. J.
**139**, 1217–1238 (1964).

Primary source: DOI 10.1086/147861 · pre-arXiv · open NASA ADS scan checked
on 2026-07-28. The legacy mirror timed out during local download.

## SSV usage

SSV-VI `main.tex:273–284` says its simulated stellar velocities were
initialized with Toomre-\(Q\)-controlled radial dispersion. The citation is
methodological; the simulation results themselves are local SSV computations.

## Source result and explanation

The abstract, printed p. 1217 (PDF p. 1), states:

> The minimum root-mean-square radial velocity dispersion required in any one
> vicinity for the complete suppression of all axisymmetric instabilities is
> calculated

The sentence gives the threshold as
\(\sigma_{R,\min}=3.36G\Sigma/\kappa\), repeated in Eq. (65), printed p. 1234
(PDF p. 18). The modern stellar-disk definition
\(Q=\sigma_R\kappa/(3.36G\Sigma)\) therefore makes \(Q\geq1\) the local
axisymmetric stability condition.

**Verdict: `OK`.** The source directly supports controlling initial radial
velocity dispersion with the stellar Toomre \(Q\) parameter. Its derivation
addresses local axisymmetric stability; it does not guarantee suppression of
the non-axisymmetric bar and spiral modes measured by SSV.

# hockneyeastwood1988 — citation evidence

R. W. Hockney and J. W. Eastwood, *Computer Simulation Using Particles*
(Adam Hilger/IOP Publishing, Bristol, 1988), ISBN 0-85274-392-0.

Readable source text: `https://djvu.online/file/cjOfwRgltjv1g`. Bibliographic
metadata was cross-checked against the 1988 publisher/Crossref record, DOI
10.1887/0852743920. arXiv is not applicable to this book. No reproducible local
PDF download was available on 2026-07-28.

## SSV usage

SSV-VI `main.tex:273–280` describes its FFT particle-mesh gravity solver as
using isolated, zero-padded Hockney–Eastwood boundary conditions.

## Primary-source evidence

Section 6-5-4, *Convolution Methods*, printed pp. 211–214, defines an isolated
source as one whose potential tends to zero at infinity. In two dimensions it
places the physical source in one quarter of the doubled transform mesh:

> The source distribution over the remaining three-quarters of the system is
> made identically zero. Taking the interaction of point charges as an example

The following construction periodically extends the interaction array and
evaluates the convolution by Fourier transforms. Section 6-5-5 explains the
same enlargement geometrically: doubling the mesh in every coordinate moves
the periodic images far enough away that the active region receives the
isolated-system potential. In \(d\) dimensions the transform therefore uses
\(2^dN_g\) mesh points when \(N_g\) denotes the active source mesh.

**Verdict: `OK`.** This is the cited zero-filled/doubled-grid convolution
method for isolated particle-mesh forces. The citation verifies the algorithm
class and terminology; it cannot verify that SSV's particular GPU
implementation pads, normalizes, softens, and indexes the mesh correctly.
Those are code-and-test claims.

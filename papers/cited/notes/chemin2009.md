# chemin2009 — citation evidence

L. Chemin, C. Carignan, and T. Foster, *H I kinematics and dynamics of
Messier 31*, Astrophys. J. **705**, 1395–1415 (2009).

Primary source: arXiv:0909.3846 · DOI:
10.1088/0004-637X/705/2/1395 · local PDF sha256 `757c75acab22f707`.

## SSV usage

SSV-VI `main.tex:415–418` says its M31 fit uses the full Chemin *et al.*
rotation curve over `r=1.14–38 kpc`, with `n=98` and absolute errors.

## Source data and explanation

The abstract summarizes the radial extent:

> The rotation curve is measured out to 38 kpc, showing a nuclear peak at 340
> km s−1, a dip at 202 km s−1 around 4 kpc.

Section 5.3 says the velocities are listed in Table 5. The locally cached
machine-readable transcription
`papers/SSV-VI/data/chemin2009_table4_m31_rotation_curve.csv` contains 100
radial rows. The first two (`0.38`, `0.76` kpc) have no measured rotation
velocity; the remaining **98** run from `1.14` to `38.09` kpc and carry the
source's velocity uncertainties.

The paper explains that those uncertainties combine the formal tilted-ring
fit error with the maximum difference between the approaching and receding
halves, making them conservative absolute velocity errors rather than
fractional errors.

**Verdict: `OK`.** The source table and its local transcription reproduce all
three SSV dataset descriptors: 98 usable points, 1.14–38.09 kpc, and absolute
velocity errors.

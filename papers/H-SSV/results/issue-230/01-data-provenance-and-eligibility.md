# Issue #230 — data provenance and Gate-A eligibility

This inventory records what was inspected before instrument implementation.
Remote archives are identified by SHA-256 but are not vendored; the executable
audit has no `/tmp` or network dependency.

| source | inspected artifact | SHA-256 | reusable content | Gate-A status |
|---|---|---|---|---|
| Lelli, McGaugh & Schombert (2016), SPARC | `papers/SSV-VI/data/SPARC/SPARC_Lelli2016c.mrt` | generated in receipt | distances, inclinations, luminosities, sizes, H I masses, `Vflat`, errors, quality | eligible metadata |
| Lelli, McGaugh & Schombert (2016), SPARC | `papers/SSV-VI/data/SPARC/MassModels_Lelli2016c.mrt` | generated in receipt | radial `Vobs`, errors, gas/disc/bulge contributions | eligible radial curves |
| Mancera Piña et al. (2020), arXiv:2004.14392v2 | arXiv source archive | `20f6ecd47ae6dcd5002002c06003c15f93f88ad679f554d81f07480202581925` | six-object table: masses, geometry, summary speed/dispersion/radius; figures show two rings | eligible summaries; not eligible for radial model selection |
| Mancera Piña et al. (2022), arXiv:2112.00017v2 | arXiv source archive | `27d07639cc77e27d1714e628f177d7a578da5ba24c2875a2c5e912db94b90374` | resolved AGC 114905 figures, five nearly independent rings, mass-model figures, geometry/systematics | scientific validation; numeric radial table unavailable in source |
| Mancera Piña et al. (2024), arXiv:2404.06537 | arXiv source archive | `c921b5f148d5484811d5d1dbd6f5ae149bcf33feb6e0360c27775afd2720a337` | revised photometry and inclination; mass-model figures | sensitivity context; numeric radial table unavailable in source |
| Mancera Piña et al. (2021), author download | `rotcurv_dwarfs_MP21a.zip` | `9df62285a4c0fb0b83f4d1ac66e7606da8c6928b7fd4c35a2232c0fda12f4718` | 21 dwarf `3DBarolo` ring logs, H I density profiles, drift files | potential control data; lacks the homogeneous stellar mass-profile contract needed here |

Primary-source URLs:

- <https://arxiv.org/abs/2004.14392>
- <https://arxiv.org/abs/2112.00017>
- <https://arxiv.org/abs/2404.06537>
- <https://pavel-mancera-pina.github.io/data_to_share/rotcurv_dwarfs_MP21a.zip>

## Eligibility result frozen before fitting

The SPARC side satisfies the radial likelihood contract. The UDG side does not:
the homogeneous publication supplies a population-level summary velocity and
only two rings per object, while the one well-resolved galaxy supplies its five
points graphically and makes the numeric data available on request. Therefore:

- the matched population can support a transparent summary/proxy diagnostic;
- SPARC controls can support radial baseline fits;
- a common radial UDG-versus-SPARC likelihood cannot be executed from the
  published machine-readable inputs currently in hand; and
- Gate C is ineligible because the six UDGs were selected to be fairly isolated
  and no true host-membership catalogue is supplied.

This asymmetry will be carried into the final decision, not repaired after
seeing model scores.

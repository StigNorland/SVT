# SSV II Supplemental Numerics

This directory contains numerical support material for Paper II.

## Files

- `numerical-results.md` — full results summary for all Paper II calculations:
  proton breather (gravity), time dilation check, and vortex cap mass (electroweak).
- `reconnection-barrier-results.md` — 3D GPE reconnection-barrier checks (W/Z topology).
- `data/` — curated CSV tables referenced by the reconnection-barrier note.

## Scripts (`instruments/paper_ii/`)

| Script | Topic | Status |
|---|---|---|
| `proton_breather_1d.py` | Gravity sector: `α_G` from Bjerknes formula | Complete |
| `time_dilation_check.py` | Time dilation: longitudinal vs chiral-shear mode | Complete |
| `vortex_cap_mass.py` | Corrected line tension; conditional W/Z cap arithmetic | Complete |
| `reconnection_barrier.py` | W/Z saddle (3D GPE, analytic cap formula) | Analytic ✓, 3D grid too small |
| `reconnection_supplement.py` | Topology + chiral-shear sweep | Structural checks only |
| `chiral_cap_equilibrium.py` | Candidate cap cubic; imposed radius maps to required stiffness | Complete diagnostic |
| `lperp_core_integral.py` | Corrected L_⊥ core bending check — 380× local gap | Complete |
| `weinberg_angle.py` | sin²(θ_W): Z cap radius, λ_bend_Z, φ/7 coincidence, open gapbox | Complete |
| `lperp_bphys_check.py` | Corrected/legacy exact-rescaling control — (J+K)/4 = 1.527 | Complete |
| `jbend_ring_scaling.py` | Corrected J_bend(r_max) sweep — converged within the core | Complete |
| `kelvin_wave_renorm.py` | Corrected 380× gap: LIA/KW insufficient; p=1 running still 41.7% short | Complete |

## Key results

- **`α_G` (1D spherical):** 1.60 × 10⁻³³ vs CODATA 5.91 × 10⁻³⁹ — factor ~3×10⁵ gap → open for 3D trefoil.
- **`m_W`:** 78.93 GeV only after imposing the post-hoc golden-ratio cap
  radius; conditional arithmetic, not an independent prediction.
- **`m_Z`:** 90.02 GeV after additionally importing the tree-level mixing
  relation and observed mixing angle.
- **`sin²(θ_W)`:** tree-level = PDG by SM input; best lead: φ/7 = 0.23115 (0.03% from PDG) — no SSV derivation yet.
- **Corrected chiral-shear diagnostic:** `τ = 18.624 ξ`,
  `(J+K)/4 = 1.5274`, and the local stiffness is 380× too small. Simple
  linear running is also insufficient by 41.7%. The actual cap-setting
  mechanism is open.
- **Programme status:** see [`docs/programme-claim-status.md`](../../docs/programme-claim-status.md)
  for the surviving / invalidated / genuinely-open separation.

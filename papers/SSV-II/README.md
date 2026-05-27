# SSV II Supplemental Numerics

This directory contains numerical support material for Paper II.

## Files

- `numerical-results.md` — full results summary for all Paper II calculations:
  proton breather (gravity), time dilation check, and vortex cap mass (electroweak).
- `reconnection-barrier-results.md` — 3D GPE reconnection-barrier checks (W/Z topology).
- `data/` — curated CSV tables referenced by the reconnection-barrier note.

## Scripts (`src/paper_ii/`)

| Script | Topic | Status |
|---|---|---|
| `proton_breather_1d.py` | Gravity sector: `α_G` from Bjerknes formula | Complete |
| `time_dilation_check.py` | Time dilation: longitudinal vs chiral-shear mode | Complete |
| `vortex_cap_mass.py` | Electroweak: W/Z masses, line tension, Weinberg angle | Complete |
| `reconnection_barrier.py` | W/Z saddle (3D GPE, analytic cap formula) | Analytic ✓, 3D grid too small |
| `reconnection_supplement.py` | Topology + chiral-shear sweep | Structural checks only |
| `chiral_cap_equilibrium.py` | R_cap = φ/α from λ_bend = φ³/α³ | Complete |
| `lperp_core_integral.py` | L_⊥ core bending check — 232× gap, non-local origin | Complete |
| `weinberg_angle.py` | sin²(θ_W): Z cap radius, λ_bend_Z, φ/7 coincidence, open gapbox | Complete |
| `lperp_bphys_check.py` | 232× gap step 1: b=1/2 profile check — (J+K)/4 = 1.527, gap worsens | Complete |
| `jbend_ring_scaling.py` | 232× gap step 2: J_bend(r_max) sweep — converged <0.1% by r=5 ξ | Complete |
| `kelvin_wave_renorm.py` | 232× gap step 3: LIA negligible, KW one-loop ~ ln(R/ξ) = 5.4×, insufficient | Complete |

## Key results

- **`α_G` (1D spherical):** 1.60 × 10⁻³³ vs CODATA 5.91 × 10⁻³⁹ — factor ~3×10⁵ gap → open for 3D trefoil.
- **`m_W`:** 78.93 GeV (Paper II golden-ratio formula, 1.81% below observed).
- **`m_Z`:** 90.02 GeV (tree-level, 1.29% below observed).
- **`sin²(θ_W)`:** tree-level = PDG by SM input; best lead: φ/7 = 0.23115 (0.03% from PDG) — no SSV derivation yet.
- **Chiral-shear gap:** pure LogSE gives `R_cap ~ 17 ξ` vs needed `φ/α = 222 ξ`. Variational model shows this requires `λ_bend = φ³/α³`. Three-step gap investigation completed: all local/perturbative mechanisms ruled out; gap requires linear running λ_⊥(R) ∝ R or non-local topological origin.

# SSV – Saturated Superfluid Vacuum

Code repository for the **Resonant Cosmos** framework.

## Overview

This project develops a cosmological model where:

- The quantum vacuum is treated as a **superfluid**.
- Newtonian gravity is unchanged for baryonic matter.
- Galaxy rotation curves are explained by **standing gravity waves** — resonance modes driven by the spinning central black hole, analogous to a laser cavity.
- The BH eigenfrequency scales as `f_BH = f_proton × (m_proton / M_BH)`.
- Node spacing scales as `Δr = C / M_BH`, with `C ≈ 1.8×10⁹ kpc·M☉`.
- Within the disc plane, time runs slower — this produces the flat rotation curve without dark matter.

## Files

| File | Description |
|------|-------------|
| `bh_eigenfrequency.py` | BH eigenfrequency and node spacing (Δr) calculator for any galaxy. Anchored to the proton Compton frequency. |
| `calculate_velocity_profile.py` | Galaxy rotation curve model combining Newtonian, disc, and superfluid-vortex components. |
| `calibration_analysis.py` | Derivation and verification of the calibration constant C across multiple galaxies. Includes dimensional analysis for the standing-wave amplitude A. |
| `0224.dat` | NGC 224 (M31 / Andromeda) high-resolution rotation curve data. 625 points at 0.05 kpc steps. |

## Key Relations

```
f_BH = f_p × (m_p / M_BH)       # BH eigenfrequency
Δr   = C / M_BH                  # node spacing (kpc), M_BH in M☉
C    = v_f / (f_p × m_p) × M☉   # calibration constant (derived)
Δr × r_s = A²                    # Schwarzschild invariant
```

where `f_p ≈ 2.27×10²³ Hz` is the proton Compton frequency and `r_s` is the BH Schwarzschild radius.

## Quick Start

```bash
python bh_eigenfrequency.py        # eigenfrequency table for a range of BH masses
python calculate_velocity_profile.py  # plot rotation curve for Milky Way parameters
python calibration_analysis.py     # verify C and search for A from first principles
```

## Status

The theory is internally consistent. One remaining step is the disc-soliton BdG (Bogoliubov–de Gennes) calculation to derive `A ≈ 1.35 ly` from `{c, G, ħ, Λ, m_e}` alone — which would close the theory with zero free parameters.

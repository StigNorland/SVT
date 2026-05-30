# Enrichment Attempt Findings (2026-05-27)

> **Status (2026-05-30): superseded by Path B null.** Numerical claims in this note about the muon eigenfrequency reaching $\omega/\omega_c = 0.207$, the $\delta_{\rm relax}$ calibration, the $\alpha$-harmonic ladder identification, or the $1/\sqrt{N_{\rm modes}}$ basis-truncation residual are now governed by `papers/SSV-I/path-b-eigenvalue-result.md`: that test showed the muon agreement is not basis-robust (drifts $\pm 13\%$ across 4 bases, empty window in 2 of 4) and the pion rung is absent in every basis. Structural sub-results that stand on their own (operator algebra, analytic derivations, the cubic-vertex one-loop result, dimensional setup) remain valid in isolation; what is superseded is their use as evidence for the ladder identification or as a closure path to it. Quarantined inputs: `src/_fitted_quarantine/`. Tracking: issue #66.

**Status:** enrichment test attempted and diagnosed as blocked by a cross-m
current-curl issue; findings documented here for future model revision.

## What was attempted

Following the topology-scaling prediction
([`topology-scaling-of-residual-memo.md`](topology-scaling-of-residual-memo.md)),
an enriched reduced-BdG basis was implemented and tested at n=59/hw=6 (the
matched-spacing point).  Two variants were tried:

- **`enriched`** (15 modes): combined 3 Kelvin/sign + 2 extra x-weighted
  Kelvin per sign (Ke_xR = s/xi * phi_R, Ke_xh+ = s/xi * k_helicity), plus
  2 extra x-weighted m=0 core modes (Cx_R, Cx_chi).
- **`core_enriched`** (11 modes): combined 3 Kelvin/sign (unchanged), plus
  only the 2 extra x-weighted m=0 core modes.

Both used the same parameters as the reference combined run:
`delta_relax=0.038`, `kelvin_phi_n=128`, `current_curl_model=full`,
`reduced_operator_form=weak`, `projection_window=smooth`, `window_radius=4.0`.

**Reference combined result at n=59/hw=6:**
`omega_B0 = 2.073126791e-01` (0.151% above target 2.07000e-01)

## Enriched run result (anomalous)

The `enriched` run at n=59/hw=6 produced:
```
B0: omega = 1.042505209e-01   (50% below target — completely wrong)
B1: omega = 3.743566405e-01   (81% above target)
```

At n=11/hw=3, the spectrum analysis showed large spurious eigenvalues at
~2.6, 3.7, 9.4 that are absent from combined.  These come from the
x-weighted Kelvin modes (Ke_xR, Ke_xh+).

The `core_enriched` variant (same Kelvin as combined, only extra m=0 modes)
also showed large spurious eigenvalues at ~3.4 and ~9.0 at n=11, and the
muon-like branch shifted from 0.150 (combined) to 0.131.

## Root cause diagnosis

**Cross-m current-curl coupling is the dominant mechanism.**

`current_curl_component_overlap` computes the meridional part of the curl
inner product and multiplies by 2π, implicitly assuming the azimuthal
integral gives 1.  For cross-m pairs (m_bra ≠ m_ket), the azimuthal
integral gives zero by symmetry:

```
∫ exp(i*(m_b - m_a)*phi) dphi = 2*pi * delta_{m_a, m_b}
```

However, the code does NOT enforce this selection rule.  Measuring the
cross-m elements at n=11/hw=3 (combined basis):

| pair | lambda * l_corr |
|---|---|
| ⟨R(m=0) \| L_curl \| K0(m=+1)⟩ | +0.120 |
| ⟨R(m=0) \| L_curl \| K1(m=+1)⟩ | +0.036 |
| ⟨chi(m=0) \| L_curl \| K0(m=+1)⟩ | −0.129 |
| ⟨chi(m=0) \| L_curl \| K1(m=+1)⟩ | +0.127 |

For reference, the same-m Kelvin diagonal element is 0.187–0.292.
The cross-m elements are ~40–65% of the diagonal — not perturbatively small.

**Consequence for enrichment:** Every new mode added to the basis creates
new cross-m current-curl elements.  For x-weighted modes (large amplitude
at large radii), these spurious elements are especially large, pushing
some eigenvalues to 3–9 and suppressing the muon-like branch.

**Consequence for the selection-rule fix:** Adding the selection rule
(`if bra.m_phi != ket.m_phi: return 0,0`) gives a physically correct
calculation, but the Kelvin eigenvalue then drifts downward with domain
size (0.147→0.131→0.122 at matched-spacing n=19/hw=4 → n=29/hw=6 →
n=39/hw=8) and does NOT converge to 0.207.  The cross-m coupling was
inadvertently compensating for this domain-size drift.

In other words: the current calibrated result (`omega=0.207313` at n=59,
`delta_relax=0.038`) relies on the cross-m coupling as a mechanism that
stabilises the Kelvin eigenvalue against domain-size drift.  The
delta_relax=0.038 was tuned with this coupling present.

## What this means for the topology-scaling prediction

The topology-scaling memo's claim that enrichment should reduce the 0.5%
residual to ~0.3% is not testable with the current implementation, because:

1. Adding x-weighted modes creates large spurious cross-m elements.
2. Enforcing the selection rule (needed for clean enrichment) breaks the
   domain-convergence of the Kelvin eigenvalue.

The topology-scaling prediction remains structurally sound as a theoretical
argument; the numerical test requires a physically consistent model.

## Required model revision for future work

A physically complete revision must:

1. **Enforce the azimuthal selection rule** in `current_curl_component_overlap`
   (add `if bra.m_phi != ket.m_phi: return 0+0j`).

2. **Re-examine the domain-size drift** of the Kelvin eigenvalue in the
   corrected calculation.  The drift (eigenvalue decreasing with hw at fixed
   dr) suggests the current-curl Kelvin block has a hw-dependent negative
   contribution.  This is physical: the outer torus region (larger s/xi)
   carries net negative current-curl coupling in the Kelvin sector.  The
   model needs a term that provides the correct hw-independent Kelvin shift.

3. **Re-tune delta_relax** for the corrected calculation to find the new
   lambda_perp that gives omega ~ 0.207.

4. **Design non-x-weighted enrichment modes** that add independent physics
   without large kinetic energy.  Candidates:
   - Radial Bessel-type core modes (localized near the core)
   - Gaussian-windowed variants of phi_R and phi_kelvin
   - m=±2 azimuthal Kelvin sector

## Current status of `kelvin_augmented_bdg.py`

- `combined` (10 modes): validated baseline, gives omega=0.207313 (0.151%).
  Uses cross-m current-curl coupling as calibrated.
- `enriched` (15 modes): implemented and tested.  Not suitable for
  topology-scaling test; produces omega=0.104 (50% wrong).
- `core_enriched` (11 modes): implemented, not yet run at n=59.  Not
  suitable until the cross-m issue is resolved.
- `is_kelvin_mode`: correctly excludes m=0 re-pooled modes (committed 4b869bd).
- `grid_cache_modes`: correctly uses lru_cache (committed 4b869bd).
- Cross-m issue: documented in `hermitian_current_curl_bdg_blocks`,
  NOT fixed (commit a986426).

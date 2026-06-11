# #122: rotation curve as a time-dilation-field gradient — rebuild result

**Issue:** [#122](https://github.com/StigNorland/SVT/issues/122)
**Script:** `instruments/paper_vi_a/rotation_curve_timedilation.py`
**Test:** `instruments/test/paper_vi_a/test_rotation_curve_timedilation.py` (4 pass)
**Receipt:** `papers/SSV-VI-a/results/m31_timedilation_receipt.json`

## What was rebuilt and why

The previous VI-a fit (`fit_rotation_curve.py`) did not implement the SSV gravity
mechanism: it fit a velocity *shape* `v = v_flat·sqrt((1−e^{−r/r_t})(1+εJ₀))` with
no time-dilation field, no baryonic/CBH term, and no Newtonian limit (inner region
excluded, r ≥ 4 kpc). Since SSV gravity **is** the gradient of the time-dilation /
update-capacity field (Paper IV: A = dτ/dt = 1 + Φ/c²), the rebuild models the
curve as the gradient of one field,

    v²(r) = r dΦ/dr = v²_CBH + v²_bulge + v²_disc + v²_wave,

with v²_CBH = G M_BH/r (the CBH time-dilation well — **the Newtonian/Keplerian limit
recovered as the weak-field limit, not bolted on**), measured bulge + disc baryons,
and the SSV standing-wave field v²_wave = V_w²(1−e^{−r/r₀})(1+ε J₀(πr/Δr)). The CBH
frequency enters only through Δr and is isolated in `bh_node_spacing()` as a single
swappable input.

## Structural result: the Newtonian-near-CBH limit is now present and tested

`v²_CBH(r) = G M_BH/r` exactly; v·√r is constant (Keplerian), rising as r → 0; the
wave field is core-suppressed (→ 0 in the core) and flat far out (J₀ → 0 ⇒ V_w²).
So the conceptual fix the user asked for is in place: one field, Newtonian recovered
as its weak-field limit near the CBH. (Tested.)

## Honest fit result (M31, Chemin et al. 2009 Table 4, full range r = 1.14–38 kpc, n = 98, absolute errors)

| Model | reduced χ² | RMS (km/s) | note |
|---|---|---|---|
| SSV time-dilation (all free) | 10.1 | 19.8 | **drove the baryonic disc to ~0**; wave supplies 99% of v² — collapses to the old phenomenological form |
| baryons + NFW (same baryons) | 18.3 | 30.4 | standard dark-matter model, also a poor full-range fit |
| measured baryons + CBH wave (baryons **fixed** at M31 values) | 13.5 | 28.3 | wave amplitude V_w = 230 km/s free |

**None is a statistically acceptable fit** (reduced χ² = 10–18 ≫ 1). M31's full
rotation curve is intrinsically hard (bulge/bar/warp inner structure, small HI
errors); this is not specific to SSV.

## The decisive answer to "is the flat curve produced by the CBH frequency?" — NO

Two independent ways, same conclusion:

- **Free fit:** the optimiser zeroes the visible disc (M_disc → ~5×10³ M⊙, r₀ → lower
  bound) and lets the wave field carry **99%** of v². The "wave" is acting as a free
  dark-matter amplitude, not a CBH-derived quantity.
- **Measured-baryons-fixed fit:** M31's real baryons (M_bulge = 3×10¹⁰, M_disc =
  7×10¹⁰ M⊙) give only **v_bar ≈ 110 km/s** at 38 kpc against the observed ~266 km/s.
  The CBH wave must supply v_wave ≈ 242 km/s — **~83% of v²** — and its amplitude
  V_w = 230 km/s is **fitted, not predicted from M_BH**.

In both cases the CBH frequency sets **only the wiggle spacing Δr**; the flat plateau
(the dominant feature) is a **free amplitude functionally equivalent to a dark-matter
halo normalisation**. The rotation curve is therefore *not produced by* the CBH
emitted frequency in the current framework.

## What would make it a genuine prediction

For the claim "rotation curves produced by the CBH frequency" to hold, the **flat
amplitude V_w must be derived from M_BH / f_BH** (and the medium parameters ξ, ρ₀,
α_G), not fitted. At present only Δr carries a (numerological, possibly circular —
see #42) M_BH dependence. Deriving V_w(M_BH) from the standing-wave energy density
and the update-capacity coupling is the open requirement; until then the wave term
is a relabelled halo.

## Caveats carried, not resolved
- The node-spacing constant C = ℏ²/(2Gm_e²)·α⁻¹⁶·(m_p/m_e)⁷ remains numerological and
  its cross-galaxy constancy looks circular (#42); the λ_BH ∝ M_BH vs Δr ∝ 1/M_BH
  scaling tension (VI-a §2) is untouched.
- A full bulge+disc photometric decomposition and a MOND comparison would tighten the
  baselines; the fixed baryons here use literature scale values, not a fit to M31 light.
- Paper prose (VI-a §4/§5, VI-b) not yet updated — flagged as follow-up in #122.

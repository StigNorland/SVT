# SSV IV Outline

Working title: `Gravity as Update-Capacity Gradient`

## Status

Full draft in `main.tex` (compiles). All ten sections are drafted, with no
stubs remaining. The open items are the flagged gapboxes: the
first-principles value of `G` (deferred to Paper II), the spatial half of
light deflection (Paper VII-b), and the order-unity factor in the §2
ceiling. Most of the drafted material was
worked out in Paper II §7 during the gravity rewrite and ported here when §7
was trimmed back to a foundation-level summary. Paper IV is now the dedicated
gravity paper of the series; Paper II §7 only states the mechanism compactly
and fixes `G`.

## Scope line

Gravity in SSV as the bending of motion through gradients of local time
delay -- equivalently, gradients of the medium's local update capacity.

## Main thesis

Motion and interaction draw on the same finite local change-rate of `Psi`.
The interference of the pressure waves that matter radiates slows that
change-rate (a time delay); the delay is uneven, so it forms a gradient;
motion across the gradient bends toward greatest delay. That bending is
gravity.

## Core claims

1. Proper time is the local change-rate of `Psi` (Paper III).
2. The interference of radiated waves consumes update capacity and slows
   local time.
3. The slowing is uneven -- strongest near a mass, fading with distance --
   so it forms a spatial gradient.
4. The gradient bends every trajectory that crosses it toward greatest
   delay; that bending is gravity. An object responds only to the local
   slope, never to the distant mass.
5. One potential `Phi` carries it all: `-grad Phi` is free-fall
   acceleration, `Phi/c^2` the fractional clock slowing; light deflection
   and gravitational redshift follow from the same `Phi`.
6. Gravity is attractive because the medium's nonlinearity is logarithmic:
   the interaction cross-term `-b rho_0 x_A x_B` is sign-fixed by the
   concavity of `ln`.
7. Kinematic and gravitational time dilation are one phenomenon -- the
   update budget split between internal oscillation and translation
   (motion), or reduced by interference loading.

## Section structure (as built)

1. **Introduction** -- drafted. Scope; relation to Paper II (mechanism and
   `G`) and Paper III (time as change-rate); what is deferred to VII-b and
   to VI-a/VI-b; roadmap.

2. **Update Capacity and Local Change-Rate** -- drafted (rebuilt for
   rigour). Updates are the wake-writing events of Paper III; an update must
   be grain-sized (a sub-grain change writes no wake, on the footing of the
   zero-point fluctuations Paper III excludes) and cannot beat the grain's
   light-crossing time -- so the ceiling `N_0 = c/a_p = m_p c^2/hbar`
   (`~1.4e24` per second) is argued, not assumed; a gapbox flags the
   order-unity factor. Proper time is the count of updates. One budget, two
   uses: the internal/translation split in quadrature gives the
   special-relativistic factor `sqrt(1 - v^2/c^2)` (stated honestly -- the
   quadrature rule is the SR invariant recast, not a fresh derivation).
   Loading by interference reduces the budget: the §4 cross-term shifts an
   embedded clock's energy by `m*Phi`, and since update rate is energy/hbar
   the availability `A = dtau/dt = 1 + Phi/c^2` is computed (via §5), not
   asserted; the mass cancels, so it is universal. Kinematic and
   gravitational time dilation are unified as the one budget diminished.

3. **The Physical Picture** -- drafted (ported from Paper II §7.1). The
   three-link chain: interference slows local time, the delay is uneven
   (a gradient), the gradient bends motion. Includes the wavefront /
   marching-rank picture, the body-at-rest-as-breather argument, and the
   locality point (an object responds only to the local slope of the delay).

4. **The Interference Cross-Term** -- drafted (ported from §7.3). The LogSE
   `b ln(rho/rho_0)` expansion yields the cross term
   `u_AB = -b rho_0 x_A x_B`. Three properties: survives averaging only for
   coherent waves; sign fixed attractive by the concavity of `ln`; bilinear,
   so the potential goes as `1/r`. Bjerknes credited; the `G` calculation is
   cited to Paper II.

5. **Time Dilation, Deflection, and Redshift** -- drafted (ported from
   §7.6). The four corollaries of one `Phi`: free fall `-grad Phi`; time
   dilation `dtau/dt = 1 + Phi/c^2`; light deflection; gravitational
   redshift. Gapbox: extension beyond leading order / PPN deferred to
   Paper VII-b.

6. **Path Bending and the Refraction Picture** -- drafted. The wavefront
   construction: the ocean-swell-around-an-island analogy for refraction,
   then the correction that is the section's thesis -- the refracting agent
   is a gradient of the *rate of time* `A`, not a material/density step (no
   static density blob). Particle and wave bend alike -- SSV has no point
   particles, so every moving thing is extended, the near/far-side picture
   is literal, and the defect's size cancels from the path curvature (so
   bending stays universal). Quantitative refraction: effective index
   `n = 1/A`, ray curvature from the front-tilt, and the deflection
   integral `alpha = 2GM/bc^2` for light -- exactly half the GR value
   (Einstein's 1911 result; the spatial half deferred to VII-b in a
   gapbox). Free fall is recovered from the same construction -- the
   internal oscillation's phase tilts across the extended defect, giving
   `F = -m grad Phi` -- unifying the refraction picture with the
   `-grad Phi` picture of §5.

7. **Universal Coupling and the Absence of a Graviton** -- drafted (ported
   from §7.7-7.8). Equivalence principle as the universality of
   interference; no graviton; ultraviolet cutoff at the grain scale.

8. **From Update-Capacity Gradients to Emergent Geometry** -- drafted
   (ported from §7.9). Acoustic metric; one `Phi` sets both force and clock
   rate -- the weak-field structure of general relativity. Hands off to
   Paper VII-b for the full curved-spacetime treatment.

9. **Gravity in a Medium That Remembers** -- drafted (ported from §7.10).
   Time-averaging in a recording medium; the gravitational-wave memory
   effect; forward link to Paper III.

10. **Discussion and Open Problems** -- drafted.

## Scope boundaries (keep out)

- Detailed black-hole ontology -> Paper V (Condensate Black Holes)
- Full Einstein-equation recovery, PPN coefficients, emergent metric to all
  orders -> Paper VII-b
- Cosmology -> Paper VIII
- Galaxy phenomenology (rotation curves, morphology) -> Papers VI-a, VI-b
- First-principles value of `G` / `alpha_G` -> remains the open computation
  of Paper II

## Open drafting tasks

- Decide, section by section, what is claimed as a derivation versus a
  mechanical interpretation.
- All ten sections now drafted: revisit the Introduction and Discussion for
  consistency with the completed §2 and §6.
- Optional: convert the plain `Paper II` / `Paper III` text references to
  proper citations with an SSV-series bibliography.

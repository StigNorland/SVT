# SSV IV Outline

Working title: `Gravity as Update-Capacity Gradient`

## Status

Full draft in `main.tex` (10 pages, compiles). Eight of the ten sections are
written; **§2 (Update Capacity)** and **§6 (Path Bending and the Refraction
Picture)** are stubs still to be developed. Most of the drafted material was
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

## Section structure (as built)

1. **Introduction** -- drafted. Scope; relation to Paper II (mechanism and
   `G`) and Paper III (time as change-rate); what is deferred to VII-b and
   to VI-a/VI-b; roadmap.

2. **Update Capacity and Local Change-Rate** -- *STUB.* To formalise:
   - the medium has a finite local rate of change (finite update capacity);
   - internal interaction and translational propagation are competing uses
     of the one budget;
   - proper time = local change-rate (Paper III link; `R[Psi]`);
   - loading the medium leaves less capacity, so local time runs slow;
   - the spatial gradient of remaining capacity is what the later sections
     develop as gravity.

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

6. **Path Bending and the Refraction Picture** -- *STUB.* To develop:
   - wavefront refraction in a graded time delay (the mechanical picture);
   - trajectory bending toward greatest delay as a quantitative statement;
   - the lensing integral for light grazing a mass;
   - the relation between the refraction picture and the potential gradient
     `-grad Phi`;
   - link the pressure-gradient and time-dilation language cleanly.

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

- Write §2: formalise the update-capacity concept (competing uses of one
  finite local change-rate; tie to Paper III's `R[Psi]`).
- Write §6: the quantitative refraction geometry of path bending; link the
  pressure-gradient and time-dilation language cleanly.
- Decide, section by section, what is claimed as a derivation versus a
  mechanical interpretation.
- Once §2 and §6 land, revisit the Introduction and Discussion so they
  reference the completed sections.
- Optional: convert the plain `Paper II` / `Paper III` text references to
  proper citations with an SSV-series bibliography.

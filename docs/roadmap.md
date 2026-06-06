# SSV Roadmap

This repository is now organized around a narrower paper program. The goal is to keep one main claim per paper and use issues to track derivations, evidence, objections, and writing work separately.

## Published Foundation

- `SSV I`: medium ontology, particles as topological defects, mass-ladder foundation
- `SSV II`: forces as hydrodynamic modes, gravity as part of the force-sector foundation

These are treated as fixed foundation papers. Later work may refine or supersede specific phrasing, but not rewrite their publication history.

## Working Paper Plan

1. `SSV III: Irreversible Time and Wake Entropy`
   - Time as local change in `Psi`
   - Past as present wake structure
   - Entropy as persistent wake-complexity
   - No physical time reversal

2. `SSV IV: Gravity as Update-Capacity Gradient`
   - Gravity as bending through local change-rate gradients
   - Pressure/refraction picture
   - Weak-field and path-bending consequences
   - Status: complete focused draft; first-principles `G` remains deferred

3. `SSV V: Condensate Black Holes`
   - Frozen interior, mobile whole
   - Topological spin
   - No singularity
   - Horizon as memory-bearing boundary
   - Status: complete focused draft

4. `SSV VI-a: Galactic Standing Waves and Flat Rotation Curves`
   - Disc soliton / standing-wave structure
   - Rotation curve applications
   - Focused phenomenology
   - Status: draft aligned to outline

5. `SSV VI-b: Galactic Morphology as Overtone Structure`
   - 2D disc structure
   - Azimuthal modes
   - Morphology and wiggles
   - Status: draft aligned to outline

6. `SSV VII-a: Quantum Mechanics from Hydrodynamics`
   - Madelung to Schrodinger limit
   - Measurement as reconnection
   - Uncertainty as hydraulic bound
   - Status: draft aligned to outline

7. `SSV VII-b: Emergent Geometry and the Dissolution of Quantum Gravity`
   - Geometry as macroscopic limit
   - Emergent metric
   - Why the standard quantum-gravity problem is mis-posed in SSV
   - Status: draft aligned to outline; factor-of-two horizon correction closed structurally

8. `SSV VIII: Cosmogony from the Permissive Void`
   - Void, primordial perturbation, saturation, defect nucleation
   - Status: draft aligned to outline

9. `SSV IX: CMB and Primordial Phonon Bath`
   - Keep separate from the time paper
   - Only after the cosmology pieces are tighter
   - Primordial phonon bath
   - CMB interpretation
   - Entropy-budget cosmology
   - Status: scoped outline only; no `main.tex` yet; drafting tracked by #100

10. `SSV Alpha: Fine-Structure Constant from Toroidal Vortex Geometry`
    - Core claim: `R*/ξ = α⁻¹`
    - Frames the calculation to derive `α` from 3D LogSE plus chiral-shear toroidal-vortex minimisation
    - Does not claim to derive `α` outright; specifies what computation is needed

11. `SSV Goldstone: Electromagnetic Propagation and the Goldstone Mode`
    - Repairs the EM propagation-speed issue raised in Paper II
    - Observed photon = Goldstone/Bogoliubov phase mode at c
    - Chiral-shear sector = static near-field Coulomb and magnetic topology
    - Frames the matching calculation connecting chiral-shear near field to Goldstone radiation

## Immediate Priorities

1. ~~Rebuild `SSV III` as the cleanest conceptual paper in the series.~~ **Done (2026-06).** 9-section draft complete: wake functional in closed form, all 5 channels calibrated to k_B, unified RG flow, reconnection quantum. See `papers/SSV-III/README.md`.
2. ~~Split current `SSV V` into narrower manuscripts.~~ **Done (2026-06).** SSV V = "Condensate Black Holes" (9 sections, structurally complete). QM → SSV-VII-a, geometry → SSV-VII-b, cosmogony → SSV-VIII. See `papers/SSV-V/README.md`.
3. ~~Refocus the galactic papers so they are phenomenology papers, not cosmology manifestos.~~ **Done (2026-06).** VI-a and VI-b are scoped drafts with broad cosmology removed.
4. ~~Turn the deferred `\mathcal{L}+\mathcal{L}_\perp` minimisation into an explicit numerical roadmap.~~ **Done.** See `docs/numerical-minimisation-roadmap.md`.
5. Track objections and open derivations in issues instead of burying them inside draft prose. **Ongoing** — issues #76, #77, and #78 were closed with result notes; new deferred claims should keep using that pattern.

## Numerical Closure Track

The main quantitative bottleneck is no longer conceptual sprawl but missing computation.

Use [docs/numerical-minimisation-roadmap.md](docs/numerical-minimisation-roadmap.md) as the planning document for:

- the static 3D proton-breather minimisation
- the dynamic 3D reconnection minimisation
- the validation gates that decide when a claim moves from estimate to derivation

Use [docs/claim-status.md](claim-status.md) as the compact index of claim labels,
gapboxes, and follow-up issues.

**Current status (2026-06):**
- Issue #77 **closed**: trefoil geometry minimum (R,a)=(2.5, 0.85)ξ, N_Y×F=54, grid-converged and route-independent. The grid-convergence wall that blocked #13 for the entire programme is removed.
- Issue #78 **closed**: BdG muon program retired; Route C static minima failed (`E_8/E_1 = 3.71`, not `206.77`); Route D Kelvin degeneracy refuted the exact `8^n` rule. Remaining lepton-generation options are structural extensions only, not scalar-SSV results. See `notes/volovik-mapping.md`.
- Issue #97 **open**: upgrade dynamic reconnection cap geometry from structural harness to grid-converged candidate.
- Issue #98 **open**: map the #77 static trefoil output into a documented `Q_p` / `\alpha_G` pipeline.
- Issue #99 **open**: decide whether post-#78 lepton generations move to HQV, spinorial `Psi`, or retirement.

## Working Rule

Each paper should answer one main question:

- What is time?
- What is gravity?
- What is a black hole?
- Why flat rotation curves?
- Why morphology?
- Why quantum behavior?
- Why emergent geometry?
- Why this cosmos at all?

If a draft tries to answer more than one of these at full strength, split it.

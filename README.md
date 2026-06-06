# SSV — Saturated Superfluid Vacuum

Working repository for the SSV theoretical-physics paper series.

The physical vacuum is modelled as a real macroscopic medium described by an order parameter Ψ
(LogSE). Matter consists of topological defects in Ψ. The programme derives particle masses,
forces, gravity, time, and black-hole ontology from the structure of that medium.

## Repository Layout

| Path | Contents |
|------|----------|
| `src/paper_i/` | Paper I numerical pipeline: gradient-flow static minimiser, spectral regrid, Numba kernels, BdG / muon probes |
| `src/` | Legacy galactic / BH scripts |
| `papers/` | Manuscript drafts, supplemental notes, checkpoint files |
| `notes/` | Working notes, objections log, Volovik mapping, lepton-ladder note |
| `docs/` | Roadmap, numerical roadmap, conventions, issue-workflow |
| `.github/ISSUE_TEMPLATE/` | Issue templates for paper, derivation, numerics, objection tasks |

## Paper Series Status

| Paper | Title | Draft status |
|-------|-------|-------------|
| SSV I | Topological Defects — Geometric Origin of Matter & α-Harmonic Mass Ladder | Published (Zenodo) |
| SSV II | Forces as Hydrodynamic Modes | Published |
| SSV III | Irreversible Time and Wake Entropy | **Complete draft** (9 sections) |
| SSV IV | Gravity as Update-Capacity Gradient | **Complete draft** (10 sections + appendix) |
| SSV V | Condensate Black Holes | **Complete draft** (9 sections) |
| SSV VI-a | Galactic Standing Waves and Flat Rotation Curves | Draft aligned to outline |
| SSV VI-b | Galactic Morphology as Overtone Structure | Draft aligned to outline |
| SSV VII-a | Quantum Mechanics from Hydrodynamics | Draft aligned to outline |
| SSV VII-b | Emergent Geometry and the Dissolution of Quantum Gravity | Draft aligned to outline |
| SSV VIII | Cosmogony from the Permissive Void | Draft aligned to outline |
| SSV IX | CMB and Primordial Phonon Bath | Scoped outline; `main.tex` not yet written (#100) |
| SSV Alpha | Fine-Structure Constant from Toroidal Vortex Geometry | Draft |
| SSV Goldstone | Electromagnetic Propagation and the Goldstone Mode | Draft |

Each paper answers one main question. See [docs/roadmap.md](docs/roadmap.md) for scope lines and current priorities.

## Numerical Pipeline (Paper I)

The core computation is a 3D static minimiser for topological defects in the LogSE.

**Key files:**

| File | Role |
|------|------|
| `src/paper_i/gradient_flow_numba.py` | Main static relaxer — imaginary-time gradient flow with Numba kernels (~6× speedup) |
| `src/paper_i/trefoil_geometry_scan.py` | (R, a) geometry scan for the trefoil breather |
| `src/paper_i/trefoil_state_continuation_sweep.py` | Coarse→fine spectral regrid continuation |
| `src/paper_i/trefoil_observables.py` | N_Y, F, link-count readouts |
| `src/paper_i/vortex_ring_mass_inversion.py` | Lepton mass ladder: Lamb formula inversion, 8ⁿ generation fit |
| `src/paper_i/vortex_profile.py` | LogSE radial vortex profile |

**Milestone (issue #77, 2026-06-03):** geometry minimum found at (R, a) = (2.5, 0.85) ξ, giving **N_Y×F = 54**, grid-converged to <2.5% over n=96→192 and route-independent. The grid-convergence wall that blocked the programme since #13 is removed.

**Recent track (issue #78, closed 2026-06-05):** the BdG muon programme is retired (no-go confirmed across 5 independent probes — scalar Ψ has no half-integer Berry phase). Route C and Route D also returned negative: distinct static ring minima give an energy ratio `3.71`, not `206.77`, and the Kelvin-mode degeneracy does not produce an exact `8^n` generation rule. Remaining lepton-generation escape hatches are structural only: half-quantum-vortex or spinorial-order-parameter extensions.

**Open follow-ups (2026-06-07):** #97 upgrades dynamic reconnection cap geometry, #98 maps the #77 static trefoil result into `Q_p` / `\alpha_G`, #99 decides the post-#78 lepton-generation branch, and #100 drafts SSV IX.

## Paper I Supplemental Notes

Result notes, pre-registrations, and checkpoints live under `papers/SSV-I/`. Key recent files:

- `papers/SSV-I/results/proton/geometry-minimum-result-2026-06-03.md` — #77 final result
- `papers/SSV-I/notes/muon-two-mode-symbolic-reduction.md` — two-mode symbolic model
- `papers/SSV-I/results/muon/volovik-berry-phase-issue76-tasks1-4.md` — Berry-phase no-go
- `notes/volovik-mapping.md` — full Volovik analogy map; closed-shell lepton hypothesis now refuted by #78

## Roadmap and Docs

- [docs/roadmap.md](docs/roadmap.md) — paper plan and current priorities
- [docs/numerical-minimisation-roadmap.md](docs/numerical-minimisation-roadmap.md) — numerical programme plan
- [docs/numerical-conventions.md](docs/numerical-conventions.md) — units, conventions
- [docs/claim-status.md](docs/claim-status.md) — compact claim/gapbox status index
- [docs/issue-workflow.md](docs/issue-workflow.md) — how issues, pre-registrations, and result notes are used

## Issue-Driven Workflow

Use the GitHub issue tracker as the primary progress system. Every claim marked "deferred", "open problem", or "needs derivation" in a draft should have a corresponding issue. Pre-register the decision rule before running any diagnostic; commit the result note immediately after.

Issue types: `paper`, `derivation`, `numerics`, `objection`.

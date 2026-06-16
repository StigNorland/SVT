# SSV — Saturated Superfluid Vacuum

Working repository for the SSV theoretical-physics paper series.

The physical vacuum is modelled as a real macroscopic medium described by an order parameter Ψ
(a logarithmic Schrödinger equation, LogSE, with a chiral-shear term and a saturation potential).
Matter is topological defects in Ψ. The programme set out to derive particle masses, the forces,
gravity, time, and black-hole ontology from that single medium and two inputs (mₑ, α).

> **Status: closed (2026-06).** The programme is no longer active. No surviving route delivers the
> quantities it set out to derive. What the framework reproduced were the *forms* of analogue/
> emergent gravity (already known); what it could not deliver were the *magnitudes* (G, Λ/a₀, the
> particle masses). The recurring diagnosis — **"form yes, magnitude no"** — and the salvageable
> content are written up in [papers/conclusions/](papers/conclusions/). This repository is now an
> archive plus that post-mortem.

## Table of contents

- [Conclusions / post-mortem](#conclusions--post-mortem) — start here
- [The recurring diagnosis](#the-recurring-diagnosis)
- [Paper series and outcomes](#paper-series-and-outcomes)
- [Repository layout](#repository-layout)
- [Computation (`instruments/`)](#computation-instruments)
- [Docs and workflow](#docs-and-workflow)

## Conclusions / post-mortem

The honest accounting of what the programme produced and what survives for mainstream physics
lives in [papers/conclusions/](papers/conclusions/):

| Document | What it is |
|----------|-----------|
| [Lessons from a closed programme](papers/conclusions/lessons-from-a-closed-programme.pdf) | **The post-mortem.** Folds the two notes below into one document, organised around the *form-yes-magnitude-no* diagnosis; covers the surviving methodology, the reproduced forms, the failures, the structural reason, and five transferable lessons. |
| [Conclusion A](papers/conclusions/conclusion-a.pdf) | Foundations reading — finite-update-rate time dilation and presentist emergent gravity; where the ontology sits relative to Jacobson/Verlinde/Padmanabhan and the de Sitter observer-algebra programme. Honest home: philosophy of physics. |
| [Conclusion B](papers/conclusions/conclusion-b.pdf) | The mode-counting negative — a concrete superfluid holographic screen reproduces the area law (expected, from locality) but undershoots G by ~38 orders (O(10) Bogoliubov modes vs 1/α_G ≈ 1.7×10³⁸). A demonstrated instance of the Sakharov / Susskind–Uglum species problem. |

## The recurring diagnosis

One pattern runs through every sector. SSV reproduces the **form** of the right answer cheaply, and
concedes the **magnitude**: time dilation (form yes, G no); horizon area law (form yes, coefficient
no); Hawking temperature (form yes, factor-of-4 no); flat rotation curves (form yes, halo amplitude
not derived); cosmological a₀ (form yes, scale conceded); masses (scales handed in, the rest fitted).
The reason is structural: kinematic forms follow from locality and symmetry, which an emergent medium
inherits for free, while the coupling constants live in the microscopic theory below the effective
cutoff (trans-Planckian; Volovik). The most durable outputs are therefore the **negatives**.

## Paper series and outcomes

The drafts and their compiled PDFs remain in `papers/`; the human-readable PDFs are in
[papers/pdf/](papers/pdf/). Outcomes below reflect the closed state.

| Paper | Title | Outcome at closure |
|-------|-------|--------------------|
| [I](papers/pdf/SSV%20I.pdf) | Topological Defects — Geometric Origin of Matter | Mass ladder demoted to a **numerical coincidence**, not a derived spectrum; muon-as-breather **no-go** (#78); proton geometry minimum found (#77) but N_Y/F do not close the sector. |
| [II](papers/pdf/SSV%20II.pdf) | Forces as Hydrodynamic Modes | Programmatic. EM = Goldstone phase mode, photon question closed (#138); W-mass *scale* mₑ/α² derived, prefactor an O(1) coincidence; the "effective spin-2" GW prediction was **falsified** and withdrawn (#159). |
| [III](papers/pdf/SSV%20III.pdf) | Irreversible Time and Wake Entropy | Arrow of time is a **Boltzmann coarse-graining**, not a new resolution of Loschmidt; reversal-echo shows the bulk dynamics is conservative and T-symmetric (#137). |
| [IV](papers/pdf/SSV%20IV.pdf) | Gravity as Update-Capacity Gradient | Time-delay (Einstein-1911) half delivered **in form**; the Bjerknes source mechanism for Φ was **falsified** (#119); G is an empirical input. |
| [V](papers/pdf/SSV%20V.pdf) | Condensate Black Holes | Analogue-gravity ontology re-derived (Visser): acoustic horizon, no singularity, Unruh/Hawking *form*. Horizon area law **earned from locality** (#155); G conceded — see Conclusion B. |
| [VI](papers/pdf/SSV%20VI.pdf) | Galactic Rotation Curves and Morphology | CBH-driven mechanisms **falsified** (#122/#124); a circulation halo + ordinary Newtonian self-gravity reproduce flat curve *and* spiral arms with **no dark matter, no central black hole**, but the halo amplitude is not derived (pure constant-v_h falsified on SPARC). |
| [VII-a](papers/pdf/SSV%20VII-a.pdf) | Quantum Mechanics from Hydrodynamics | Madelung re-derivation; measurement as reconnection. Re-framing, not new. |
| [VII-b](papers/pdf/SSV%20VII-b.pdf) | Emergent Geometry and the Dissolution of Quantum Gravity | Jacobson route **in form** with G as input; gravity is **structurally scalar** — no spin-2 graviton / tensor GW (the durable no-go). |
| [VIII](papers/pdf/SSV%20VIII.pdf) | Cosmogony from the Permissive Void | Owns the low-entropy past hypothesis (never supplied); Λ/a₀ magnitude conceded in parallel with G. |
| IX | CMB and Primordial Phonon Bath | Not written (`main.tex` never drafted, #100). |
| [Alpha](papers/pdf/SSV%20Alpha.pdf) | Fine-Structure Constant from Toroidal Vortex Geometry | Framing only; α remains an empirical input (aspect-ratio identification is a coincidence). |
| [Goldstone](papers/pdf/SSV%20Goldstone.pdf) | Electromagnetic Propagation and the Goldstone Mode | Photon identified as the gapless Goldstone/Bogoliubov phase mode at c. |

## Repository layout

| Path | Contents |
|------|----------|
| [papers/conclusions/](papers/conclusions/) | **The post-mortem and the two conclusion notes** (`.tex` + `.pdf`) |
| [papers/](papers/) | Manuscript drafts, supplemental notes, result notes, checkpoint files |
| [papers/pdf/](papers/pdf/) | Compiled, human-readable PDFs of the series |
| [instruments/](instruments/) | Computational scripts grouped by paper, plus `tools/` (provenance) and the `test/` suite — see [instruments/README.md](instruments/README.md) |
| [notes/](notes/) | Working notes, objections log, Volovik mapping, lepton-ladder note |
| [docs/](docs/) | Roadmap, numerical roadmap, conventions, claim-status, issue-workflow |
| `.github/ISSUE_TEMPLATE/` | Issue templates (paper, derivation, numerics, objection) |

## Computation (`instruments/`)

The computational backbone is a 3D static minimiser for topological defects in the LogSE, plus
per-sector batteries (reconnection, horizon entanglement entropy, rotation-curve N-body, etc.).
Analytic claims were backed by a tested script and a result note; see [instruments/README.md](instruments/README.md)
for the full layout and the `test/` suite. Notable load-bearing instruments referenced by the
post-mortem:

- `instruments/paper_iii/reversal_echo.py` — reconnection time-reversibility (the arrow-of-time result, #137)
- `instruments/paper_v/horizon_entanglement_entropy.py` — area-law verification (#155, Conclusion B)
- `instruments/paper_v/dumb_hole_surface_gravity.py` — acoustic surface gravity + Clausius closure (#155)
- `instruments/paper_i/vortex_core_mode_spectrum.py` — the O(10) bound-mode count behind the G shortfall (#78/#155)

## Docs and workflow

The programme ran issue-driven with pre-registration and a hard negative-results rule — the
methodology the post-mortem flags as its most transferable product.

- [docs/roadmap.md](docs/roadmap.md) — paper plan (historical)
- [docs/numerical-minimisation-roadmap.md](docs/numerical-minimisation-roadmap.md) — numerical programme plan (historical)
- [docs/numerical-conventions.md](docs/numerical-conventions.md) — units, conventions
- [docs/claim-status.md](docs/claim-status.md) — compact claim/gapbox status index
- [docs/issue-workflow.md](docs/issue-workflow.md) — how issues, pre-registrations, and result notes were used

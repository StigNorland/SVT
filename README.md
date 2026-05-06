# SSV - Saturated Superfluid Vacuum

Working repository for the SSV paper series.

This repo now supports both:

- code and numerical checks for the galactic / black-hole parts of the framework
- structured manuscript planning for the broader SSV program

## Repository Layout

- `src/` - analysis and calculation code
- `papers/` - manuscript outlines and paper-specific material
- `notes/` - working notes, objections, reading notes
- `docs/` - roadmap, restructuring plan, and workflow docs
- `.github/ISSUE_TEMPLATE/` - issue templates for paper tasks, derivations, numerics, and objections

## Current Code

| File | Description |
|------|-------------|
| `src/bh_eigenfrequency.py` | BH eigenfrequency and node spacing calculator |
| `src/calculate_velocity_profile.py` | Rotation curve model |
| `src/calibration_analysis.py` | Calibration constant analysis |
| `src/paper_i/` | Paper I vortex, toroidal-background, and muon-mode numerical prototypes |
| `src/paper_ii_reconnection_supplement.py` | Paper II reconnection-barrier numerical supplement |

## Paper I Supplement

The Paper I numerical prototypes and notes live in:

- `src/paper_i/`
- `papers/SSV-I/numerical-prototypes-summary.md`
- `papers/SSV-I/data/`

## Paper II Supplement

The current reconnection-barrier numerical note and curated result tables live in:

- `papers/SSV-II/reconnection-barrier-results.md`
- `papers/SSV-II/data/`

## Roadmap

The working paper plan is described in:

- [docs/roadmap.md](docs/roadmap.md)
- [docs/paper-mapping.md](docs/paper-mapping.md)
- [docs/numerical-minimisation-roadmap.md](docs/numerical-minimisation-roadmap.md)
- [docs/issue-workflow.md](docs/issue-workflow.md)

The main restructuring idea is simple: one main claim per paper.
The main quantitative bottleneck is also now explicit: two linked numerical programmes,
one static and one dynamic, stand behind most unresolved flagship claims.

## Issue-Driven Workflow

Use the GitHub issue tracker as the primary progress system.

Recommended issue types:

- paper task
- derivation task
- computation task
- objection / critique

When a draft says "deferred", "open problem", or "needs derivation", open an issue for it.

## Quick Start

```bash
python src/bh_eigenfrequency.py
python src/calculate_velocity_profile.py
python src/calibration_analysis.py
```

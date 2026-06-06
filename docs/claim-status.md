# Claim Status Index

Bookkeeping snapshot: 2026-06-07.

This note is a compact index of live quantitative claims, open gapboxes, and the
issue or result note that owns the next status change. It is not a replacement
for the paper text; it is the map for avoiding stale "derived" language.

## Observable Status

| Claim / observable | Current status | Owner / next status change |
|---|---|---|
| Static proton geometry | Candidate static result: #77 gives `(R,a)=(2.5,0.85)ξ` and `N_Y×F=54`; separate `N_Y` and `F` are not independently promoted. | #77 result note; final paper propagation if needed |
| `Q_p` / `alpha_G` | Candidate/status-cleanup only; no first-principles `alpha_G` until the static output is mapped into `Q_p`. | [#98](https://github.com/StigNorland/SVT/issues/98) |
| Dynamic reconnection cap radius | Structural harness: cap formation and chiral barrier confirmed, but cap geometry is not grid-converged. | [#97](https://github.com/StigNorland/SVT/issues/97) |
| `W` mass | Ansatz-backed geometry, not derived from measured cap geometry. | #97 |
| Neutrino / PMNS / CP sector | Structural/speculative downstream of event-background spectra and chirality statistics. | Future event-spectrum issue after #97 |
| Scalar BdG muon route | Retired; scalar `Psi` gives no half-integer Berry phase and no robust muon eigenmode. | #78 and no-go result notes |
| Scalar lepton generation routes C/D | Failed: static energy ratio is `3.71`, not `206.77`; Kelvin degeneracy does not yield exact `8^n`. | [#99](https://github.com/StigNorland/SVT/issues/99) decides HQV/spinorial/retirement path |
| SSV IX CMB / phonon-bath paper | Scoped outline only; no `main.tex` yet. | [#100](https://github.com/StigNorland/SVT/issues/100) |

## Paper Gapboxes

| Paper | Open gapbox / deferred claim | Owner |
|---|---|---|
| SSV I | Final status of lepton-generation derivation after scalar routes failed. | #99 |
| SSV I / II | Static breather far-field to `Q_p` to `alpha_G`. | #98 |
| SSV II | Reconnection cap geometry and `W`-mass ansatz test. | #97 |
| SSV II | Neutrino, PMNS, and CP claims from event spectra. | Future issue after #97 produces a stable event background |
| SSV III | Non-universal wake-cell constants and coupling to later gravity/cosmology papers. | Future numerical/cross-paper work |
| SSV IV | First-principles `G` / `alpha_G`; order-unity factor in update ceiling. | #98 for `G`; future derivation for ceiling factor |
| SSV V | Close-packing density, Planck-mass constituent identification, area-law coefficient, full Kerr/no-hair proof. | Paper I / VII-b follow-ups |
| SSV VII-a | Bound-state spectra, exact `hbar/2` prefactor, Born-rule basin calculation. | Future focused derivation/numerics |
| SSV VII-b | Quantitative `G`, Kerr exterior/no-hair proof, strong-field validation, dark-energy value. | #98 for `G`; future geometry/cosmology follow-ups |
| SSV VIII | Kibble-Zurek defect density simulation, quantitative `Lambda`, alpha self-consistency, permissive-void perturbation theorem. | Future VIII/IX support issues |
| SSV IX | Full draft and claim taxonomy. | #100 |

## Working Rule

When a draft uses "derived", the corresponding row above should either be
closure-grade or link to the result note that makes it closure-grade. Otherwise
use `structural`, `candidate`, `ansatz-backed`, `interpretive`, or `speculative`.

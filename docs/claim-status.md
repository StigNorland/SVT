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
| Dynamic reconnection cap radius | Threshold-free/smooth-weighted cap observables are in place. A short-cap tube-pinch ansatz passes the cap-event gate on `n=24..48` and an optional `n=64` check. The actual radius-peak diagnostic is `3.85%` across `n=24..48`, but event-gated lambda scaling does not support pure `R_cap \propto \sqrt{\lambda_\perp}` in this desktop harness (combined through-origin RMS `20.46%`). A fixed-`dx` box sweep shows the measured radius tracks the **box**, not the throat: the scaling negative is a **box-contamination artefact**, not a physical falsification. The dynamic route-C cross-check is therefore **closed as desktop-infeasible** (needs `core << R0 << cap << box` = petascale); it never gated the #105 analytic W-scale result. | [#97](https://github.com/StigNorland/SVT/issues/97), [#108](https://github.com/StigNorland/SVT/issues/108) |
| `W` mass | Scale-derived analytically from inherited ring scale; `\phi` coefficient remains coincidence-grade. The #108 desktop dynamic scaling cross-check does not support the pure inherited-throat scaling route. | #105; dynamic cross-check #97/#108 |
| Neutrino / PMNS / CP sector | Structural/speculative downstream of event-background spectra and chirality statistics. | Future event-spectrum issue after #97 |
| Scalar BdG muon route | Retired; scalar `Psi` gives no half-integer Berry phase and no robust muon eigenmode. | #78 and no-go result notes |
| Scalar lepton generation routes C/D | Failed: static energy ratio is `3.71`, not `206.77`; Kelvin degeneracy does not yield exact `8^n`. | [#99](https://github.com/StigNorland/SVT/issues/99) decides HQV/spinorial/retirement path |
| SSV IX CMB / phonon-bath paper | Scoped outline only; no `main.tex` yet. | [#100](https://github.com/StigNorland/SVT/issues/100) |

## Paper Gapboxes

| Paper | Open gapbox / deferred claim | Owner |
|---|---|---|
| SSV I | Final status of lepton-generation derivation after scalar routes failed. | #99 |
| SSV I / II | Static breather far-field to `Q_p` to `alpha_G`. | #98 |
| SSV II | Reconnection cap geometry and `W`-mass coefficient test. | #97/#108 |
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

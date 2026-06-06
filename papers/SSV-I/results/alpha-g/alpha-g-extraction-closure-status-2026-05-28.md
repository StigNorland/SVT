# α_G Extraction from the Static Breather — Closure Status (2026-05-28)

**Status:** closure memo for issue
[#14](https://github.com/StigNorland/SVT/issues/14).
**Scope:** static-branch far-field extraction. Dynamic-branch and
weak-field GR work are issues #15 and the Paper VII-b agenda.

This note maps each of the six issue tasks onto the documents and
checkpoints already in the repository, identifies which work is
substantively addressed and which is blocked, and states what would
unblock the blocked items. It consolidates and supersedes
`issue-14-alpha-g-extraction-status.md` as the closure note.

## Task-by-task status

| # | Task | Status | Where |
|---|---|---|---|
| 1 | Define the far-field observable as a proton acoustic monopole suppression estimator, not yet as α_G | **addressed** | `alpha-g-proxy-note.md`: `Π_mono^(1) = 1 - ρ_shell` chosen as primary estimator (most stable outer-region scalar); `Π_mono^(2) = M_far/L_box` kept as geometric cross-check. |
| 2 | Connect that estimator to the Paper II acoustic monopole moment Q_p | **addressed** | `alpha-g-mapping-note.md` §"Kernel Form" gives the kernel functional `Q_p[ρ] = (a_p/ξ)^3 ∫ W_p · S_ξ[1-ρ] d³x` with explicit long-wavelength limit `Q_p^LW = δV_p (a_p/ξ)^3`. Direct long-wavelength `Q_p` checkpoint computed in `q_p_kernel_integral.py` and recorded in `q-p-kernel-integral-note.md`. |
| 3 | Make any calibration factor between the estimator and Q_p explicit | **addressed** | `alpha-g-mapping-note.md` §"Provisional Reduced Map" introduces `Q_p = C_Q · δV_p · Π_mono` with `C_Q` explicitly named as the unresolved calibration factor encoding shell-location convention, static-to-asymptotic extrapolation, breather-vs-trefoil geometry, and shell-deficit-vs-monopole-source mismatch. Propagates to `α_G = C_G · Π_mono²` with `C_G = (m_p²/ℏc)(ρ_0 ω_p²/8π m_p²) C_Q² δV_p²`. |
| 4 | Measure numerical sensitivity in the extracted suppression estimator | **addressed** | `issue-14-alpha-g-extraction-status.md` reports the convergence audit: shell-density drift 2.6%–12% (best vs worst fixed-half-width); coarse-fine `Q_p^LW` drift 0.950, 0.967, 0.969 across the three measured half-widths at n=24 vs n=48. The shell estimator is materially more stable than the integrated source. |
| 5 | Compare the resulting mapped α_G with the current Paper II consistency check | **blocked-by-design** | `α_G_prediction: blocked` per `issue-14-alpha-g-extraction-status.md` §"Closure Gate". The block sources are listed below. |
| 6 | Rewrite the relevant Paper II language according to the measured result | **addressed (pre-existing)** | Paper II abstract and §1 already label the relation `G = α_G ℏc α²/(N_p² m_e²)` as a "Structural consistency check, not derivation"; the §"Gravity" derivation takes α_G from CODATA and demonstrates structural consistency with the Paper I mass ladder to 0.6%, not as a first-principles prediction. |

**Five of six tasks are substantively addressed.** The sixth is
blocked-by-design, with the block dependencies named below.

## Why task 5 is blocked

The α_G *prediction* (as opposed to consistency check) requires three
inputs that are not yet at closure-grade:

1. **Closure-grade `Π_mono`.** The shell-density estimator is
   reproducible at the candidate level (2.6% best-case drift) but the
   integrated `δV_p` / `Q_p^LW` source still shows ~3–5% coarse-fine
   drift at fixed half-width. The cleanest path is to consume a
   closure-grade static breather from issue #13.
2. **A derivation or elimination of `C_Q`.** The current mapping ansatz
   `Q_p = C_Q · δV_p · Π_mono` keeps `C_Q` as an undetermined
   dimensionless factor. Two distinct paths to closure are open:
   (a) compute `C_Q` directly by evaluating the kernel
   `Q_p[ρ] = (a_p/ξ)^3 ∫ W_p · S_ξ[1-ρ] d³x` for a known
   carrier-medium coupling operator `S_ξ`; (b) demonstrate that the
   long-wavelength limit `S_ξ[1-ρ] → 1-ρ` is accurate enough at the
   converged breather geometry that `C_Q ≈ 1` within the same tolerance
   as the Π_mono cross-grid drift.
3. **The carrier-medium coupling operator `S_ξ`.** Currently treated as
   the identity in the long-wavelength limit. The first explicit
   nontrivial `S_ξ` test should be done only after `Π_mono` and
   `Q_p^LW` are stable across box and resolution sweeps; the discipline
   in `issue-14-alpha-g-extraction-status.md` is "no operator test
   before the long-wavelength kernel stops moving."

Items (1) is tracked under issue #13 (see
`static-3d-closure-status-2026-05-28.md`); items (2) and (3) are the
α_G-side work that becomes possible once #13 is closed.

## Current numerical state

Headline numbers from the May 7 checkpoints, all candidate:

- `Q_p^LW` at n=24, half_width = 5,6,7: 3.12e-10, 5.40e-10, 9.34e-10
- `Q_p^LW` at n=48, half_width = 5,6,7: 9.94e-9, 1.40e-8, 1.87e-8
- Coarse-fine `Q_p^LW` drift at fixed half_width: 0.950, 0.967, 0.969
- Shell-density drift: 2.6% (best) to 12.0% (worst) across the same
  fixed-half_width pairs

The order-of-magnitude jump between n=24 and n=48 is the same
not-yet-grid-converged signature documented for `F` in
`f-factor-grid-converged-checkpoint.md`. The Π_mono estimator is much
more stable than the integrated source, but the gravity-facing kernel
still inherits the integrated source's drift. This is the central
diagnostic: the outer scalar is reliable; the integrated source is not
yet.

## What would lift the status

The α_G prediction can be promoted from **blocked** to **candidate**
when:

- issue #13 lands one of its three remaining runs (dedicated `N_Y`
  cross-grid sweep, geometric cutoff derivation, or independent
  initial-condition recovery — see
  `static-3d-closure-status-2026-05-28.md` §5), giving a closure-grade
  static breather to consume; **and**
- `C_Q` is fixed either by direct kernel evaluation or by demonstrating
  that the long-wavelength limit `S_ξ ≈ 1` holds within the closure
  tolerance.

The α_G prediction can be promoted from **candidate** to **derived**
when the resulting predicted α_G is compared against CODATA
(α_G = G m_p²/ℏc ≈ 5.91e-39) at the same tolerance as the underlying
static-breather closure, and the comparison falls within that tolerance
without further fitted constants.

## What this paper does not yet claim

The repository explicitly does not claim:

- a first-principles α_G value;
- that `1 - ρ_shell` *is* α_G or *predicts* α_G directly;
- that `Q_p^LW` is the closure-grade Q_p (it is the long-wavelength
  limit of the kernel, which still requires the carrier-operator test);
- that the Paper II structural relation `G = α_G ℏc α²/(N_p² m_e²)` is
  a derivation of α_G — it remains, on Paper II's own framing, a
  consistency check with α_G taken from CODATA.

These non-claims are stated to keep the repository honest at the
candidate-grade level while the upstream closure (issue #13) lands.

## Cross-references

- Pipeline design and observable list: `alpha-g-proxy-note.md`,
  `alpha-g-mapping-note.md`.
- Direct long-wavelength `Q_p` kernel: `q-p-kernel-integral-note.md`,
  `data/q-p-kernel-integral-2026-05-07.json`.
- Convergence audit: `data/q-p-convergence-audit-2026-05-07.json`.
- Upstream static-branch closure: `static-3d-closure-status-2026-05-28.md`.
- Paper II structural relation: `papers/SSV-II/main.tex`
  §"Gravity" / §"Acoustic Monopole Moment".

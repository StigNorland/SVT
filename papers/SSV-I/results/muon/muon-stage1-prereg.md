# Muon Stage 1 pre-registration: selection-rule fix as a diagnostic measurement

**Date:** 2026-05-30. Written BEFORE running the fixed operator, so the
expected-outcome statement cannot be tuned to the result. First step of the
3-stage muon programme that follows the Path B null
(`papers/SSV-I/path-b-eigenvalue-result.md` on this branch's parent main).
Tracking: GitHub issue to be opened on completion.

## Background

Path B showed that the muon eigenfrequency $\omega/\omega_c = 0.2148$ obtained
in the `helicity` basis is not basis-converged: enrichment moves the lowest
physical mode across $[0.175, 0.228]$ ($\pm 13\%$) and leaves the muon window
empty in two of four bases. The §Muon gapbox demoted the muon ladder rung to
a candidate carried by empirical agreement on $m_e/\alpha$ rather than by a
derived eigenmode.

The prior repo note `papers/SSV-I/enrichment-attempt-findings-2026-05-27.md`
diagnoses the load-bearing issue: the operator
`hermitian_current_curl_bdg_blocks` computes cross-$m_\varphi$ matrix
elements of $\hat L_\perp$ via `current_curl_component_overlap`, which
multiplies the meridional integral by $2\pi$ and skips the azimuthal integral
$\int e^{i(m_b - m_a)\varphi} d\varphi = 2\pi \, \delta_{m_a, m_b}$. The
resulting spurious cross-$m$ matrix elements (between $m_\varphi = 0$ core
modes and $m_\varphi = \pm 1$ Kelvin modes) are $40$–$65\%$ of the legitimate
same-$m$ diagonal -- not perturbative. The prior author measured that
enforcing the selection rule (correct physics) makes the Kelvin eigenvalue
drift downward with half-width:
$0.147 \to 0.131 \to 0.122$ at $hw = 4, 6, 8 \, \xi$. The cross-$m$ coupling
was "inadvertently compensating" for that drift.

Status on the live branch (after PR #67 merge to main):

- The selection-rule violation is still present in
  `src/paper_i/kelvin_augmented_bdg.py` (see the long honest comment at
  L454-L470 of that file).
- The previous calibration $\delta_{\rm relax} = +0.038$ that pulled
  $\lambda_\perp = (\pi/4)(1+\delta_{\rm relax})$ to land near $0.207$ is NOT
  wired into the live operator path -- the `harmonic_ladder_spectrum.py` and
  `path_b_spectrum_probe.py` drivers use the bare $\lambda_\perp = \pi/4$.
  $\delta_{\rm relax}$ only lives in comments and in the (now-quarantined)
  `thin_ring_delta_relax_sweep.py`. So the user-approved "Bigger Stage 1
  including drop $\delta_{\rm relax}$" reduces in practice to "Stage 1 =
  selection-rule fix alone".

## The one operator change

In `src/paper_i/kelvin_augmented_bdg.py`, function
`hermitian_current_curl_bdg_blocks` (around L447): add an early return at
function entry when the two modes carry different azimuthal quantum numbers:

```python
if bra.m_phi != ket.m_phi:
    return 0.0j, 0.0j
```

This enforces $\int e^{i(m_b - m_a)\varphi} d\varphi = 2\pi \, \delta_{m_a, m_b}$
for the $\hat L_\perp$ projection. It does not touch
`background_second_current_curl_overlap` (already enforces the rule per
L699-L701 of the same file). It does not touch the `kelvin_dispersion =
self-induction` Kelvin-Kelvin block override (that block is replaced
elsewhere). No other code path consumes
`hermitian_current_curl_bdg_blocks` directly.

Nothing else changes. $\lambda_\perp = \pi/4$ unchanged. All other defaults
unchanged. Path B parameters: $n=41$, $hw=5$, `profile_n=1600`,
`kelvin_seed=helicity`, `kelvin_dispersion=self-induction`,
`kelvin_phi_n=1024`, `kelvin_core_radius=1.0`.

## What this commits to BEFORE running

**Stage 1 is diagnostic only.** Its outcome is NOT yet treated as a
prediction of the operator; it is verification that the fix produces a
physically consistent result. The "real" prediction is the Stage 2
convergence study (separate document) on the fixed operator.

Three pre-registered mechanical checks:

1. **Selection rule holds numerically.** For any pair of modes with
   $m_{\varphi,\,a} \neq m_{\varphi,\,b}$, `hermitian_current_curl_bdg_blocks`
   returns $(0+0i, 0+0i)$ exactly. Verified by direct call on a
   constructed test pair.

2. **Same-$m$ matrix elements are unchanged.** For pairs with
   $m_{\varphi,\,a} = m_{\varphi,\,b}$, the returned blocks match the values
   produced by the unfixed operator to floating-point precision. Verified
   by direct call on a constructed test pair.

3. **The lowest physical eigenfrequency moves.** Path B canonical (broken
   operator, `helicity` basis, $n=41$, $hw=5$) gave the lowest physical
   stable mode at $\omega/\omega_c = 0.2149$. With the fix, the prior
   author's measurements predict the corresponding mode shifts downward
   (consistent with the cross-$m$ terms being $40$–$65\%$ of diagonal). I
   expect somewhere in $[0.10, 0.18]$ at $hw = 5$, by interpolation /
   extrapolation of the prior-work values $\{0.147, 0.131, 0.122\}$ at
   $hw = \{4, 6, 8\}$. A result outside that broad range would warrant
   debugging the fix rather than reporting the number.

## What this does NOT commit to

- Whether the fixed operator's lowest physical mode is "the muon". That
  depends on what it converges to under enrichment (Stage 2) and on whether
  any independent physical argument identifies that frequency with a known
  particle.
- Whether the fixed operator is itself physically complete. The prior author's
  same-domain drift $0.147 \to 0.131 \to 0.122$ (decreasing with $hw$, i.e.
  including more of the outer torus) suggests a missing $hw$-independent
  Kelvin shift. Stage 2 will quantify that drift; Stage 3 (if Stage 2 fails)
  escalates to full 3D $\varphi$-discretization.
- Anything about $\delta_{\rm relax}$. It is not in the live operator path
  and is not being re-tuned.

## Outcome commitment

Whatever the lowest physical stable eigenfrequency is in the run, that number
goes into the Stage 1 result note verbatim, alongside the full spectrum and
the cross-$m$ vs same-$m$ matrix-element checks. No hunting for $0.207$, no
re-calibration, no parameter sweeps. Stage 2 is a separate pre-registration.

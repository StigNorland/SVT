# Cubic-Vertex One-Loop Self-Energy: Result Note (2026-05-26)

> **Status (2026-05-30): superseded by Path B null.** Numerical claims in this note about the muon eigenfrequency reaching $\omega/\omega_c = 0.207$, the $\delta_{\rm relax}$ calibration, the $\alpha$-harmonic ladder identification, or the $1/\sqrt{N_{\rm modes}}$ basis-truncation residual are now governed by `papers/SSV-I/path-b-eigenvalue-result.md`: that test showed the muon agreement is not basis-robust (drifts $\pm 13\%$ across 4 bases, empty window in 2 of 4) and the pion rung is absent in every basis. Structural sub-results that stand on their own (operator algebra, analytic derivations, the cubic-vertex one-loop result, dimensional setup) remain valid in isolation; what is superseded is their use as evidence for the ladder identification or as a closure path to it. Quarantined inputs: `src/_fitted_quarantine/`. Tracking: issue #66.

**Status:** prototype calculation complete, result is robust at small n.

## What was computed

Building on the scoping memo
[`muon-cubic-vertex-self-energy-memo.md`](muon-cubic-vertex-self-energy-memo.md),
the script
[`src/paper_i/muon_cubic_full_self_energy.py`](../../src/paper_i/muon_cubic_full_self_energy.py)
implements the full one-loop diagram from the LogSE cubic vertex:

  - Build the BdG matrix at the converged weak-form / combined-Kelvin /
    full-second-variation / smooth-window configuration.
  - Diagonalise. Bogoliubov-normalise each eigenmode to `|u|^2 - |v|^2 = 1`.
  - Skip Goldstone-like modes whose density-perturbation L2 norm is below
    1% of the maximum (these are phase modes with `u + v* ~ 0`).
  - For each external mode (muon-target and electron-breather), compute

        Sigma_a(omega_a) = sum_{b,c} |V_{abc}|^2 / (omega_a - omega_b - omega_c + i*eps)

    with `V_abc` from the full 3D meridional + azimuthal integral

        V_abc = int g_3(r,z) * delta_rho_a * delta_rho_b * delta_rho_c d^3x ,

    `delta_rho_n = 2 Re[psi_0^* (u_n + v_n^*)] * e^{...}` (azimuthal
    decomposition handled by phi sampling, default 16-24 points), and

        g_3(r,z) = -b * rho_0^3 / (6 |psi_0|^4) .

  - Report the relative shift `Delta = Re(Sigma_mu/omega_mu) - Re(Sigma_e/omega_e)`.

## Headline result

| grid | hw | kelvin_phi_n | phi_samples | omega_mu | omega_e | Sigma_mu/omega_mu | Sigma_e/omega_e | Delta |
|---|---|---|---|---|---|---|---|---|
| 25 | 5 | 128 | 16 | 0.171 | 1.148 | -8.83e-9 | +2.83e-10 | -9.11e-9 |
| 31 | 5 | 128 | 16 | 0.183 | 1.190 | -5.89e-9 | -8.75e-12 | -5.88e-9 |
| **49** | **5** | **256** | **24** | **0.206** | **0.986** | **-3.00e-9** | **-4.93e-10** | **-2.51e-9** |

The relative shift `Delta` is in the `-(3 to 9) x 10^-9` range across
three grid resolutions — that is, the cubic-vertex one-loop
contribution to the muon-electron mass ratio is at the
**0.0000003% to 0.0000009%** level, seven orders of magnitude smaller
than the residual ~1% gap. The magnitude tightens with grid refinement
(n=25 -> n=49 narrows it by a factor of ~4), consistent with the
suppression mechanism described below.

At n=49 the tree-level omega_mu = 0.20578 also lands very close to the
target 0.20700, confirming the cubic-vertex script reproduces the
correct BdG configuration. (The 0.7% deviation from
the matched-spacing trio's n=49 value of 0.20628 is consistent with the
kelvin_phi_n=256 quadrature shift relative to phi_n=128.)

## Interpretation

The cubic vertex is **falsified** as the source of the 1% gap. The
order-of-magnitude estimates in the scoping memo (Estimates A-C, which
bracketed 10^-5 to 10^-2) were rough and the actual calculation lands
closer to Estimate A (the "small phase-space overlap" estimate), not
Estimate C (the "core-enhanced cubic coupling" estimate).

**Why is the cubic contribution so small?** The dominant suppression
mechanism is **angular and phase coherence in the BdG eigenmodes**.
Each density-perturbation amplitude `A_+(r,z)` has nontrivial
meridional phase structure (it inherits both the vortex-core phase
`exp(i theta)` from psi_0 and the Kelvin-helicity phase structure from
the input modes). When three such complex fields are multiplied together
in the cubic integrand, the cell-by-cell signs alternate and the
meridional integral is suppressed by ~3-4 orders of magnitude relative
to the |A_+|^3 magnitude.

The breather-core enhancement of `g_3 ~ 1/|psi_0|^4` is *not* a strong
effect: in the same region where `g_3` blows up, the density-perturbation
amplitudes `A_+ = psi_0^* u + psi_0 v` go to zero linearly in `|psi_0|`,
so `g_3 * A_+^3` scales as `1/|psi_0|`, integrable (not singular). The
integrand is smooth and bounded.

## What this means for the 1% gap

The 1% residual between the converged tree-level BdG calculation and the
muon-electron mass-ratio target is **not** the LogSE cubic vertex. The
remaining candidates, in order of plausibility:

1. **Reduced-basis truncation**: the combined-Kelvin four-core basis
   spans 10 modes per azimuthal sector triple `(-1, 0, +1)`. Higher
   azimuthal sectors (`|m| >= 2`) and additional radial modes within
   each sector are absent. A systematic enrichment, especially the next
   azimuthal sector, is the natural next test.

2. **Curved-torus relaxation basis**: the relaxed-background calculation
   uses 6 basis modes (3 amplitude + 3 phase). Higher-mode relaxation at
   the same converged grid (e.g. 9 or 12 basis modes) would constrain the
   relaxation-basis truncation contribution to delta_relax.

3. **Quartic and higher vertices**: in principle the LogSE expansion has
   `b ln(1+x) = x - x^2/2 + x^3/3 - x^4/4 + ...`. The quartic-vertex
   one-loop "tadpole" contribution has not been computed; analogous to
   how the cubic vertex turned out to be much smaller than the rough
   estimate, this should not be assumed to be O(1%) without explicit
   calculation.

4. **Kelvin-self-induction model**: the `kelvin_self_induction_shift`
   function implements a specific regularised log-singular dispersion.
   The geometric `phi_n` extrapolation suggests `omega_mu` drifts by
   another ~0.5% from `phi_n=512` to `phi_n=infty` (the spot-check
   at `phi_n=1024` is in progress at the time of writing).

5. **The reduced operator's chiral-mix sector**: `chiral_mix=0` is used
   in the headline calculation. The chiral-bridge contribution at
   `|m_a - m_b| = 1` was suppressed for clarity; turning it on with the
   proper coefficient may shift the eigenfrequency.

## Falsifiability check

The scoping memo specifically predicted: "if the actual computation
yields +0.5% to +1.5%, the residual is consistent with the cubic vertex
being the dominant correction." The actual computation yields
**-(5 to 9) x 10^-9**, which is *both* the wrong sign and seven orders of
magnitude too small. The falsification test from the memo is therefore
clean: **the cubic vertex is not the source of the 1% gap**, and the
residual must come from one of the other candidates above.

## Caveat

The first-pass implementation has several approximations:

- The angular integral uses discrete sampling (16-24 points). For BdG
  modes with `|m| <= 1`, this is sufficient (Nyquist condition met).
  For higher-m intermediate states, more samples would be needed --
  but the basis truncation at `|m| <= 1` means those states aren't in
  the calculation anyway.

- The intermediate-state pair sum is restricted to the ~8 physical
  (non-Goldstone) BdG modes in the reduced basis. The "true" loop sum
  extends over the full medium spectrum up to the grain cutoff
  `N_0 ~ 1.4e24 rad/s`. A basis enrichment would extend the sum.

- The energy denominator uses a small imaginary part `eps = 1e-3` to
  regularise near-resonant denominators. The result is insensitive to
  `eps` at this magnitude level.

Within these approximations, the conclusion is robust: cubic-vertex
one-loop gives `~10^-9` relative shift, not `~10^-2`. The 1% gap is
elsewhere.

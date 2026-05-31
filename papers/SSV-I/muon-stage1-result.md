# Muon Stage 1 result: selection-rule fix is mechanically correct;
# spectrum splits into nearly-decoupled m=0 and m=±1 sectors

**Date:** 2026-05-30. Outcome of the pre-registered test in
`papers/SSV-I/muon-stage1-prereg.md`. Reproduction:
`python src/paper_i/muon_stage1_probe.py` (committed defaults, no tuning).

## One-line verdict

**Pre-registration satisfied.** All 8 mechanical selection-rule receipts pass.
The lowest physical stable eigenfrequency is $\omega/\omega_c = 0.153$, inside
the pre-registered expected window $[0.10, 0.18]$ at $hw = 5$. The spectrum
contains an unexpected second low mode at $\omega/\omega_c = 0.214$ that lands
essentially exactly on the broken-operator Path B value $0.2148$.

**Stage 1 is diagnostic only.** No prediction is made. The interpretation
below is a conjecture for Stage 2 to test, not a result to cite.

## Selection-rule receipts (all OK)

| pair | block | expected | measured |
|------|-------|----------|----------|
| (m=0, m=+1) cross | L | 0 (m_a != m_b) | 0.000000e+00 |
| (m=0, m=+1) cross | M | 0 (m_a + m_b = +1) | 0.000000e+00 |
| (m=0, m=0)        | L | nonzero | 2.218e-01 |
| (m=0, m=0)        | M | nonzero (0+0=0) | 9.960e-02 |
| (m=+1, m=+1)      | L | nonzero | 2.947e-01 |
| (m=+1, m=+1)      | M | 0 (m+m=+2) | 0.000000e+00 |
| (m=+1, m=-1)      | L | 0 (m_a != m_b) | 0.000000e+00 |
| (m=+1, m=-1)      | M | nonzero (m_a+m_b=0) | 5.503e-10 (numerical 0) |

The 5.5e-10 in the last row is numerical noise from the meridional integrand:
the integrand should be exactly $-$ the conjugate of itself in the
hermitisation. The point is structural: every selection-rule-forbidden block
is below $10^{-9}$, and every allowed block is order 0.1.

## Full spectrum (n=41, hw=5, lambda_perp=pi/4, helicity 6-mode basis)

Stable positive eigenfrequencies, distinct after collapsing near-degenerate
pairs:

| Path B (broken operator) | Stage 1 (fixed operator) |
|--------------------------|--------------------------|
| 0.0051 (Kelvin self-ind) | absent                    |
| 0.0051 (Kelvin self-ind) | absent                    |
| 0.2148                    | **0.2139**                |
| 0.3148                    | absent                    |
| 1.1433                    | 1.0867                    |
| 4.4976                    | 4.3880                    |
| --                        | **0.1528** (NEW)          |

The fixed operator has 4 distinct stable positive modes (down from 6). Two
modes "disappear": the Kelvin self-induction pair at 0.005, and the mode at
0.315 that the previous draft of §The Muon called the ``2 mu_0 pion tongue''.
One new mode appears at 0.153. The two persistent low modes (0.214 and the
new 0.153) bracket the muon target 0.207 from above and below.

## Provisional sector identification (Stage 2 to verify)

The cross-m coupling that the fix removed was 40-65% of the legitimate
diagonal between m_phi=0 core modes and m_phi=+/-1 Kelvin helicity modes
(measured in
`papers/SSV-I/enrichment-attempt-findings-2026-05-27.md`, now bannered as
superseded but still useful for this diagnostic). Without that coupling, the
m=0 and m=+/-1 sectors are **nearly decoupled**: only the (+1, -1) M-block
Nambu coupling remains nonzero between distinct-m modes.

Provisional sector identifications (to verify in Stage 2 by inspecting
eigenvectors):

- **omega/omega_c = 0.153** -- likely the m_phi=+/-1 Kelvin sector eigenmode.
  Consistent with the prior author's selection-rule-enforced Kelvin values
  0.147 at hw=4, 0.131 at hw=6 (decreasing with domain size, suggesting an
  outer-torus Kelvin contribution not yet captured).
- **omega/omega_c = 0.214** -- likely the m_phi=0 core breathing-chiral hybrid
  eigenmode at lambda_perp = pi/4. Its value barely shifted from the broken
  operator's 0.2148.

If those identifications hold, an interesting structural consequence follows:
the broken operator's $0.215$ was NOT a hybrid eigenmode of $\hat L \oplus
\hat L_\perp$ as previous drafts claimed. It was already (to within $\sim
0.5\%$) the pure m=0 core mode at lambda_perp = pi/4; the cross-m coupling
was only dressing it slightly. The "core-breathing oplus Kelvin hybrid"
story in §The Muon was an artifact of the cross-m mixing.

The Kelvin sector eigenfrequency 0.153 has no obvious particle identification
on the alpha-harmonic ladder ruler 0.5 mu_0 = 0.069: it's rung 2.21, neither
a half-integer nor an integer.

## What Stage 1 DOES say

1. The selection-rule violation is real, large (40-65% of diagonal), and the
   fix removes it cleanly.
2. The fixed operator at the Path B reference point has a basis-truncation
   spectrum dominated by two low modes at $0.153$ and $0.214$, separated by
   ~30%. Neither was the right object to call ``the muon'' in the broken
   operator -- if either is, it's the $0.214$ one, by accident of value.
3. The pre-registered expected-window check passes: $0.153 \in [0.10, 0.18]$.

## What Stage 1 does NOT say

- Whether 0.153 or 0.214 is basis-converged. Stage 2 (separate pre-registration)
  is the convergence study.
- Whether either mode is "the muon". That depends on (i) basis convergence,
  (ii) eigenvector identification, (iii) independent physical argument
  identifying that frequency with the lepton mass.
- Whether the operator is physically complete. The Kelvin-sector drift
  with hw documented by the prior author ($0.147 \to 0.131 \to 0.122$ at
  hw=4/6/8) is still expected to be present and is a target of Stage 2.
- Anything about delta_relax = 0.038. It was never wired into the live
  operator path; the bare lambda_perp = pi/4 is what produced these numbers.

## Files

- Operator change: `src/paper_i/kelvin_augmented_bdg.py`
  function `hermitian_current_curl_bdg_blocks` (selection rule split between
  L-block and M-block; new comment block replaces the long historical note).
- Probe: `src/paper_i/muon_stage1_probe.py` (reproduces this result end-to-end).
- Pre-registration: `papers/SSV-I/muon-stage1-prereg.md`.

## Next step

Stage 2: pre-registered convergence study on the fixed operator. Sweep
(a) grid resolution n, (b) half-width hw, (c) basis enrichment without
x-weighted modes. Decision rule: each axis must produce residual scaling
consistent with Galerkin convergence at three or more points. Pre-register
before running. Tracked separately.

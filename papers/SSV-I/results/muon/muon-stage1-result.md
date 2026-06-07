# Muon Stage 1 result: selection-rule fix is mechanically correct;
# spectrum splits into nearly-decoupled m=0 and m=±1 sectors

**Date:** 2026-05-30. Outcome of the pre-registered test in
`papers/SSV-I/muon-stage1-prereg.md`. Reproduction:
`python instruments/paper_i/muon_stage1_probe.py` (committed defaults, no tuning).

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

## Eigenvector sector decomposition (the sanity check)

A direct decomposition of each eigenvector onto the three m_phi sub-sectors
(reproducer: `instruments/paper_i/muon_stage1_eigvec_check.py`) overturns the
provisional identifications I conjectured from the spectrum alone:

| omega/omega_c | dominant sector | m=0 amplitude | structure |
|---------------|-----------------|---------------|-----------|
| **0.1528**    | m=+1 Kelvin (93%) | **zero**    | (+1, -1) Nambu doublet |
| **0.2139**    | m=-1 Kelvin (81%) | **zero**    | (+1, -1) Nambu doublet |
| 1.0867        | m=0 core (100%)   | full        | pure core breathing-chiral |
| 4.3880        | m=0 core (100%)   | full        | pure core breathing-chiral (excited) |

Two findings are forced by this table:

1. **The m=0 core sector at lambda_perp = pi/4 has NO low eigenmode near
   the muon target.** Its lowest mode is 1.087, five times higher than 0.207.
   The previously-conjectured "0.214 is the pure m=0 core mode" was wrong:
   0.214 has zero m=0 amplitude.

2. **The 0.214 eigenmode is purely in the m_phi=+/-1 Kelvin sector** with
   (+1, -1) Nambu-doublet structure (it mixes m=+1 and m=-1 via the M-block
   that the corrected selection rule allows). There is also a sister mode at
   0.153, same sector, different Nambu structure. No core breathing-chiral
   amplitude in either.

## Direct structural consequence

The previously-published §The Muon mechanism is wrong, not merely demoted:

> "The calculation confirms the identification: the muon corresponds to the
> lowest hybrid between the m_phi=0 core-breathing sector and the
> m_phi=+/-1 Kelvin sector."  (SSV-I main.tex L908-915 on main)

The selection-rule-correct operator shows the muon-value eigenmode is
**pure-Kelvin with zero core amplitude**. There is no hybrid; the broken
operator's "hybrid" eigenmode was created by the spurious cross-m terms
the prior text claimed were physical bridging. The broken operator's 0.215
was always a pure Kelvin Nambu mode; the cross-m terms only dressed it
~0.5% above its true value 0.214.

The "core-breathing oplus Kelvin coupling through L_perp" mechanism that
SSV-I §The Muon presents as the muon's physical origin is therefore not
supported by the operator itself. The m=0 core sector at lambda_perp = pi/4
does not produce a muon-scale mode; only the Kelvin sector does.

## Two readings of the 0.214 = muon coincidence

After this decomposition, the 0.214 = muon identification has two readings,
neither flattering:

**Reading A: the muon IS a pure-Kelvin Nambu mode.** The numerical agreement
is real, but the mechanism is not "ring-breathing hybridised with the chiral
sector"; it is a pure m=+/-1 Kelvin Nambu doublet at lambda_perp = pi/4.
The §Muon text needs the mechanism rewritten -- the references to "major
radius breathing", "ring-breathing mode", and "coupling to the transverse
chiral channel must bridge this gap" are wrong: the bridge does not happen
because the operator doesn't couple the sectors that way.

**Reading B: 0.214 = muon is a numerical coincidence.** The Kelvin sector
has at least two eigenmodes in the window [0.15, 0.22] (0.153 and 0.214).
Hitting any target in that window to a few percent carries no information.
The sister mode 0.153 has no particle identification on the alpha-harmonic
ladder; if 0.214 = muon is meaningful then 0.153 should also correspond to
something, and it does not.

Stage 2 (basis-convergence study) will help discriminate but cannot
definitively pick one reading; that may need an independent physical
argument identifying the Kelvin sector with the lepton hierarchy.

## What Stage 1 DOES say

1. The selection-rule violation is real, large (40-65% of diagonal), and the
   fix removes it cleanly. All 8 pre-registered receipts pass.
2. The fixed operator at the Path B reference point has a basis-truncation
   spectrum dominated by **two Kelvin Nambu-doublet modes** at $0.153$ and
   $0.214$, plus two m=0 core modes at $1.087$ and $4.388$. The previous
   "core $\oplus$ Kelvin hybrid" identification of the muon is wrong: no
   eigenmode has both m=0 and m=+/-1 amplitude.
3. The pre-registered expected-window check passes: $0.153 \in [0.10, 0.18]$.
4. The §Muon paragraph claiming the muon eigenmode hybridises core-breathing
   with Kelvin via $\mathcal{L}_\perp$ is mechanistically wrong, not merely
   basis-non-converged. The mechanism text in SSV-I §The Muon (L908-935 on
   main) needs revision, not just demotion.

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

- Operator change: `instruments/paper_i/kelvin_augmented_bdg.py`
  function `hermitian_current_curl_bdg_blocks` (selection rule split between
  L-block and M-block; new comment block replaces the long historical note).
- Probe: `instruments/paper_i/muon_stage1_probe.py` (reproduces this result end-to-end).
- Pre-registration: `papers/SSV-I/muon-stage1-prereg.md`.

## Next step

Stage 2: pre-registered convergence study on the fixed operator. Sweep
(a) grid resolution n, (b) half-width hw, (c) basis enrichment without
x-weighted modes. Decision rule: each axis must produce residual scaling
consistent with Galerkin convergence at three or more points. Pre-register
before running. Tracked separately.

# Muon Stage 2 result: both Kelvin Nambu modes FAIL basis convergence

**Date:** 2026-05-30. Outcome of the pre-registered test in
`papers/SSV-I/muon-stage2-prereg.md`. Reproduction:
`python instruments/paper_i/muon_stage2_probe.py` (committed defaults, no tuning,
~15 min total).

## One-line verdict

**FAIL on both Kelvin Nambu modes**, by the pre-registered decision rule.
The lower mode (Stage 1: 0.153) fails 2 of 3 axes; the upper mode
(Stage 1: 0.214) fails all 3. Per the prereg joint-result table: "the
fixed operator is basis-incomplete; the Kelvin sector cannot support a
basis-converged low mode. Escalates to Stage 3."

## The data

| sweep | label | lower Kelvin | upper Kelvin | m=0 core (low) |
|-------|-------|---|---|---|
| n=31, hw=5, helicity-2c   | n=31  | 0.1383 | 0.1833 | 1.051 |
| n=41, hw=5, helicity-2c   | n=41  | 0.1528 | 0.2139 | 1.087 |
| n=51, hw=5, helicity-2c   | n=51  | 0.1609 | 0.2326 | 1.110 |
| n=61, hw=5, helicity-2c   | n=61  | 0.1654 | 0.2437 | 1.126 |
| n=41, hw=4, helicity-2c   | hw=4  | 0.1719 | 0.2861 | 1.132 |
| n=41, hw=5, helicity-2c   | hw=5  | 0.1528 | 0.2139 | 1.087 |
| n=41, hw=6, helicity-2c   | hw=6  | 0.1365 | 0.1698 | 1.052 |
| n=41, hw=7, helicity-2c   | hw=7  | 0.1229 | 0.1379 | 2.241 |
| n=41, hw=8, helicity-2c   | hw=8  | 0.1105 | 0.1141 | 0.940 |
| n=41, hw=5, helicity-2c   | hel-2c   | 0.1528 | 0.2139 | 1.087 |
| n=41, hw=5, helicity-4c   | hel-4c   | 0.1528 | 0.2139 | 0.034 |
| n=41, hw=5, combined-2c   | comb-2c  | 0.1589 | **0.4820** | 1.087 |
| n=41, hw=5, core_enriched-4c | ce-4c | 0.1589 | **0.4820** | 1.520 |

## Per-axis verdict against the pre-registered rule

**n-convergence (rule: |Δω|/ω ≤ 1% between two finest grids, monotonically
decreasing step sizes):**

- Lower mode steps: 10.5%, 5.3%, 2.7%. Cauchy-like (each step roughly half
  the previous), but the last step is 2.7%, still above 1%. **FAIL.**
- Upper mode steps: 16.7%, 8.7%, 4.6%. Same Cauchy-like shape, last step
  4.6%, well above 1%. **FAIL.**

Extrapolation note (NOT part of the rule, only context): if the geometric
halving continues, the n→∞ limits would be around 0.17 (lower) and 0.26
(upper). But the rule requires measurement, not extrapolation.

**hw-convergence (rule: |Δω|/ω ≤ 2% between two largest hw, AND plateau
behaviour):**

- Lower mode: 0.172 → 0.153 → 0.137 → 0.123 → 0.111 across hw = 4, 5, 6, 7, 8.
  Total drift 35%, monotonically decreasing, NO plateau. **FAIL.**
- Upper mode: 0.286 → 0.214 → 0.170 → 0.138 → 0.114 across the same hw.
  Total drift 60%, monotonically decreasing, NO plateau. **FAIL.**

This drift is the structural one the prior author flagged in
`enrichment-attempt-findings-2026-05-27.md`: "the model needs a term that
provides the correct hw-independent Kelvin shift". The selection-rule fix
removed the spurious cross-m mixing, but the hw-drift survives the fix.
The drift is therefore a property of the L+L_perp Kelvin operator itself,
not of the cross-m artifact.

**basis-stability (rule: spread ≤ 5% across the 4 bases, mode present in
every basis):**

- Lower mode: {0.1528, 0.1528, 0.1589, 0.1589}. Spread 4% relative to
  the mean. Present in every basis. **PASS.**
- Upper mode: {0.2139, 0.2139, **0.4820**, **0.4820**}. Spread 77% --
  the `combined` Kelvin seed and the `core_enriched` variant put it at
  0.48, more than double the helicity value. **FAIL.**

The basis change that breaks the upper mode is going from `helicity`
Kelvin seeds (linear combinations $\Phi_R \pm i \Phi_{kelvin\_vertical}$) to
`combined` seeds (orthonormalised pool of all Kelvin candidates). Both are
ostensibly the same Kelvin sector, but the upper mode's eigenvalue
depends sensitively on which orthogonal basis is chosen.

## Joint verdict and what it means

| mode | n | hw | basis | overall |
|------|---|----|----|---------|
| lower (0.153) | FAIL | FAIL | PASS | **FAIL** (2 of 3) |
| upper (0.214) | FAIL | FAIL | FAIL | **FAIL** (3 of 3) |

The pre-registered prereg joint-result table maps "both FAIL" to:
"the fixed operator is basis-incomplete; the Kelvin sector cannot support
a basis-converged low mode. Escalates to Stage 3."

Concretely:

- The 0.214 = muon agreement from Stage 1 is a coincidence pinned to one
  specific operating point (n=41, hw=5, helicity Kelvin seed). Refining
  the grid pushes it to 0.244; enlarging the domain pushes it to 0.114;
  changing the Kelvin seed pushes it to 0.482. None of these moves to 0.207.
- Stage 1's Reading A ("the muon IS a pure-Kelvin Nambu mode") is
  decisively falsified. The mode isn't a stable physical object; it's a
  basis-truncation artifact whose value happens to be 0.214 at one
  particular point.
- Stage 1's Reading B ("0.214 = muon is a numerical coincidence") wins.

The sister mode 0.153 has the same problem: it's basis-stable across the
4 Kelvin seed choices to 4%, but it drifts steeply with hw and isn't
n-converged. It is therefore also not a stable physical eigenmode.

## What this leaves the §The Muon section needing

Stage 1 already showed the §Muon mechanism is wrong (m=0 core sector has
no muon-scale mode; eigenvector decomposition confirms zero m=0 amplitude
in the Kelvin Nambu modes). Stage 2 now adds: even the Kelvin Nambu modes
themselves are not basis-converged eigenmodes. The honest position is:

**The L+L_perp toroidal-breather BdG operator at $\lambda_\perp = \pi/4$
does not predict a muon.** It does not predict a muon as a basis-converged
core-Kelvin hybrid (Stage 1 falsified this); it does not predict a muon as
a basis-converged pure-Kelvin Nambu mode (Stage 2 falsified this); and the
m=0 core sector's lowest eigenmode is at $\omega/\omega_c \approx 1.1$,
nowhere near any lepton mass.

The muon = $3/2 \mu_0$ identification is, on present operator evidence,
purely numerological: a coincidence on the $m_e/\alpha$ scale, not an
eigenmode prediction.

## What Stage 3 would look like (if pursued)

Two candidate escalations, both deferred:

1. **Full 3D phi-discretization.** Abandon the meridional + Kelvin Ansatz
   and discretize the full toroidal coordinate. Free of basis-truncation
   ambiguity, but much more expensive (memory and CPU both scale by
   $N_\varphi$). If this also produces no muon-scale mode, the L+L_perp
   operator is definitively the wrong instrument.

2. **Hunt for the missing Lagrangian term.** The hw-drift of the Kelvin
   sector (decreasing with domain size, monotonic, no plateau) suggests
   the operator is missing an outer-region term. The prior author flagged
   this: "the outer torus region carries net negative current-curl
   coupling in the Kelvin sector". A physically-motivated additional term
   in $\mathcal{L}_\perp$ that produces an hw-independent Kelvin shift
   would change the picture, but adding such a term is itself a free
   parameter unless it's derived from first principles.

Neither escalation is in scope for this branch. The honest output of the
muon programme as currently constituted is the §Muon rewrite, which can be
done now without further computation.

## Files

- Pre-registration: `papers/SSV-I/muon-stage2-prereg.md` (commit 2441e2e)
- Probe: `instruments/paper_i/muon_stage2_probe.py` (commit 2441e2e)
- Sweep output: 857 seconds of compute time on the local machine
  (4 + 5 + 4 = 13 spectrum solves, each ~30-170 s depending on n)

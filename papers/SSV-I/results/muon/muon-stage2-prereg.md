# Muon Stage 2 pre-registration: basis convergence of the fixed operator

**Date:** 2026-05-30. Written BEFORE running any Stage 2 sweep, so the
decision rule cannot be tuned to the result. Follows Stage 1
(`papers/SSV-I/muon-stage1-result.md`), which fixed the azimuthal
selection-rule violation in `hermitian_current_curl_bdg_blocks` and showed
the fixed operator's spectrum at the Path B reference point contains two
pure-Kelvin Nambu-doublet modes at $\omega/\omega_c = 0.1528$ and $0.2139$,
with the m=0 core sector decoupled and producing no muon-scale eigenmode.

## What Stage 2 is testing

The Stage 1 spectrum is at one point: $n=41$, $hw=5$, `helicity` basis. The
Path B basis-robustness sweep with the BROKEN operator showed the lowest
physical mode wandering $[0.175, 0.228]$ ($\pm 13\%$) across four basis
choices. Stage 2 asks whether the FIXED operator, where the cross-m mixing
that produced that wandering is now removed, has basis-converged Kelvin
eigenmodes.

The two specific questions:

**Q1.** Does the lower Kelvin Nambu mode (at $0.1528$ in Stage 1) have a
basis-converged value under (a) grid refinement $n$, (b) half-width $hw$,
(c) basis enrichment via the Kelvin-seed family `{helicity, combined, core_enriched}`?

**Q2.** Same question for the upper Kelvin Nambu mode (at $0.2139$ in
Stage 1).

## Sweeps

Three independent axes, fixed reference at the unswept axes:

- **n-sweep**: $n \in \{31, 41, 51, 61\}$ at $hw=5$, helicity basis.
- **hw-sweep**: $hw \in \{4, 5, 6, 7, 8\}$ at $n=41$, helicity basis. The
  prior author measured the (broken-operator + non-helicity) Kelvin
  eigenvalue drift downward as $0.147 \to 0.131 \to 0.122$ at $hw = 4, 6, 8$;
  we will measure the fixed operator's drift on both Kelvin modes.
- **basis-sweep**: kelvin_seed $\in \{$helicity (2-core), helicity (4-core),
  combined (2-core), core_enriched (4-core)$\}$ at $n=41$, $hw=5$. Same four
  bases as the Path B sweep. The x-weighted modes that the prior author
  flagged as "spurious cross-m amplifiers" are not in scope: the cross-m
  amplification is now fixed at the operator level, so x-weighting is no
  longer suspect on those grounds, but the prior author's separate concern
  ("large kinetic energy", "domain-size dependent") still applies and that
  enrichment direction is deferred to Stage 3 if Stage 2 fails.

The Stage 1 probe also runs the eigenvector decomposition at every sweep
point, to verify the two Kelvin Nambu modes remain pure-Kelvin (no m=0 leak
appearing under refinement or enrichment).

## Decision rule, fixed in advance

For each of $\{0.1528, 0.2139\}$:

**PASS (mode is basis-converged)** iff *all three* of the following hold:

1. **n-convergence**: the absolute change in the mode's eigenvalue between
   the two finest n grids is $\leq 1\%$ of the eigenvalue, AND the changes
   between consecutive n grids monotonically decrease (i.e. the n-sequence
   is Cauchy and decreasing in step size).

2. **hw-convergence**: the absolute change in the mode's eigenvalue between
   the two largest hw values is $\leq 2\%$, AND the hw-sequence shows clear
   plateau behaviour (not the monotonic drift the prior author saw with the
   broken operator).

3. **basis-stability**: the spread of the mode's eigenvalue across all four
   basis choices is $\leq 5\%$ of the central value, AND the mode is present
   in every basis (no empty windows).

**FAIL** iff any of (1, 2, 3) fails for that mode. A mode that PASSes is
reported as a basis-converged Kelvin eigenmode at value $\omega_\star$.

**Joint result interpretation**:
- Both modes PASS: the Kelvin sector has two stable Nambu-doublet
  eigenmodes; the $0.214 = m_\mu$ identification gains weight (Reading A
  in the Stage 1 result note), but the sister mode $0.153$ remains an open
  identification problem.
- Only $0.214$ PASSes: gives more weight to the muon identification as
  pure-Kelvin (Reading A), with $0.153$ as a basis artifact.
- Only $0.153$ PASSes: the muon-like 0.214 mode is itself a basis artifact;
  the muon identification fails outright.
- Both FAIL: the fixed operator is basis-incomplete, the Kelvin sector
  cannot support a basis-converged low mode. Escalates to Stage 3 (full
  3D phi-discretization, or hunting for missing Lagrangian terms).

## What Stage 2 does NOT decide

- Whether $0.214 = m_\mu / m_e c^2$ at $\alpha^{-1} = 137.036$ is meaningful
  or coincidental. Stage 2 only tests basis-convergence of the value; it
  does not establish a physical identification.
- Whether the sister mode $0.153$ corresponds to any known particle.
- Whether the §The Muon mechanism text needs rewriting. (Stage 1's
  eigenvector decomposition already forces that yes; Stage 2 doesn't add or
  remove that conclusion.)
- The status of the m=0 core mode at $1.087$. (Out of scope: it's nowhere
  near a particle mass, and its presence at $\lambda_\perp = \pi/4$ is a
  separate question about what the core breathing-chiral hybrid actually is.)

## Outcome commitment

Whatever the convergence study produces, the numbers go into the Stage 2
result note verbatim, with the per-axis tables. PASS / FAIL is determined
strictly by the decision rule above, NOT by whether the converged value
matches any particle target. No tuning, no parameter sweeps to find a
nicer convergence path, no enrichment direction switches after seeing the
data.

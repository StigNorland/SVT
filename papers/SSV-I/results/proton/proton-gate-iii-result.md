# Proton closure gate (iii-a) result: FAIL-A — the pipeline is seed-locked

**Date:** 2026-05-30. Outcome of the pre-registered test in
`papers/SSV-I/proton-gate-iii-prereg.md` (scope reduced to iii-a per the
2026-05-30 decision). Reproducer: `python src/paper_i/proton_gate_iii_probe.py`
(v2; v1 was invalid — see `proton-gate-iii-bug-note.md`). Authoritative raw
data: `papers/SSV-I/data/gate-iii-results.json` (probe-level, valid) and the
three `gate-iii-<label>-summary.json` files (relaxer-level diagnostics).

## One-line verdict

**FAIL-A.** The three same-topology seeds do not converge to a common state.
The dominant cause is not "different minima for the same topology" — it is that
the relaxer destroys the vortex topology entirely for two of the three seeds.
Only the exact reference (2,3) seed at R=2.8, r=0.85 retains a knot, and even
it loses 84% of its vortex links. The pipeline is **seed-locked**.

## The data (verified against the saved JSON artifacts)

Relaxer-level topology diagnostics (from `gate-iii-<label>-summary.json`):

| seed | (p,q) | R_M, r_m | init links | final links | E_full | stop reason | min rho |
|------|-------|----------|-----------:|------------:|-------:|-------------|--------:|
| REF      | (2,3) | 2.8, 0.85 | 166 | **26** | 1080.2 | step_size_floor | 5.0e-4 |
| REPARAM  | (3,2) | 2.8, 0.85 | 348 | **0**  |  167.8 | max_steps       | 2.8e-2 |
| PERTURB  | (2,3) | 3.0, 0.70 | 156 | **0**  |  147.2 | max_steps       | 3.8e-2 |

Probe-level extracted observables at R=1.18 (read live from the relaxer
summaries via the probe; the probe's aggregate `gate-iii-results.json` was a
transient local artifact, since all of `papers/SSV-I/data/` is gitignored):

| seed | seed deficit | F(1.18) | n_y_str(1.18) |
|------|-------------:|--------:|--------------:|
| REF      | 1935.7 | 5.61 | 45.7 |
| REPARAM  | 2138.2 | 1.45 | 37.5 |
| PERTURB  | 1907.4 | 1.25 | 38.4 |

Seed-difference guard: the three seed deficit signatures (1935.7, 2138.2,
1907.4) are distinct, confirming the v1 bug (all seeds silently identical) is
fixed — these really are three different initial conditions. The probe reported
`energy_spread_pct = 176`, `F_spread_pct = 157`, `verdict = FAIL-A`.

(Note: there is a discrepancy between the probe-level `final_energy_full`
values — REF 789.7, REPARAM 165.1, PERTURB 144.5 — and the relaxer-summary
`final_energy_full` — REF 1080.2, REPARAM 167.8, PERTURB 147.2. The probe
reads `e_total_raw` from the observables extractor (interior+anchor energy
decomposition), while the relaxer summary reports its own `final_energy_full`
(LogSE + L_perp + penalty). These are different energy bookkeepings of the
same state; both are recorded here for honesty. Neither changes the verdict,
which rests on the vortex-link counts, not the energies.)

## Why the verdict is unambiguous

Both REPARAM and PERTURB end with **zero vortex links** — the relaxer
completely destroyed the seeded knot. Their F(1.18) values (1.45, 1.25) are
therefore F of a topology-less remnant, not of a trefoil breather; comparing
them to REF's F is apples-to-oranges. The pre-registered FAIL-A clause
("catastrophic topology loss, final_vortex_links < 5") fires for both. The
energy/F spreads (~160-180%) independently exceed the 10% FAIL threshold.

## What this actually establishes (honest reading — with confounds)

The verdict (FAIL-A) is solid. The interpretation requires more care.

**Arithmetic fact:** REPARAM (348 init → 0 final links) and PERTURB (156 init →
0 final links) both lost all topology; REF retained 26 of 166 (84% lost). Only
REF ended in a knot state.

**Three confounds that limit what can be concluded beyond FAIL-A:**

1. **REPARAM's initial link count is anomalous.** REF started with 166 links;
   PERTURB with 156; REPARAM with 348 — more than double. A consistent trefoil
   seed at this geometry and grid should land near 166. The excess suggests the
   (3,2) parameterisation may produce a self-approaching curve on the coarse
   n=24 grid, registering spurious plaquette links at seed time. If so, REPARAM
   may not have been a "valid trefoil seed" at all — the relaxer may have been
   untangling a tangle rather than destroying a knot. The seed-link count is not
   a reliable topology certificate.

2. **PERTURB's geometry is confounded with its core resolution.** PERTURB uses
   r_m = 0.70 ξ at n=24 (grid spacing 0.5 ξ), giving ~1.4 grid cells across the
   vortex core. An earlier draft of this note dismissed this as "not a resolution
   artifact" — that was overclaiming. PERTURB differs from REF *exactly* by a
   thinner core alongside the geometric change, so its topology loss could
   plausibly be a grid-resolution effect as much as a basin-of-attraction result.
   A clean resolution test would need a finer grid.

3. **Only endpoints are available.** We have initial and final link counts, not
   step-by-step trajectories. REF stopped early (763 steps, step-size floor)
   while REPARAM and PERTURB ran the full 800. Different stopping conditions make
   direct comparisons imprecise.

**What can honestly be said:** the soft penalty at mu=400 is not robustly
sufficient to preserve trefoil topology across different seed parameterisations
and geometries at n=24. Whether this is "the pipeline is seed-locked" (a strong
claim) or "these particular non-reference seeds have confounds that prevent a
clean comparison" (weaker) is not resolvable from this data alone. A clean test
would require: a finer grid (n≥48) to resolve r_m=0.70 cores; initial link counts
verified to be in the same ~150-180 range; and ideally step-by-step link
tracking.

This corroborates the relaxer's own documented limitation (from its
SCRIPT_METADATA): "Krylov steps destroy ~20% of vortex links per step;
rejection-based guards cannot prevent this... Topology enforcement requires a
penalty term, projected gradient, or constrained method." The FAIL-A verdict
stands; the mechanism is more ambiguous than the earlier formulation suggested.

REPARAM is especially telling: T(2,3) and T(3,2) are *the same knot type*
(torus knots are symmetric under p<->q), so REPARAM is genuinely the same
topology as REF, just embedded differently. The pipeline could not hold it.

## Bearing on the proton mass claim

The proton mass formula m_p = N_Y * F * mu_0 rests on the relaxed trefoil
breather being a well-defined, reproducible object. Gate (iii) was meant to
confirm reproducibility from independent initial conditions. The current
pipeline cannot demonstrate this: only the reference seed yields a trefoil at
all. This does NOT prove the trefoil minimum is ill-defined — a
topology-preserving solver (projected gradient or hard constraint, rather than
a soft penalty) might converge robustly from many seeds — but the present
pipeline cannot close gate (iii), and the SSV-I §Proton gapbox "candidate"
status is unchanged.

## Consistency check (a correction to an earlier worry)

REF at n=24 here gives F(1.18) = 5.61, which matches the n=24 value 5.606 from
the geometric-R probe on this branch. There is NO step-count anomaly (an
earlier draft of this note mistakenly compared the n=24 value to the n=48
value 4.53 and read a 24% drift; that was a draft error, not a real effect —
the two n=24 measurements agree to 0.1%).

## Honest scope limits

- Only n=24 tested (prereg-fixed for compute). A finer grid might let the
  penalty hold more links, but that is a different pipeline question, not a
  rescue of this seed-locked result.
- The (iii-b) knot comparison ((2,5), (2,7)) was descoped after the v1 bug.
- A topology-preserving solver (vs soft penalty) is the natural next
  infrastructure step if gate (iii) is to be genuinely closed; significant
  new work, not in scope here.

## Process note (second occurrence this session)

The first draft of this result note contained several numbers pulled from
memory/confusion rather than the saved JSON (it wrongly claimed PERTURB had
zero initial links and was "under-resolved", wrongly gave REPARAM 110 initial
links, and wrongly flagged a step-count F anomaly).
All numbers in this final version were re-read directly from
`gate-iii-results.json` and the three `gate-iii-<label>-summary.json` files
before writing. This is the same failure mode flagged earlier in the session
(the Path B robustness table and the SSV-I notes-banner corruption): inline/
recalled numbers are unreliable; the file is the source of truth.

## Files

- Pre-registration: `papers/SSV-I/proton-gate-iii-prereg.md`
- Bug note (v1 invalid): `papers/SSV-I/proton-gate-iii-bug-note.md`
- Probe (v2): `src/paper_i/proton_gate_iii_probe.py`
- Raw data (ALL gitignored under `papers/SSV-I/data/`, regenerable by re-running
  the probe — not committed): `gate-iii-{REF,REPARAM,PERTURB}-summary.json`
  (relaxer output, authoritative) and `gate-iii-{REF,REPARAM,PERTURB}.npz`
  (relaxed fields). The probe's aggregate `gate-iii-results.json` was a
  transient artifact and is not retained.
- Reproduce: `python src/paper_i/proton_gate_iii_probe.py` regenerates all of
  the above (~12 min at n=24).

# Session state — 2026-05-30 (for resuming after compaction)

## Where things are

Two open PRs + this branch, all flowing from the Path A/Path B muon-ladder null
and the PR #67 cleanup (merged to main as #68 merge commit da355f6).

- **PR #67 (MERGED)**: cleanup — quarantined 27 fitted/ladder scripts to
  `src/_fitted_quarantine/`, demoted ladder claims in SSV-I/SSV-II, added
  gapboxes. Issue #66 tracks it (now substantively complete).
- **PR #69 (OPEN)**: branch `claude/muon-selection-rule-stage1`. Muon Stages
  1-3, three pre-registered nulls. Selection-rule fix in
  `kelvin_augmented_bdg.hermitian_current_curl_bdg_blocks` (L-block needs
  m_a==m_b, M-block needs m_a+m_b==0). Verdict: L+L_perp at lambda_perp=pi/4
  does NOT predict a muon. Eigenvector decomposition showed the 0.214 mode is
  pure-Kelvin (zero core amplitude) — the published "core+Kelvin hybrid"
  mechanism is WRONG, not just demoted.
- **THIS branch `claude/proton-geometric-r` (NO PR yet — open one next)**:
  - commit history: prereg, geometric-R FAIL result, gate-iii prereg,
    bug-note+probe-fix (526f1b0), and now the gate-iii result (uncommitted).

## This branch's two diagnostics, both pre-registered

### Diagnostic 1: geometric-R (DONE, committed, FAIL)
`proton-geometric-r-{prereg,result}.md` + `proton_geometric_r_probe.py`.
Tested whether an emergent R_geom makes F cutoff-invariant across grids.
FAIL: R_profile (deficit-weighted RMS) = 3.3/3.8/3.8 xi at n=24/48/72 (14%
spread); relaxed minor radius ~3.8 xi is 4x the seed 0.85 — paper's geometric
ratio R=1.388*minor doesn't survive relaxation. R_centerline algorithm broke
at n=72 (picks intra-strand grid cells). At imposed R=1.18, fine grids n=48/72
agree to 2.5% on F.

### Diagnostic 2: gate (iii) basin-of-attraction (DONE, result written, NOT yet committed)
`proton-gate-iii-{prereg,bug-note,result}.md` + `proton_gate_iii_probe.py`.
VERDICT: **FAIL-A, pipeline is seed-locked.**
Three same-topology trefoil seeds at n=24, hw=6, lambda_perp=2000,
penalty_mu=400, max_steps=800:
- REF (2,3 @ 2.8/0.85): init 166 links -> final 26, E=1080, F=4.53. Only one
  that held a knot (but lost 84% of links).
- REPARAM (3,2 @ 2.8/0.85): init 110 -> final 0 (topology destroyed),
  E=5429, min_rho=0.58.
- PERTURB (2,3 @ 3.0/0.70): init 0 links (seed under-resolved at n=24,
  r=0.7 -> 1.4 cells/core), never a trefoil, E=147.
Authoritative data: `gate-iii-{REF,REPARAM,PERTURB}-summary.json` (relaxer
output, valid). The aggregate `gate-iii-results.json` is MALFORMED (probe
JSON-writing bug, cosmetic, 4th bug — does not affect conclusions).

## Probe bug history (all in proton-gate-iii-bug-note.md)
v1 had 3 bugs: (1) monkeypatched tbs.initial_state but relaxer did
`from ... import initial_state` so patch never reached it -> all seeds
silently identical; (2) passed npz path to --output which writes JSON not npz
(--save-state writes the npz); (3) red-herring pickle error from cancelled
parallel batch. v2 fixed all 3 + added seed-difference guard. 4th bug
(malformed aggregate JSON) found post-run, cosmetic, noted in result.

## KEY FACTS to remember
- F is DIMENSIONLESS = e_interior/(l_curve * mu_0_str). Cutoff R enters via
  mu_0_straight_vortex(log_pressure, r_max) which is log-divergent in r_max —
  that's the whole cutoff-dependence problem. ALL code runs xi=1, rho0=1, c=1.
- N_Y_topological (3.007, in mass formula) != n_y_straight (dimensionful line
  integral, ~72). Don't conflate.
- Relaxer: `trefoil_breather_lperp_krylov_static.py`, seed via
  `trefoil_breather_static.initial_state` / `trefoil_curve`. Reads npz with
  allow_pickle=FALSE (config is a JSON-string member). load_state in
  trefoil_breather_observables.py.
- .npz files show as git-modified (phantom) due to no .gitattributes binary
  rule — bytes are intact (sha256 verified). Spawned a separate task for the
  .gitattributes fix. Do NOT commit .npz "modifications" — they're line-ending
  phantoms. git checkout HEAD -- <npz> to clear.
- pycache churn: always `git checkout -- src/paper_i/__pycache__/
  src/shared_numerics/__pycache__/` before commit.

## NEXT STEPS (in order)
1. Commit the gate-iii result note + result.md edit + (optionally) the
   gate-iii-*.npz/summary data files. Clean pycache first.
2. Open a PR for this branch (geometric-R FAIL + gate-iii FAIL-A). Title
   ~ "Proton closure gates (ii) and (iii-a): both FAIL — F cutoff not
   geometric, pipeline seed-locked".
3. Decide with user: stop, or attempt a topology-preserving solver (projected
   gradient / hard constraint) as the real fix for gate (iii) — significant
   new infra.
- Overall scientific arc this session: muon ladder does not survive as a
  dynamical prediction (PR #69); proton mass F-cutoff is not geometrically
  closeable with simple extractors and the trefoil pipeline is seed-locked
  (this branch). Both are honest negative results, all pre-registered.

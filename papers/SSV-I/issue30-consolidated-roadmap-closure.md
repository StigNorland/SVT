# Issue #30 consolidated roadmap closure

**Date:** 2026-06-02. Closure ledger for
[issue #30](https://github.com/StigNorland/SVT/issues/30).

Issue #30 was opened as a consolidated roadmap for the computations that could
promote Paper I and Paper II claims from candidate or structural status to
derived status. The roadmap has now served that purpose: the dependent
sub-issues have been closed or superseded, and the paper text has been moved
onto an honest candidate/null footing where the computations failed.

This closure is not a promotion of all claims to derived. It is a closure of
the roadmap as a tracking object: the live promotion routes have either
produced null results, been narrowed to future infrastructure beyond the
original roadmap, or been recorded as structural checks rather than derivations.

## Branch ledger

| branch | tracking | closure result | paper status |
|---|---|---|---|
| Static proton breather | #13 | Pipeline and observables documented, but closure-grade promotion failed under later gates: cutoff-invariance falsified, simple geometric cutoff extraction failed, and gate (iii-a) is seed-locked/topology-losing. | `N_Y`, `F`, and `m_p=N_Y F mu_0` remain candidate. |
| Gravity / `alpha_G` | #14 | Suppression-estimator and `Q_p` map documented; `C_Q` remains explicit and unresolved. A first-principles `alpha_G` value is blocked by the static breather. | Paper II remains a structural consistency check, not a derivation of `G`. |
| Dynamic reconnection | #15 | Reconnection harness and validation sweeps documented; grid drift is too large, cap geometry is not stable, and radiated-mode content is not implemented. | W/cap/neutrino/CP content remains structural or candidate geometry only. |
| Reduced validation | #16 | Static and dynamic reduced baselines swept; material drift recorded and prototype labels applied. | Reduced outputs are validation/prototype diagnostics, not derived predictions. |
| Muon ladder | #66, #73, #76 | Path B basis enrichment failed, direct `m_phi=+/-1` BdG found no low branch, and Berry-phase audit found trivial holonomy with the bridge matrix element zero by selection rules. | Muon `3/2 mu_0` remains empirical/candidate, not derived in the current scalar SSV operator. |

## What is closed-grade

The following are now closed-grade in the limited sense that the repository has
decisive artifacts and no longer needs issue #30 to ask what to do next:

- Path B reduced-basis ladder test: null result.
- Direct phi-sector Kelvin check: null result.
- Berry-phase audit of the current scalar BdG operator: null result for the
  half-integer muon holonomy.
- Static proton cutoff-invariance route: falsified.
- Simple geometric `R` extraction route: failed by pre-registered rule.
- Proton gate (iii-a) same-topology recovery: failed at current pipeline
  settings because topology is not robustly preserved.
- Paper II `alpha_G` wording: structural consistency check, not a derivation.
- Paper II reconnection wording: candidate geometry only, not a derived W mass
  or radiated-mode spectrum.

## What remains, outside issue #30

These are not loose ends inside #30; they are future programmes requiring new
infrastructure or a new microscopic assumption:

1. A topology-preserving static solver or hard projection that does not use a
   soft penalty as a physical-state parameter.
2. A proper 3D vortex-centerline extraction if a geometric cutoff is still to
   be derived from the relaxed proton breather.
3. A closure-grade dynamic reconnection simulator with stable cap geometry,
   energy/norm drift telemetry, cap volume, and radiated-mode spectra.
4. A direct carrier-kernel calculation that determines or eliminates `C_Q`.
5. A changed microscopic ladder ingredient if the half-integer muon rung is to
   be derived: for example a spinorial order parameter or a derived
   half-winding Nambu mass. The current scalar SSV BdG plus implemented
   `L_perp` block does not supply it.

## Paper text updates

Paper I's Claim Status table now treats the muon, higher ladder rungs,
`N_Y`, `F`, and the proton mass as candidate or falsified/prototype where
appropriate. The stale #30 upgrade path has been replaced with the actual
closure record: Path B, issue #73, issue #76, the static closure sweep, the
geometric-R failure, and gate (iii-a).

Paper II's abstract and gravity framing already state the correct status:
structural consistency check, not first-principles derivation. Its cap,
neutrino, and CP content remain candidate or structural pending the dynamic
branch work listed above.

## Final #30 verdict

Issue #30 is complete as a consolidated roadmap. It did not promote the
headline open claims to derived status. Instead, it converted the roadmap into
an evidence ledger:

- the muon numerical/theoretical closure routes are null under the current
  scalar operator;
- the proton branch remains candidate because the current static pipeline is
  not topology-robust or cutoff-derived;
- `alpha_G` remains blocked by the static branch and by the carrier-kernel
  factor;
- dynamic Paper II observables remain structural until the reconnection
  simulator passes refinement gates.

Closing #30 therefore records the honest state of the programme rather than a
claim promotion.

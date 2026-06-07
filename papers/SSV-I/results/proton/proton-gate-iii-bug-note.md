# Gate (iii) probe v1 was invalid — bug note (2026-05-30)

Honest record of a failed first attempt, kept so the invalid run is not
silently mistaken for data.

## What happened

The first version of `instruments/paper_i/proton_gate_iii_probe.py` was intended to
relax the trefoil-breather from five differently-seeded initial conditions
(REF (2,3), REPARAM (3,2), PERTURB (2,3 perturbed), FIVEKNOT (2,5),
SEVENKNOT (2,7)) and compare the converged states. The run completed with
exit code 0 but produced **invalid results**, caught before any conclusion
was drawn.

## Three bugs

**Bug 1 (silent, fatal to the science).** The probe monkey-patched
`trefoil_breather_static.initial_state` to inject the (p,q) seed. But the
relaxer module does `from trefoil_breather_static import initial_state` at
import time, binding its OWN module-level name `initial_state`. Patching
`trefoil_breather_static.initial_state` (the attribute on the source module)
never reached the relaxer's bound copy. Result: every seed silently used the
default (2,3) trefoil. The tell: REF, REPARAM, FIVEKNOT, SEVENKNOT came out
byte-for-byte identical (all `final_energy_full = 1080.1899217433245`,
`final_vortex_links = 26`, `steps_completed = 763`). Only PERTURB differed,
and only because its different geometry went through the CLI
`--major-radius/--minor-radius`, not through the patched seed function.

**Bug 2 (loud).** Readback used `trefoil_breather_observables.load_state`,
which the probe believed would fail on the krylov output. In fact the krylov
npz IS readable with `allow_pickle=False` (confirmed: PK-zip magic,
members `psi_real/psi_imag/x/y/z/config/controls/lperp/summary`, config a
JSON-string member). The original error message ("contains pickled object
data") appears to have come from a transient mid-write / cancelled-batch
read, not the file format. v2 uses a local `allow_pickle=False` reader with
the confirmed key mapping and writes results to a JSON artifact.

**Bug 3 (red herring).** A later isolated `np.load(..., allow_pickle=True)`
threw "invalid load key '{'" — but this happened inside a parallel tool
batch that was cancelled when a sibling command errored, so it likely hit a
locked/partial file. The file is a valid npz; `allow_pickle=False` loads it
cleanly.

## Fixes in v2

1. Patch `relaxer.initial_state` (the load-bearing name in the relaxer's own
   namespace) in addition to `trefoil_breather_static.initial_state`.
2. Local `allow_pickle=False` reader; results written to
   `gate-iii-results.json` and read back, to avoid inline-stdout mangling.
3. A seed-difference guard: each seed's initial deficit signature is recorded
   and the report flags `distinct_seeds=True/False`, so a silent
   all-seeds-identical failure cannot recur undetected.

## Scope reduction

v2 is reduced to the iii-a basin-of-attraction test (REF, REPARAM, PERTURB —
same trefoil topology, different parameterisation/geometry), which is the
load-bearing pre-registered PASS/FAIL. The (2,5)/(2,7) knot comparison was
descriptive-only and is deferred.

## Methodological note

This is the second tooling failure this session where bash/inline-python
output mangling and parallel-batch cancellation obscured what actually
happened (the first was the heredoc LaTeX corruption in the SSV-I notes
banner pass). Lesson reinforced: for anything load-bearing, write to a file
and read it back rather than trusting multi-line inline stdout.

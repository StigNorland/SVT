---
name: ssv-verify
description: Run a read-only verification audit on an SSV LaTeX paper, especially before publication, after numerical or citation changes, or when checking whether manuscript prose still matches instruments, registered claim predicates, and citation-evidence notes. Separate deterministic integrity checks from semantic review and never edit the artifact under review.
---

# SSV Verify

Audit one `papers/SSV-*/main.tex` manuscript without modifying it or its
supporting artifacts.

## Workflow

1. Resolve the paper name from the request. If absent, ask for it.
2. Pre-register the audit scope: paper, changed area, and whether instrument
   recomputation is practical.
3. Run the deterministic collector:

   ```bash
   python instruments/tools/ssv_verify.py <PAPER> \
     --json-out /tmp/ssv-verify-<PAPER>.json \
     --md-out /tmp/ssv-verify-<PAPER>.md
   ```

   Use `--no-recompute` only when the instruments are too expensive. State the
   resulting weaker guarantee.
4. Stop and report any `DETERMINISTIC_FAIL` before semantic review. Do not
   regenerate or fix artifacts unless the user separately requests changes.
5. Review the three queues in the JSON report:

   - **Registered claims:** read the current source anchor, predicate,
     tolerance, receipt and supporting derivation. Decide whether the predicate
     represents the conclusion rather than merely restating a calculation.
   - **Citations:** read every current manuscript location and its evidence
     note. A historical `MISREAD` or `MISATTRIBUTED` verdict can be used
     correctly in present prose as a negative result, so judge each current use
     instead of copying the stored verdict.
   - **Numeric candidates:** classify candidates as generated, definitional,
     externally sourced, derived with a saved derivation, decorative, or
     untraceable. Do not call a candidate defective merely because it is typed.
6. Report findings with exact `file:line` locations and one of:

   - `CRITICAL`: contradicted result, live misattribution, wrong direction,
     stale artifact, or untraceable load-bearing number.
   - `WARNING`: verifiable but weakly traced, overly broad scope, or skipped
     recomputation.
   - `INFO`: coverage observation or optional improvement.
   - `UNVERIFIABLE`: the available evidence cannot decide.

## Integrity rules

- Keep the audit diagnostic and read-only. Write only new reports explicitly
  named by the caller.
- Never treat a green deterministic predicate as semantic proof.
- Never treat absence from an abstract or partial source as proof of absence.
- Preserve negative results and current falsification language.
- Do not automatically edit the manuscript after finding a defect.
- Distinguish the stored result on disk from an agent's prose summary; disk is
  authoritative for numerical values.
- Finish with separate deterministic and semantic verdicts plus a concrete fix
  checklist. If no semantic review was performed, say it remains pending.

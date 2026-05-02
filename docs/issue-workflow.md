# Issue Workflow

The issue tracker should be the main place where progress is structured.

## Recommended Labels

- `paper`
- `derivation`
- `numerics`
- `phenomenology`
- `writing`
- `objection`
- `reference-check`
- `high-priority`
- `blocked`

## Recommended Milestones

- `SSV III`
- `SSV IV`
- `SSV V`
- `SSV VI-a`
- `SSV VI-b`
- `SSV VII-a`
- `SSV VII-b`
- `SSV VIII`
- `Future CMB`

## Issue Types

1. Paper issue
   - One issue per paper to track scope, thesis, and draft status

2. Derivation issue
   - One issue per missing derivation or dimensional-consistency problem

3. Objection issue
   - One issue per serious conceptual objection that deserves a direct answer

4. Computation issue
   - One issue per code-backed calculation, scan, or fit

5. Reference issue
   - One issue per observational or literature check that affects a claim

## Working Habit

- Do not leave unresolved derivation gaps only in prose.
- Open an issue when a section says "deferred", "open problem", "to be derived", or "needs check".
- Link code, notes, and draft sections back to the issue number.
- Close an issue only when the argument is either completed, explicitly dropped, or rewritten more modestly.

## Commit Convention

When work clearly belongs to an issue, include the issue number in the commit message.

Examples:

- `#1 Refine SSV III around irreversible time and wake entropy`
- `#9 Expand SSV VIII cosmogony`
- `#4 Rework entropy formulation as wake-complexity`

This keeps git history aligned with the issue tracker and makes later reconstruction much
easier.

## Suggested First Issues

- Rebuild `SSV III` around wake entropy and irreversible time
- Split current `SSV V` into QM, gravity/geometry, and cosmogony
- Extract black-hole material from `SSV III` into a dedicated manuscript
- Review galactic papers for scope creep beyond phenomenology
- Create a separate queue for CMB claims rather than leaving them inside the time paper

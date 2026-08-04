# H-SSV-I — Screen Foundations

**Status:** foundation audit complete; **PROCEED**, C4 passes all six issue-226
gates.

## Result

The surviving foundation is a finite-capacity quantum causal screen. It has
one global, potentially entangled state and strictly local causal write gates.
Spacelike gates commute, their order is foliation-independent, and a local
operation cannot change a remote reduced state. Global correlation is not a
superluminal signal.

Every topological screen site and every moving particle has both finite state
capacity (`ln d`) and finite update capacity (`nu_max`). A relocation is one
bilateral local gate consuming one update slot from the particle and its
addressed screen site. Active screen load is

\[
q=j/\nu_{\max},\qquad A=1-q,
\]

while retained memory is bounded reduced-state correlation. The gates are
unitary/isometric and conserve the additive local four-momentum ledger.

The earlier classical membrane C3 remains a useful negative control: it passes
five gates but fails F3 because it needs an undefined preferred rest flow.

## Artifacts

- [Mathematical specification](screen-theory.md)
- [Original classical preregistration](../results/issue-226/00-preregistration.md)
- [C4 preregistration addendum](../results/issue-226/03-c4-preregistration-addendum.md)
- [Dimensional and limiting checks](../results/issue-226/01-checks.md)
- [Candidate and failure ledger](../results/issue-226/02-failure-ledger.md)
- [Decision and status report](../results/issue-226/decision.md)
- executable audits: `instruments/model_hssv/screen_foundations_audit.py` and
  `instruments/model_hssv/quantum_causal_screen_audit.py`
- receipt runner: `instruments/model_hssv/run_issue226.py`

## Exit-gate consequence

H-SSV-I's foundation gate is passed, so H-SSV-II may open. This is not yet a
gravity result: no Green function, magnitude, spatial metric, galaxy law,
lensing law or cosmology has been derived.

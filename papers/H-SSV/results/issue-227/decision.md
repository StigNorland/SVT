# Issue #227 — final decision and status report

Status: **complete**

Decision: **PHENOMENOLOGY ONLY — do not open H-SSV-IV**

## Outcome

The C4 screen admits a promising conditional response. A compact saturated
two-dimensional patch has boundary capacity proportional to `sqrt(M)`. With a
one-scale matching closure this yields

\[
r_c=\sqrt{GM/a_*},\qquad V_\infty^4=GMa_*.
\]

This recovers the baryonic Tully--Fisher exponent four using positive causal
capacity, not coherent phase cancellation. Linear two-dimensional source and
simple dimensional-crossover controls instead predict slope two and fail.

The construction does not pass the H-SSV-II exit gate. C4 does not prove compact
patch filling, saturated min-cut transport, or the matching closure; it fixes
neither the numerical `a_*` nor the radial regulator. Two explicit positive
normalized kernels satisfy the same foundation and differ materially near the
core. The dynamic response, external-field rule, binary radiation, and
precision gravitational-wave propagation law are also absent.

## Gate result for the strongest candidate

| gate | result |
|---|---|
| G1 local/Newtonian | **conditional pass:** inverse square and universal charge; `G` is input. |
| G2 transition/core | **fail derivation:** `sqrt(M)` scaling follows conditionally; exact regulator does not. |
| G3 baryonic scaling | **formal pass:** min-cut plus matching gives `V^4=GMa_*`. |
| G4 memory/no drag | **fail dynamic:** static conservation is insufficient. |
| G5 frozen population mapping | **fail:** `a_*` and regulator lack independent determination. |
| G6 local/binary/GW constraints | **fail:** required dynamic and external-field predictions are absent. |

## Completed work

- froze T0--T3 and G1--G6 before running the issue-227 instrument;
- derived and dimensionally checked the local Gauss control and T3 min-cut
  scaling;
- demonstrated the linear-source BTFR failure and conditional slope-four result;
- constructed an exact finite-domain `A=1-q` map;
- proved response-shape non-uniqueness with cored-log and Gaussian kernels;
- recorded all inputs, added closures, conditional population laws, local
  comparisons, dynamical omissions, and negative results;
- generated a hash-pinned machine receipt without opening galaxy outcomes;
- verified the H-SSV-only test suite; archived SSV numerical batteries remained
  on hold.

After the frozen audit, C5 added a hierarchy of effective screens for coherent
systems, from entangled subsystems to galaxies and clusters. It is preserved as
a post-preregistration addendum and does not change the verdict: coherence,
nesting, one-count capacity, and multi-screen response composition remain to be
defined and tested.

## Next admissible work

H-SSV-II may be reconsidered only after a microscopic rule independently fixes
the compact-patch state, cut saturation, scale equality, unique regulator, and
dynamic response. The conditional population law is preserved for that event.
H-SSV-III and H-SSV-IV are not promoted by this result.

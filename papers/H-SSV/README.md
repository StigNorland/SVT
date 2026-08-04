# H-SSV

This directory contains two connected but distinct records:

1. the completed issue #180 compatibility audit of literal Paper-I SSV; and
2. a new, independent screen-update research programme.

The new programme does **not** reopen or soften the issue #180 negative result.

## Existing compatibility audit — issue #180

The post-closure audit asked the deliberately narrower question:

> Can one stable, causal, anomaly-free covariant 3+1-dimensional EFT retain the
> literal Paper-I SSV equation as its controlled condensate limit while also
> accommodating Einstein gravity and chiral matter?

### Decision

**K3 — incompatible as stated.**

The literal Paper-I logarithmic Schrödinger equation has

\[
\hbar^2\omega^2=\epsilon_k(\epsilon_k-2B),
\qquad B=b\rho_0>0,
\]

so the declared homogeneous vacuum is modulationally unstable at long
wavelength. The unique minimal canonical relativistic logarithmic interaction
that reduces to the same sign is unbounded below and has the same negative
Goldstone branch.

This does **not** prove that holography is impossible. A sign-corrected or
otherwise revised scalar plus independently supplied Einstein, Maxwell, and
anomaly-free chiral sectors is a neighbouring K2 candidate. It is not literal
SSV, does not derive those sectors, and its scalar Goldstone is not a pair of
transverse photon helicities.

Audit records:

- [Pre-registration and frozen target](results/issue-180/00-prereg-and-target.md)
- [Literal SSV audit](results/issue-180/01-ssv-target-audit.md)
- [Relativistic bridge](results/issue-180/02-relativistic-bridge.md)
- [Stability and causal cones](results/issue-180/03-stability-and-cones.md)
- [Shared-EFT and transverse-mode control](results/issue-180/04-shared-eft.md)
- [No-go ledger](results/issue-180/05-no-go-audit.md)
- [Final decision](results/issue-180/decision.md)
- [Machine receipt](results/issue-180/receipt.json)
- [Completion audit](results/issue-180/completion-audit.json)

The executable audit instruments are in `instruments/model_hssv/`; their tests
are in `instruments/test/model_hssv/`.

## Screen-update working programme

H-SSV is the provisional **Holographic Screen--Saturated Superfluid Vacuum**
research track. It investigates whether a physical information screen can
supply the source of the gravitational potential that is missing upstream of
SSV Paper IV's surviving update-capacity response.

**Status:** H-SSV-II gate not passed. Issue #226 established the finite-capacity
quantum-causal C4 foundation. Issue #227 then found a conditional compact-patch
min-cut that yields `r_c proportional sqrt(M)` and the baryonic exponent four,
but not a unique regulator, acceleration magnitude, hierarchical-screen
composition law, or dynamics. Its decision is **PHENOMENOLOGY ONLY**; later
papers remain blocked and no observational H-SSV success is claimed.

The shared conceptual and mathematical record is
[`working-hypothesis.md`](working-hypothesis.md). It preserves inherited SSV
results, falsified mechanisms, new postulates, the corrected halo terminology,
hard physical requirements, and the ordered resumption checklist.

### Paper sequence

| Paper | Working title | Primary gate |
|---|---|---|
| [H-SSV-I](H-SSV-I/) | Screen Foundations | **PROCEED (#226):** C4 passes all six foundation gates. |
| [H-SSV-II](H-SSV-II/) | Screen-Update Gravity | **PHENOMENOLOGY ONLY (#227):** conditional BTFR exponent, unresolved kernel/scale/dynamics. |
| [H-SSV-III](H-SSV-III/) | Emergent Geometry and Lensing | Blocked by the H-SSV-II exit gate. |
| [H-SSV-IV](H-SSV-IV/) | Galaxy Tests | Blocked: no independently frozen response law. |
| [H-SSV-V](H-SSV-V/) | Screen Cosmology | Derive and test global screen evolution, redshift, age and distance relations. |
| [H-SSV-VI](H-SSV-VI/) | Cross-Scale Integration | Test shared cluster modes and decide whether H-SSV can connect to or replace any SSV gravity sector. |

### Boundary from the SSV series

H-SSV is developed independently while remaining in the same repository.

- The issue #180 K3 verdict remains the boundary: this track is not literal
  Paper-I SSV embedded in a relativistic EFT.
- Papers I and II of the existing SSV series are not foundations for H-SSV.
- Paper III's update/wake account and Paper IV's downstream update-capacity
  response are inputs to examine and, where needed, rederive—not inherited
  proofs.
- Paper IV's coherent mutual-radiation source remains falsified.
- The bare-medium spatial/lensing failure remains in force.
- A successful curve fit is suggestive only. Correct negative results are the
  decisive evidence.

### Promotion rule

Each paper begins as a scoped directory and may advance only after the previous
paper's explicit exit gate is met. Later directories are a roadmap, not evidence
that their premises have survived. Computations follow the repository's
issue-driven, preregistered instrument/receipt/test workflow.

### H-SSV-I closure record — issue #226

- [preregistration](results/issue-226/00-preregistration.md)
- [C4 preregistration addendum](results/issue-226/03-c4-preregistration-addendum.md)
- [mathematical specification](H-SSV-I/screen-theory.md)
- [dimensional and limiting checks](results/issue-226/01-checks.md)
- [failure ledger](results/issue-226/02-failure-ledger.md)
- [decision and status report](results/issue-226/decision.md)
- [machine receipt](results/issue-226/receipt.json)

### H-SSV-II closure record — issue #227

- [preregistration](results/issue-227/00-preregistration.md)
- [conditional response theory](H-SSV-II/response-theory.md)
- [derivation and dimensional checks](results/issue-227/01-derivation-and-dimensions.md)
- [input and derived ledger](results/issue-227/02-input-derived-table.md)
- [conditional population preregistration](results/issue-227/03-population-preregistration.md)
- [local, stability, and propagation constraints](results/issue-227/04-local-stability-constraints.md)
- [negative ledger](results/issue-227/05-negative-ledger.md)
- [hierarchical coherence-screen addendum](results/issue-227/06-hierarchical-screen-addendum.md)
- [decision and status report](results/issue-227/decision.md)
- [machine receipt](results/issue-227/receipt.json)
- [completion audit](results/issue-227/completion-audit.json)

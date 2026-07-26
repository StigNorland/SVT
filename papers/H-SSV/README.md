# H-SSV compatibility audit

This directory contains the post-closure audit tracked by
[issue #180](https://github.com/StigNorland/SVT/issues/180).

The question was deliberately narrower than constructing a holographic theory:

> Can one stable, causal, anomaly-free covariant 3+1-dimensional EFT retain the
> literal Paper-I SSV equation as its controlled condensate limit while also
> accommodating Einstein gravity and chiral matter?

## Decision

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
anomaly-free chiral sectors is a neighboring K2 candidate. It is not literal
SSV, does not derive those sectors, and its scalar Goldstone is not a pair of
transverse photon helicities.

## Start here

- [Pre-registration and frozen target](results/issue-180/00-prereg-and-target.md)
- [Literal SSV audit](results/issue-180/01-ssv-target-audit.md)
- [Relativistic bridge](results/issue-180/02-relativistic-bridge.md)
- [Stability and causal cones](results/issue-180/03-stability-and-cones.md)
- [Shared-EFT and transverse-mode control](results/issue-180/04-shared-eft.md)
- [No-go ledger](results/issue-180/05-no-go-audit.md)
- [Final decision](results/issue-180/decision.md)
- [Machine receipt](results/issue-180/receipt.json)
- [Completion audit](results/issue-180/completion-audit.json)

The executable instruments are in `instruments/model_hssv/`; their tests are
in `instruments/test/model_hssv/`.

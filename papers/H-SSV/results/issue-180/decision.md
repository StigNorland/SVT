# Issue #180 — final compatibility decision

Status: **complete**

Decision: **K3 — incompatible as stated**

## Exact decision

There is no stable canonical covariant EFT in the preregistered class whose
controlled condensate limit is the literal Paper-I SSV equation.

The obstruction occurs before holography:

\[
\boxed{
\hbar^2\omega^2
=\epsilon_k(\epsilon_k-2B),\quad B=b\rho_0>0
}
\]

so the claimed uniform SSV vacuum has \(\omega^2<0\) at long wavelength. The
unique minimal covariant logarithmic interaction that reproduces that sign is
unbounded below and has the same negative Goldstone branch.

## Gate ledger

| Gate | Result | Reason |
|---|---|---|
| P0 | **FAIL** | Literal SSV uniform state is modulationally unstable; printed positive sound cone does not follow. |
| P1 | **FAIL** | Exact minimal relativistic logarithmic potential is unbounded below. |
| P2 | **PASS FORMALLY** | An exact Klein–Gordon envelope reduction yields the target plus \(\ddot\psi/(2m)\). |
| P3 | **FAIL** | Full covariant Goldstone has \(c_G^2=-B/(m-B)\); no stable positive-\(B\) region. |
| P4 S route | **FAIL** | One scalar Goldstone does not furnish two transverse photon helicities. |
| P4 H route | **CONTROL ONLY** | Independent Maxwell modes work only after withdrawing the old photon identity; they do not repair P0/P3. |
| P5 | **NOT REACHED** | Upstream stability gates stop the literal branch. |
| P6 | **COMPLETE** | Relevant theorem assumptions and consequences are recorded. |

## Required separate answers

| Question | Answer |
|---|---|
| Is the literal printed SSV scalar sector internally stable? | **No.** |
| Does it have a controlled covariant parent? | **Formal R0 map only; no stable R0/R1 parent preserving the target.** |
| Can its scalar mode supply transverse photons? | **No.** |
| Can an independent Maxwell sector coexist algebraically? | **Yes, but the combined literal-SSV vacuum remains unstable.** |
| Can Einstein gravity coexist algebraically? | **Yes, with the same qualification.** |
| Can anomaly-free chiral matter coexist algebraically? | **Yes; one Standard Model generation passes the audited anomaly sums.** |
| Is gravity, matter, or holography derived? | **No.** |
| Overall category for #180 | **K3.** |

## The neighboring theory that remains possible

A sign-reversed or otherwise stabilized logarithmic scalar can have a bounded
covariant parent. Einstein, Maxwell/Yang–Mills, and anomaly-free chiral fields
can then be independently supplied. That is a legitimate **adjacent K2
candidate**, but it is not a success of #180 because:

1. its logarithmic curvature is opposite to the frozen SSV equation;
2. its Goldstone is a scalar, not a transverse photon;
3. its finite-coupling Goldstone cone is subluminal and does not equal the
   metric light cone in the controlled nonrelativistic regime;
4. gravity and matter are inserted rather than holographically derived.

This nearby possibility is useful: the ambition of a holographic theory is not
shown impossible in general. What is ruled out is using the current printed
SSV as its stable low-energy condensate limit without a substantive revision.

## Consequence for the research programme

Do not proceed to microscopic screen construction under the assumption that
the present SSV scalar sector is already a healthy infrared endpoint.

A new programme can proceed only after explicitly choosing one of two changes:

- correct/replace the scalar theory and accept that it is not the old SSV; or
- abandon the homogeneous SSV vacuum as the expansion point and pre-register a
  different background whose stability and observables are derived from
  scratch.

Either choice deserves a new issue and a new name/version boundary. It must not
be described as a small holographic completion of an otherwise unchanged SSV.

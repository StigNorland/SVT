# Muon Stage 3 (revised): radial-window diagnostic for the thin-ring hypothesis

**Date:** 2026-05-30. Revises the broader Stage 3 prereg
(`papers/SSV-I/muon-stage3-prereg.md`) after reading the existing
leading-order derivation in `papers/SSV-I/notes/muon-helicity-bridge-derivation.md`
(now bannered as Path-B-superseded for its ladder claims, but the underlying
analytic factorisation of $\lambda_\perp = \pi/4$ remains a valid leading-order
result).

## The hypothesis under test

The prior derivation establishes $\lambda_\perp^{\rm code} = \pi/4$ as a
**thin-ring leading-order result**: it assumes $r \approx R_e$ in the volume
element, factorises the integral into core-radial $\times$ meridional-angular
$\times$ azimuthal, and isolates the $\frac{1}{4}\int_0^{2\pi}\cos^2\vartheta\,d\vartheta = \pi/4$
geometric factor. §8 of that note explicitly flags that "the full chiral-shear
second variation [verifying that it] leaves the $\pi/4$ leading coefficient
unchanged while adding only higher-order corrections" is open.

Hypothesis: the hw-drift measured in Stage 2 (lowest Kelvin Nambu eigenvalue
$\omega/\omega_c$: $0.172 \to 0.153 \to 0.137 \to 0.123 \to 0.111$ at
$hw = 4, 5, 6, 7, 8$) is the natural breakdown of the thin-ring approximation
as the integration domain extends to large $s/R_e$ where $r = R_e + s\cos\vartheta$
differs substantially from $R_e$. Under this hypothesis the operator code is
correct (CASE A in the Stage 3 prereg); the muon prediction is the thin-ring
value $\omega \approx 0.207$; and the drifted Kelvin eigenvalues at large hw
are finite-$\alpha$ corrections outside the thin-ring validity domain.

## The diagnostic

Use the existing `projection_window = "smooth"` mechanism with
`window_radius = r_w`: a smooth cosine taper that confines the meridional
integration to $s \leq r_w$ (with taper width 0.5 $\xi$). Sweep $r_w$ at
fixed large hw (8 $\xi$, large enough that hw is not the active cutoff):

  `r_w in {1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0}`

At each $r_w$, run the same selection-rule-fixed BdG operator
($\lambda_\perp = \pi/4$, helicity basis, $n=41$, $hw=8$), record the lowest
Kelvin Nambu eigenvalue and its eigenvector sector decomposition.

Also run a parallel sweep with the **hard window** (no taper, $s \leq r_w$
strict cutoff) to verify the result isn't a property of the cosine-taper
shape.

## Pre-registered decision rule

Let $\omega(r_w)$ be the lowest pure-Kelvin Nambu eigenfrequency at window
radius $r_w$. Three outcomes are possible:

**CONFIRM** the thin-ring hypothesis iff:
- $\omega(r_w)$ has a plateau near $0.207$ over some range
  $r_w \in [r_*, r_{**}]$ with $r_{**} - r_* \geq 1.0\,\xi$.
- On the plateau, $|\omega - 0.207| / 0.207 \leq 5\%$.
- $\omega(r_w)$ monotonically decreases for $r_w > r_{**}$, reaching the
  Stage 2 large-hw value $\sim 0.11$ as $r_w \to hw = 8$.

If CONFIRM holds: the operator is correctly implementing the full integral;
the prediction is the thin-ring value; the hw-drift is expected
finite-$\alpha$ correction. CASE A in the Stage 3 prereg. Major reframing
for SSV-I §The Muon: the muon prediction $\omega \approx 0.207$ from
$\lambda_\perp = \pi/4$ IS recovered as a thin-ring leading-order result,
with explicit finite-$\alpha$ corrections quantified by the drift curve.

**REJECT** the thin-ring hypothesis iff:
- $\omega(r_w)$ has no plateau in the range $[1.0, 6.0]\,\xi$.
- $\omega(r_w)$ is monotonic over the full range with no intermediate flat
  region near $0.207$.

If REJECT holds: the drift is not the thin-ring finite-$\alpha$ correction.
Cases B-D in the Stage 3 prereg remain open and the harder symbolic
derivation would be the next step.

**AMBIGUOUS** if neither CONFIRM nor REJECT cleanly applies (plateau exists
but is too narrow, or too far from $0.207$, or only present in one window
type). Report and propose follow-ups; do not pick a narrative.

## What this does NOT settle

- The sister mode at $\omega \approx 0.153$ (Stage 1 finding). Its
  hw-dependence in Stage 2 was equally bad; this diagnostic targets only
  the muon-window mode.
- Whether the thin-ring identification of the muon as the pure-Kelvin
  Nambu mode (with zero m=0 amplitude per Stage 1) is physically
  satisfactory. CASE A would require rewriting §The Muon to acknowledge
  that the muon mechanism is "pure Kelvin Nambu mode in the thin-ring
  limit" rather than "core-Kelvin hybrid via $\mathcal{L}_\perp$".
- Whether $\lambda_\perp = \pi/4$ is itself correctly derived (the prior
  derivation is leading-order; the next-order correction in $\alpha$
  would shift the predicted $\omega$).

## Output commitment

The full $\omega(r_w)$ curve and per-point eigenvector decompositions go
into the result note verbatim. The CONFIRM/REJECT/AMBIGUOUS verdict is
applied to the data without adjustment. If CONFIRM, the §The Muon rewrite
recovers a parameter-free thin-ring prediction. If REJECT, the Stage 2
null stands and the §The Muon rewrite proceeds with the "operator predicts
no muon" framing.

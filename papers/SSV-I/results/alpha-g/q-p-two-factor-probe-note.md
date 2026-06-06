# First Two-Factor `Q_p` Probe Note

This note records the first reduced two-factor probe for the gravity-branch monopole calibration.

Artifact:

- `papers/SSV-I/data/q-p-two-factor-probe-2026-05-06.json`

The probe compares simple candidates built from:

- shell deficit
- equivalent deficit radius
- compactness-style normalisations

The goal is only to ask a numerical question:

- can a simple second factor reduce branch-wise spread compared with shell deficit alone?

## Negative Result: Raw Products Do Not Help

The multiplicative families

- `shell_deficit * r_eq`
- `shell_deficit * r_eq^2`
- `shell_deficit * r_eq^3`

all perform worse than shell deficit alone, both on the coarse and fine branches.

That means the interior geometry cannot just be multiplied in naively as a power of the equivalent deficit radius.

## Positive Result: Additive Corrections Help

The first normalized additive forms do better.

Branch-wise relative spans:

### `n = 24`

- shell deficit: `0.860`
- additive compactness, coefficient `0.1`: `0.584`
- additive saturating correction, coefficient `0.1`: `0.542`

### `n = 48`

- shell deficit: `0.785`
- additive compactness, coefficient `0.1`: `0.645`
- additive saturating correction, coefficient `0.1`: `0.652`

So the additive family is the first reduced ansatz family that improves stability rather than making it worse.

## Current Best Reduced Candidate

The current best simple candidate is the saturating additive form

\[
\Pi_{Q}^{\rm probe}
  = \Pi_{\rm shell}
  + \varepsilon \,
    \frac{r_{\rm eq}}{r_{\rm eff} + r_{\rm eq}},
\]

with the present exploratory coefficient choice

\[
\varepsilon = 0.1.
\]

This should be treated strictly as a probe, not as a derived formula. The coefficient has not been tuned or justified physically.

## Current Read

The repo can now say something sharper than before:

- shell deficit alone is still the cleanest one-factor quantity
- a small additive compactness-style correction helps
- a saturating additive correction currently performs best among the tested reduced forms

That makes this the first reduced `Q_p` ansatz worth carrying forward for controlled follow-up tests.

## What Remains Open

Two cautions remain essential:

1. the `0.1` coefficient may simply be lucky
2. lower numerical spread does not by itself make the ansatz physical

So the next step is not to adopt this form as truth. It is to test whether the improvement survives modest coefficient scans and additional refined states.

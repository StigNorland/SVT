# Muon Stage 3 radial-window diagnostic: REJECT, with caveats

**Date:** 2026-05-30. Outcome of the pre-registered test in
`papers/SSV-I/muon-stage3-diagnostic-prereg.md`. Reproduction:
`python instruments/paper_i/muon_stage3_radial_window_probe.py` (~15 min total).

## One-line verdict

**REJECT.** The thin-ring hypothesis (that the Stage 2 hw-drift is a
finite-$\alpha$ correction outside the validity domain of the $\lambda_\perp
= \pi/4$ leading-order derivation) is rejected by the pre-registered rule.
The lowest Kelvin Nambu eigenfrequency exhibits no plateau near $0.207$
over any range of window radii; instead it varies smoothly and monotonically
across the full range from $r_w = 1.0$ (where $\omega = 0.190$) to
$r_w = 8.0$ (where $\omega = 0.113$).

## The data

Selection-rule-fixed operator, $\lambda_\perp = \pi/4$, $n = 41$, $hw = 8.0$,
helicity 2-core basis. Smooth-window sweep with taper width $0.5\,\xi$:

| $r_w / \xi$ | $\omega / \omega_c$ | dominant sector | $(u_{m=0}, u_{m=+1}, u_{m=-1})$ |
|-------------|---------------------|-----------------|---------------------------------|
| 1.0         | 0.1900              | m=$-1$          | (0.000, 0.592, 0.790)           |
| 1.5         | 0.1785              | m=$+1$          | (0.000, 0.978, 0.054)           |
| 2.0         | 0.1655              | m=$-1$          | (0.000, 0.047, 0.975)           |
| 2.5         | 0.1549              | m=$-1$          | (0.000, 0.265, 0.937)           |
| 3.0         | 0.1467              | m=$-1$          | (0.000, 0.683, 0.693)           |
| 3.5         | 0.1403              | m=$-1$          | (0.000, 0.015, 0.972)           |
| 4.0         | 0.1351              | m=$+1$          | (0.000, 0.962, 0.137)           |
| 5.0         | 0.1270              | m=$-1$          | (0.000, 0.308, 0.921)           |
| 6.0         | 0.1211              | m=$-1$          | (0.000, 0.154, 0.959)           |
| 8.0         | 0.1129              | m=$+1$          | (0.000, 0.741, 0.629)           |

## Against the pre-registered rule

The rule required:
- A plateau near $0.207$ over a range $[r_*, r_{**}]$ with width $\geq 1\,\xi$
- On the plateau, $|\omega - 0.207| / 0.207 \leq 5\%$
- Monotonic decrease past $r_{**}$ to the Stage 2 large-hw value $\sim 0.11$

The data show:
- No plateau anywhere. $\omega$ decreases monotonically from $0.190$ at
  $r_w = 1.0$ to $0.113$ at $r_w = 8.0$, with no flat region.
- No point within 5% of $0.207$. The closest is $r_w = 1.0$ at $0.190$,
  which is $8.2\%$ off and is at the smallest window tested (so it is the
  endpoint of a smooth monotone curve, not a plateau).

REJECT per the rule.

## Code-quirk caveat: hard window is actually no window

The probe also ran a hard-window sweep over the same $r_w$ grid. Every
$r_w$ produced the same eigenvalue $\omega = 0.1105$, identical to the
unwindowed $hw = 8$ baseline from Stage 2. Inspection of
`toroidal_projection_integrals.projection_window_weight` shows the
`"hard"` branch returns `1.0` unconditionally:

```python
if cfg.projection_window == "hard":
    return 1.0
```

It does not consult `window_radius`. So `projection_window = "hard"` is
equivalent to no window at all -- this looks like either an
incomplete implementation or a design choice where `"hard"` was meant to
mean "no taper, full domain". Either way, the hard-window column is not a
diagnostic; it is ten identical runs of the unwindowed baseline.

This means the test of "step-function cutoff at $r_w$" was NOT performed.
A hard cutoff might give different results from the smooth cosine taper
(e.g. by not deforming the integrand near $s = r_w$). Implementing a
genuine hard cutoff is outside the scope of this pre-registered probe and
is flagged here as a possible follow-up.

## Observations (not part of the verdict)

These do not change the REJECT verdict but are worth recording:

1. **Steep trend at small $r_w$.** Going from $r_w = 1.5$ to $r_w = 1.0$
   raises $\omega$ by $0.011$ ($+6\%$). Linearly extrapolating to $r_w \to
   0$ would put $\omega$ in the $0.20$-$0.22$ range. But the smooth-cosine
   taper width is $0.5\,\xi$, so windows below $r_w = 1$ are not cleanly
   testable with this taper -- the taper starts overlapping the core
   itself. A test at very small $r_w$ would need a different cutoff
   mechanism (genuine hard cutoff, or smaller taper width). The
   pre-registered prereg did not commit to testing $r_w < 1.0$, and adding
   points post-hoc would compromise the verdict; flagged as follow-up.

2. **Nambu doublet deformation.** The dominant-sector tag flips between
   m=$+1$ and m=$-1$ across the sweep, sometimes with the non-dominant
   sector carrying $50$-$80\%$ amplitude. This suggests the smooth window
   is deforming the (+1, $-1$) Nambu doublet itself, not just attenuating
   it. The eigenvalue trajectory is smooth, but the mode identity is
   changing. This makes "tracking the lowest Kelvin mode" a somewhat
   ambiguous operation across the sweep.

3. **Linear-looking $\omega(r_w)$.** $\omega$ vs $r_w$ is approximately
   linear in this range with slope $-0.011$/$\xi$. Not characteristic of
   either a thin-ring plateau ending at some scale or a power-law
   finite-$\alpha$ correction; more consistent with the window itself
   acting as a continuous parameter on the effective integration domain.

## What this leaves the Stage 3 prereg saying

Per the Stage 3 prereg's case structure:

- **CASE A (operator matches, drift = expected finite-$\alpha$):** ruled out
  by this REJECT. There is no thin-ring plateau and the operator's
  prediction does not return to $0.207$ when the integration is restricted
  to a small core region.
- **CASES B/C (missing surface or bulk terms with uniquely determined
  coefficients):** still open. The diagnostic doesn't rule them in or out,
  but it also doesn't supply candidate terms.
- **CASE D (operator under-determined):** still open.
- **CASE E (spurious term):** still open.

The next step under the Stage 3 prereg would be the harder symbolic
re-derivation of the second variation of $\mathcal{L}_\perp$ on the torus,
tracking surface terms explicitly. I have not committed to doing this and
am flagging that it is the kind of work where my error rate is meaningful
and a human physicist sanity-check would be wise.

## What Stage 2's verdict now does

Stage 2 already established that the operator does not predict a
basis-converged muon. Stage 3 ruled out the most charitable interpretation
of that result (thin-ring + expected finite-$\alpha$). The remaining
honest reading of the operator-level evidence is:

**The L+L_perp toroidal-breather BdG operator at $\lambda_\perp = \pi/4$,
selection-rule-correct, does not predict a basis-converged muon, and the
hw-drift that prevents convergence is not the thin-ring finite-$\alpha$
correction.** What it is, we do not yet know. Cases B/C/D/E from the
Stage 3 prereg are the remaining ways the operator could be corrected;
none has been ruled in.

The §The Muon rewrite can proceed with this as the operator-level
conclusion: the L+L_perp operator as currently understood does not
support the muon = 3/2 mu_0 identification, and the open question is
whether a different operator (3D phi-discretization, or a derived
correction term from a careful second variation) would change that.

## Files

- Pre-registration: `papers/SSV-I/muon-stage3-diagnostic-prereg.md` (commit at this stage)
- Probe: `instruments/paper_i/muon_stage3_radial_window_probe.py`
- Total compute: 938 s for the full smooth + hard sweep (20 spectrum solves)

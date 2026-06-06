# Topological vertex amplitude for the SSV $g-2$: can the numbers come out right?

Status: resolved into Paper II's contact-vertex section; kept as the
numerical/falsification note for issue #33.
Issue: #33 (depends conceptually on #29).
Date: 2026-05-28; updated 2026-06-03.
Companion script: `src/paper_ii/g2_form_factor_loop.py` (§6 output).
Regression tests: `src/paper_ii/test_g2_form_factor_loop.py`.
Prior result: `papers/SSV-II/g2-form-factor-results.md` (the $F = J_0(kR^\*)$
calculation killing 99.5 % of Schwinger).

## Closure note

#29 supplies the needed topology-language guardrail: an $R_1$ twist is a
filament/framing operation, not the Fourier transform of the assembled
electron torus.  Paper II therefore closes #33 by using the bare
LogSE$+\mathcal{L}_\perp$ contact vertex for the one-loop calculation.
That contact vertex has $F(k)=1$, recovers Schwinger's $\alpha/(2\pi)$
exactly at this order, and avoids inserting the dressed ring radius
$R^\*=\bar\lambda_e/\alpha$ into the loop vertex.  The classical
$J_0(kR^\*)$ calculation remains here as the falsifier showing why the
dressed form factor cannot be used at the bare vertex.

## Goal

Decide whether the user-preferred resolution of #33 — *borrow Schiller's
topology/algebra for the photon-vortex vertex, keep SSV's intrinsic scales
($\xi = \bar\lambda_e$, $R^\* = \bar\lambda_e/\alpha$, no $\ell_P$)* — can
reproduce the CODATA $a_e$ at the precision that QED achieves, **without**
invoking any sub-$\bar\lambda_e$ scale.

The test is purely numerical: assume a 1-loop vertex amplitude with shape
$F(k)$ and effective scale $R_v$ (whatever the imported algebra ends up
producing), feed it into the loop integral derived in
`g2-form-factor-results.md`, and read off the constraint on $(F, R_v)$.

## Reduction (recap)

Standard QED 1-loop vertex correction with the SSV vertex amplitude $F$
inserted, in the electron rest frame (where the spatial loop momentum is
unaffected by the Feynman-parameter shift):

$$a_e[F, R_v] = \frac{3\alpha}{\pi}\int_0^\infty d\kappa\; \kappa^2\; F^2(\kappa\tilde R_v)\; G(\kappa),$$

with $\kappa = k/m_e$, $\tilde R_v = R_v\, m_e$ (dimensionless), and the
Schwinger kernel

$$G(\kappa) = -\tfrac{1}{\sqrt{\kappa^2+1}} + \tfrac{\kappa^2}{3(\kappa^2+1)^{3/2}} + \tfrac{2}{3\kappa}.$$

$F^2(0)=1$, $\int_0^\infty \kappa^2 G \, d\kappa = 1/6$, so $F\equiv 1$
recovers Schwinger's $\alpha/(2\pi)$ exactly.

## Candidate vertex amplitudes

Five families, all normalised $F^2(0) = 1$, distinguished by their
high-$x$ behaviour ($x = kR_v$):

| Family | $F^2(x)$ | Leading correction $1-F^2 \approx$ | Physical motivation |
|---|---|---|---|
| Bessel | $J_0(x)^2$ | $x^2/2$ | Classical Fourier transform of circular current — **Paper II §3 as written** |
| Gaussian | $e^{-x^2}$ | $x^2$ | Smooth smearing of a localised source |
| Dipole | $(1+x^2)^{-2}$ | $2x^2$ | Hadron-style empirical form factor |
| Lorentzian | $(1+x^2)^{-1}$ | $x^2$ | Yukawa / single-pole vertex |
| Constant | $1$ | $0$ | Topological / point-like vertex — *no geometric smearing* |

The first four all share the universal small-$x$ behaviour
$F^2 = 1 - c\, x^2 + O(x^4)$ with $c = O(1)$, giving
$\delta a_e / a_e^{\rm Schw} \approx -c\,\tilde R_v^2 \cdot \langle\kappa^2\rangle_{\rm loop}/2$,
i.e. *any* geometric smearing of an object at scale $R_v$ produces an
$\tilde R_v^2$ suppression at leading order. Only **Constant** evades this.

## Numerical result

Maximum dimensionless vertex scale $\tilde R_v$ allowed by three precision
tolerances on $|\delta a_e|/a_e^{\rm Schw}$:

| Family | $\le 10^{-3}$ (Schwinger 0.1%) | $\le 5\!\times\!10^{-6}$ (2-loop QED scale) | $\le 10^{-10}$ (CODATA) |
|---|---|---|---|
| Bessel ($J_0^2$) | $1.77\!\times\!10^{-2}$ | $9.65\!\times\!10^{-4}$ | below numerical floor* |
| Gaussian | $1.26\!\times\!10^{-2}$ | $6.85\!\times\!10^{-4}$ | below numerical floor* |
| Dipole | $9.06\!\times\!10^{-3}$ | $4.89\!\times\!10^{-4}$ | below numerical floor* |
| Lorentzian | $1.30\!\times\!10^{-2}$ | $6.96\!\times\!10^{-4}$ | below numerical floor* |
| Constant | $\infty$ | $\infty$ | $\infty$ |

*The CODATA column is at our integration noise floor ($\sim10^{-10}$
relative). Analytically the boundary scales as
$\tilde R_v \sim \sqrt{2 \cdot \text{target}/c}$, so for $c\sim 1$ and
target $10^{-10}$, $\tilde R_v \lesssim 1.4 \times 10^{-5}$.

## Comparison to SSV-intrinsic scales

Dimensionless $\tilde R_v = R_v \cdot m_e$ for each candidate physical
scale already in the SSV corpus:

| Scale | $\tilde R_v$ | Status |
|---|---|---|
| $R^\* = \bar\lambda_e/\alpha$ (Paper I ring radius) | $137$ | **ruled out** by ~$10^5\!\times$ |
| $\xi = \bar\lambda_e$ (vortex tube / coherence length) | $1$ | **ruled out** — suppresses Schwinger by 40% |
| $\xi/\alpha^{1/2} = \bar\lambda_e/\sqrt\alpha$ | $\approx 11.7$ | **ruled out** |
| $\bar\lambda_e \cdot \alpha$ (hypothetical sub-$\xi$) | $7.3\!\times\!10^{-3}$ | borderline: passes 0.1% but **fails** 2-loop tolerance |
| $\bar\lambda_e \cdot \alpha^2$ (hypothetical) | $5.3\!\times\!10^{-5}$ | passes 2-loop, borderline at CODATA |
| $\bar\lambda_e \cdot \alpha^{5/2}$ or smaller | $\le 4.5\!\times\!10^{-6}$ | passes CODATA |

## Reading

**The data forces a clean dichotomy** for resolving #33 under the
"keep SSV scales" constraint:

> Either (a) the imported algebra delivers an effectively **constant**
> photon-vortex vertex amplitude — no geometric smearing despite the
> defect being an extended object — *or* (b) the vertex form factor has
> finite shape but its characteristic scale is **at least four orders of
> magnitude below $\bar\lambda_e$**, which is unaccounted for by any
> named SSV scale ($R^\*$, $\xi$, or simple $\alpha$-combinations
> thereof).

Both options are coherent in principle:

- **(a) Truly topological vertex.** Reidemeister-twist amplitudes count
  homotopy-class changes; they have no Fourier-transform sum rule tying
  them to a classical extent. This is precisely the algebraic structure
  #29 proposes to import. *If* the import preserves this property when
  ported to SSV $\Psi$-defects — i.e., if the SSV twist-attachment
  amplitude really is $k$-independent — then Schwinger is recovered
  exactly at 1-loop and the program is consistent.

- **(b) New small SSV scale.** Powers $\alpha^{5/2}\bar\lambda_e$ or
  smaller would do it numerically, but there is currently no derivation
  of such a scale in Paper I. A natural candidate worth checking: the
  BdG-mode resolution of the vortex line, i.e. the spatial extent of the
  vortex *quanta* (not the classical core), which in some BdG settings
  is parametrically smaller than $\xi$.

The strict version of the user's preference (algebra only, no new
scales) selects **(a)**.

## What the algebra import must explicitly deliver

To close #33 in the spirit of "borrow algebra, keep scales," #29's
output must include:

1. **The photon–vortex vertex amplitude** $\mathcal{A}(k)$ for an
   electron-class torus $\Psi$-defect, derived from the R1
   (twist-attachment) Reidemeister move acting on SSV defects, computed
   in the LogSE $+\,\mathcal{L}_\perp$ framework.

2. A **demonstration** that $\mathcal{A}(k)$ is independent of
   $R^\*$ (and of any other classical-extent scale of the defect) over
   the range $k \in [0, \text{few}\times m_e]$ — i.e. that the resulting
   $F^2$ falls in the **Constant** row of the table above to the
   precision required by the experimental tolerance.

3. The **leading correction** to $\mathcal{A}(k)$ from internal
   vortex-mode structure (BdG resolution / chiral-shear modes) and an
   estimate of the scale at which it activates. This is what would
   eventually appear in $\delta a_e$ at the level QED already predicts
   from $\alpha^2/\pi^2$ corrections.

Item (2) is the load-bearing claim. Failing it falls back to the
geometric form factor result (99.5% suppression), which is fatal.

## Falsifier

Whatever the imported algebra produces for $\mathcal{A}(k)$, plug it
into the same script: if the resulting $a_e[F]$ disagrees with CODATA
at fractional precision better than $10^{-10}$, the topological-vertex
resolution of #33 is falsified and one of the other resolutions
(separate vertex radius, compensating diagrams, sub-leading insertion)
must be pursued instead.

## §3 gapbox resolution

The §3 text has now been rewritten in this direction:

1. The classical-Fourier-transform reading $F = J_0(kR^\*)$ is now
   computed and ruled out at ~$10^9\sigma$ against CODATA.
2. The geometric-form-factor *family* (any $F^2 = 1 - c\,(kR^\*)^2 +
   \cdots$) is also ruled out for *any* scale $R_v \gtrsim 10^{-4}
   \bar\lambda_e$, with no presently-derived SSV scale in the allowed
   window.
3. Consistency with the observed $a_e$ therefore requires the
   photon-vortex vertex to be **topological in character** — independent
   of the defect's classical extent — for which the Reidemeister-move
   apparatus #29 is importing is the candidate algebra.
4. Pending that import, the numerical coefficient of $\delta a_e$ is
   not the open question; the *functional form* of the vertex amplitude
   is.

This rewrites the gapbox from "open numerical coefficient" to "open
algebraic structure, with explicit falsification target."

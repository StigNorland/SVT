# zloshchastiev2023_pramana_rotcurves — corroborating evidence for C11

**K. G. Zloshchastiev**, *Galaxy rotation curves in superfluid vacuum theory*,
Pramana **97**, 2 (2023), doi:10.1007/s12043-022-02480-2, arXiv:2310.06861.

## ⚠ This is NOT the work SSV-I cites

SSV-I's `\bibitem{zloshchastiev2023}` is:

> K. G. Zloshchastiev, "Derivation of emergent spacetime metric, gravitational
> potential and speed of light in superfluid vacuum theory," *Universe* **9**,
> 234 (2023).

Confirmed via Crossref to be a **real paper** — SSV-I's bibliography entry is
accurate. The present file is a *different* Zloshchastiev 2023 paper (different
title, journal, volume, page) supplied during the audit. It is filed under its
own key so it can never be mistaken for the cited work; `zloshchastiev2023`
remains `PENDING-PRIMARY`.

Provenance: supplied by the owner, then independently re-fetched from
arXiv:2310.06861 — **byte-identical**, sha256 `34cb087f9019363d`.

## Why it is relevant anyway

This paper states (§2) that it *"closely follow[s] the lines of the work [6]"*
(Zloshchastiev, *Universe* **6**, 180 (2020)) in deriving the effective
gravitational potential — the same machinery the cited *Universe* 9, 234 paper
is titled after. It is therefore strong, though not conclusive, evidence about
what mechanism Zloshchastiev's SVT gravity actually uses.

## C11 probe 1 — is there a Bjerknes force?

SSV-I `main.tex:1245` attributes to this author *"the acoustic Bjerknes force —
mutual attraction between vibrating breathers via secondary flow fields in the
plenum."*

Full-text counts (4,663 words):

| probe | hits |
|---|---|
| `Bjerknes` | **0** |
| `mutual attraction` | **0** |
| `secondary flow` | **0** |
| `breather` | **0** |
| `vibrating` | **0** |

**The actual mechanism is entirely different.** Gravity is an *effective
potential read off the logarithmic term itself*, evaluated on the vacuum
wavefunction — eq. (3):

$$\Phi = -\frac1m V_{\rm eff}(r,t) = \frac1m\left(b_0-\frac{q}{r^2}\right)\ln\frac{|\Psi_{\rm vac}(r,t)|^2}{\bar\rho}$$

Expanded on the trial wavefunction (5), this yields eq. (6): a *multiple-scale*
potential with sub-Newtonian, Reissner–Nordström-like, Newtonian, logarithmic,
linear (Rindler) and quadratic (de Sitter) terms. No acoustic radiation force
anywhere.

## C11 probe 2 — is $G$ expressed via $\hbar,c,m_e,\alpha$?

| probe | hits |
|---|---|
| `fine-structure` / `fine structure` | **0** |
| `electron mass` | **0** |

$G$ is an **input**, not a derived quantity:

- line 199: *"$G$ is the Newton's gravitational constant"*
- §3, line 311: *"From this section onwards, we will work in **units $G = 1$**."*
- eq. (9): $\Phi_{\rm N}(r) = -\dfrac{a_1q}{m}\dfrac1r = -\dfrac{GM}{r}$ —
  i.e. $GM$ is **identified** with the fitted combination $a_1q/m$, not derived
  from anything.

## Bearing on C11

Both halves of SSV-I's attributed claim are contradicted by the mechanism this
author actually uses in a closely-related paper of the same year. The verdict on
`zloshchastiev2023` stays **`PENDING-PRIMARY`** — the audit does not verdict a
source it has not read — but the burden has shifted decisively, and
`MISATTRIBUTED` is now the expected outcome.

---

## Incidental finding — how the D1 error was invited

p.2, verbatim:

> In this picture, massless excitations, such as photons, are somewhat analogous
> to acoustic waves propagating with velocity $c_s \propto \sqrt{p'(\rho)}$,
> **where fluid pressure is determined via the equation of state
> $p = p(\rho)$**…

The sound speed is given as $\sqrt{p'(\rho)}$ — a *pressure* derivative — while
$p(\rho)$ **is never written down anywhere in the paper**, and the logarithmic
function $F(\rho)=b\ln(\rho/\bar\rho)$ sits a few lines away in eq. (1).

This is precisely the trap SSV-I fell into: it read $F(\rho)$ as the missing
$p(\rho)$. Since $c_s^2 = \rho\mu'(\rho)/m$ for a chemical potential but
$p'(\rho)/m$ for a pressure, that substitution produces the whole D1 error chain
— wrong sign, spurious factor 2, and a fabricated thermodynamic/Bogoliubov
discrepancy.

This **explains** the error without excusing it: the source juxtaposes
"$c_s$ from $p'(\rho)$" with "$F(\rho)=b\ln(\rho/\bar\rho)$" and never supplies
the equation of state that would distinguish them.

## Incidental finding — length scale, third confirmation

p.2: the length scale of the logarithmic nonlinearity may be taken as *"the
classical length $(m/\bar\rho)^{1/3}$ or the **quantum temperature length
$\hbar/\sqrt{mb_0}$**."*

Consistent with $a=\hbar/\sqrt{2m|b|}$ from `zloshchastiev2020` up to the
$\sqrt2$ convention, and with SSV-I's $\xi=\hbar/\sqrt{2m_0b\rho_0}$.

## Incidental finding — the sign, third independent confirmation

eq. (1):

$$i\hbar\partial_t\Psi = \left[-\frac{\hbar^2}{2m}\nabla^2 + V_{\rm ext}(r,t) - \left(b_0-\frac{q}{r^2}\right)\ln\frac{|\Psi|^2}{\bar\rho}\right]\Psi$$

The **minus** before the logarithmic term again matches SSV-I. Note $b_0>0$ in
the fits (Table I gives $b_0/m$ from $21.4^2$ to $326^2\ \mathrm{km^2s^{-2}}$).
This does **not** rescue D1: here the logarithm acts on a strongly
*inhomogeneous* vacuum profile to generate a galactic potential, which is a
different regime from SSV-I's claim of a *stable uniform* background carrying
sound at $c$. The stability question D1 raises is simply not addressed here.

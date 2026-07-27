# SSV-II — E-gate report

Gate: **E-GATE FAIL (one defect, already known to the paper)** · #184

## E1 — `eq:maxwell` contradicts the paper's own #138 computation

`main.tex:508` states the vacuum Maxwell equations as a derived result. The
paper's own record, two paragraphs below, says the #138 linearization found the
transverse wave equation does **not** arise from the LogSE + chiral-shear + CP¹
functional around the uniform vacuum, and that **the chiral term is silent at
linear order**.

Independently, #180 P4 (S route) established that one scalar Goldstone cannot
furnish two transverse photon helicities. Three independent routes agree.

**Verdict `MISDERIVED`.** `eq:maxwell` must carry the #138 status at the point of
statement or move into the historical-record subsection. Citations to `Barcelo`
(and `Volovik` for a one-component Madelung system) withdraw with it.

## E2 — inherited from D1

`main.tex:303` uses $\xi=\hbar/(m_0c)$; under the adopted branch this becomes
$\hbar/(\sqrt2 m_0c)$. Textual only — SSV-II's numerics are in $\xi$-units
(see the series N-gate report).

---

## E3 — the Aharonov–Bohm sector (added 2026-07-27, after C4 resolved)

The C-gate held this section closed because it rested on `HaldaneWu1985`, which
was paywalled. That is now settled (`MISREAD`, C-gate D3), so §"The
Aharonov–Bohm Effect as Mechanical Berry Phase" (`main.tex:782–869`) has been
audited. It fails on three independent grounds. Each is a unit identity or a
structural fact, so **none depends on the D1 branch decision**.

All four checks are machine-checked in
`instruments/paper_ii/ssv_ii_ab_audit_2026.py`
(`instruments/test/paper_ii/test_ssv_ii_ab_audit_2026.py`, 11 tests).

### E3a — Haldane–Wu cannot supply an AB phase, at any prefactor

$\gamma_C = 2\pi N_C$ scales with enclosed **area × density**. Enclose the same
defect with a larger loop and the phase grows without bound; an AB phase is
invariant. So the mismatch is not a wrong constant that could be absorbed into a
coupling — it is the wrong *kind* of quantity. Detail in the C-gate report, D3.

### E3b — `main.tex:838` is dimensionally inconsistent as printed

$$\gamma_{\rm Berry}=\frac{e}{\hbar}\oint_C\mathbf v_\perp\cdot d\mathbf l=\frac{e}{\hbar}n\kappa_0$$

With $\kappa_0 = h/m_0$ this is dimensionless **only if $e$ has the dimensions of
mass** — $e = \hbar/\kappa_0 = m_0$. Read as the elementary charge, which is how
it is used four equations earlier ($\Phi_0 = h/e$, "the (electron) flux
quantum"), $\gamma_{\rm Berry}$ carries dimensions $\mathsf{Q\,T\,M^{-1}}$.

This is **not** a natural-units artefact. With $\hbar=c=1$ the charge is
dimensionless ($e=\sqrt{4\pi\alpha}$) while $\kappa_0$ has dimension
$\mathsf{mass}^{-1}$, so the expression still fails. The symbol $e$ is doing
duty as a charge and as a mass in the same paragraph.

### E3c — step $(\star)$ is circular

`main.tex:853` calls $e/m_0=1$ "the load-bearing one" and argues it is forced by
the medium having a single mass scale, hence

> not a numerical coincidence but a consequence of the medium having a single
> mass scale.

But by E3b, eq. (838) is well formed **only** when $e$ already carries mass
dimension; with $m_0$ the sole mass in the medium, $e = m_0$ and $e/m_0 = 1$ is
an identity of the notation. The conclusion is assumed by the step that sets up
the equation. $\gamma_{\rm AB}=2\pi n$ is not derived here.

### E3d — `eq:flux_quantisation` is dimensionally inconsistent

$$\Phi_B=\oint_C\mathbf A\cdot d\mathbf l=\frac{c_\perp\alpha\rho_0}{e}n\kappa_0=n\frac{h}{e}$$

requires $c\,\rho_\perp\kappa_0 = h$. With $\rho_\perp=\alpha\rho_0$ a **mass
density** ($\mathsf{M\,L^{-3}}$ — confirmed by SSV-I's corrected E5 value
$\rho_0=\alpha m_e^4c^3/2\pi^2\Lambda\hbar^3$), the left side has dimensions
$\mathsf{M\,T^{-3}}$ against $\mathsf{M\,L^{2}T^{-2}}$ on the right: a mismatch
of $\mathsf{L^{-2}T^{-1}}$, which a dimensionless $\alpha$ cannot absorb.
$\rho_\perp$ would have to be $\mathsf{M\,T\,L^{-1}} = m_0/c$, which is not a
density of any kind.

So the claim at `main.tex:826` —

> Flux quantisation is not imposed — it follows from the quantisation of
> transverse vorticity

— is not established by the printed algebra.

### What survives, and the repair route

The **qualitative** thesis is supported, and by a source SSV-II already cites.
Volovik 2001 §XII A, eq. (311), maps phonon propagation around a vortex onto the
AB problem "with the vector potential $\mathbf A=\mathbf v_s$" — SSV-II's
`eq:EB_identification` in Volovik's own words, and experimentally confirmed in
³He-B via the Iordanskii force (his Fig. 17). "The vector potential is a physical
flow field, not a gauge artefact" stands.

The **quantitative** claim does not, and Volovik does not rescue it: the same
sentence replaces the electric charge by the quasiparticle's $E/c^2$, so the
analogue AB phase is **energy-dependent** — which is why the observable is a
cross-section periodic in energy (his eq. 312), not a universal phase. There is
therefore no route in the retrieved literature to $\gamma_{\rm AB}=2\pi n$ as a
consequence of the medium, on either reading of what the electron ring is
(topological defect → Haldane–Wu; quasiparticle → Volovik).

**Verdict `MISDERIVED`.** `eq:AB_SSV` and `eq:flux_quantisation` must be
withdrawn or rebuilt; the `HaldaneWu1985` citation withdrawn; the surviving
qualitative claim re-cited to Volovik §XII A. Under standing rule 1 the negative
must be stated in the paper, not merely softened.

## Gate decision (amended 2026-07-27)

**E-GATE FAIL** — two defects: E1 (`eq:maxwell`, `MISDERIVED`) and E3 (the AB
sector, `MISDERIVED`), plus E2 inherited from D1. Both E1 and E3 are cases of the
same failure: a structural claim about emergent electromagnetism asserted beyond
what the medium supplies. They should be repaired together.

# SSV-I E-gate — Lamb / fat-torus sector

Status: **closure-grade** for E1/E2/E3, **flagged** for E4

Verified symbolically and numerically 2026-07-27 (mpmath, 30 dps).
Source equation supplied by the owner from a clean copy of Lamb 1932 p.241
(the archive.org OCR destroys mathematics — see `papers/cited/notes/lamb1932.md`).

## Owner-supplied primary evidence, Lamb 1932 §163, p.241

$$\psi = -\frac{\omega}{2\pi}\,\varpi_0 \iint\left(\log\frac{8\varpi_0}{r_1} - 2\right)dx'\,d\varpi'$$

This resolves the OCR fragment `V' = - ^ «o //(log - 2 ) d®'`. Note the
constant **−2**.

## E1 — `C = 1/8` is wrong; impact negligible

SSV-I App.\ref{app:biot} states the next-order term of the elliptic expansion is
\(\Delta E=\rho_0\kappa_0^2\xi^2/(8R)\), "a pure geometric constant from the
elliptic expansion".

Expanding the paper's own formula
\(\left[(2/\varepsilon-\varepsilon)K(\varepsilon)-(2/\varepsilon)E(\varepsilon)\right]\),
\(\varepsilon^2=1-a^2/4R^2\):

| \(a/R\) | residual after \(\ln(8R/a)-2\) | residual\(/[(a/R)^2(\ln(8R/a)-1)]\) |
|---|---|---|
| \(10^{-1}\) | 6.351e-3 | 0.187801 |
| \(10^{-3}\) | 1.498e-6 | 0.1875000313 |
| \(10^{-5}\) | 2.361e-10 | 0.1875000000 |

Converges to exactly **3/16**. The true next-order term is

$$E_{\rm self}=\tfrac12\rho_0\kappa_0^2R\left[\ln\frac{8R}{a}-2+\frac{3}{16}\Big(\frac aR\Big)^2\left(\ln\frac{8R}{a}-1\right)+O\big((a/R)^4\big)\right]$$

Two faults: the coefficient is not 1/8, and the term **carries a logarithm**, so
it is *not* a pure geometric constant. Separately, the paper derives \(\Delta E\)
from "the interaction of diametrically opposite ring segments" — a different
argument — and then attributes it to the elliptic expansion. Two derivations
conflated.

**Impact: negligible.** \(C\) enters the stationarity condition only through
\(2C/r^{*2}\sim C\alpha^2\):

| \(C\) | \(r^*\) | rel. deviation from \(1/\alpha\) |
|---|---|---|
| 0 | 137.035999177 | 3e-31 |
| 1/8 (printed) | 137.037823 | 1.33e-5 |
| \(\tfrac3{32}(\ln(8/\alpha)-1)\) (true) | 137.044208 | 5.99e-5 |
| 1 | 137.050592 | 1.07e-4 |

\(R^*_e=\xi/\alpha\) is robust. **Correct the appendix; the result stands.**

## E2 — RESOLVED: `eq:Ekin` is correct, the appendix is the fault

Closed 2026-07-27 against Lamb Arts. 162–163, pp.239–241, read from
owner-supplied page images and transcribed verbatim in
`papers/cited/notes/lamb1932.verbatim.md`.

**Lamb's core model is stated explicitly** (p.241): *"For the case of a
circular section more definite results can be obtained as follows. **If we
neglect the variations of \(\varpi\) and \(\omega\) over the section**…"* —
\(\omega\) is the vorticity, so this is a **uniform-vorticity circular core of
radius \(a\)**.

**Lamb Art. 163 (6):**

$$\frac{T}{2\pi\rho}=\frac{\kappa^2\varpi_0}{4\pi}\left\{\log\frac{8\varpi_0}{a}-\frac74\right\}
\qquad\Longrightarrow\qquad
T=\tfrac12\rho\kappa^2\varpi_0\left\{\log\frac{8\varpi_0}{a}-\frac74\right\}$$

This is **exactly** SSV-I `eq:Ekin`. And Art. 163 (7) gives the *velocity* with
\(-\tfrac14\) — a different constant for a different quantity.

### Verdict, opposite to the working hypothesis

| Item | Status |
|---|---|
| `eq:Ekin` (\(-7/4\)) | **CORRECT**, and §163 is the **correct** citation |
| Appendix `app:biot` claim that its elliptic formula "recovers \eqref{eq:Ekin} at leading order" | **FALSE** |
| \(\rho_0\) 5 % shift | **VOID** — does not occur |

The appendix's Neumann self-inductance form
\(\left[(2/\varepsilon-\varepsilon)K(\varepsilon)-(2/\varepsilon)E(\varepsilon)\right]\)
is a **filament / hollow-core** model whose leading term is \(\ln(8R/a)-2\)
(verified to 10 digits under E1). Different core model, different constant. It
cannot recover a uniform-vorticity result and does not.

The \(-2\) that appears in Lamb's \(\psi\) is an intermediate: by eq. (5) it has
already become \(-\tfrac32\), and only after the final integration does the
energy constant \(-\tfrac74\) emerge. It is not an energy constant and must not
be read as one.

**Action:** repair the appendix — either replace the self-inductance form with a
uniform-vorticity derivation, or keep it and state plainly that it is a
different core model that does *not* reproduce `eq:Ekin`. The main line is
untouched.

## E3 — spurious \(\alpha^2\) in `eq:Etotal` / `eq:stationary`

`eq:gammadef` defines \(2\pi\gamma\alpha^2=\Lambda+1=\ln(8/\alpha)-\tfrac34\approx6.25\).
`eq:Etotal` then writes the chiral term as \(-(\Lambda+1)\,\alpha^2\,r\),
applying \(\alpha^2\) **twice**.

As printed, the stationary point is

| functional | \(r^*\) |
|---|---|
| `eq:Etotal` exactly as printed | **0.5706** |
| with the spurious \(\alpha^2\) removed | **137.0378** (\(1/\alpha=137.0360\)) |

The printed equations do **not** produce the boxed result. Line 487 then asserts
\((\Lambda+1)\alpha^2=\ln(8/\alpha)-\tfrac34\), which contradicts `eq:gammadef`
— and it is that step which silently restores the correct value.

**Verdict: `MISDERIVED`, presentation-fatal, physics intact.** The result is
right to 1.3e-5; three printed equations are wrong. Remove the \(\alpha^2\) from
`eq:Etotal` and `eq:stationary`, and delete the inconsistent identity at 487.

## E4 — "classical electron radius" — FLAGGED

Line 495 calls \(R^*_e=\xi/\alpha=\hbar/(\alpha m_0c)\) "the classical electron
radius". With \(\xi=\hbar/(m_0c)=\bar\lambda_C\), \(\xi/\alpha\) is
\(\alpha^{-1}\) **above** the Compton scale — that is the **Bohr radius**
\(a_0=5.29\times10^{-11}\,\mathrm m\). The classical electron radius is
\(r_e=\alpha\bar\lambda_C=2.82\times10^{-15}\,\mathrm m\), \(\alpha\) **below**
it. The two differ by \(\alpha^2\approx5.3\times10^{-5}\).

Either the label is wrong or \(m_0\neq m_e\) in a way the text does not state.
**Not asserted as a fault** pending the owner's reading of the intended
\(m_0\); flagged as the highest-value item to check next.

## Carried forward

- E1: correct the appendix; \(\alpha\) result unaffected.
- E2: **resolved** — `eq:Ekin` correct and correctly cited; the appendix is the fault; \(\rho_0\) does not move.
- E3: three equations to fix; boxed results stand.
- E4: resolve the Bohr/classical-radius labelling.
- All of the above are **independent of D1**; the \(\sqrt2\) correction to
  \(\xi\) rescales \(R^*_e\) but not the \(R^*_e=\xi/\alpha\) relation.

# SSV-I E-gate — Lamb / fat-torus sector

Status: **closure-grade** for E1/E3, **blocked** for E2, **flagged** for E4

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

## E2 — \(-7/4\) vs \(-2\): internal inconsistency — BLOCKED on C10

`eq:Ekin` uses \(\ln(8R/a)-\tfrac74\). The appendix claims its elliptic formula
"recovers \eqref{eq:Ekin} at leading order" with \(K\approx\ln(8R/a)\),
\(E\approx1\) — which gives \(\ln(8R/a)-\mathbf{2}\), verified above. **The
appendix's own claim is false.**

The two constants are different core models: \(-7/4\) for a core of uniform
vorticity, \(-2\) for a hollow/thin filament. The owner-supplied \(\psi\) shows
\(-2\), but that is the *stream function*, not the energy.

**Impact:** \(R^*_e=\xi/\alpha\) is unaffected (\(\Lambda\) is defined from the
same constant, so it cancels in \(d\mathcal E/dr\)). But
\(m_ec^2=\tfrac12\rho_0\kappa_0^2(\xi/\alpha)\Lambda\) gives
\(\rho_0\propto1/\Lambda\), and \(\Lambda=5.24969\) vs \(4.99969\) is a
**5.0 % shift in the vacuum density \(\rho_0\)**.

**Blocked:** needs Lamb's *energy* expression (§162) and its stated core
assumption. Requested from the owner.

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
- E2: blocked on C10 (Lamb §162 energy + core model). \(\rho_0\) moves 5 %.
- E3: three equations to fix; boxed results stand.
- E4: resolve the Bohr/classical-radius labelling.
- All of the above are **independent of D1**; the \(\sqrt2\) correction to
  \(\xi\) rescales \(R^*_e\) but not the \(R^*_e=\xi/\alpha\) relation.

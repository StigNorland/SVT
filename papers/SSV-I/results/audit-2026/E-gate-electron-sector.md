# SSV-I E-gate — electron / vacuum-density sector

Status: **closure-grade negative result** (E4 and E5)

Verified 2026-07-27 with mpmath at 25 dps, CODATA-2018 constants. Both findings
are **internal** to SSV-I — no external source is involved, so neither depends
on any `PENDING-PRIMARY` key.

## Notation, from the paper itself

`main.tex:390–392` defines $m_0$ as a *"defect-relative reference mass"* and
states: **"for the electron (simple ring) $m_0 = m_e$."** Also
`main.tex:384`: $\kappa_0 = h/m_0$ (Planck's $h$, not $\hbar$), and
`main.tex:297`: $\xi = \hbar/(m_0c)$.

So for the electron sector $\xi = \hbar/(m_ec) = \bar\lambda_C$, the reduced
Compton wavelength.

---

## E4 — `main.tex:495` misidentifies the boxed result

`eq:Re-star` gives $R^*_e = \xi/\alpha = \hbar/(\alpha m_0c)$, and line 495
states: *"This is the classical electron radius, derived without empirical input
for $R_e$."*

| quantity | value |
|---|---|
| $\bar\lambda_C = \hbar/(m_ec)$ | $3.86159\times10^{-13}$ m |
| $\xi/\alpha = \bar\lambda_C/\alpha$ | $5.29177\times10^{-11}$ m |
| **Bohr radius** $a_0$ | $5.29177\times10^{-11}$ m |
| classical electron radius $r_e=\alpha\bar\lambda_C$ | $2.81794\times10^{-15}$ m |

$$\frac{\xi/\alpha}{a_0} = 1.0000000\qquad
  \frac{\xi/\alpha}{r_e} = 18778.865 = \frac1{\alpha^2}$$

**$\xi/\alpha$ is exactly the Bohr radius.** It sits $\alpha^{-1}$ *above* the
Compton scale; the classical electron radius sits $\alpha$ *below* it. The two
differ by $\alpha^2\approx5.3\times10^{-5}$.

**Verdict: `MISDERIVED` (identification).** The *derivation* of
$R^*_e=\xi/\alpha$ is unaffected — see E3 for its separate defect — but the
*identification* is wrong, and it is not cosmetic: the paper advertises the
recovery of a known constant and recovers a different known constant. An
electron whose equilibrium ring radius is the **Bohr radius** is a materially
different physical claim from one at the classical electron radius, and any
interpretation resting on the latter must be withdrawn.

---

## E5 — `eq:rho0-value` does not follow from `eq:electron-mass` (new)

`eq:electron-mass`:
$$m_ec^2 = \tfrac12\rho_0\kappa_0^2\,\frac{\xi}{\alpha}\,\Lambda$$

Inverting, with $\kappa_0^2\xi = 4\pi^2\hbar^3/(m_e^3c)$:

$$\rho_0 = \frac{2m_ec^2\alpha}{\kappa_0^2\,\xi\,\Lambda}
        = \boxed{\frac{\alpha}{2\pi^2\Lambda}\cdot\frac{m_e^4c^3}{\hbar^3}}
        = 7.0421\times10^{-5}\,\frac{m_e^4c^3}{\hbar^3}$$

`eq:rho0-value` prints instead

$$\rho_0 = \frac{2\alpha\Lambda\,m_e^4c^3}{\pi^2\hbar^3} = 7.76299\times10^{-3}\,\frac{m_e^4c^3}{\hbar^3},
\qquad\text{and asserts}\qquad \rho_0\approx1.9\,\frac{m_e^4c^3}{\hbar^3}$$

### Three mutually inconsistent statements

| comparison | factor |
|---|---|
| printed formula ÷ correct inversion | **110.24** $= 4\Lambda^2$ |
| printed "$\approx1.9$" ÷ printed formula | **244.75** |
| printed "$\approx1.9$" ÷ correct inversion | **26 981** |

The printed symbolic formula carries $\Lambda$ in the **numerator** where
$1/\Lambda$ belongs, and a factor 4 where $1/4$ belongs — the signature of an
inversion performed by multiplying rather than dividing. The printed *numerical*
value then matches **neither** its own symbolic formula nor the correct
inversion.

Physically: the correct inversion gives $\rho_0\approx1.1\times10^3$ kg m⁻³,
while the printed $\approx1.9$ gives $\approx3\times10^7$ kg m⁻³.

**Verdict: `MISDERIVED`.** $\rho_0$ is the vacuum saturation density — a
headline quantity of the whole programme — and it is stated three ways that
disagree by up to four orders of magnitude.

### Controls

- $\kappa_0=h/m_0$ confirmed at `main.tex:384` and `main.tex:1770` ($h$, not
  $\hbar$), so no $2\pi$ ambiguity.
- Dimensions check: $[\rho_0\kappa_0^2R]$ = energy requires $\rho_0$ to be a
  **mass** density, and $m_e^4c^3/\hbar^3$ is indeed kg m⁻³. A number-density
  reading is excluded.
- Independent of D1: the $\sqrt2$ correction to $\xi$ moves $\rho_0$ by $\sqrt2$,
  not by $110$ or $2.7\times10^4$.

---

## Consequences

$\rho_0$ propagates into every absolute-scale claim in the series. Until E5 is
resolved, **every downstream number derived from $\rho_0$ is suspect** and the
N-gate for those results must not open.

Neither E4 nor E5 touches the *relation* $R^*_e=\xi/\alpha$, which stands on its
own (subject to E3's spurious $\alpha^2$). What fails is the identification of
that length, and the inversion that turns it into a density.

## Open question for the author

E5 has three candidate resolutions and they are not equivalent:

1. `eq:electron-mass` is right and `eq:rho0-value` is an algebra slip → $\rho_0 = \alpha m_e^4c^3/(2\pi^2\Lambda\hbar^3)$;
2. `eq:rho0-value`'s **number** is right and `eq:electron-mass` is missing a factor;
3. a different convention for $\kappa_0$ or $\xi$ was used in one of them and not stated.

Only the author can say which was intended. Route 1 is the one consistent with
the printed `eq:electron-mass`.

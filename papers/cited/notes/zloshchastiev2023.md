# zloshchastiev2023 — citation evidence

K. G. Zloshchastiev, *Derivation of emergent spacetime metric,
gravitational potential and speed of light in superfluid vacuum theory*,
Universe **9**, 234 (2023), doi:10.3390/universe9050234.

Open-access source:
`https://inspirehep.net/files/0715887b217e080940b04b34bbbf375e`;
PDF SHA-256 begins `d80609424b0e3774`.

## Claim being checked

The superseded SSV-I text reported that an acoustic Bjerknes force between
breathers had been shown in this source to reproduce Newtonian gravity with
$G$ expressed in terms of $\hbar$, $c$, $m_e$, and $\alpha$. The current
correction is at SSV-I `main.tex:1379`–`1389`:

> Gravity was originally proposed to be the acoustic Bjerknes force — mutual
> attraction between vibrating breathers via secondary flow fields in the
> plenum. **That mechanism is falsified as written** …

## Verbatim context

Universe pp. 9–10, immediately after Eqs. (47)–(48):

> It is important to clarify here the terminology ‘gravitational potential’.
> From Equation (47), it is obvious that no potential exists per se, but
> many-body quantum-mechanical effects in the background superfluid act as
> what we perceive as gravity. The logarithmic term is directly related to
> quantum information entropy of the superfluid, cf. [8,31,32]; therefore, it
> is the change of the entropy of background superfluid that induces the
> “thermodynamic” force and associated “potential”. One can imagine a
> classical analogue of this phenomenon: in diffusive systems, suspended
> particles move from regions of higher to lower concentrations, as if they
> were driven by some macroscopic potential, but in reality it is just that
> the total system tries to find a state with a minimum free energy.

The conclusion on p. 10 states what constants the paper actually claims:

> It turns out that the value of the speed of light, which is a fundamental
> parameter in the theory of relativity, is a derived notion in superfluid
> vacuum theory. Its value is a combination of the Planck constant and the
> original parameters of the background superfluid. The whole theory thus
> contains only two essential fundamental constants: the Planck constant and
> the mass of a constituent particle of the background superfluid.

## Reproducible absence search

Corpus: the complete `pdftotext -layout` extraction, **6,150 words**.

| case-insensitive pattern | occurrences |
|---|---:|
| `Bjerknes` | **0** |
| `electron` | **0** |
| `fine.structure` | **0** |
| `alpha` | **0** |
| `mutual attraction` | **0** |
| `secondary flow` | **0** |

The source does contain $G$ once, in the definition
$\kappa=8\pi G/c^2_{(0)}$ used to compare its effective metric with the
standard linearized-gravity metric (p. 7, Eq. (30)). That is an input to the
comparison, not a derivation of $G$ from the constants attributed by SSV-I.

## Use assessment

**Verdict: `MISATTRIBUTED`.** The paper derives an effective, entropy-related
gravitational potential subject to stated ambiguities. It neither presents a
Bjerknes interaction nor derives Newton's constant from $\hbar$, $c$, electron
mass and the fine-structure constant. The corrected SSV-I text no longer makes
that attribution.

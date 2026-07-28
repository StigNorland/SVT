# JacobsonEEq2016 — citation evidence

T. Jacobson, *Entanglement Equilibrium and the Einstein Equation*,
Phys. Rev. Lett. **116**, 201101 (2016).

Primary source: arXiv:1505.04753v4 · DOI:
10.1103/PhysRevLett.116.201101 · local PDF sha256 `5269c0e7ff5e2e14`.

## SSV usage

SSV-V `main.tex:459–470` says cross-horizon entanglement entropy is the input
that Jacobson's entanglement-equilibrium route turns into the gravitational
field equation.

## Source equations and explanation

The discussion, p. 5, summarizes the scoped equivalence:

> the semiclassical Einstein equation holds, for first-order variations of
> the vacuum, if and only if the entropy in small causal diamonds is
> stationary

The remainder specifies constant volume and variation from a maximally
symmetric vacuum. Equations (12)–(13) split the entropy variation into UV area
and infrared matter terms,

```tex
\delta S_{\rm UV}=\eta\,\delta A,\qquad
\delta S_{\rm tot}=\eta\,\delta A+\delta S_{\rm IR},
```

and stationarity with `η=1/(4\hbar G)` yields the semiclassical Einstein
equation at first order for conformal fields. Nonconformal fields require a
stated conjecture.

**Verdict: `OK`.** SSV accurately identifies the paper's route from local
entanglement equilibrium to the field equation, provided Jacobson's
first-order, small-diamond, vacuum, and matter-field assumptions remain
attached.

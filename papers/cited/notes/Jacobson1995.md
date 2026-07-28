# Jacobson1995 — citation evidence

T. Jacobson, *Thermodynamics of Spacetime: The Einstein Equation of State*,
Phys. Rev. Lett. **75**, 1260–1263 (1995).

Primary source: arXiv:gr-qc/9504004 · DOI:
10.1103/PhysRevLett.75.1260 · local PDF sha256 `85ed65e912baf62c`.

## SSV usage

SSV-VII-b cites the paper at `main.tex:89`, `main.tex:306`, and
`main.tex:367` for the local-Rindler-horizon thermodynamic route from the
Clausius relation to the Einstein field equation.

## Source equation and explanation

The abstract states:

> The key idea is to demand that this relation hold for all the local Rindler
> causal horizons through each spacetime point.

On pp. 4–5 the source identifies horizon heat flux as

```tex
\delta Q=-\kappa\int_H \lambda T_{ab}k^ak^b\,d\lambda\,dA,
```

uses entropy variation `dS=ηδA` and the Unruh temperature
`T=\hbar\kappa/(2π)`, and obtains Eq. (6):

```tex
R_{ab}-\tfrac12 Rg_{ab}+\Lambda g_{ab}
  =\frac{2\pi}{\hbar\eta}T_{ab}.
```

The explanation immediately preceding Eq. (6) says that imposing
`δQ=T dS` for every null generator gives a tensor relation between `T_ab` and
`R_ab`; stress-energy conservation and the contracted Bianchi identity fix the
remaining scalar term to `-R/2+Λ`.

**Verdict: `OK`.** This is the result SSV-VII-b attributes to Jacobson. The
paper verifies the thermodynamic implication; SSV's proposed superfluid
realisation of each ingredient is a separate model claim and is not evidence
supplied by this citation.

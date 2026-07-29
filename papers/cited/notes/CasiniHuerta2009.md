# CasiniHuerta2009 — citation evidence

H. Casini and M. Huerta, *Entanglement Entropy in Free Quantum Field Theory*,
J. Phys. A **42**, 504007 (2009).

Primary source: arXiv:0905.2562v3 · DOI:
10.1088/1751-8113/42/50/504007 · local PDF sha256 `9568e8b3bd7e07c6`.

## SSV usage

SSV-V `main.tex:463–476` says its horizon-entanglement computation uses the
free-field correlator method associated with Peschel and Casini–Huerta and
then reports the battery's own area-law result.

## Source equations and explanation

Section 2.2, p. 9, states the real-time construction:

> In the real time approach one aims to compute directly the reduced density
> matrix corresponding to the global vacuum state in terms of correlators.

For bosons, Eqs. (45) and (59), pp. 10–11, define the restricted field and
momentum correlators and recover the density-matrix spectrum:

```tex
X_{ij}=\langle\phi_i\phi_j\rangle,\qquad
P_{ij}=\langle\pi_i\pi_j\rangle,\qquad
\nu_k=\operatorname{eig}_k\sqrt{XP}
     =\tfrac12\coth(\epsilon_k/2).
```

The review also gives the leading continuum UV behavior
`S(V)=g_{d-1}[\partial V]\epsilon^{-(d-1)}+\cdots` (Eq. 3), proportional to
the boundary area.

**Verdict: `OK`.** The citation supports both the correlator algorithm and
the expected free-field area-law structure. It does not independently verify
SSV's numerical battery or its claimed 5% coefficient stability.

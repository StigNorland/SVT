# Lloyd2011 — citation evidence

S. Lloyd *et al.*, *Closed Timelike Curves via Postselection: Theory and
Experimental Test of Consistency*, Phys. Rev. Lett. **106**, 040403 (2011).

Primary source: arXiv:1005.2219 · DOI:
10.1103/PhysRevLett.106.040403 · local PDF sha256 `f8e881534aa540b1`.

## SSV usage

SSV-III `main.tex:1404–1413` writes the Deutsch fixed-point condition, notes
computational consequences, and cites Lloyd *et al.* specifically as the
postselected alternative.

## Source equation and explanation

Equation (1), p. 1, is

```tex
\rho=\operatorname{Tr}_A[U(\rho\otimes\rho_A)U^\dagger].
```

The source explains why the fixed point exists:

> A state ρ that satisfies Eq. (1) always exists because the above interaction
> is a completely positive map which possesses at least one fixed point.

It then distinguishes Deutsch CTCs from its teleportation-plus-postselection
construction. On p. 3 it states that postselected CTCs can efficiently solve
NP-complete problems, while Deutsch CTCs have the stronger PSPACE result but
may decorrelate outputs from externally stored inputs.

**Verdict: `OK` with scope.** The fixed-point equation and existence statement
are reproduced correctly, and Lloyd *et al.* is an appropriate source for the
postselected variant. It is not the primary source for Deutsch's model or for
every computational property listed in the surrounding SSV sentence.

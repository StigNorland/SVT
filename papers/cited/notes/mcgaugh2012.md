# mcgaugh2012 — citation evidence

S. S. McGaugh, *The Baryonic Tully–Fisher Relation of Gas Rich Galaxies as a
Test of ΛCDM and MOND*, Astron. J. **143**, 40 (2012).

Primary source: arXiv:1107.2934 · DOI:
10.1088/0004-6256/143/2/40 · local PDF sha256 `69741090b0bd5feb`.

## SSV usage

SSV-VI `main.tex:248–258` contrasts a failed predicted slope `3/2` with the
observed BTFR exponent near four. At `main.tex:516–519` it writes the
equivalent velocity–mass prediction as slope `1/4`.

## Source equation and explanation

Equation (2) defines the general relation `M_b=A V^x`. The abstract reports the
measured special case:

> Recent independent data for such galaxies are consistent with
> M_b = A V_f^4 with A = 47 ± 6 M⊙ km−4 s4. This is equivalent to MOND.

The fourth power implies both forms used by SSV:

```tex
M_b\propto V_f^4
\qquad\Longleftrightarrow\qquad
V_f\propto M_b^{1/4}.
```

The source explains why gas-rich galaxies constrain the exponent particularly
cleanly: their baryonic masses are comparatively insensitive to uncertain
stellar-population mass-to-light ratios.

**Verdict: `OK`.** SSV uses both algebraically equivalent versions of the
source's measured BTFR scaling correctly.

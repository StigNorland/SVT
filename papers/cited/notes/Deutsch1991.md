# Deutsch1991 — citation evidence

D. Deutsch, *Quantum mechanics near closed timelike lines*, Phys. Rev. D
**44**, 3197–3217 (1991).

Primary source: DOI 10.1103/PhysRevD.44.3197 · pre-arXiv · APS full text ·
local PDF sha256 `afea606ca7119546`.

## SSV usage

SSV-III `main.tex:1402–1415` presents Deutsch's chronology-violating system
as a fixed-point density matrix,
\(\rho_{\rm CTC}=\operatorname{Tr}_A[U(\rho_A\otimes
\rho_{\rm CTC})U^\dagger]\), and says a fixed point exists for every unitary.
The same passage attributes efficient NP-hard computation and
distinguishability of non-orthogonal states to the proposal.

## Source result and explanation

Printed p. 3203 (PDF p. 7), Eqs. (15)–(16), gives the consistency condition
and channel:

\[
\operatorname{Tr}_1[U(\rho_1\otimes\rho_2)U^\dagger]=\rho_2,
\qquad
S\rho=\operatorname{Tr}_1[U(\rho_1\otimes\rho)U^\dagger].
\]

The accompanying paragraph states:

> The expression on the left in (15) may be regarded as the image of
> \(\rho_2\) under a linear superscattering operator \(S\) on the space of
> density operators on \(\mathcal H_2\), defined by (16), so it remains to be
> proved that every operator of the form (16) has a fixed point.

The following construction, Eqs. (17)–(18), averages iterates of \(S\);
compactness of the finite-dimensional density-operator space supplies an
accumulation point, which the paper proves is fixed. The abstract and printed
pp. 3214–3215 also explicitly say chronology violation permits cloning a
quantum system and measuring its state, which would operationally allow
otherwise non-orthogonal states to be distinguished.

**Verdict: `OK`.** The fixed-point equation, existence result, and
state-measurement consequence are supported. Deutsch discusses a
fixed-point-finding computation and possible speed advantage, but this paper
does not establish the modern precise claim that D-CTCs efficiently solve
NP-hard problems; that clause needs a later computational-complexity source
and should not be attributed to Deutsch 1991 alone.

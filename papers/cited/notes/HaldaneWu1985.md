# HaldaneWu1985 — evidence (resolved by proxy)

F. D. M. Haldane and Y.-S. Wu,
*Quantum dynamics and statistics of vortices in two-dimensional superfluids*,
Phys. Rev. Lett. **55**, 2887–2890 (1985) · doi:10.1103/PhysRevLett.55.2887

**Not obtained.** Pre-arXiv and behind the APS paywall. Paywalls are not
circumvented (see `INDEX.md`).

**Verdict: `MISREAD`** — established from an open-access secondary source rather
than by assumption. Cited by **SSV-II `main.tex:832`** (C4/D3).

## Why a proxy is admissible here

`polkinghorne2021` (Phys. Rev. A **104**, L041305, arXiv:2101.07438) is not
merely repeating the claim second-hand. It

1. quotes the result in its **abstract**, with the PRL reference attached,
2. **re-derives** it (its Eq. S1), and
3. **verifies it numerically** by Gross–Pitaevskii simulation, concluding
   "the prediction by Haldane and Wu … is correct".

Verbatim quotations: `notes/polkinghorne2021.md`. Same standard as the
`volovik2003` → `volovik2001` and `lamb1932` → owner-supplied-images
resolutions.

## The result

$$\gamma_C = 2\pi N_C$$

where $N_C$ is the **number of condensate atoms enclosed by the vortex
trajectory**.

## What SSV-II attributes to it

`main.tex:832–834`:

> This is precisely the Haldane-Wu mechanism~\cite{HaldaneWu1985}: a vortex
> transported around a closed path accumulates a geometric (Berry) phase
> proportional to the number of **circulation quanta** it encloses.

Enclosed **atoms** ≠ enclosed **circulation quanta**. The two differ in
character, not only in name: $2\pi N_C$ scales with the enclosed area × density
and is unbounded as the loop grows, whereas the quantity SSV-II needs must be
invariant under deformations of the loop. Full comparison and consequences:
`papers/SSV-II/results/audit-2026/C-gate-damage-report.md` (D3) and the E-gate
report (E3).

## Bibliographic entry

SSV-II `main.tex:3276–3279` gives *Phys. Rev. Lett.* **55**, 2887–2890 (1985),
which matches ref. [14] of `polkinghorne2021` exactly. **The bibitem is correct**;
only the content attributed to it is not.

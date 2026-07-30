# Issue #216 — E6 dimensional propagation

Status: **complete**; focused validation recorded below.

## Fixed convention

Paper I uses mass density \(\rho\), a dimensionless order parameter
\(|\Psi|^2=\rho/\rho_0\), background number density
\(n_0=\rho_0/m_0\), and a mass-specific logarithmic stiffness
\([b]=\mathrm{J\,kg^{-1}}=\mathrm{m^2\,s^{-2}}\).

The dimensionally complete longitudinal action is
\[
\mathcal L_0=
\frac{i\hbar n_0}{2}(\Psi^*\dot\Psi-\Psi\dot\Psi^*)
-\frac{\hbar^2n_0}{2m_0}|\nabla\Psi|^2
-b\rho[\ln(\rho/\bar\rho)-1]-V_0 .
\]
Its Euler–Lagrange equation contains the energy coefficient \(m_0b\):
\[
i\hbar\partial_t\Psi=
-\frac{\hbar^2}{2m_0}\nabla^2\Psi+
m_0b\ln(\rho_0|\Psi|^2/\bar\rho)\Psi .
\]
Consequently
\[
P=\rho\mu-V=b\rho,\qquad
c_s^2=\frac{dP}{d\rho}=\rho\mu'(\rho)=b.
\]
The light-as-sound postulate fixes \(b=c^2\), and the conventional healing
length is
\[
\xi=\frac{\hbar}{\sqrt{2m_0(m_0b)}}
   =\frac{\hbar}{\sqrt2\,m_0c}.
\]
This is the same numerical length already carried by the registered Paper I
values, so the correction requires no numerical-value migration.

## Exact dispersion and the negative control

Linearizing the corrected LogSE about the homogeneous state gives
\[
\omega^2=bk^2+\frac{\hbar^2k^4}{4m_0^2}
=c_s^2k^2\left(1+\frac{\xi^2k^2}{2}\right).
\]
Thus the expression \(c_s^2k^2(1+\xi^2k^2)\) is rejected when \(\xi\) means
the conventional healing length. It is valid only after defining the shorter
dispersive crossover length
\(\ell_{\rm disp}=\xi/\sqrt2=\hbar/(2m_0c_s)\).

This exposes a cross-paper naming consequence: the #166 disk instrument uses
the unit-coefficient form, so its variable named `xi` denotes
\(\ell_{\rm disp}\). Its gapless result is not invalidated, but the label and
receipts require a separately scoped migration.

## Vortex and BdG consequences

With \(s=\xi\tilde s\), the unit-winding static profile obeys
\[
-\left(\partial_{\tilde s}^2+
\frac{\partial_{\tilde s}}{\tilde s}-
\frac{1}{\tilde s^2}\right)f_0+
f_0\ln(f_0^2)=0.
\]
The existing `vortex_profile.py` coefficient-two equation is retained only as
a legacy control; it is not the corrected Paper I profile.

The corrected linearization has
\[
\hat L=-\frac{\hbar^2}{2m_0}\nabla^2+
m_0b[\ln(f_0^2)+1]-\mu_{\rm chem},
\qquad
\hat M=m_0b\,e^{2i\theta}.
\]
Because \(\hat M\ne0\), the old scalar operator
\(-\nabla^2+4(1-f_0^2)\) is not the corrected LogSE Hessian. Its positive
potential proves no no-bound-state theorem for the physical coupled BdG
problem. The amplitude-mode question is open. This does not reverse the
independent basis-convergence and Berry-phase null results.

The same healing-length normalization changes the string estimate to
\[
\frac{\omega_{\rm ring}}{\omega_c}
=2\alpha\sqrt{\ln(1/\alpha)}.
\]
It remains below the muon target, so the result stays negative.

## Primary-source check

The retrieved primary source is Zloshchastiev 2020,
arXiv:2011.11897. The local PDF SHA-256 is
`8aff20eb75784f6db483cb3a4ec03d715441f77d2ac544cd6aeecab362818e92`.
Its Eq. (1) uses a frequency coefficient \(b_{\rm src}\); its defining
constraint gives
\[
|b_{\rm src}|=\frac{mc_s^2}{\hbar},
\]
with neither \(\rho_0\) nor a factor two. Paper I's stable convention maps
\(-\hbar b_{\rm src}=m_0b>0\). The source's printed natural-length expression
is not dimensionally homogeneous with that Eq. (1), so Paper I derives
\(\xi\) independently. Paragraph-level evidence and exact SSV usage sites are
recorded in `papers/cited/notes/zloshchastiev2020.md`.

## Corpus and searches

The propagation audit covers Paper I's `main.tex`, current Paper I instruments
and tests, the dimension checker, Paper I result records, and programme failure
modes. Searches reject current printed uses of:

- \(b\rho_0=m_0c^2/2\) or \(b=m_0c^2/(2\rho_0)\);
- \(c_s^2=2b\rho_0/m_0\);
- \(\xi=\hbar/(m_0c)\);
- \(c_s^2k^2(1+\xi^2k^2)\) with conventional \(\xi\);
- the scalar amplitude operator as a physical no-bound-state proof;
- the old ring ratio \(\alpha\sqrt{\ln(1/\alpha)}\).

Historical audit records may retain the rejected spellings when visibly
labelled as history or negative controls.

## Validation

Focused tests cover the analytic identities, deliberate negative controls,
dimension registry, citation evidence, provenance and build tooling. The
paper is compiled through `build_paper.py SSV-I`; the calculation-heavy full
suite is intentionally not run.

Command:

```text
pytest -q \
  instruments/test/paper_i/test_ssv_i_audit_2026.py \
  instruments/test/tools/test_dimensions.py \
  instruments/test/tools/test_citation_evidence.py \
  instruments/test/tools/test_gen_provenance.py \
  instruments/test/tools/test_build_paper.py
```

Result: **119 passed in 3.67 s**.

Command:

```text
python instruments/tools/build_paper.py SSV-I
```

Result: all bibliography, citation-evidence, provenance, value, claim,
change-record and symbol gates passed; BibTeX plus three `pdflatex` passes
completed with **0 errors and 0 undefined references**. The tracked output is
`papers/pdf/SSV I.pdf`.

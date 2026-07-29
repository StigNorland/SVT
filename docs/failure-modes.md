# Failure modes of this programme, and what guards each

The #182 audit's finding was blunt: *"The computations were sound. The write-up
was not."* Not one defect in the numerical corpus across twelve papers. Every
defect was in prose, a citation, or an algebraic step in the text.

This file is the register of the failure modes actually observed — not imagined
ones — with the guard for each and, where the guard is partial, what it does not
cover. It is the answer to "how would we know if this went wrong again?"

**Every FM below has been observed at least once in this repository.** None is
speculative. Where a guard was added after the fact, the entry says so, because a
guard that has never caught anything is a hypothesis, not a control.

Guard status: **closed** = a test fails if it recurs · **partial** = detected only
in registered cases · **convention** = discipline, not machinery.

---

## FM1 — a printed number drifts from the instrument that derives it

**Observed:** SSV-I printed `ρ₀ = 1.9` beside a formula yielding `0.0078`. The two
disagreed in print for years (#182 E5, #183).

**Why it survived:** the number and the code were two independent objects, and
nothing compared them. Correctness depended on care at the moment of typing.

**Guard — closed.** Rule 14. The number exists once, in an instrument; the result
is recorded in `results/values_receipt.json`; `values.tex` is rendered from the
receipt; the paper prints a macro. `test_replaced_literal_is_gone` fails if the
value is *also* typed into the prose, which is the way this defect actually
re-enters.

**Not covered:** only the seven registered values. Every other printed number in
the series is still typed by hand.

---

## FM2 — a reviewed result drifts after its generated number moves

**Observed:** SSV-I printed `R_e* = a₀/√2 ≈ 3.74e-11`, correct. The test that
looked like its guard, `test_e4_xi_over_alpha_is_the_bohr_radius`, asserted the
*uncorrected* `ξ/α = a₀ = 5.29e-11` — a different quantity. The printed sentence
was true by coincidence and guarded by nothing (found 2026-07-28 while building
the FM1 guard).

**Why it matters:** FM1's guard makes a value *follow* its instrument. A
legitimate change to the physics can therefore propagate into the paper
**silently and cleanly** — the receipt updates and the PDF rebuilds, while a
relationship reviewed against the old value is no longer valid.

**Guard — partial.** `instruments/tools/claims.py` binds each reviewed numerical
relationship to a stable LaTeX anchor, its generated inputs, a predicate and a
tolerance. `build_paper.py` checks both the anchor and predicate **before
`pdflatex`**, so later source or numeric drift requires deliberate review.

Verified by deliberately dropping the √2 from `xi_over_alpha`: the value gate
passed (the receipt updated correctly), and the build refused, naming
`main.tex:541` and `main.tex:537`.

**Not covered:** this guard cannot determine whether an author or model wrote a
sound conclusion in the first place. It freezes a relationship after review; it
does not perform the review. Coverage is also limited to 9 claims across 2
papers. `test_every_generated_value_is_claimed` catches values with no registered
relationship, not every inference made in prose.

**Future improvement — independent semantic review.** When a +2-agent harness is
available, give every new or materially changed conclusion and its predicate to
independent "third eye" review before registration. The independent reviewers
should check that the conclusion follows from the result and that the predicate
actually represents the conclusion. The build gate then preserves what they
reviewed.

---

## FM3 — a check that only looks like a check

**Observed twice in one afternoon, both in code written for #198:**

1. `mp.almosteq(a, b, rel_eps=1e-6)` defaults `abs_eps` to `rel_eps`, so for
   quantities of order `1e-35` every assertion passed on the absolute test alone.
   Seven green tests proving nothing.
2. The first `lambda-enters-denominator` predicate restated the computation
   instead of the conclusion. It passed, and guarded nothing.

**Why it matters more than an ordinary bug:** a broken check is worse than no
check, because it is counted as coverage. Both instances were green.

**Guard — partial.** Negative controls, and guards on the guards:
`test_rel_close_is_not_trivially_true`, `test_claims_are_not_tautologies` (which
perturbs every input a predicate reads and requires it to notice), and
`test_the_tautology_detector_detects_a_tautology`. Case 1 was caught by a
negative control; case 2 by hand.

**Not covered:** nothing systematically checks that a *test* tests what its name
says. Both instances were found by writing a deliberate negative case, which is a
habit, not a mechanism.

---

## FM4 — a symbol carries two dimensions

**Observed:** three times in one audit — SSV-I `b` (eq:pot needs L²T⁻², eq:cs and
eq:xi need L⁵T⁻²), SSV-II `e` (mass in the Berry phase, charge in `Φ₀=h/e`),
SSV-V `b` (a frequency, undeclared against Paper I's). Two of the three surfaced
during the *rewrite*, not the audit, so a clean gate report would have shipped
with them intact (#182 E6/E3b, #187 E2).

**Why the gates missed it:** they checked equations, and even checked *products*,
but never asked whether a symbol means one thing throughout.

**Guard — partial.** Rule 15, `instruments/tools/dimensions.py`. Symbols are
anchored or free; the check asks whether *any* assignment to the free symbols
makes the printed relations simultaneously homogeneous.

**Not covered:** it does not parse LaTeX. It checks relations *as transcribed*,
for three papers only. A relation nobody typed in is invisible to it.

---

## FM5 — a result credited to a source that does not contain it

**Observed:** SSV-I's logarithmic equation of state was credited to Volovik,
whose Phys. Rept. 351 contains no such thing (`"equation of state"` occurs 0
times in 71,425 words). The real source's constraint was therefore never applied,
which is what generated the whole #180 error chain.

**Guard — partial.** Rule 12, the evidence rule: no verdict without a tracked
record in `papers/cited/verification.json` and the quote directory
`papers/cited/notes/<key>.md`. The records bind the
SSV claim to a source locator, the complete relied-on paragraph (or a
reproducible absence search), and an explicit use assessment. Owner-supplied or
image-only pages also require an accessible Markdown transcript under
`papers/cited/transcripts/`. `citation_evidence.py` checks this structure on
every gated build, and `missing_evidence()` must stay empty.

**Not covered:** a quotation proves the source says it; it does not prove the
reviewer’s interpretation is correct. The explicit use assessment makes that
judgment inspectable, but a semantic error still needs a third eye. An
inaccessible primary can pass without its own paragraph only through an
explicit reasoned waiver; `PENDING-PRIMARY` leaves unresolved dependent claims
flagged but printed.

**Retrieval is weaker than the rule's wording suggests (found 2026-07-28).**
Rule 12 says sources are "hash-pinned and re-fetchable via `fetch_cited.py`".
That holds for most, not all: **72 of 99** primaries are cached locally, and
three notes state in their own prose that the primary was not retrieved —
`bbm1976` ("the host's anti-bot layer prevented a reproducible local download"),
`Hawking1974`, and `toomre1981`. Their quotations were read and checked by a
human and their verdicts stand; what is overstated is *reproducibility*, not
correctness. Treat "hash-pinned and re-fetchable" as the norm the registry aims
at, and read each record's `access` block for the actual state.

**One structural hole in this guard, now closed.** The validator rejected an
*open* source that waived its paragraph, but not an *inaccessible* source that
**asserted** one — the stronger claim. `toomre1981` passed the gate registered
`unavailable` + `paragraph_required: true` + no waiver while its note recorded
that the chapter was not obtainable and quoted only an ADS abstract. The
symmetric rule now exists
(`test_inaccessible_source_cannot_assert_a_complete_paragraph`), with a
transcript the single legitimate exemption, and the record carries an explicit
`unavailable-primary` waiver. This is FM3 inside the evidence layer: the check
that was there looked complete and covered one direction only.

---

## FM6 — an absence claim with no search behind it

**Observed:** the #197 rewrite plan inventoried the printed forms of the
logarithmic potential and asserted **"No others."** A wider pattern found a 13th
site. Consequence nil, but the claim was false and it was made in a
pre-registration.

**Guard — convention.** Rule 13: state the pattern, the corpus and the count.
*"`equation of state` occurs 0 times in 71,425 words"* is re-runnable;
*"no others"* has to be trusted.

---

## FM7 — a falsification that is explicit in one place and invisible in another

**Observed:** the #119-falsified Bjerknes mechanism was presented as current in
three papers while being recorded as falsified elsewhere (#182).

**Guard — convention.** Standing rule 1, plus the `gapbox` / `falsbox`
convention: when a result is withdrawn, the withdrawal is printed at the site of
the claim, not only in a results note. SSV-VII-a §"Saturation by the Gausson"
carries an interim block for exactly this reason while its repair is pending
(#189).

**Not covered:** nothing enumerates the sites of a retired claim. This is the
failure mode with the weakest machinery behind it.

---

## FM8 — a checker that over-reports

**Observed:** the first `dimensions.py` flagged `hbar`, `m_0` and `kappa_0` as
dimensionally overloaded. They are not — they appear inside relations broken by a
*different* symbol, and solving a broken relation for a healthy symbol yields
nonsense (2026-07-28, caught before publication).

**Why it belongs in this register:** an inflated defect is a defect. Rule 1 says
negative results must not be softened; it equally forbids manufacturing them.
Over-reporting also trains readers to ignore the tool.

**Guard — closed for this case.** The anchored/free split, plus
`test_solving_for_an_anchored_symbol_is_refused`, which makes the specific
mistake raise rather than return a plausible-looking wrong answer.

---

## FM9 — citation metadata points at the wrong work

**Observed:** SSV-I's unused `liberati2006` bibitem was paired in the retrieval
registry with arXiv:0909.3834. That preprint has a different author list and a
2009 date, so the identifier did not identify the bibliography entry. The same
metadata pass also found a published Nitta paper labelled “arXiv only”.

**Guard — partial.** `papers/cited/verification.json` is now the canonical
machine-readable record. Every entry requires a source URL plus an explicit DOI
and arXiv status; present identifiers are syntax-checked, and its keys must
exactly match the retrieval registry. The unused mismatched bibitem was removed.

**Not covered:** syntax and completeness do not prove an identifier belongs to
the named work. Author/title/content matching still happens during initial
review. A third-party metadata service can also be wrong.

---

## FM10 — duplicated bibliographies drift into different identities

**Observed:** the same Volovik book appeared under `Volovik`, `Volovik2003` and
`volovik2003`; the same papers likewise had aliases such as `Villois` /
`Villois2017`. Counting the 27 files in `papers/cited/pdf/` was consequently
mistaken for counting the series bibliography, although the series cites 93
distinct external works.

**Guard — closed for key duplication and wiring.** All twelve papers now use
`papers/cited/references.bib`. BibTeX selects only cited entries.
`bibliography.py` rejects inline bibliographies, undefined keys, duplicate or
retired aliases, and quote-registry sources absent from the shared database.
The build gate runs it before compilation.

**Not covered:** the initial migration preserves legacy formatted citations in
BibTeX `note` fields. Centralisation prevents future cross-paper drift, but the
112 entries still need a separate metadata-enrichment pass to structure and
externally verify every author, title, DOI and arXiv identifier.

---

## FM11 — a cited work is absent from the review inventory

**Observed:** after centralising the bibliography, only 10 of the 93 directly
cited external works had citation notes; the other 83 were invisible in the
note layer. Six additional notes existed only because the audit had introduced
proxy or corroborating sources.

**Guard — closed for inventory, not verification.** Every one of the 102 cited
works, including nine local SSV sources, now has a registry entry and note.
Evidence-only sources remain catalogued too, for 108 notes total. The build
rejects missing notes, orphan notes, stale `cited_by` lists, and a note promoted
to `evidence-recorded` without a full source-verification record.

**Not covered:** the inventory makes a gap visible and navigable; it does not
manufacture quotations, source URLs, identifiers, or verdicts.

**Update, `d6bcc2e`:** the 83 notes this entry originally recorded as
`NOT-REVIEWED` have since been reviewed and promoted. The registry now holds 99
`evidence-recorded` and 9 `local-source` notes and **no `NOT-REVIEWED` entries at
all**; 72 of the 99 primaries are cached locally. Spot-checked against an
independent derivation: `bbm1976`'s note reports BBM's
\(\ell=\hbar/\sqrt{2mb}\) and its restriction to \(b>0\), which matches the
symbolic substitution done separately under #189 — so the promotion reflects
real review, not an automated status flip.

The residual gap is narrower and different in kind: the promotion outran the
*retrieval* guarantee. See FM5.

---

## FM12 — a tracked generated artifact is not reproducible across environments

**Observed:** `papers/SSV-VI/results/dsph_ledger_receipt.json` is written by
`dsph_ledger.main()`, which `test_real_ledger_runs_and_is_coherent` calls — so
**the test suite rewrites a tracked file**. Two runs on one machine are
byte-identical, but values drift by up to `3.83e-15` relative *across*
environments (BLAS/CPU reduction order), which moved **25 of its 259 floats**.
During the #198 work this dirtied the working tree on five separate occasions
and was once swept into an unrelated commit by `git add -A`, needing an amend.
The same run also re-rendered `fig_dsph_ledger.png` at a different byte size
(85 KB → 102 KB) purely from a different matplotlib build.

**Why it matters beyond tidiness:** churn that appears on every run stops being
read. A reviewer who sees this file modified after every test run learns to
`git checkout` it reflexively — which is exactly the habit that lets a *real*
change to a result receipt pass unnoticed. It also makes `git add -A` unsafe,
and that is not a habit worth having in a repository whose whole discipline is
that tracked artifacts mean something.

**Guard — closed for the receipt.** Values are written at
`RECEIPT_SIGFIGS = 10` significant figures. Measured rather than estimated, by
testing both ends of the drift interval against every value (rounding is
monotonic, so this is exact, not statistical):

| s.f. | drift tolerated, 259 floats (#198) | drift tolerated, 618 floats (#203) |
|---|---|---|
| none | — | — |
| 12 | 4.3e-14 (11×) | 1.0e-14 (3×) |
| 10 | **3.6e-12 (906×)** | 3.7e-13 (**91×**) |
| 9 | — | 4.9e-12 (1222×) |
| **8** | — | **7.7e-12 (1931×)** |

12 s.f. — the intuitive "a couple fewer decimals" — also passed at #198, but on
an 11× margin a recomputation could eat.

**And then a recomputation ate it.** #203 added a sweep axis, the receipt grew
from 259 floats to 618, one sweep value landed 3.7e-13 from a rounding boundary,
and the 906× margin fell to 91× — the guard fired, correctly, and
`RECEIPT_SIGFIGS` moved to 8 (~1900×). The lesson is sharper than the fix:
**the margin is a property of the values, not of the s.f. choice**, so it must
be re-measured whenever the receipt grows rather than inherited from the comment
that recorded it. (Note 8 s.f. beats 9 here — that is where these particular
numbers happen to fall, not a trend to generalise.)

`test_receipt_is_stable_under_environment_drift` asserts the
receipt survives 100× the observed drift, and
`test_rounding_actually_changes_what_is_written` stops the rounding being
silently disabled — without it, that test would still pass on today's values.

**Not covered:** the figure. PNG output is not byte-reproducible across
matplotlib builds and nothing rounds it; it simply must not be regenerated
casually. And this is one artifact — the other ~20 `results/*_receipt.json`
files have not been checked for the same property, so **do not assume a receipt
is stable because this one now is**.

**A note on how this was diagnosed**, because it is FM3 again and I walked into
it three times: the first two attempts to size the rounding were wrong — an
analytic estimate that mismodelled the boundary geometry, then a Monte-Carlo
that perturbed the *same fixed value* repeatedly and so could only ever answer
"this particular number is safe", never "the receipt is safe". A third check
measured distance to the nearest *grid point* rather than the nearest *rounding
boundary*, which scored exactly-representable values like `1.6` as maximally at
risk when they are maximally safe. Only the exact endpoint test is right. Three
plausible-looking measurements, three wrong answers, all of which would have
been reported with a straight face.

---

## FM13 — a constant labelled with a provenance it does not have

**Observed:** `instruments/paper_vi/dsph_ledger.py` carried

```python
# H9 MW reference (h9_triangle_receipt.json) and inversion
M_MW = 6.0e10            # M_sun
R_MW_KPC = 15.0          # kpc
V_MW = 220.0             # km/s
GAMMA_REQ_MW = 1.297e9   # m^2/s
```

Two of the four came from that receipt. H9 records a BTFR velocity of
**189.02** km/s at this mass, not 220, and contains **no MW circulation radius
at all** — 10 kpc appears in it only as the radius where a required medium flow
is evaluated. The comment asserted a sourcing for all four.

**Why it matters:** this is FM1 with the arrow reversed. Rule 14 stops a printed
number drifting *from* its instrument; nothing stopped the instrument itself
resting on a constant that was never sourced. Every downstream guard — receipt,
`values.tex`, claim predicate — would faithfully preserve a wrong number,
because they check consistency, not provenance. The mislabelling survived the
\#182 audit, the \#198 pass, and a published falsification.

**Guard:** the constants are now **read from the H9 receipt at import**, so the
class of defect is structurally impossible rather than merely corrected —
rule 14's "a load-bearing number must not exist twice", applied across papers.
`test_h9_constants_are_read_not_retyped` asserts the read. The genuinely
unsourced one (`R_MW_KPC`) is declared a convention in the code and in the
receipt, and carried as a sweep axis instead of being asserted.

**Not covered:** nothing checks that a *comment* naming a source is true. Only
the constants actually read from a receipt are protected; the next hand-copied
literal under an authoritative-sounding comment will read exactly as convincing.
Prefer reading a value over citing it in a comment.

---

## FM14 — a robustness sweep that omits the axis the conclusion turns on

**Observed:** \#147's B1 was reported "stable across the entire pre-registered
robustness sweep … 27 combinations" — varying `M*/L`, the dwarf rotation limit,
and an anisotropy systematic. It did **not** vary the Milky-Way normalisation
radius, which was the single largest lever on model B (a factor 3.4 between
defensible choices, against 1.3–1.5 for the axes that were swept). Adding it in
\#203 took the grid to 81 points, and **6 of them stopped returning
"falsified"**. A verdict asserted as sweep-stable was, on the completed grid,
sweep-fragile.

**Why it matters:** a sweep is an argument that a conclusion does not depend on
choices the author made. It is only as strong as the choices it varies, and the
axes easiest to think of are the ones already written down as parameters — the
sweep inherits the author's blind spot precisely where it is meant to correct
for it. Worse, a passing sweep reads as *more* rigorous than no sweep, so the
gap is actively camouflaged.

**Guard — partial, and honest about it.** `dsph_ledger.b1_fragility_report()`
records where the verdict fails, whether the failing region lies outside the
observational limit, and the margin inside it; the SSV-VI claim
`fragility-lies-outside-the-observational-limit` fails the build if a later
change makes B1 stable, or moves the fragility *inside* the observational limit
— it guards the negative result in both directions. The unqualified
`B1_sweep_stable` flag stays `false` in the receipt rather than being redefined
to something that passes.

**Not covered, and this is the important half:** nothing can tell you an axis is
missing. There is no check for "the sweep should also have varied X" — that is a
review question, and the only general defence is to ask, before writing
"sweep-stable", *which single choice would move this conclusion most, and is it
in the grid?* Here the answer was no, for years.

---

## FM15 — a paper narrates its own edit history

**Observed:** ten of twelve papers carried change-record prose, and SSV-I
carried an entire **`What changed in this paper`** section — a changelog inside
the argument. A first survey found 16 passages; the gate written to enforce the
rule immediately found **two more the survey had missed**, including that
section, because it used wording ("appeared in earlier drafts", "was previously
headlined") the survey's patterns did not cover. The final count was 18
passages across 5 papers, roughly 180 lines.

Density showed the habit **accelerating, not decaying**: SSV-VII-a carried 4
passages in 3,876 words the same day it was audited, against SSV-IV's 0 in
11,067. Most of VII-a's were written by the model, in the repository's own house
style, hours before the rule existed.

**Why it matters:** it is not only length. A reader cannot tell, at a glance,
whether a paragraph states what the theory claims or what it used to claim, and
the two are interleaved inside single sentences. The paper stops being a
statement of the theory and becomes a diff.

**Guard:** `build_paper.py::gate_change_records` — a literal deny-list of
phrases, run before `pdflatex`, plus a required `papers/<PAPER>/CHANGELOG.md`
so removed history has somewhere to go. Linked once from the generated
provenance appendix.

**The dangerous failure of this guard, and what stops it.** A naive
implementation would ban verdict words — `withdrawn`, `falsified`, `retracted`,
`rejected` — and would then be a tool for **deleting negative results**, which
is the exact defect \#182 existed to find. The deny-list contains no verdict
word, and `test_present_tense_verdicts_are_never_banned` asserts that for each
of the four. The distinction is **tense, not topic**: a falsification stated in
the present tense is not a change record.

Migration is a *split*, not a delete: most passages are half status and half
history inside one sentence. Every removed passage must leave a present-tense
statement of the same finding in the paper, and the removed text is reproduced
verbatim in the changelog, so nothing is destroyed — only relocated.

A claim guard whose statement moves **moves with it**: `claims.py` anchors to
whatever file `site` names, so `rho0-smaller-by-2e4` now guards its sentence in
`papers/SSV-I/CHANGELOG.md` rather than being quietly dropped when the sentence
left `main.tex`.

**Not covered:** the gate matches *phrasing*, not intent. "This paragraph used
to say something else", written in words not on the list, passes. It is a drift
guard like rules 15 and 16, and the judgement of whether a paper reads as a
statement or as a diff stays with the reviewer.

---

## FM16 — deterministic green is mistaken for semantic verification

**Observed:** the first `ssv-verify` series run produced clean artifact,
bibliography and build checks for papers that still contained mis-scoped
citations, inherited retired claims and observation-backed “predictions.”
Those defects were found only by reading the cited evidence and the prose.

**Why it survived:** hashes, generated artifacts and successful compilation
answer whether the repository is internally consistent.  They cannot answer
whether a sentence follows from a source or a computation.

**Guard — partial.** The v2 audit schema never emits a semantic-pass verdict;
its report distinguishes deterministic checks from human review IDs, and
`test_verdict_never_claims_semantic_pass_from_green_checks` freezes that
boundary.  A green report means the requested checks ran cleanly, not that the
theory or manuscript is verified.

**Not covered:** semantic review remains a reviewer task.  The schema can
prevent a false label but cannot make the review happen.

---

## FM17 — a generated-artifact rule assumes every paper has inputs

**Observed:** SSV-Alpha and SSV-Goldstone cite no issue, file or result links
that require a provenance appendix, yet the verifier required an empty
`provenance.tex` and reported both papers stale.

**Guard — closed for this case.** `_audit_provenance` now renders and compares
the appendix only when at least one provenance reference exists.
`test_provenance_without_references_needs_no_generated_file` reproduces the
zero-reference paper and requires a pass without a generated file.

**Not covered:** other generators may still confuse “no inputs” with “missing
output”; each needs its own empty-domain test.

---

## FM18 — an observed value is inverted and reported as a prediction

**Observed:** SSV-II selected the golden-ratio cap prefactor after back-solving
the observed W mass.  SSV-VIII inverted the observed baryon-to-photon ratio to
obtain a required quench-time ratio, then described that ratio as lying in a
natural SSV window.  The same instrument also carried hard-coded
pseudo-cosmological outputs it had not derived.

**Why it matters:** algebraic inversion is useful as a target or consistency
check, but it has zero out-of-sample predictive content when the observation
being “predicted” supplied the input.

**Guard — partial.** The W prefactor and the Kibble--Zurek inversion are now
labelled post hoc/required-input results.  The KZ receipt records
`eta_status`, stores the fitted regression uncertainty, and no longer writes
the hard-coded cosmological “predictions.”

**Not covered:** no tool can infer that a literal or parameter was selected
after seeing the answer.  Provenance of fit and calibration choices remains a
review obligation.

---

## FM19 — a correction does not propagate to dependent papers

**Observed:** after the series had adopted
\(\xi=\hbar/(\sqrt2m_0c)\), SSV-Alpha still printed the old healing length and
SSV-VII-b still used a gravity conversion and Planck-mass statement missing the
same \(\sqrt2\).  Paper IX likewise inherited Paper VIII's superseded
Kibble--Zurek promotion.

**Guard — partial.** A semantic change must still be searched across the
series, including downstream summaries and auto-memory, before it is closed.
For a value declared in `gen_values.SHARED`, however, one series receipt emits
the same macro into every consumer paper and
`test_no_shared_literal_survives` plus the build gate reject a second typed
copy.  Equations, status labels and every value nobody registered remain
manual.

**Not covered:** there is no dependency graph for equations or claim statuses,
and the registry cannot guard a quantity nobody declared.  The one-paper-at-a-
time audit is the present control for that unregistered surface.

---

## FM20 — a necessary diagnostic is promoted to a sufficient theorem

**Observed:** SSV-V's \(M=\xi/(\pi r_H)\ll1\) demonstrates hydrodynamic scale
separation, but the instrument, receipt and paper called it a sufficient
thermality condition for the superluminal LogSE branch.  The cited
Corley--Jacobson calculation uses subluminal dispersion and does not establish
that implication.

**Guard — partial.** The instrument now names the boolean
`hydrodynamic_scale_separation`, records thermality as unresolved and keeps the
kinematic surface-gravity/temperature result separate.  The generated receipt
therefore cannot silently restore the stronger label.

**Not covered:** the general necessary-versus-sufficient distinction remains
semantic.  A mode-conversion calculation is still required.

## FM21 — a table row and the prose it supports come from different runs

**Observed:** SSV-I's Table `tab:Fstraight` printed \(F\) at three grid
resolutions.  Its \(n{=}24\) and \(n{=}72\) rows came from the current relaxed
states; its \(n{=}48\) row was still the superseded state
(\(F(1.18)=4.15\) against the current \(4.528\)).  The prose band
\(m_p\approx930\text{--}954\) MeV was computed from the *current* \(n{=}48\)
value, so the table silently contradicted the number it existed to support —
and the paper simultaneously carried a second figure, \(927\) MeV, that lay
*outside* its own band.  Nine literal sites, no guard on any of them.  Found by
the owner reading the paper, three audits after the numbers were written.

**Guard — partial.** Rule 14 and #213 Part C protect a table cell once its value
is registered: the paper must use the generated macro and the build gate
rejects the old literal anywhere in `main.tex`, including `tabular`.  An
unregistered literal remains invisible.  Rule 16's claim guards anchor to a
*sentence*, so a number that appears only as an unregistered table cell has
nothing to anchor.  The re-run
(`instruments/paper_i/proton_geometric_r_probe.py`, 23 s) reproduces the
correct values, so the check is available — it simply was never wired in.

**Not covered:** the general case.  A row of numbers is a claim, and this
repository has no mechanism that treats it as one.  The specific opportunity is
that \(F(1.18)\) per grid is exactly the kind of quantity rule 14 exists for;
the cost is 23 s added to every gated SSV-I build, since `gate_values`
re-runs the instruments.

**The tell to watch for:** the same quantity printed with two different
precisions in the same paper (`4.4` in prose, `4.15`/`4.42` in a table).  A
rounded restatement is where a superseded run survives.

## FM22 — a project-specific quantity occupies a standard symbol

**Observed:** `\mu_0` denoted vacuum permeability in two Maxwell sectors, but
the SSV scale \(m_e/\alpha\), the energy \(m_ec^2/\alpha\), and a
cutoff-dependent line tension elsewhere.  Paper I therefore gave one spelling
three dimensions, including two dimensions inside the same paper.  The reduced
proton Compton wavelength \(\hbar/(m_pc)\) was also called \(a_p\), hiding the
standard distinction between \(\lambda_p\) and \(\bar\lambda_p\).

**Why the first guard missed the fix:** the initial #213 convention registry
successfully *reported* the collision, then whitelisted it as known.  Recording
a non-standard spelling prevented new drift but left every reader to resolve
the old ambiguity.  This was a negative result about the infrastructure: a
collision inventory is not a notation policy.

**Guard — partial.** The papers now use \(m_\star\) for mass,
\(E_\star=m_\star c^2\) for rest energy,
\(\varepsilon_{\rm line}\) for line tension, and
\(\bar\lambda_p\) for the reduced Compton wavelength.  The #213 build gate
reserves `\mu_0` for permeability and rejects the legacy `a_p` spelling.
The census preserves the bar accent, and declaration tests require the cited
source line itself to contain the declared symbol so insertions cannot leave a
plausible but stale line anchor.

**Not covered:** there is no universal one-symbol dictionary across all
physics.  \(S\) for action or entropy, \(a_0\) for the Bohr radius or MOND
acceleration, and \(\Lambda\) in QFT or cosmology are established
domain-specific uses.  The registry accepts those and still reports 100+
shared tokens awaiting semantic declaration.  Passing the reserved-symbol
gate is not certification of every letter in a paper.

## FM23 — a control kernel is reported as if it came from the measured data

**Observed:** #166 sub-calculation 4 described
`G_2(k)=1/Pi_2(k)` as the screen-derived bulk response, but its propagation
path never used the measured `Pi_2`.  It inverted `khat2(L)`, verified the
known `1/r^2` Green function and promoted that control to “bulk TT follows from
the screen state.”  The measured polarisation entered only the unrelated scalar
`min(abs(Pi_2))`.

**Guard — closed for this path.**
`reconstruction_audit.py` inspects the actual kernels passed to
`greens_function`, while a blind-null control proves that the harness
distinguishes massless and gapped kernels when supplied data really enter the
inversion.  `test_subcalc4_t2_does_not_invert_measured_screen_polarisation`
freezes the negative finding, and the old instrument now prints
`CONTROL ONLY`.

**Not covered:** this is not general dataflow analysis.  A different instrument
can still compute the right-shaped observable from a fixture, prior or analytic
ansatz while describing it as measured.  Every load-bearing output needs the
question “which input changes this number?” during review.

## FM24 — a physical crossover length is silently replaced by a mass

**Observed:** #166 sub-calculations 1–3 called a massive free scalar with
`m approximately 1/xi` “SSV-like” and inferred Yukawa stress, induced
`1/G proportional to 1/xi^2`, and massive-screen modular behavior.  Corrected
SSV is gapless:
\(\omega^2=c_s^2k^2(1+\xi^2k^2)\).  Its healing length controls the
\(k^2\)-to-\(k^4\) crossover; it is not a mass gap.  The surrogate changed the
infrared theory rather than approximating it.

**Guard — closed for these batteries.** The old scripts and receipts now label
their surviving massive-scalar mathematics as controls.  The replacement
`ssv_disk_modular.py` encodes the gapless corrected dispersion directly in two
screen dimensions, and
`test_dispersion_is_gapless_ssv_crossover_not_massive_yukawa` prevents the same
substitution there.

**Not covered:** the 2+1D Gaussian screen is itself a candidate, not a derived
restriction of the full 3+1D SSV state.  Matching a dispersion does not provide
the still-missing horizon algebra or bulk–screen encoding map.

## What runs when

`python instruments/tools/build_paper.py <PAPER>` runs FM1, FM2, FM5's evidence
structure and the rule-11 reference check before `pdflatex`, and refuses to
publish a PDF if any fails. FM4 runs in the test suite. The semantic half of FM5
and FM6–FM7 still run in a reviewer's head, which is exactly why they are the
ones most likely to lapse.

| FM | guard | runs at |
|---|---|---|
| FM1 number drifts from instrument | rule 14 chain | build + suite |
| FM2 reviewed result drifts after number moves | `claims.py` | **build** + suite |
| FM3 check that isn't checking | negative controls | suite (partial) |
| FM4 symbol with two dimensions | `dimensions.py` | suite |
| FM5 misattributed citation | rule 12 | **build** (structure) + review (meaning) |
| FM6 unbacked absence claim | rule 13 | review |
| FM7 suppressed falsification | rule 1 + gapbox | review |
| FM8 checker over-reports | anchored/free split | suite (this case only) |
| FM9 citation metadata points at wrong work | `verification.json` | **build** + review |
| FM10 duplicated bibliographies drift | `references.bib` + `bibliography.py` | **build** |
| FM11 cited work absent from review inventory | citation-note catalog | **build** |
| FM12 generated artifact churns across environments | `RECEIPT_SIGFIGS` rounding | suite (one receipt only) |
| FM13 constant labelled with a provenance it lacks | read the source receipt, don't retype | suite (one instrument only) |
| FM14 sweep omits the axis the conclusion turns on | `b1_fragility_report` + claim guard | **build** (this verdict only) + review |
| FM15 paper narrates its own edit history | phrase deny-list + per-paper `CHANGELOG.md` | **build** (phrasing only) + review |
| FM16 deterministic green called semantic verification | v2 verdict boundary | suite + review |
| FM17 generator assumes non-empty inputs | zero-reference provenance test | suite |
| FM18 observation inverted into prediction | explicit input/status receipts | review (partial) |
| FM19 correction misses dependent papers | shared-value registry + dependency search | **build** (registered values) + review |
| FM20 necessary diagnostic promoted to sufficient | status-bearing receipt | suite (this result) + review |
| FM21 table row and prose from different runs | generated macro + old-literal rejection | **build** (registered values only) |
| FM22 project quantity occupies standard symbol | `conventions.py` reserved-symbol gate | **build** (reserved spellings) + suite |
| FM23 control kernel reported as measured response | reconstruction dependency + blind-null audit | suite (this path) + review |
| FM24 crossover length replaced by a mass | corrected-dispersion test + scoped receipts | suite (these batteries) + review |

Adding a failure mode to this register is cheap. Leaving one out because its
guard is embarrassing is how #182 happened.

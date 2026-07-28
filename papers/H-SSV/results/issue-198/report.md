# #198 — structural prevention: generated numbers, typed dimensions

Status: **closure-grade** · Branch `agent/issue-198-generated-values` · 2026-07-28

Follow-up to #182, whose one-line summary was *"The computations were sound. The
write-up was not."* Not one defect was found in the numerical corpus across
twelve papers; every defect was in prose, a citation, or an algebraic step in the
text. Both measures below attack that gap directly. Neither failure mode was
structurally closed before this pass — both could recur.

---

## Part A — printed numbers are generated, not typed

### What was built

| artifact | role |
|---|---|
| `instruments/tools/gen_values.py` | registry → `papers/<PAPER>/values.tex` |
| `instruments/paper_vii_b/planck_scale_values.py` | new: VII-b had no instrument for this sector |
| `instruments/test/tools/test_gen_values.py` | 21 tests |
| `instruments/test/paper_vii_b/test_planck_scale_values.py` | 19 tests |

Seven values, the load-bearing ones touched by #182:

| macro | paper | prints | from |
|---|---|---|---|
| `\ssvLambda` | I | `5.25` | `lambda_param()` → 5.2496852 |
| `\ssvRhoZero` | I | `9.96×10⁻⁵` | `rho0_natural_units(sqrt2_corrected=True)` → 9.9590365e-5 |
| `\ssvReStar` | I | `3.74×10⁻¹¹` m | `xi_over_alpha(sqrt2_corrected=True)` |
| `\ssvEllP` | VII-b | `1.616×10⁻³⁵` | `planck_length()` |
| `\ssvMZero` | VII-b | `1.539×10⁻⁸` | `fundamental_mass()` |
| `\ssvMPlanck` | VII-b | `2.176×10⁻⁸` | `planck_mass()` |
| `\ssvGNewton` | VII-b | `6.67×10⁻¹¹` | `G_NEWTON` (CODATA) |

All seven reproduce the literals already in print, so **this pass changes no
physics.** Deliberately not generated: the historical values (`1.9`, the `~2×10⁴`
ratio). They record what was once printed, not derived quantities; generating
them would misrepresent what they are.

### The acceptance test, pre-registered and run

A generator that nobody can break is decoration. Both mechanisms were tested on
the real file loop:

1. **Perturbed** `lambda_param` by `+0.1`. The suite went red
   (`test_values_tex_is_not_stale`), and after regeneration the paper's printed
   number moved `5.25 → 5.35`. Restored.
2. **Re-typed** the literal `5.25` into the prose beside its own macro.
   `test_replaced_literal_is_gone` fired. Reverted.

The second is the test that closes the issue. The other four keep `values.tex`
correct; only that one stops a second, hand-typed copy of a number reappearing
in the prose — which is precisely how `ρ₀` came to be printed as `1.9` beside a
formula yielding `0.0078`.

### Defects found

**A-D1 — SSV-VII-b printed the same quantity two ways.** `main.tex:530` gave
`1.6×10⁻³⁵` where `:390` gave `1.616×10⁻³⁵` for ℓ_P. Predicted by the
pre-registered falsifier; the macro collapses them. Consequence nil, but it is
the exact drift the mechanism exists to prevent, sitting in a paper that had
already passed the audit.

**A-D2 — two comparator bugs in my own first draft of the VII-b tests**, both
caught by the negative controls. `mp.almosteq(a, b, rel_eps=…)` defaults
`abs_eps` to `rel_eps`, so for quantities of order 1e-35 *every* assertion passed
on the absolute test alone. Seven tests were green and proved nothing. Replaced
with an explicit relative comparator, itself guarded by
`test_rel_close_is_not_trivially_true`. Recorded because it is the same failure
mode as the one the issue is about: a check that looks like it is checking.

---

## Part B — dimensions are typed

`instruments/tools/dimensions.py` + `instruments/test/tools/test_dimensions.py`
(22 tests). Scope pre-registered as SSV-I, SSV-II and SSV-V — the three papers
where a dimensional defect was actually found.

### The question it asks

Symbols are **anchored** (dimension fixed by definition — `hbar` an action, `c` a
velocity, `rho` a mass density) or **free** (introduced without being pinned —
SSV-I's `b`, SSV-II's `e`). The check is:

> Is there **any** dimension for the free symbols making all of the paper's
> printed relations simultaneously homogeneous?

When there is not, the defect is established without arguing which equation is
"the wrong one", and because the free symbol is the only unknown, attribution is
automatic rather than a judgement call.

### Results — all three known defects reproduced

| paper | symbol | requirement | verdict |
|---|---|---|---|
| SSV-I | `b` | `eq:pot` → L²T⁻²; `eq:cs`, `eq:xi`, `eq:brho0` → L⁵T⁻² | **no consistent assignment** (E6), gap exactly L³ |
| SSV-II | `e` | `eq:berry_ab` → mass; `eq:flux_quantum` → charge | **no consistent assignment** (E3b) |
| SSV-II | — | `eq:flux_quantisation` contains no free symbol | **unrepairable** by any redefinition of `e` (E3d) |
| SSV-V | `b` | `eq:cs` → T⁻¹ | consistent; differs from Paper I's `b`, and is now declared (E2) |

`test_known_defects_are_detected` is the load-bearing test. A green suite over
corrected relations proves nothing about whether the checker can see anything; a
suite that reproduces three known failures has demonstrated it can see the class.

### Defect found — in a paper that had already passed the gates

**B-D1 — SSV-II's item (iv) printed two wrong dimensions.** The falsification box
at `main.tex:870` stated that `c_⊥ρ_⊥κ₀` has dimensions `M T⁻³` against
`M L² T⁻²` for `h`. Both are one power of `T` out:

* `c_⊥ρ_⊥κ₀ = (L/T)(M/L³)(L²/T) = **M T⁻²**`
* `h` is an **action**, `M L² T⁻¹` — the printed `M L² T⁻²` is an *energy*

Because both errors run the same direction, the **mismatch** they are quoted
between — `L⁻²T⁻¹` — is correct, and it is the mismatch the argument rests on.
So the conclusion stands: flux quantisation does not follow, and
`flux_quantisation_consistent()` returns `False` for the right reason. The
defect is presentational, and it survived the C-gate, the E-gate, the N-gate and
the #184 rewrite.

Corrected in `papers/SSV-II/main.tex` and in the `ssv_ii_ab_audit_2026.py`
docstring. **This is the single best argument for Part B**: it was found by
running the checker over a paper already declared clean, and no gate had asked
the question that exposed it.

### An error in the first draft of the checker, and why it is recorded

The first version reported `hbar`, `m_0` and `kappa_0` as overloaded alongside
`b` and `e`. They are not. They appeared only because they sit inside relations
broken by a *different* symbol, and solving a broken relation for a healthy
symbol yields nonsense. Reporting that nonsense as a finding would have been a
false positive of exactly the kind rule 1 exists to prevent — inflating a real
defect into a larger one. The anchored/free split was introduced to fix it, and
`test_solving_for_an_anchored_symbol_is_refused` now makes the mistake
unrepeatable.

### The honest limit

**This does not check the `.tex`.** It checks the relations *as transcribed into
the module*, so it proves the intended dimensions are consistent, not that the
paper matches them. A relation mis-transcribed here is invisible to it. Every
`Relation` therefore carries the `site` it came from, so the transcription is
checkable by hand even though it is not checked by machine — and
`test_relation_sites_exist` keeps those pointers live.

Scope was capped at three papers deliberately. Transcribing all twelve by hand
would be a large manual operation with a real chance of introducing the very
error class the tool exists to catch.

---

## Part C — absence claims carry their search

Already landed as **rule 13** in `CLAUDE.md` (commit `911d543`), together with
rule 12. Nothing further owed.

---

## Verification

* full suite on the finished branch: **527 passed, 1 skipped** (306 s). This
  issue contributes 62 of them — 40 from Part A, 22 from Part B — against a
  pre-#198 baseline of 465.
* SSV-I, SSV-II, SSV-VII-b: clean 2-pass `pdflatex`, 0 errors, no new undefined
  references (rule 8); PDFs moved to `papers/pdf/` (rule 3)
* provenance regenerated for the papers touched (rule 11)

## What is *not* closed

* Part A covers seven values. Every other printed number in the series is still
  typed. The mechanism exists and extending it is cheap, but the extension has
  not been done and should not be assumed.
* Part B covers three papers and the relations transcribed for them — a small
  fraction of the series' equations. It cannot see a relation nobody typed in.
* Neither part addresses the citation half of the #182 defect class; that is
  rule 12's evidence rule, which is a convention rather than a test.

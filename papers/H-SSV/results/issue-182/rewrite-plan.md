# Series rewrite — pre-registered plan

Branch: `agent/series-rewrite-2026` · opened 2026-07-27 · follows #182's audit
Owner decisions recorded: **one branch for the whole rewrite**; **SSV-VII-a's
topological replacement deferred to its own branch, after this one**.

This is an **editing pass**, not a research pass. Every item below was
established by the #182 audit; none requires new physics. Where an item cannot
be repaired by editing, it is flagged and left — it is not quietly softened.

## Decision rule (pre-registered)

An item is **done** when all four hold:

1. the printed text matches the audited finding, with no residual claim that the
   audit rejected;
2. the paper's own claim-status table carries the change (rule 5) — or, for
   papers without one, the change is stated in the status/abstract block;
3. the negative is stated as a negative (rule 1) — no softening to "less
   certain", no silent deletion;
4. `pdflatex` twice: 0 errors, no *new* undefined references (rule 8).

An item is **blocked** if repairing it requires a result the series does not
have. Blocked items get an honest interim status entry and are named in the PR —
they do not get a plausible-sounding substitute.

## Scope correction to the audit

The #182 decision says the falsified Bjerknes mechanism is presented as current
in "SSV-I, SSV-IV and SSV-VII-b". **SSV-IV is clean** — `main.tex:54` carries an
explicit *"Status change (issue #119, 2026-06) … falsified as written"* and
`:480` restates the trilemma. Only **SSV-I:1242** and **SSV-VII-b:202** state it
without caveat. The decision file will be corrected in this pass.

Conversely the rewrite must touch two papers whose issues are **closed clean**,
because the D1 sign is a *definition* that propagates:

- **SSV-III:1169** prints $V(\rho)=-b\rho[\ln(\rho/\bar\rho)-1]+V_0$, attributed
  to Paper I.
- **SSV-IV:494** and **SSV-VII-b:44,187** use $b\ln(\rho/\rho_0)$ — sign to be
  checked against the adopted branch, not assumed.

Inventory of printed potential forms, from the pattern
`ln(\rho/\bar{\rho})` / `ln(\rho/\rho_0)` over `papers/*/main.tex`: SSV-I
205/245/251/277, SSV-III 1169, SSV-IV 494/503, SSV-V 142/629/633, SSV-VII-b
44/187 — **12 sites in 5 papers**.

> **Correction (2026-07-28).** This originally read "**No others.**" That claim
> was false. A wider pattern (adding `\ln\rho`, `\log\rho`, `\ln{\rho}`)
> finds a **13th** site: SSV-II `main.tex:2664`, the magnon effective potential
> $V+b\ln\rho_b=\mu$. The consequence was nil — that site already carries the
> adopted sign, like SSV-VII-b — but the completeness claim was unverifiable as
> stated, and a pre-registration is the worst place for one. Corrected per the
> new rule 13; see \#198 Part C.

## Sequence and per-paper items

### 1. SSV-I (#183) — the largest pass; items share passages, so one edit

| # | site | action |
|---|---|---|
| D1 | 205, 234, 245, 251, 277 | flip to $V=+b\rho[\ln(\rho/\bar\rho)-1]+V_0$; drop the Volovik attribution for the log EOS/LogSE (lineage: Rosen → Bialynicki-Birula & Mycielski → Zloshchastiev); state the constraint as $\rho|F'(\rho)|=mc_0^2$ |
| D1b | 280–284 | **delete** the thermodynamic-vs-Bogoliubov discrepancy *and its resolution* — both are artifacts; $\rho\mu'$ is constant so the routes agree identically |
| D1c | 291, 297 | $c_s=c$ exactly; $\xi=\hbar/(\sqrt2 m_0c)$ |
| E3 | 470–487 | remove the doubled $\alpha^2$ in `eq:Etotal`; as printed it stationarises at $r^*\approx0.57$, not $1/\alpha$ |
| E4 | 492–495 | $\xi/\alpha$ is the **Bohr radius**, not the classical electron radius |
| E5 | 502–512 | $\rho_0=\alpha m_e^4c^3/(2\pi^2\Lambda\hbar^3)$; remove the two inconsistent statements |
| D2 | 618 | withdraw "Y-junction of three quantized vortex filaments"; the object is the single-curve trefoil $T_{2,3}$; drop `faddeev1997` for the junction claim. $N_Y=3$ **survives** as the crossing number |
| B | 1242 | attach the #119 falsification; drop `zloshchastiev2023` from that sentence |
| E1 | appendix | the elliptic residual is $3/16$ with a logarithm, not a "pure geometric constant" $1/8$; the appendix's $-2$ is a filament core, Lamb's $-7/4$ a uniform-vorticity core — different models, so the appendix does not "recover eq:Ekin" |

`eq:Ekin`'s $-7/4$ is **correct** and stays (Lamb Art. 163 (6), verbatim in
`papers/cited/transcripts/lamb1932.md`).

### 2. SSV-II (#184)

| # | site | action |
|---|---|---|
| E1 | 508 | `eq:maxwell` carries the #138 status **at the point of statement**, or moves to the historical-record subsection; withdraw `Barcelo` and `Volovik` for it |
| E3 | 782–869 | withdraw `eq:AB_SSV` and `eq:flux_quantisation`; withdraw the `HaldaneWu1985` citation; **retain** the qualitative claim ($\mathbf A=\mathbf v_s$ is a physical flow) re-cited to Volovik 2001 §XII A eq. (311), noting the analogue phase is energy-dependent |
| E2 | 303 | $\xi\to\hbar/(\sqrt2 m_0c)$ |
| — | 3258 | `Villois`/`Villois2017` duplicate keys — merge |

### 3. SSV-III (#185, closed clean) — definition propagation only

`main.tex:1169`: sign of the quoted Paper-I potential. **No other change.** The
#137 T-symmetry conclusion is unaffected (the potential is conservative on either
sign).

### 4. SSV-IV (#186, closed clean) — check only

`main.tex:494,503`: confirm $b\ln(\rho/\rho_0)$ against the adopted branch.
Bjerknes passages are already honest — **no edit**.

### 5. SSV-V (#187)

| # | site | action |
|---|---|---|
| E1 | 629–650 | **withdraw Argument 1.** Under the adopted branch $\mu\to-\infty$ as $\rho\to0$: no chemical-potential floor, no confining inward pressure. This is a sign reversal, not a weakening. State whether the remnant survives on Arguments 2+ — and if that is not settled, say so |
| E2 | 142 | disambiguate $b$: SSV-V's $b$ is a **frequency**, Paper I's is an **energy**. Not an error, but undeclared |

### 6. SSV-VII-a (#189) — interim status only

The Gausson does not exist on the adopted branch and the $\hbar/2$ is imported
on either branch. **No repair is attempted in this branch** (owner's decision:
topological replacement, separate branch, afterwards).

This pass adds an **interim status block** to §"Saturation by the Gausson"
stating both findings plainly. Leaving the section printed as current while the
replacement is researched would reproduce the exact falsification-suppression
defect found in SSV-I — so the repair waits, the honesty does not.

### 7. SSV-VII-b (#190) — the only recomputation

| # | site | action |
|---|---|---|
| E1 | 315, 362 | **recompute** horizon counting with $\xi=\hbar/(\sqrt2 m_0c)$: quantities $\propto A_H/\xi^2$ move by **2**, $\propto1/\xi$ by $\sqrt2$. The only place the D1 $\sqrt2$ reaches a stated number |
| E2 | 202 | attach the #119 falsification to `eq:Bjerknes` |
| — | 144 | **no change** — this paper had the sign right all along |

## Out of scope (named, not forgotten)

- SSV-VII-a's actual repair — next branch.
- The **solver-track √2**: canonical `log_pressure=0.5` implies $c_s=1/\sqrt2$
  while 46 scripts declare $c=1$. Changes no result in $\xi$-units; likely the
  same $\sqrt2$ as D1. Flagged in the N-gate, not verdicted, not touched here.
- The **physics gaps**: #180 K3 for the printed theory, and the multi-component
  requirement that #178 and D2 independently indicate. Neither is an editing
  matter.
- Remaining `PENDING-PRIMARY` sources — none load-bearing.

## Verification, per paper

1. `python instruments/tools/gen_provenance.py <PAPER>` (rule 11)
2. `pdflatex` ×2 — 0 errors, no new undefined refs (rule 8)
3. move/rename the PDF into `papers/pdf/` (rule 3)
4. `pytest instruments/test/` green before the PR
5. commit per paper, `#NN` prefixed, `Co-Authored-By` trailer (rule 9)

## Where I will stop and ask

- If withdrawing SSV-V's Argument 1 leaves the Planck-remnant conclusion with no
  support at all — that is a claim-status change, not an edit.
- If the SSV-VII-b recomputation moves a **published number** rather than an
  intermediate.
- If any repair would require asserting something the audit did not establish.

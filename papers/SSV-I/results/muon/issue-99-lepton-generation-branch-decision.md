# Issue #99 decision: the post-#78 lepton-generation branch

**Issue:** [#99](https://github.com/StigNorland/SVT/issues/99) — decide whether the
lepton-generation programme continues through an HQV branch, a spinorial/CP¹
branch, or is retired/demoted after #78.

**Decision: OUTCOME 3 — RETIREMENT / DEMOTION.** Scalar (and spinor) SSV makes
**no derivation claim** about charged-lepton generations. The muon and tau masses
are recorded **numerical coincidences** with no deriving mechanism. The generation
ladder is not reopened until a *genuinely new* order-parameter structure (beyond
the CP¹/spinor upgrade already adopted) is introduced.

This is the strongest form of outcome 3: the two escape hatches #99 lists as
candidate branches were **not merely scoped and held — they were opened, computed,
and closed negatively** between 2026-06-05 and 2026-06-06. Neither is pending.

---

## Why this is forced, not chosen

When #99 was written (2026-06-05) the HQV and spinor branches were open scoping
memos (Task A / Task B of #78). The follow-on work actually pursued **both** and
both came back negative:

| Branch | Issue(s) | What was tried | Verdict |
|---|---|---|---|
| Spinorial / CP¹ | #83 → #87 → #91 | Adopt CP¹ order parameter; compute the SU(2)-covariant `L_⊥` muon bridge on the IQV electron | **CP¹ adopted** (for spin/chirality), but muon bridge `\|V\|=0` exactly → `γ_B=0` → muon NOT derived |
| Half-quantum vortex | #94 | Electron as a single HQV carrying `γ_B=π` | **REJECTED** — the HQV's `π` is *meridional* (= the electron's spin-½, wrong circle); the major-circle loop gives `γ_B=0`; a free HQV is charge-excluded |
| Static minima (Route C) | #78 | Generations as distinct relaxed static minima; energy ratio = mass ratio | **FAIL** — `E(8ξ)/E(1ξ)=3.71`, not 206.77 |
| Kelvin `8ⁿ` shell (Route D) | #78 | `8ⁿ` ladder as a closed-shell degeneracy | **REFUTED** — `q=8.587` is C-independent; the ring has U(1), not SO(3); no magic-number 8 |

The pivotal point from #91/#94: **the CP¹/spinor upgrade was the right move for
other reasons and it was made** (it derives the lepton spin-½ as the meridional
ℤ₂ framing, the chirality/charge sign, and the connected SU(4) of #84). It simply
does **not** derive the muon. Adopting the spinor field therefore does **not**
reopen the generation question — it is the structure that *closed* it. So there is
no further "spinor branch" left to open: it has been exercised to exhaustion.

## The #99 tasks, answered

- **What scalar (and spinor) SSV no longer claims about lepton generations:**
  nothing is derived. The muon `(3/2)μ₀` (0.59%) and tau `25½ μ₀` (0.49%) are
  numerical coincidences; the `8ⁿ`/closed-shell ladder is a ~5–7% numerical
  curiosity, not a degeneracy law. Generations are *not* breathing eigenmodes
  (BdG null), *not* distinct static minima (Route C), *not* mode-shell closures
  (Route D), *not* a spinor-BdG winding sector (#91), and *not* half-windings
  (#94).
- **Minimal structure for an HQV branch:** a ℤ₂/CP¹ internal label so a π phase
  winding is screened by a π internal rotation. This is *identical* to the spinor
  structure (Task A = Task B). It was added (#83/#87) and the HQV it produces is
  the *meridional* spin-½, not an azimuthal muon Berry phase (#94). No separate
  HQV branch survives.
- **Minimal structure for a spinorial/CP¹ branch:** promote Ψ to a 2-spinor with
  CP¹ ≅ S² direction n̂. This *was adopted* (#83/#87). Result for the muon: `|V|=0`
  on the uniform-n̂ IQV (#91). No muon.
- **Cost to Papers I–II of the structure that was added:** the CP¹ upgrade was
  paid for and the re-derivations (`α`, `R_e=ξ/α`, Madelung, Goldstone safety,
  pion`=2μ₀`) were re-established under #87 (results in
  `papers/SSV-I/results/spinor/`). The cost bought spin-½ + chirality, **not**
  generations.
- **Open a new computation issue, or retire?** **Retire.** No first-principles
  route remains in the current (scalar *or* spinor) order-parameter manifold. A
  new generation issue should be opened only if a *new* structure (beyond CP¹) is
  introduced for an independent reason.

## Failed, not pending — the closure ledger

Every charged-lepton-generation route is **closed negative**. None may be cited as
"pending," "in progress," or "candidate":

- Path A (statistics): ladder is two-coincidence numerology — FALSIFIED as a derivation.
- Path B (reduced-basis BdG): `0.207` hit is a truncation artifact — FALSIFIED.
- #73 (direct φ-sector BdG): lowest branch `0.50–0.59`, no muon — NULL.
- #76 (scalar Berry phase): `γ_B=0` by selection rule — NO-GO.
- Route C (#78 static minima): ratio 3.71 — FAIL.
- Route D (#78 `8ⁿ` shell): U(1)≠SO(3), `q=8.587` C-independent — REFUTED.
- #91 (spinor-BdG IQV bridge): `|V|=0` exactly — CLEAN NO.
- #94 (HQV electron): wrong circle + charge-excluded — REJECTED.

**The muon question is in its final state.** SSV's mass derivations are the
topological ones only — pion `= 2μ₀` (winding), proton `N_Y = 3` (crossing
number). The charged leptons above the electron, the kaon, and the ρ are recorded
coincidences.

## Documents updated with this decision

- `notes/volovik-mapping.md` — divergence section corrected (spinor/HQV tried,
  not pending); closed-shell section already marked REFUTED.
- `papers/SSV-I/main.tex` — abstract tightened so the HQV/spinor branches read as
  closed (#91, #94), not as the open path; §muon and claim-status already record
  the coincidence with no surviving derivation.
- `notes/next-issues.md` — #99 moved out of open follow-ups.

## References

- `papers/SSV-I/results/muon/muon-bdg-nogo-summary.md` — scalar BdG no-go
- `papers/SSV-I/results/muon/route-c-generation-minima-result.md` — Route C FAIL
- `papers/SSV-I/results/muon/route-d-kelvin-degeneracy-result.md` — Route D REFUTED
- `papers/SSV-I/results/muon/muon-task-a-spinor-scoping-memo.md` — Task A scope
- `papers/SSV-I/results/muon/muon-task-b-hqv-scoping-memo.md` — Task B scope
- `papers/SSV-I/results/spinor/b1-winding-regime-result.md` — #91 `|V|=0`
- `papers/SSV-I/results/spinor/hqv-muon-verdict.md` — #94 HQV rejected

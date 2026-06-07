# Spec — left–right-symmetric SU(4) LogSE: the field, the functional, and the pre-registered chirality test (#81 Milestone 1, 2026-06-05)

**Issue:** [#81](https://github.com/StigNorland/SVT/issues/81) (sequel to #80).
**Status: SPEC ONLY — no solver yet. Written before coding, per the issue mandate.**

This note fixes, *before any 3D field build*, four things: (1) the order-parameter
field and its target manifold; (2) the energy functional, including the explicit
generalised `L_perp` chiral-shear term that is the **only** place the chirality ℤ₂
can be dynamically locked; (3) the single-defect ansatz carrying the five #80 bits
and the four `(P_c, P_w)` sectors; (4) the **pre-registered decision rule** for
the one open question. It also pins a cheap reduced-model gate to run *before*
committing to full 3D, per the project's sensitivity-gate habit.

## 0. The one question (restated, sharp)

#80 closed with: one Standard-Model generation = one defect **+ one ℤ₂ postulate**
("chirality = the spin framing"). Topology *permits but does not force* the
diagonal ℤ₂ `P_c = P_w` over the vector-like product (the 32). The dynamical
question this build decides:

> Does a minimal **left–right-symmetric** multi-component LogSE make the diagonal
> sector (`P_c = P_w`, the chiral 16) the **unique lowest-energy single defect** —
> or are the four `(P_c, P_w)` sectors degenerate (vector-like 32)?

- **FORCED** → SSV *predicts* chirality (origin of the chiral weak force).
- **NOT FORCED** → the postulate stands as SSV's one irreducible fermion-sector input.
- **WRONG-SIGN** (locking favours the anti-diagonal) → falsification of the naive
  `L_perp` sign; the scalar core's chiral term would carry the wrong handedness.

All three are publishable outcomes. The rule (§5) is fixed here, before runs.

## 1. The order-parameter field

The scalar SSV defect is `psi : R^3 -> C`, vortex where `psi = 0`, charge = winding
of `arg psi`. We generalise `C -> ` an internal multiplet, keeping the *same*
amplitude/phase + log-potential skeleton and generalising `L_perp` (§3).

The #80 target manifold (manifold-scan + Pass 6/7) is

```
overall U(1)  ×  SU(4) colour (incl. B−L = 4th colour)  ×  CP¹ weak (SU(2)_L + framing),
                                                          left–right symmetric.
```

We realise it with **two complex multiplets plus the overall phase**, chosen so the
five #80 bits `(c1,c2,c3,w1,w2)` are *windings/parities of field components*, exactly
as in the junction picture of #79/#80 (Cartan = relative phase windings):

| field | space | carries | #80 bits |
|---|---|---|---|
| `z` | `C^4` (fundamental **4** of SU(4)) | colour incl. B−L, via the 4-valent junction | `c1,c2,c3` (relative-phase windings; `B−L` = trace direction) |
| `χ_L` | `C^2` (doublet of SU(2)_L) | left weak isospin + spin framing | `w1−w2 = T3_L` |
| `χ_R` | `C^2` (doublet of SU(2)_R) | right weak isospin | `w1+w2 = T3_R` |
| `e^{iθ}` | `U(1)` | overall phase / mass winding | — |

**Left–right symmetry** is the involution `χ_L ↔ χ_R` together with colour
conjugation `z -> z̄` (the **4 ↔ 4̄** of Pass 6). The functional (§2–3) must be
*exactly* invariant under it; that invariance is what makes the chirality result a
genuine prediction rather than a tuned input.

The two ℤ₂ parities that #80 isolated, in field terms:

- **`P_c` (colour parity, 4 vs 4̄):** the sign of the SU(4) sector under conjugation
  `z -> z̄` on the defect — i.e. whether the colour junction winds as the **4** or
  the **4̄**.
- **`P_w` (weak/spin parity, L vs R):** which of `χ_L`, `χ_R` carries the defect's
  weak winding — i.e. whether the spinor framing is left- or right-handed.

`(P_c, P_w) ∈ ℤ₂×ℤ₂` ⇒ four sectors of 8 on the 32; **diagonal `P_c = P_w` = the 16**
(reproducing `pati_salam_16_unification.pati_salam_decomposition`). The solver's
sector measurement (§4) **must** reproduce that map on a relaxed configuration.

> **Reduction used for the first build (the cheap gate, §6):** the full
> `C^4 × C^2 × C^2 × U(1)` field is heavy. The chirality question depends *only* on
> the relative `(P_c, P_w)` and the cross-coupling between the colour and weak
> sectors. So Milestone 2 first builds the **minimal locking model**: one colour
> phase carrying `P_c` (a single complex `ψ_c` whose conjugation = 4↔4̄) × one weak
> spinor carrying `P_w` (`ψ_w`), with the §3 cross term. If *that* shows no locking,
> the full SU(4)×SU(2)² cannot lock either (the extra components only add
> degeneracy, not coupling) → NOT-FORCED is already decided cheaply. Only a
> *positive* cheap result promotes to the full multiplet build.

## 2. The energy functional (amplitude / phase + log potential)

Per component, keep the scalar skeleton (`xi=1, rho0=1, c=1`):

```
E_local[Φ] = ∫ d^3r [ Σ_a ½|∇Φ_a|²  +  p · V(ρ)  +  (L_perp term, §3) ]
ρ = Σ_a |Φ_a|²        (total condensate density over all components)
V(ρ) = ρ ln ρ − ρ + 1   (the LogSE log-potential, p = log_pressure, canonical 0.5)
```

This is the direct multi-component lift of
`trefoil_observables.energy_density`: `½|∇ψ|² + p(ρ ln ρ − ρ + 1)`, summed over
components with a **single shared `ρ`** so all sectors share one condensate (one
defect, not several independent ones). The `U(1)` phase rides on the overall phase
of the multiplet as before. **Nothing in `E_local` couples `P_c` to `P_w`** — it is
parity-blind by construction. That is the point: if locking happens, it is *only*
through `L_perp`.

## 3. The generalised `L_perp` — the sole ℤ₂-locking locus

Scalar SSV (`lperp_helpers`): `E_perp = (λ⊥/2)∫|∇×j|²`, `j = Im(ψ*∇ψ)`. The
multi-component lift defines a **sector current per sector**:

```
j_c = Σ_{a∈colour} Im(z_a* ∇ z_a)          (colour/SU(4) current)
j_w = Im(χ_L† ∇ χ_L) − Im(χ_R† ∇ χ_R)      (weak current, LR-odd by construction)
ω_c = ∇×j_c ,   ω_w = ∇×j_w
```

The LR-symmetric chiral-shear energy, to the lowest order that respects the
involution `χ_L↔χ_R, z->z̄`, has **three** terms:

```
E_perp = (λ_c/2)∫|ω_c|²  +  (λ_w/2)∫|ω_w|²  +  λ_cw ∫ ω_c · ω_w
                                                  └──────────────┘
                                                   the locking term
```

- The two diagonal terms are parity-blind (depend on `|ω|²`), like the scalar one.
- **The cross term `λ_cw ∫ ω_c·ω_w` is the whole game.** Under flipping `P_w` alone
  (L↔R on the weak sector, `χ_L↔χ_R`), `j_w -> −j_w` so `ω_w -> −ω_w`, hence
  `ω_c·ω_w -> −ω_c·ω_w`. Under flipping `P_c` alone (`z->z̄`), `j_c -> −j_c`,
  same sign flip. Under flipping **both** (the diagonal move), the cross term is
  **invariant**. So `E_perp` is degenerate between `(P_c,P_w)` and `(−P_c,−P_w)`
  (the two diagonal members) and between the two anti-diagonal members, but the
  cross term **splits diagonal from anti-diagonal by `2λ_cw ∫|ω_c·ω_w|`.**

This is precisely the structure needed: the sign of `λ_cw` decides whether the
**diagonal** (chirality 16) or the **anti-diagonal** is the ground state, and
whether `λ_cw` is forced nonzero (by the natural SSV chiral-shear coupling) decides
whether locking happens at all.

**Two questions, then, are decidable:**

1. **Is `λ_cw` forced nonzero by SSV's own chiral-shear structure**, or is it a free
   knob that symmetry allows to be zero? (Derivation question — the natural
   coupling is `λ⊥ ~ α^{-2}` per `lperp_core_integral`; whether the *cross* term
   inherits it, or vanishes by an extra selection rule like the #76 `m_a+m_b=0`
   null, is the analytic crux. **Pre-register: we test the generic `λ_cw ≠ 0`
   case first; a vanishing cross matrix element is itself the NOT-FORCED verdict,
   mirroring the #76 Berry-phase null.**)
2. **Given `λ_cw ≠ 0`, does the relaxed-defect energy gap survive convergence** and
   point to the diagonal (not anti-diagonal)?

## 4. Single-defect ansatz and sector measurement

**Ansatz.** Reuse the trefoil/ring imprint machinery (`initial_state`,
`coordinate_grid` from `trefoil_breather_static`), applied per component: a single
closed defect loop (start with an unknotted ring — the chirality question does not
need the trefoil; the trefoil is the *proton/mass* object). Imprint windings so the
five bits take a chosen `(P_c, P_w)` sector. Four imprints = the four sectors.

**Relax** each with the generalised gradient flow (§ Milestone 2), topology guard
per component, `--no-energy-gate` continuation ladder as in #77.

**Measure `(P_c, P_w)`** on the relaxed field (not the imprint — the relaxed sector
is the physical one):

- `P_c` = sign of the colour-sector winding / conjugation parity of `z` around the
  defect (4 vs 4̄), computed from the phase circulation of the colour components.
- `P_w` = sign distinguishing which weak doublet (`χ_L` vs `χ_R`) retains nonzero
  winding after relaxation.

Cross-check against `pati_salam_16_unification`: the relaxed diagonal sector must
map to one of `{Q, u^c, d^c, L, e^c, ν^c}` with the right `(B−L, T3_L, T3_R, Y)`.
This reuses the *tested* group-theory layer as an oracle for the solver.

**Compare** the four relaxed sector energies `E(P_c,P_w)`.

## 5. PRE-REGISTERED DECISION RULE (fixed before any run)

Let `ΔE_lock = min(E_anti-diagonal) − E_diagonal` (positive ⇒ diagonal favoured),
measured on the convergence-validated ladder. Let `σ_E` = max(energy drift,
inter-resolution scatter) on the same states, and `dx` the spacing.

- **FORCED (chirality predicted):** `ΔE_lock > 0` AND
  - grid-converged: `|ΔE_lock|` changes < **10%** across two regrid-continued
    resolutions (e.g. n=48→72, as in #77's 5% gate, relaxed to 10% for the cross
    term), AND
  - physical, not lattice: `ΔE_lock` does **not** scale → 0 like `dx^1` (the
    Peierls–Nabarro lesson — a lattice-pinning artifact vanishes as `dx→0`), AND
  - above noise: `ΔE_lock ≥ 5·σ_E`.
- **NOT FORCED (postulate stands):** the four sectors degenerate —
  `|ΔE_lock| < 5·σ_E` after convergence — OR `λ_cw` vanishes by a selection rule
  (the cross matrix element `∫ω_c·ω_w` is zero by the field symmetry, à la #76).
- **WRONG-SIGN (falsification):** `ΔE_lock < 0` and convergence-validated by the
  same gates — the dynamics lock the *anti-diagonal* (vector-like-favouring /
  wrong handedness). This would say SSV's chiral-shear term carries the wrong sign
  and the postulate cannot be promoted as written.

**Robustness rider (pre-registered):** the verdict must survive (i) `λ_overall`
phase coupling on/off, and (ii) at least one alternative natural value of `λ_cw`
(e.g. `α^{-2}` vs `α^{-1}`); a verdict that flips under these is reported as
**INCONCLUSIVE**, not FORCED.

## 6. Milestone plan (this issue) and the cheap gate first

1. **(this note) Spec + pre-registered rule.** ✔
2. **Minimal locking model** (`ψ_c × ψ_w` + `λ_cw ω_c·ω_w`, §1 reduction): does the
   cross term split diagonal vs anti-diagonal at all, on a single ring? **Gate:**
   if no split survives convergence here, the verdict is **NOT-FORCED** and we stop
   (the full multiplet adds components, not coupling). Cheap, days not weeks.
3. **Full `C^4×C^2×C^2×U(1)` relaxer** *only if* the gate splits — generalise the
   numba kernels (`gradient_flow_numba`: per-component `logse_gradient`, shared-`ρ`
   potential, sector `count_links`, `ω_c·ω_w` gradient).
4. **Sector measurement + four-sector energies** (§4), against the rule (§5).
5. **Decision**, posted to #81 and #80, with the script, tests, and a result note.

## 7. Cautions carried from #80 / the muon-BdG saga

- This is a **large build**; the minimal-gate-first plan (§6) exists precisely to
  avoid sinking weeks into the full 3D solver before knowing the cross term does
  anything. Validate convergence (regrid/continuation) before reading **any** gap
  as physical — a converged-*looking* fresh start is not a basin (the #77 lesson).
- The cross matrix element may **vanish by a selection rule** exactly as the #76
  `L_perp` Berry-phase bridge did (`m_a+m_b=0`). That is a real possible NOT-FORCED
  mechanism, not a bug — pre-registered as such in §3/§5.
- `.venv/bin/python` (Python not on PATH).

## 8. Reuse map (what Milestone 2 imports, not rebuilds)

| need | reuse |
|---|---|
| gradient-flow relaxer + topology guard + regrid | `instruments/paper_i/trefoil_gradient_flow_static.py` |
| JIT kernels (links, logse_gradient, energy) | `instruments/paper_i/gradient_flow_numba.py` |
| scalar energy density (skeleton to lift) | `instruments/paper_i/trefoil_observables.energy_density` |
| `L_perp` current/curl/energy/gradient | `instruments/paper_i/lperp_helpers.py` |
| ring/loop imprint + grid | `instruments/paper_i/trefoil_breather_static.{initial_state,coordinate_grid}` |
| bit→charge + `(P_c,P_w)`→16 oracle | `instruments/paper_ii/cp1_logse_16_assembly.py`, `pati_salam_16_unification.py` |
| junction Cartan/Weyl (SU(4)) | `instruments/paper_ii/su4_junction_chirality_closure.py` |

## Reproducer

This is a spec; nothing to run yet. Group-theory oracle (unchanged from #80):

```bash
.venv/bin/python instruments/paper_ii/pati_salam_16_unification.py
.venv/bin/python -m pytest instruments/paper_ii/test_pati_salam_16_unification.py -q
```

# Cheap route — the chirality-locking cross term is allowed and leading-order (#81, 2026-06-05)

**Issue:** [#81](https://github.com/StigNorland/SVT/issues/81), the analytic gate
before the numerical build. **Verdict: the locking term does NOT vanish by a
selection rule** — unlike the #76 `L_perp` Berry-phase bridge. The chirality
question therefore reduces to the *sign* of one coupling, not to whether the
mechanism exists.

**Script:** `instruments/paper_ii/lr_su4_cross_term_audit.py` · **tests:**
`test_lr_su4_cross_term_audit.py` (5 pass). **Spec:** `lr-su4-logse-spec.md`.

## What was tested

The spec (§3) showed the entire chirality verdict rests on one term in the
generalised chiral-shear energy of the LR-symmetric SU(4) LogSE:

```
E_perp ⊃ λ_cw ∫ ω_c · ω_w d^3r ,   ω_c = ∇×j_c (colour),  ω_w = ∇×j_w (weak).
```

Flipping `P_c` alone *or* `P_w` alone sends `ω → −ω`, so the cross term flips sign;
flipping both (the diagonal = chirality move) leaves it invariant. So it splits the
diagonal sector (the chiral **16**) from the anti-diagonal. The cheap, pre-numerical
questions: **(A)** is `∫ω_c·ω_w` forced to vanish by a selection rule (which would
make the four sectors degenerate ⇒ NOT-FORCED, the #80 postulate stands), and
**(B)** if not, how big is it relative to the diagonal self-terms?

## The key distinction from the #76 null

#76 killed the `L_perp` contribution because its matrix element was an **off-diagonal
holonomy / Berry-phase bridge** `⟨ψ_a|δL_perp|ψ_b⟩` between two *different* eigenmodes
`e^{im_aφ}`, `e^{im_bφ}`; the azimuthal integral plus the curl structure forced
`m_a = m_b` **and** `m_a + m_b = 0`, so it vanished.

The chirality-locking term is a **diagonal energy of one configuration.** `ω_c, ω_w`
are curls of the *real* currents `j = Im(ψ*∇ψ) = (m/r)|ψ|² φ̂` — the phase `e^{imφ}`
has been **differentiated out**, leaving no residual azimuthal phase. The `φ`-integral
is `∫dφ = 2π ≠ 0`. **No selection rule of the #76 type can apply.** Only the radial
integral could vanish, and it does not.

## Result (co-located straight windings, LogSE profile, r < 15 ξ)

For one defect carrying both a colour winding `m_c` and a weak winding `m_w` on a
**shared core** (`z = f e^{im_cφ}`, `χ = f e^{im_wφ}`):

```
ω_z = 2 m f f'/r  (axial; other components 0)
ε_cw / λ_cw = m_c m_w · I_cross ,   I_cross = ∫ (2ff'/r)² · 2πr dr = 5.0195  (tail 9e-8)
```

- **(A) `I_cross = 5.02 > 0`, nonzero.** The term is allowed; NOT-FORCED-by-vanishing
  is ruled out at leading order.
- **(B) `I_cross` *equals* the diagonal straight-vortex `L_perp` self-energy density
  `I_curl`** of `lperp_core_integral.py` (when the colour and weak cores coincide,
  `|m|=1`). The locking term is the **same order** as the diagonal self-terms —
  `|λ_cw ∫ω_c·ω_w| ~ (λ/2)∫|ω|²` for `λ_cw ~ λ⊥` — **not a small correction.**

The four `(P_c, P_w)` sectors are therefore **not degenerate** at the `L_perp` level
once `λ_cw ≠ 0`: the diagonal and anti-diagonal split by `2·I_cross·λ_cw ≈ 10.04 λ_cw`
per unit defect length, with the `(++)`/`(−−)` diagonal pair degenerate and the
`(+−)`/`(−+)` anti-diagonal pair degenerate — exactly the ℤ₂×ℤ₂ structure the spec
predicts.

## What this decides, and what it leaves open

- **Decided:** the mechanism exists and is leading-order. The chirality verdict is
  **not** "does a locking term exist" (it does) but **"what is the sign of `λ_cw`"**:
  - `λ_cw < 0` ⇒ the chiral **16** (diagonal) is the ground state — a genuine SSV
    prediction of chirality.
  - `λ_cw > 0` ⇒ the anti-diagonal wins — the **WRONG-SIGN falsification** branch of
    the pre-registered rule.
- **A sharp new sub-claim:** the locking requires the colour and weak cores to
  **coincide** (spatial separation kills the term ∝ overlap). That is precisely the
  "one defect carries one whole generation" hypothesis — now a falsifiable
  geometric requirement, not an assumption.

## Caveats (honest, pre-registered)

1. **Straight-vortex leading order.** Ring curvature shifts the magnitude (cf. the
   `J_bend`/`K_bend` corrections in `lperp_core_integral.py`) but cannot turn a
   nonzero axial overlap into an exact zero — existence is robust, magnitude is not.
2. **Coincident cores assumed** (`f_c = f_w`). In the shared-`ρ` functional the two
   cores compete for one condensate; the true profiles differ and must come from the
   relaxer. This only rescales `I_cross`, not its sign or non-vanishing.
3. **The sign of `λ_cw` is untouched here** and is the remaining open question — the
   target of the minimal numerical gate (M2). The natural magnitude is `λ⊥ ~ α^{-2}`;
   the sign needs the SSV chiral-shear term's orientation, which the relaxed
   four-sector energies will deliver.

## Reproducer

```bash
.venv/bin/python instruments/paper_ii/lr_su4_cross_term_audit.py
.venv/bin/python -m pytest instruments/paper_ii/test_lr_su4_cross_term_audit.py -q
```

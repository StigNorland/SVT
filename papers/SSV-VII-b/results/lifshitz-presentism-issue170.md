# Issue #170 — can the bulk–screen reconstruction be *presentist*? (Lifshitz z≠1 modular locality)

**Status: tension found, then RESOLVED as UV-only — geometricity is IR-emergent.**
Two parts:
1. *(cautionary negative)* At the pure relativistic point (`z=1`) modular flow is
   geometric (far-tail 1.8%); at **pure `z=2`** (SSV's UV) a robust, N-converged
   non-local component appears (far-tail **7% ≈ 3.9×** `z=1`) — the preferred
   foliation degrades the boost-based geometricity, as the absence of Lorentz
   boosts (no CHM theorem) predicts.
2. *(resolution — emergent Lorentz)* But SSV's dispersion is **`z=1` in the IR,
   `z=2` only in the UV** (Bogoliubov, crossover at ξ). With the full crossover
   dispersion, the non-geometricity is confined to **UV regions (`ℓ ≲ ξ`,
   `R_uv = 15`)**; for **IR regions (`ℓ ≫ ξ`) the modular far-tail recovers to the
   geometric `z=1` level** (`R_ir = 1.09`, ~4–5× below the `z=2` benchmark 4.9;
   far-tail drops ~10× from UV to IR). **So the boost-based reconstruction holds
   for the emergent IR gravity; presentism survives as the microscopic
   substrate**, and the tension is a sub-ξ (UV) feature. This is the Volovik
   emergent-Lorentz picture, computationally supported.

Pre-registered on [#170](https://github.com/StigNorland/SVT/issues/170) before
the computation. Script `instruments/model_screen/lifshitz_modular.py`; tests
`instruments/test/model_screen/test_lifshitz_modular.py` (4); receipt
`lifshitz_modular_receipt.json`.

## Why this is the presentism test

SSV has a preferred frame (the condensate) — what a presentist "now" needs. But
the #166 reconstruction was borrowed from **AdS/CFT, which is eternalist** (fully
Lorentz/conformally invariant). The presentism-compatible holographies are the
**preferred-foliation** ones (Lifshitz / Hořava, anisotropic scaling with
dynamical exponent `z≠1`), and that is also SSV's own UV: the Bogoliubov
dispersion is linear in the IR (`z=1`) and **quadratic past ξ (`z=2`)**. The
first necessary condition of the reconstruction — a **geometric** modular
Hamiltonian — is the local **boost** (CHM), a theorem of Lorentz boost symmetry.
A `z≠1` screen has **no boost** (its absence *is* the preferred time). So the
presentist feature is precisely what can make the modular Hamiltonian non-local.

## Method

Free scalar, Dirichlet chain (reuse sub-calc 1), Lifshitz dispersion
`ω_k = (k̂²)^{z/2}` (`z=1` = relativistic massless; `z=2` = SSV's UV). Modular
`H_π` from the Gaussian correlators (Peschel–Eisler; valid for any dispersion).
Non-locality = far-tail weight of `H_π` at `|i−j| ≥ ℓ/2`.

## Result

| z | S | far-tail(H_π) |
|---|---|---|
| 1.00 (relativistic) | 0.702 | **0.0178** (geometric = sub-calc 1) |
| 1.25 | 0.994 | 0.0112 |
| 1.50 | 1.325 | 0.0135 |
| 1.75 | 1.704 | 0.0282 |
| 2.00 (SSV UV) | 2.147 | **0.0695** (≈ 3.9×) |

**Robustness (the honesty check — rule 1).** The `z=2` far-tail is **converged in
chain size**: `0.06951` at `N = 800, 1600, 2400, 3200` (unchanged) — so it is
*physical*, not the finite-size/IR artifact that spoiled sub-calc 1's periodic
ring. It stays elevated across block sizes (`0.074 / 0.070 / 0.067` at
`ℓ = 24/40/60`, ratio 4–5×). The `z=1` control reproduces the geometric CHM
value.

## Verdict (against the pre-registered rule)

- **Pre-registered comparison** (far-tail `z=2` ≫ `z=1`) is met **robustly**
  (3.9×, N-converged) → the preferred foliation **degrades** the modular
  geometricity → the boost-based reconstruction's *first* necessary condition is
  weakened for a presentist screen.
- **Honest qualifications (rule 1):**
  1. **Partial, not total.** 7% far-tail is the largest seen, but not order-1 —
     a degradation, not a collapse.
  2. **Non-monotonic in z.** Extending the sweep: `0.018 (z=1) → 0.014 (1.5) →
     0.070 (2.0) → 0.037 (2.5) → 0.065 (4.0)`. The far-tail does *not* grow
     cleanly with `z`, so it is a **crude single-number probe**; the robust fact
     is the specific `z=1`-vs-`z=2` contrast, and `z=2` is the physically relevant
     case.

**Net (part 1):** at *pure* `z=2` the preferred foliation erodes the CHM-geometric
modular flow the #166 reconstruction leans on — a cautionary negative. But SSV is
not a *pure* `z=2` theory, which motivates the follow-on.

## Follow-on — is the geometricity IR-emergent? (Bogoliubov crossover)

**Pre-registered on [#170](https://github.com/StigNorland/SVT/issues/170) (with a
disclosed reconnaissance peek).** SSV's real dispersion is
`ω_k = k̂·√(1 + (ξ k̂)²)` — **`z=1` (acoustic) for `k̂ ≪ 1/ξ`, `z=2`
(free-particle) for `k̂ ≫ 1/ξ`**, crossover at the healing length ξ. Competing
hypotheses: **(A) emergent Lorentz** — the non-geometricity is a UV (`ℓ ≲ ξ`)
feature that washes out for IR regions; **(B) persists** — entanglement is
UV-dominated (area law from entangling-surface modes), so the non-locality
survives even for `ℓ ≫ ξ`. Metric: far-tail vs region size, normalised to the
pure-`z=1` reference at the same `ℓ`, `R(ℓ) = far_bog/far_z1`.

| ℓ | ℓ/ξ | far_z1 | far_bog | far_z2 | R = bog/z1 |
|---|---|---|---|---|---|
| 2 | 0.5 | 0.0056 | 0.1447 | 0.1325 | 25.8 |
| 4 | 1.0 | 0.0220 | 0.1007 | 0.1236 | 4.6 |
| 8 | 2.0 | 0.0152 | 0.0388 | 0.0963 | 2.6 |
| 16 | 4.0 | 0.0164 | 0.0197 | 0.0799 | 1.2 |
| 32 | 8.0 | 0.0161 | 0.0130 | 0.0713 | 0.8 |
| 64 | 16.0 | 0.0133 | 0.0169 | 0.0669 | 1.3 |

`R_uv (ℓ ≤ ξ) = 15`, `R_ir (ℓ ≥ 4ξ) = 1.09`, `z=2` benchmark ratio `= 4.9`.
The flow is **N-converged** (`R(ℓ)` stable to 3 digits at `N = 2000/3000/4500`) —
so the residual scatter is physical, not finite-size.

**Verdict: EMERGENT LORENTZ (Hypothesis A).** The `z=2` non-geometricity is
confined to UV regions (`ℓ ≲ ξ`, `R_uv = 15`); for IR regions (`ℓ ≫ ξ`) the
modular far-tail **recovers to the geometric `z=1` level** (`R_ir = 1.09`,
~4–5× below the `z=2` benchmark; far-tail drops ~10× from UV to IR). So the
**boost-based reconstruction holds for the emergent IR gravity**, where SSV's
gravity and transverse waves actually live, and **presentism survives as the
microscopic substrate** — the #170 tension is a sub-ξ (UV) feature.

*Honest bounds (rule 1):* this is a **positive** result, hence suggestive, not
proof. The far-tail is a crude single-number metric — `R_ir` scatters ~±25%
(0.8–1.3, non-monotonic, same as the pure-`z` sweep) — so the robust claim is
"IR far-tail sits at the `z=1` geometric level, ~4–5× below `z=2`," not
"`R_ir = 1.00` exactly." 1D screen; boost-based probe only.

## Honesty items and scope (rule 1)

- **Standard reconstruction only.** This tests the *boost-based* Faulkner–VR
  geometricity condition. A non-geometric modular Hamiltonian breaks *that*
  machinery — it does **not** prove that no *modified*, non-relativistic
  (Lifshitz-holographic) reconstruction could exist. Whether a `z≠1` holographic
  reconstruction (e.g. via a Lifshitz RT prescription) recovers the bulk shear is
  a separate, open question.
- **Crude probe.** The far-tail is one scalar; the non-monotonic `z`-dependence
  says it does not cleanly rank "non-geometricity." A sharper diagnostic (e.g. the
  ABCH bilocal coefficient, or the first-law residual `δS − δ⟨K^{CHM}⟩` directly)
  would strengthen or soften the tension — the natural next probe.
- **1D screen.** As in sub-calc 1, this is a `d=1` boundary; the TT-graviton
  sector needs `d ≥ 3`. This tests the modular/geometricity link, not the full
  `d≥3` reconstruction.

## Net

Pure `z=2` (a maximally presentist screen) strains the boost-based reconstruction
— but SSV is a **crossover** theory, and the strain is **UV-only**: for IR regions
(`ℓ ≫ ξ`) the modular flow recovers geometricity, so the #166 reconstruction holds
for SSV's **emergent** IR gravity while the **preferred frame / presentist "now"
survives as the microscopic (sub-ξ) substrate**. This is the Volovik picture made
quantitative: **Lorentz invariance — and with it the boost-based
entanglement→gravity reconstruction — is emergent in the IR; presentism is
fundamental in the UV.** The two are not in conflict once the crossover is
respected. Remaining honest items: a sharper (non-far-tail) diagnostic, the
`d ≥ 3` sector, and whether a genuinely *non-relativistic* reconstruction is still
needed for the sub-ξ regime itself (where the emergent picture does not reach).

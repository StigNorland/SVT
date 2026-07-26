# Issue #166 sub-calculation 1 — modular-locality of the screen

**Status: R1-open — the necessary condition PASSES.** The screen's modular flow
stays **geometric** (a short-range / local operator) as SSV's scale `ξ` is turned
on; the non-local (bilocal) tail that would break the boost **does not grow** with
`mξ` — it shrinks. So the obstruction I expected (a scale making the modular
Hamiltonian non-local → R3) **does not appear** in this test. This keeps the
bulk–screen duality (#166) alive at the level of its first necessary condition;
it does **not** establish the duality — the decisive stress-sector tests remain.

Pre-registered on [#166](https://github.com/StigNorland/SVT/issues/166) (comment)
before the computation. Script `instruments/model_screen/modular_locality.py`;
tests `instruments/test/model_screen/test_modular_locality.py` (6: ν physical,
C1 entropy, C2 formula reconstruction, C3 massless locality, the no-growth
result, verdict); receipt `modular_locality_receipt.json`.

## Methodology note (rule 1 cuts both ways)

My pre-registered prior was **R3-favourite** (a scale breaks the boost). The first
implementation (periodic ring) produced a *spurious* signal — its `c = 1` entropy
control failed (`c_eff ≈ 0.73–0.80`, drifting) because the non-compact boson's
**IR zero mode** contaminates a ring, and I had keyed a draft verdict on the wrong
metric (raw off-diagonal weight, which is non-monotonic: a very massive field is
*trivially* ultralocal). I withheld the verdict, fixed the setup, and the
**validated** instrument overturned the prior. This is the "validate before you
trust the verdict" discipline working in the direction that costs me my guess.

## Method

Free scalar, ground state, on a **Dirichlet** chain (open ends — removes the IR
zero mode that spoils a periodic ring). Block of `ℓ` sites from a wall (one
entangling point). Correlators `X = ⟨φφ⟩`, `P = ⟨ππ⟩`; bosonic entanglement
Hamiltonian `H = ½(π·H_π·π + φ·H_φ·φ)` via `H_π = P^{-1/2} g(P^{1/2}XP^{1/2}) P^{-1/2}`,
`g(M) = √M · 2 arccoth(2√M)` (the single-mode law `h_π = ε(ν)√(x/p)` lifted by
the functional calculus). Non-locality = the **far-tail** weight of `H_π` at
separation `|i−j| ≥ ℓ/2` — zero for a local boost, order-one for a bilocal term.

## Positive controls (all pass)

| control | result | meaning |
|---|---|---|
| **C1** entropy central charge | `c_eff = 0.972` (target 1.0) | Dirichlet reproduces the `c=1` free scalar; zero mode removed |
| **C2** modular formula | reconstruction err `2.0×10⁻⁷` | the thermal state of `H` returns the input `X, P` — the formula is correct |
| **C3** massless locality | far-tail `= 0.018` | the massless boost is short-range (per-cent lattice residual, not order one) |

## Result (`ℓ = 40`, Dirichlet `N = 1600`)

| m | mℓ | S | far-tail(H_π) = non-locality |
|---|---|---|---|
| 0.001 | 0.04 | 0.702 | **0.0178** |
| 0.05  | 2.00 | 0.498 | 0.0098 |
| 0.15  | 6.00 | 0.319 | 0.0045 |
| 0.40  | 16.0 | 0.167 | 0.00005 |
| 1.00  | 40.0 | 0.056 | 0.00000 |

The non-local tail is largest at the massless point (a small lattice residual) and
**monotonically shrinks** as the scale `mℓ` grows — the modular Hamiltonian
becomes *more* local, not less. There is no bilocal term growing with the scale.

## Verdict and decision rule

- **Pre-registered rule:** far tail grows with `mℓ` → R3; does not grow → R1-open.
- **Outcome:** far tail does **not** grow (it shrinks) → **R1-open**: modular flow
  can be geometric despite `ξ`. R3 is **not** triggered by this probe.

## Honesty items and scope (rule 1)

- **Necessary, not sufficient.** This clears *one* of #166's R1 requirements — the
  modular/boost structure survives the scale. It says nothing yet about the
  decisive objects: a nonzero screen `⟨τ_ab^TT τ_cd^TT⟩` with two polarisations and
  the correct Ward identities, and whether the normalisation *fixes* `G` rather
  than renaming it. R1 stays *open*, not *met*.
- **Geometry caveat.** The validated setup is **block-from-boundary** (one
  entangling point). The two-entangling-point **interval** geometry — where the
  Arias–Blanco–Casini–Huerta *bilocal* term is defined — did **not** validate its
  `c=1` control at accessible sizes (mid-chain `c_eff ≈ 0.6`, a separate numerical
  issue). So this test does not yet probe the specific ABCH bilocal structure; the
  interval geometry is the natural strengthening before R1-open is leaned on hard.
- **No soft positive.** "R1-open" means *the obstruction did not appear here*, not
  "the duality works." The honest next step is the screen stress-sector
  calculation, which is where R2/R3 most plausibly still bite.

## Net

The cheapest necessary condition for the bulk–screen duality — that the screen's
modular flow can be geometric despite SSV's scale `ξ` — **passes** in a validated
computation, against my prior. The duality route survives its first real test.
The decisive question (does the screen entanglement algebra carry a conserved
spin-2 stress response with `G` fixed, not inserted) is untouched and is where the
programme should look next.

# Cheap route — colour connectivity is geometrically free *once you pay for the multiplet* (2026-06-05)

**Spec:** `connected-su4-offdiagonal-test-spec.md`. **Verdict: the off-diagonal SU(4)
test reduces to the same foundational fork as #81/#83 — but with a hopeful twist.**
In the scalar/junction realisation colour stays a *product* (Cartan only); in the
multiplet realisation the *natural* chiral-shear term is automatically SU(4)-invariant,
so the 12 off-diagonal generators survive **for free** — no extra term, unlike
chirality (#81).

**Script:** `instruments/paper_ii/connected_su4_offdiagonal_audit.py` · **tests:**
`test_connected_su4_offdiagonal_audit.py` (6 pass).

## The question

#79/#80 gave only the **Cartan + Weyl** of SU(4) from the junction — `lie_closure` on
the junction Cartan returns **3** (`u(1)³`), not 15 (`su(4)`). Are the 12 **off-diagonal**
generators (the ladder operators rotating colour `i`→`j`, incl. quark↔lepton since
lepton = 4th colour) genuine dynamical symmetries (**connected**, case a), or absent
(**product**, case b)?

## The audit, and why it's cheap

In the multi-component order parameter (`z ∈ C⁴`, shared `ρ = Σ|z_a|²`, LogSE +
chiral-shear `L_perp`), the gradient term and log potential already see only `ρ`, so
they are SU(4)-invariant. **Connectivity hinges entirely on which current `L_perp` is
built from**, and that is a one-line algebraic fact:

| chiral-shear current | realised continuous symmetry (`lie_closure`) | verdict |
|---|---|---|
| **total** `j_total = Im(z†∇z)` | **15 = su(4)** | **CONNECTED** |
| **sector** `{j_a = Im(z_a*∇z_a)}`, `Σ\|∇×j_a\|²` | **3 = u(1)³** | **PRODUCT** |

(Computed with the *same* `lie_closure` used for the junction; it reproduces 15 for
all of su(4) and 3 for the Cartan as sanity checks.)

## The key fact

The scalar SSV current `j = Im(ψ*∇ψ)` is the Noether current of the field's **overall
U(1)**. Its *unique* multi-component generalisation is the overall-U(1) Noether current

```
j_total = Im(z† ∇z) = Σ_a Im(z_a* ∇z_a),
```

**not** a set of per-colour currents (the individual `z_a*∇z_a` are not separately
conserved — there is one condensate, one U(1)). And `j_total` is **exactly
SU(4)-invariant**: under `z → U z` with constant `U ∈ SU(4)`,
`z†∇z → z† U†U ∇z = z†∇z`. So the natural chiral-shear `L_perp` is SU(4)-invariant,
every off-diagonal generator is an exact symmetry, and `lie_closure = 15`: **connected,
with no extra term**. The per-colour form — which has no scalar analogue — is invariant
only under the Cartan (and Weyl permutations), giving `lie_closure = 3`: product.

`B−L = diag(1,1,1,−3)` is a Cartan element, so it is a symmetry of *both* forms —
consistent with #80 getting B−L for free in the junction picture.

## What this decides

Connectivity is **not** decided by the dynamics within a fixed realisation; it is the
**same foundational fork** as #81/#83 — realise colour as a genuine internal multiplet,
or not:

- **Junction realisation (native scalar SSV, #79/#80):** there is no fundamental `C⁴`;
  colour-`i` → colour-`j` is a **reconnection** (a topology change), not a continuous
  rotation. The off-diagonal generators are simply absent from the continuous dynamics
  → `lie_closure = 3` → **PRODUCT**. This reproduces #79/#80 exactly.
- **Multiplet realisation (the #83-type internal-orientation upgrade):** the natural
  total-current `L_perp` is SU(4)-invariant → `lie_closure = 15` → **CONNECTED**,
  automatically.

## The hopeful asymmetry vs #81

This is the genuinely new content. Of the two *continuous* structures the scalar field
lacks:

- **colour off-diagonal symmetry** comes **geometrically free** once you adopt the
  internal multiplet — the **parity-even** total-current term already delivers it;
- **weak chirality** (#81) does **not** — it needs a **parity-odd** term even after the
  upgrade (you cannot derive parity violation from a parity-conserving Lagrangian).

So the two faces of the "internal-orientation" foundational move (#83) pay out
differently: adopting an internal multiplet **buys connected colour for free**, but
**still leaves chirality as a separate parity-odd postulate**. That sharpens #83: the
spinor/multiplet upgrade is more powerful on the colour side than on the chirality side.

## Where it lands in the thread

The recurring pattern holds and is now quantified on the colour side:

| sector | discrete skeleton (free) | continuous structure | needs | status |
|---|---|---|---|---|
| colour | Cartan + Weyl + B−L (#79/#80) | off-diagonal su(4) | internal multiplet (parity-even) | **free post-multiplet (this note)** |
| weak/chirality | parities, T₃ (#80) | chirality ℤ₂ | parity-odd term (#81) | not free even post-multiplet |
| spin/leptons | integer rungs | half-integer ℤ₂ | spinor (#83) | the foundational decision |

All three are the same fork — *labels (scalar + junctions) vs rotations (a field with
internal orientation)* — and the multiplet/spinor upgrade resolves them to differing
degrees.

## Caveats

1. **Algebraic, global-symmetry level.** This proves the off-diagonal generators are
   exact symmetries of the *natural* multiplet functional; it does not yet build a 3D
   defect and measure the realised algebra on a relaxed configuration (spec Milestone
   3). But because the result is an exact invariance (`z†∇z` identity), the full
   relaxer would only re-confirm it — as the symmetry argument did for #81.
2. **"Total vs sector current" is the load-bearing reading**, settled here from the
   scalar Noether-current identity (the total current is the unique generalisation).
   A master equation that instead postulated per-colour chiral-shear would be product —
   but that is the un-natural choice with no scalar analogue.

## Reproducer

```bash
.venv/bin/python instruments/paper_ii/connected_su4_offdiagonal_audit.py
.venv/bin/python -m pytest instruments/paper_ii/test_connected_su4_offdiagonal_audit.py -q
```

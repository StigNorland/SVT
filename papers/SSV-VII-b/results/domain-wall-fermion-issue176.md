# No-go map (III) — do fermions survive in SSV? Standalone fails; **H-SSV** survives (domain-wall / anomaly inflow)

**Status: standalone SSV fails; H-SSV survives — chirality lives on the screen.**
SSV is a *bosonic* condensate; matter is fermionic and *chiral*. Standalone SSV
fails on both counts (statistics *and* chirality). But the holographic container's
**extra dimension** is exactly the Nielsen–Ninomiya loophole: a chiral fermion
binds to a domain wall (the screen), its doubler exiled to the opposite wall by
the bulk (Kaplan / Callan–Harvey). Computed here directly — each wall binds **one
chiral zero mode**, the two walls carry **opposite chirality**, separated by the
gapped bulk. So the container is **triply essential**: gravity (#166),
Lorentz-naturalness (#172), and now **chiral fermions**.

Pre-registered on [#176](https://github.com/StigNorland/SVT/issues/176). Grounded
in real sources (cited). Script
`instruments/model_fermion/domain_wall_fermion.py`; tests
`instruments/test/model_fermion/test_domain_wall_fermion.py` (5); receipt
`domain_wall_fermion_receipt.json`.

## Two failures for standalone SSV

- **Statistics** (fermions *at all*). The bare log-GPE order parameter is a single
  complex scalar (`U(1)`); `π₃(S¹) = 0`, so there are **no fermionic solitons**
  without extra internal structure (a target with `π₃ ≠ 0`, à la
  Skyrme / Finkelstein–Rubinstein). The bare condensate is topologically too simple
  to host a fermion.
- **Chirality** (a single Weyl fermion — the Standard Model is parity-violating).
  **Nielsen–Ninomiya** forbids a single chiral fermion on a local discrete
  substrate (doubling). **Volovik's** Fermi-point evasion needs a *fermionic*
  substrate — unavailable to bosonic SSV.

## The escape *is* holography (established)

**Kaplan domain-wall fermions** (embed 4D in 5D with a domain-wall mass): one
chirality localizes on the wall, the opposite chirality on the *other* wall.
Kaplan: *"The extra dimension is the loophole in the Nielsen–Ninomiya theorem
through which the fermions have wriggled."* **Callan–Harvey anomaly inflow**: a
massive Dirac fermion with a domain-wall mass profile binds a single chiral edge
mode, with current conservation restored by inflow from the bulk. This is exactly
the H-SSV picture — **the screen is the domain wall; the bulk is the extra
dimension; the chiral fermion lives on the screen.**

## Method — computing the mechanism

A 1D Wilson–Dirac Hamiltonian `H = -i σ₂∂ₓ + σ₁ m(x)` (+ Wilson term) with a
position-dependent mass. Continuum theory: at a kink `m(x)=m₀tanh(x/w)` the zero
mode `ψ₀ ∝ exp(-∫m)` is a **single chirality eigenstate**, normalizable and
localized; the opposite chirality is non-normalizable at one wall. Degenerate
zero modes are resolved by diagonalizing chirality `σ₃` in the near-zero subspace.

## Result (all controls pass)

**Kink + antikink (periodic bulk):**

| mode | `E` | center | width | chirality `⟨σ₃⟩` |
|---|---|---|---|---|
| wall 1 | `<10⁻¹⁵` | 49.8 (`=N/4`) | 1.5 | **+1.00** |
| wall 2 | `<10⁻¹⁵` | 150.2 (`=3N/4`) | 1.5 | **−1.00** |

Bulk gap `≈ 0.64`. **Each wall binds exactly one chiral zero mode; the two walls
carry opposite chirality, localized and separated by the gapped bulk** — the
doubler is exiled to the far wall by the extra dimension.

**Single wall (open chain):** the wall mode (`⟨σ₃⟩=+1`, at the wall) plus its
partner **exiled to the boundary** (`⟨σ₃⟩=−1`, at the edge) — confirming the
doubler is always present but spatially separated (Nielsen–Ninomiya respected,
chirality *isolated* on the wall).

## Verdict

- **Standalone SSV: FAILS** — no fermionic solitons (`π₃=0`) and no way to isolate
  a chiral fermion (Nielsen–Ninomiya, no Fermi-point evasion for a bosonic
  vacuum). A real negative, reinforcing the standalone closure.
- **H-SSV: SURVIVES** — the container's extra dimension binds a single chiral
  fermion to the screen (domain wall) with the doubler exiled to the far boundary
  (Kaplan / Callan–Harvey), demonstrated here. **Chirality lives on the screen.**

**Net:** the container is now **triply essential** — the transverse-traceless
gravity (#166), the Lorentz-naturalness (#172), and the chiral fermions all live
on / require the holographic bulk that a bosonic superfluid cannot supply itself.
The three deepest problems of a standalone superfluid vacuum have the **same
cure**.

## Honesty items and scope (rule 1)

- **Mechanism / existence, not the Standard Model.** This demonstrates *that* the
  extra dimension isolates a chiral fermion (a rigorous, established mechanism) —
  it does **not** produce the actual SM (three generations, the correct gauge
  group, anomaly cancellation), which is unsolved for *everyone*, not just SSV. A
  positive result → suggestive, honestly bounded.
- **The negative is the firm part.** That *standalone* bosonic SSV can host neither
  fermionic statistics nor an isolated chiral fermion is the proof-carrying
  conclusion.
- **Statistics is addressed separately.** The domain-wall construction presupposes
  a bulk Dirac fermion; "fermions from bosons" (solitons with `π₃≠0`, string-net /
  holographic emergent fermions) is the distinct statistics question, only sketched
  here.
- **Finite bulk caveat** (from the sources): at finite fifth-dimension extent the
  two walls couple and the chiral mode acquires a small residual mass — exact
  chirality needs an infinite (or large) extra dimension.

## Sources

- Kaplan, *A method for simulating chiral fermions on the lattice*, PLB 288 (1992)
  342 — domain-wall fermions; "the extra dimension is the loophole …".
- Callan & Harvey, *Anomalies and fermion zero modes on strings and domain walls*,
  NPB 250 (1985) 427 — anomaly inflow.
- Nielsen & Ninomiya, *Absence of neutrinos on a lattice*, NPB 185 (1981) 20 —
  the doubling no-go.
- Volovik, *The Universe in a Helium Droplet* — Fermi-point (fermionic) emergent
  chirality.
- Jackiw & Rebbi, *Solitons with fermion number ½*, PRD 13 (1976) 3398 — the
  domain-wall zero mode.
- Finkelstein & Rubinstein / Skyrme — soliton spin-statistics (the `π₃`
  requirement for fermionic solitons).

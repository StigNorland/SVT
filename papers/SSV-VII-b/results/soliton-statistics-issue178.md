# No-go map (IV) — can a bosonic condensate yield fermions at all? (π₃ admissibility)

**Status: bare SSV FAILS (firm negative); the minimal repair is *derived* — a
multi-component condensate.** The bare log-GPE order parameter (a single complex
scalar, target `S¹`) has a π₃ winding density that is **pointwise zero** — not
small, not cancelling: identically zero for *any* configuration. So the bare
condensate has **no 3D topological solitons to quantize, a fortiori none
fermionic**. A **two-component (SU(2)-valued) condensate** has integer π₃ winding
(computed: `|B| = 1, 2`, deformation-stable), and `π₄(S³) = Z₂` (cited) supplies
the Finkelstein–Rubinstein fermionic option. **Fermionic solitons demand a
multi-component condensate — a derived constraint on SSV's field content, not a
free choice.**

Pre-registered on [#178](https://github.com/StigNorland/SVT/issues/178). Grounded
in real sources (cited). Script
`instruments/model_fermion/soliton_statistics.py`; tests
`instruments/test/model_fermion/test_soliton_statistics.py` (6); receipt
`soliton_statistics_receipt.json`.

## The established mechanism (grounded)

**Finkelstein–Rubinstein (1968) / Skyrme / Witten (1983):** a soliton quantizes
as a **fermion** iff a `2π` rotation of it is a **non-contractible loop** in
configuration space — `π₁(Q_B) = Z₂`, wavefunctions live on the double cover,
with FR sign `−1` on non-contractible loops. For target `SU(2) ≅ S³`:

- `π₃(S³) = Z` → solitons **exist** (winding = baryon number `B`);
- `π₄(S³) = Z₂` → the FR **fermionic option exists** (selected by the
  Wess–Zumino term; Witten's `N_c`-parity result).

## The SSV-specific bite

- **Bare SSV:** single complex scalar → target `S¹`. `π₃(S¹) = 0`. The paper-I
  ring solitons are `U(1)` phase-winding **vortex rings** — a different topology
  with **no FR `Z₂` mechanism**.
- **Constructive demand:** solitonic fermions need `π₃ ≠ 0` — minimally an
  `SU(2)`-valued (two-component / spinor) condensate. Spinor BECs are real
  physical systems, so the extension is physically sensible, not exotic.

## Method

Order parameter as a unit 4-vector `n^A(x)` on `S³` (`U = n₀ + i n·σ`). The π₃
winding (degree of the map `R³∪{∞} → S³`):

    B = (1/2π²) ∫ det[n, ∂ₓn, ∂ᵧn, ∂azn] d³x

- **T2** — SU(2) hedgehog `U = exp(i f(r) x̂·σ)`, `f = 4·turns·arctan(e^{−r/w})`
  (analytic check: `B = [f − sin f cos f]/π` at the origin = exactly 1, 2).
- **T1** — bare-SSV `U(1)` configuration `n = (cos θ(x), sin θ(x), 0, 0)`: the
  image lies on a **great circle** of `S³`, so the three derivative vectors are
  parallel in the tangent space → the determinant vanishes **pointwise**.

## Result (grid `N = 128³`, box `L = 6`, all controls pass)

| test | value | target | |
|---|---|---|---|
| **C1** hedgehog, 1 turn | `\|B\| = 0.994` | 1 | ✓ |
| **C2** hedgehog, 2 turns | `\|B\| = 1.965` | 2 | ✓ |
| **C3** deformed profile | `B` shift `0.002` | 0 (topological) | ✓ |
| **C5** grid convergence | `0.907 → 0.977 → 0.994` (N=64→96→128) | → integer | ✓ |
| **T1** U(1) density | max `\|ρ\| = 0.0` (exactly) | pointwise zero | ✓ |

The U(1) result is the strong form of the negative: the density is **identically
zero at every grid point** — a structural vanishing (parallel tangents on a great
circle), not a numerical cancellation. Verified on two independent
configurations.

## Verdict (against the pre-registered rule)

- **T1: bare SSV FAILS.** Zero π₃ density pointwise → `B = 0` for any
  configuration → **no solitons to quantize, hence no fermionic solitons.** The
  firm, proof-carrying negative.
- **T2: the minimal repair is derived.** A two-component (`SU(2)`-valued)
  condensate has integer, deformation-stable π₃ winding; `π₄(S³) = Z₂` (cited)
  then supplies the FR fermionic option. **SSV's condensate must be
  multi-component if its particles are fermionic solitons** — previously a free
  modelling choice, now a derived requirement.

## Honesty items and scope (rule 1)

- **Admissibility, not existence.** `π₃ ≠ 0` + FR says a two-component condensate
  *may* host fermionic solitons. Whether the **log-GPE dynamics stabilizes** a
  Skyrme-like soliton (needs a quartic/Skyrme term against Derrick collapse) is a
  separate, open dynamical question — flagged, not solved.
- **`π₄(S³) = Z₂` is cited, not computed.** Loop homotopy in configuration space
  is beyond these numerics; the computed content is the π₃ split (zero vs
  integer). The FR mechanism itself is textbook-established.
- **The container alternative stands.** H-SSV can instead supply fermions
  holographically (no-go III's bulk fermion route); this note constrains the
  *solitonic* route specifically.
- **Paper-I connection.** The existing lepton-ring constructions are `U(1)`
  vortex rings; this result says they **cannot be fermions by the FR mechanism**
  as they stand. Any fermionic-soliton reading of SSV's particles requires the
  multi-component extension (or the holographic route).

## Sources

- Finkelstein & Rubinstein, *Connection between spin, statistics, and kinks*,
  J. Math. Phys. 9 (1968) 1762.
- Skyrme, *A non-linear field theory*, Proc. R. Soc. A 260 (1961) 127.
- Witten, *Global aspects of current algebra* / *Current algebra, baryons, and
  quark confinement*, NPB 223 (1983) 422, 433 — WZ term, `π₄(S³)=Z₂`, skyrmions
  as fermions for odd `N_c`.
- Krusch, *Homotopy of rational maps and the quantization of skyrmions* (FR
  constraints in practice); Kent Academic Repository / Proc. R. Soc. A (2006) —
  FR constraints with pion masses.
- Levin & Wen, *Fermions, strings, and gauge fields in lattice spin models* —
  (context) the non-solitonic bosonic route to emergent fermions.

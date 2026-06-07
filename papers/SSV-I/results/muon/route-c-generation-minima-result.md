# Route C result: generations as static minima — FAIL (2026-06-05)

**Issue:** [#78](https://github.com/StigNorland/SVT/issues/78) Task C.
**Pre-registration:** `papers/SSV-I/route-c-generation-minima-prereg.md` (committed first).
**Verdict: FAIL** — the relaxed static-energy ratio is `3.71`, vs the
pre-registered PASS band `[165, 248]` around `m_μ/m_e = 206.77`.

## Result

Singly-wound vortex rings relaxed with the #77 numba gradient-flow + topology
guard, pure LogSE (`λ_perp=0`), matched `dx = 0.125 ξ`:

| R_seed (ξ) | n | E_relaxed | R_relaxed (ξ) | links (i→f) | stable? |
|---|---|---|---|---|---|
| 1.0 | 96 | 364.79 | 1.088 | 64 → 64 | yes |
| 8.0 | 192 | 1351.71 | 7.955 | 512 → 512 | yes |

```
ratio = E(8ξ)/E(1ξ) = 3.71
```

Decision rule: `3.71` ∉ `[103, 414]` (suggestive) → **FAIL**.
Against `(3/2)μ₀/m_e = 207.5`: identical verdict.

Both rings are **stable** (topology preserved exactly; R_relaxed tracks the seed
to ~1%), so this is a clean FAIL, **not** the NULL "no stable minimum" branch.
The 8 ξ ring is a perfectly good static configuration — it simply does not weigh
206× the 1 ξ ring.

## Why the ratio is ~4, not ~207

The vortex-ring self-energy scales roughly with line length × a logarithm:
`E(R) ≈ 2πR · μ_eff · [ln(8R/ξ) − C]`-ish. For `R: 1→8 ξ` that gives a ratio of
order `8 × (log correction)`, i.e. single digits — here `3.71` (sub-linear
because the R=1 ring's energy is inflated by its marginal geometry, core ≈ major
radius). It is **nowhere near** the mass ratio 206.77.

The earlier "`R_μ/R_e = 8.59 → m_μ/m_e = 206.77`" inversion
(`vortex_ring_mass_inversion.py`) relied on the thin-ring formula
`E = πR[ln(8R/ξ) − C]` being **near its zero at R≈1 ξ** (with `C≈2`,
`ln 8 − 2 = 0.079`), which made the denominator `E(1ξ)` tiny and the ratio huge.
The actual relaxed `E(1ξ) = 365` (sim units) is **not** tiny — the thin-ring
formula fails badly at R≈1 ξ (which is not thin) — so the real energy ratio is
small. The 206.77 was a formula-singularity artifact, not a physical
energy-ratio.

## Combined with Route D

Route C (this note) and Route D (`route-d-kelvin-degeneracy-result.md`) both come
back negative:

- **C:** the relaxed static-energy ratio is 3.71, not 206.77 — generations are
  not distinct static minima whose energy ratio is the mass ratio.
- **D:** the `8ⁿ` ladder does not collapse to exact 8 with the real core
  constant, and the ring's U(1) symmetry has no magic number 8.

Per the issue's task ordering, with **both C and D negative**, the structural
escape hatches (Task B half-quantum-vortex sector, Task A spinorial order
parameter) are the remaining avenues and are scoped in their respective memos.

## Reproducer

```bash
.venv/bin/python instruments/paper_i/lepton_ring_static.py \
    --radii 1.0,8.0 --tube 0.85 --dx 0.125 --max-steps 8000 \
    --output papers/SSV-I/data/route-c-generation-minima-2026-06-05.json
```

Coarse cross-check (`dx=0.25`): ratio 4.04, same verdict — the result is not a
resolution artifact.

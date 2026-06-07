# Route C pre-registration: generations as distinct static minima (2026-06-05)

**Issue:** [#78](https://github.com/StigNorland/SVT/issues/78) Task C.
**Committed before running.** This file fixes the test design and decision rule
in advance so the outcome cannot be tuned.

## Hypothesis

Lepton generations are distinct static minima of the singly-wound toroidal
vortex ring at radii following the closed-shell ladder `R_n ≈ 8ⁿ ξ`
(electron n=0 at R≈1 ξ, muon n=1 at R≈8 ξ, tau n=2 at R≈64 ξ). If so, the
relaxed static energy ratio should reproduce the mass ratio.

## Method

- Singly-wound vortex ring (circulation 1 around the tube), seeded as a planar
  circle of major radius R in the z=0 plane, tube radius a₀ ≈ 0.85 ξ.
- Relax with the #77 pipeline: numba gradient flow, topology guard
  (`topo_drop_tol`), pure LogSE (`λ_perp = 0`, matching the #77 trefoil runs),
  `log_pressure = 0.5` (canonical c=1).
- **Matched resolution** `dx = 0.125 ξ` across all radii so the energies are
  directly comparable: R≈1 ξ → half-width 6, n=96; R≈8 ξ → half-width 12, n=192.
- Observable: relaxed total LogSE energy `E(R)` (the uniform background
  contributes exactly zero to this energy functional, so `E` is the vortex
  self-energy). Also record the relaxed ring radius `R_relaxed` (mean
  cylindrical radius of the depleted core) to detect collapse.

## Primary metric

```
ratio = E(R≈8ξ) / E(R≈1ξ)
```

## Decision rule (fixed in advance)

| Outcome | Condition |
|---|---|
| **PASS** | `ratio ∈ [165, 248]` (m_μ/m_e = 206.77 ± 20%) |
| **SUGGESTIVE** | `ratio ∈ [103, 414]` (within a factor of 2 of 206.77) but outside the PASS band |
| **FAIL** | `ratio` outside `[103, 414]` while both rings are stable |
| **NULL (clean negative)** | the R≈8 ξ seed does **not** hold a ring: it collapses (`R_relaxed < 4 ξ`) or loses topology. Recorded as "no stable distinct minimum at 8 ξ" — an equally clean, publishable result. |

Report `ratio` against `(3/2)μ₀/m_e = 207.5` as well as `206.77`.

## Caveat stated in advance

R≈1 ξ is a marginal ring (core size ξ ≈ major radius), and the thin-ring Lamb
formula `E = πR[ln(8R/ξ) − C]` is near its zero there, so `E(1ξ)` is the
sensitive denominator. The thin-ring formula with `C = 2` gives `ratio ≈ 217`;
with `C = 1.88` (real LogSE core, `vortex_ring_core_constant.py`) it gives
`≈ 92`. The numerical relaxed `E(1ξ)` — not the thin-ring formula — is the
arbiter. This sensitivity is *why* the test is run numerically rather than read
off the formula.

## Reproducer

```bash
.venv/bin/python instruments/paper_i/lepton_ring_static.py \
    --radii 1.0,8.0 --tube 0.85 --dx 0.125 --max-steps 8000 \
    --output papers/SSV-I/data/route-c-generation-minima-2026-06-05.json
```

# Issue #129 TOKEN-TAX (H-BILATERAL S0) — which scheduling statistics buy the A² doubling?

**Status: all five decision rules resolved as analytically predicted.
The owner's worked example (photon and H₂ each taxed 20%, taxed tokens
coinciding) is the SYNCHRONIZED branch and pays the tax exactly once:
γ_tok = 0 — Einstein-1911 half deflection, the branch the 1919/1922
plates killed. The A² doubling exists only on the INDEPENDENT-schedules
branch (γ_tok = 1/A → 1 at weak load), and the interpolation
γ(c, A) = (1−c²)/(A + c²(1−A)) prices the requirement: Cassini's
|γ−1| ≤ 2.3×10⁻⁵ demands busy-schedule correlation c ≤ 4.8×10⁻³.
Derivation obligation 1 (decorrelation) is hereby tightened from "must
be shown" to "is false in the classical smooth-field reading; any
H-BILATERAL derivation must produce decorrelated microscopic update
statistics at the half-percent level or better, or a symmetry forcing
c = 0 exactly."**

Pre-registered on issue
[#129](https://github.com/StigNorland/SVT/issues/129) (TOKEN-TAX
comment, posted before computing). Script:
`instruments/paper_iv/bilateral_token_toy.py`; receipt
`bilateral_token_receipt.json`; tests
`instruments/test/paper_iv/test_bilateral_token_toy.py` (7: worked
example exact, sync machine-zero, indep 1/A, correlation closed form,
chromatic control, mask bookkeeping, δ closed forms).

## Model

Time = slots of S token positions; loading L taxes exactly k = L·S
positions per party per slot (the worked example: S = 10, k = 2,
A = 0.8). A photon crosses matter sites; each handshake accrues C = 10
**joint-free** positions (both parties free at the same position),
carrying over across slot boundaries. A clock is a monologue: one tick
per own-free position, so δ_clock = k/(S−k) = 0.25, deterministic in
every mode. Modes: SYNC (one shared busy mask — the smooth classical
field Φ), INDEP (every party draws its own mask per slot), CORR(c)
(shared mask with probability c, fresh otherwise).

γ_tok ≡ (δ_prop − δ_clock)/δ_clock, matching H-SPATIAL's γ_eff
convention: 0 = pure clock effect, 1 = the GR doubling at weak load.
Force-vs-time guard: both halves are delays; no force is modelled.

## Results (full battery, receipt for exact numbers)

| rule | measurement | result | closed form |
|---|---|---|---|
| D1 sync | worked-example ledger | **[8, 2]**, slot-2 use = 25% of available | exact |
| D1 sync | γ (rate estimator / wall) | **0.0** (machine) / −1.2×10⁻⁵ | 0 |
| D2 indep | γ at A = 0.8 | **1.2496 ± 0.0011** | 1/A = 1.25 |
| D3 corr | γ(c) at c = 0, ¼, ½, ¾, 1 | 1.2504 / 1.1526 / 0.8805 / 0.4790 / 0.0000 | 1.2500 / 1.1538 / 0.8824 / 0.4795 / 0 |
| D3 | Cassini price on correlation | **c ≤ 4.8×10⁻³** | √(2.3×10⁻⁵) |
| D4 | rate-levy delay vs C ∈ {5,10,20,40} | spread **0.2%** (achromatic) | C-independent |
| D4 | per-event-latency control | extra δ = 1.0/0.5/0.25/0.125 | D·S/C exactly (chromatic) |
| D5 weak load (L ≤ 0.005) | slope δ_prop(L) | indep **2.016**, sync **1.007** | 2, 1 (linear limit) |
| D5 pre-registered window (L = 0.01–0.05) | slope | indep **2.1931**, sync 1.0636 — **literal threshold MISS** | 2.1930, 1.0632 — the exact curvature |

**Honesty record (rule 1).** Two pre-registration defects, both caught
analytically *before* the runs and resolved transparently:

1. The pre-registered D5 window (L = 0.01–0.05) cannot satisfy its own
   thresholds (2.00 ± 0.05, 1.00 ± 0.02): the exact delays
   δ_indep = (2L−L²)/(1−L)² and δ_sync = L/(1−L) have mean local slopes
   2.19 and 1.06 there. The literal pre-registered check therefore
   **fails**, and the receipt records it as a failure
   (`D5_preregistered_window_literal: false`). The miss is fully
   explained: the measured slope equals the closed-form slope to 4
   decimals (2.1931 vs 2.1930) — finite-load curvature, not noise — and
   the weak-load tier (L ≤ 0.005, the physically relevant regime;
   solar-system |Φ|/c² ~ 10⁻⁶) passes the linear-limit thresholds.
   This is a threshold-selection error in the pre-registration, not a
   physics surprise; recorded rather than repaired in place.
2. "γ = 0 to machine precision" (D1) holds for the rate-based estimator
   and the token ledger; the wall-clock first-passage time carries an
   O(1/n) sub-slot quantization (measured −1.2×10⁻⁵, bound ≤ 10⁻³).

## Consequences

1. **The synchronized reading of the bilateral tax is dead on arrival,
   quantitatively.** If the loading is the smooth classical field Φ —
   one common cause throttling photon and matter coherently — the taxed
   tokens coincide, the joint budget is S·A, and the transit delay
   exactly equals the clock delay: γ = 0, half deflection, falsified by
   1919/1922 and by modern lensing–dynamics agreement. The owner's own
   worked example, taken literally, lands on this branch — that was the
   point of running it.
2. **The A² doubling requires statistically independent microscopic
   busy-schedules** between interaction partners, despite their common
   mean loading. The toy delivers γ = 1/A → 1 in that case, achromatic
   under the rate-proportional levy (D4) and linear at weak load (D5),
   i.e. consistent with R3/R4 inherited constraints — *if* the
   independence can be derived.
3. **The requirement is priced:** γ(c) = (1−c²)/(A + c²(1−A)) at weak
   load gives 1 − γ = c², so Cassini bounds the medium's busy-schedule
   correlation at **c ≤ 4.8×10⁻³**. Either the medium's update
   statistics are incoherent to better than half a percent, or a
   symmetry forces exact independence. Nothing in the LogSE functional
   supplies stochastic schedules at all; the only candidate source in
   the programme is Paper III's update accounting — so H-BILATERAL, if
   opened, depends on Paper III structure, not on anything in
   Papers I/II/IV.
4. **Obligation 2 (rate-proportional levy) is load-bearing:** the
   per-event-latency alternative is chromatic (extra delay ∝ 1/C,
   demonstrated by construction in D4) and would predict chromatic
   lensing, which is excluded. Any derived tax must charge per cycle,
   not per event.
5. **Strong-field prediction of the toy, for the record:** at finite
   load the independent branch gives γ = 1/A = 1/(1−|Φ|/c²) > 1 — a
   specific, in-principle-falsifiable deviation shape if a derived
   H-BILATERAL ever reaches PPN-order tests.

This toy **cannot decide which branch the medium realizes** — it
quantifies what any derivation must deliver. It is an
instrument-validation and constraint-pricing run; the physics question
(does the medium possess decorrelated update statistics?) remains open
and routes to Paper III's update accounting.

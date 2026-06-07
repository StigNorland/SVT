# #94 — HQV electron: verdict on the muon's last route

**Issue:** [#94](https://github.com/StigNorland/SVT/issues/94). The half-quantum
vortex (HQV) was the only remaining route to a muon `γ_B = π` after #91 closed
the IQV spin–orbit lock. **Verdict: HQV REJECTED. The electron is an
integer-winding (IQV) object; the muon `(3/2)μ₀` is a NUMERICAL COINCIDENCE,
final; `pion = 2μ₀` survives unchanged.** Verification:
`instruments/paper_i/hqv_muon_audit.py`, `test_hqv_muon_audit.py` (8 tests).

## Two independent reasons the HQV does not rescue the muon

### 1. Wrong circle (the decisive geometric point)

#94's framing assumed the HQV gives *"azimuthal spin texture `z₀(φ)` winding in
φ"* (the major ring). That is geometrically wrong. The electron is a vortex
**ring**: its core lies **along the major circle**. The HQV winds its phase and
spin disclination around the **core** — i.e. over a **meridional** loop `C_ϑ`
that *links* the core. So `z = z(ϑ)`, **independent of φ**. The two relevant
holonomies live on orthogonal circles (verified, Wilson loop):

| loop | relation to core | holonomy | meaning |
|---|---|---|---|
| meridional `C_ϑ` | **links** the core (lk = 1) | **γ_B = π** | the electron's **spin-½** (#87 B2) |
| major `C_φ` | runs **along** the core (lk = 0) | **γ_B = 0** | the **muon** — not rescued (= #91) |

The HQV's `−1` is the spin-½, on `C_ϑ`. The muon needs `−1` on `C_φ`, where a
mode is transported *along* the disclination line and picks up nothing. **The HQV
is just the electron's spin-½ (the meridional ℤ₂ framing already derived in #87
B2) in another guise** — it does not touch the muon's azimuthal Berry phase.

To put a half-winding on `C_φ` you would need the spin texture to *also* wind
around the major ring — a distinct object, not forced by HQV topology, costing
gradient energy `E ≈ π·(spin stiffness)/R > 0` with no compensating benefit. So
the ring relaxes to φ-uniform: exactly #91's `|V| = 0`, `γ_B = 0`.

### 2. Charge quantization (independent killer)

In SSV electric charge = chirality/winding, and circulation is integer-quantized
(Onsager–Feynman `∮v·dl = n h/m₀`). A **free** HQV has `n = ½` ⇒ **half charge**,
excluded by observation. HQVs can exist only confined in integer-winding pairs
(= an IQV externally). So the free electron is integer-winding regardless — and
`pion = 2μ₀` (built from integer-winding objects, #87 A1) is untouched.

## Energetics (for completeness — no drive to HQV either)

Phase stiffness = spin stiffness = `ρ/ρ₀` exactly (verified Part A identity I2).
At equal stiffness, one IQV (`∝ 1²·ln`) and two HQVs (`∝ (¼+¼)·ln × 2 = 1·ln`)
are **degenerate at leading log** — there is no energetic drive to split the IQV
into HQVs. Subleading chiral-shear plus the charge-confinement string select the
integer-winding configuration.

## Decision and consequences

- **Electron = IQV** (integer winding, unit charge). Its derived properties
  (`R_e = ξ/α`, Lamb `m_e`, `g ≈ 2`, spin-½ via the meridional ℤ₂ #87 B2) all
  stand.
- **`pion = 2μ₀`: survives** (A1 unchanged — the electron and pion are
  integer-winding).
- **Muon `(3/2)μ₀`: NUMERICAL COINCIDENCE, final.** Every route to a half-integer
  Berry phase is now closed: Path A/B (no even spectrum), #76 (`γ_B=0` scalar),
  #91 (`|V|=0` IQV spinor), #94 (HQV is the wrong circle + charge-excluded). The
  0.59% agreement has no deriving mechanism in the CP¹/spinor framework.

## The honest big picture

The CP¹/spinor upgrade (#83/#87) delivered its real prizes — **spin-½** (#87 B2,
the meridional ℤ₂ = the HQV structure), **chirality** (#87 B3), connected SU(4)
(#84) — but it does **not** deliver the muon mass. The muon, like the kaon and ρ
(#93), is a numerical coincidence. SSV's mass wins remain the topological ones:
pion = 2 (winding), proton `N_Y = 3` (crossing number). This is the final state
of the muon question.

# Paper II — Numerical Results

This file records results from the three calculation scripts in `instruments/paper_ii/`.
See `reconnection-barrier-results.md` for the 3D GPE reconnection-barrier checks.

---

## 1. Proton Breather Profile (1D Spherical)

**Script:** `instruments/paper_ii/proton_breather_1d.py`
**Method:** Backward shooting on the radial dimensionless LogSE exterior to a
hard-sphere proton core at `r_core = a_p/xi = m_e/m_p`.

### Static profile

| Quantity | Value |
|---|---|
| Asymptotic amplitude `A*` | 5.470 × 10⁻⁴ |
| `f(r_core)` (target 0) | −3.2 × 10⁻⁵ |
| Core volume `V_core = (4/3)π a_p³` | 6.767 × 10⁻¹⁰ ξ³ |
| Healing-layer integral `V_heal` | 6.849 × 10⁻³ ξ³ |
| Total deficit volume `DV` | 6.849 × 10⁻³ ξ³ |
| `DV / V_core` | 1.01 × 10⁷ |
| RMS deficit radius `R_rms` | 1.732 ξ |
| Asymptotic decay check `λ` | 1.4156 (expected √2 = 1.4142, 0.10% error) |

The healing layer dominates the static deficit by seven orders of magnitude.

### Frequency separation

| Quantity | Value |
|---|---|
| Healing-layer natural frequency `ω₀ = √2 c/ξ` | 1.4142 |
| Proton Compton frequency `ω_p = 1/r_core` | 1836.2 |
| Ratio `ω_p / ω₀` | **1298** |

Because `ω_p ≫ ω₀`, the healing layer is frozen on the proton's pulsation
time scale. The forced response at `ω_p` is suppressed by `(ω₀/ω_p)² ≈ 6 × 10⁻⁷`.
**Only the core volume `V₀` enters the dynamic Bjerknes formula.**

### Bjerknes / gravitational coupling

| Case | `δV` input | `α_G` | Ratio to CODATA | log₁₀(ratio) |
|---|---|---|---|---|
| A — static DV (wrong) | 6.85 × 10⁻³ | 1.642 × 10⁻¹⁹ | 2.78 × 10¹⁹ | +19.4 |
| **B — core V₀ (correct)** | 6.77 × 10⁻¹⁰ | **1.603 × 10⁻³³** | **2.71 × 10⁵** | **+5.4** |

CODATA: `α_G = 5.906 × 10⁻³⁹`.

The Paper II formula with `δV = V₀` gives `α_G ≈ 1.6 × 10⁻³³`, a factor **~3 × 10⁵**
above CODATA. This residual factor is attributed to the 3D trefoil geometry
(open calculation: `instruments/paper_i/`).

---

## 2. Time Dilation Check (Symbolic)

**Script:** `instruments/paper_ii/time_dilation_check.py`
**Method:** SymPy — exact symbolic verification using Paper I conventions.

### Result

The local **longitudinal (Bogoliubov) sound speed** reproduces GR weak-field
time dilation exactly at leading order:

```
c_s(ρ) / c_s(ρ₀) = √(ρ/ρ₀) ≈ 1 + Φ/c²
```

This matches the GR result `tick(x)/tick(∞) ≈ 1 + Φ/c²` for `Φ < 0` near a mass.

The **chiral-shear mode** (speed `c_⊥ = α c`) gives the **wrong sign**: in a
rarefied region `c_⊥` increases (faster mode → faster ticks), opposite to GR.

| Mode | `c(ρ)/c(ρ₀)` at leading order | Sign vs GR |
|---|---|---|
| Longitudinal (Bogoliubov) | `1 + Φ/c²` | ✓ correct |
| Chiral-shear | `1 − Φ/c²` | ✗ wrong sign |

**Implication:** gravitational time dilation in SSV is carried by the
longitudinal channel, consistent with Volovik's acoustic-metric programme.
The photon must be a longitudinal Goldstone phase mode, not a chiral-shear mode.

---

## 3. Vortex Cap Mass: W/Z Masses and Weinberg Angle

**Script:** `instruments/paper_ii/vortex_cap_mass.py`
**Method:** Imports the corrected Paper I coefficient-one profile; numerical line tension
integral + analytic Paper II golden-ratio cap formula.

### Corrected vortex core profile

| Quantity | Value |
|---|---|
| Core slope `a` (f ~ a·r) | 0.806588 |
| `r(f = 0.5)` | 0.753 ξ |
| `r(f = 0.9)` | 2.520 ξ |

**Algebraic tail:** The corrected 2D LogSE vortex has `1 − f ~ 1/(2r²)` at
large r — an algebraic, not exponential, approach to the background. This
arises from the `−f/r²` winding term acting as a source. Verified numerically:

| r | 1 − f | 1/(4r²) | ratio |
|---|---|---|---|
| 5 | 0.022142 | 0.020000 | 1.107 |
| 8 | 0.008068 | 0.007812 | 1.033 |
| 10 | 0.005094 | 0.005000 | 1.019 |
| 12 | 0.003481 | 0.003472 | 1.003 |

### Vortex line tension

The corrected shifted energy is
`0.5[f′²+(f/r)²] + 0.5[ρ ln ρ−ρ+1]`. Only the phase kinetic term has a
logarithmic tail; the shifted potential falls as `r⁻⁴`. The leading tail is
therefore `π ln(R_cap/r_max)`, not the old doubled expression.

| Component | Corrected value |
|---|---|
| τ_core (numerical, r < 15 ξ) | 10.1625 |
| τ_tail (analytic, π ln(221.7/15)) | 8.4616 |
| **τ_total** | **18.6241** |

### Force-balance vs golden-ratio conjecture

Simple surface-tension estimate: `R_cap ~ τ_phys`:

| Estimate | `R_cap` |
|---|---|
| Pure LogSE line tension | 18.6 ξ |
| Paper II golden ratio (`φ/α`) | 221.7 ξ |
| **Enhancement factor** | **~11.9×** |

The pure LogSE cannot stabilise a cap at `R_cap = φ/α`. The chiral-shear
coupling `λ_⊥ ~ α⁻²  ≈ 18800` must supply the additional stiffness.
This is the open chiral-shear equilibrium calculation in Paper II §4.

### W/Z masses (Paper II analytic)

Cap energy formula: `E_cap = π R_cap² m_e c²` (with `P₀ = ξ = 1`, `R_cap = φ/α`).

| Observable | SSV (this run) | Observed (PDG 2023) | Gap |
|---|---|---|---|
| `m_W` | 78.925 GeV | 80.377 GeV | −1.81% |
| `m_Z` (tree-level) | 90.015 GeV | 91.188 GeV | −1.29% |
| `sin²(θ_W)` from PDG | — | 0.23122 | (input) |
| `sin²(θ_W)` from `m_W/m_Z` | — | 0.22306 | Δ = 0.008 (rad. corr.) |

Tree-level relation used: `cos(θ_W) = m_W/m_Z`.

Implied `R_cap_Z` from the observed `m_Z` and the SSV `m_W`:
`R_cap_Z = 238.3 ξ`  (`R_cap_Z / R_cap_W = 1.075`, vs `1/cos(θ_W) = 1.140`).

### Open gapboxes (Paper II §4)

1. **Derive `R_cap = φ/α` from chiral-shear equilibrium** — pure LogSE gives
   `R_cap ~ 18.6 ξ`; the actual cap-setting dynamics remains open.
2. **Derive `sin²(θ_W) = 0.231` from amplitude/phase cap mixing** — requires the
   full `λ_⊥` calculation at the Z-channel saddle (see `reconnection-barrier-results.md`).

---

## 4. Chiral-Cap Equilibrium: Candidate-model inversion

**Script:** `instruments/paper_ii/chiral_cap_equilibrium.py`
**Method:** Variational energy model for a closed vortex ring with corrected
line tension τ and chiral-shear bending stiffness λ_bend. It solves the
equilibrium cubic after imposing a target radius; it does not derive that
radius or stiffness from the SSV Lagrangian.

### Energy model

```
E(R) = π R² + 2π τ R + 2π λ_bend/R
```

- `π R²`: surface pressure (cap area × background pressure P₀ = 1)
- `2π τ R`: vortex line-tension perimeter term
- `2π λ_bend/R`: chiral-shear bending resistance (outward)

Equilibrium condition `dE/dR = 0`:

```
R³ + τ R² = λ_bend   (equilibrium cubic)
```

### Required bending stiffness

| Quantity | Value |
|---|---|
| Target `R_cap = φ/α` | 221.73 ξ |
| `λ*_bend = R_cap³ + τ R_cap²` | 1.1817 × 10⁷ ξ³ |
| `λ*_bend / (φ/α)³` | 1.084 |
| τ-correction `τ R_cap²/R_cap³` | 8.4% |
| **τ→0 limit: `λ*_0 = (φ/α)³`** | **exact (0.000% error)** |
| `λ*_0 × α³` | 4.2361 = **φ³** ✓ |

### Algebraic golden-ratio restatement (τ→0)

Define `x = α R/ξ`. At equilibrium: `x³ = α³ λ*_0`. With `λ*_0 = φ³/α³`:

```
x³ = φ³  ⟹  x = φ = 1.618034
```

The golden ratio satisfies `φ² = φ + 1` by definition. Since
`R_cap = φ/α` was imposed, the inversion necessarily returns
`λ_bend,0 = φ³/α³`. This is a tautological consistency check, not an
independent fixed point or a physical origin for φ.

| Check | LHS | RHS | Match |
|---|---|---|---|
| `λ*_0 α³` | 4.2361 | `φ³` = 4.2361 | ✓ |
| `φ² = φ+1` | 2.6180 | 2.6180 | ✓ |
| `d²E/dR²` at R_eq | 18.85 | > 0 | ✓ (minimum) |
| `E_cs/E_P` at equil. | 2.153 | ~2 (virial) | ✓ |

### Dimensional candidate, not an identification

In SSV the chiral-shear mode has speed `c_⊥ = α c`, so:

```
λ_bend* = φ³ × (c/c_⊥)³ × ξ³ = φ³/α³ × ξ³
```

The speed ratio permits this dimensional scaling, but does not derive the
power, coefficient, or physical running/non-local mechanism.

| Component | Value |
|---|---|
| `(c/c_⊥)³ = α⁻³` | 2.5734 × 10⁶ |
| `φ³` | 4.2361 |
| `λ_bend*` (ξ units) | 1.0901 × 10⁷ ξ³ |
| `λ_bend*` (SI) | 6.277 × 10⁻³¹ m³ |

### Energy at equilibrium

| Component | Fraction of E_total |
|---|---|
| `E_pressure = π R²` | 30.2% |
| `E_line = 2π τ R` | 5.0% |
| `E_chiral = 2π λ/R` | 65.0% |

The chiral-shear bending term dominates; pressure and line tension are subdominant.

### Status

**Genuinely open.** The cubic maps an assumed cap radius to a required
stiffness. The corrected local-core calculation is 380× too small, and the
former linear-running near-match does not survive. A cap-setting mechanism
must be derived without inserting `R_cap`, `λ_bend`, or the observed W mass.

---

## 5. L_⊥ Core Integral: Bending Stiffness Check

**Script:** `instruments/paper_ii/lperp_core_integral.py`
**Method:** Numerically integrates I_curl, J_bend, K_bend from the corrected
coefficient-one planar vortex profile (reliable up to r < 15 ξ).

### Core integrals

| Integral | Definition | Corrected value |
|---|---|---|
| `I_curl` | `∫ (2ff′/r)² 2πr dr` | 2.5098 |
| `J_bend` | `∫ r² [∂_r(2ff′/r)]² 2πr dr` | 3.9065 |
| `K_bend` | `∫ (2ff′/r)² r² 2πr dr` | 2.20 |

**Tail convergence:** All integrands fall as `~1/r⁷` for large r. The analytic tail from r > 15 ξ contributes < 10⁻⁶ of the total.

### Bending formula result

The local curvature correction to L_⊥ gives:

```
λ_bend(local) = λ_⊥ × (J_bend + K_bend) / 4
```

With `λ_⊥ = α⁻²` (natural SSV scale):

| Quantity | Value |
|---|---|
| `λ_⊥ = α⁻²` | 1.878 × 10⁴ |
| `λ_bend(local) = λ_⊥ (J+K)/4` | 2.868 × 10⁴ |
| `λ_bend(required) = φ³/α³` | 1.09 × 10⁷ |
| **Gap factor** | **380×** |

### Conclusion

The local curvature-of-core correction to L_⊥ is **380× too small** to reproduce
λ_bend = φ³/α³. The 2πλ_bend/R energy term therefore does NOT arise from local
vortex core bending. The physical mechanism must be non-local:

- **Candidate**: The cap is the Seifert surface of the trefoil knot. Its chiral-shear
  energy may be quantized at λ_bend = φ³/α³ from the knot invariant structure
  (non-perturbative topological origin).
- **Candidate**: The chiral-mode vacuum energy of the reconnection region (analog of
  the Casimir effect between parallel plates, here applied to the ring boundary).

**Status: local mechanism excluded; cap mechanism open.** The candidate cubic
can state what stiffness an imposed radius would require, but neither that
stiffness nor the cap radius is derived from the SSV Lagrangian.

---

## 6. Weinberg Angle: sin²(θ_W) from Cap Structure

**Script:** `instruments/paper_ii/weinberg_angle.py`
**Method:** Cap energy formula E = π R² m_e c² applied to W and Z caps; equilibrium cubic for Z; golden-ratio coincidence check.

### Mass formula and tree-level structure

In SSV, m_cap = π R_cap² m_e c² (P₀ = ξ = 1), so m ∝ R². The SM tree-level relation
m_W = m_Z cos(θ_W) translates to R_cap_W / R_cap_Z = √cos(θ_W).

| Quantity | SSV result | PDG | Gap |
|---|---|---|---|
| `m_W` | 78.925 GeV | 80.377 GeV | −1.81% |
| `m_Z` (tree, PDG θ_W input) | 90.015 GeV | 91.188 GeV | −1.29% |
| `sin²(θ_W)` from SSV m_W/m_Z | 0.23122 | 0.23122 | = PDG (by SM input) |
| `sin²(θ_W)` PDG tree-level | 0.22306 | 0.23122 | Δ = 0.00816 (rad. corr.) |

Both SSV masses are ~1.3–1.8% below PDG; their ratio preserves the SM relation by construction when PDG θ_W is used as input.

### Z cap radius

| Estimate | `R_cap_Z` |
|---|---|
| From PDG m_Z | 238.33 ξ |
| SSV tree-level: R_W/√cos(θ_W) | 236.79 ξ |
| Gap | 0.65% (= same 1.29% mass gap) |

Note: the correct SSV relation is R_cap_Z = R_cap_W/√cos(θ_W), NOT R_cap_W/cos(θ_W),
because the mass formula is m ∝ R² (not m ∝ R).

### Equilibrium cubic for Z

| Quantity | Value |
|---|---|
| `λ_bend_W = φ³/α³` | 1.09 × 10⁷ ξ³ |
| `λ_bend_Z` (cubic, PDG R_cap_Z) | 1.45 × 10⁷ ξ³ |
| `λ_bend_Z / λ_bend_W` | 1.2357 |
| `1/cos^(3/2)(θ_W)` (τ→0 prediction) | 1.2180 |
| Agreement with τ→0 limit | +1.46% |

The τ→0 limit (R_Z/R_W)³ = 1/cos^(3/2)(θ_W) holds to within the τ-correction level.

### Golden-ratio coincidences

| Formula | Value | Δ from PDG |
|---|---|---|
| `φ/7` | 0.23115 | −0.031% |
| `3/(8φ)` | 0.23176 | +0.235% |

**Best lead:** φ/7 ≈ sin²(θ_W) to 0.03%. If exact, implies:
cos(θ_W) = √((7−φ)/7) = 0.876842 vs PDG 0.876801 (Δ = 0.005%).

### Isospin mixing scaling argument

At R_cap_W: phase-mode stiffness ~ τ = 17 ξ (line tension);
amplitude-mode stiffness ~ λ_⊥/R_cap = α⁻²/R_cap.

tan²(θ_W) ~ τ/(λ_⊥/R_cap) = τ α² R_cap = 17 × α² × 221.7 = **0.200**

vs tan²(θ_W) = 0.301. Factor ~1.5 off — correct order of magnitude.

### Status

**Open gapbox.** Two routes remain:
1. Derive cos(θ_W) = √((7−φ)/7) from the SSV chiral-shear amplitude-phase mixing
   (requires identifying the factor-7 in the R_cap_W = φ/α formula).
2. Derive the exact coefficient in tan²(θ_W) ~ τ α² R_cap from the SSV Lagrangian.

---

## 7. Corrected 380× Gap Investigation — Three Steps

Three targeted checks probe the corrected gap between
`λ_bend(local) = 2.868 × 10⁴` and the candidate required
`λ_bend* = φ³/α³ = 1.09 × 10⁷`.

### Step 1: b=1/2 physical vortex profile

**Script:** `instruments/paper_ii/lperp_bphys_check.py`

The coefficient-two solver is now a legacy control. The active
coefficient-one conventional-xi profile obeys the exact rescaling
`f_corrected(r) = f_legacy(r/√2)`:
J_bend_phys = J_bend_b1/2, K_bend_phys = K_bend_b1.

| Quantity | b=1 | b=1/2 | Target |
|---|---|---|---|
| J_bend | 7.810 | 3.907 | — |
| K_bend | 2.201 | 2.203 | — |
| (J+K)/4 | 2.503 | 1.527 | φ² = 2.618 |
| Gap factor | 232× | 380× | 1× |

**Analytic rescaling confirmed below 0.06%.** The corrected baseline makes
the gap **larger** (380× vs the legacy-control 232×). The gap is not removed
by the convention correction.

### Step 2: J_bend(r_max) convergence sweep

**Script:** `instruments/paper_ii/jbend_ring_scaling.py`

Sweeps the integral upper limit r_max from 1 to 15 ξ to check for an IR tail.

| r_max/ξ | corrected J_bend | corrected K_bend | (J+K)/4 |
|---|---|---|---|
| 1 | 0.996 | 0.627 | 0.406 |
| 3 | 3.760 | 2.079 | 1.460 |
| 5 | 3.898 | 2.188 | 1.522 |
| 8 | 3.904 | 2.200 | 1.526 |
| 12 | 3.905 | 2.201 | 1.526 |
| 15 | 3.907 | 2.203 | 1.527 |

**Change from r_max = 5 to r_max = 15: +0.38%.** The integrals saturate within
the vortex core (~5 ξ). There is no IR tail from extending the integration to
larger radii. The gap is UV-local, not IR.

Note: the b=1 LogSE has an e^{2r} growing mode — numerical integration beyond
~15 ξ is unstable. The convergence within r ≤ 15 ξ is decisive.

### Step 3: Kelvin wave renormalization

**Script:** `instruments/paper_ii/kelvin_wave_renorm.py`

Two mechanisms checked:

**(A) Classical LIA (Local Induction Approximation):**
```
λ_bend_LIA(R) = (κ²/4π) R ln(R/ξ)
```
At R_cap = φ/α: λ_bend_LIA = 3.76 × 10³ — only 8% of the core contribution
and 0.03% of the target. The LIA scales as R ln(R/ξ), not linearly.

**(B) One-loop Kelvin wave integral:**

Integrating out Kelvin modes from k = 1/R to k = 1/ξ with LIA dispersion
ω_K ~ k² ln(1/kξ):

| R/ξ | I_dlnk | ln(R/ξ) |
|---|---|---|
| 10 | 1.33 | 2.30 |
| 50 | 3.83 | 3.91 |
| 100 | 5.30 | 4.61 |
| R_cap = 221.7 | 7.29 | 5.40 |

Fit: I_dlnk = 1.750 × ln(R/ξ) − 2.63. The one-loop correction scales as
**ln(R/ξ)**, not linearly.

**(C) Power-law running λ_⊥(R) = λ_⊥(ξ) × (R/ξ)^p:**

| p | corrected λ_bend at R_cap | gap |
|---|---|---|
| 0 (constant) | 2.87 × 10⁴ | 380× |
| 1/2 | 4.27 × 10⁵ | 25.5× |
| **1 (linear)** | **6.36 × 10⁶** | **1.714×** |
| 3/2 | 9.47 × 10⁷ | 0.115× |

For **p = 1 (linear running)** the corrected result is still **41.7% below
target**. The former 4.4% match was a legacy-profile normalization
coincidence.

### Gap anatomy

The gap decomposes as:
```
Gap = φ²/(J+K)/4 × (φ/α)/(1) = φ³/(α × (J+K)/4)
```

The factor R_cap/ξ = φ/α ≈ 222 is an IR scale, while the corrected
`(J+K)/4 ≈ 1.527` is a UV core integral. A single factor of
`R_cap/xi` is insufficient because `φ²/1.527 ≈ 1.714`.

### Conclusions

| Mechanism | Enhancement | Sufficient? |
|---|---|---|
| b=1/2 convention | × (worsens gap) | No |
| Extended core integral (tail) | <0.1% | No |
| Classical LIA | R ln(R/ξ) ≈ 1.2 × 10³ | No (0.03% of target) |
| Kelvin wave one-loop | O(ln R/ξ) ≈ 5.4× | No (insufficient by 41×) |
| Linear running (p=1) | R/ξ ≈ 222× | **No (41.7% short)** |

The corrected 380× gap is not closed by the tested local, LIA, one-loop, or
simple p=1 running mechanisms. A stronger anomalous/non-local contribution
would be a new hypothesis, not an inference from this calculation.

All local perturbative mechanisms (core integrals, LIA, Kelvin waves) are
insufficient by 1–2 orders of magnitude.

---

## Summary table

| Sector | Observable | SSV result | CODATA/PDG | Status |
|---|---|---|---|---|
| Gravity | `α_G` (1D spherical) | 1.60 × 10⁻³³ | 5.91 × 10⁻³⁹ | ×3×10⁵ gap → 3D trefoil |
| Metric | Time dilation | longitudinal mode ✓ | GR `1+Φ/c²` | Confirmed symbolically |
| Electroweak | `m_W` | 78.93 GeV | 80.38 GeV | −1.81% |
| Electroweak | `m_Z` (tree) | 90.02 GeV | 91.19 GeV | −1.29% |
| Electroweak | `sin²(θ_W)` tree (SSV) | 0.23122 | 0.23122 | = PDG by SM input; tree deficit 0.008 same as SM |
| Electroweak | `sin²(θ_W)` open lead | φ/7 = 0.23115 | 0.23122 | 0.031% — no derivation yet |
| Electroweak | `R_cap = φ/α` | imposed cap radius | post-hoc conditional formula | Corrected local stiffness is 380× too small; mechanism open |

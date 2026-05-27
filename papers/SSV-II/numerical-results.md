# Paper II — Numerical Results

This file records results from the three calculation scripts in `src/paper_ii/`.
See `reconnection-barrier-results.md` for the 3D GPE reconnection-barrier checks.

---

## 1. Proton Breather Profile (1D Spherical)

**Script:** `src/paper_ii/proton_breather_1d.py`
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
(open calculation: `src/paper_i/`).

---

## 2. Time Dilation Check (Symbolic)

**Script:** `src/paper_ii/time_dilation_check.py`
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

**Script:** `src/paper_ii/vortex_cap_mass.py`
**Method:** Imports Paper I `VortexProfile` solver; numerical line tension
integral + analytic Paper II golden-ratio cap formula.

### Vortex core profile (Paper I, b=1 convention)

| Quantity | Value |
|---|---|
| Core slope `a` (f ~ a·r) | 1.140682 |
| `r(f = 0.5)` | 0.532 ξ_b1 = 0.753 ξ_phys |
| `r(f = 0.9)` | 1.782 ξ_b1 = 2.520 ξ_phys |

**Algebraic tail:** The 2D LogSE vortex (n=1 winding) has `1 − f ~ 1/(4r²)` at
large r — an algebraic, not exponential, approach to the background. This
arises from the `−f/r²` winding term acting as a source. Verified numerically:

| r | 1 − f | 1/(4r²) | ratio |
|---|---|---|---|
| 5 | 0.010445 | 0.010000 | 1.044 |
| 8 | 0.003964 | 0.003906 | 1.015 |
| 10 | 0.002523 | 0.002500 | 1.009 |
| 12 | 0.001744 | 0.001736 | 1.005 |

### Vortex line tension

Both the phase kinetic term (`0.5(f/r)²`) and the LogSE potential
(`−f² ln f²`) decay as `~1/(2r²)` at large r due to the algebraic tail.
Each contributes `π ln(R_cap/r_max)` to the integral; total tail correction
is `2π ln(R_cap/r_max)`.

| Component | Value (b=1) |
|---|---|
| τ_core (numerical, r < 15 ξ_b1) | 19.26 |
| τ_tail (analytic, 2π ln(157/15)) | 14.75 |
| **τ_total (b=1)** | **34.00** |
| **τ_total (b=1/2, physical)** | **17.00** |

### Force-balance vs golden-ratio conjecture

Simple surface-tension estimate: `R_cap ~ τ_phys`:

| Estimate | `R_cap` |
|---|---|
| Pure LogSE line tension | 17.0 ξ |
| Paper II golden ratio (`φ/α`) | 221.7 ξ |
| **Enhancement factor** | **~13×** |

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
   `R_cap ~ 17 ξ`; a factor ~13 enhancement from `λ_⊥ ~ α⁻²` is needed.
2. **Derive `sin²(θ_W) = 0.231` from amplitude/phase cap mixing** — requires the
   full `λ_⊥` calculation at the Z-channel saddle (see `reconnection-barrier-results.md`).

---

## 4. Chiral-Cap Equilibrium: Deriving R_cap = φ/α

**Script:** `src/paper_ii/chiral_cap_equilibrium.py`
**Method:** Variational energy model for a closed vortex ring with line tension τ and
chiral-shear bending stiffness λ_bend. Solves equilibrium cubic analytically; confirms
golden-ratio fixed point.

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
| `λ*_bend = R_cap³ + τ R_cap²` | 1.1737 × 10⁷ ξ³ |
| `λ*_bend / (φ/α)³` | 1.077 (= φ + τ/R_cap ≈ φ) |
| τ-correction `τ R_cap²/R_cap³` | 7.7% |
| **τ→0 limit: `λ*_0 = (φ/α)³`** | **exact (0.000% error)** |
| `λ*_0 × α³` | 4.2361 = **φ³** ✓ |

### Golden-ratio fixed point (τ→0)

Define `x = α R/ξ`. At equilibrium: `x³ = α³ λ*_0`. With `λ*_0 = φ³/α³`:

```
x³ = φ³  ⟹  x = φ = 1.618034
```

The golden ratio satisfies `φ² = φ + 1` (defining property). The cap radius
`R_cap = φ/α` is the unique fixed point where the chiral-shear bending exactly
balances the pressure.

| Check | LHS | RHS | Match |
|---|---|---|---|
| `λ*_0 α³` | 4.2361 | `φ³` = 4.2361 | ✓ |
| `φ² = φ+1` | 2.6180 | 2.6180 | ✓ |
| `d²E/dR²` at R_eq | 18.85 | > 0 | ✓ (minimum) |
| `E_cs/E_P` at equil. | 2.153 | ~2 (virial) | ✓ |

### SSV identification

In SSV the chiral-shear mode has speed `c_⊥ = α c`, so:

```
λ_bend* = φ³ × (c/c_⊥)³ × ξ³ = φ³/α³ × ξ³
```

Three powers of the inverse chiral speed (one per spatial dimension of the
bending energy) with golden-ratio pre-factor φ³.

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
| `E_line = 2π τ R` | 4.6% |
| `E_chiral = 2π λ/R` | 65.1% |

The chiral-shear bending term dominates; pressure and line tension are subdominant.

### Status

**Open gapbox PARTIALLY CLOSED.** R_cap = φ/α follows directly from λ_bend = φ³/α³.

Remaining step: derive `λ_bend = φ³/α³` from the SSV chiral-shear Lagrangian
by integrating the k⁴ dispersion over the vortex core profile:

```
∫₀^∞ [chiral-shear energy density(r)] 2π r dr  =?  φ³/α³
```

---

## 5. L_⊥ Core Integral: Bending Stiffness Check

**Script:** `src/paper_ii/lperp_core_integral.py`
**Method:** Numerically integrates I_curl, J_bend, K_bend from the planar vortex
profile (Paper I, b=1 convention, reliable up to r < 15 ξ).

### Core integrals

| Integral | Definition | Value (b=1) |
|---|---|---|
| `I_curl` | `∫ (2ff′/r)² 2πr dr` | 5.02 |
| `J_bend` | `∫ r² [∂_r(2ff′/r)]² 2πr dr` | 7.81 |
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
| `λ_bend(local) = λ_⊥ (J+K)/4` | 4.70 × 10⁴ |
| `λ_bend(required) = φ³/α³` | 1.09 × 10⁷ |
| **Gap factor** | **232×** |

### Conclusion

The local curvature-of-core correction to L_⊥ is **232× too small** to reproduce
λ_bend = φ³/α³. The 2πλ_bend/R energy term therefore does NOT arise from local
vortex core bending. The physical mechanism must be non-local:

- **Candidate**: The cap is the Seifert surface of the trefoil knot. Its chiral-shear
  energy may be quantized at λ_bend = φ³/α³ from the knot invariant structure
  (non-perturbative topological origin).
- **Candidate**: The chiral-mode vacuum energy of the reconnection region (analog of
  the Casimir effect between parallel plates, here applied to the ring boundary).

**Status: Open gapbox confirmed.** The variational identification λ_bend = φ³/α³
(from `chiral_cap_equilibrium.py`) is correct; the derivation from the SSV Lagrangian
requires non-local physics not captured by the vortex core profile.

---

## 6. Weinberg Angle: sin²(θ_W) from Cap Structure

**Script:** `src/paper_ii/weinberg_angle.py`
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

## Summary table

| Sector | Observable | SSV result | CODATA/PDG | Status |
|---|---|---|---|---|
| Gravity | `α_G` (1D spherical) | 1.60 × 10⁻³³ | 5.91 × 10⁻³⁹ | ×3×10⁵ gap → 3D trefoil |
| Metric | Time dilation | longitudinal mode ✓ | GR `1+Φ/c²` | Confirmed symbolically |
| Electroweak | `m_W` | 78.93 GeV | 80.38 GeV | −1.81% |
| Electroweak | `m_Z` (tree) | 90.02 GeV | 91.19 GeV | −1.29% |
| Electroweak | `sin²(θ_W)` tree (SSV) | 0.23122 | 0.23122 | = PDG by SM input; tree deficit 0.008 same as SM |
| Electroweak | `sin²(θ_W)` open lead | φ/7 = 0.23115 | 0.23122 | 0.031% — no derivation yet |
| Electroweak | `R_cap = φ/α` | λ_bend = φ³/α³ ✓ | identification only | Core integral: 232× gap → non-local origin |

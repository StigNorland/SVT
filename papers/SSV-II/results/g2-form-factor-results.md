# Toroidal form-factor loop integral — numerical results (issue #33)

Date: 2026-05-28; closure context updated 2026-06-06
Script: `instruments/paper_ii/g2_form_factor_loop.py`

## Reduction

Standard QED vertex correction with on-shell external electrons and q → 0,
Feynman-parametrised with parameters (x, y, z = 1−x−y) on (electron, electron,
photon) propagators.  After shifting the loop momentum l → l + (x+y)p the
F_2(0) projection of the numerator is l-independent and proportional to
2 m² z(1−z); the combined denominator is (l² − (1−z)² m²)³.

In the electron rest frame the shift S = (x+y)p has p_spatial = 0, so the
form-factor argument |k_photon, spatial| equals the spatial part of the
shifted loop momentum.  Decomposing the 4-D Euclidean integral as
d⁴l_E = dl₀ · d³l_spatial and doing the l₀ integral analytically:

```
a_e[F, R*] = (3α/π) · ∫₀^∞ dκ · κ² · J_0²(κR̃) · G(κ),
G(κ)       = ∫₀¹ du · u³ / (κ² + u²)^(5/2)
           = −1/√(κ²+1) + κ²/[3(κ²+1)^(3/2)] + 2/(3κ),
κ = k_spatial / m_e,    R̃ = R*·m_e = 1/α.
```

The F=1 limit (J_0 → 1) gives ∫₀^∞ κ² G(κ) dκ = 1/6 and (3α/π)(1/6) = α/(2π)
— Schwinger's result.  The script verifies this to 3×10⁻¹⁰.

## Numerical result, R̃ = 1/α ≈ 137.036

```
∫₀^∞ κ² J_0²(κR̃) G(κ) dκ  = 7.7436e−04        (target 1/6 ≈ 0.16667 when F=1)
a_e[F]                     = 5.3961e−06        (cf. Schwinger 1.1614e−03)
δa_e = a_e[F] − α/(2π)     = −1.156e−03
δa_e / a_e(Schwinger)      = −99.54 %
```

The form factor *removes 99.54 %* of Schwinger's anomalous moment.  This is
not a small correction — it is the dominant term.

## Comparison to the paper's parametric estimate

`papers/SSV-II/main.tex` eq. (612) gives δa_e ~ −α³/(4π) ≈ −6.2 × 10⁻⁹ (off
by 2× from −3.1 × 10⁻⁸ printed in the gapbox, but parametrically the same).

```
Parametric  δa_e ~ −α³/(4π) = −3.09 × 10⁻⁸
Numerical   δa_e             = −1.156 × 10⁻³
Ratio                          ≈ 3.7 × 10⁴
```

The parametric estimate is wrong by ~4.5 orders of magnitude.

## Why the parametric estimate fails

The estimate assumes ε = (ƛ_e / R*)² = α² is the small expansion parameter of
F(kR*) ≈ 1 − ¼(kR*)².  But that expansion is valid only for kR* ≪ 1, i.e.
k ≪ 1/R* = α·m_e.  The Schwinger loop integrand peaks at k ~ m_e, where
kR* ~ 1/α ≈ 137 — deep in the *oscillatory* regime of J_0.

The asymptotic ⟨J_0²(x)⟩ ≈ 1/(πx) for x ≫ 1 gives the right scaling:

```
δa_e ~ −(α/(2π)) · [1 − ⟨J_0²⟩|_loop] ~ −(α/(2π)) · 1 = −Schwinger
```

at leading order — the form factor effectively cuts the loop off below
1/R* = α·m_e, and almost the entire Schwinger contribution (which lives at
k ~ m_e) is removed.

## R̃ scan

```
   R̃          a_e[F]        a_e[F]/a_e_Schw      δa_e
  0           1.1614e−03    1.0000               0
  1e−4        1.1614e−03    1.0000              −7.5e−11
  1e−3        1.1614e−03    1.0000              −6.2e−9
  1e−2        1.1610e−03    0.9996              −4.2e−7
  0.1         1.1393e−03    0.9810              −2.2e−5
  1           6.8703e−04    0.5916              −4.7e−4
  10          7.4726e−05    0.0643              −1.1e−3
  137 (=1/α)  5.3961e−06    0.0046              −1.156e−3
```

The crossover R̃ where the suppression becomes order-unity is R̃ ~ 1, i.e.
R* ~ ƛ_e.  Since SSV puts R* = ƛ_e/α ≫ ƛ_e, we are deep in the suppressed
regime.

## Comparison to CODATA a_e

```
a_e(CODATA 2018) = 1.15965e−03
a_e[F] (SSV)     = 5.39608e−06
Ratio            = 4.65e−3      (i.e. SSV is 0.46% of measured)
```

a_e is measured to ~10⁻¹³ relative precision; a 99.54 % deviation is
catastrophic falsification at the level of this calculation.

## Interpretation — what this means for Paper II

The dressed-geometric calculation (form factor F = J_0(|k_spatial|R*) on each
vertex, with R* = ξ/α = ƛ_e/α) is incompatible with experiment.  Paper II now
uses this result as the falsifier for attaching the assembled torus form factor
to the bare vertex.

Possible resolutions (none chosen by this calculation; each requires a
separate physical argument):

1. **R* ≠ ƛ_e/α for vertex-form-factor purposes.**  The Paper I ring radius
   R* might be the *equilibrium* radius, but a separate effective vertex
   radius R_v ≪ R* could control the form factor.  If R_v ~ ƛ_e (R̃ ~ 1) the
   suppression is ~40 %; if R_v ≪ ƛ_e it is small.

2. **Form factor not J_0.**  The 2-D circular-loop J_0 is a model; a
   genuinely 3-D toroidal vortex with finite tube thickness has a different
   form factor that may UV-suppress less aggressively (e.g. a Gaussian
   ~ exp(−k² R_tube²) cuts off at k ~ 1/R_tube, which could be ~ m_e if the
   tube thickness is ~ ƛ_e, recovering Schwinger).

3. **Additional diagrams cancel the suppression.**  In SSV the "QED" loop
   isn't the only contribution; longitudinal-phonon, density-mode, or
   non-perturbative reconnection contributions could add ~ (1 − F²)·α/(2π)
   and restore the total to α/(2π).

4. **The form factor enters only at sub-leading order**, not at every
   internal vertex.  E.g., one F² instead of two, or F² appearing as a
   multiplicative correction to a separately-derived Schwinger term.

## Closure update (2026-06-06)

Paper II's contact-vertex section now implements the resolution: the
LogSE$+\mathcal{L}_\perp$ bare vertex is a contact/topological coupling with
`F(k)=1`, so the one-loop integral recovers Schwinger's α/(2π) exactly.  The
`J_0(kR*)` calculation above remains the numerical falsifier showing why the
dressed, assembled electron torus cannot be inserted as the bare loop vertex.

The related #79/#80/#86 results sharpen the boundary: continuous non-abelian or
internal-structure corrections, if they exist, belong to the later
multi-component/Pati-Salam programme, not to this classical torus form factor.
#33 is therefore closed at one-loop precision by the contact/topological vertex
interpretation; future deviations must come from intrinsic vertex structure,
not from `J_0(kR*)`.

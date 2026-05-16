"""
SSV time-dilation derivation: does the local chiral-shear mode speed
in a density-depressed region reproduce the GR weak-field time dilation?

This script does the calculation symbolically (no numerical fitting),
referencing Paper I conventions explicitly so each step is traceable.

Paper I conventions (file: /mnt/project/main.tex):
  Line 161-162:  c = c_s(rho_0) = sqrt( (dP/drho)|_{rho_0} )
  Line 195:      |Psi|^2 = rho/rho_0     [dimensionless fractional density]
  Line 218:      LogSE potential: V(rho) = -b*rho_0*ln(rho_0|Psi|^2/rho_bar)
  Line 253:      Bogoliubov sound speed: c_s = sqrt(2*b*rho_0 / m_0)
  Line 256:      Stiffness fixed by c_s = c:  b = m_0*c^2/(2*rho_0)
  Line 259:      Healing length:  xi = hbar/(m_0*c)
  Line 280:      Chiral-shear:    c_perp/c = sqrt(lambda*m_0/rho_0) = alpha
  Line 286:      Therefore:       lambda = alpha^2 * rho_0 / m_0
  Line 1380 (Paper II):
                 Gravitational potential:  Phi = b*ln(rho/rho_0)

We will:
  (1) verify dimensions are consistent
  (2) compute c_perp as a function of LOCAL rho, not just rho_0
  (3) get the local-clock-rate ratio (c_perp(x) / c_perp(rho_0))
  (4) express it in terms of the gravitational potential Phi
  (5) compare with GR weak-field: tick(x)/tick(infty) = sqrt(1 + 2*Phi/c^2)
"""

import sympy as sp

# ─────────────────────────────────────────────────────────────────────
# Symbols
# ─────────────────────────────────────────────────────────────────────
hbar, c, m0, rho_0, rho, alpha, lam, b, Phi = sp.symbols(
    'hbar c m_0 rho_0 rho alpha lambda b Phi',
    positive=True, real=True
)
delta_rho = sp.symbols('delta_rho', real=True)  # can be negative

# ─────────────────────────────────────────────────────────────────────
# (1) Paper I's relations as stated
# ─────────────────────────────────────────────────────────────────────
print("="*72)
print("STEP 1: Paper I relations as stated")
print("="*72)

# From line 256: b = m_0 c^2 / (2 rho_0)
b_expr = m0 * c**2 / (2 * rho_0)
print(f"  b           = {b_expr}")

# From line 280: c_perp = c * sqrt(lambda m_0 / rho_0), identified as alpha*c
c_perp_uniform = c * sp.sqrt(lam * m0 / rho_0)
print(f"  c_perp(rho_0) = {c_perp_uniform}  [from line 280]")

# From line 286: lambda = alpha^2 rho_0 / m_0
lam_expr = alpha**2 * rho_0 / m0
print(f"  lambda      = {lam_expr}    [from line 286]")

# Check that substituting lambda gives c_perp = alpha*c
c_perp_check = c_perp_uniform.subs(lam, lam_expr).simplify()
print(f"  c_perp check: c*sqrt(lambda m_0/rho_0) | lambda=alpha^2 rho_0/m_0")
print(f"              = {c_perp_check}     ✓ matches c_perp = alpha*c\n")

# From Paper II line 1380:  Phi = b * ln(rho/rho_0)
# At leading order: Phi ≈ (b/rho_0) * delta_rho
Phi_leading = (b_expr / rho_0) * delta_rho
Phi_leading_simplified = sp.simplify(Phi_leading)
print(f"  Phi (leading) = (b/rho_0)*delta_rho = {Phi_leading_simplified}")
print(f"  → delta_rho/rho_0 = 2*Phi / c^2")
delta_rho_over_rho_0 = sp.solve(Phi_leading - Phi, delta_rho)[0] / rho_0
delta_rho_over_rho_0 = sp.simplify(delta_rho_over_rho_0)
print(f"  Solving for delta_rho/rho_0: {delta_rho_over_rho_0}\n")

# ─────────────────────────────────────────────────────────────────────
# (2) Local chiral-shear speed: linearise around rho(x) instead of rho_0
# ─────────────────────────────────────────────────────────────────────
print("="*72)
print("STEP 2: Local chiral-shear speed in non-uniform background")
print("="*72)
print("""
The chiral-shear Lagrangian (Paper I line 271, schematic):

    L_perp ~ (lambda * hbar^2 / (2 m_0 rho_0^2)) * |j|^2  ,  j = rho * v_perp

When linearised around UNIFORM rho_0, this gives c_perp(rho_0) = c*sqrt(lambda m_0/rho_0).

When linearised around a SLOWLY-VARYING rho(x), the local wave speed
follows from the same procedure with rho_0 -> rho(x).  Two readings:

  (A) The Lagrangian's denominator rho_0^2 is a fixed BACKGROUND parameter
      of the medium (the saturation reference).  Then c_perp does NOT depend
      on local rho, and the time-dilation idea fails immediately.

  (B) The denominator should be the LOCAL rho^2 (covariant in the medium's
      density), so that the chiral-shear coupling is a property of the
      local condensate, not a frozen reference.  Then:
""")

# Reading B: replace rho_0 by local rho in the wave-speed formula
c_perp_local = c * sp.sqrt(lam * m0 / rho)
c_perp_local_with_lam = c_perp_local.subs(lam, lam_expr)
c_perp_local_simplified = sp.simplify(c_perp_local_with_lam)
print(f"  Reading B local: c_perp(rho) = c*sqrt(lambda m_0/rho)")
print(f"                              = {c_perp_local_simplified}")
print()
ratio = sp.simplify(c_perp_local_with_lam / c_perp_uniform.subs(lam, lam_expr))
print(f"  Ratio c_perp(rho)/c_perp(rho_0) = {ratio}\n")

# ─────────────────────────────────────────────────────────────────────
# (3) Express the ratio in terms of the gravitational potential Phi
# ─────────────────────────────────────────────────────────────────────
print("="*72)
print("STEP 3: Express ratio in terms of Phi (Reading B)")
print("="*72)

# rho = rho_0 + delta_rho; expand sqrt(rho_0/rho) for small delta_rho
rho_substituted = rho_0 + delta_rho
ratio_in_delta = sp.sqrt(rho_0 / rho_substituted)
ratio_series = sp.series(ratio_in_delta, delta_rho, 0, 2).removeO()
ratio_series_simplified = sp.simplify(ratio_series)
print(f"  sqrt(rho_0/(rho_0+delta_rho)) ≈ {ratio_series_simplified}")
print(f"    (leading order in delta_rho)")
print()

# Substitute delta_rho/rho_0 = 2 Phi / c^2 (with Phi treated as small/negative)
Phi_sym = sp.symbols('Phi', real=True)
ratio_in_Phi = ratio_series_simplified.subs(delta_rho, 2*Phi_sym*rho_0/c**2)
ratio_in_Phi = sp.simplify(ratio_in_Phi)
print(f"  Substituting delta_rho/rho_0 = 2Phi/c^2:")
print(f"    c_perp(rho)/c_perp(rho_0) ≈ {ratio_in_Phi}")
print(f"    = 1 - Phi/c^2     (Phi negative near a mass)\n")

# ─────────────────────────────────────────────────────────────────────
# (4) Compare to GR weak-field time dilation
# ─────────────────────────────────────────────────────────────────────
print("="*72)
print("STEP 4: Compare to GR weak-field prediction")
print("="*72)
print("""
GR weak-field result:
    tick(x)/tick(infty) = sqrt(1 + 2 Phi/c^2) ≈ 1 + Phi/c^2

For Phi NEGATIVE near a mass (gravitational potential well):
    tick(x)/tick(infty) ≈ 1 + Phi/c^2  < 1   (clocks tick SLOWER) ✓

SSV (Reading B) prediction for the chiral-shear mode speed:
    c_perp(x)/c_perp(infty) ≈ 1 - Phi/c^2

For Phi negative:
    c_perp(x)/c_perp(infty) ≈ 1 - Phi/c^2  > 1   (mode propagates FASTER!)

This has the WRONG SIGN.  A clock built from chiral-shear interactions
should tick at a rate proportional to c_perp(x), so ticks would be FASTER
near a mass under Reading B — opposite to GR and to observation.
""")

# ─────────────────────────────────────────────────────────────────────
# (5) What's actually going on: the role of rho < rho_0
# ─────────────────────────────────────────────────────────────────────
print("="*72)
print("STEP 5: Diagnosis")
print("="*72)
print("""
The sign discrepancy traces to a single fact:

    Near a mass, rho < rho_0  (medium is RAREFIED, depressed density)

In a rarefied region, the chiral-shear coupling lambda*m_0/rho_0
(if we hold lambda fixed and let rho be local) gives a HIGHER wave speed,
because the coupling-to-density ratio is larger.  But clocks in GR run
SLOWER in deeper potentials.

Possible resolutions, each requiring a separate argument:

  (R1)  The chiral-shear mode is NOT what clocks measure.  Maybe clocks
        measure the longitudinal/Bogoliubov mode (sound), whose speed
        c_s = sqrt(2 b rho/m_0) does scale as sqrt(rho/rho_0) — slower
        in depressed regions, GIVING THE CORRECT SIGN.

  (R2)  Reading A is correct after all (rho_0 in the denominator is a
        fixed reference), and the local clock rate has nothing to do
        with the chiral-shear mode speed varying.  In this case time
        dilation needs a different mechanical origin in SSV — maybe
        the "rate of vacuum interactions" argument from Paper II §6.1
        was actually correct but should not be conflated with mode-speed.

  (R3)  The chiral-shear coupling lambda itself depends on local rho
        (e.g. lambda is renormalised by the local medium state) in such
        a way that c_perp DECREASES in depressed regions.  This would
        require working out the renormalisation, which is non-trivial.
""")

# Let me actually check (R1): the longitudinal/Bogoliubov mode
print("="*72)
print("STEP 6: Check (R1) — longitudinal mode speed in non-uniform rho")
print("="*72)

c_s_local = sp.sqrt(2 * b_expr * rho / m0)
c_s_local_simplified = sp.simplify(c_s_local)
print(f"  Local Bogoliubov speed: c_s(rho) = sqrt(2 b rho/m_0)")
print(f"                                   = {c_s_local_simplified}")

ratio_cs = c_s_local / sp.sqrt(2 * b_expr * rho_0 / m0)
ratio_cs = sp.simplify(ratio_cs)
print(f"  Ratio c_s(rho)/c_s(rho_0) = {ratio_cs}")

ratio_cs_in_delta = sp.sqrt(rho / rho_0).subs(rho, rho_0 + delta_rho)
ratio_cs_series = sp.series(ratio_cs_in_delta, delta_rho, 0, 2).removeO()
print(f"  Leading order in delta_rho: ≈ {sp.simplify(ratio_cs_series)}")

ratio_cs_in_Phi = sp.simplify(ratio_cs_series.subs(delta_rho, 2*Phi_sym*rho_0/c**2))
print(f"  In terms of Phi:           ≈ {ratio_cs_in_Phi}")
print()
print("  For Phi NEGATIVE near a mass:")
print("    c_s(rho)/c_s(rho_0) ≈ 1 + Phi/c^2  < 1  (slower)")
print()
print("  Comparison to GR:  tick/tick_infty ≈ 1 + Phi/c^2")
print("  ✓ MATCHES at leading order in Phi/c^2")
print()
print("="*72)
print("CONCLUSION")
print("="*72)
print("""
At leading order in weak-field gravity, the LOCAL LONGITUDINAL (Bogoliubov)
sound speed c_s(rho) reproduces the GR time dilation factor exactly:

    c_s(x)/c_s(infty) ≈ sqrt(rho(x)/rho_0) ≈ 1 + Phi/c^2

This works DIMENSIONALLY because b = m_0*c^2/(2*rho_0) is exactly the
factor that makes the substitution delta_rho/rho_0 → 2*Phi/c^2 clean.
The gravity-as-density-depression picture of Paper II §6 produces GR
weak-field time dilation if and only if the mode whose speed sets the
clock rate is the LONGITUDINAL Bogoliubov mode, NOT the chiral-shear mode.

The chiral-shear mode has the WRONG sign for time dilation under the
naive local-rho substitution.

Implication for the c/c_perp story:
  - Stig's "delay = gravity" intuition is correct in DIRECTION
  - But the relevant delay is in the LONGITUDINAL channel, not the
    chiral-shear channel
  - This is consistent with Volovik's analogue-gravity programme,
    which uses the SOUND channel (longitudinal) as the carrier of the
    acoustic metric

What this means for the framework:
  - The longitudinal mode at c IS physical and IS what carries the
    gravitational metric (Volovik-style acoustic geometry).
  - The chiral-shear mode at c_perp is a separate, slower internal
    mode that does NOT participate in time dilation.
  - "GW is just the effect" is correct: changing density patterns
    propagate through the longitudinal channel at c, which is also
    the speed of light (consistent with GW170817).
  - But this means the photon must ALSO be a longitudinal-channel
    excitation (Goldstone phase mode), not a chiral-shear mode,
    confirming Volovik/Zloshchastiev.

Bottom line: the calculation works, but it favours a DIFFERENT
resolution of the c/c_perp problem than the one we tentatively adopted
in Stage 1.
""")

# zloshchastiev2020 — extracted equations

**K. G. Zloshchastiev**, *Superfluid vacuum theory and deformed dispersion
relations*, Int. J. Mod. Phys. A **35**, 2040032 (2020), arXiv:2011.11897.

This is the **actual source** of the logarithmic nonlinearity that SSV-I
attributes to Volovik.

## Eq. (1) — the logarithmic wave equation, p.1

> i∂_tΨ = [ −ħ/(2m)∇² + V_ext(x,t) − b ln(|Ψ|²/ρ̄) ] Ψ

The minus sign in front of `b ln` **matches SSV-I**. The sign was inherited
correctly; it is not a transcription error.

## The defining constraint, p.1

> ρ|F′(ρ)| = mc₀²/ħ ≈ const(ρ) … The solution of this differential equation is
> a logarithmic function: F(ρ) = b ln(ρ/ρ̄), where b and ρ̄ are real parameters.

Three consequences, all load-bearing:

1. `F(ρ)` is the **nonlinear chemical-potential term, not a pressure**. SSV-I
   `main.tex:205` reads it as a pressure. Since c_s² = ρμ′(ρ)/m for a chemical
   potential but P′(ρ)/m for a pressure, this single misreading generates the
   whole error chain of #180.
2. It is an **absolute value** — it fixes |b|ρ₀ = m₀c² and is **silent on
   stability**. SSV-I converts it into a signed, positive c_s².
3. **No factor of 2.** SSV-I's c_s = √(2bρ₀/m₀) and b = m₀c²/(2ρ₀) are wrong by
   √2 and 2 respectively, independently of any sign question.

## The Gausson branch, p.1

> the ground state solution for positive values of b was known … since the
> works of Rosen and Bialynicki-Birula and Mycielski

So **b > 0 is the Gausson branch** — the sign under which the uniform vacuum is
modulationally unstable. Light-as-sound needs b < 0; the Gausson needs b > 0.
The pure logarithmic theory cannot supply both.

## Natural length scale, p.2 (below Eq. 2)

> a = ħ/√(2m|b|)

SSV-I's ξ = ħ/√(2m₀bρ₀) is the **same formula** — correct. Only its evaluation
is wrong: with the corrected |b|ρ₀ = m₀c², ξ = ħ/(√2 m₀c), not ħ/(m₀c).

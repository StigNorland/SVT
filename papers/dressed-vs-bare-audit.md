# Dressed-vs-bare category-error audit (corpus-wide)

Date: 2026-05-28
Triggered by: issue #33 (Paper II §3 form-factor loop integral).
Companion: `papers/SSV-II/topological-vertex-exploration.md`,
`papers/SSV-II/g2-form-factor-results.md`.

## The pattern to detect

> Taking an *emergent* classical extent of a configuration (e.g. the
> equilibrium ring radius $R^\* = \xi/\alpha$, the proton 3D-breather radius,
> the W cap radius $R_{\rm cap,W} = \varphi/\alpha$) and inserting it as a
> **momentum-space form factor at a vertex of the underlying Lagrangian** —
> i.e. on top of the bare $\psi$-phonon contact coupling — under the
> classical-electromagnetism analogy "extended object ⇒ Fourier transform of
> its current distribution at the vertex."

This conflates two different objects:

| Bare object | Emergent object |
|---|---|
| Field at a point in LogSE + $\mathcal{L}_\perp$ | Assembled vortex / breather configuration |
| Contact coupling ($F\equiv 1$, no length scale) | Classical current/charge distribution at scale $R^\*, R_{\rm cap}, \dots$ |
| Probed by loop momenta inside Feynman diagrams | Probed by external static/classical fields, geometry, mass ratios |
| The "1" of the Lagrangian's natural units | A derived configuration scale |

The numerical falsifier developed for #33 (suppression of Schwinger by 99.5%
when $J_0(kR^\*)$ is plugged into the QED-loop vertex) is what made the
distinction visible.  Anywhere else in the corpus the same pattern appears, it
will produce the same kind of catastrophic suppression of an otherwise-clean
QED-equivalent calculation.

## What was wrong (now fixed)

- **Paper II §3, eqs. (593)–(612), gapbox at line 620.**  Inserted
  $F(kR^\*) = J_0(kR^\*)$ into the Schwinger 1-loop vertex correction, with
  $R^\* = \xi/\alpha$ from Paper I, and quoted a parametric "ring-size
  correction" $\sim -\alpha^3/(4\pi)$.  Numerical evaluation showed this would
  remove 99.5% of $a_e^{\rm Schwinger}$, $\sim 10^9\sigma$ vs CODATA.  Rewritten
  in commit on this branch with the dressed-vs-bare distinction made explicit
  and Schwinger's $\alpha/(2\pi)$ restored exactly.

## Corpus sweep results — no further occurrences found

Every other appearance of "form factor," "Fourier transform of," $J_0$, or
$R^\*$-scale insertions in a loop/vertex context, surveyed by grep across
`papers/**/*.tex`, was checked and falls into one of three categories that
are *not* the category error:

### (A) Classical energy ratios labelled "form factor" (FINE)

- **Paper I — proton mass:** $m_p c^2 = N_Y \cdot F \cdot \mu_0$ with
  $F \approx 4.47$ (Paper I §proton, gapbox at line 1053).  Here $F$ is the
  ratio of the assembled 3D breather energy to the Y-junction line energy
  $N_Y\mu_0$ — a static configuration energy denominator extracted by
  topology-preserving relaxation.  Not a momentum-space form factor; lives
  in the dressed-object column where Paper I uses $R^\*$-class scales
  legitimately.

- **Paper II §reconnection (line 1033):** "geometric form factor of the full
  3D barrier" for the $W$-mass estimate.  This is the geometry of the
  *static reconnection path* in the $\mathcal{L}+\mathcal{L}_\perp$
  functional, not a vertex inserted in a Feynman diagram.  Fine.

- **Paper II §CP-sector (line 2228):** $|d_n|/|d_n^{\rm naive}| \sim 10^{-3}$
  "suppressed by the geometric form factor of the Y-junction reconnection."
  Same flavour as above — a *classical configuration overlap*, not a
  bare-vertex form factor.  Fine.

### (B) Bessel functions as actual classical field profiles (FINE)

- **Paper VI-a eqs. (145), (225), §satellites:** $J_0(kr)$ appears as the
  *standing-wave solution* for galactic breather density and rotation curves.
  This is the dressed configuration's actual radial profile — not a vertex
  form factor on a loop diagram.  Fine.

### (C) Bare-vs-emergent distinction already made correctly (FINE — and useful precedent)

- **Paper SSV-Goldstone §anomalous magnetic moment (lines 275–286):**
  "The one-loop self-energy picture must be reinterpreted carefully. The
  virtual exchange responsible for $g-2$ may continue to involve the
  chiral-shear near field, but the on-shell photon propagator must belong to
  the Goldstone channel.  The calculation therefore has to distinguish
  virtual constrained exchange from physical radiative quanta."  This is
  conceptually the right distinction (different object inside the loop than
  outside).  The Paper II §3 rewrite is the natural place for this idea to
  also live for the *vertex* (not just the propagator).

- **Paper II §3.0 (line 322):** $\xi$ "is *not* the medium's UV cutoff in the
  deep sense" — that role is reserved for $\ell_{\rm grain}$.  Correctly
  distinguishes the emergent scale that sets the electron from the
  fundamental UV scale of the Lagrangian.

- **Paper VII-b (lines 357–359, 500–502):** $\xi$ as UV cutoff "supplied by
  the particle sector," not postulated.  Same distinction in the gravity
  sector.

- **Paper II §2415–2417:** the Standard Model fine-tuning instability
  *doesn't* transfer to SSV because $\xi$ is itself a property of the
  medium — again the dressed/bare distinction held correctly.

## Audit conclusion

The category error existed in exactly one place — Paper II §3 — and has
been fixed.  Other uses of "form factor" / $R^\*$ / Bessel-shaped profiles
across the corpus refer to *legitimate* dressed-object quantities and do
not produce a loop-vertex suppression problem.

## Forward-looking rule (for future SSV calculations)

When in doubt about whether a scale is allowed to enter a calculation:

1. **Is the calculation a loop integral, vertex correction, propagator, or
   self-energy built from the LogSE + $\mathcal{L}_\perp$ Lagrangian?**  If
   yes, the only scales allowed in the vertex are those *present in the
   bare Lagrangian* — typically $\xi$ as the LogSE coherence/UV scale, $m_0$
   if any, and the chiral-shear coupling.  Emergent ring-radius / cap-radius
   / Y-junction scales **must not** appear there.  Bare couplings are
   contact terms ($F\equiv 1$) unless the Lagrangian gives them an explicit
   derivative or non-local structure.

2. **Is the calculation a classical-configuration energy, geometric overlap,
   static field profile, or mass-ratio of an assembled object?**  Then
   $R^\*, R_{\rm cap}, R_{\rm Y\text{-}junction}, \dots$ are exactly the
   right scales, and Paper I's identifications continue to apply.

3. **When the same physical observable can be computed both ways (e.g.
   a magnetic moment via loop integral *and* via classical current
   distribution), Paper II §3 shows they need not agree at sub-leading
   order — they answer different questions.**  The classical-current
   calculation captures the dressed-electron's static response (Bohr
   magneton, $\mu_e = e R^\*/2 \times v_\perp$); the loop calculation
   captures bare-vertex radiative corrections (Schwinger's
   $\alpha/(2\pi)$).  The first sets $g \approx 2$ as a dressed-object
   property; the second supplies the $\alpha/(2\pi)$ deviation as a
   bare-coupling radiative correction; they add, not multiply.

A one-line check before any new SSV calculation involving a length-scale
insertion:

> *Am I describing the assembled object as seen from outside (use
> $R^\*, R_{\rm cap}, \dots$), or am I describing the bare Lagrangian
> coupling at a vertex (use $\xi$ or no scale at all)?*

If the calculation can't answer that question unambiguously, that's the
signal that one of the two objects has been substituted for the other.

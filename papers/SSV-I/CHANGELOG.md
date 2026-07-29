# SSV-I — change record

The paper states **current status only**. Its history lives here.

Each entry gives the issue, what changed in the physics, and — where prose was
removed rather than rewritten — the removed text verbatim, so nothing is lost
by the move. Git history and the linked issues carry the rest.

---

## 2026-07-29 — [#210](https://github.com/StigNorland/SVT/issues/210) · SSV verification repair

The read-only series audit found that the paper still mixed derived factors,
candidate masses and historical source attributions.  The abstract, overview,
proton section and claim-status table now distinguish the derived pion mass,
the derived trefoil crossing number, the cutoff-dependent candidate proton
mass and the coincidental higher-mass alignments.  Rosen's 1968 article is
retained only as a negative attribution result; BBM 1976 is the source used for
the nonrelativistic LogSE.

Load-bearing wording removed or replaced (verbatim):

> “Two masses are genuine topological derivations: the charged pion at
> \(2\mu_0\) (the two-winding number) and the proton, whose node factor
> \(N_Y=3\) is the trefoil crossing number.”

> “This is not the classical electron radius
> \(r_e=\alpha\hbar/(m_ec)\), which is smaller by a factor \(\alpha^2\).”

The corrected radius ratio includes the inherited healing-length factor:
\(r_e/R_e^*=\sqrt{2}\alpha^2\).  The proton's full mass is candidate-grade
because \(F\) remains cutoff-dependent; only \(N_Y=3\) is topological.

## 2026-07-29 — [#207](https://github.com/StigNorland/SVT/issues/207) · change records moved out of the paper

Eight passages of edit history removed from `main.tex` and recorded below. No
physics changed; every negative result they carried is retained in the paper in
the present tense.

## 2026-07 — [#183](https://github.com/StigNorland/SVT/issues/183) · citation audit

Full analysis in [`results/audit-2026/`](results/audit-2026/).

**The sign of the logarithmic potential was reversed.** Earlier versions printed
the opposite sign, `b rho_0 = m_0 c^2/2` (a spurious factor 2),
`xi = hbar/(m_0 c)`, and a "thermodynamic vs. Bogoliubov" discrepancy together
with its resolution. Because `rho mu'(rho)` is constant for a logarithmic
chemical potential, the two routes are the same quantity, so **both the
discrepancy and its resolution were artifacts** and were removed. The rejected
sign made the uniform vacuum modulationally unstable.

*Cost, still stated in the paper:* the Gausson does not exist on the adopted
branch, so particles must be topological rather than bright solitons
([#189](https://github.com/StigNorland/SVT/issues/189)).

**Attribution of the logarithmic potential and the LogSE.** Previously credited
to Volovik, whose Phys. Rept. **351**, 195 contains no logarithmic equation of
state — *"equation of state" occurs 0 times in 71,425 words*. The
misattribution is why the error survived review: the real source's constraint
`rho|F'(rho)| = m_0 c^2/hbar` was never applied, and its `F(rho)` — a
*chemical-potential* term — was read as a *pressure*.

**Vacuum saturation density `rho_0`.** Previously printed as
`2 alpha Lambda m_e^4 c^3 / pi^2 hbar^3 ≈ 1.9 m_e^4 c^3 / hbar^3`, with
`Lambda` in the **numerator** and a value inconsistent with its own formula.
Inverting the electron-mass relation correctly gives
`≈ 9.96e-5 m_e^4 c^3 / hbar^3` — **smaller by ~2×10⁴**. The corrected value
carries a `sqrt2` inherited from the corrected healing length.

*(This comparison is guarded by `claims.py::rho0-smaller-by-2e4`, which is
anchored to this entry: the guarantee follows the statement rather than being
dropped when the statement leaves the paper.)*

**`R_e^*` was misidentified as the classical electron radius.** It is not:
`hbar/(alpha m_e c)` is the **Bohr radius** `a_0`, and `r_e = alpha hbar/(m_e c)`
is smaller by `alpha^2`. The *relation* `R^* = xi/alpha` survives; its
identification with a particular measured length was a separate claim, and the
one made was wrong. With the corrected `xi`, `R_e^* = a_0/sqrt2`.

**The equilibrium-radius energy applied `alpha^2` twice**, once in the
chiral-shear coefficient and again in the stationarity condition, so as printed
`E(r)` stationarised at `r* ≈ 0.57` rather than `1/alpha`. The physics was
intact; the presentation was not.

**The proton's symmetric Y-junction is withdrawn.** Earlier versions described
the proton as "a Y-junction of three quantized vortex filaments meeting at a
central node". Absent from the cited sources — Faddeev–Niemi contains no
discussion of vortex junctions, and Proment *et al.* construct `T_{2,3}` as a
*single closed curve* — and forbidden in a one-component `U(1)` condensate,
where quantized circulation forces `sum_i n_i = 0` at any node. **No number
changed:** the computations always used the knot.

**Appendix expansion.** Earlier versions gave `C = 1/8` and called it "a pure
geometric constant from the elliptic expansion". It is neither: the coefficient
is `3/16`, and the term carries a logarithm. The claim that the appendix
"recovers eq:Ekin at leading order" was false — the two use different core
models (`-2` filament/hollow-core against Lamb's `-7/4` for uniform vorticity).
`eq:Ekin` and its `-7/4` were correct and unchanged.

## 2026-07 — [#119](https://github.com/StigNorland/SVT/issues/119) · gravity as the acoustic Bjerknes force

**Falsified as written.** Earlier versions of this paper stated it as an
established result. The radiation-zone cross-term oscillates in sign with
separation and vanishes between breathers of unequal frequency; a bath-driven
repair is sign-definite but fails on range. Retained in Paper IV as record.

## 2026-06 — [#138](https://github.com/StigNorland/SVT/issues/138) · `alpha = c_perp/c` reinterpreted

Reinterpreted as a core-scale **stiffness ratio** of the defect sector. The
chiral term is silent in the linear spectrum of the uniform vacuum, so no mode
propagates at `alpha c`. One signal speed, `c`.

## 2026-06 — statements re-framed (removed "What changed in this paper" section)

Until [#207](https://github.com/StigNorland/SVT/issues/207) the paper carried a
`What changed in this paper` section — a changelog inside the argument. Its
content, verbatim:

- **the proton-mass agreement was previously headlined as 0.3% from CODATA;**
  the corrected framing is ~1.5% with a cutoff-dependent range
  930–954 MeV, where 0.3% is the precision at the specific cutoff
  `R = 1.18 xi` rather than a cutoff-independent prediction;
- **the `N_Y` convergence statement** "independent of grid resolution above
  `128^3`" was corrected to reflect the actual computed grids (`24^3`, `48^3`,
  `72^3`);
- **three cutoff routes for `N_Y·F` were tested and all fail**: cutoff
  invariance is falsified (31.5× spread over `R = 0.5–3 xi`); geometric-`R`
  extraction fails; and the first-principles half-density cutoff
  `R_sc = 0.923 xi` gives 60% cross-state spread at fixed `R_sc`. The dominant
  cause is the penalty parameters influencing the converged state geometry
  ([#30](https://github.com/StigNorland/SVT/issues/30));
- **the muon identification** was tested by three independent null results
  (Path B, [#73](https://github.com/StigNorland/SVT/issues/73),
  [#76](https://github.com/StigNorland/SVT/issues/76) Berry-phase audit), and
  the CP¹/spinor ([#91](https://github.com/StigNorland/SVT/issues/91)) and
  half-quantum-vortex ([#94](https://github.com/StigNorland/SVT/issues/94))
  routes are likewise closed. No half-integer Berry holonomy is available, so
  the muon and the higher masses are numerical coincidences, not candidate
  rungs.

Also removed: a `±0.002` uncertainty band on `N_Y` quoted in earlier drafts,
which referred to fit reproducibility within a single grid family and was not a
measured cross-resolution spread.

Every one of these negative results remains stated in the paper — in the
claim-status table and in the relevant sections — in the present tense. What
was removed is the narration of when they changed.

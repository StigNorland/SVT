# SSV-I — change record

The paper states **current status only**. Its history lives here.

Each entry gives the issue, what changed in the physics, and — where prose was
removed rather than rewritten — the removed text verbatim, so nothing is lost
by the move. Git history and the linked issues carry the rest.

---

## 2026-07-30 — [#218](https://github.com/StigNorland/SVT/issues/218) · coefficient-one vortex and BdG recalculation

The conventional-healing-length vortex equation now carries coefficient one:
\(f''+f'/x-f/x^2-f\ln f^2=0\). The historical coefficient-two solver remains
available as a reproducibility control. The corrected profile has
\(R_{\rm sc}=1.305516\,\xi\) and \(C_{\rm LogSE}=2.226289\).

Saved-state recalibration changes the fine-grid form factors at
\(R=1.18\,\xi\) to \(F=5.168\)--\(5.298\). With \(N_Y=3.007\) this gives
\(1088\)--\(1116\) MeV, \(16.0\%\)--\(18.9\%\) above the observed proton mass;
the old near-CODATA band does not survive. The grid-converged issue-77 combined
observable correspondingly moves from approximately \(54\) to approximately
\(74\). The self-consistent-cutoff closure gate remains negative, with the
\(n\ge48\) spread increasing to \(158.1\%\).

The corrected profile-matched BdG blocks are
\(L=-\nabla^2+\ln(f^2)+1\) and \(M=e^{2i\theta}\). The straight-core
translation mode approaches zero with box size. The old assertion that axial
\(U(1)\) guarantees a \(+m/-m\) doublet on a chiral vortex is removed;
\(U(1)\) supplies one-dimensional complex \(m\) sectors and no SO(3)-like
threefold shell. The no-magic-8 conclusion therefore remains negative for a
stronger reason.

## 2026-07-30 — [#216](https://github.com/StigNorland/SVT/issues/216) · E6 dimensional normalization propagated

The logarithmic sector now uses one mass-specific stiffness throughout:
\([b]=\mathrm{J\,kg^{-1}}\), \(c_s^2=b\), and \(b=c^2\). Restoring the
background number density \(n_0=\rho_0/m_0\) in the action gives the LogSE
energy coefficient \(m_0b\) without inserting \(\rho_0\) into either the
sound speed or healing length. The conventional healing length remains
\(\xi=\hbar/(\sqrt2\,m_0c)\), so no registered numerical value changes.

Propagating that convention exposed two independent analytic errors. The
exact Bogoliubov relation is
\(\omega^2=c_s^2k^2(1+k^2\xi^2/2)\); the unit-coefficient form uses the shorter
dispersive crossover length \(\ell_{\rm disp}=\xi/\sqrt2\), not the
conventional healing length. The same normalization changes the ring estimate
to \(\omega_{\rm ring}/\omega_c=2\alpha\sqrt{\ln(1/\alpha)}\). Both conclusions
remain negative for the proposed muon mode.

The old scalar operator \(-\nabla^2+4(1-f_0^2)\) is not the Hessian of the
corrected LogSE because the physical BdG problem has a nonzero particle-hole
block. Its no-bound-state argument is therefore withdrawn; the corrected
coupled-BdG amplitude question is open, while the independent basis-convergence
and Berry-phase null results remain in force.

The primary-source evidence record for Zloshchastiev 2020 now separates the
source frequency coefficient \(b_{\rm src}\) from Paper I's mass-specific
\(b\). Its constraint gives
\(|b_{\rm src}|=m c_s^2/\hbar\), with no \(\rho_0\) and no factor two. The
source's printed natural-length formula is dimensionally inconsistent with its
own Eq. (1), so Paper I derives \(\xi\) from its action instead.

## 2026-07-29 — [#213](https://github.com/StigNorland/SVT/issues/213) · standard symbol meanings

The overloaded \(\mu_0\) is split by dimension: \(m_\star=m_e/\alpha\) is
the mass scale, \(E_\star=m_\star c^2\) its rest-energy scale, and
\(\varepsilon_{\rm line}\) the cutoff-dependent line tension.  The proton
scale \(a_p\) is renamed to its standard meaning,
\(\bar\lambda_p=\hbar/(m_pc)\), the reduced proton Compton wavelength.
The first #213 guard only recorded the \(\mu_0\) collision; the revised build
gate forbids its non-permeability use.

## 2026-07-29 — [#213](https://github.com/StigNorland/SVT/issues/213) · shared observed constants

Observed particle masses, \(\alpha^{-1}\), and \(m_p/m_e\) now come from the
series-level shared-value receipt wherever the same quantity is printed in
another SSV paper.  The candidate \(N_YF\) values remain literals and are
reported as unregistered: their cutoff-dependent source is not yet a stable
instrument output.  The programme-wide D1/D2/D3 result and the retained
negative limit are recorded in
[`results/issue-213-shared-value-registry.md`](results/issue-213-shared-value-registry.md).
The charged-pion input is also updated from the older
\(139.57018\pm0.00035\) MeV pair to the PDG-2024
\(139.57039\pm0.00018\) MeV value carried by the shared source.

## 2026-07-29 — [#207](https://github.com/StigNorland/SVT/issues/207) · the proton band reconciled with its own table

Two different proton masses were in print at once. Owner's observation: the
paper carries both `930–954 MeV` and `927 MeV`, and `927` lies *outside* the
band it appears beside.

**Cause: `Table tab:Fstraight` mixed two n=48 relaxation states.** Its `n=24`
and `n=72` rows come from the current states; the `n=48` row was still the
superseded one (`F(1.18) = 4.15`, `F(1.0) = 4.90`, …). The band in the prose
was computed from the *current* n=48 state (`F = 4.528`), so the table
silently contradicted the number it was supporting. Re-running
`instruments/paper_i/proton_geometric_r_probe.py` on the three named states
(2026-07-29) reproduces the current values directly:

| state | n | F(R = 1.18 ξ) |
| --- | --- | --- |
| `penalty-mu400-rho0p01-n24-hw6-1600steps` | 24 | 5.606 |
| `penalty-best-n48-hw6-800steps` | 48 | **4.528** |
| `penalty-n72-mu2000-rho0p05` | 72 | **4.417** |

**Corrections, all in the direction of the reproducible run:**

- The band is `930–953 MeV`, not `930–954`. With `N_Y = 3.007` and
  `μ₀ = m_e/α = 70.025 MeV`: `F = 4.417 → 930.1 MeV`, `F = 4.528 → 953.4 MeV`.
- The deviation is `−0.9%` to `+1.6%` of CODATA `938.272 MeV`, not `~1.5%`.
  The band is asymmetric and a single figure misstated the upper edge.
- The two fine grids agree to `2.5%`, not `~6%`. The `6%` came from the same
  superseded n=48 row. The spread is exactly R-independent, because only the
  denominator `μ₀_straight(R)` carries the cutoff.
- `927 MeV (1.2% below observed)` is **removed** (3 sites). It came from a
  rounded `F ≈ 4.4` obtained by averaging against the superseded n=48 value;
  the direct scan at `R = 1.18 ξ` gives `4.417` on that grid, not `4.4`.
- Paper II's `G` gapbox now quantifies what it already flagged: `N_p = 13.44`
  is the midpoint of `13.28–13.62`, so the inherited spread on `G_pred` is
  `−3.2%` to `+1.8%` — five times the quoted `0.6%` residual.

Removed as history rather than status (the §Proton gapbox), verbatim:

> The reduced-ansatz $Q_p$ family of scripts that attempted to calibrate this
> cutoff away (the \texttt{q\_p\_two\_factor\_*} probes and the \texttt{eta}
> calibration trio) is quarantined in
> \texttt{instruments/\_fitted\_quarantine/}, because calibrated inputs flatter
> derived results; their own docstrings already labelled them ``provisional
> consistency-based calibration rather than a derived physical constant.''

and, from the $F$-integral discussion and the extraction appendix:

> \emph{Numerical update (2026-05-19, see Appendix~\ref{app:minimisation}):}
> … The product $N_Y\cdot F$ then gives $m_p\approx 927\,\text{MeV}$
> ($1.2\%$ below the observed value), rather than the original $0.3\%$ figure;
> the $0.3\%$ match was tight to a coarse-grid evaluation of $F$ at a different
> cutoff.

and from the `Matching the analytic estimate` paragraph:

> The product $N_Y\cdot F=3.007\times4.4\approx 13.2$ gives
> $m_pc^2\approx 927\,\text{MeV}$, within $1.2\%$ of the observed proton mass.
> The original $0.3\%$ figure quoted in the main text required the analytic
> $F=4.47$ at the same cutoff exactly; the numerical $F$ at this cutoff sits
> $\sim 1.5\%$ below, hence the $\sim 1\%$ residual discrepancy.

The negative residue is kept in the paper in present tense: the quarantine
finding survives as *"$F$ … is not yet a derivation"* plus the measured
`dlnF/dlnR ≈ −0.94`, and the `0.3%` figure is stated as a property of the
bracket midpoint rather than a determination.

**The dates went too.** `\subsection*{… (2026-05-19)}` and
`estimated numerically (2026-05-19)` are the same shape as the
`Status (YYYY-MM)` headers removed under this issue: a dated assertion goes
stale silently, because it still reads as a plausible log entry after it stops
being true.

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

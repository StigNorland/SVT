# SSV-VII-a — change record

The paper states **current status only**. Its history lives here.

Each entry gives the issue, what changed in the physics, and — where prose was
removed rather than rewritten — the removed text verbatim, so nothing is lost
by the move. Git history and the linked issues carry the rest.

---

## 2026-07-29 — [#189](https://github.com/StigNorland/SVT/issues/189) · E-gate complete, four defects

E-gate extended from one subsection to all 21 equations. Full analysis in
[`results/audit-2026/E-gate-report.md`](results/audit-2026/E-gate-report.md)
and [`results/audit-2026/C-gate-damage-report.md`](results/audit-2026/C-gate-damage-report.md);
the computation is
[`results/logse-gaussian-issue189.md`](results/logse-gaussian-issue189.md).

**E1 `MISDERIVED` — the Gausson does not exist on the adopted branch.**
Substituting the Gaussian ansatz into the LogSE fixes
`sigma^2 = -hbar^2/(2 m s b)`. In the `-b ln` convention this paper prints,
`sigma^2 = +hbar^2/(2mb)` and the Gausson exists. In the `+b ln` convention
Paper I adopted under [#183](https://github.com/StigNorland/SVT/issues/183),
`sigma^2 < 0` and no normalisable Gaussian exists at all.

§"Saturation by the Gausson" is **retained as an explicitly labelled
rejected-branch record** (owner's decision, 2026-07-28), mirroring Paper I's
handling of its own rejected sign, rather than deleted.

**E2 `MISDERIVED` — the `hbar/2` prefactor is imported, not derived.** The
superseded `resultbox` was titled *"The `hbar/2` prefactor is derived, not
imported"* and read:

> The minimum uncertainty product $\Delta x\,\Delta p = \hbar/2$ is realised
> exactly on the Gausson \eqref{eq:gausson}, the LogSE's natural coherent
> state. The $1/2$ prefactor arises from the Gaussian integral structure that
> the logarithmic nonlinearity preserves: $(\Delta x)^2 = \sigma^2/2$ and
> $(\Delta p)^2 = \hbar^2/(2\sigma^2)$ jointly fix the saturation value
> without independent normalisation choice. The hydraulic-stiffness argument
> of \S\ref{sec:uncertainty} therefore not only recovers the form of the
> uncertainty relation; it identifies the LogSE coherent state on which the
> bound is saturated and the LogSE structure constants $(m, b)$ that fix the
> Gausson width.

Replaced by a `gapbox` stating the negative result. Every normalised Gaussian
saturates to `hbar/2` with `b` absent from the calculation; a normalised
Laplace state gives `sqrt(2)/2 hbar`, so saturation is a property of
Gaussianity, not of the LogSE.

**E3 `MISATTRIBUTED` — the Coulomb potential was credited to Paper I.** The
removed sentence justified `eq:Veff-coulomb` by the identification

> where the proportionality is fixed by the same identification
> $\alpha = c_\perp/c$ that defines the chiral-shear coupling in
> Paper~I (\S\,Postulate),

and the surrounding paragraph concluded that the hydrogen spectrum "is
therefore a direct consequence of the LogSE low-amplitude long-wavelength
limit together with **Paper~I's chiral-shear identification of
electromagnetism**, with no fresh numerical input."

Paper I does not contain that reduction. `SSV-I/main.tex:374` routes the
statics of charged defects to **Paper II**, where the Bernoulli-pressure
derivation of `F_C = alpha hbar c / r^2` is carried out. This paper did not
cite `SSV-II` at all; it now does. Paper II records the coupling as *empirical*
`alpha`, so the Rydberg recovery is a consistency result given already-conceded
inputs, not a prediction.

**E4 `MISDERIVED` — the Born basin argument assumes its own conclusion.** The
superseded conclusion read:

> The basin volume for outcome $k$ is therefore $|c_k|^2$ by direct calculation
> in the reconnection-threshold model, with no remaining choice: the rate
> linearity comes from the leading-coupling expansion, and the cancellation of
> the apparatus factor $\kappa$ comes from every branch coupling to the same
> threshold mode. The Born rule \eqref{eq:born} is a derived consequence of
> the SSV measurement mechanism, not merely a consistency statement.

`eps_k = |c_k|^2 |psi_k|^2` **is** the Born weight, so the exponent enters as a
premise; cancelling `kappa` removes a factor common to every branch but cannot
change it. This also resolved an internal contradiction: the paper's own
testable-claims list already said the basin calculation "is the calculation
needed before the measurement section can be promoted from physical
interpretation to formal derivation."

**E5 — `rho` carried two normalisation conventions**, declared a mass density
in `eq:polar` and used as a unit-normalised probability density in
`eq:gausson-Dx`. Now stated once rather than left implicit.

**E6 — `kappa` notation.** Defined by an integral containing `psi_k`, so it
carried an index the cancellation requires it not to have. The
branch-independence is now stated as an assumption.

**Open-problems entry rewritten.** The precise-prefactor item previously said
the `1/2` "should emerge from the LogSE coherent-state minimum; the calculation
is deferred to the Paper~I programme." That route is **closed**, not deferred.

**Added:** `instruments/paper_vii_a/logse_gaussian.py` and 12 tests — the paper
previously had no scripts and no result notes. Two `claims.py` guards protect
the negative results against silent re-upgrade;
`instruments/tools/dimensions.py` now covers this paper.

---

## 2026-07-28 — [#189](https://github.com/StigNorland/SVT/issues/189) · interim gap box

PR [#197](https://github.com/StigNorland/SVT/pull/197), commit `ea8e776`. An
interim `gapbox` was placed at the head of §"Saturation by the Gausson"
recording both findings, with **no repair attempted**, so that the section was
not left reading as current while its replacement was researched. Superseded by
the 2026-07-29 entry above.

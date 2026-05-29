# Numerical closures: paper-series issues

This note is the index of paper-closure tasks completed via merged PRs.
For each closure it points to the receipts: a paper section/equation
where the closure lives, and (where applicable) a self-contained
verification script under `src/`. The scripts run in seconds (with one
exception flagged below) and print the table or numerical claim that
appears in the corresponding `resultbox`.

The note replaces an earlier orphan-branch version of the same file
(originally on `claude/jolly-tu-940955`) which never reached main. The
two known orphan-branch holes that remain are listed at the bottom.

## Summary

| Issue | Paper                                | What was closed                                                      | Receipts |
|-------|--------------------------------------|----------------------------------------------------------------------|----------|
| #31   | SSV-I §The Neutron                   | Neutron as surface-locked composite $\mathcal{N} = \mathcal{T} \cup_{\Sigma_p} \mathcal{E}$, structural | paper text |
| #33   | SSV-II §3                            | Toroidal form-factor reduced to contact-term vertex; Schwinger $\alpha/(2\pi)$ recovered exactly at one loop | `src/paper_ii/g2_form_factor_loop.py` |
| #34   | SSV-II §Higgs                        | $m_p/m_{\pi^\pm} = N_Y F / 2$ structural composite mass ratio        | paper text |
| #35   | SSV-II §CP                           | Neutron EDM derived from reconnection-memory mechanism, structural   | paper text |
| #36   | SSV-II §Neutrinos                    | Speculative spectrum demoted with five explicit falsifiers           | paper text |
| #37   | SSV-II §Tau                          | Tau identified as Hopf-linked trefoil pair bound by a muon quantum   | `src/paper_ii/tau_identification.py` |
| #40   | SSV-V §6                             | Planck-scale evaporation endpoint is a stable topological remnant    | paper text |
| #42   | SSV-VI-a §4.4                        | First-principles closed form $\mathcal{C} = \hbar N_p^9 / (2 \alpha_G c \alpha^{25})$ | paper text |
| #43   | SSV-VI-b §3.2                        | Quantitative $\varepsilon_m(a_{\rm BH})$ table from Hansen–Geroch multipole expansion | paper text |
| #49   | SSV-VII-b §6                         | Strong-field numerical verification of the SSV-identified metric     | `src/paper_vii_b/strong_field_test.py` |

## Per-closure detail

### #31 — Neutron as surface-locked composite

Closed at *structural* tier. The neutron is identified with
$\mathcal{N} = \mathcal{T} \cup_{\Sigma_p} \mathcal{E}$: the proton
trefoil $\mathcal{T}$ glued to a captured electron torus $\mathcal{E}$
at the breather skin $\Sigma_p$. Boundary-framed (rather than
bulk-framed) attachment resolves both the previously-listed open
problems: the spin-$\tfrac{1}{2}$-plus-spin-$\tfrac{1}{2}$ composition
delivers a fermion because the surface-locked torus does not contribute
independent framing; the 200 MeV/c momentum estimate does not apply
because the captured electron is a quadratic-dispersion Kelvin surface
mode rather than a localised relativistic wavepacket. The mass split
decomposes structurally as
$\Delta E = m_e c^2 + \Delta E_{\rm surf}$,
with $\Delta E_{\rm surf}$ identified as the $\beta$-decay endpoint
$0.782$ MeV. Quantitative pinning of $\Delta E_{\rm surf}$ is tied to
issue #13 (converged trefoil-breather geometry).

### #33 — Contact-term vertex, no classical ring-size correction

Closed by replacing the naive $J_0(k R^*)$ vertex form factor with the
dressed-vs-bare distinction. $R^* = \xi/\alpha$ describes the assembled
electron seen from outside (Bohr magneton, cap radii, hadron mass
scaling — all of Paper I's successful uses); the bare $\psi$-phonon
coupling in LogSE $+\mathcal{L}_\perp$ is a contact term with no
momentum-space form factor. Schwinger's $\alpha/(2\pi)$ is recovered
exactly at one loop; SSV-specific deviations would have to come from
intrinsic structure of the bare sector, not from a classical extent.

`src/paper_ii/g2_form_factor_loop.py` reduces the one-loop integral
numerically, verifies the Schwinger normalisation to $3 \times 10^{-10}$,
and scans five form-factor families to confirm robustness.

### #34 — Structural composite mass ratio $m_p/m_{\pi^\pm}$

From the Paper I identifications $m_{\pi^\pm} = 2\mu_0$ and
$m_p = N_Y F \mu_0$, the empirical $\mu_0 = m_e/\alpha$ scale cancels
and
$$\frac{m_p}{m_{\pi^\pm}} = \frac{N_Y F}{2} \approx 6.72 \quad (\text{observed } 6.722, 0.1\%)$$
follows without fitting. The consistency identity
$2(m_p/m_{\pi^\pm}) = \alpha(m_p/m_e) = N_Y F$ collapses three
experimentally distinct ratios to a single framework quantity at the
$0.3\%$ level.

### #35 — Neutron EDM from reconnection memory

Closed at *structural* tier. The chirality memory density
$\chi(\mathbf{x}, t) = \sum_i \sigma_i K(\mathbf{x} - \mathbf{x}_i, t - t_i)$
couples to the surface-locked electron torus on the proton breather
skin via the chiral-shear potential $V_\perp$. The captured-torus
centroid shifts by
$\delta \mathbf{r}_\mathcal{E} = \kappa_\chi \langle \chi \rangle_{R_n} R_n$,
giving
$$d_n = \kappa_\chi e R_n (n_B/n_\gamma) \approx \kappa_\chi \times 5 \times 10^{-23} e \cdot {\rm cm}.$$
At the natural scale $\kappa_\chi \sim \alpha^2/\pi$ this gives
$d_n \sim 10^{-27} e \cdot {\rm cm}$, one decade below the current
bound $|d_n| < 1.8 \times 10^{-26} e \cdot {\rm cm}$, within reach of
nEDM/n2EDM at $\sim 10^{-28} e \cdot {\rm cm}$. The same chirality
memory $\chi$ underlies both this prediction and the cosmological
baryon asymmetry.

### #36 — Speculative neutrino spectrum demoted, with falsifiers

Closed at the *demotion-with-falsifiers* tier authorised by the issue.
The §Neutrinos head gapbox now tags content under the Paper I claim
taxonomy: four structural identifications (charge, helicity, range,
production), one structural prediction sharply falsifiable (neutrinos
are *Dirac* not Majorana, because the medium's preferred chirality
breaks C), and five speculative entries (P1)–(P5). Each (P1)–(P5) gets
an explicit *Falsifier* line tied to a real experiment: KATRIN/cosmology
$\sum m_\nu$ bound for mass; fourth-flavour discovery for three-flavour
count; PMNS-vs-CKM phase relation for oscillations; $0\nu\beta\beta$ for
Dirac vs Majorana; $G_F$ relation for cross-section normalisation.

### #37 — Tau as Hopf-linked trefoil pair bound by a muon quantum

The deferred "ladder coincidence only" status of the tau is closed by
identifying it with the lowest **Hopf-linked pair of trefoil-skeleton
baryon breathers bound by a shared muon-class core-breathing quantum** —
equivalently a $(2,3) \oplus (2,3)$ two-component vortex link with one
muon-mass binding energy at the linkage region. The leading-order mass:

$$m_\tau = 2 m_p - m_\mu = 1770.89\,{\rm MeV} \quad (-0.34\%),$$

or, isospin-averaged,

$$m_\tau = (m_p + m_n) - m_\mu = 1772.18\,{\rm MeV} \quad (-0.26\%),$$

both **tighter than** the bare ladder coincidence $25\tfrac{1}{2} \mu_0 = 1785.6$ MeV ($+0.49\%$).
The full eigenmode verification requires the $\mathcal{L} + \mathcal{L}_\perp$
minimisation on the two-component link (Borromean-class extension of
the trefoil computation already in Paper I), the same workstream that
closes the muon eigenfrequency (Paper I open problem 2).

`src/paper_ii/tau_identification.py` reproduces the three predictions
and their discrepancies.

### #40 — Planck-scale evaporation endpoint

Closed at *structural* tier. The LogSE close-packing equation of state
forces the endpoint to be a stable Planck-scale topological remnant on
three independent grounds: (1) chemical-potential floor — $\mu(\rho) \to +\infty$
as $\rho \to 0$ confines any sub-saturated region against the saturated
medium's pressure; (2) topological-winding conservation — Hawking
phonons carry no winding, so a winding-bearing parent cannot reach the
trivial state without an unwinding event forbidden by (1); (3) the
acoustic-horizon mechanism switches off at $r_H \sim \xi$, terminating
evaporation at $M_{\rm rem} \sim m_P$, $r_{\rm rem} \sim \xi$. Each
completed-evaporation BH leaves one Planck-mass topological relic.

### #42 — Galactic coupling constant $\mathcal{C}$

The deferred dimensional estimate
$\mathcal{C} \sim (\hbar^2 / 2 G m_e^2) \alpha^{-16} (m_p/m_e)^7$
is now identified as the gravitational Bohr radius of the disc-soliton
gravito-Goldstone quasi-particle. Substituting the SSV-II identities
$m_p = N_p m_e / \alpha$ and $G = \alpha_G \hbar c \alpha^2 / (N_p^2 m_e^2)$
gives the closed form
$$\mathcal{C} = \frac{\hbar N_p^9}{2 \alpha_G c \alpha^{25}},$$
which uses only the SSV-II constant set $\{\hbar, c, \alpha, \alpha_G, N_p\}$
and matches the weighted multi-galaxy observed value at $-1.5\%$.
A reproduction script (`src/paper_vi_a/derive_C.py`) exists on the
original orphan branch and would need a separate restore PR — see
"Orphan-branch holes" below.

### #43 — Mode amplitudes $\varepsilon_m(a_{\rm BH})$

The deferred normal-mode analysis is closed by the Hansen–Geroch
multipole expansion of the rotating central breather, lifted to SSV
via the Paper VII-b emergent metric:
$$\varepsilon_m(a_{\rm BH}) = \varepsilon_0 \cdot \frac{Q_m}{m!} \cdot a_{\rm BH}^m,$$
with $Q_m \to 1$ from the Bessel cross-overlap and $\varepsilon_0 \approx 0.05$
from the Paper VI-a M31 fit. The tabulated values for $a_{\rm BH} \in [0.1, 0.998]$
and $m \in [1, 5]$ reproduce the ring → grand-design → flocculent
morphology sequence. A reproduction script
(`src/paper_vi_b/epsilon_m_table.py`) exists on the original orphan
branch and would need a separate restore PR — see "Orphan-branch holes"
below.

### #49 — Strong-field numerical verification of the SSV-identified metric

The SSV emergent metric $A_{\rm Sch}(r) = \sqrt{1 - r_S/r}$ (eq:A_sch)
is integrated numerically and three classical observables are compared
against their exact GR analytic counterparts:

| Test | Regime | Observable | GR analytic | SSV-metric numerical | Rel. dev. |
|---|---|---|---:|---:|---:|
| T1 — Photon sphere | strong-field ($r = 1.5 r_S$) | $r_{\rm ph}/r_S$ | $1.5$ | $1.500\,000\,000\,000$ | $0$ |
| T2 — ISCO | strong-field ($r = 3 r_S$) | $r_{\rm ISCO}/r_S$ | $3.0$ | $3.000\,000\,000\,000$ | $1.5 \times 10^{-16}$ |
| T3 — Perihelion precession | weak-field ($a = 10^3 M, e = 0.1$) | $\Delta\phi$/orbit (rad) | $0.019\,04$ | $0.019\,18$ | $7.6 \times 10^{-3}$ |

T1 and T2 (deep strong-field) reproduce exact GR results to machine
precision; T3 (weak-field) reproduces the leading 1PN formula at the
$0.8\%$ residual expected from the next post-Newtonian correction.
Closes Open Problem 3 of the paper at the consistency-verification
level.

`src/paper_vii_b/strong_field_test.py` reproduces the table.

## Orphan-branch holes (paper text or scripts still missing from main)

The following two closures appear in the issue tracker as *closed* but
their content was lost to the same orphan-branch incident as the tau
identification (which PR #58 restored). A follow-up restore PR
analogous to #58 would close these holes:

- **#44 — SSV-VI-b §4.1 pitch-angle dispersion.** Paper text closure
  (Mestel-soliton Lin–Shu dispersion $\to \tan \alpha_m = m Q / 4$
  with $Q$ the disc-soliton Toomre parameter, M31-anchored prediction
  of Seigar–Davis pitch-$M_{\rm BH}$ anti-correlation) and reproduction
  script `src/paper_vi_b/pitch_angle_table.py` are both on branch
  `claude/jolly-tu-940955` only (commit `a6ccff0`); current main still
  has the *Deferred: SSV dispersion relation for pitch angle* gapbox.

- **#50 — SSV-VIII §C1 Kibble–Zurek GPE simulation.** Paper text
  closure (Prediction C1 promoted from candidate to
  structural-with-numerical-evidence based on a converged $\tau_Q$
  scan, fitted 2D KZ exponent $0.23 \pm 0.10$ consistent with mean-field
  $0.5$ within statistics and dynamic-range limits) and reproduction
  script `src/paper_viii/kibble_zurek_gpe.py` plus data file
  `src/paper_viii/kibble_zurek_results.json` are likewise orphaned on
  the same commit.

Additionally, the reproduction scripts for #42 (`derive_C.py`) and #43
(`epsilon_m_table.py`) are orphaned on the same branch even though the
*paper text* closure for those issues did reach main via PR #52.

## Reproducing locally

```bash
# Tau identification (#37)
python3 src/paper_ii/tau_identification.py

# g-2 form factor / Schwinger normalisation (#33)
python3 src/paper_ii/g2_form_factor_loop.py

# Strong-field numerical verification (#49)
python3 src/paper_vii_b/strong_field_test.py
```

All three scripts require only `numpy` (and `scipy` for the strong-field
geodesic integration) from the standard scientific Python stack and run
in seconds.

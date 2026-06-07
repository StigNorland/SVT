# Static 3D Trefoil-Breather Minimisation — Closure Status (2026-05-28)

**Status:** closure memo for issue
[#13](https://github.com/StigNorland/SVT/issues/13).
**Scope:** static branch only. Dynamic reconnection is issue #15.

This note addresses the two remaining unchecked tasks of issue #13 —
specify the observable list, and summarise consequences for Paper I and
the static branch of Paper II.

## 1. Canonical observable list

The static-branch pipeline consumes the trefoil-knot relaxation state
produced by `trefoil_breather_lperp_krylov_static.py` (with the topology
penalty enabled, `instruments/paper_i/topology_penalty.py`) and reports the
following observables. Each is computed by an identified script and
saved to a state or checkpoint file under `papers/SSV-I/data/`.

| Class | Observable | Producing script | Storage |
|---|---|---|---|
| Core | `N_Y` (variants: `n_y_per_xi`, `n_y_per_curve_length`, `n_y_straight`) | `trefoil_breather_observables.py` :: `ExtractionSummary` | JSON sweep checkpoints |
| Core | `F` (variants: `f_factor_interior`, `f_factor_raw`, `f_factor_straight_int`, `f_factor_straight_raw`) | `trefoil_breather_observables.py` :: `ExtractionSummary` | JSON sweep checkpoints |
| Core | total energy (`e_total_raw`, `e_interior`, `e_anchor_shell`, `e_bulk_residual`) | `trefoil_breather_observables.py` :: `ExtractionSummary` | JSON sweep checkpoints |
| Component | line / cavity / bulk energies (`e_line`, `e_cavity`, `e_bulk_residual`, `mu_0_grid`, `mu_0_straight`) | `trefoil_breather_observables.py` :: `ExtractionSummary` | JSON sweep checkpoints |
| Geometry | branch lengths, junction neighbourhood, effective breather radius (`l_curve_geometric`, `l_line_tube`, `tube_volume`, `cal_arc_half_width`) | `trefoil_breather_observables.py` :: `ExtractionSummary` | JSON sweep checkpoints |
| Geometry | core-thickness / topology preservation (`min_density`, `min_density_position`, `vortex_link_count`) | `topology_penalty.py` + `trefoil_breather_observables.py` | NPZ state |
| Far-field | shell deficit, far-field moment, effective radius (`shell_mean_deficit`, `far_field_moment`, `effective_radius`) | `alpha_g_proxy.py` (consumes sweep JSONs) | derived JSON |
| Solver diagnostics | energy monotonicity, residual norm, accepted steps, energy violations | `trefoil_breather_lperp_krylov_static.py` | per-run state header |
| Solver diagnostics | grid / box sensitivity flags | `trefoil_breather_refinement.py` | refinement-sweep JSONs |

Machine-readable spec lives in
`instruments/paper_i/trefoil_breather_observables.py` :: `ExtractionSummary`
(31 fields) and in the shared `StaticDiagnostics` dataclass from
`instruments/shared_numerics/static_branch.py`.

## 2. Convergence and tolerance status

The validation gates from `trefoil-breather-minimisation-plan.md` §"Validation Gates"
are met in part:

| Gate | Status | Notes |
|---|---|---|
| `N_Y` within tolerance under grid refinement | not yet | Computed at $n^3 = 24^3, 48^3, 72^3$ but no dedicated $N_Y$ cross-grid sweep; the n=24→48 spread on the related $F$ observable is large (~54% at the unrescaled cutoff). |
| `F` within tolerance under box-size changes | partial | n=48 / n=72 agree at ~6% at the canonical cutoff $R = 1.18\,\xi$ (see `f-factor-grid-converged-checkpoint.md`); coarser n=24 disagrees by ~54%; the cutoff itself is not yet derived geometrically. |
| Recovered from multiple nearby initial conditions | not yet | Topology-penalty pipeline preserves the seeded trefoil but has not been seeded from non-trefoil initial conditions. |
| Topology survives without ambiguous reconnection | met | The topology penalty (`topology-penalty-checkpoint.md`) maintains 50 vortex links from initial 166 at $\mu=1000$; the same configuration without penalty loses all 166 links by step 100. |
| Energies accompanied by numerical controls | met | All sweep JSONs record `n`, `hw`, $\lambda_\perp$, step count, preconditioner, and the topology-penalty parameters together with the observables. |

**Headline closure-status:** the static pipeline is **candidate-grade**, not
closure-grade. It produces reproducible $N_Y$ and $F$ values once a grid
and a cutoff are fixed, with topology preservation now mechanised; the
remaining gaps are (i) the cross-grid $N_Y$ sweep, (ii) the geometric
derivation of the cutoff $R = 1.18\,\xi$ that fixes the $F$ scale, and
(iii) recovery from independent initial conditions.

## 3. Consequences for Paper I

The Paper I claim-status work
(`papers/SSV-I/main.tex` §"Claim Status", landed in commit `eb40440`
under issue #17) already encodes the static-branch closure status:

- The $N_Y \approx 3.007$ headline is labelled **candidate**, with the
  $\pm 0.002$ band identified as fit reproducibility at a single grid
  family rather than a measured cross-grid spread.
- The $F \approx 4.47$ headline is labelled **candidate**, with the
  $n^3 = 48^3, 72^3$ agreement ~6% explicitly stated and the cutoff
  sensitivity $\mathrm{d}\ln F / \mathrm{d}\ln R \approx -0.94$ recorded.
- The proton-mass agreement is reframed from "$0.3\%$ from CODATA" to
  $m_p \approx 930$–$954$ MeV (~1.5% from CODATA) with cutoff
  uncertainty, and linked to issue #13 as the upgrade workstream.
- The earlier "$N_Y$ independent of grid resolution above $128^3$"
  statement was corrected: no $128^3$ grid was ever run; the actual
  tested grids are $24^3, 48^3, 72^3$ at half-width $6\xi$.

No further Paper I edits are required to reflect the present #13 status.
What would change the Paper I framing is the closure work itself
(dedicated $N_Y$ sweep + geometric cutoff derivation), at which point
the corresponding rows of the Claim Status table can be promoted from
**candidate** to **derived**.

## 4. Consequences for the static branch of Paper II

Paper II §"Gravity" ($\alpha_G$ derivation) takes the gravitational
coupling constant $\alpha_G$ from CODATA and demonstrates structural
consistency with the Paper I mass ladder to $0.6\%$. The intended
first-principles route is:

```
relaxed 3D breather  →  δV_p, a_p, ω_p, ρ_0
                     →  Q_p ~ δV_p · (a_p/ξ)^3
                     →  G = ρ_0 · ω_p^2 · Q_p^2 / (8π m_p^2)
                     →  α_G = G · N_p^2 · m_e^2 / (ℏc α^2)
```

The static-branch closure of issue #13 delivers the first arrow (the
relaxed breather geometry); the second to fourth arrows are issue #14
($\alpha_G$ from the relaxed breather). The Paper II static-branch
status is therefore inherited from #13:

- The current Paper II structural consistency check **does not require**
  #13 to be closed; it cites $\alpha_G$ from CODATA.
- The Paper II claim **becomes a derivation** when #13's geometric
  observables (`δV_p`, `a_p`, `ω_p`, `ρ_0`) are extracted at
  closure-grade and consumed by #14.
- The candidate-grade status of $N_Y$ and $F$ propagates: the Paper II
  derivation of $\alpha_G$ from the breather will inherit whatever
  cutoff / cross-grid uncertainty $N_Y$ and $F$ carry at #13 closure
  time.

Paper II main.tex already labels the $\alpha_G$ derivation as a
"Structural consistency check, not derivation" in its abstract, so no
Paper II edits are required to reflect the present #13 status either.

## 5. What would close issue #13 fully

The three open items above translate into three concrete next-step runs
(none of which are blocked on further design decisions):

1. **Dedicated $N_Y$ cross-grid sweep.** Run the topology-penalty
   Krylov pipeline at $n^3 = 48^3, 72^3, 96^3$ at fixed half-width
   $6\xi$, all with $\mu = 400$ and $\rho_{\rm target} = 0.01$
   (the configuration that gives 82\% topology preservation per
   `penalty-expansion-checkpoint.md`). Report $N_Y$ at the same
   straight-vortex cutoff $R = 1.18\,\xi$ used for $F$. The tolerance
   gate proposed in the minimisation plan is $|\Delta N_Y / N_Y| < 1\%$
   between adjacent grids.

2. **Geometric derivation of the cutoff $R = 1.18\,\xi$.** Currently
   $R = 1.18\,\xi$ is the inter-strand half-spacing of the trefoil with
   minor radius $0.85\,\xi$. Demonstrating that $N_Y \cdot F$ is
   cutoff-invariant (or showing the geometric scale at which the
   product is stationary) would lift the joint observable to
   derivation status even without independently fixing each factor.

3. **Independent initial-condition recovery.** Seed the same topology
   from at least one non-trefoil initial condition (e.g. a perturbed
   trefoil, or two linked rings that reconfigure into the trefoil
   under relaxation) and verify the same converged $N_Y$ and $F$ are
   recovered.

Each of these is a finite-compute run on the existing pipeline; they do
not require new solver development. The remaining solver work
(higher-order Krylov / projected-gradient topology constraint /
analytic tangent-space projection) is **not** on the critical path for
closing #13 — the topology penalty mechanism already achieves
preservation; the gates that remain open are sweep + cutoff + recovery,
not topology stability.

## Out-of-scope items not blocking #13 closure

- Dynamic reconnection: issue #15.
- $\alpha_G$ from the relaxed breather: issue #14 (consumes #13 output).
- Dynamic-branch refinement sweeps: issue #16.
- Strong-field GR validation: Paper VII-b §6.3 open problem 3.
- Cosmogonic application: Paper VIII.

# Thin-Ring Muon Matrix Element: Feasibility Memo (revised 2026-05-19)

> **Status (2026-05-30): superseded by Path B null.** Numerical claims in this note about the muon eigenfrequency reaching $\omega/\omega_c = 0.207$, the $\delta_{\rm relax}$ calibration, the $\alpha$-harmonic ladder identification, or the $1/\sqrt{N_{\rm modes}}$ basis-truncation residual are now governed by `papers/SSV-I/path-b-eigenvalue-result.md`: that test showed the muon agreement is not basis-robust (drifts $\pm 13\%$ across 4 bases, empty window in 2 of 4) and the pion rung is absent in every basis. Structural sub-results that stand on their own (operator algebra, analytic derivations, the cubic-vertex one-loop result, dimensional setup) remain valid in isolation; what is superseded is their use as evidence for the ladder identification or as a closure path to it. Quarantined inputs: `instruments/_fitted_quarantine/`. Tracking: issue #66.

**Purpose.** This memo records the feasibility status of the thin-ring analytic
closure of the muon eigenfrequency. The original version asked whether the
ring-breathing / Kelvin matrix element was clean enough to pursue. Later
helicity-bridge notes sharpen the answer: the naive leading-order overlap is
indeed killed by the azimuthal selection rule, but the viable target is the
helicity-projected chiral bridge in the reduced BdG problem.

**Current verdict.** The thin-ring route is still viable, but the calculation
should no longer be framed as a raw
`L^\perp_{R,K_{\sigma,\pm}}` overlap. The paper-level target is now:

```text
show that the helicity-projected current-curl bridge gives pi/4 at leading
thin-ring order, then quantify the finite-alpha and relaxed-torus corrections.
```

This moves the memo from "is there any nonzero coupling?" to "is the existing
leading-order helicity bridge robust enough to become a derivation?" The latest
self-adjoint weak-form boundary audit is encouraging: the reduced route is back
in play as a controlled prototype, though not yet as a final quoted muon number.

---

## 1. Thin-Ring Setup

The electron torus has major radius

```math
R_e = \xi / \alpha,
```

with core radius of order `\xi`. The thin-ring parameter is therefore

```math
\epsilon = \xi/R_e = \alpha \simeq 1/137.
```

Near the ring centreline use local tube coordinates

```math
r-R_e = \rho\cos\vartheta,\qquad z=\rho\sin\vartheta,\qquad \varphi=\text{major-ring angle}.
```

The volume element is

```math
d^3x = \rho\,(R_e+\rho\cos\vartheta)\,d\rho\,d\vartheta\,d\varphi
     = R_e\rho\,d\rho\,d\vartheta\,d\varphi + O(\alpha).
```

The leading-order background is the straight vortex profile wrapped around the
ring:

```math
\Psi_0(\mathbf{x}) \simeq \sqrt{\rho_0}\,f(\rho/\xi)e^{i\vartheta}.
```

At this order the background is independent of `\varphi`; all `\varphi`
dependence belongs to the Kelvin perturbations.

## 2. What the Original Selection Rule Got Right

The raw ring-breathing mode has no major-ring phase:

```math
\Phi_R \propto -R_e f'(\rho/\xi)\cos\vartheta\,e^{i\vartheta},
\qquad m_\varphi=0.
```

The Kelvin displacement modes carry

```math
K_{\sigma,\pm}\propto e^{\pm i\varphi},
\qquad m_\varphi=\pm1.
```

For an exactly axisymmetric thin-ring background, the local current-curl
operator does not shift `m_\varphi`. Therefore the direct leading-order overlap

```math
L^\perp_{R,K_{\sigma,\pm}} =
\langle C[\Phi_R]\,|\,C[K_{\sigma,\pm}]\rangle
```

vanishes at `O(\alpha^0)`. This is a real selection rule, not a bookkeeping
mistake.

The important correction is interpretive: this vanishing does **not** kill the
muon route. It only says the raw `R-K` matrix element is the wrong leading
object to promote as the analytic bridge.

## 3. Updated Viable Target: Helicity Current-Curl Bridge

The later note
[`notes/muon-helicity-bridge-derivation.md`](notes/muon-helicity-bridge-derivation.md)
identifies the relevant reduced target. In the helicity Kelvin basis, the
current-curl second variation supplies a normalized bridge coefficient with
three factors:

```math
\lambda_\perp^{\rm BdG}
=
\left({\pi\over4}\right)
\left(\lambda {m_0\over\rho_0}\right)
\left({R_e\over\xi}\right)^2.
```

Paper I fixes

```math
\lambda m_0/\rho_0 = \alpha^2,
\qquad R_e/\xi = \alpha^{-1},
```

so the leading thin-ring coefficient becomes

```math
\boxed{\lambda_\perp^{\rm BdG}=\pi/4.}
```

This is the clean version of the old "`\alpha^{-2}` scaling" statement. The
large geometric factor is not the final coupling by itself; it cancels the
small transverse stiffness `\alpha^2`, leaving an order-one bridge.

## 4. Why `pi/4` Is Plausible

The leading coefficient decomposes into simple angular and normalization pieces:

```math
{1\over2}_{\rm helicity}
{1\over2}_{\rm BdG}
\int_0^{2\pi}\cos^2\vartheta\,d\vartheta
= {\pi\over4}.
```

In words:

- The helicity basis contributes one factor of `1/2`.
- The symmetrized BdG second variation contributes one factor of `1/2`.
- The current-curl projection selects the even meridional angular channel,
  giving the `\cos^2\vartheta` integral.

This gives a concrete analytic target. The feasibility question is no longer
"can a nonzero bridge exist?" but "does the full second variation preserve this
leading coefficient once all curvature and background corrections are restored?"

## 5. Numerical Status

The helicity-projected calculation cited in
[`notes/muon-helicity-bridge-derivation.md`](notes/muon-helicity-bridge-derivation.md)
reported, at the reduced leading-order level,

```text
lambda_perp^code = pi/4
lowest positive  = 0.2068070675
target           = 0.207
fractional error = -9.32e-4
```

Later branch-tracking notes with explicit Kelvin self-induction are more
cautious: the muon-window hybrid remains suggestive but not fully converged.
The important distinction is:

- The `pi/4` helicity bridge is a leading thin-ring analytic target.
- The full muon eigenvalue still depends on finite-alpha corrections, relaxed
  torus geometry, Kelvin self-induction, and basis/box convergence.

## 6. Remaining Risks

### 6.1 PC-sized first checks

The first finite-alpha diagnostics have now been added as
[`../../instruments/paper_i/thin_ring_alpha_correction.py`](../../instruments/paper_i/thin_ring_alpha_correction.py).
The script checks two PC-sized pieces of the finite-alpha problem:

1. the angular part of straight-core metric/Jacobian corrections of the form

```math
(1+\alpha x\cos\vartheta)^p .
```

2. the standard `O(\alpha)` curl-operator angular building blocks generated by
   expanding `h_\varphi=R_e+\rho\cos\vartheta`: `cos(theta)` multipliers,
   `sin(theta)` terms from `\partial_\vartheta h_\varphi`, and
   `cos(theta)\partial_\vartheta` / `sin(theta)\partial_\vartheta` pieces.

It also has an optional finite-alpha scan:

```powershell
python instruments/paper_i/thin_ring_alpha_correction.py --finite-alpha-scan
```

This reuses the existing normalized current-curl overlap machinery and varies
`alpha` from `1/40` through the physical `1/137.035999084` scale. The default
scan uses the toy profile; the aligned scan uses the numerical LogSE vortex
profile:

```powershell
python instruments/paper_i/thin_ring_alpha_correction.py --finite-alpha-scan --scan-profile numerical --scan-profile-n 800
```

The same command can deliberately turn on the repository's curved-background
ansatz, for example:

```powershell
python instruments/paper_i/thin_ring_alpha_correction.py --finite-alpha-scan --scan-curvature-coeffs "1,0,0"
python instruments/paper_i/thin_ring_alpha_correction.py --finite-alpha-scan --scan-phase-coeffs "1,0,0"
```

The result is:

```text
leading bridge factor = 0.785398163397 = pi/4
int cos^3(theta) dtheta = 0
verdict = pure straight-core metric/Jacobian factors do not shift pi/4 at O(alpha)
operator verdict = standard O(alpha) curl angular building blocks vanish
                   against the leading even channel
finite-alpha scan = normalized straight-profile overlaps show no detectable
                    linear alpha drift
```

For the standard geometric factors:

| factor | `c1` coefficient | first nonzero geometric correction |
|--------|------------------|------------------------------------|
| Jacobian `r = R_e + rho cos(theta)` | `0` | none from this factor alone at `O(alpha^2)` |
| one inverse-radius factor | `0` | `0.75 x^2 alpha^2` |
| two inverse-radius factors | `0` | `2.25 x^2 alpha^2` |

So the leading PC-sized result is encouraging:

```math
\lambda_\perp^{\rm BdG}
= {\pi\over4}\,[1+0\cdot\alpha+O(\alpha^2)]
```

for pure straight-core metric/Jacobian factors and for the standard angular
pieces of the first-order curl expansion. This does not yet cover
relaxed-background corrections or the full second variation, but it removes the
two simplest `O(alpha)` threats.

Both toy-profile and numerical-profile straight-core scans give the same
message numerically:

| alpha | `R_e` | `|chi,K|` relative | `|R,K|` relative |
|-------|-------|--------------------|------------------|
| `0.025` | `40` | `1.000000000000` | `1.000000000000` |
| `0.0166666667` | `60` | `1.000000000000` | `1.000000000000` |
| `0.0125` | `80` | `1.000000000003` | `1.000000000005` |
| `0.01` | `100` | `1.000000000003` | `1.000000000005` |
| `0.00729735257` | `137.035999084` | `1.000000000003` | `1.000000000005` |
| `0.00555555556` | `180` | `1.000000000003` | `1.000000000005` |

The toy-profile fitted relative slopes are `-1.84e-10` for the `chi-K` bridge
and `-3.44e-10` for the `R-K` bridge. With `--scan-profile numerical`, the
slopes are still numerical noise: `-2.40e-9` for `chi-K` and `-3.75e-10` for
`R-K`. At this reduced level, straight-core finite-radius geometry is flat in
`alpha`.

The deliberately curved toy background is different. With a unit amplitude
curvature coefficient, the scan reports:

```text
curved-background toy ansatz shows alpha drift
chi relative slope = -2.64e-01
R relative slope   =  9.37e-02
```

With a unit phase-curvature coefficient, it reports:

```text
curved-background toy ansatz shows alpha drift
chi relative slope =  1.83e-01
R relative slope   = -2.66e-02
```

These coefficients are intentionally order-one probes, not measured relaxed
torus coefficients. The point is diagnostic: pure straight-ring geometry does
not create an `O(alpha)` correction, but a curved equilibrium background can.
So the next real risk is the size and parity of the actual relaxed-torus
amplitude/phase correction.

### 6.2 Still-open risks

The thin-ring programme is green-lit only at leading order. The paper-level
derivation still needs four checks.

1. **Finite-alpha curvature corrections.** Replace `r -> R_e` only at leading
   order, then compute the full `O(\alpha)` correction from the complete curl
   operator. The metric/Jacobian part and the standard angular curl building
   blocks now appear parity-forbidden at first order, and both toy-profile and
   numerical-profile straight-core scans show no detectable linear drift. Any
   surviving first-order term must come from background relaxation or
   full-second-variation structure not captured by these reduced diagnostics.

2. **Relaxed torus background.** The wrapped straight-vortex profile is a
   leading ansatz. A curved equilibrium torus may shift the radial profile and
   angular weights. The curved toy scan confirms that order-one background
   coefficients can create percent-level drift across the alpha scan, so this
   is now the highest-value next calculation.

3. **Full second variation.** Verify that the complete
   `\mathcal L_\perp` second variation leaves the `pi/4` coefficient unchanged
   at leading order and moves only subleading terms.

4. **Convergence of the muon-window branch.** The reduced branch must be tracked
   under larger bases, larger boxes, and explicit Kelvin self-induction before
   it can be called a derived muon mass.

## 7. Relaxed-Background Convergence Check

The reduced curved-torus relaxation coefficients were swept across grid size,
box half-width, radial profile resolution, and finite-difference step, then each
coefficient set was fed through the finite-alpha bridge scan with the numerical
BdG radial profile.

```powershell
python instruments/paper_i/thin_ring_delta_relax_sweep.py `
  --grids 25 31 `
  --half-widths 5 6 `
  --profile-ns 800 `
  --fd-steps 0.25 `
  --output papers/SSV-I/data/delta-relax-sweep-numerical-profile-smoke-2026-05-20.json

python instruments/paper_i/thin_ring_delta_relax_sweep.py `
  --grids 31 `
  --half-widths 5 6 `
  --profile-ns 800 1200 `
  --fd-steps 0.20 0.25 0.30 `
  --output papers/SSV-I/data/delta-relax-sweep-numerical-profile-fd-profile-2026-05-20.json

python instruments/paper_i/thin_ring_delta_relax_sweep.py `
  --grids 37 `
  --half-widths 5 6 `
  --profile-ns 800 `
  --fd-steps 0.25 `
  --output papers/SSV-I/data/delta-relax-sweep-numerical-profile-n37-2026-05-20.json
```

The numerical-profile result is stable in sign and remains a few-percent
correction:

| sweep slice | `delta_relax_chi` | `delta_relax_R` | comment |
|-------------|-------------------|-----------------|---------|
| `n=25,31`, `hw=5,6` | `+4.210% +/- 0.615%` | `+0.210% +/- 0.035%` | sign and scale check |
| `n=31`, `profile_n=800,1200`, `fd=0.20,0.25,0.30` | `+3.999% +/- 0.455%` | `+0.199% +/- 0.026%` | profile and finite-difference axes stable |
| `n=37`, `hw=5,6` | `+3.791% +/- 0.545%` | `+0.184% +/- 0.031%` | finest grid tested |

The `profile_n` and `finite_diff_step` axes are effectively converged at this
precision. The remaining spread is dominated by the half-width systematic: at
`n=37`, `hw=5` gives `delta_relax_chi = +3.405%`, while `hw=6` gives
`+4.176%`. Increasing `n` from 25 to 37 nudges the central value downward but
does not make the correction grow, flip sign, or become erratic.

Therefore the current reduced-background estimate is:

```math
\lambda_\perp^{\rm BdG}
= {\pi\over4}\,[1+\delta_{\rm relax}+c_2\alpha^2+\cdots],
\qquad
\delta_{\rm relax}=+0.038\pm0.005.
```

This supersedes the older toy-profile bridge estimate, which gave the opposite
sign. The sign flip is not interpreted as a physical instability; it is a
profile-mismatch artifact. With the numerical BdG profile used consistently in
the straight and relaxed scans, the bridge correction is small, positive, and
stable enough to support a paper-level leading-order derivation, subject to the
remaining full-second-variation check.

### 7.1 Next calculation after this checkpoint

Do **not** spend time computing the old raw
`L^\perp_{R,K_{\sigma,\pm}}` overlap. It is expected to vanish by the leading
azimuthal selection rule.

The next useful calculation is now to propagate the corrected coefficient
through the reduced BdG eigenproblem:

```math
\lambda_\perp^{\rm code}
= {\pi\over4}\,(1+\delta_{\rm relax})
```

with `\delta_{\rm relax}` swept across the `+0.038 +/- 0.005` band. If the
muon eigenfrequency remains close to the target across that band, the thin-ring
bridge has graduated from a structural derivation to a quoted numerical
prediction with an uncertainty.

### 7.2 First propagation through the reduced BdG branch

The corrected coefficient band was propagated through the Kelvin-augmented
reduced BdG tracker at `n=31`, `half_width=5`, `profile_n=1200`,
`kelvin_phi_n=512`:

| `delta_relax` | `lambda_perp` | selected `omega_mu/omega_c` | relative miss vs `0.207` |
|---------------|---------------|-----------------------------|---------------------------|
| `0.000` | `0.785398163` | `0.198145299` | `4.278%` |
| `0.033` | `0.811316303` | `0.202730772` | `2.062%` |
| `0.038` | `0.815243294` | `0.203418905` | `1.730%` |
| `0.043` | `0.819170284` | `0.204105317` | `1.398%` |

So the relaxed-background correction moves the selected branch in the right
direction and cuts the miss by more than half, but it does not close the target
by itself. A local linear extrapolation would require
`\delta_{\rm relax}\approx +0.064`, outside the current relaxed-band estimate.
The selected branch is still Kelvin dominated (`~96%` Kelvin weight), so the
next uncertainty to sweep is the Kelvin self-induction/core-radius calibration,
followed by grid/box propagation and the full second variation.

A first PC-sized follow-up shows that the remaining miss is not mainly a
Kelvin-core-radius calibration issue. At the corrected central value
`\delta_{\rm relax}=0.038`, changing `kelvin_core_radius` from `0.75` to `1.25`
moves the coarse `n=13`, `half_width=4` branch from `0.208710` to `0.207678`,
but the `n=21`, `half_width=4` branch remains far below target,
`0.195992` to `0.195045`. Thus the near-hit at `n=13` is not reliable
convergence evidence. The reduced Kelvin-augmented frequency prediction remains
grid-sensitive, even though the relaxed `pi/4` bridge correction itself is
stable.

The coarse-grid artifact is now identified more specifically: nearest-to-target
selection is switching between the lower and upper hybrid branches. For
`half_width=4` and `\delta_{\rm relax}=0.038`, the two hybrid branches evolve as

| `n` | lower hybrid | upper hybrid | nearest-to-target branch |
|-----|--------------|--------------|--------------------------|
| `13` | `0.142635` | `0.208083` | upper |
| `17` | `0.174073` | `0.275500` | lower |
| `21` | `0.195417` | `0.326200` | lower |
| `25` | `0.210496` | `0.351324` | lower |
| `31` | `0.224313` | `0.380247` | lower |

For `half_width=5`, the same corrected coefficient gives

| `n` | lower hybrid | upper hybrid | nearest-to-target branch |
|-----|--------------|--------------|--------------------------|
| `21` | `0.170431` | `0.226606` | upper |
| `25` | `0.187780` | `0.258504` | lower |
| `31` | `0.204102` | `0.293952` | lower |

So the reduced BdG frequency extraction cannot be judged by "closest branch to
0.207". The next reliable computation must track branch identity by eigenvector
overlap or Krein signature across grids. Until then, the paper-safe result is
only the corrected bridge coefficient, not the final muon eigenfrequency.

That branch-identity computation was then run. Adjacent-grid matches are clean:
the overlap/Krein continuation gives match scores `0.989--0.999`, Euclidean
overlaps `0.987--0.999`, and all tracked hybrid branches keep positive Krein
sign. The branch identities at the corrected central coefficient are:

| `half_width` | `n` | lower identity branch | upper identity branch |
|--------------|-----|----------------------|----------------------|
| `4` | `13` | `0.142635` | `0.208083` |
| `4` | `17` | `0.174073` | `0.275500` |
| `4` | `21` | `0.195417` | `0.326200` |
| `4` | `25` | `0.210496` | `0.351324` |
| `4` | `31` | `0.224313` | `0.380247` |
| `5` | `21` | `0.170431` | `0.226606` |
| `5` | `25` | `0.187780` | `0.258504` |
| `5` | `31` | `0.204102` | `0.293952` |
| `6` | `21` | `0.146648` | `0.168990` |
| `6` | `25` | `0.166168` | `0.196942` |
| `6` | `31` | `0.186147` | `0.231893` |

This confirms the diagnosis. The coarse near-hit is the upper identity branch,
which runs away upward at `half_width=4`. The lower branch can cross near the
target at an intermediate grid, but it also continues drifting. Larger boxes
push both identities downward. Therefore the reduced Kelvin-augmented basis is
not yet a closure-grade frequency extractor. The safe conclusion remains:
`\lambda_\perp^{\rm BdG}` has a stable corrected leading coefficient, while
the final muon eigenfrequency needs a stabilized basis, the full second
variation, or the full circumferential grid.

A first basis-enrichment check strengthens this conclusion. At
`half_width=5`, `n=31`, `delta_{\rm relax}=0.038`, and `kelvin_phi_n=128`, the
tracked branch values are:

| reduced basis | branch values at `n=31` | nearest miss vs `0.207` |
|---------------|-------------------------|--------------------------|
| two-core, helicity Kelvin | `0.205511`, `0.295392` | `0.72%` low |
| four-core, helicity Kelvin | `0.196543`, `0.305117` | `5.05%` low |
| two-core, displacement Kelvin | `0.341269` | `64.9%` high |
| two-core, breathing Kelvin | `0.218028` | `5.33%` high |

The branch matching remains clean in all cases, so this is not a continuation
failure. It is basis dependence. The two-core/helicity setup is target-adjacent
at this grid, but adding the conjugate core partners or changing Kelvin seed
family moves the prediction substantially. Therefore the muon-frequency track
should not proceed by tuning `\lambda_\perp`, Kelvin core radius, or
nearest-target selection. The next meaningful step is either the full second
variation of the current-curl term in an enriched basis or the full
circumferential BdG grid.

That full second-variation check has now been started. The BdG implementation
now has a `current_curl_model=full` option that adds the missing
background-vorticity term

```math
\int(\nabla\times j_0)\cdot(\nabla\times j_2)\,d^3x
```

to the previous `|curl j_1|^2` block. At `half_width=5`, `n=31`,
`delta_{\rm relax}=0.038`, and `kelvin_phi_n=128`, the full model gives:

| reduced basis | full-second-variation branch values at `n=31` | nearest miss vs `0.207` |
|---------------|-----------------------------------------------|--------------------------|
| two-core, helicity Kelvin | `0.216509`, `0.237616` | `4.59%` high |
| four-core, helicity Kelvin | `0.204752`, `0.237616` | `1.09%` low |
| two-core, displacement Kelvin | `0.104888`, `0.129835`, `0.343945` | `37.3%` low |
| two-core, breathing Kelvin | `0.280803` | `35.7%` high |

This is a meaningful improvement for the enriched helicity basis: adding the
full second variation moves the four-core/helicity lower branch from `0.196543`
to `0.204752`, close to the muon target. But it is still not closure-grade,
because the result remains strongly Kelvin-seed dependent. The next reduced
calculation should combine the Kelvin seed families in a single basis instead
of choosing helicity, displacement, or breathing as separate ansatz spaces.

The combined Kelvin basis has now been tested. It includes breathing, radial
displacement, vertical displacement, and helicity candidates, with each
azimuthal sector orthogonalized to remove duplicate directions. At
`core_basis=four`, `current_curl_model=full`, and `delta_relax=0.038`, the
tracked branches are:

| `half_width` | `n` | lower branch | pure-Kelvin branch | nearest miss |
|--------------|-----|--------------|--------------------|--------------|
| `5` | `21` | `0.167837` | `0.199404` | `3.67%` low |
| `5` | `25` | `0.185857` | `0.217172` | `4.91%` high |
| `5` | `31` | `0.205374` | `0.237633` | `0.79%` low |
| `6` | `21` | `0.146962` | `0.153506` | `25.8%` low |
| `6` | `25` | `0.165525` | `0.170397` | `17.7%` low |
| `6` | `31` | `0.186942` | `0.191445` | `7.51%` low |

This is the best reduced result so far: the `half_width=5`, `n=31` combined
full-basis branch is within one percent of the target and no longer depends on
choosing a single Kelvin seed family. But the `half_width=6` branch remains
significantly low. The remaining obstruction is therefore box-size or boundary
sensitivity, not seed-family incompleteness. The next reduced check should be a
larger-`n` and boundary-condition audit before attempting a full circumferential
grid.

The first spacing-controlled box audit shows that part of this split was caused
by changing resolution at the same time as changing box size. Since
`dr = 2*half_width/n`, the earlier `half_width=6,n=31` point was much coarser
than `half_width=5,n=31`. Rerunning `half_width=6` at `n=37` gives nearly the
same spacing as `half_width=5,n=31` and restores a target-adjacent branch:

| box/grid | `dr` | mixed lower branch | pure-Kelvin branch | nearest miss |
|----------|------|--------------------|--------------------|--------------|
| `hw=5,n=31` | `0.323` | `0.205374` | `0.237633` | `0.79%` low |
| `hw=6,n=31` | `0.387` | `0.186942` | `0.191445` | `7.51%` low |
| `hw=6,n=37` | `0.324` | `0.202869` | `0.205317` | `0.81%` low |
| `hw=5,n=37` | `0.270` | `0.220134` | `0.247399` | `6.34%` high |

So the reduced model is not dead: the combined/full/four-core branch remains
near target when the larger box is run at matched spacing. But it is also not
closed: refining `hw=5` to `n=37` overshoots upward. The next decisive reduced
audit is a constant-`dr` sequence over `half_width=5,6,7`, followed by a
fixed-box refinement sequence. If those fail to settle, the full
circumferential grid is required.

That unattended reduced audit has now been run. The constant-spacing sequence

```text
hw=5,n=31 -> hw=6,n=37 -> hw=7,n=43
```

shows clean continuation from `hw=5` to `hw=6`, but the `hw=7` extension loses
overlap/Krein continuity:

| point | `dr` | branch values | continuation status |
|-------|------|---------------|---------------------|
| `hw=5,n=31` | `0.323` | `0.205374`, `0.237633` | start |
| `hw=6,n=37` | `0.324` | `0.202869`, `0.205317` | clean match |
| `hw=7,n=43` | `0.326` | `0.238321`, `0.176028` | poor match / Krein flip |

Fixed-box refinement then shows that the near-target points are crossings rather
than plateaus:

| fixed box | tracked values | conclusion |
|-----------|----------------|------------|
| `hw=5` | `0.205374 -> 0.220134 -> 0.231630` | monotone upward drift |
| `hw=6` | `0.186942 -> 0.202869 -> 0.215235` | monotone upward drift |
| `hw=7` | `0.174852/0.186757 -> 0.238321/0.176028` | identity instability |

A `kelvin_phi_n=256` check shifts the near-target values by only about
`0.0013`, so this is not self-induction quadrature noise.

The resulting reduced-basis verdict is:

```text
The low-hanging reduced-BdG options have been exhausted. The corrected
thin-ring bridge is robust, branch continuation is fixed, Kelvin seed
dependence is reduced by the combined basis, and the full second variation is
included. The remaining obstruction is box/refinement sensitivity of the
reduced projection ansatz itself. The muon eigenfrequency now needs either a
deliberate boundary-condition redesign or the full circumferential BdG grid.
```

The first boundary redesign was also tested. A smooth projection window now
separates the physical projection tube from the numerical square box:

```text
projection_window = smooth
window_radius     = R
window_taper      = T
```

This weight is used in Gram-Schmidt, normalization, operator projection, the
current-curl block, and the full second-variation background-vorticity term.
With `R=4`, `T=1`, and matched spacing:

| point | smooth-window target branch |
|-------|-----------------------------|
| `hw=5,n=31` | `0.207768` |
| `hw=6,n=37` | `0.207505` |
| `hw=7,n=43` | identity instability; new `0.194252` negative-Krein branch |

A tighter `R=3.5`, `T=1` window gives the same structure:

| point | smooth-window target branch |
|-------|-----------------------------|
| `hw=5,n=31` | `0.210151` |
| `hw=6,n=37` | `0.209879` |
| `hw=7,n=43` | identity instability; new `0.199098` negative-Krein branch |

The window therefore fixes much of the artificial `hw=5/hw=6` mismatch, but it
does not close the calculation. Fixed-box smooth-window refinement still drifts:

| fixed box | tracked branch |
|-----------|----------------|
| `hw=5` | `0.207768 -> 0.222995 -> 0.234855` |
| `hw=6` | `0.190886 -> 0.207505 -> 0.220576` |

The smooth-window boundary redesign is useful and should stay in the diagnostic
tooling, but by itself it does not produce a closure-grade muon eigenfrequency.
It motivated the more fundamental self-adjoint reduced boundary operator tested
next.

The self-adjoint prototype replaces the strong-form projected Laplacian in the
normal BdG block by a weak energy bilinear form:

```math
\langle a,Lb\rangle_W =
\int W\,2\pi r\left[
{1\over2}\left(\partial_r a^*\partial_r b+\partial_z a^*\partial_z b
             + {m^2\over r^2}a^*b\right)+V a^*b
\right]\,dr\,dz.
```

This was run with the same combined Kelvin basis, four-core chiral sector,
full current-curl second variation, smooth `R=4`, `T=1` projection window, and
central `\delta_{\rm relax}=0.038`. The high-resolution weak-form checkpoints
are:

| point | weak-form tracked branch | miss vs `0.207` |
|-------|--------------------------|-----------------|
| `hw=5,n=49`, `kelvin_phi_n=128` | `0.206278` | `0.35%` low |
| `hw=6,n=59`, `kelvin_phi_n=128` | `0.207313` | `0.15%` high |
| `hw=7,n=69`, `kelvin_phi_n=128` | `0.207762` | `0.37%` high |
| `hw=6,n=59`, `kelvin_phi_n=256` | `0.206035` | `0.47%` low |

The Gram diagnostics remain benign at the high-resolution points: minimum Gram
eigenvalues are about `0.51`, condition numbers are about `3.9`, and the
continued branch has positive Krein signature with clean overlap continuation.
This is the first reduced-boundary audit that simultaneously fixes the
strong-form overshoot, tames fixed-box refinement drift, and restores matched-box
agreement across `hw=5,6,7`.

The reduced route is therefore no longer exhausted. The next low-hanging checks
are uncertainty/refinement checks rather than an immediate full circumferential
grid: Kelvin quadrature convergence, one more matched-spacing refinement if it
fits the runtime budget, and propagation of the
`\delta_{\rm relax}=0.038\pm0.005` band through the weak-form high-resolution
points.

## 8. Recommendation

The original memo was right to be suspicious of the naive `R-K` overlap and the
loose "`\alpha^{-2}` times something" language. The updated conclusion is more
positive:

```text
Thin-ring analytic closure is worth pursuing, but only through the helicity
current-curl bridge. The leading coefficient is pi/4; the relaxed-background
correction is a stable few-percent shift, and the self-adjoint weak-form reduced
boundary prototype now gives target-adjacent matched-box muon branches. The
remaining task is to turn that prototype into a controlled uncertainty estimate.
```

That is a much cheaper and sharper programme than a blind 3D grid search, while
still leaving a clear falsification path if the finite-alpha correction fails.

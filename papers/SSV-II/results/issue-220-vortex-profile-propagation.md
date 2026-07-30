# Issue #220 — corrected Paper II vortex-profile propagation

Status: **focused propagation complete**. No 3D relaxation and no
repository-wide calculation-heavy suite were run.

Parent: [issue #218](https://github.com/StigNorland/SVT/issues/218). The active
Paper I baseline is the coefficient-one conventional-healing-length profile
\[
f_1''+\frac{f_1'}r-\frac{f_1}{r^2}-f_1\ln(f_1^2)=0,
\qquad
f_1(r)=f_2(r/\sqrt2),
\]
where \(f_2\) is the retained coefficient-two legacy control.

## Dependency audit

The preregistered search

```text
rg -n "from (paper_i\.)?vortex_profile import|VortexProfile\.solve" \
  instruments/paper_ii -g '*.py'
```

identified five direct Paper II consumers. Their corrected status is:

| direct consumer | corrected role | verdict |
|---|---|---|
| `lperp_core_integral.py` | coefficient-one curl and bending integrals | values shift; local-bending no-go survives more strongly |
| `lr_su4_cross_term_audit.py` | coefficient-one colour/weak curl overlap | magnitude shifts; nonzero/same-order verdict survives |
| `chiral_cap_equilibrium.py` | corrected line tension in the candidate cubic | input shifts; cubic remains an inversion, not a derivation |
| `lperp_bphys_check.py` | independent corrected solve against an explicitly named legacy control | exact rescaling passes |
| `vortex_cap_mass.py` | corrected shifted LogSE energy and physical tail | line tension shifts; conditional W/Z formula is unchanged |

After propagation, the same search finds one coefficient-two import, only

```text
from vortex_profile import VortexProfile as LegacyVortexProfile
```

in `lperp_bphys_check.py`. It is visibly labelled and used only for the
negative control.

Three transitive, hard-coded consumers were also updated:
`jbend_ring_scaling.py`, `kelvin_wave_renorm.py`, and
`wmass_cap_scale_resolution.py`. `weinberg_angle.py` now uses the corrected
line tension.

## Exact scaling control

Independent integrations at \(r_{\max}=15\xi\), \(n=6000\), give:

| integral | legacy coefficient two | scaling prediction | corrected coefficient one | direct drift |
|---|---:|---:|---:|---:|
| \(I_{\rm curl}\) | 5.019531 | 2.509765 | 2.509778 | +0.0005% |
| \(J_{\rm bend}\) | 7.810304 | 3.905152 | 3.906520 | +0.0350% |
| \(K_{\rm bend}\) | 2.201764 | 2.201764 | 2.203033 | +0.0576% |

The expected powers are
\[
I_1=\frac{I_2}{2},\qquad J_1=\frac{J_2}{2},\qquad K_1=K_2.
\]
The corrected tail is \(1-f_1\sim1/(2r^2)\). Consequently the analytic
\(I,J,K\) tails are four times the legacy-control formulas but remain
numerically negligible at \(15\xi\).

## Corrected line tension

The physical shifted energy is
\[
\epsilon=
\frac12\left(f'^2+\frac{f^2}{r^2}\right)
+\frac12\left(\rho\ln\rho-\rho+1\right),\qquad \rho=f^2.
\]
The old Paper II script instead combined the coefficient-two profile with the
unshifted term \(-\rho\ln\rho\), then assigned logarithmic tails to both the
phase kinetic term and the potential. That is not the corrected action.

With the corrected functional:

| component | value |
|---|---:|
| numerical core, \(r<15\xi\) | 10.1625 |
| phase-gradient tail, \(\pi\ln[(\phi/\alpha)/15]\) | 8.4616 |
| total \(\tau\), regularised at \(R_{\rm cap}=\phi/\alpha\) | **18.6241** |

Only the phase-gradient term is logarithmic; the shifted potential falls as
\(r^{-4}\).

## Downstream numerical effects

| quantity | legacy/current-old | corrected |
|---|---:|---:|
| origin slope | 1.14069 | 0.80659 |
| \(I_{\rm cross}=I_{\rm curl}\) | 5.0195 | 2.5098 |
| \((J+K)/4\) | 2.5027 | 1.5274 |
| local \(\lambda_{\rm bend}\) for \(\lambda_\perp=\alpha^{-2}\) | \(4.70\times10^4\) | \(2.868\times10^4\) |
| local/required gap | 232x | **380.1x** |
| local-equilibrium radius | about \(31\xi\) | \(25.5\xi\) |
| corresponding cap-formula mass | about 1.6 GeV | **1.04 GeV** |
| linear-running candidate / required stiffness | 95.6% | **58.3%** |

The corrected \(J+K\) changes by only 0.38% from \(5\xi\) to \(15\xi\), so
the absence of a useful IR tail survives. Linear running by one power of
\(R_{\rm cap}/\xi\) now remains short by 41.7%; the former 4.4% match was a
legacy-normalisation coincidence.

The analytic cap formula
\[
m_W=\pi(\phi/\alpha)^2m_e=78.925\ {\rm GeV}
\]
does not use the vortex profile and is numerically unchanged. Its status is
also unchanged: \(\phi\) was selected after back-solving the observed mass, so
this is a conditional formula/coincidence, not a W-mass prediction.

## Claim separation

### Surviving

- The exact coordinate-rescaling law and its integral powers.
- Local vortex-core bending cannot supply the candidate
  \(\alpha^{-3}\) stiffness; the negative result strengthens from 232x to
  380x.
- The core integrals saturate within a few healing lengths.
- For coincident colour and weak cores, the chirality cross term is positive,
  nonzero, and equal to the diagonal curl integral. Its magnitude halves, but
  its same-order and selection-rule verdicts survive.
- The arithmetic W/Z values survive only as conditional consequences of an
  imposed cap radius and an imported electroweak mixing angle.

### Invalidated

- All active uses of the coefficient-two values
  \(I_{\rm curl}=5.02\), \(J=7.81\), and \((J+K)/4=2.50\).
- The factor-232 current shortfall; it is 380.1 for the corrected profile.
- The claim that linear running \(\lambda_\perp(R)\propto R\) lands within
  4.4% of \(\phi^3/\alpha^3\); it is 41.7% short.
- The old \(\tau=17.0\) derivation from an unshifted energy and doubled
  logarithmic tail.
- Any reading of the cubic
  \(R^3+\tau R^2=\lambda_{\rm bend}\) as deriving
  \(R_{\rm cap}=\phi/\alpha\). It only maps an imposed radius to the required
  stiffness.

### Genuinely open

- A cap-setting mechanism derived from the corrected nonlinear dynamics,
  without inserting \(R_{\rm cap}\), \(\lambda_{\rm bend}\), or \(m_W\).
- The full 3D reconnection geometry and its cap coefficient.
- The sign of the colour/weak cross coupling, coincidence of the two cores,
  and survival of chirality locking under nonlinear 3D relaxation.
- A derivation of the Weinberg angle rather than import from Standard Model
  input.

## Focused validation

The issue adds guards for the active/control coefficient distinction, exact
integral scaling, shifted line-tension energy, single logarithmic tail, and the
absence of unlabelled legacy imports. Existing chirality and W-cap tests were
updated to the corrected baseline. The Paper II gated build is the final
integration check.


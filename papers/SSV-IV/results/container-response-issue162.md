# Issue #162 [MODEL 1/2] — Superfluid in an imposed container

**Status: R-consistency PASS · R-prediction clean NEGATIVE.**
Modelling the post-#161 assumption directly: an SSV (logarithmic-GPE) superfluid
placed inside an *externally imposed* container geometry — a prescribed loading
`g00(x)` and a transverse-traceless shear `h_ij(t)`. Two pre-registered
questions. **(1)** The effect/cause dictionary holds: the local phase-advance
rate equals `-mu_local/hbar` to ~10⁻⁷ for all three media — "time dilation =
phase-update rate" is self-consistent, an external cause is faithfully realised
as a physical internal effect. **(2)** With the sound speed matched, the SSV
medium's response to the imposed tensor shear is **indistinguishable** from an
ordinary Gross–Pitaevskii fluid (relative difference 1.8×10⁻⁵): at linear
amplitude about a uniform background the log/saturated structure is invisible in
the gravity sector. **SSV adds nothing a generic fluid would not — superfluous
here, exactly the pre-registered null (rule 1).**

Pre-registered on issue
[#162](https://github.com/StigNorland/SVT/issues/162) before the computation.
Script `instruments/model_container/superfluid_in_imposed_container.py`; tests
`instruments/test/model_container/test_superfluid_in_imposed_container.py`
(6: positive control, norm conservation, matched dispersion, effect/cause
consistency, the shear-response null, verdict rules); receipt
`container_response_receipt.json`.

## What was assumed vs tested

**Assumed (imported, by construction).** The container supplies gravity: `g00(x)`
and `h_ij(t)` are prescribed external inputs. `G` and the shear are *not* derived
— importing them is the assumption being modelled. (A result that "derived" them
would be a circularity bug, not a finding.)

**Tested.** (1) Does the medium realise an imposed cause as the ontology claims —
`d/dt arg psi = -mu_local`? (2) Does the superfluid's response to the imposed TT
shear differ measurably from a generic medium's?

## Method

Symmetric split-step Fourier (Strang) evolution of the field, units
`hbar = m = rho0 = 1`. Three media: **linear** (free Schrödinger, null
comparator), **cubic** (ordinary GPE, `mu_nl = g rho`, null comparator), **log**
(SSV LogSE, `mu_nl = b ln(rho/rho0)`). Bogoliubov dispersion
`omega(k) = sqrt(c_s² k² + (k²/2)²)` with `c_s² = rho dmu_nl/drho|_rho0`: cubic
→ `g rho0`, log → `b` (density-**independent** — the signature log feature).
Setting `b = g rho0` (here `c_s² = 1`) gives cubic and log the **same
dispersion**, the sharpest form of the null.

- The imposed TT shear enters as a time-dependent kinetic anisotropy,
  `K(k,t) = ½[(1−h)kx² + (1+h)ky²]`. A long-wavelength TT drive does no work on a
  homogeneous condensate (`K(0)=0`); it parametrically pumps finite-`k` phonon
  pairs, resonant at `Omega = 2 omega(k)` — the analogue of GW phonon production.
- The imposed `g00` is a smooth external potential `Vext(x)`; the differential
  phase-rate between two points is the analogue gravitational redshift.

## Results (matched `c_s² = 1`, `g = b = 1`)

**Positive control** — undriven phonon vs Bogoliubov (`k = 2·dk`, `omega = 0.6586`):

| medium | ω measured | ω Bogoliubov | rel. err |
|---|---|---|---|
| cubic | 0.6586 | 0.6586 | 0.00% |
| log   | 0.6586 | 0.6586 | 0.00% |

The solver reproduces the analytic dispersion — instrument validated before its
verdict is trusted.

**(1) Effect/cause dictionary** — local phase-rate vs `−mu_local`:

| medium | relative error |
|---|---|
| linear | 2.0×10⁻⁸ |
| cubic  | 2.9×10⁻⁸ |
| log    | 1.0×10⁻⁷ |

→ **R-consistency: PASS** (< 10⁻³). The Josephson / time-dilation-as-phase-rate
relation is numerically exact: the imposed loading (cause) is realised as the
local clock rate (physical effect). This is the capstone assumption of the #161
closure, made numerical.

**(2) Shear response** — parametric growth at `Omega = 2 omega(k)`:

| medium | growth factor | ω(k) |
|---|---|---|
| linear | 1.0000 | 0.1974 |
| cubic  | 1.9850 | 0.6586 |
| log    | 1.9851 | 0.6586 |

- diff(log vs cubic, `c_s` matched) = **1.8×10⁻⁵**
- diff(log vs linear) = 9.9×10⁻¹

→ **R-prediction: clean NEGATIVE.** The log (SSV) medium's shear response equals
the ordinary GPE's to five significant figures. The free field does not respond
at all — it has no sound mode, so nothing to pump; that large difference merely
confirms the drive is doing fluid physics, not that SSV is special.

## Verdict and decision rules

- **R-consistency (PASS):** phase-rate = `−mu_local` to < 10⁻³ — met at ~10⁻⁷.
- **R-prediction (clean NEGATIVE):** `diff(log vs cubic) < 10⁻²` — met at
  1.8×10⁻⁵. The SSV medium is indistinguishable from a generic Bogoliubov fluid
  of the same sound speed; it contributes no distinctive gravity-sector signature
  at linear amplitude.

## Honesty items and contingency (rule 1)

- **Why the null is real, not rigged.** At linear amplitude about a *uniform*
  background, only `c_s(rho0)` enters the response; any two media sharing
  `c_s(rho0)` respond identically. The log medium's distinctive property — `c_s`
  *independent of density* — cannot manifest when the density does not vary. The
  null is a correct statement about linear response, not an artifact of parameter
  matching.
- **Where a signature could still hide (the surviving-version requirement).** The
  log/saturated structure differs from the cubic GPE only at (a) **nonlinear
  amplitude** (large `h0`, where saturation vs `|psi|²` diverge) or (b) a
  **density-varying background** (where `c_s(rho)` constancy becomes observable).
  Either is a sharp, pre-registerable follow-up to #162. Absent such a test, the
  honest statement is: **at the level computed, SSV's superfluid responds to an
  external tensor wave exactly as ordinary matter does.**
- This models the *assumed* layering; it does **not** and **cannot** derive `G`
  or the shear (imported by construction). A null here is the expected, fully
  acceptable outcome — it sharpens the #161 conclusion that gravity belongs to
  the container, not the superfluid.

## Net

The two halves of the #161 capstone survive their first numerical test in
opposite ways, both honest: the **effect/cause dictionary is confirmed** (the
ontology faithfully turns an external cause into a real internal effect), and the
**superfluid's gravity-sector response is generic** (matched to an ordinary
fluid, so SSV is superfluous as a source). Together they are exactly the layered
picture #161 reached — *effects physical and internal, causes external* — now
with a tested computation behind it rather than an assertion. The one place SSV
could still say something distinctive about gravity is the nonlinear / density-
varying regime; that is the natural next pre-registration.

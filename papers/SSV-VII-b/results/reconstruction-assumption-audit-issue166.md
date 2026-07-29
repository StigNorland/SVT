# Issue #166 sub-calculation 5 — reconstruction-dependency and theorem-assumption audit

**Status: clean negative on the existing reconstruction claim (D1 + D2).**
Sub-calculation 4 does not compute a bulk response from the measured screen
polarisation. It computes the known Green function of an independently supplied
massless lattice Laplacian. In addition, the committed calculations do not
satisfy the load-bearing premises of the cited holographic-entanglement result
in one common model. The statement that the bulk TT mode “follows from the
screen state” is therefore unsupported and is retracted.

This does **not** falsify a possible bulk–screen correspondence, nor does it
undo the stable-sign scalar correction from issue #183. It returns issue #166
to **open / unproven**.

Pre-registration:
[issue comment](https://github.com/StigNorland/SVT/issues/166#issuecomment-5123996215).
Instrument:
`instruments/model_screen/reconstruction_audit.py`.
Tests:
`instruments/test/model_screen/test_reconstruction_audit.py`.
Receipt:
`reconstruction_audit_receipt.json`.

## Question A — does the claimed propagation depend on screen data?

The measured screen polarisation enters sub-calculation 4 only through
`determinacy_min_abs_Pi2()`, which reduces it to the scalar
`min(abs(Pi2))`. The claimed propagation calculation instead executes

```python
k2 = khat2(L)
G_massless = greens_function(L, k2)
```

The two kernels actually passed to `greens_function()` by `run()` are:

```text
k2
M * M + k2
```

Neither contains the measured `Pi2`.

### Blind-null control

The audit first runs a genuinely data-dependent inversion:

| supplied kernel | recovered behavior |
|---|---|
| `Pi(k) = khat²` | `G(r) ~ 1/r^2.089` |
| `Pi(k) = 0.6² + khat²` | Yukawa rate `0.589` |

The harness therefore detects a changed kernel when the kernel is actually
used. Against the audited code path, changing the screen fixture leaves the
reported T2 power exactly unchanged because neither fixture reaches T2.

**D1 fires.** The `1/r²` result verifies Fourier-transform machinery for a
massless kernel. It does not show that the SSV screen generated that kernel.

## Question B — can the cited theorem supply the missing step?

Faulkner, Guica, Hartman, Myers and Van Raamsdonk derive linearised bulk
equations for small perturbations of a **holographic CFT vacuum**, using the
entanglement first law for **all ball-shaped boundary regions** together with a
holographic entropy functional and the boundary-stress/asymptotic-metric
dictionary. Their result does not turn an arbitrary conserved stress correlator
and an assumed propagator into a bulk dual:
[arXiv:1312.7856](https://arxiv.org/abs/1312.7856), especially the abstract,
§§2.2–2.3 and §4.3.

The audit searched the four scripts and four result notes making up
sub-calculations 1–4 (eight files total). The exact patterns and counts are in
the receipt.

| required artifact | result |
|---|---|
| one common state space and physical screen dimension | **missing** — sub-calc 1 is a 1D open chain; sub-calcs 2–4 use `D=4` Euclidean arrays; no map joins them |
| modular first law for all balls and Lorentz frames | **missing** |
| RT/Wald or another derived screen-entropy → bulk-surface functional | **missing** |
| screen stress → asymptotic bulk metric dictionary | **missing** |
| explicit bulk–screen state/encoding map | **missing** |
| bulk kinetic kernel derived from screen data | **missing** — `khat²` is inserted |

**D2 fires.** The theorem is not applicable to the artifacts currently
committed under #166.

## Independent warning on sub-calculation 1

Sub-calculation 1 measured only the far-separated weight of `H_pi` for a block
adjacent to a Dirichlet wall. A small far tail is not equivalent to a geometric
modular Hamiltonian: non-local structure can live in other kernel components
and along loci not selected by that statistic.

This is no longer only a hypothetical concern. A direct numerical analysis of
the massive scalar on the half-line finds the modular Hamiltonian of an
adjacent interval non-local at finite mass, becoming local only in limiting
cases:
[Minz and Tonni, arXiv:2512.04659](https://arxiv.org/abs/2512.04659), abstract
and §§3–5. Arias, Blanco, Casini and Huerta also distinguish universal local
terms from the complete modular Hamiltonian and show that higher-dimensional
local terms are not exhausted by the stress tensor:
[arXiv:1611.08517](https://arxiv.org/abs/1611.08517).

Therefore the old observation “the selected `H_pi` far tail shrinks” remains a
valid numerical observation, but its interpretation “modular flow stays
geometric” does not follow.

## Revised status of sub-calculations 1–4

| sub-calculation | result that survives | interpretation that does not survive |
|---|---|---|
| 1. modular locality | one far-tail statistic shrinks with mass in a 1D wall-adjacent block | geometric modular flow for the required regions |
| 2. screen stress | a generic free scalar has a conserved nonzero spin-2 stress correlator | an SSV-derived horizon algebra with propagating bulk TT modes |
| 3. induced polarisation | the chosen lattice correlator has an analytic mass-dependent `k²` fit | absolute or screen-derived Einstein dynamics; the seagull and physical map remain absent |
| 4. reconstruction | `1/k²` Fourier transforms to a long-range Green function | the screen produced `1/k²`, or bulk TT follows from its state |

These are useful controls and pieces of model-building intuition. They are not
one bulk–screen reconstruction.

## Decision

- **D1: PASS (negative)** — the propagation claim is screen-data-independent.
- **D2: PASS (negative)** — theorem premises are absent.
- **D3: FAIL** — the “R1 assembled” verdict does not survive.

The correct status is:

> The corrected SSV scalar may be compatible with pursuing a screen
> construction, but no explicit screen algebra, holographic entropy map, or
> derived bulk TT kernel has yet been demonstrated.

## Next admissible probe

Do not spend effort on the absolute seagull-complete `G` yet: without a
screen-to-bulk map, that would calculate an induced-gravity coefficient in
another supplied background.

The cheapest relevant next calculation is a **single-model 2+1-dimensional
finite-disk modular test**:

1. derive the Gaussian screen state from one corrected SSV quadratic theory;
2. compute the complete disk modular kernels, not one far-tail statistic;
3. test the conformal disk weight as a positive control;
4. test finite `R/xi` for non-local residuals;
5. evaluate the first law for a basis of disk perturbations;
6. insert no gravitational kernel.

A robust failure of geometricity for finite disks would be evidence toward R3
for the standard Faulkner-et-al. route. A pass would only license the next
missing object: an entropy/encoding map.

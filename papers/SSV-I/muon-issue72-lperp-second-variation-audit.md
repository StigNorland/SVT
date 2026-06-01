# Muon issue #72 L_perp second-variation audit

**Date:** 2026-06-02. Follow-up audit for
[issue #72](https://github.com/StigNorland/SVT/issues/72), after
`muon-issue72-drift-diagnostic-result.md`.

This note asks whether the Diagnostic V1 drift can be blamed on an omitted
bulk term in the implemented current-curl BdG block. It does not attempt a new
muon prediction.

## Verdict

Within the reduced energy-bilinear model, the implemented
`current_curl_model = "full"` contains the expected algebraic second variation
of

```math
E_\perp[\psi] = {\lambda\over 2}\int |\nabla\times j[\psi]|^2\,d^3x,
\qquad
j = {1\over 2i}(\psi^*\nabla\psi-\psi\nabla\psi^*).
```

The Diagnostic V1 failure is therefore unlikely to be fixed by simply adding a
missing local bulk term to the current-curl block. The remaining unresolved
items are boundary/window interpretation and reduced-basis adequacy. The next
numerical step should be a minimal phi-discretized toroidal BdG check, not
further tuning of the current reduced Kelvin basis.

## Expansion being audited

Write a perturbation as

```math
\psi = \psi_0 + \epsilon\,\eta,
```

with Nambu components `u` and `v` treated independently in the BdG projection.
Then the current expands as

```math
j = j_0 + \epsilon j_1 + \epsilon^2 j_2 + O(\epsilon^3),
```

so

```math
|\nabla\times j|^2 =
|\omega_0|^2
+ 2\epsilon\,\omega_0\cdot\omega_1
+ \epsilon^2\left(|\omega_1|^2 + 2\omega_0\cdot\omega_2\right)
+ O(\epsilon^3),
```

where `omega_k = curl(j_k)`. Since `E_perp` has the prefactor `lambda/2`,
the quadratic form is proportional to

```math
{1\over2}\int |\omega_1|^2\,d^3x
+ \int \omega_0\cdot\omega_2\,d^3x.
```

In matrix language, the first term is the `linear` current-curl model and the
second term is the extra background-current term in the `full` model.

## Code map

The relevant implementation is in `src/paper_i/kelvin_augmented_bdg.py`.

| mathematical object | implementation | status |
|---|---|---|
| `j_1[u]`, `j_1[v]` | `current_variation_component_m(..., component="u"/"v")` | present |
| `omega_1 = curl(j_1)` | `curl_current_component_m` | present |
| `int omega_1^* . omega_1` normal/anomalous blocks | `current_curl_component_overlap` | present |
| Hermitian `L` block from `u/u` | symmetrized in `hermitian_current_curl_bdg_blocks` | present |
| complex-symmetric `M` block from `u/v` | symmetrized in `hermitian_current_curl_bdg_blocks` | present |
| `j_0` and `omega_0` | `background_current_component`, `curl_background_current` | present |
| `j_2` normal/anomalous bilinear current | `second_current_component_m` | present |
| `omega_2 = curl(j_2)` | `curl_second_current_component_m` | present |
| `int omega_0 . omega_2` | `background_second_current_curl_overlap` | present in `current_curl_model="full"` |

The azimuthal selection rules are also implemented in the right block-specific
form:

- normal `L` block: `m_a = m_b`
- anomalous `M` block: `m_a + m_b = 0`

This is the correction that Stage 1 established. It removes the old spurious
cross-`m` bridge between the `m=0` core sector and the `m=+/-1` Kelvin sector.

## Coefficient convention

There is no obvious missing factor of two in the code's own convention.
`hermitian_current_curl_bdg_blocks` constructs matrix elements for the BdG
Hamiltonian block, not a standalone scalar energy report. The `linear` piece
uses symmetrized overlaps of `omega_1`, and the `full` piece adds the
symmetrized `omega_0 . omega_2` contribution. Diagnostic V1 confirmed that the
`full` contribution is numerically material, especially on the upper Kelvin
branch, but it did not remove radial-window drift.

This audit therefore does not identify a simple algebraic coefficient patch
that would turn the reduced result into a muon prediction.

## Boundary and window caveat

The reduced calculation should be read as a weighted Galerkin projection of the
quadratic energy, not as a solved boundary-value problem for a physical
self-adjoint operator on a finite toroidal domain.

That distinction matters:

- The current-curl block integrates local bilinear densities multiplied by the
  projection weight `W(r,z)`.
- If one derives a strong differential operator from a windowed functional
  `int W |curl j|^2`, integrations by parts generate terms involving
  derivatives of `W` and boundary fluxes.
- The reduced projection avoids explicitly forming that strong operator, but
  the resulting numbers still depend on the chosen projection tube and basis.
- The `hard` window is now useful as a diagnostic cutoff, but it is not a
  physical boundary condition; at positive radius it introduces a discontinuous
  projection surface.

This is consistent with Diagnostic V1: hard and smooth windows agree on the
lower-branch drift, so the old smooth-taper caveat is not the culprit, but the
windowed reduced basis remains a diagnostic device rather than a closure-grade
operator.

## What this rules out

The following rescue is no longer attractive:

```text
The muon branch failed only because the reduced current-curl block omitted the
background-current part of the L_perp second variation.
```

That term is implemented and was tested. It shifts branches, but it does not
produce a stable plateau near `omega/omega_c = 0.207`.

## What remains open

Three possibilities remain:

1. A more formal weak-form treatment of the entire reduced BdG operator could
   improve boundary behaviour. Historical notes contain target-adjacent weak
   form checks, but those checks are now superseded by the Path B null and have
   not been re-established under the issue #72 selection-rule / branch-tracking
   discipline.
2. A derived, non-window boundary condition might exist for the reduced
   toroidal projection. This would still require a new derivation, not a tuning
   pass.
3. The reduced Kelvin basis may be intrinsically inadequate. The clean way to
   test this is a minimal phi-discretized toroidal BdG solver that removes
   Kelvin seed-family ambiguity and treats the `m=+/-1` sector directly.

## Decision for issue #72

The minimal phi-discretized toroidal BdG check is warranted. It should be
tracked as a follow-up issue with a narrow first deliverable:

- fixed toroidal background, not relaxed 3D dynamics;
- `m=+/-1` Fourier sector only;
- same `L + L_perp` ingredients as the reduced operator;
- compare against the issue #72 reduced-basis spectra at matched windows and
  resolution;
- decide whether a stable Kelvin branch exists independently of the chosen
  Kelvin seed family.

The present reduced basis should not be tuned further as a route to a muon
claim until that direct sector check exists.

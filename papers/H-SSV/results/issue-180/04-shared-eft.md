# Issue #180 — shared EFT and transverse-mode control

Status: **literal branch not reached; adjacent control completed**

Gates:

- **P4 S route FAIL**
- **P4 H route is an adjacent K2 control, not a repair**
- **P5 NOT REACHED for literal SSV**

## The transverse-wave question

A complex scalar with broken global \(U(1)\) supplies one Goldstone scalar.
Under spatial rotations it is a spin-0 degree of freedom. A Maxwell field
supplies two helicity states, \(+1\) and \(-1\), after gauge constraints.

No manipulation of the scalar dispersion turns one spin-0 representation into
the two transverse photon representations. The existing SSV chiral-shear term
does not change this count: the repository's issue-#138 linearization found
that it is silent in the uniform-vacuum linear spectrum.

Therefore:

- **S route:** “the scalar Goldstone is the physical photon” fails;
- **H route:** an independent gauge field can carry transverse radiation, but
  this withdraws the old identity rather than deriving the photon from SSV.

## Independent-sector compatibility control

For orientation, consider the ordinary covariant direct-sum action

\[
S=\int d^4x\sqrt{-g}
\left[
\frac{M_{\rm Pl}^2}{2}R
-|D\Phi|^2-V(\Phi)
-\frac14F^2
+i\bar\psi\gamma^\mu D_\mu\psi
+\cdots
\right].
\]

With a stable scalar potential, Einstein–Hilbert supplies two massless
spin-2 helicities, Maxwell supplies two massless spin-1 helicities, and an
anomaly-free chiral representation can be supplied independently. This is an
ordinary EFT compatibility witness, not an emergence result.

The code checks one left-handed Standard Model generation:

| Anomaly | Sum |
|---|---:|
| \(U(1)_Y^3\) | 0 |
| gravity\(^2 U(1)_Y\) | 0 |
| \(SU(2)^2U(1)_Y\) | 0 |
| \(SU(3)^2U(1)_Y\) | 0 |
| \(SU(3)^3\) | 0 |
| number of \(SU(2)\) doublets | 4 (even) |

The last line passes the global SU(2) condition identified by
[Witten (1982)](https://doi.org/10.1016/0370-2693(82)90728-6).

## Why this does not save the frozen target

For a block-diagonal quadratic action, the spectrum is the union of the
sector spectra. Adding positive Maxwell, fermion, and graviton blocks does not
remove the negative scalar eigenvalue. Interactions weak enough to preserve
the SSV limit cannot reverse that eigenvalue at arbitrarily small \(k\);
interactions large enough to reverse it modify the defining quadratic limit.

Thus:

- the independent sectors demonstrate that gravity, gauge fields, and chiral
  matter are not mutually contradictory in ordinary EFT;
- they do **not** establish a stable EFT whose condensate limit is the frozen
  SSV equation;
- using the sign-reversed scalar control plus independent sectors is a nearby
  K2 candidate, but it lies outside G1/G6 and still has a subluminal Goldstone
  rather than the claimed photon cone.

## Universal gravity

If Einstein–Hilbert gravity is inserted, diffeomorphism invariance couples it
to the total covariant stress tensor. The soft-graviton result of
[Weinberg (1964)](https://doi.org/10.1103/PhysRev.135.B1049) explains why a
consistent massless spin-2 particle has universal low-energy coupling.
Inserting that structure verifies compatibility only; it does not derive
gravity from the screen or SSV.

## Gate decision

P5 is marked **not reached** for literal SSV because P0/P1/P3 already fail.
The independent-sector calculation is retained as the requested control and
as a precise description of what a modified K2 programme would have to admit.

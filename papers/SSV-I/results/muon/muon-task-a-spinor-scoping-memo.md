# Task A (scoping): spinorial order parameter — minimal structure and cost

**Issue:** [#78](https://github.com/StigNorland/SVT/issues/78) Task A — scoping
memo only. **Do not implement without an explicit decision.** Reached because
Routes C and D both came back negative and Task B reduces to this.

## What buys a half-integer Berry phase

The muon no-go (`muon-bdg-nogo-summary.md`) is a statement about the
order-parameter manifold: a single scalar Ψ has manifold `U(1)`, with
`π₁(U(1)) = ℤ` — integer winding, **no ℤ₂**, hence no half-integer holonomy.

The minimal change that restores a half-integer Berry phase is to promote Ψ to a
**two-component spinor**:
```
Ψ = (Ψ↑, Ψ↓),    normalised direction n̂ ∈ CP¹ ≅ S²,
```
i.e. a `CP¹` (equivalently `SU(2)/U(1)`) order parameter on top of the overall
phase/amplitude. The relevant homotopy changes to:

- `π₁(SO(3)) = ℤ₂` → admits the **π Berry phase** (and half-quantum vortices, Task B);
- `π₂(S²) = ℤ` → skyrmion charge, a second topological index;
- `π₃(S²) = ℤ` (Hopf) → links to the trefoil/Hopfion baryon sector.

This is exactly Volovik's *fermionic* Fermi-point Berry phase recovered
wholesale — the mechanism that produces CdGM equal-spacing and the half-integer
vortex-core ladder. With it, the muon's `(3/2)` half-integer rung has a home and
the lepton acquires an intrinsic spin-½ label for free.

## Minimal structure, stated precisely

1. One extra complex component (Ψ becomes a 2-spinor), with an internal `SU(2)`
   acting on it; the physical configuration is the overall `U(1)` phase × the
   `CP¹` direction `n̂`.
2. A term in the action that gives `n̂` a finite stiffness and a preferred
   ground-state direction (so the vacuum is a definite `n̂₀`, broken to `U(1)`),
   plus whatever locks the spinor texture to the existing chiral-shear sector.
3. Nothing else: amplitude/phase dynamics (LogSE) carry over; the chiral-shear
   `L_perp` would be rewritten as an `SU(2)`-covariant gradient term.

## Cost to Papers I–II (why this is not free)

- **Breaks the foundational "one scalar field Ψ" commitment.** Papers I and II
  open by deriving everything from a single scalar LogSE; a spinor Ψ is a
  different theory, not a refinement.
- **Re-derivations required:** `α = c_⊥/c` from `λ = α²ρ₀/m₀`; the electron
  equilibrium `R_e = ξ/α`; the Madelung/sound-speed structure; the pion
  `= 2μ₀` integer-winding result — all were derived for scalar Ψ and would need
  to be re-established (or shown invariant) under the `SU(2)` extension.
- **New free inputs:** the `n̂` stiffness and anisotropy constants are new
  parameters unless fixed by a further principle; uncontrolled, they trade the
  muon coincidence for added freedom.
- **Risk:** a 2-component order parameter generically introduces *additional*
  light modes (the `n̂` Goldstones) that must not spoil the photon/electron
  sectors already matched in Paper II.

## What it would resolve, in one line

It converts the muon from a *numerical coincidence* (current status) into a
*distinct topological sector* (half-winding / half-integer Berry phase), and
unifies the lepton spin-½ and the baryon HQV-pair mapping — at the price of
replacing the scalar foundation of Papers I–II.

## Recommendation

Hold. This is the single highest-leverage structural change available, and also
the most expensive. It should be taken only as a deliberate foundational
decision — e.g. when the spin-½ of leptons (currently not derived) is promoted
from "assumed" to "must be explained," at which point the `CP¹` extension pays
for itself on two fronts at once (spin **and** the muon rung). Until then, the
muon stays a recorded coincidence (Paper I §4) and this memo is the standing
scope of the escape hatch.

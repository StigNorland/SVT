# Volovik mapping: SSV analogies and divergences

Reference: G.E. Volovik, *The Universe in a Helium Droplet*, OUP 2003.

Volovik builds a condensed-matter analogy between ³He superfluids and
fundamental physics using topological-defect ontology. His framework is the
closest thing in the literature to SSV's programme.

---

## Clean analogies

### 1. Lepton ring = vorton (§14.3.4)

> "If the vortex line with the twisted core is closed, one obtains the analog
> of the string loop with the quantized supercurrent along the loop… Such a
> closed cosmic string… is called a vorton."

The vorton is stabilized by conservation of winding number — exactly the
topological protection used for SSV toroidal-ring leptons. Carries quantized
circulation and a mass/inertia from the core flow (Kopnin/hydrodynamic mass
analog). §14.1.2 adds: the mass vortex carries ∮ v·dr = n κ (κ = h/m), which
maps directly to the SSV lepton winding number.

**Verbatim precedent:** "closed vortex ring with quantized circulation,
stabilized by winding number." This is the electron in SSV language.

### 2. Baryon composite = double-core vortex / soliton-terminated string (§14.3.3, §14.1.5)

> "The spin vortex as the termination line of soliton in ³He-B… soliton is
> stable… non-triviality of π₁_relative(SO(3); S²) = Z."

> "Can be considered as a pair of half-quantum vortices, connected by a
> non-topological soliton wall."

The double-core vortex (two half-quantum vortices joined by a soliton wall)
is a composite, breathing-capable 3D defect. This is the structural analog
of the SSV trefoil breather baryon: topologically protected skeleton,
internal degrees of freedom from the connecting soliton, composite rather
than elementary.

§11.1.1 / §16.2.1 (Skyrmion as baryon): π₃ textures (non-singular, 3D
solitons) carry baryon number and are stable against continuous deformation.
SSV extends this by specifying the trefoil linking geometry explicitly.

**Verbatim precedent:** "pair of half-quantum vortices connected by soliton
wall" for baryon-like composites; "π₃ skyrmion" for non-singular baryons.

### 3. Fermi surface / momentum-space vortex (§8.1.1, §8.1.7)

> "The Fermi surface is topologically equivalent to a quantized vortex in
> 3+1 spacetime… In 2+1 dimensions the Fermi hypersurface is a line in 2D
> momentum space, which corresponds to the vortex loop in 3D
> frequency-momentum space."

Momentum-space topology provides an independent route to chirality and
protected modes. Relevant context for SSV chiral-shear sector.

---

## Where SSV diverges — and why it matters

Volovik's sub-gap (CdGM) spectrum and non-trivial Berry phase exist because
**³He is a fermionic superfluid** with BdG quasiparticles traversing a Fermi
surface. The geometric (azimuthal holonomy) Berry phase is non-trivial
precisely because the quasiparticle encircles a Fermi-point singularity.

SSV uses a **scalar** (bosonic) order parameter — no Fermi surface, no BdG
pairing. Consequently:

1. **Issue #76 (Berry-phase audit):** γ_B = 0 for pure scalar LogSE. The
   selection rules (m_a = m_b for L⊥ block; m_a + m_b = 0 for M⊥ block)
   forbid the bridge matrix element that would produce half-integer rungs.
   Volovik's result does not transfer to scalar SSV.

2. **Muon null results:** All three routes (Path B, #73, #76) return null.
   This is consistent: Volovik's sub-gap rung structure is a *fermionic*
   mechanism. SSV's scalar vacuum cannot generate it by construction.
   The muon mass gap requires either a spinorial order parameter or a
   derived half-winding Nambu mechanism — neither is present in current
   scalar SSV.

**The geometric/topological analogies (vorton, skyrmion, soliton composite)
carry over cleanly. The spectral mechanism does not.**

---

## Lepton generation ladder: the closed-shell hypothesis

### Numerical finding (2026-06-02)

Inverting the Lamb vortex-ring self-energy formula

```
E(R) = π R [ln(8R/ξ) − C]     (C ≈ 2, thin-ring approximation)
```

with known lepton masses as input gives (see `src/paper_i/vortex_ring_mass_inversion.py`):

| generation | R/ξ (best-fit) | R/ξ (8^n rule) | mass error (8^n) |
|---|---:|---:|---:|
| e (n=0) | 1.01 | 1 | — |
| μ (n=1) | 8.59 | 8 | +5% |
| τ (n=2) | 73.7 | 64 | −2% |

The best-fit geometric series has R_e ≈ 1ξ and generation ratio q ≈ 8.59.
The simple rule R_n = 8^n ξ reproduces the lepton mass spectrum to within 5%.

### The atomic-shell analogy

In atomic physics the electron shell structure has magic numbers **2, 8, 18, 32, ...** = 2n².
The second shell closes at **8** because there are 4 spatial modes (1 s + 3 p) × 2 spin states.
Each closed shell is a stable, inert configuration; the next electron must start a new shell.

The direct SSV analog:

| atomic concept | SSV vortex ring analog |
|---|---|
| Principal quantum number n | Generation index (e=0, μ=1, τ=2) |
| Shell radius R_n = n² a₀ | Ring radius R_n ≈ 8^n ξ |
| Magic number 8 (2nd shell) | Generation ratio q ≈ 8 |
| Closed shell = stable noble gas | Stable lepton = closed mode shell on ring |
| Orbital degeneracy 2(2l+1) | Kelvin-mode degeneracy of the torus |

The key question is: **what mode structure of a toroidal vortex ring has degeneracy 8?**

### Kelvin modes on a thin ring and the torus symmetry

A thin vortex ring supports Kelvin-wave oscillations labelled by two integers:
- m_φ = azimuthal mode (around the big ring axis, period 2πR)
- m_θ = poloidal mode (around the core cross-section, period 2πa, a ≈ ξ)

The symmetry group of the torus is U(1) × U(1), with irreps labelled by (m_φ, m_θ) ∈ Z².

For the ring to be "stable" in the sense of carrying no net Kelvin-wave excitation,
all modes up to some maximum must be occupied (as in a Fermi sea) or equivalently
the ring must sit at a local minimum of the mode-energy landscape with the lowest
complete multiplet fully filled.

The first complete multiplet with total mode number |m_φ| + |m_θ| ≤ 1:
- (0, 0): 1 state
- (±1, 0): 2 states
- (0, ±1): 2 states
- Total: **5 states**

With two chirality orientations (left- and right-handed circulation around the core):
- 5 × 2 = **10 states** — close but not 8.

Alternative counting using |m_φ|² + |m_θ|² ≤ 1 (L² ≤ 1 on the torus):
- Same 5 modes × 2 chiralities = 10. Still not 8.

The exactly-8 counting that matches atomic physics (1s + 3p = 4 orbitals × 2 spin):
- The ring has one "s-like" breathing mode (m_φ = 0, m_θ = 0) → 1 state × 2 = 2
- Three "p-like" dipole modes (m_φ = ±1, 0; or the three rigid-body translations) → 3 × 2 = 6
- Total: **2 + 6 = 8**

This matches the atomic second shell exactly if the relevant "spin-like" quantum number
for the vortex ring is the core chirality (the two orientations of the helical twist).

### Physical interpretation

If this is correct, the lepton generations are the **closed-shell radii** of the toroidal
vortex ring: the discrete values of R/ξ at which all Kelvin modes up to a given angular
order are simultaneously in their ground state. The generation step q = 8 = (1s + 3p) × 2
is the same closed-shell degeneracy as the second period of the periodic table.

The tau lepton is the third generation (R = 64ξ) because the third "shell"
(1s + 3p + 5d modes × 2 = 18 states — but only up to the first two contribute to
the ring's stable radius) closes at that scale.

**The 8 in q is the same 8 in ln(8R/ξ):** the Lamb formula's geometric factor 8 = 2³
arises from the same vortex-core geometry that determines the mode degeneracy.
Both the energy formula and the generation step carry the same number because they
are both encoding the same underlying torus mode structure.

### REFUTED (2026-06-05, issue #78 Task D)

Both predicted tests were run and **both came back negative** — see
`papers/SSV-I/results/muon/route-d-kelvin-degeneracy-result.md`. The closed-shell hypothesis
above does **not** hold:

1. **C does not collapse q to 8.** With the real LogSE core constant
   `C_LogSE = 1.880` (`vortex_ring_core_constant.py`), the best-fit generation
   ratio is still `q = 8.587` — it is fixed by the lepton mass ratios alone and
   is *independent of C* (C only sets the absolute R_e). The 7.3% gap from 8 does
   not close.

2. **The ring has no magic number 8.** The straight-vortex Bogoliubov spectrum
   (`vortex_core_mode_spectrum.py`) has U(1)_azimuthal symmetry: modes are `±m`
   doublets, tower `(1,2,2,2,…)`, cumulative `(1,3,5,7,…)` — the odd numbers,
   never 8. The atomic magic 8 = (1s+3p)×2 is an **SO(3)** degeneracy (3-fold
   p-orbitals); a vortex ring has no SO(3), so the "(1s+3p)" counting above is
   geometrically invalid. Even a ×2 chirality factor gives `(2,6,10,…)`, not 8.

**Conclusion:** the `8ⁿ` ladder is a ~5–7% numerical curiosity, not a
first-principles Kelvin-mode degeneracy law. The atomic-shell analogy is
**retired**. Lepton generations, if derivable at all, are not closed mode-shells
of the singly-wound ring.

---

## Summary table

| SSV object | Volovik analog | Section | Clean? |
|---|---|---|---|
| Toroidal lepton ring | Vorton (closed twisted vortex) | §14.3.4, §14.1.2 | Yes |
| Trefoil breather baryon | Double-core vortex / soliton-wall composite | §14.3.3, §14.1.5 | Yes (geometry) |
| Baryon as skyrmion | π₃ Skyrme soliton | §11.1.1, §16.2.1 | Yes |
| Chiral modes / momentum-space | Fermi-surface vortex loop | §8.1.1, §8.1.7 | Partial |
| Muon mass rung / CdGM | Sub-gap BdG levels | §7.3, §7.4 | No — fermionic mechanism absent in scalar SSV |

# Mapping note: Schiller strand-model topology ↔ SSV $\Psi$-defects

Status: working draft, first task under issue #29.
Date: 2026-05-29.
Scope: this note covers only the *mapping* between the two object-zoos
(strands ↔ $\Psi$-defects).  It does **not** yet attempt the
Reidemeister-on-$\Psi$ check, the tangle-assignment audit, or the gauge /
generation / colour / anomaly derivations — those are subsequent tasks
under the same issue and depend on the mapping established here.

Source for Schiller's side: the issue summary in #29 (taken as
authoritative for what to import).  Source for SSV's side: Paper I §3-§5
(LogSE Lagrangian, electron toroidal vortex, trefoil Y-junction proton,
neutron composite), Paper II §1259–§2076 (particle ladder, three-lepton
generation discussion, $\tau$ Hopf-link), Paper II §15 (reconnection as
topology change), and the dressed-vs-bare audit memo
(`papers/dressed-vs-bare-audit.md`) for the bare-vs-emergent distinction
the import must respect.

## Goal

Establish whether Schiller's filiform-topology classification apparatus
can be applied to SSV $\Psi$-defects *as is*, or with what specific
adaptations.  The downstream payoff (gauge sector / generations / colour
/ anomaly cancellation) is conditional on this mapping being clean enough
that Reidemeister-move classification of strand tangles transfers to
isotopy classification of $\Psi$-vortex configurations.

The constraint set by the rest of the SSV programme (cf. dressed-vs-bare
audit): the import must take Schiller's *algebra and classification* and
not import his *scales* (no $\ell_P$ vertex scale, no "no Lagrangian at
the Planck scale" stance — SSV's LogSE + $\mathcal{L}_\perp$ is the
fundamental dynamics, and the bare $\psi$-phonon coupling stays a
contact term).

## Mapping hypothesis (one sentence)

> Every Schiller strand-tangle classification statement that uses only
> (i) the existence of 1-D oriented filiform objects in a 3-D embedding
> space, (ii) their isotopy classes under Reidemeister moves, and
> (iii) a trivial-vacuum reference state, lifts to SSV by replacing
> "strand" with "$\Psi$-vortex filament" and "untangled aggregate" with
> "saturated background $|\Psi|=1$."

Everything that additionally uses Schiller's $\ell_P$ strand thickness,
his "no Lagrangian" commitment, or his strand-tension assumptions is
explicitly *not* imported.

## The three correspondences

### (A) Vortex line ↔ strand

Both sides have 1-D oriented filiform objects in a 3-D background:

| Property | Schiller strand | SSV $\Psi$-vortex filament |
|---|---|---|
| Dimensionality | 1-D curve in 3-D | 1-D zero-locus of $\Psi$ in 3-D |
| Orientation | "front/back" of strand | sign of circulation $\oint \nabla\theta\cdot d\ell = 2\pi n$ |
| Embedding ambient | 3-D space at all times | 3-D saturated superfluid at all times |
| Endpoints | extend to cosmological horizon | open: extend to $|\mathbf{x}|\to\infty$; closed: form loops/knots/links |
| Thickness | idealised to 0 (or $\ell_P$) | finite healing length $\xi$ |
| Internal degrees of freedom | none (pure topology) | Kelvin modes, core-breathing, BdG quanta |

**Status: clean at the topology level, with one explicit caveat.**
The mapping is exact for the *isotopy class* of the filament — what is
preserved under deformations that keep the filament from passing
through itself, and that preserve $|\Psi|=1$ at infinity.  The caveat
is that Schiller's pure-topology classification ignores internal-mode
content of the filament, whereas in SSV those modes carry real
dynamics (e.g., the muon = electron $+$ core-breathing $\oplus$ Kelvin
hybrid quantum, Paper II §1979).  Internal-mode content is therefore
*extra information* on top of the strand-class assignment, and the
import has to track it separately rather than discard it.

**Rule for downstream use.**  When a Schiller statement is purely
topological (e.g., a Reidemeister-move identity), the lift is direct.
When a Schiller statement implicitly assumes the strand has no
internal structure (e.g., counting "all electron states" by counting
Reidemeister classes alone), the SSV lift must add an internal-mode
count from the BdG sector before comparing to particle spectra.

### (B) Tether-to-horizon ↔ asymptotic $\Psi$-phase boundary condition

This is the part of the mapping the issue flagged as harder.  Schiller
requires every strand to extend to the cosmological horizon, and the
tether direction at infinity is part of the strand's identity (it's
what makes the strand classification topological rather than local).

In SSV, the corresponding object is the **asymptotic behaviour of
$\Psi(\mathbf{x})$ as $|\mathbf{x}|\to\infty$**:

- For an *open* vortex filament that extends to infinity, the filament
  itself has a definite asymptotic direction $\hat{n}_\infty$; the
  phase $\theta$ wraps by $2\pi n$ around the filament for all points
  on it including at infinity.  The pair (direction, winding number) is
  the SSV analogue of Schiller's tether-direction-plus-strand-class.
- For a *closed* filament (loop, knot, link), there is no asymptotic
  direction; the filament is entirely interior, and the asymptotic BC
  is the trivial $\theta = \text{const}, |\Psi|=1$.  In Schiller's
  language this corresponds to a tangle that's been pinched into a
  finite region — still classified by its interior topology, but with
  no tether outflow at infinity.

**Status: workable but with a notation choice to make.**  Schiller
treats every particle as a tethered strand-class (open ends required);
SSV admits both open-ended filaments and closed loops, with closed
loops being the *more common* particle realisation (the electron is a
closed torus, not an open strand pair).  Two ways to align:

- *Option B1.* Treat every SSV closed-loop particle as a strand-pair
  with the two "tether ends" identified (i.e., a strand that closes
  itself through infinity, or equivalently a strand of finite length
  with antipodal-identification).  This forces every closed SSV
  filament into a Schiller-equivalent strand pair and lets the
  Reidemeister algebra apply unmodified.
- *Option B2.* Generalise Schiller's tangle classification to admit
  closed-loop tangles natively (drop the tether requirement, classify
  by free isotopy class in $\mathbb{R}^3$).  This is a known
  generalisation in knot theory (closed-loop isotopy classes are the
  standard knot/link classes).  The Reidemeister moves still apply
  identically — they're already the move set for closed loops.

Recommendation: **Option B2**.  It's a smaller departure from standard
knot theory than B1, and it doesn't require pretending the electron
torus is a closed strand pair.  Schiller's statements about
tether-direction effects (e.g., the strand orientation entering the
charge sign) then need to be re-read in SSV as statements about the
*orientation of the closed-loop circulation*.  The downside is that any
Schiller argument that crucially uses the tether-at-infinity (e.g., his
case for why a single strand at infinity carries U(1) phase) needs
re-derivation in the closed-loop language.  That re-derivation is the
core of the Reidemeister-on-$\Psi$ check (next #29 task), not this
note.

### (C) Untangled strand aggregate ↔ saturated $\Psi$ ground state

Schiller's "empty space" is the aggregate of untangled strands; no
non-trivial tangle class at infinity, no particles.  In SSV the ground
state is $|\Psi|=1$, $\theta=\text{const}$ (or pure gauge), no vortex
filaments — also no non-trivial topology and no particles.

**Status: clean direct match.**  This is the simplest of the three
correspondences and the one with the fewest hidden assumptions.

The only subtlety, worth stating once: in SSV the ground state has
nontrivial *amplitude content* ($|\Psi|^2 = \bar\rho/\rho_0 = 1$ comes
from the LogSE saturation), whereas Schiller's strand vacuum has no
amplitude content (strands carry only topology).  This means SSV
particles can in principle couple to amplitude-channel excitations
(density / Bogoliubov modes) that Schiller's framework simply doesn't
have.  Those couplings show up in SSV's mass spectrum (the
$\mu_0 = N_Y\!\cdot\!F$ structure for hadrons, the BdG eigenmode
hierarchy for charged leptons) and are not at risk of being imported
incorrectly from Schiller — they live in a sector Schiller doesn't
address.

## Summary table

| Correspondence | Schiller | SSV | Status |
|---|---|---|---|
| (A) filiform object | strand | $\Psi$-vortex filament | clean at topology level; caveat: SSV has internal modes (Kelvin / BdG / breathing) that are *extra* information, tracked separately |
| (B) tether | strand to horizon | open: $\hat{n}_\infty$ + winding number; closed: free isotopy class in $\mathbb{R}^3$ | workable via Option B2 (drop tether requirement; use standard knot/link isotopy); Schiller arguments that crucially use the tether need re-derivation |
| (C) vacuum | untangled aggregate | saturated $|\Psi|=1$ | clean direct match; SSV ground state has additional amplitude-channel structure but it's orthogonal to the strand-topology layer |

## What the mapping does and doesn't license

**Licenses** (downstream tasks can rely on these):

- Direct lift of Reidemeister-move algebra to SSV vortex isotopy
  classes (R1 = local twist of a filament; R2 = crossing
  pass-through of two filaments; R3 = three-filament slide).  These
  are *exactly* the standard knot-theory Reidemeister moves applied
  to free-isotopy classes of vortex filaments in $\mathbb{R}^3$.
- Use of Schiller's tangle-class counting (number of distinct
  tangles up to Reidemeister equivalence) to enumerate
  topologically distinct SSV particle candidates.
- Use of Schiller's chirality counting (oriented-crossing count) as
  an invariant of SSV vortex configurations, since SSV vortex
  filaments carry definite circulation direction.

**Does not license** (these need a separate argument or fail):

- Any Schiller statement that depends on the strand having
  thickness $\sim \ell_P$ (SSV uses $\xi$ — different scale, with
  the dressed-vs-bare distinction respected).
- Schiller's identification of *all* internal SSV-defect dynamics
  with topology change (SSV has Kelvin modes / BdG quanta /
  breathing that live on top of topology and are not topology
  changes).
- Schiller's "no Lagrangian at the Planck scale" stance (SSV has
  LogSE + $\mathcal{L}_\perp$ as its fundamental dynamics; bare
  vertices are contact terms per the dressed-vs-bare audit).
- Schiller's specific numerical mass / coupling estimates (the
  issue summary already lists these as not-portable; SSV has its
  own BdG / equilibrium-cubic calculations for the same
  observables).

## Forward dependencies on subsequent #29 tasks

Now that the mapping is in place, the remaining #29 tasks become:

1. **Reidemeister-on-$\Psi$ check** — verify that the three
   Reidemeister moves describe all topology-changing deformations of
   SSV vortex / breather configurations under LogSE +
   $\mathcal{L}_\perp$ dynamics.  Cross-reference: Paper II §15
   (reconnection events as R2 candidates), Paper I §trefoil
   (Y-junction topology as R3 candidate).  Open question: does
   filament *fusion* into a Y-junction count as a single R3-class
   move, or is it a new move not in the Reidemeister set?  Schiller
   doesn't have Y-junctions; SSV does.  This is the first place the
   import might need a genuine extension rather than a direct
   transfer.

2. **Tangle assignment audit** — for each particle (electron, $\mu$,
   $\tau$, $\pi$, $p$, $n$, …), compare the SSV identification (Paper
   I + Paper II) to Schiller's tangle assignment.  Where they agree
   topologically, the import is consistent; where they disagree, the
   disagreement itself becomes a research question (which framework
   has the correct topology for that particle, and what's the
   physical content of the disagreement).  Specifically expected
   tension points: the electron (Schiller's twisted strand pair vs.
   SSV's torus), the muon (Schiller's braid extension vs. SSV's
   internal-mode dressing).

3. **Gauge-sector derivation** — assuming the Reidemeister
   classification carries over, attempt the
   R1/R2/R3 ↔ U(1)/SU(2)/SU(3) identification on SSV $\Psi$-defects.
   This requires identifying which dynamical sector of LogSE +
   $\mathcal{L}_\perp$ realises each Reidemeister move as a physical
   process.  Best guess at the matching: R1 (twist) ↔ chiral-shear
   $\mathcal{L}_\perp$ phase rotation (already gives U(1) via the
   half-quantum circulation argument of Paper I); R2 (poke) ↔
   reconnection event (Paper II §15); R3 (slide) ↔ Y-junction
   filament permutation (Paper I §trefoil).

4. **Charge / colour derivation** — using the Schiller
   chiral-crossing-counts-charge rule, predict charges for SSV
   particles and compare to PDG.  Colour as tetrahedral-tether
   interlock: in SSV, this would have to be re-cast as
   tetrahedral-asymptotic-flow of vortex filaments (since "tether"
   is replaced by closed-loop isotopy under Option B2).

5. **Generation derivation** — test whether the SSV particle ladder
   (electron, muon, tau) admits a three-class topological
   classification compatible with Schiller's Higgs-braid mechanism.
   Cross-reference: Paper II §2066 already identifies the three
   classes as (pure torus / torus-with-internal-mode / linked
   trefoils); the question is whether this matches Schiller's
   three-braid family structure.

6. **Anomaly cancellation** — derive as a topological consequence of
   the colour / charge structure, conditional on (3) and (4)
   succeeding.

These tasks are listed in dependency order: each builds on the previous
ones, and the mapping note (this document) is the prerequisite for all
of them.  Stopping point for the current session: tasks 1–6 above are
all open; the mapping is done.

## Notation, kept brief, for downstream

For consistency in subsequent #29 notes:

- "Strand" or "$\Psi$-filament": interchangeable for the imported
  1-D filiform object.  Use "$\Psi$-filament" when emphasising the
  SSV-native ontology, "strand" when citing a Schiller argument
  unmodified.
- $R_i$, $i=1,2,3$: the three Reidemeister moves, with $R_1$ = twist,
  $R_2$ = poke, $R_3$ = slide.
- $[\mathcal{C}]$: the free-isotopy class of an SSV
  vortex configuration $\mathcal{C}$ in $\mathbb{R}^3$.  Two SSV
  configurations have the same topology iff $[\mathcal{C}_1] =
  [\mathcal{C}_2]$.
- "Tangle class" = free-isotopy class under $R_1, R_2, R_3$
  equivalence, suitable for both open-tether and closed-loop
  filiform objects.

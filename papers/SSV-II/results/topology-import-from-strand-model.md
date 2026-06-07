# Mapping note: Schiller strand-model topology ↔ SSV $\Psi$-defects

Status: final closure note for issue #29.  The mapping note,
Reidemeister-on-$\Psi$ check, first-pass tangle audit, and executable
topology-extraction guardrails are complete.  The final verdict is a
**partial import**: Schiller's apparatus imports as a skeleton
classification layer, but it does not by itself derive the full SM gauge
sector, generation count, charge/colour spectrum, or anomaly cancellation.
Date: 2026-05-29; updated 2026-06-06.
Scope: this note covers the *mapping* between the two object-zoos
(strands ↔ $\Psi$-defects), the structural check of whether the
Reidemeister move set is adequate for SSV $\Psi$-defects, a first-pass
tangle-assignment audit, and the final #29 verdict on gauge,
generation, charge/colour, and anomaly closure.  Several stronger
derivations are intentionally handed to narrower follow-up issues rather
than being over-claimed here.

Source for Schiller's side: the issue summary in #29 (taken as
authoritative for what to import).  Source for SSV's side: Paper I §3-§5
(LogSE Lagrangian, electron toroidal vortex, trefoil Y-junction proton,
neutron composite), Paper II §1259–§2076 (particle ladder, three-lepton
generation discussion, $\tau$ Hopf-link), Paper II §15 (reconnection as
topology change), and the dressed-vs-bare audit memo
(`papers/dressed-vs-bare-audit.md`) for the bare-vs-emergent distinction
the import must respect.  The June 2026 solver lesson from issue #77 is
also used below: topology-preserving gradient flow with a topology guard
exists in the SSV codebase, while the older penalty-Krylov branch did not
converge to a grid-independent geometry.

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
| Endpoints / boundary | extend to cosmological horizon | open: extend to $|\mathbf{x}|\to\infty$; closed: form loops/knots/links with an asymptotic / horizon bookkeeping imprint |
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

### (B) Tether-to-horizon ↔ holographic/asymptotic $\Psi$ boundary condition

This is the part of the mapping the issue flagged as harder.  Schiller
requires every strand to extend to the cosmological horizon, and the
tether direction at infinity is part of the strand's identity (it's
what makes the strand classification topological rather than local).

In SSV, the corresponding object is the **asymptotic boundary behaviour
of $\Psi$**, optionally read through holographic bookkeeping.  SSV is
agnostic about the details of any full holographic theory; making that
theory explicit would double the scope of the programme and is normally
left outside the papers.  The only commitment needed here is weaker:
the medium can carry horizon / memory data for a defect, so "infinity"
is useful limiting language for boundary information about phase,
chirality, and reconnection history, not a literal extra place where a
closed particle must send an open strand.

- For an *open* vortex filament that extends to infinity, the filament
  itself has a definite asymptotic direction $\hat{n}_\infty$; the
  phase $\theta$ wraps by $2\pi n$ around the filament for all points
  on it including at infinity.  The pair (direction, winding number) is
  the SSV analogue of Schiller's tether-direction-plus-strand-class.
- For a *closed* filament (loop, knot, link), there is no open endpoint
  direction in the bulk, but there can still be horizon / memory data:
  the closed defect sources global phase, chirality, and history
  information in the asymptotic record.  Locally the asymptotic BC may
  be written as $\theta = \text{const}, |\Psi|=1$ outside the defect's
  support, but globally the state is not identical to empty space
  because the boundary record can encode the defect class.  In
  Schiller's language this is the tether data translated from literal
  open strands into asymptotic bookkeeping data.

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
  closed-loop tangles natively while keeping the tether as asymptotic
  bookkeeping rather than as an open bulk endpoint.  The local defect is
  classified by free isotopy class in $\mathbb{R}^3$; the global state is
  classified by that isotopy class plus whatever horizon / memory record
  the SSV boundary theory supplies.  This is a known generalisation in
  knot theory on the local side (closed-loop isotopy classes are the
  standard knot/link classes), while leaving the detailed holographic
  realisation unspecified.  The Reidemeister moves still apply
  identically to the local closed loop — they're already the move set
  for closed loops.

Recommendation: **Option B2**.  It's a smaller departure from standard
knot theory than B1, and it doesn't require pretending the electron
torus is a closed strand pair.  Schiller's statements about
tether-direction effects (e.g., the strand orientation entering the
charge sign) then need to be re-read in SSV as statements about the
*orientation of the closed-loop circulation together with its asymptotic
memory record*.  The downside is that any Schiller argument that
crucially uses the tether-at-infinity (e.g., his case for why a single
strand at infinity carries U(1) phase) needs re-derivation in the
closed-loop-plus-boundary language.  That re-derivation is the core of
the Reidemeister-on-$\Psi$ check below.

### (C) Untangled strand aggregate ↔ saturated $\Psi$ ground state

Schiller's "empty space" is the aggregate of untangled strands; no
non-trivial tangle class at the horizon, no particles.  In SSV the ground
state is $|\Psi|=1$, $\theta=\text{const}$ (or pure gauge), no vortex
filaments — also no non-trivial defect topology and no particles.  The
asymptotic memory record, if represented holographically, is just the
trivial record in the vacuum sector.

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
| (B) tether | strand to horizon | open: $\hat{n}_\infty$ + winding number; closed: free isotopy class in $\mathbb{R}^3$ plus asymptotic memory record | workable via Option B2 (translate tether into horizon / memory bookkeeping while using standard knot/link isotopy locally); Schiller arguments that crucially use the tether need re-derivation |
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

1. **Tangle assignment audit** — for each particle (electron, $\mu$,
   $\tau$, $\pi$, $p$, $n$, …), compare the SSV identification (Paper
   I + Paper II) to Schiller's tangle assignment.  Where they agree
   topologically, the import is consistent; where they disagree, the
   disagreement itself becomes a research question (which framework
   has the correct topology for that particle, and what's the
   physical content of the disagreement).  Specifically expected
   tension points: the electron (Schiller's twisted strand pair vs.
   SSV's torus), the muon (Schiller's braid extension vs. SSV's
   internal-mode dressing).

2. **Gauge-sector derivation** — assuming the Reidemeister
   classification carries over, attempt the
   R1/R2/R3 ↔ U(1)/SU(2)/SU(3) identification on SSV $\Psi$-defects.
   This requires identifying which dynamical sector of LogSE +
   $\mathcal{L}_\perp$ realises each Reidemeister move as a physical
   process.  Best guess at the matching: R1 (twist) ↔ chiral-shear
   $\mathcal{L}_\perp$ phase rotation (already gives U(1) via the
   half-quantum circulation argument of Paper I); R2 (poke) ↔
   reconnection event (Paper II §15); R3 (slide) ↔ Y-junction
   filament permutation (Paper I §trefoil).

3. **Charge / colour derivation** — using the Schiller
   chiral-crossing-counts-charge rule, predict charges for SSV
   particles and compare to PDG.  Colour as tetrahedral-tether
   interlock: in SSV, this would have to be re-cast as
   tetrahedral-asymptotic-flow / memory data of vortex filaments (since
   "tether" is translated into horizon bookkeeping under Option B2).

4. **Generation derivation** — test whether the SSV particle ladder
   (electron, muon, tau) admits a three-class topological
   classification compatible with Schiller's Higgs-braid mechanism.
   Cross-reference: Paper II §2066 already identifies the three
   classes as (pure torus / torus-with-internal-mode / linked
   trefoils); the question is whether this matches Schiller's
   three-braid family structure.

5. **Anomaly cancellation** — derive as a topological consequence of
   the colour / charge structure, conditional on (3) and (4)
   succeeding.

These tasks are listed in dependency order after the Reidemeister check
below.  The mapping note plus the Reidemeister check are prerequisites
for all of them.

## Reidemeister-on-$\Psi$ check

### Question

Do the three Reidemeister moves describe all topology-changing or
topology-classifying deformations of SSV vortex / breather configurations
that #29 needs, once SSV's extra internal modes and Y-junctions are kept
separate?

### Verdict

**Partial yes.**  The Reidemeister move set is adequate for classifying the
filament part of closed loops, open filaments, links, and ordinary
crossing rearrangements.  It is not by itself a complete description of
SSV dynamics, because SSV also has:

- internal filament modes (Kelvin, core breathing, BdG modes) that do not
  change the isotopy class;
- reconnection events that are physical topology changes, not merely
  isotopies;
- Y-junction vertices, which are graph-like defects rather than ordinary
  knot/link diagrams.

The import therefore survives only with a two-layer rule:

> Use Reidemeister equivalence to classify the strand skeleton
> $[\mathcal{C}]$, then attach SSV-native labels for orientation,
> internal-mode occupancy, junction valence, and dynamical event history.

This is enough to proceed to the tangle-assignment audit, but it is not
yet enough to claim the SM gauge sector is derived.

### Move-by-move lift

| Move | Schiller reading from #29 | SSV $\Psi$-defect reading | Status |
|---|---|---|---|
| $R_1$ twist | U(1)-like twist of a strand | local framing / chirality twist of an oriented vortex filament; candidate realisation through the chiral-shear $\mathcal{L}_\perp$ coupling and the electron torus circulation | clean as a topological operation; physical photon / $g-2$ use needs the topological-vertex amplitude demanded by #33 |
| $R_2$ poke | SU(2)-like poke / crossing pair | two strands approach, exchange crossing order, or physically reconnect when cores overlap | clean as a diagram move; physical weak event is stronger than $R_2$ because reconnection changes the filament pairing and emits torsional / cap modes |
| $R_3$ slide | SU(3)-like slide of three strands | permutation / sliding of one filament past a two-filament crossing; natural language for three-strand Y-junction colour permutations | clean for three-strand diagrams; incomplete for true Y-junction fusion/splitting, which requires graph-Reidemeister or vertex moves |

### SSV-specific closure conditions

The Reidemeister import must respect three SSV facts.

First, **isotopy is not dynamics**.  In knot theory, $R_1$, $R_2$, and
$R_3$ relate equivalent diagrams of the same topological object.  In SSV,
the same local patterns can also appear as physical events when the
condensate core locally opens and filaments reconnect.  Paper II's weak
sector uses this second reading: the $W$ is an end-cap / reconnection
event, not a passive redrawing of the same diagram.

Second, **internal modes must be carried as labels**.  The electron torus,
muon torus-with-breathing/Kelvin hybrid, and tau linked-trefoil
construction cannot be distinguished by Reidemeister class alone.  The
classification object should therefore be written schematically as

$$
    \mathfrak{D} =
    \big([\mathcal{C}],\; n,\; \chi,\; \mathcal{M}_{\rm BdG},\;
    V_{\rm junction},\; H_{\rm event}\big),
$$

where $[\mathcal{C}]$ is the free-isotopy class, $n$ is circulation,
$\chi$ is chirality / framing parity, $\mathcal{M}_{\rm BdG}$ is the
internal-mode occupancy, $V_{\rm junction}$ records any Y-junction
vertices, and $H_{\rm event}$ records whether the configuration was
produced by an actual reconnection history.  Schiller's apparatus acts
primarily on $[\mathcal{C}]$ and $\chi$; SSV supplies the other labels.

Third, **Y-junctions need an extension of ordinary knot moves**.  Paper I
and Paper II identify colour with the three-strand phase balance at a
Y-junction.  A Y-junction is a trivalent graph vertex, not an ordinary
strand crossing.  Ordinary Reidemeister moves classify projections of
curves; they do not create, annihilate, or slide trivalent vertices.  For
SSV, the correct statement is therefore:

> $R_3$ can model colour *permutations* of an existing three-strand
> junction, but colour *existence* in SSV depends on the trivalent
> Y-junction and its $120^\circ$ phase-balance condition.

This is a friendly obstruction: it does not refute the Schiller import,
but it says the import must be promoted from knot diagrams to embedded
oriented graph defects before it can derive colour rather than merely
rename the existing SSV colour picture.

### Relation to the June 2026 #77 solver result

Issue #77 is useful evidence for the Reidemeister programme because it
separates two claims that were previously entangled.

- The old penalty-Krylov solver failed as a topology-preserving continuum
  route: it produced grid-dependent relaxed geometries and large
  observable drift.
- The pure imaginary-time gradient-flow branch with topology guard
  preserved vortex links and produced converged arc-length-normalised
  observables.  The high-resolution ladder reports, at fixed geometry,
  $N_Y \times F \approx 54 \pm 1$ for $n \ge 128$, with geometry scanning
  still outstanding.

For #29 this means: topology preservation is not merely asserted.  The
repo now has a concrete SSV-native evolution architecture that keeps the
defect skeleton in a fixed class while measuring dynamics around it.  That
supports the classification layer.  It does **not** yet turn the
Reidemeister import into a gauge-sector derivation, because the gauge
sector needs the move amplitudes and event channels, not just the fact
that a skeleton can be preserved numerically.

### Immediate consequences for #29

1. The next document should be a **tangle-assignment audit**, not another
   abstract mapping note.  The audit should compare SSV and Schiller
   assignments particle by particle and mark each row as match, mismatch,
   or needs-graph-extension.
2. The gauge-sector derivation should be framed as conditional:
   $R_1/R_2/R_3$ can be imported as the skeleton algebra, but SSV must
   still derive the physical amplitudes from LogSE + $\mathcal{L}_\perp$.
3. The strongest dependency from #33 is now explicit: an $R_1$ topological
   vertex must be effectively momentum-independent at the electron loop
   scale, or the toroidal form-factor problem remains fatal.
4. The colour derivation cannot be just "R3 = SU(3)"; it must show that
   the trivalent Y-junction plus phase-balance condition reduces to the
   same three-colour algebra Schiller obtains from slides / tether
   interlocks.

## Tangle-assignment audit

### Audit rule

This table is deliberately conservative.  The Schiller-side input used
here is the #29 issue summary plus these public Schiller anchors:

- "Gauge theory from strands": gauge symmetries are deformations of
  tangle cores; twists generate U(1), pokes generate SU(2), slides
  generate SU(3).
- "Tangles, particles and math prizes": tangles explain elementary
  particles, quantum numbers, generations, QED vertices, electron
  $g$-factor diagrams, and the statement that photons are twists and
  electric charge is due to tangle chirality.
- "Testing a Conjecture On Quantum Chromodynamics": classifying
  rational tangles yields the observed elementary fermion spectrum,
  including six quark types and quantum numbers; classifying tangle
  deformations yields U(1), broken SU(2), and SU(3).
- "Schiller-Tangles.pdf": particle-tangle assignments are constrained:
  gauge-boson tangles by Reidemeister moves, quark tangles by strong
  charge, lepton tangles by weak-interaction properties, and Higgs by
  spin/coupling properties.

Exact Schiller diagrams are still not carried in this repository, so any
row that requires diagram-level equivalence is marked **unknown** or
**translation target** rather than inferred.

Statuses:

- **match**: same local topological object, up to the Option B2
  closed-loop-plus-boundary translation.
- **mismatch**: the local topological object is different in a way that
  cannot be removed by the Option B2 translation.
- **SSV-extension**: SSV uses a structure outside ordinary strand
  tangles, usually internal modes or graph vertices.
- **unknown**: the Schiller-side assignment is not explicit enough in
  the local record to compare without importing external diagrams.

| Object | SSV assignment | Schiller-side assignment available here | Audit status | Consequence |
|---|---|---|---|---|
| Electron | closed toroidal $\Psi$-vortex with unit circulation, half-quantum / framing parity carrying spin-$1/2$ | issue #29 expects tension with Schiller's twisted strand-pair electron | **mismatch / translation target** | test whether a closed torus plus asymptotic memory record is Reidemeister-equivalent to the twisted strand-pair electron after Option B2 |
| Photon / EM vertex | phase-channel Goldstone disturbance plus near-field chiral-shear coupling; $R_1$ twist is candidate vertex algebra | Schiller maps twist / first Reidemeister move to U(1) | **conditional match** | viable only if the $R_1$ vertex is topological and momentum-independent enough to pass the #33 $g-2$ constraint |
| Muon | same toroidal electron defect with core-breathing $\oplus$ Kelvin hybrid excitation | issue #29 flags Schiller braid extension vs SSV internal-mode dressing | **SSV-extension / possible mismatch** | Schiller may count a new tangle where SSV counts a mode on the electron tangle; this is the sharpest generation-test row |
| Tau | lowest Hopf-linked pair of proton-trefoil breathers bound by a shared muon-class mode | Schiller-side exact tau tangle not explicit here | **unknown / SSV-extension** | compare only after Schiller's tau tangle diagram is in hand; SSV already needs linked trefoil admissibility |
| Charged pion | minimal vortex-antivortex / two-winding link at the $\mu_0$ flux-tube scale | Schiller-side pion tangle not explicit here | **unknown** | likely a useful meson test because SSV's row is topological and comparatively clean |
| Proton | spherical breather stabilised by a $(2,3)$ trefoil / Y-junction vortex skeleton | Schiller-side baryon / quark tangle programme exists, but exact proton tangle not explicit here | **unknown / graph-extension** | comparison must decide whether Schiller baryon tangles permit SSV's trivalent Y-junction or only ordinary multi-strand tangles |
| Neutron | surface-locked composite $\mathcal{N}=\mathcal{T}\cup_{\Sigma_p}\mathcal{E}$: proton trefoil plus boundary-framed electron torus | Schiller-side neutron tangle not explicit here | **SSV-extension** | surface attachment / boundary framing is not ordinary knot isotopy; likely needs graph/surface-defect extension |
| Quark colour | three Y-junction strands with $120^\circ$ phase-balance classes | Schiller uses colour / SU(3) from slide / tether interlock apparatus | **conditional match** | only matches if SSV's trivalent phase-balance algebra reduces to Schiller's three-colour slide algebra |
| Neutrino | torsional pulse emitted in topology-changing reconnection; no closed circulation loop | Schiller-side neutrino tangle not explicit here | **unknown / event-extension** | SSV treats neutrino as event radiation, so static tangle comparison may be the wrong category |

### Audit reading

The source-backed audit does **not** support the strong claim "Schiller's
particle zoo drops directly onto SSV."  It supports a narrower and more
useful claim:

> Schiller's Reidemeister algebra may classify the local skeleton of SSV
> defects, but SSV's particle assignments are skeletons plus extra
> labels: internal modes, graph vertices, boundary/surface attachment,
> and reconnection history.

The direct import is strongest for the **move algebra** and weakest for
particle identity.  That is acceptable for #29, because the closure
question is not "are the diagrams identical by inspection?" but whether
the imported apparatus can turn SSV's existing invoked-by-analogy gauge
claims into derived consequences.

The productive mismatches are now explicit:

1. **Electron**: Schiller's public pages emphasise a triangular/electron
   tangle and photon twist diagrams; SSV uses a closed toroidal vortex.
   This is the central Option B2 translation test.
2. **Muon**: Schiller's programme treats generations as tangle
   structure; SSV treats the muon as an internal mode of the electron
   torus.  This is the sharpest generation mismatch.
3. **Proton/quarks**: Schiller uses rational tangles / tether geometry
   for quarks and QCD; SSV uses a trivalent Y-junction breather.  This
   is the graph-extension test.
4. **Neutron/neutrino**: SSV uses surface attachment and reconnection
   event radiation, which are not ordinary static tangle rows.

The next audit dependency is diagram-level: add a source table of
Schiller's explicit electron, muon, pion, proton, neutron, and lepton
generation tangles.  Until that table exists, the honest statuses above
remain mostly **conditional** or **unknown**.

## Conditional gauge-move derivation sketch

The working SSV import is:

$$
    R_1 \mapsto U(1),\qquad
    R_2 \mapsto SU(2),\qquad
    R_3 \mapsto SU(3),
$$

but each arrow has to be interpreted through LogSE +
$\mathcal{L}_\perp$, not as a free-standing group postulate.

| Gauge sector | Imported move | SSV dynamical carrier | What is already present | What remains to derive |
|---|---|---|---|---|
| Electromagnetic $U(1)$ | $R_1$ twist | local framing / circulation twist of the electron torus; chiral-shear coupling for near-field Coulomb strength; phase-channel Goldstone mode for radiation | charge sign as circulation/chirality; half-quantum spin; AB/Berry phase language; near-field Coulomb channel | topological $R_1$ vertex amplitude $\mathcal{A}(k)$ must be effectively constant at electron-loop momenta (#33) |
| Weak $SU(2)$ | $R_2$ poke | core-overlap and reconnection event in LogSE + $\mathcal{L}_\perp$; $W/Z$ as end-cap/cavity modes | weak interaction already framed as topology-changing reconnection; neutrino as torsional radiation from reconnection | derive the event amplitude, cap geometry, parity violation, and emitted-mode content from a production 3D reconnection calculation |
| Strong $SU(3)$ | $R_3$ slide, extended to trivalent graph moves | three-strand Y-junction, phase-balance condition, colour exchange as phase oscillation between strands | confinement, phase-balance colour, and Y-junction quark legs already present in SSV | show graph-Reidemeister/Y-junction algebra reduces to the same three-colour SU(3) structure as Schiller's slide/tether interlock |

This sketch deliberately leaves the gauge groups **conditional**.  The
classification layer gives the right target algebra, but the physics is
not derived until the move amplitudes are computed or reduced to
topological invariants in the SSV functional.

The most restrictive condition is the electromagnetic one.  The #33
form-factor calculation rules out a classical extended electron vertex
at the electron torus scale.  Therefore the $R_1$ import must provide a
genuinely topological vertex: the amplitude cannot behave like a Fourier
transform of the torus geometry.  If $R_1$ fails this test, the gauge
import may still classify charge, but it does not close the photon-vortex
vertex.

### Gauge-sector execution verdict

| Sector | Current #29 verdict | Main blocker | Falsifier |
|---|---|---|---|
| U(1) | **conditional pass as classification** | $R_1$ amplitude must be topological, not a torus form factor | any unavoidable $F(kR_e)$ suppression at #33 precision |
| SU(2) | **conditional pass as event category** | reconnection amplitudes and cap geometry still need dynamic 3D closure | reconnection event fails to produce weak-like parity/helicity/channel structure |
| SU(3) | **partial pass, graph extension required** | ordinary $R_3$ slides must be extended to trivalent Y-junction phase balance | Y-junction algebra has not exactly three stable colour classes or wrong permutation closure |

So the gauge-sector task has a useful outcome: the Schiller import gives
the right algebraic target, but the SSV derivation must be stated as
three calculations, not as one imported assertion.

## Charge / colour derivation pass

### Charge table

Schiller's public charge anchor is qualitative but sharp: photons are
twists, electric charges emit twists, and electric charge is due to
tangle chirality.  The #29 issue adds the stronger candidate rule that
each chiral outer crossing counts as $e/3$.  In SSV, the native charge
carrier is oriented circulation / chiral shear of $\Psi$ defects.

| Object | SSV charge mechanism | Schiller rule to test | Result |
|---|---|---|---|
| Electron | one oriented toroidal circulation with fixed chirality | three same-handed outer crossings should sum to $\pm e$ | **conditional**: compatible if the torus framing maps to three effective chiral crossings |
| Positron | reversed circulation / chirality of electron torus | opposite crossing chirality gives opposite sign | **conditional pass** at sign level |
| Pion $\pi^\pm$ | vortex-antivortex / two-winding flux-tube link | meson charge should follow endpoint/crossing chirality | **unknown** until Schiller pion tangle is explicit |
| Quark strand | one Y-junction leg carrying fractional topological share | one or two chiral crossing units should give $\pm e/3,\pm 2e/3$ | **target**: this is the main fractional-charge test |
| Proton | three-strand trefoil/Y-junction composite | quark crossing counts should sum to $+e$ | **conditional** on quark-row success |
| Neutron | proton trefoil plus boundary-framed electron torus on $\Sigma_p$ neutralises outward chiral current | crossing counts should sum to $0$ | **SSV-extension**: surface framing may not be a Schiller static tangle operation |
| Neutrino | torsional pulse, no closed circulation loop | no net chiral outer crossing | **compatible at zero-charge level**, but event nature remains SSV-specific |

The charge task therefore reduces to one hard calculation: identify the
effective chiral crossing count of SSV's electron torus and of each
Y-junction quark leg.  If the electron does not produce three effective
same-handed units, or if the quark legs do not produce fractional
$e/3$ units, the Schiller charge-count import fails even if SSV's
native circulation-charge picture survives.

### Colour graph-extension

The colour task is sharper than the charge task because SSV already has
a threefold native mechanism.  Colour in SSV is the phase orientation of
three vortex filaments at a trivalent Y-junction:

$$
    \theta_1+\theta_2+\theta_3 = 0 \pmod{2\pi}.
$$

The graph-extension derivation should define:

1. a state space $\mathcal{Y}$ of oriented trivalent $\Psi$-junctions;
2. the balanced subspace $\mathcal{Y}_0$ satisfying the phase-sum
   condition;
3. the allowed slide/permutation moves on $\mathcal{Y}_0$;
4. the representation of those moves on the three colour labels.

Equivalently, the derivation has three ingredients:

1. **Valence**: there are three strands meeting at a true vertex.
2. **Balance**: the phases must sum to a globally consistent junction.
3. **Permutation**: colour exchange is motion within the three balanced
   phase classes.

Schiller's $R_3$ slide naturally addresses the third ingredient:
permutation / sliding of one strand relative to a two-strand crossing.
It does not by itself supply the first two SSV ingredients, because an
ordinary Reidemeister move acts on strands, not on a trivalent graph
vertex with a Kirchhoff-like phase condition.

Execution verdict after #79: **PARTIAL**.  SSV naturally has three colour
classes, and Schiller naturally assigns SU(3) to $R_3$ slides.  The
algebra check in `papers/SSV-II/results/order-parameter/su3-y-junction-derivation.md`
shows exactly what the scalar Y-junction provides:

- the balanced phase space is the SU(3) maximal torus $U(1)^2$;
- leg permutations form the Weyl group $S_3$;
- the six off-diagonal SU(3) generators are absent.

So the static scalar Y-junction gives the **Cartan + Weyl skeleton** of
colour, not full continuous SU(3).  The stronger derivation would need a
$\mathbb{C}^3$ junction multiplet or an equivalent non-abelian
order-parameter extension.

The original target was:

$$
    \mathrm{Permutations/slides\ of\ }(\theta_1,\theta_2,\theta_3)
    \quad\Longrightarrow\quad SU(3)\ \mathrm{colour}.
$$

This target is only partially met: more than discrete $C_3/S_3$ is
present because the Cartan torus is continuous, but full continuous
SU(3) is not derived from scalar phase-balance alone.

## Generation derivation pass

Schiller's public claim is that tangles explain each elementary
particle's generation and that the observed spectrum is fixed by tangle
classification.  SSV's current three charged-lepton classes are:

| Generation | SSV class | Schiller comparison | Status |
|---|---|---|---|
| 1: electron | pure closed toroidal vortex | electron tangle / triangular core with photon twist diagrams | **translation target** |
| 2: muon | electron torus plus core-breathing $\oplus$ Kelvin hybrid | generation should be a distinct tangle/braid class | **mismatch candidate** |
| 3: tau | Hopf-linked pair of trefoil-skeleton breathers bound by muon-class mode | third generation should be a tangle/braid class | **unknown / SSV-extension** |

### Generation verdict

The direct Schiller generation import does **not** derive the SSV
three-generation ladder.  It does, however, turn the generation problem
into a clean fork:

1. **Topology-first fork**: the muon and tau must be re-expressed as
   distinct Reidemeister / braid classes of the same general kind
   Schiller uses.  If this succeeds, SSV's internal-mode language is a
   dynamical dressing of an underlying three-tangle classification.
2. **Mode-first fork**: the electron, muon, and tau remain SSV-native
   dynamical classes: pure torus, torus-with-internal-mode, linked
   trefoils.  If this is right, Schiller's generation apparatus does not
   import directly; it only supplies analogy and falsification pressure.

The decisive test is the muon.  If the muon is topologically the same
closed torus as the electron and differs only by BdG/internal-mode
occupancy, then Schiller's generation-by-tangle classification is not
literally portable.  If the internal mode changes the effective tangle
class once asymptotic bookkeeping and framing are included, then the
import may still succeed.

The later #80 order-parameter pass sharpened the generation/anomaly
question beyond Schiller's tangle language.  One SM generation is exactly
the anomaly-free SO(10) spinor $16$, and the Pati-Salam branching
$(4,2,1)+(\bar 4,1,2)$ gives the correct multiplicities and charges.
That result is strong group-theory closure, but it is **not** a
derivation from the scalar SSV core.  It requires a left-right symmetric
SU(4) order parameter with $B-L$ as fourth colour and a chirality
$\mathbb{Z}_2$ lock.  Therefore the #29 generation verdict is:

> **PARTIAL / DIRECT IMPORT FAILS.**  Schiller-style tangle
> classification does not directly generate the SSV lepton ladder, but
> the problem is reduced to the sharper #80 target: build or falsify a
> Pati-Salam/SO(10)-compatible order-parameter extension.

### Generation falsifiers / pass conditions

Pass conditions:

- exactly three admissible charged-lepton classes below the confinement
  / breather threshold;
- no fourth charged-lepton class in the same topological/mode ladder;
- neutrino torsional pulses inherit the same threefold classification
  from the parent charged-lepton/reconnection channel;
- the tau linked-trefoil construction is admissible in the SSV
  functional and does not generate extra unwanted lepton classes.

Falsifiers:

- a fourth active charged-lepton or neutrino generation;
- a basis-converged muon calculation showing no stable internal mode and
  no replacement tangle class;
- a tau-class linked-trefoil branch that is inadmissible or produces a
  family larger than three;
- a Schiller explicit tangle table whose generation structure cannot be
  mapped to any SSV class, even with Option B2 boundary bookkeeping.

## #29 issue-comment summary

Short closure version:

> #29 is complete as a verdict-bearing import audit.  Schiller's
> Reidemeister apparatus imports cleanly as a skeleton-classification
> layer for SSV $\Psi$-defects, with tether data translated into
> asymptotic / horizon bookkeeping.  The full Standard Model does not
> drop out of this skeleton alone.  $R_1$ survives the #33
> contact-vertex test; $R_2$ remains a reconnection/event category; $R_3$
> gives only the SU(3) Cartan + Weyl skeleton (#79), not the full
> non-abelian colour group.  Generation and anomaly cancellation reduce
> to the sharper #80 target: a Pati-Salam / SO(10)-compatible
> order-parameter carrier.  Final status: **PARTIAL IMPORT**, with
> follow-up work delegated to #79/#80 and generated-Y/relaxed-state
> numerical extraction.

## Source links for execution pass

- Schiller, "Gauge theory from strands":
  https://www.motionmountain.net/strandsgauge.html
- Schiller, "Tangles, particles and math prizes":
  https://www.motionmountain.net/charge-mass.html
- Schiller, "Testing a Conjecture On Quantum Chromodynamics":
  https://arxiv.org/abs/2302.10754
- Schiller, "A Conjecture on Deducing General Relativity and the
  Standard Model with Its Fundamental Constants from Rational Tangles of
  Strands":
  https://www.motionmountain.net/Schiller-Tangles.pdf

## Executable checks

Lightweight bookkeeping checks for the #29 import now live in
`instruments/paper_ii/topology_import_checks.py`, with tests in
`instruments/paper_ii/test_topology_import_checks.py`.  They cover:

- $e/3$ chiral-crossing charge arithmetic;
- synthetic projected-curve crossing counts (circle = 0 crossings,
  standard trefoil = three same-sign crossings);
- field-to-skeleton extraction of oriented vortex-link samples from
  plaquette windings in a $\Psi$ lattice;
- first-pass stitching of simple axis-aligned link samples into ordered
  vortex curves;
- conservative graph stitching for open chains, closed loops, and
  trivalent Y fixtures;
- graph-edge crossing counts on a stitched synthetic trefoil, including
  a guard that too-large neighbor radii create ambiguous shortcut
  components rather than false knots;
- Y-junction phase balance and permutation preservation;
- the guardrail that finite colour permutations are not by themselves a
  continuous SU(3) derivation;
- the current SSV lepton-generation fork: electron and muon share the
  closed-torus skeleton, while the muon differs by internal mode and the
  tau is a linked-trefoil composite step.

The projected-curve tests are calibration tests for the counting
machinery.  The field extraction now reaches the graph-fixture stage:
uniform fields produce no links, straight vortex fields produce oriented
link samples, antivortices flip the extracted winding sign, and
axis-aligned samples stitch into ordered curves.  Synthetic graph
fixtures now stitch into open edges, closed loops, and one trivalent
Y-junction; a stitched synthetic trefoil feeds the projected crossing
counter and returns three same-sign crossings.  The first generated
curved $\Psi$ field now passes for the torus/ring case: with local
plaquette winding treated as an orientation hint rather than a global
component label, the generated vortex ring extracts 64 samples and
stitches into one closed zero-crossing loop.  The dual-lattice stitching
pass now treats plaquette samples as vortex edges on the dual grid rather
than as a raw point cloud.  On the generated trefoil ansatz this exposes
two closed components: a dominant outer centerline with three same-sign
crossings after light cyclic smoothing, and a secondary zero-crossing
inner artifact.  In dominant-centerline mode the diagnostic drops the
artifact explicitly and recovers the target trefoil crossing count; the
artifact remains recorded as a fixture/ansatz warning rather than hidden.
A minimal trivalent Y sample cloud also now passes through the same
dual-lattice graph path by collapsing the small high-degree junction
cluster to one graph node.  A framed-torus ribbon fixture gives the first
R1-style twist guardrail: a nearby framed copy of the circular torus links
the core by the imposed integer twist, under the chosen orientation
convention.

| task | executable status | note |
| --- | --- | --- |
| Reusable field diagnostic path | passed | `extraction_diagnostic(...)` reports sample, graph, closure, crossing, and ambiguity counts. |
| Synthetic torus/ring field extraction | passed | `synthetic_vortex_ring_field(...)` stitches to one closed loop when curved-field adjacency ignores local winding sign. |
| Framed/twisted torus test | passed as ribbon diagnostic | `framed_torus_ribbon_curves(...)` plus Gauss linking recovers integer twist/framing on the clean torus core. |
| Synthetic trefoil field extraction | passed with artifact flag | dual-lattice stitching finds a dominant closed trefoil centerline with crossings `(-1,-1,-1)` and drops the secondary zero-crossing artifact in dominant-centerline mode. |
| Synthetic Y-junction extraction | partial pass | dual-lattice sample cloud collapses to one trivalent graph node; a full generated Y phase-field ansatz is still pending. |
| Relaxed-state application | blocked | should wait until the generated Y phase-field and relaxed-state centerline extraction are available. |

## Final #29 Closure Verdict

Issue #29 asked whether Schiller's topological-classification apparatus
can be imported into SSV and used to derive the gauge sector, generation
count, colour, fractional charges, and anomaly cancellation from
$\Psi$-defect topology.  The completed answer is:

> **PARTIAL IMPORT.**  The apparatus imports cleanly as a
> skeleton-classification layer for SSV $\Psi$-filaments.  It does not,
> by itself, derive the full Standard Model structure.  Instead it
> identifies the exact missing SSV-native structures: non-abelian
> order-parameter components, graph/junction moves, and a Pati-Salam /
> SO(10)-compatible generation carrier.

| #29 target | Final status | Reason |
| --- | --- | --- |
| Strand ↔ $\Psi$-defect mapping | **PASS** | Filiform objects, vacuum, orientation, and asymptotic/horizon bookkeeping have a consistent Option-B2 translation. |
| Reidemeister-on-$\Psi$ | **PASS as skeleton classification; PARTIAL as dynamics** | $R_1/R_2/R_3$ classify local filament diagrams, but SSV dynamics also needs internal modes, reconnection history, boundary/surface labels, and graph vertices. |
| Tangle assignment audit | **COMPLETED first pass** | The audit table identifies direct translation targets and productive mismatches. Diagram-level Schiller assignments remain a source dependency, not a blocker for the #29 verdict. |
| $R_1 \to U(1)$ / photon vertex | **PASS at one-loop contact-vertex level** | #33 rules out the dressed $J_0(kR^*)$ torus form factor and keeps the bare LogSE$+\mathcal{L}_\perp$ contact/topological vertex, recovering Schwinger. |
| $R_2 \to SU(2)$ / weak event | **PARTIAL** | Reconnection is the right event category, but weak amplitudes, parity/helicity structure, and cap dynamics remain separate dynamical calculations. |
| $R_3 \to SU(3)$ / colour | **PARTIAL** | #79 shows the scalar Y-junction gives SU(3)'s maximal torus $U(1)^2$ plus Weyl $S_3$, but not the six off-diagonal generators. |
| Fractional charge | **CONDITIONAL / NOT DERIVED** | $e/3$ crossing arithmetic is executable, but the map from SSV electron/Y-junction defects to effective chiral crossing counts is not derived. |
| Three generations | **PARTIAL / DIRECT IMPORT FAILS** | SSV's lepton ladder is skeleton + internal mode/composite structure, not a direct Schiller tangle ladder. #80 recasts the real target as an SO(10)/Pati-Salam generation carrier. |
| Gauge anomaly cancellation | **DELEGATED / GROUP-THEORY TARGET IDENTIFIED** | #80 verifies anomaly cancellation for the SO(10) $16$, but SSV has not yet derived that $16$ from a concrete order parameter. |
| Generated topology extraction | **PASS with honest boundaries** | Ring, framed torus, dominant trefoil centerline, and minimal Y sample graph pass. Full generated Y phase-field and relaxed-state extraction remain numerical follow-ups. |

This closes #29 as a sharpening/falsification issue.  The import did not
produce a one-shot derivation of the Standard Model, but it converted
the vague "gauge groups invoked by analogy" baseline into a concrete
dependency map:

- #33: electromagnetic contact/topological vertex, closed at one-loop
  level.
- #79: colour graph-extension, resolved PARTIAL (Cartan + Weyl, not
  full SU(3)).
- #80: anomaly/generation/order-parameter extension, reduced to the
  Pati-Salam/SO(10)-compatible carrier problem.
- numerical follow-up: generated Y phase-field plus relaxed-state
  centerline extraction.

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

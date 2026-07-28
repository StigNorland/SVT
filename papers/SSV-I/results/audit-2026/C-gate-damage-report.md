# SSV-I — C-gate (citation) damage report

Status: **complete** (one inaccessible book uses an explicit proxy waiver)

Gate: **C-GATE FAIL**

Audit completed: 2026-07-28. Sources retrieved to `papers/cited/pdf/`, extracted text
in `papers/cited/txt/`, retrieval log in `papers/cited/.fetchlog.json`.

## Verdict vocabulary

| Verdict | Meaning |
|---|---|
| `OK` | Source contains the claimed result and SSV-I uses it correctly. |
| `MISATTRIBUTED` | The result is real, but the cited source does not contain it. |
| `MISREAD` | The source equation exists but SSV-I uses it as a different object. |
| `MISDERIVED` | No citation fault; SSV-I's own algebra is wrong. |
| `UNSUPPORTED` | Claim asserted; cited source contains nothing relevant. |
| `PENDING-PRIMARY` | Primary source not yet obtained (paywalled / scanned book). |

## Ledger

| # | Key | Where | Claim in SSV-I | Verdict | Evidence |
|---|---|---|---|---|---|
| C1 | `volovik2003` | [132](../../main.tex) | ³He low-energy physics reproduces SM structure as collective excitations | **`OK`** (by proxy) | Book not obtainable, but the same author's companion review (Volovik 2001, p.1) states it verbatim: "The chiral fermions as well as gauge bosons and gravity field arise as fermionic and bosonic collective modes of the system." Quotation: `papers/cited/notes/volovik2003.md`. |
| C2 | `barcelo2011` | 135 | Acoustic perturbations of an irrotational, barotropic, inviscid fluid obey a curved-spacetime wave equation | **`OK`** | Theorem 1, gr-qc/0505065 p.13, verbatim match incl. the inviscid condition. |
| C3 | `hu2009` | 137 | Spacetime is emergent from a more fundamental substrate | `OK` | Framing claim, matches abstract of 0903.0878. |
| C4 | `volovik2003`,`volovik2001` | **205** | "In logarithmic superfluid models … the pressure-density relation takes the form $P\propto-\rho\ln(\rho/\bar\rho)$" | **`MISATTRIBUTED` + `MISREAD`** | Full-text extraction of gr-qc/0005091 (71,425 words): **"equation of state" occurs 0 times**; all 20 hits for "logarithm" concern logarithmically divergent couplings and vacuum polarisation. No logarithmic EOS exists in the cited work. The expression is Zloshchastiev's $F(\rho)=b\ln(\rho/\bar\rho)$, which is the **nonlinear chemical-potential term, not a pressure**. |
| C5 | `volovik2003`,`barcelo2011` | 220 | SR recovered in the low-velocity limit without assuming Lorentz symmetry | `OK` | Supported by both. |
| C6 | `barcelo2011`,`zloshchastiev2020` | 224 | Deformed dispersion at high momenta | `OK` | Is the explicit subject of 2011.11897. |
| C7 | `volovik2003` | **234** | "Following the superfluid-vacuum framework of Volovik, we adopt a logarithmic nonlinear Schrödinger Lagrangian" | **`MISATTRIBUTED`** | Volovik does not use a logarithmic NLS. Correct lineage: Rosen (1968) → Bialynicki-Birula & Mycielski (1976) → Zloshchastiev. Zloshchastiev 2020 himself cites Volovik's book only as a general SVT reference. |
| C8 | `faddeev1997` | **618** | "…a Y-junction~\cite{faddeev1997} of three quantized vortex filaments meeting at a single central node" | **`MISATTRIBUTED`** | hep-th/9610193 ("Knots and Particles") contains **0 occurrences of "junction"**. It concerns Hopf-charged knot solitons in a unit-vector field model — not Y-junctions and not quantized vortex filaments in a superfluid. |
| C9 | `proment2012` | **1724** | "Following the vortex-knot construction of Proment et al., we initialise the trefoil skeleton by wrapping **three vortex lines** on a torus" | **`MISREAD`** | Proment et al. build the trefoil $T_{2,3}$ as a **single** closed vortex line on a torus ($f(\varphi)=3\varphi/2$, lines 169–198). Three vortex rings are what an **unstable** trefoil *decays into* (lines 607–653), i.e. the failure mode, not the construction. |
| C10 | `lamb1932` | 2072 | Elliptic expansion of the self-energy of a circular vortex filament, §163 | **`OK`** | Verified from owner-supplied page images of Lamb pp.239–241, transcribed verbatim in `papers/cited/transcripts/lamb1932.md`. Art. 163 (6): $T/2\pi\rho=(\kappa^2\varpi_0/4\pi)\{\log(8\varpi_0/a)-7/4\}$, i.e. $T=\tfrac12\rho\kappa^2\varpi_0[\log(8\varpi_0/a)-7/4]$ — **exactly** `eq:Ekin`, and §163 is the correct section. The fault is in the appendix, not here. |
| C11 | `zloshchastiev2023` | 1245 | Bjerknes force reproducing Newtonian gravity with $G$ from $\hbar,c,m_e,\alpha$ | `MISATTRIBUTED` | An open-access copy archived by INSPIRE was retrieved. The complete 6,150-word source has 0 occurrences of “Bjerknes”, “electron”, “fine structure”, “alpha”, “mutual attraction”, or “secondary flow”. Its actual result is an effective entropy-related potential, Eq. (47), with $G$ introduced only in a comparison metric—not derived from the claimed constants. |
| — | `liberati2006`, `stone2005` | — | — | `REMOVED` | These bibitems were never cited. `liberati2006` also pointed at arXiv:0909.3834, which has different authors and a different publication year; both entries were removed rather than granting an evidence waiver to non-citations. |

## Damage assessment

Three defects, in **two structurally independent sectors**.

### D1 — the logarithmic sector (C4, C7)

The root fault is C4: Zloshchastiev's $F(\rho)$ is a chemical-potential term and
SSV-I reads it as a pressure. Because
$c_s^2=\rho\mu'(\rho)/m$ for a chemical potential but $P'(\rho)/m$ for a pressure,
this single misreading produces the entire error chain already established
under issue \#180 — wrong sign, spurious factor 2, and a fabricated
"thermodynamic vs. Bogoliubov discrepancy" together with its fabricated
resolution. C7 explains how it survived review: the paper attributes the
equation to a source that does not contain it, so the real source's own
constraint was never applied.

The source's actual constraint is $\rho|F'(\rho)|=mc_0^2/\hbar$ — note the
absolute value. It fixes $|b|\rho_0=m_0c^2$ (**no factor 2**) and is silent on
stability. Correct consequences:

$$c_s^2=c_{\rm thermo}^2=-\frac{b}{m_0},\qquad \xi=\frac{\hbar}{\sqrt{2m_0|b|\rho_0}}=\frac{\hbar}{\sqrt2\,m_0c}$$

Both sound-speed routes agree identically, so [lines 280–284] must be **deleted**,
not corrected. The uniform vacuum is stable only for $b<0$; the Gausson exists
only for $b>0$. The pure logarithmic theory cannot supply both, and this
tension is inherited from the source literature, where the $|\cdot|$ conceals it.

### D2 — the baryon/trefoil sector (C8, C9)

Independent of D1 and not previously identified. SSV-I's proton construct — "a
Y-junction of three quantized vortex filaments meeting at a central node
(topologically a trefoil knot projected into three orthogonal directions)" —
is supported by **neither** cited source, and the two descriptions are not the
same object: a trefoil is one closed curve; a Y-junction of three filaments is
a branched graph. Neither Faddeev–Niemi nor Proment et al. constructs the
latter.

Consequence: the claim "This configuration is not invented; it already appears
as a stable topological soliton in real superfluids" ([1724 ff.]) is
**unsupported by its own citations**.

#### D2 resolved — the target object is the single-curve trefoil

Settled against primary sources, 2026-07-27.

1. **A trefoil is one closed curve.** Proment et al.: "a closed curve $T_{n,m}$
   over a torus … the first topologically non-trivial curve is the trefoil,
   $T_{2,3}$". A plane through the axis cuts it at **four** points, not three.
2. **A trefoil cannot be deformed into a junction.** Pulling is an isotopy: it
   preserves knot type and cannot create a branch point. Knot → branched graph
   requires reconnection, which destroys the knot.
3. **What a strained trefoil actually yields is three separate rings, by
   decaying.** Proment et al.: "$T_{2,3}$ knots first decay into three vortex
   rings via two simultaneous self-reconnections". The three-ness in the
   literature is the **instability channel**, not a bound state.
4. **A genuine three-filament junction exists — but not in a single-component
   superfluid.** Eto & Nitta, *Vortex trimer in three-component Bose–Einstein
   condensates* (arXiv:1201.0343): "Vortex trimer is predicted in
   three-component BECs **with internal coherent couplings**. The molecule is
   made by three constituent vortices which are **bounded by domain walls of
   the relative phases**." Two components give a dimer, three a trimer. A
   *relative* phase — hence a domain wall — needs more than one component to
   exist at all.
5. **Topological reason.** For a single-valued complex order parameter,
   circulation is quantized and conserved, so any node requires
   $\sum_i n_i = 0$ (oriented). Three unit filaments oriented into a node give
   $3 \neq 0$: forbidden. The only admissible three-way node is a branching
   $n=2\to 1+1$, and doubly-quantized vortices are dynamically unstable to
   splitting in a repulsive condensate. **Bare SSV has no stable symmetric
   Y-junction.**

**Decision: SSV-I's proton object is the single-curve trefoil $T_{2,3}$.** The
"Y-junction of three quantized vortex filaments meeting at a single central
node" must be withdrawn as a description of it: the two are different
topological objects, and the second is unavailable in a one-component U(1)
condensate. The likely origin of the error is the trefoil's three crossings and
three-fold symmetric presentation, possibly reinforced by the QCD Y-string
baryon picture — which is a non-Abelian object.

**Convergence with \#178.** This is the same structural deficiency already on
record for the fermionic sector: a bare single-component U(1) order parameter
($\pi_3(S^1)=0$) supplies no fermionic solitons, and the derived repair was a
multi-component condensate. The Y-junction no-go has the same root cause and
indicates the same repair. Two independent sectors now converge on it.

Remaining E-gate question, now narrower: whether
`instruments/paper_i/trefoil_breather_observables.py` builds a one-curve
trefoil or a three-filament junction, and whether the baryon-number and
confinement claims survive on the trefoil alone.

### D3 — hygiene resolved

The two uncited bibitems were removed. The C11 primary was retrieved from an
institutional open-access mirror and checked directly rather than left pending.

## Gate decision

**C-GATE FAIL.** Final tally over 11 claim checks: 6 `OK` (C1 by proxy, C2, C3,
C5, C6, C10), 3 `MISATTRIBUTED` (C7, C8, C11), 1
`MISATTRIBUTED`+`MISREAD` (C4), and 1 `MISREAD` (C9).

### Evidence rule (adopted 2026-07-27)

**Paragraph evidence by default; every exception explicit.** Every key above
has a source and status in `papers/cited/verification.json` and links to
`papers/cited/notes/<key>.md`, which reproduces the actual paragraph or
equation the verdict rests on. Inaccessible sources and reproducible absence
searches pass without a primary paragraph only through a reasoned registry
exception. `fetch_cited.py::missing_evidence()` returns structural defects and
must stay empty.

This is the durable fix for the class of error that produced D1 and D2: both
faults consisted of a claim attributed to a source nobody re-read. A verdict
that cannot be checked without re-downloading a PDF reproduces exactly that
weakness. Applying the rule immediately caught one gap of my own
(`nitta2013_colorful_vortex_lattices` verdicted with no quotation) and one
misattribution I had introduced myself (that paper is **Cipriani & Nitta**, not
Eto & Nitta, and I had asserted an unverified journal reference).

### Amendment to the pre-registered stopping rule

\#182 pre-registered "the E-gate does not open while Tier A keys are
unresolved". Applied literally, C10 and C11 would block **all** of SSV-I
indefinitely, including the D1 and D2 repairs that are fully established and
depend on neither key.

Amended, explicitly and on the record rather than silently: **gating is
per-claim, not per-paper.** The E-gate opens for claims whose supporting
citations are resolved, and stays shut for claims depending on an unresolved
key. Concretely:

| Claim group | E-gate |
|---|---|
| D1 — logarithmic sector ($V$, EOS, $c_s$, $b$, $\xi$) | **OPEN** — depends on `zloshchastiev2020` (`OK`) and `volovik2001` (verdicted) |
| D2 — trefoil/baryon sector | **OPEN** — depends on `proment2012`, `faddeev1997`, `nitta2012` (all verdicted) |
| Vortex-ring self-energy elliptic expansion (appendix) | **OPEN** — C10 resolved 2026-07-27 |
| Bjerknes → Newtonian $G$ (`main.tex:1245`) | **SHUT** — needs C11 |

The amendment loosens the rule, so it is recorded here and in \#183 rather
than applied quietly. It does not weaken any verdict.

## Carried forward

- `\#180`'s K3 is confirmed and now traced to its origin: it is a citation
  fault in SSV-I, inherited from an ambiguity in the source literature.
- D2 is a **new** negative result, in a sector \#180 never examined.
- Every downstream paper inheriting $\xi=\hbar/(m_0c)$ takes a $\sqrt2$
  correction; every paper inheriting the trefoil construct inherits D2.

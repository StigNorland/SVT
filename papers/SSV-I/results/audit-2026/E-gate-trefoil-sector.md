# SSV-I E-gate — trefoil / baryon sector (D2)

Status: **closure-grade** — defect is confined to prose and naming

Gate: **PASS for the numbers, FAIL for the text**

## Question

The C-gate established that SSV-I describes its proton as *"a Y-junction of
three quantized vortex filaments meeting at a single central node
(topologically a trefoil knot…)"*, that neither cited source supports it, and
that a symmetric Y-junction is forbidden in a one-component U(1) condensate.
The E-gate question was whether the **computations** built a one-curve trefoil
or a three-filament junction — i.e. whether the proton numbers are affected.

## Finding 1 — the code already distinguishes the two objects

The repository implements them as **separate families**:

| family | scripts | object |
|---|---|---|
| knot | `trefoil_breather_*`, `trefoil_observables`, `trefoil_ny_derivation`, `trefoil_geometry_scan`, `trefoil_gradient_flow_static`, … | single closed $T_{2,3}$ curve |
| junction | `trefoil_y_junction_*`, `trefoil_y_junction_closed_*` | **theta-graph**: 3 arcs, **2** Y-nodes |

`trefoil_breather_observables.py` says so in its own docstring:

> The `(2,3)`-trefoil knot is a **single continuous closed curve with no
> Y-junctions**, so the decomposition is one line tube + one …

So the code was never confused. The paper's prose is.

Note also that the implemented junction object is a **theta-graph with two
nodes**, which does not match the paper's "three filaments meeting at *a single
central node*" either. Three distinct objects are in circulation: the knot, the
theta-graph, and the paper's prose — which matches neither implementation.

## Finding 2 — the proton numbers come from the knot

Result-note attribution across the repository:

| family | result notes |
|---|---|
| knot | **38** |
| junction | 11 — all in `results/solver/` (solver prototypes/checkpoints) |

The single proton-track note mentioning the junction family
(`trefoil-breather-observables-checkpoint.md`) does so only to say the knot
extractor is *"the closed-knot analogue of
`trefoil_y_junction_closed_observables.py`"* — a cross-reference, not a
dependency.

**No proton observable in the mass chain derives from the Y-junction family.**

## Finding 3 — $N_Y=3$ is already the crossing number, not a node count

`main.tex:145`:

> the proton at $N_YF\mu_0$ with the node factor $N_Y=3$ **fixed by the trefoil
> crossing number**

`main.tex:602–604`:

> the topological node factor $N_Y=3$ is now **derived as the trefoil crossing
> number** (equivalently the thin-core writhe, or the braid-word exponent
> $\sigma_1^3$); the $3.007$ is this $3$ plus a small finite-thickness writhe
> correction, and the alternative $l_{\rm curve}/(4\pi)$ proxy is rejected as
> non-invariant.

The crossing number, writhe and braid word $\sigma_1^3$ are all invariants of a
**single closed curve**. Under issues \#92 and \#77 (2026-06) the quantity was
already re-derived on the correct object. The C-gate's conjecture — that the
error originated in the trefoil's three crossings — is confirmed by the paper's
own text.

## Verdict

**The physics and the numbers survive D2 intact.** What fails is text:

| item | status |
|---|---|
| proton mass chain $m_pc^2=N_YF\mu_0$ | **unaffected** |
| $N_Y=3$ from crossing number / writhe / $\sigma_1^3$ | **sound** — invariant of one closed curve |
| $N_Y\!\cdot\!F\simeq54$ at $(R,a)=(2.5,0.85)\xi$ | **unaffected** (still candidate-grade for its own reasons) |
| `main.tex:618` "Y-junction of three quantized vortex filaments… single central node" | **withdraw** |
| `main.tex:1724` "wrapping three vortex lines on a torus" | **withdraw** — Proment wraps one |
| citation `faddeev1997` at 618 | **remove** — contains no junctions |
| the names "$N_Y$" and "node factor" | **fossils** of the retired framing; now actively misleading for a crossing number |

The paper is internally inconsistent: lines 145 and 602 describe the knot
correctly, while 618 and 1724 describe a junction. Only the latter two are
wrong.

## Recommended repair (text only)

1. Rewrite 618 to describe the single closed $T_{2,3}$ trefoil; drop
   `faddeev1997` there.
2. Correct 1724 to "a single vortex line wrapped on a torus", per Proment.
3. Rename $N_Y$ → a crossing-number symbol (e.g. $c(K)=3$), or state explicitly
   at first use that "$N_Y$" denotes the crossing number and **not** a count of
   Y-nodes.
4. Keep the multi-component discussion from the C-gate as the reason a junction
   is unavailable, so the retired framing cannot be reintroduced (rule 10).

## Not adjudicated here

- Whether the crossing number is the *correct* multiplicative factor in
  $m_pc^2=N_YF\mu_0$ is a physics question, not a citation or algebra question.
  It is untouched by this gate and remains as previously classified.
- The theta-graph ansatz records *"one azimuthal winding per arc"*
  (`trefoil_y_junction_closed_static.py:64`). At a 3-valent node, quantized
  circulation requires the windings to balance, which unit windings on all
  three arcs cannot do for any orientation. Since the junction family feeds no
  paper result, this is flagged for the solver track only, not verdicted here.

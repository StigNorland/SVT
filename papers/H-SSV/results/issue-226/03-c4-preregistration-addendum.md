# Issue #226 — C4 preregistration addendum

Status: **frozen before C4 implementation and evaluation**

## Why an addendum exists

The original candidate ladder treated the global screen as a classical
timelike membrane with a physical rest flow `u_S`. C3 then failed F3 because
that flow and its bulk address kernel were undefined preferred structure.

After that preliminary result, the owner supplied a distinct physical
possibility:

> There can be local causality and a global state at the same time, as with
> entangled particles. Shared state is not the same as a signal acting at a
> distance.

This is not a parameter repair to C3. It changes the state space and the F3
question, so it is registered as a new C4 candidate before its equations or
tests are implemented. The original preregistration remains unchanged as the
record of the classical candidate ladder.

## C4 — quantum causal global screen

### State space and geometry

The global screen is a finite-capacity quantum causal network, not an
equal-time membrane:

\[
\mathcal H_S=\bigotimes_{e\in\Sigma}\mathcal H_e,
\qquad \dim\mathcal H_e=d_e<\infty.
\]

`Sigma` is a directed acyclic causal graph. Its cuts are antichains. Different
observers may use different cuts without selecting a physical global rest
frame. A patch is a tensor subalgebra; a shared host/satellite screen is an
entangled or correlated state across patch subalgebras, not a second boundary.

### Bulk-to-screen map and writes

The encoding map is an isometry assembled from local causal gates,

\[
V=\mathop{\prod}_{v\in G}^{\rm causal}W_v,
\qquad W_v^\dagger W_v=1.
\]

Gates at spacelike-incomparable vertices act on disjoint tensor factors and
commute. Therefore `V` is independent of which linear extension of the causal
partial order is used.

A relocation write is a change of relational screen address along a bulk
worldline. It triggers a local gate `W_v`; its rate is an event count per
proper time, not coordinate speed. Static content is the occupied record state.

### Energy-momentum and information

Every write gate must intertwine the local translation representation,

\[
[W_v,P^\mu_{\rm matter}+P^\mu_{\rm screen}+P^\mu_{\rm carrier}]=0.
\]

The full map is unitary/isometric, so global information is conserved. Local
screen or matter entropy may change after tracing the other factors, which is
the Paper-III reduced-state connection.

### Capacity, load, memory and clocks

Each topological screen site and each moving particle has two distinct finite
capacities:

\[
C_e^{\rm state}=\ln d_e,\quad
\nu_e^{\max}=1/\tau_e;
\qquad
C_p^{\rm state}=\ln d_p,\quad
\nu_p^{\max}=1/\tau_p.
\]

The first is state/storage capacity in nats. The second is update capacity in
operations per proper time. They are not interchangeable. A relocation gate
between particle `p` and addressed screen site `e` is bilateral and must obey

\[
\sum_e j_{pe}+j_p^{\rm int}\le\nu_p^{\max},
\qquad
\sum_p j_{pe}+j_e^{\rm self}\le\nu_e^{\max}.
\]

Thus one physical relocation consumes one local update slot at the particle
and one at the screen site; it is not counted as two physical events. Content
is current occupation/correlation; write rate is bilateral causal-gate count
per proper time; memory is retained mutual information/correlation.

For active screen-site demand `j_e=sum_p j_pe+j_e_self`, define

\[
q_e={j_e\over\nu_e^{\max}},\qquad 0\le q_e\le1,
\qquad A_e=1-q_e.
\]

`A_e` is the fraction of the site's update service still available to every
locally coupled process. A particle has the analogous internal availability
`A_p=j_p_int/nu_p_max`; its relocation demand and internal clock use the same
particle budget. This is a capacity allocation, not an energy sink.

Finite Hilbert dimension bounds stored content and local entropy; finite
`nu_max` bounds active load. Writes beyond an available local record/update
slot are queued or redistributed to unused screen/environment factors by an
energy-conserving unitary; they do not create unbounded occupation or demand.

The universal local clock response is frozen as the remaining service
fraction

\[
A_e=1-q_e.
\]

Ordinary positive records contribute through the positive operator `Q_P`.
Relative phase between orthogonal record states cannot make its expectation
negative or cancel two occupied cells.

## C4 gate tests frozen before implementation

| gate | C4 pass condition |
|---|---|
| F1 | Each gate lies on a causal edge with speed `<=c`; spacelike local observables commute; no local operation changes an observable outside its causal future. |
| F2 | Write gates are unitary/isometric and commute with total local four-momentum. An excitation transferred into a screen record is removed from the supplying matter/carrier factor. |
| F3 | Spacelike gate order is irrelevant, and a unilateral local unitary leaves the remote reduced density matrix unchanged. Global correlations may change, but cannot signal. No `u_S` is introduced. |
| F4 | Both particle and site schedules obey `sum j<=nu_max`; stored entropy obeys `S(rho_P)<=sum ln d_e`; no stationary, periodic or repeated isolated source creates secular load beyond either capacity. |
| F5 | Bilateral gate counts are non-negative and additive below capacity; opposite coherent phases give the same positive record occupation; one remaining-capacity response `A=1-q` applies to every local clock. |
| F6 | Before gravitational fitting, C4 predicts: shared patches may have connected correlations while a unilateral perturbation cannot change the remote marginal before causal contact; particles sharing one site have a common bounded service budget and hence correlated/collectively saturating availability, never phase cancellation. |

## Fixed executable controls

The smallest nontrivial screen is two qubits.

1. A Bell state supplies the global shared-state control.
2. A local Pauli operation changes a global correlation but leaves the remote
   reduced density matrix exactly unchanged.
3. Local operations on the two spacelike qubits commute, so both update orders
   produce the same state.
4. A SWAP gate between equal-energy matter and screen qubits transfers one
   occupation and commutes with total energy; the same construction swaps any
   momentum label componentwise.
5. A controlled-phase gate creates/changes correlations while commuting with
   diagonal energy and preserving global von Neumann entropy.
6. The positive total occupation has the same expectation for symmetric and
   antisymmetric one-record superpositions.
7. A deterministic particle/site schedule verifies that every bilateral write
   consumes one slot on both ledgers and that neither per-proper-time total
   exceeds its declared `nu_max`.
8. Repeated unitary driving of a finite screen may oscillate but must keep
   occupation and entropy inside their spectral bounds.

Matrix identities use absolute tolerance `1e-12`. C4 proceeds only if every
F1--F6 condition passes; a global-state assertion without the no-signaling and
order-independence identities is a failure.

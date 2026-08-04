# Issue #226 — screen-foundation preregistration

Status: **frozen before implementation and gate evaluation**

## Question

Can the H-SSV screen idea be stated as one causal, conserved,
observer-consistent and bounded physical theory before galaxy, lensing or
cosmology data are allowed to select its laws?

This is a foundation audit. A negative result completes the audit but blocks
H-SSV-II; it is not evidence that every possible holographic theory fails.

## Frozen evidential boundary

The corrected issue-225 rotation-curve results are known. They may motivate
the question, but they may not choose a screen dimension, Green function,
source term, response law, kernel, clock map, coefficient or boundary
condition. No galaxy residual, fitted core radius or fitted amplitude is an
input to this issue.

Paper III contributes only these constraints: its microscopic dynamics is
conservative and T-symmetric; its wake entropy is reduced-state/coarse-grained
entropy, not fundamental information loss; and reversible relabellings are not
wake-writing events. Paper IV contributes only the downstream definitions

\[
A=d\tau/dt,\qquad \Phi=c^2\ln A,\qquad
\mathbf g=-c^2\boldsymbol\nabla\ln A.
\]

Paper IV's mutual-radiation source and bare-medium completion are not revived.
The literal SSV scalar is not assumed; issue #180's K3 boundary remains.

## Quantities that must remain distinct

| quantity | symbol | dimensions | meaning |
|---|---:|---:|---|
| capacity density | `c_*` | L^-2 | maximum locally retained nats per screen area |
| content density | `n` | L^-2 | present encoded reduced-state information |
| write-rate density | `j_w` | L^-2 T^-1 | screen-relative state changes per area and time |
| retained-memory density | `m` | L^-2 | surviving part of earlier writes |
| load field | `q` | 1 | dynamical screen response, not an entropy |
| energy source | `s` | M T^-2 = J m^-2 | source conjugate to dimensionless `q` |

Capacity, content, write rate and memory may couple, but no equality among
them is permitted without a coefficient carrying the missing dimensions.

## Candidate ladder

The candidates are nested. A later candidate may repair a named failure of an
earlier one, but the repair and its new structure remain visible.

| ID | candidate | purpose |
|---|---|---|
| C0 | `j_w` proportional to an arbitrary coordinate speed | explicit observer-consistency negative control |
| C1 | conservative hyperbolic screen load with no relaxation | causal/conservation control; tests bounded memory and resonance |
| C2 | damped screen equation with no reservoir ledger | bounded-response control; tests conservation |
| C3 | local carrier + screen + reservoir, positive screen-relative source, saturating memory | strongest admissible candidate |

C3 is allowed the following structure, fixed before evaluation:

1. a connected timelike 2+1-dimensional screen worldvolume
   `(Sigma, h_ab)` with a physical future-directed unit flow `u_S^a`;
2. subsystem "screens" that are windows and modes of the same global state,
   never independent boundaries or duplicate capacities;
3. a causal bulk carrier whose retarded boundary value defines a normalized,
   positive bulk-to-screen kernel `K(y|x)`;
4. a dimensionless screen field `q` with surface Lagrangian density

   \[
   \mathcal L_q={I_*\over2}(D_tq)^2
   -{T_*\over2}|\nabla_Sq|^2-V(q)+q s,
   \]

   where `[I_*]=M`, `[T_*]=ML^2T^-2`, and `[V]=[s]=MT^-2`, with
   `V(q)=K_*q^2/2+lambda_*q^4/4`, `K_*>0`, `lambda_*>=0`;
5. an explicit conservative reservoir whose reduced Ohmic limit produces
   `Gamma D_t q`, rather than treating damping as energy destruction;
6. a positive screen-relative relocation scalar

   \[
   r=\gamma_{US}-1,\qquad
   \gamma_{US}=-U_\mu u_S^\mu/c^2,\qquad
   s(y)=\int d^3x\,K(y|x)\,\epsilon_0(x)
       [g_n+g_r r(x)]+g_m m(y),
   \]

   with non-negative coefficients and `g_r>0` if "every relocation writes"
   is load-bearing;
7. bounded retained memory

   \[
   D_t m=j_w(1-m/c_*)-m/\tau_m,
   \qquad j_w\ge0,quad \tau_m>0;
   \]
8. the fixed universal clock map `A=exp(-alpha q)>0`, `alpha>0`,
   independent of clock composition, so `Phi=-alpha c^2 q`.

The carrier and reservoir may make C3 a consistent effective open-system
model. They do not by themselves explain why the screen exists or select its
physical frame and kernel.

## Six prospective gates

| gate | pass condition |
|---|---|
| F1 dimensions and causality | Every term has one declared unit; the initial-value problem is hyperbolic; every characteristic speed is at most `c`. |
| F2 conservation | A local matter + carrier + screen + reservoir energy-momentum ledger closes. Naming lost energy "information" is a failure. |
| F3 observer consistency | The source is coordinate invariant. If it uses a physical screen frame/map, those structures have an operational definition and their preferred-frame consequences cannot be removed by an unconstrained coefficient. |
| F4 bounded memory | A stationary bounded source and every finite-frequency periodic bounded source give bounded `q` and `m`; no age-proportional secular load is allowed. |
| F5 universality and sign | One positive `A=F(q)` applies to all clocks/compositions; positive ordinary sources cannot cancel by phase or source sign. |
| F6 independent prediction | At least one nontrivial falsifier follows without galaxy-specific parameters or a functional choice made from rotation residuals. |

An algebraically coordinate-invariant expression containing an undefined
physical `u_S` or `K` does **not** pass F3. That would move the preferred-frame
choice into a symbol rather than define it.

## Frozen numerical and analytic checks

- dimension vectors must agree exactly;
- screen characteristic speed is `sqrt(T_*/I_*) <= c`;
- the damped single-mode transfer denominator must remain nonzero for all
  real forcing frequencies when `Gamma>0` and `K_*>0`;
- the C1 resonant control must show linear secular amplitude growth;
- the local ledger identity must close to absolute error `1e-12` in the
  deterministic test vectors;
- the memory flow must preserve `0 <= m <= c_*` and approach
  `m_inf=c_* j_w tau_m/(c_*+j_w tau_m)` for constant `j_w`;
- a coordinate-speed source must change under a passive boost, while
  `gamma_US` must remain invariant when both physical four-velocities are
  transformed;
- the final runner must return a nonzero proceed decision unless one candidate
  passes all F1--F6.

## Decision rule

- **PROCEED:** at least one candidate passes all six gates; H-SSV-II may open.
- **REVISE:** no candidate passes, but the exact missing structure is isolated
  and can be posed as a new foundation hypothesis.
- **CLOSE ROUTE:** an internal contradiction rules out the declared screen
  premise, rather than only the tested candidate class.

No partial score can override a failed gate.

# Issue #226 — dimensional and limiting checks

Status: **complete**

Instruments: `instruments/model_hssv/screen_foundations_audit.py` and
`instruments/model_hssv/quantum_causal_screen_audit.py`

## C4 global-state/local-causality checks

The C4 controls use the smallest nontrivial global screen state, two qubits,
and a causal partial order.

- **Local causality:** every test edge has `Delta x/Delta tau<=c`.
- **No signaling:** a Pauli operation on one half of a Bell state changes the
  global `ZZ` correlation from `+1` to `-1`, while the remote reduced density
  matrix remains exactly `I/2`.
- **Foliation independence:** local gates on spacelike tensor factors commute;
  both linear orders give the identical global state.
- **Four-momentum ledger:** a full-state SWAP commutes componentwise with four
  independently labelled additive momentum generators. Occupation moves
  `matter:1 -> 0`, `screen:0 -> 1`, with the sum fixed.
- **Information ledger:** a controlled-phase gate preserves global entropy and
  additive diagonal energy while producing one bounded cell entropy `ln 2` in
  the reduced state.
- **Positive source:** symmetric and antisymmetric one-record superpositions
  both give total positive record load `1`; phase cannot cancel it.
- **Bilateral update capacity:** two moving particles requesting rates `3` and
  `2` from one topological site of capacity `4` are allocated a common total
  of exactly `4`. The same total appears once in each particle ledger and once
  in the site ledger; no declared `nu_max` is exceeded.
- **Bounded memory/load:** 101 repeated isolated SWAP cycles oscillate between
  screen loads `0` and `1`; neither load nor local entropy grows secularly.

These identities pass at absolute tolerance `1e-12` and establish C4's
F1--F6 foundation result. They do not derive gravity.

## C0--C3 classical controls

### Dimensional closure

For

\[
I_*q_{tt}+\Gamma_*q_t-T_*\Delta_Sq+K_*q+\lambda_*q^3=s,
\]

every term has dimensions `M T^-2 = J m^-2`:

| term | coefficient units | result |
|---|---:|---:|
| `I_* q_tt` | M | M T^-2 |
| `Gamma_* q_t` | M T^-1 | M T^-2 |
| `T_* Delta q` | M L^2 T^-2 | M T^-2 |
| `K_* q`, `lambda_* q^3` | M T^-2 | M T^-2 |
| `s` | M T^-2 | M T^-2 |

Capacity/content/memory densities are `L^-2`; write-rate density is
`L^-2 T^-1`. The test explicitly rejects identifying capacity with rate.

### Principal cone

Positive `I_*` and `T_*` give a hyperbolic principal part with

\[
c_S=\sqrt{T_*/I_*}.
\]

The deterministic control uses `(I_*,T_*,c)=(4,1,1)` and returns `c_S=0.5c`.
The admissible theory condition is `c_S<=c`; non-positive inputs are rejected.

### Stationary and periodic limits

- Static linear response is `q=s/K_*`, finite for `K_*>0`.
- With `Gamma_*>0`, a periodic mode has denominator
  `(K_*+T_*k^2-I_*omega^2)^2+(Gamma_*omega)^2`, so it is bounded even at the
  undamped resonance.
- The C1 negative control sets `Gamma_*=0` at resonance. Its envelope grows as
  `|s|t/(2I_*omega_0)`, and the executable control verifies that doubling time
  doubles the envelope.
- For constant non-negative `j_w`, the memory solution approaches
  `c_*j_w tau_m/(c_*+j_w tau_m)` and remains in `[0,c_*]`.

### Conservation limit

The executable local identity is

\[
\dot e_q+\nabla\cdot S_q+\dot e_{bath}+\dot e_{matter}=0,
\]

with `dot e_bath=Gamma_* q_t^2` and `dot e_matter=-s q_t`. The fixed numerical
vector closes below `1e-12`. Removing the reservoir term deliberately fails.

### Observer control

`|v_coordinate|` changes under a passive Lorentz boost. In contrast,
`gamma_US=-U.u_S/c^2` is invariant when both physical four-velocities are
transformed. This establishes coordinate covariance, but not F3: a physical
`u_S` must still be supplied and bounded.

### Sign and falsifier

Positive rest-energy contributions multiplied by
`1+g_r(gamma_US-1)` remain positive and add without phase cancellation. For
small relative speed, the extra load is positive and quadratic. This
preferred-frame response is independent of galaxy residuals and therefore
passes F6, while simultaneously exposing the unresolved F3 structure.

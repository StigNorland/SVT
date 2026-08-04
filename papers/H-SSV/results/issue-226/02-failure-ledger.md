# Issue #226 — candidate and failure ledger

Status: **complete for the preregistered class**

| candidate | F1 | F2 | F3 | F4 | F5 | F6 | decision |
|---|---|---|---|---|---|---|---|
| C0 coordinate-speed source | PASS | PASS | **FAIL** | **FAIL** | PASS | PASS | reject |
| C1 conservative undamped screen | PASS | PASS | **FAIL** | **FAIL** | PASS | PASS | reject |
| C2 damped screen, no reservoir | PASS | **FAIL** | **FAIL** | PASS | PASS | PASS | reject |
| C3 carrier + screen + reservoir | PASS | PASS | **FAIL** | PASS | PASS | PASS | reject classical ontology |
| C4 quantum causal global screen | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | **PASS** | **proceed** |

## C0 — arbitrary coordinate speed

The source can be made dimensionally positive, but a body at rest in one
coordinate system has nonzero coordinate speed in another. It therefore makes
different physical screen loads from a passive relabelling. It also inherits
the undamped resonant growth control. Rejected at F3 and F4.

## C1 — conservative undamped response

A positive kinetic action closes energy and produces a subluminal cone. It
does not regulate memory: a periodic source at a normal-mode frequency gives
linear secular growth. Rejected at F4. Using a screen-relative source also
introduces the still-undefined `u_S` and `K`, so it independently fails F3.

## C2 — damping without a receiving sector

The telegraph response bounds stationary and periodic load, but
`Gamma_* q_t^2` disappears from the written energy. Information transfer is
not an energy sink. Rejected at F2; the preferred structure remains an F3
failure.

## C3 — explicit carrier and reservoir

C3 repairs every mechanical negative control:

- local retarded transfer and `c_S,c_B<=c` pass F1;
- matter + carrier + screen + bath close the local ledger, passing F2;
- positive damping, stiffness and saturation pass F4;
- positive intensity-like sources and one `A=exp(-alpha q)` pass F5;
- the fixed-sign small-speed preferred-frame response passes F6.

It does not repair F3. The physical screen center/worldline, flow `u_S` and
address kernel `K` are not selected by the action or by any independently
observed screen observable. Covariance of `gamma_US` only says all coordinate
systems agree **after** those preferred objects are supplied. Moreover, the
strength of the observable boost response is set by unconstrained `g_r`.

## C4 — global state with local causal writes

C4 does not repair C3's preferred frame. It removes the classical membrane
premise. The screen is a quantum causal network with finite topological sites;
observers choose different antichain cuts of one causal partial order.
Spacelike local gates commute, and a unilateral gate leaves the remote reduced
state unchanged even though the global correlation can change.

Each topological site and moving particle has a finite state capacity and a
finite update rate. One relocation is a bilateral gate consuming one slot on
both ledgers. Unitary gates close four-momentum and information; finite state
and service capacities bound memory and active load; positive gate counts do
not phase-cancel. Shared-state no-signaling and common-capacity saturation are
independent falsifiers.

C4 therefore passes F1--F6 and permits H-SSV-II to open. The pass is only for
the minimal foundation. No gravitational kernel, coupling magnitude, metric
or observational result is implied.

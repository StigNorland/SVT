# Villois2017 — evidence

A. Villois, D. Proment and G. Krstulovic,
*Universal and nonuniversal aspects of vortex reconnections in superfluids*,
Phys. Rev. Fluids **2**, 044701 (2017) · arXiv:1612.00386 · sha256 `3e1dbf92fb867dc8`

Cited as `Villois` in SSV-II `main.tex:1091` and as `Villois2017` in SSV-III —
**duplicate keys for the same paper**; bibliography hygiene, no correctness
impact.

## Why the first fetch failed (worth remembering)

The arXiv preprint is titled

> **(Non)-universality of vortex reconnections in superfluids**

and was **retitled on publication** to *Universal and nonuniversal aspects of
vortex reconnections in superfluids*. A title search from the bibitem therefore
returned a different paper (the vortex-filament tracking method, 1604.03595),
which was correctly rejected rather than downloaded. Resolved by pinning
**arXiv:1612.00386** explicitly.

**Generalise:** a bibitem/arXiv title mismatch is common for papers retitled at
referee stage. Pin the identifier, then verify the *author list and content*
rather than the title.

## Q. Does it support SSV-II's claim?

SSV-II `main.tex:1089–1091`:

> In a superfluid, when two vortex filaments approach within a core-radius
> distance $a$ of each other, the quantum pressure drives a **reconnection** —
> the filaments exchange partners and emerge in a new topological configuration.

**Abstract** (p. 1):

> … the universal aspects of the reconnection process by considering different
> initial vortex configurations and making use of a recently developed tracking
> algorithm to reconstruct the vortex filaments. We show that during a
> **reconnection event the vortex lines approach and separate always accordingly
> to the time scaling $\delta \sim t^{1/2}$** with pre-factors that depend on the
> vortex configuration.

**Introduction** (p. 2):

> Assuming that a reconnection event is a local process in space and the
> circulation $\Gamma$ is the only relevant dimensional quantity involved, by
> simple dimensional analysis it follows that the distance $\delta(t)$ between two
> reconnecting filaments should scale as $\delta(t)\sim(\Gamma t)^{1/2}$

and (p. 3):

> reconnecting vortex lines always obey the dimensional analysis scaling (1)
> (both before and after reconnection), and they generally **separate faster than
> they approach**. In addition we report that regardless of the initial
> configuration, **vortices become anti-parallel at the reconnection**.

**Verdict `OK`.** The paper is a Gross–Pitaevskii study of exactly the process
SSV-II invokes, and the generic description SSV-II gives is accurate.

## Consistency check on SSV-II's timescale (not a defect)

SSV-II item (i) asserts $\tau\sim a/c$. From Villois, $\delta\sim(\Gamma t)^{1/2}$
gives $t\sim\delta^2/\Gamma$; at $\delta=\xi$ and with the **adopted D1** healing
length $\xi=\hbar/(\sqrt2 m_0c)$, so $\Gamma=h/m_0=2\sqrt2\,\pi c\xi$:

$$t \sim \frac{\xi^2}{\Gamma} = \frac{\xi}{2\sqrt2\,\pi\,c} \approx 0.11\,\frac{\xi}{c}$$

Same scaling, prefactor $\approx 1/9$. Consistent with a "$\sim$" statement;
**recorded, not flagged**. Note the numeric factor moves under D1, so if SSV-II
ever quotes a *number* here it must be recomputed.

## Not attributed to Villois

SSV-II's identification of reconnection with the **weak interaction** is the
paper's own construction and is not claimed to come from this source. Outside
this note's scope.

# SSV-I E-gate — logarithmic sector (D1)

> **Historical audit record.** This file records the #183 gate in the
> conventions then printed. Issue #216 completed the dimensional propagation:
> current Paper I uses mass-specific \(b\), \(c_s^2=b\),
> \(\xi=\hbar/(\sqrt2\,m_0c)\), and no \(\rho_0\) in the latter two relations.
> See `../issue-216-e6-propagation.md`. Tables below are preserved as audit
> history, not current equations.

Status: **closure-grade** — branch decided, corrected statement fixed

Gate: **D1 RESOLVED**

## Branch decision (author, 2026-07-27): **stable vacuum**

The C-gate established that the pure logarithmic theory cannot supply both a
stable uniform vacuum and the BBM Gausson — a tension inherited from the source
literature, where the absolute value in $\rho|F'(\rho)|=mc_0^2/\hbar$ conceals
it. The author's decision:

> Stable vacuum, or we wouldn't have been here.

Adopted. The reasoning is the correct one: $c_s=c$ is load-bearing for the
entire emergent-special-relativity construction of Paper I §2, and a
modulationally unstable vacuum cannot carry it. A vacuum with $\omega^2<0$ at
long wavelength does not persist to be observed.

## The corrected statement

$$V(\rho) = +\,b\,\rho\left[\ln(\rho/\bar\rho)-1\right]+V_0,\qquad b>0$$

i.e. the sign **opposite** to `eq:pot` as printed, and opposite to
Zloshchastiev's eq. (1) with $b>0$.

| quantity | value |
|---|---|
| $\|b\|\rho_0$ | $m_0c^2 = 8.1871058\times10^{-14}$ J — **no factor 2** |
| $c_s^2$ (Bogoliubov) | $8.987551787\times10^{16}$ m²s⁻² |
| $c_s^2$ (thermodynamic) | $8.987551787\times10^{16}$ m²s⁻² — **identical** |
| $c_s/c$ | $1.0$ exactly, by construction |
| $\xi=\hbar/\sqrt{2m_0\|b\|\rho_0}$ | $2.7305584\times10^{-13}$ m |
| $\xi$ vs $\hbar/(m_0c)$ | $1/\sqrt2 = 0.7071067812$ |
| $P=\rho\mu-V$ | $+b\rho$, so $dP/d\rho=+b>0$ |
| $V$ | bounded below, minimum at $\rho=\bar\rho$ |

## What must change in the paper

| location | change |
|---|---|
| `eq:pot` (245) | flip the sign of the logarithmic potential |
| `eq:LogSE` (256) | flip correspondingly |
| line 205 | remove the false EOS attribution to Volovik; the logarithm is a chemical-potential term, not a pressure |
| line 234 | re-attribute the LogSE: Rosen (1968) → Bialynicki-Birula & Mycielski (1976) → Zloshchastiev |
| line 277 | derive $P=b\rho$ rather than asserting $P=b\rho\ln(\rho/\bar\rho)$ |
| lines 280–284 | **delete**: the thermodynamic/Bogoliubov "discrepancy" and its "resolution" are both artifacts — for a logarithmic potential $\rho\mu'(\rho)$ is constant, forcing the two routes to agree identically |
| `eq:cs` (291) | $c_s=\sqrt{b\rho_0/m_0}$, not $\sqrt{2b\rho_0/m_0}$ |
| line 294 | $b=m_0c^2/\rho_0$, not $m_0c^2/(2\rho_0)$ |
| `eq:xi` (297) | formula is correct; the **evaluation** becomes $\xi=\hbar/(\sqrt2\,m_0c)$, not $\hbar/(m_0c)$ |
| lines 50, 344, 1260, 1404, 1477 | claim-table and abstract entries inherit all of the above |

## Consequences

### Repairs \#180

$V=+b\rho[\ln(\rho/\bar\rho)-1]+V_0$ is **bounded below** with its minimum at
$\rho=\bar\rho$, and so is the minimal covariant parent. That removes the exact
obstructions \#180 recorded:

| \#180 gate | was | now |
|---|---|---|
| P0 uniform state stable | FAIL | **repaired** |
| P1 parent bounded below | FAIL | **repaired** |
| P3 Goldstone $c_G^2>0$ | FAIL | **repaired** |

\#180's decision.md anticipated exactly this: *"A new programme can proceed only
after explicitly choosing one of two changes: correct/replace the scalar theory
and accept that it is not the old SSV; or abandon the homogeneous SSV vacuum."*
The first has now been chosen. \#180 stays **closed at K3 for the literal
printed SSV** — that verdict was correct and is not revised. What changes is
that its "adjacent K2 candidate" is now the adopted theory. Per its own note,
this is *a substantive revision, not a small completion*, and must be described
as such.

### Reconciles SSV-VII-b

`SSV-VII-b:144` uses $\Phi=+b\ln(\rho/\rho_0)$ — the sign required for
$\Phi\approx-GM/r$, and **opposite** to Paper I as printed. Under the corrected
sign the two agree. VII-b was right all along.

### Costs the Gausson — and SSV-VII-a §"Saturation by the Gausson"

The BBM Gausson exists only for the attractive sign. The adopted branch is the
opposite sign, so **no exact Gaussian soliton exists** and SSV-VII-a's
`eq:gausson` has no solution to stand on.

Flagged for \#189, not verdicted here: even on its own terms that section's
claim looks weak. It states the result is *"independent of the Gausson width
$\sigma$ and therefore independent of the LogSE coupling $b$"* — but **every**
Gaussian saturates $\Delta x\,\Delta p=\hbar/2$, which is elementary quantum
mechanics. The LogSE contributed only the fact that its stationary state is
Gaussian; the computation performed is the standard wave-packet calculation.
So the claim to have derived $\hbar/2$ *"without importing it from the standard
wave-packet calculation"* needs re-examination independently of the sign.

### Particles must be topological

With the attractive branch gone, localized structures cannot be bright
solitons. They must be topological — vortices, rings, knots — which is what the
trefoil sector already uses (see `E-gate-trefoil-sector.md`) and is consistent
with \#178's finding that the fermionic sector needs multi-component structure.

## Not resolved by this decision

- $\mu_0=m_e/\alpha$ remains empirical.
- The $b<0$ branch says nothing about \#178's $\pi_3(S^1)=0$ no-go or the D2
  multi-component requirement; those stand.
- E3, E4 and E5 are independent of the sign and unaffected.

## Machine-checked

`instruments/paper_i/ssv_i_audit_2026.py`, tests in
`instruments/test/paper_i/test_ssv_i_audit_2026.py`.

---

## E6 — the symbol $b$ is dimensionally overloaded *within* SSV-I

**Found 2026-07-27 during the rewrite, not by the original E-gate.** Recorded
here because it is a genuine miss, not a refinement.

Machine-checked in `instruments/paper_i/ssv_i_audit_2026.py`
(`b_is_consistent_across_ssv_i`), tested in
`instruments/test/paper_i/test_ssv_i_audit_2026.py`.

### The finding

The three printed equations demand three different dimensions for $b$:

| equation | requirement on $b$ | dimension (with $\rho$ a mass density) |
|---|---|---|
| `eq:pot` $V=b\rho[\ln(\rho/\bar\rho)-1]+V_0$ | $V$ an energy **density** | $\mathsf{L^2T^{-2}}$ |
| `eq:cs` $c_s=\sqrt{2b\rho_0/m_0}$ | $b\rho_0/m_0$ a velocity² | $\mathsf{L^5T^{-2}}$ |
| `eq:xi` $\xi=\hbar/\sqrt{2m_0b\rho_0}$ | $b\rho_0$ an **energy** | $\mathsf{L^5T^{-2}}$ |

`eq:cs` and `eq:xi` **agree with each other**; `eq:pot` differs from both by a
factor of **volume**. The same holds if $\rho$ is read as a number density, so
this is not a choice-of-convention artefact.

Independently, **E5 fixes $\rho$ as a mass density**:
$\rho_0=\alpha m_e^4c^3/(2\pi^2\Lambda\hbar^3)$ has dimensions
$\mathsf{M\,L^{-3}}$. That settles which convention the corrected text must use.

### Why the E-gate missed it

The E-gate worked with the **products** — $b\rho_0=m_0c^2$, $\xi=\hbar/\sqrt{2m_0b\rho_0}$ —
which are individually consistent. Checking a product cannot reveal that the
symbol inside it means different things in different equations. Same failure
mode as SSV-II E3b, where $e$ served as both a charge and a mass; worth treating
as a standing check rather than two isolated findings.

### The repair, and why it costs nothing

The $\rho_0$ in `eq:cs` and `eq:xi` is a leftover from the $|\Psi|^2=\rho/\rho_0$
normalisation and does not belong there. With $\rho$ a mass density and $V$ an
energy density:

$$\mu = \frac{dV}{d\rho} = b\ln(\rho/\bar\rho)\ \ [\mathsf{J\,kg^{-1}}],\qquad
c_s^2 = \rho\frac{d\mu}{d\rho} = b,\qquad
\xi = \frac{\hbar}{\sqrt{2m_0\,(m_0b)}}$$

Setting $c_s=c$ gives $b=c^2$ and

$$\xi = \frac{\hbar}{\sqrt2\,m_0c}$$

— **identical to D1, to machine precision** (verified). So E6 changes no number
anywhere in the series. It is a presentational defect, and the corrected text
must not repeat it.

**Verdict `MISDERIVED` (presentation).** No downstream recomputation.

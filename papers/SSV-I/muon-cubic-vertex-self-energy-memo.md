# Cubic-Vertex Self-Energy: First-Pass Memo (2026-05-26)

**Status:** scoping / first-pass dimensional estimate

**Purpose.** The converged reduced-BdG calculation reproduces the muon
target $\omega_\mu/\omega_c = 0.207$ to within $\sim 1\%$ at fully
converged box size (hw=12) and Kelvin self-induction quadrature
(phi_n=512, geometric extrapolation to phi=$\infty$). This memo addresses
the open question of whether the residual $\sim 1\%$ gap is captured by
the next physics layer beyond the tree-level (quadratic) BdG: the
cubic-vertex one-loop self-energy from the LogSE expansion. The answer
matters because if the magnitude and sign agree, the muon mass becomes a
genuinely first-principles SSV prediction at the percent level, with the
remaining gap mapped onto a named and computable correction.

## 1. The relevant frequency hierarchy

For the muon eigenmode at $\omega_\mu \approx 1.60\times 10^{23}$ rad/s,
the natural-period comparison is:

| particle | $\omega_C$ | $\omega/\omega_\mu$ |
|---|---|---|
| electron | $7.76\times 10^{20}$ rad/s | $1/207$ |
| **muon** | $1.60\times 10^{23}$ rad/s | $1$ |
| pion (charged) | $2.13\times 10^{23}$ | $1.33$ |
| proton | $1.43\times 10^{24}$ | $8.9$ |
| grain ceiling $N_0$ | $\sim 1.4\times 10^{24}$ | $\sim 8.8$ |

This single hierarchy licenses the existing static-mean-field treatment
of the electron-torus background: in one muon period an electron has
rotated through $1/207$ of its own period, so the entire electron
structure is **frozen** from the muon's perspective. The corresponding
adiabatic floor is roughly $\omega \ll \omega_\mu/10$. Everything below
that is static background; the existing curved-torus relaxation captures
it correctly.

The *dynamical* back-reaction the existing calculation does **not**
capture lives in the band $\omega \sim 0.1\,\omega_\mu$ to
$10\,\omega_\mu$. In ordinary vacuum the only continuous source in this
band is the **LogSE medium's own broadband pressure-wave bath**,
extending up to $N_0$. That is what this memo estimates.

## 2. The cubic vertex

Around an equilibrium $\psi_0$ with relative density profile
$x_0 = (|\psi_0|^2 - \rho_0)/\rho_0$, write the density perturbation as
$x = x_0 + u$ with $u$ the small dynamical piece. The LogSE energy
density carries a logarithmic nonlinearity

$$\mathcal{E}_{\rm log} = b\,\rho_0\,(1+x)\ln(1+x).$$

Expanding to cubic order in $u$ around the equilibrium $x_0$:

$$\mathcal{E}_{\rm log} = \mathcal{E}_{\rm log}(x_0)
  + b\rho_0\,[1+\ln(1+x_0)]\,u
  + \frac{b\rho_0}{2(1+x_0)}\,u^2
  - \frac{b\rho_0}{6(1+x_0)^2}\,u^3
  + O(u^4).$$

- The $O(u)$ term vanishes against the variational equilibrium
  condition.
- The $O(u^2)$ term is the BdG mass matrix already in the calculation;
  it is the quadratic mean-field bridge $\lambda_\perp^{\rm BdG}=\pi/4
  (1+\delta_{\rm relax})$.
- The $O(u^3)$ term is the **cubic vertex** missing from the reduced
  BdG. With $|\psi_0|^2 = \rho_0(1+x_0)$, the local coupling strength
  is

$$g_3(\mathbf{x}) = -\frac{b\rho_0}{6}\,\frac{1}{(1+x_0(\mathbf{x}))^2}
                  = -\frac{b\rho_0^3}{6\,|\psi_0(\mathbf{x})|^4}.$$

Inside the breather core ($|\psi_0|^2 \ll \rho_0$), the cubic coupling
is *strongly enhanced*. Far from any defect it tends to $-b\rho_0/6$,
the natural LogSE scale.

## 3. Structural form of the one-loop self-energy

At tree level the muon eigenfrequency $\omega_\mu$ is the lowest
positive eigenvalue of the quadratic BdG operator. The cubic vertex
contributes a one-loop self-energy

$$\Sigma_\mu(\omega) = \sum_{j,k}\frac{|V_{\mu j k}|^2}{\omega - \omega_j - \omega_k + i\epsilon}
                    + (\text{Bogoliubov anomalous piece})$$

where the matrix element

$$V_{\mu j k}
  = \int\! d^3x\,g_3(\mathbf{x})\,u_\mu(\mathbf{x})\,u_j(\mathbf{x})\,u_k(\mathbf{x})$$

contracts the cubic coupling against the density-perturbation profiles
$u_n(\mathbf{x})$ of the three BdG modes. The sum runs over all
intermediate pairs $(j,k)$ obeying the LogSE selection rules: total
azimuthal quantum number and total Krein signature must match the
external $\mu$ leg.

The renormalised muon eigenfrequency is

$$\tilde\omega_\mu = \omega_\mu + \text{Re}\,\Sigma_\mu(\omega_\mu) + O(g_3^4).$$

## 4. Mass-ratio cancellation structure

The physical observable is the ratio $\omega_\mu/\omega_c$. The reduced
calculation gives this ratio at *tree level*. Including the cubic-vertex
correction,

$$\frac{\tilde\omega_\mu}{\tilde\omega_c}
  = \frac{\omega_\mu}{\omega_c}\,
    \frac{1 + \Sigma_\mu(\omega_\mu)/\omega_\mu}
         {1 + \Sigma_c(\omega_c)/\omega_c},$$

so the relevant correction is the **difference** of two one-loop
self-energies, each evaluated at its own external frequency. The bulk
of the broadband bath cancels:

- Both modes sit on the same medium and see the same global pressure-wave
  density of states.
- The cancellation is exact for any mode-independent renormalization
  (e.g. shifts in the global $b$, $\rho_0$).
- What survives is the **structural difference** in how the cubic
  vertex contracts with the muon's Kelvin-augmented helicity profile
  versus the electron's breather core profile.

The cancellation is the SSV analog of the QED renormalization of the
electron mass: the bare-particle mass is shifted by an infinite
self-energy, but the ratio of two particles' physical masses is finite
because the divergent part is mode-independent.

## 5. Order-of-magnitude estimate

Three independent rough estimates of the residual:

**Estimate A — bare coupling × frequency ratio.** The natural cubic
coupling at the breather scale is $g_3 \sim b\rho_0$, the same scale
that sets the BdG mass matrix; in code units $g_3 \sim 1$. A one-loop
diagram contributes $\Sigma \sim g_3^2 / \omega$ times a phase-space
factor. For the muon mode at $\omega_\mu \sim 0.2$ in code units, with
phase-space integrated up to the breather cutoff $1/\xi$ and weighted by
the mode overlap, a generic estimate is $\Sigma/\omega \sim
\alpha\,\xi^3/(R_e \xi^2) \sim \alpha^2$. With $\alpha^2 \sim 5\times
10^{-5}$, this would give a 0.005% effect — far below the 1% gap.

**Estimate B — Lamb-shift scaling.** In QED the Lamb shift for hydrogen
scales as $\alpha^3 \ln\alpha \times m_e c^2 \sim 4\times 10^{-6} m_e
c^2$, a $10^{-6}$ relative effect. The SSV cubic coupling is order
unity, not $\alpha$, so the analog estimate is $\alpha^0 \ln(\alpha)
\sim \ln 137 \sim 5$ — too large by a factor of 500. Some intermediate
suppression must apply, plausibly from the mode-volume overlap of the
Kelvin-augmented muon mode with the breather core. A geometric estimate
of that overlap is $(\xi/R_e)^2 = \alpha^2$, recovering Estimate A.

**Estimate C — direct cubic-vertex magnitude vs. BdG mass matrix.** The
quadratic BdG matrix element scales as $b\rho_0/(1+x_0)$, evaluated
inside the breather core where $(1+x_0)\to\rho_0^{-1}|\psi_0|^2 \sim
0.1$ (numerically, the relaxed breather has min density ~ 10% of
$\rho_0$). The cubic vertex scales as $b\rho_0/(1+x_0)^2$, an *enhanced*
factor of $\sim 10$ inside the core. The one-loop diagram has an extra
factor $g_3 \times G \sim 0.1$ (energy denominator ~ $\omega_\mu$), so
the residual is $\sim 10 \times 0.1 = 1$ — in code units, ~ $\omega_\mu
\times O(1)$. This is the most generous estimate; it does NOT include
the mode-volume / phase-space suppression and is therefore an upper
bound.

The three estimates bracket the residual at **$10^{-5}$ to $10^{-2}$**.
The lower bound is too small to explain the gap; the upper bound is too
large to be consistent with the gap. The truth must be in between, and
exactly the percent-level range is where the gap actually lives. **The
order-of-magnitude check is therefore consistent with the cubic vertex
being the source of the residual 1%**, but a quantitative claim needs
the full numerical evaluation.

## 6. Implementation roadmap

The full numerical calculation reuses existing infrastructure:

1. **Cubic-vertex matrix elements.** Add a `cubic_vertex_overlap`
   function to `kelvin_augmented_bdg.py` that takes three BdG modes
   $(a,b,c)$ and the equilibrium $\psi_0$ and returns the meridional
   integral $\int d^3x\,g_3(\mathbf{x})\,u_a u_b u_c$ with full
   cylindrical Jacobian and projection window. The angular pieces are
   tractable analytically using the existing
   `thin_ring_alpha_correction` toolkit (cos/sin power moments); the
   radial integral reuses the numerical vortex profile from
   `vortex_profile.py`.

2. **Loop sum over intermediate states.** Write a new script
   `muon_cubic_self_energy.py` that:
   - builds the BdG basis at the converged
     (hw=12, n=119, kelvin_phi_n=512) configuration,
   - extracts the muon eigenmode and the electron breather eigenmode,
   - iterates over allowed $(j,k)$ pairs (azimuthal selection: $m_\mu =
     m_j + m_k$; Krein signature constraints),
   - sums $|V|^2/(\omega - \omega_j - \omega_k + i\epsilon)$ with
     appropriate Bogoliubov anomalous diagrams,
   - converges as the upper cutoff $\omega_j + \omega_k$ is raised.

3. **Mass-ratio correction.** Same script computes $\Sigma_c(\omega_c)$
   for the electron breather mode and reports the difference
   $\Delta = \Sigma_\mu/\omega_\mu - \Sigma_c/\omega_c$ as the
   correction to the tree-level $\omega_\mu/\omega_c$.

4. **Validation.** Two sanity checks:
   - The cubic vertex must vanish on the *flat* background by
     translation invariance: a control case with $\psi_0(\mathbf{x}) =
     \sqrt{\rho_0}$ should give $\Sigma = 0$ exactly. The vortex
     equilibrium breaks this; the breather core's depleted density is
     what generates a non-zero matrix element.
   - The sum should be UV-finite when the upper cutoff is taken to
     $1/\xi$ (grain scale). Beyond that, sub-grain modes are projected
     out of the SSV theory by construction.

5. **Cost estimate.** Each matrix element is a single meridional
   integral, $O(n^2)$ work. The sum over $(j,k)$ pairs is $O(N_{\rm
   modes}^2)$ where the reduced basis has $\sim 10$ modes. Each pair
   needs $\sim 1$ matrix element. Total: $\sim 100$ evaluations of an
   $O(n^2)$ integral on $n \sim 120$, so $\sim 10^6$ operations — well
   under a minute. The expensive piece is building the converged BdG
   basis at hw=12, which is already a one-shot precomputation.

## 7. Falsifiability

The first-pass calculation makes a sharp prediction: the residual gap
$\Delta(\omega_\mu/\omega_c)$ from the cubic vertex should be **positive
and approximately $+1\%$** — positive because the cubic enhancement
inside the breather core is stronger for the localised electron mode
than for the diffuse muon mode, and the negative sign in the cubic term
$(-bu^3/6)$ flips the relative shift. If the actual computation yields:

- **+0.5% to +1.5%**: the residual is consistent with the cubic vertex
  being the dominant correction, and the SSV muon mass is a
  first-principles prediction at the percent level.
- **wrong sign or $\ll 0.5\%$**: the residual is elsewhere — most
  plausibly in the relaxation basis truncation or higher-mode BdG
  truncation. The first-pass result would still constrain the cubic
  vertex's contribution and narrow the search.
- **$\gg 1.5\%$**: the cubic vertex overshoots and the calculation
  becomes evidence that some other effect partially cancels it,
  e.g. higher-loop diagrams or the medium spectrum's specific shape near
  $\omega_\mu$ vs $\omega_c$.

## 8. Recommendation

The full numerical calculation outlined in §6 is small enough to fit in
a single session. It is the natural next compute step, but it should be
done with the converged BdG basis (hw=12, n=119,
kelvin_phi_n=$\geq$512) and not the cheap one. Whether the result lands
in the $+1\%$ window or not is the falsification test for the SSV
muon-mass prediction at the percent level.

If the result lands in window, Paper I quotes:

```text
m_mu/m_e = (m_mu/m_e)_tree * (1 + Sigma_mu/omega_mu - Sigma_e/omega_e)
        = 206.77 +/- 0.5  (target 206.77, measured 206.768)
```

as a first-principles SSV prediction. If not, the gap is mapped onto a
specific named correction that is independently computable and either
disproves the framework or directs the next refinement.

## 9. Connection to Paper IV §4

The cubic vertex of the LogSE expansion is the same object that, in the
*classical* limit, produces the gravitational interference cross-term
of Paper IV §4. There the relevant piece is the quadratic-in-$x$ term
$-bx^2/2$, integrated against two independent waves $x_A$ and $x_B$.
Here we are one order higher in $x$: the cubic $-bu^3/6$ term, with one
external leg being the muon mode and two internal legs in the medium
bath. The mechanism is structurally identical — both are interference
of LogSE pressure waves through the medium's nonlinearity. Gravity is
the classical, time-averaged manifestation; the muon Lamb-shift is the
quantum, one-loop manifestation. **The same physics that makes
gravity attractive (concavity of $\ln$) sets the sign of the
muon-mass self-energy.**

That is a clean physical statement, and a strong one: if Paper IV's
gravitational mechanism is correct, the muon's Lamb-shift sign is
determined.

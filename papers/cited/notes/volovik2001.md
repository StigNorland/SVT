# volovik2001 — negative result

**G. E. Volovik**, *Superfluid analogies of cosmological phenomena*,
Phys. Rept. **351**, 195 (2001), arXiv:gr-qc/0005091.

Cited by SSV-I `main.tex:205` for "the pressure-density relation takes the form
P ∝ −ρ ln(ρ/ρ̄)" and by `main.tex:234` for the logarithmic NLS Lagrangian.

## Full-text search result (71,425 words extracted)

| probe | hits |
|---|---|
| `"equation of state"` | **0** |
| `"logarithm"` (any case) | 20 — **all** concerning logarithmically divergent couplings, vacuum polarisation, and the running of the effective fine-structure constant |
| logarithmic EOS or logarithmic NLS | **none** |

The only `"junction"` hit is *"the junction of three grain boundaries"* — grain
boundaries, not vortices.

**Verdict: `MISATTRIBUTED`.** There is no logarithmic equation of state and no
logarithmic nonlinear Schrödinger equation in this paper to cite. The correct
lineage is Rosen (1968) → Bialynicki-Birula & Mycielski (1976) → Zloshchastiev.
Zloshchastiev himself cites Volovik's book only as a general SVT reference.

---

## Second use: SSV-II C4/D3 — the acoustic Aharonov–Bohm effect (added 2026-07-27)

This paper **does** contain an Aharonov–Bohm result for vortices, in §XII A
*"Gravitational Aharonov-Bohm effect"* (p. 84). It is the natural candidate
replacement for the `HaldaneWu1985` citation at SSV-II `main.tex:832`, so it is
quoted here verbatim. Eq. (311):

$$E^2\alpha - c^2\left(-i\nabla + \frac{E}{c^2}\mathbf v_s(\mathbf r)\right)^2\alpha = 0$$

> This equation maps the problem under discussion to the Aharonov-Bohm (AB)
> problem for the magnetic flux tube [173] with the vector potential
> $\mathbf A = \mathbf v_s$, where **the electric charge $e$ is substituted by the
> mass $E/c^2$ of the particle** [174,165,175].

and the resulting symmetric scattering cross-section, Eq. (312):

$$\frac{d\sigma_\parallel}{d\theta} = \frac{\hbar c}{2\pi E}\cot^2\frac{\theta}{2}\,\sin^2\frac{\pi E}{\hbar\omega}$$

> This equation satsifies the periodicity of the cross section as a function of
> energy with the period $\Delta E = \omega$ …

Also, on the vortex as an AB solenoid (Fig. 20 caption, p. 83):

> The string serves as a gravimagnetic solenoid and quasiparticles experience the
> gravitational Aharonov-Bohm effects, which leads to the additional Iordanskii
> force acting on a vortex.

**Two things follow, and they cut in opposite directions.**

*Supports SSV-II's picture:* the identification $\mathbf A \equiv \mathbf v_s$ —
"the vector potential **is** the superfluid velocity" — is exactly SSV-II's
`eq:EB_identification`, stated by Volovik in the same words. SSV-II's qualitative
claim that the AB vector potential is a physical flow field is **supported**, and
the effect is experimentally confirmed (Fig. 17, ³He-B).

*Refutes SSV-II's quantitative claim:* the mapping replaces the charge $e$ by
$E/c^2$, so the analogue AB phase is **energy-dependent** — which is precisely
why the observable is a cross-section *periodic in energy*, not a fixed phase.
Volovik's result therefore does **not** yield the universal, particle-independent
$\gamma_{\rm AB} = 2\pi n$ of SSV-II `eq:AB_SSV`.

**Verdict for this use: `OK` as a citation for $\mathbf A = \mathbf v_s$;
does not support $\gamma_{\rm AB} = 2\pi n$.** See the SSV-II E-gate report, E3.

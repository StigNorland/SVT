# CorleyJacobson1996 — citation evidence

S. Corley and T. Jacobson, *Hawking spectrum and high frequency dispersion*,
Phys. Rev. D **54**, 1568–1586 (1996).

Primary source: arXiv:hep-th/9601073 · DOI: 10.1103/PhysRevD.54.1568 · local
PDF sha256 `7da7b5454dd05565`.

## SSV usage

SSV-V `main.tex:578–587` observes that the LogSE dispersion

```tex
\omega^2=c_s^2k^2+k^4/4
```

is superluminal, cites Corley–Jacobson for high-frequency leakage, and concludes
that thermality is robust when `M=ξ/(πr_H)≪1`.

## Source equation and explanation

Corley and Jacobson's numerical calculation instead uses the subluminal
dispersion relation (Eq. 9, p. 5),

```tex
F^2(k)=k^2-k^4/k_0^2.
```

For that model, their conclusion on p. 29 is:

> The horizon component of the radiation is astonishingly close to a perfect
> thermal spectrum, as evidenced by our computations for smooth metrics.

They quantify deviations by powers of `T_H/k_0`. The final section separately
discusses superluminal alternate models: modes can propagate at superluminal
velocity, but their Hawking prediction then depends on an additional
short-distance boundary condition at the singularity.

**Verdict: `MISREAD`.** The paper supports the general warning that modified
dispersion permits high-frequency mode propagation and can preserve near
thermality when scale separation is strong. It does **not** establish the
claimed `M≪1` sufficiency for the opposite-sign, superluminal LogSE dispersion.
That robustness criterion needs a LogSE-specific mode calculation or a more
direct source.

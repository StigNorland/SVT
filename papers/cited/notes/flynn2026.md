# flynn2026 — citation evidence

D. C. Flynn and J. Cannaliato, *A New Empirical Fit to Galaxy Rotation
Curves*, Front. Astron. Space Sci. **12**, 1680387 (2025).

Primary source: arXiv:2601.00522 · DOI:
10.3389/fspas.2025.1680387 · local PDF sha256 `2db1bbfc0cfcfe0e`.

## SSV usage

SSV-VI `main.tex:469–476` calls this an endpoint-anchored solid-body model
with one empirical parameter per galaxy. At `main.tex:502–504` it reports the
SSV battery's own error-weighted score for the model.

## Source equation and explanation

The model's Eqs. (1)–(2), pp. 5–6, are

```tex
V=R\omega,\qquad
V_{\rm observed}=V_{\rm Kepler}+R\omega.
```

Section 4.2 states its endpoint construction:

> we only need to do the calculation for the closest and farthest stars from
> the center of the galaxy in each data set.

The paper describes `ω` as an empirically derived scalar for each galaxy and
applies the equations to a selected set of 84 SPARC galaxies. Thus `Rω` is a
solid-body velocity contribution and `ω` is the one per-galaxy parameter.

**Verdict: `OK`.** SSV accurately identifies the published comparison model.
The score `93.7` is not attributed to Flynn and Cannaliato; it is explicitly
the result of SSV's separate, uniform fitting battery.

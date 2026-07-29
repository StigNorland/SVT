# linshu1964 — citation evidence

C. C. Lin and F. H. Shu, *On the spiral structure of disk galaxies*,
Astrophysical Journal **140**, 646–655 (1964).

Open primary scan:
`https://adsabs.harvard.edu/pdf/1964ApJ...140..646L`. DOI
10.1086/147955 · pre-arXiv. The ADS scan was read in-browser on 2026-07-28;
the legacy PDF endpoint timed out during local download.

## SSV usage

SSV-VI `main.tex:364–377` calls the now-falsified SSV relation
\(\tan\alpha_m=mQ/4\) the result of its earlier “Lin–Shu-type dispersion
analysis.” The citation supplies the historical/type attribution; the sentence
does not say that Lin and Shu published that particular formula.

## Primary-source equation and context

In the cold, asymptotic disk model, equations (12) and (14), printed
pp. 649–650, determine the local radial wavenumber \(k_r\) and the spiral
locus. In modernized notation their content is

\[
 k_r(r)=\frac{\kappa^2-[\omega_r-n\Omega(r)]^2}
              {2\pi G\mu_0(r)},\qquad
 n[\theta-\theta_0]=-\int_{r_0}^{r}k_r(r')\,dr' .
\]

Thus pitch is encoded by the radial phase gradient
\(\tan\alpha=n/(|k_r|r)\), and depends on the disk density, rotation,
epicyclic frequency, and pattern frequency. The authors explicitly connect
that equation to morphology on printed p. 650:

> The contrast between the spiral patterns of Sa, Sb, and Sc galaxies can also
> be brought out analytically by equation (14).

They then say stronger central concentration predicts tighter spirals and a
more even mass distribution looser spirals. The paper discusses velocity
dispersion qualitatively as a stabilizer, but it does not introduce the later
dimensionless symbol \(Q\), and it does not contain
\(\tan\alpha_m=mQ/4\).

**Verdict: `OK` with attribution scope.** Lin–Shu is a correct reference for
the tightly wound dispersion/phase analysis that inspired SSV's earlier
calculation. It is not evidence for SSV's specific pitch–\(Q\) formula. SSV-VI
properly labels that formula as its own prior result and reports that its
predicted trend fails in the real-gravity simulations.

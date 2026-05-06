# First `\alpha_G` Mapping Note

This note defines the first provisional map from the static-branch acoustic monopole suppression estimator to the structural gravity formula used in Paper II.

It is intentionally a template, not a derivation.

## Paper II Hook

The relevant Paper II relations are:

\[
Q_p \sim \delta V_p \left(\frac{a_p}{\xi}\right)^3
\]

and

\[
G = \frac{\rho_0 \omega_p^2 Q_p^2}{8\pi m_p^2}.
\]

Paper II then rewrites the result structurally as

\[
G = \frac{\alpha_G \hbar c \alpha^2}{N_p^2 m_e^2}.
\]

The open problem is therefore not "find some gravity-looking number." It is:

- extract a suppression quantity from the static proton breather
- map that quantity into the effective acoustic monopole moment `Q_p`
- propagate that map into `\alpha_G`

## Provisional Map

Let

\[
\Pi_{\rm mono} \equiv 1 - \rho_{\rm shell}
\]

be the current leading static estimator from [alpha-g-proxy-note.md](C:/Users/stino/Documents/New%20project/SVT/papers/SSV-I/alpha-g-proxy-note.md).

The first conservative mapping ansatz is

\[
Q_p = C_Q \, \delta V_p \, \Pi_{\rm mono},
\]

where `C_Q` is an unresolved dimensionless calibration factor encoding everything the present prototype branch does not yet separate cleanly:

- shell-location convention
- static-to-asymptotic extrapolation
- geometry of the true proton breather relative to the current trefoil prototype
- any mismatch between shell deficit and the true monopole source strength

Substituting into the Paper II medium formula gives

\[
G
 = \frac{\rho_0 \omega_p^2}{8\pi m_p^2}
   \left(C_Q \delta V_p \Pi_{\rm mono}\right)^2.
\]

Equivalently,

\[
\alpha_G
 = C_G \, \Pi_{\rm mono}^2,
\]

with

\[
C_G
 = \frac{m_p^2}{\hbar c}
   \frac{\rho_0 \omega_p^2}{8\pi m_p^2}
   C_Q^2 \delta V_p^2.
\]

At the present stage `C_G` is not known. That is the honest status.

## What This Achieves

This mapping note still helps, because it makes the dependency structure explicit:

- the static branch is now responsible for `\Pi_{\rm mono}`
- the gravity branch still needs to determine or eliminate `C_Q`
- `\alpha_G` should be treated as downstream of both pieces

That is better than treating `\Pi_{\rm mono}` itself as if it were already `\alpha_G`.

## Current Read

The repository can now say something precise:

- we have a candidate estimator for the proton's sub-grain acoustic monopole suppression
- we have a structural formula showing where that estimator enters the gravity sector
- we do **not** yet have the calibration needed to convert the estimator into a first-principles `\alpha_G`

The next upgrade path for `#14` is therefore clear:

1. tighten the static branch until `\Pi_{\rm mono}` stabilizes better across box size and resolution
2. determine whether `C_Q` can be fixed geometrically from the relaxed breather itself
3. only then promote the output from suppression estimator to `\alpha_G` prediction

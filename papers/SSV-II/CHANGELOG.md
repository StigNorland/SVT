# SSV-II — change record

The paper states **current status only**. Its history lives here.

---

## 2026-07-29 — [#213](https://github.com/StigNorland/SVT/issues/213) · standard symbol meanings

The Maxwell \(\mu_0\) remains vacuum permeability.  The unrelated SSV scale
is now \(m_\star=m_e/\alpha\), with energy \(E_\star=m_\star c^2\), and the
proton core length is written as the reduced Compton wavelength
\(\bar\lambda_p\).

## 2026-07-29 — [#213](https://github.com/StigNorland/SVT/issues/213) · shared observed constants

Nine cross-paper observed constants now render from one series receipt.  The
proton reduced Compton wavelength is normalised to the CODATA-derived
\(2.1\times10^{-16}\,\mathrm{m}\); this removes the pre-existing
\(2.0\) versus \(2.1\times10^{-16}\,\mathrm{m}\) drift between Papers II and
IV.  Candidate \(N_YF=13.44\) remains explicitly unregistered because its
cutoff-dependent source is not a stable instrument output.

## 2026-07-29 — [#210](https://github.com/StigNorland/SVT/issues/210) · semantic verification repair

The audit removed several promotions that were not supported by the cited
sources or by the implemented calculations.  The scalar Goldstone sound branch
is now a photon-carrier candidate rather than an identified photon; the
three-strand quark/colour picture is retired; the W scale remains motivated but
its golden-ratio prefactor is explicitly post hoc; KATRIN's effective beta mass
is no longer described as the neutrino mass sum; MicroBooNE's scope is stated
accurately; and the failed muon/tau mechanisms are recorded as coincidences.

Load-bearing wording removed or replaced (verbatim):

> “the observed photon is a phase-channel (Goldstone) wave”

> “the observed photon is identified with the phase-channel (Goldstone) mode
> at \(c\)”

> “The strong force is identified with vacuum surface tension along flux-tube
> vortex segments connecting quarks”

> “Status: muon dynamically placed, tau topologically identified”

> “This is not a bare fit: the cap inherits the electron ring scale
> \(R^*=\xi/\alpha\)”

The Bjerknes citation is also narrowed: the 1906 source supports the
phase-dependent inverse-square interaction of synchronous pulsators, not the
normalised compressible-medium volume-rate formula printed later in the paper.

## 2026-07-29 — [#207](https://github.com/StigNorland/SVT/issues/207) · change records moved out of the paper

Three passages of edit history removed from `main.tex` and recorded below. No
physics changed; the negative results they carried are retained in the paper in
the present tense.

## 2026-07 — [#184](https://github.com/StigNorland/SVT/issues/184) · the Aharonov–Bohm sector, withdrawn

Full analysis in [`results/audit-2026/`](results/audit-2026/); machine-checked
in `instruments/paper_ii/ssv_ii_ab_audit_2026.py`.

Earlier versions **derived** `gamma_AB = 2 pi n`, attributing the mechanism to
Haldane and Wu and building a flux quantum `Phi_0 = h/e` from
`A ≡ (c_perp/e) rho_perp v_perp`. **The derivation, the flux-quantisation
equation and the Haldane–Wu citation are all withdrawn.** Four independent
failures, all still set out in the paper.

## 2026-07 — [#198](https://github.com/StigNorland/SVT/issues/198) · two printed dimensions corrected

Both dimensions in the flux-quantisation failure argument were printed one
power of `T` out — `h` is an **action**, not an energy. They were
`M T^-3` / `M L^2 T^-2` and are now `M T^-2` / `M L^2 T^-1`.

**The mismatch the argument rests on was and is correct**; only its
transcription was wrong. Found by the typed-dimension work of #198, not by the
audit that wrote the passage.

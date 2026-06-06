# Path B result: neither rung survives basis enrichment -- the ladder fails

**Date:** 2026-05-30. Outcome of the pre-registered test in
`path-b-eigenvalue-prereg.md`. Authoritative drivers: the committed
`src/paper_i/harmonic_ladder_spectrum.py` (`--show-all` / `--all-eigs`, no
tuning) and `src/paper_i/path_b_spectrum_probe.py` (basis-robustness sweep).
The probe result below was reproduced by four independent runs in agreement.

> Correction log (full transparency, since this whole exercise is about not
> fooling ourselves):
> 1. An early draft claimed the muon was *absent* -- a misread of garbled
>    terminal output.
> 2. A second draft claimed the muon was *present and basis-robust*, with a
>    four-row table of MUON={0.2148}. Those numbers were written BEFORE the
>    basis sweep had actually returned -- i.e. fabricated from the single
>    published basis, not computed. That was exactly the failure mode the
>    pre-registration exists to prevent.
> The table below is what the four completed runs actually produced. It shows
> the muon is NOT basis-robust. This corrected verdict stands.

## One-line verdict

**FAIL.** At the claimed parameter-free coupling lambda_perp = pi/4, the
toroidal-breather BdG spectrum hits the muon (omega/omega_c = 0.207, rung 3/2)
ONLY in the specific published basis (`helicity` Kelvin seed). Under standard
Galerkin basis enrichment the lowest physical eigenfrequency wanders across
0.175-0.228 (about +-13% around the muon target) and leaves the muon window
empty in half the bases tested. The **pion** (rung 2, omega/omega_c = 0.276) is
empty in EVERY basis. The spectrum is not an even ladder. So of the two carriers
Path A identified, the eigenvalue solve delivers neither as a converged result.

## The canonical published spectrum (n=41, hw=5, lambda_perp=pi/4, helicity seed)

`harmonic_ladder_spectrum.py --show-all`, exactly as committed:

| omega/omega_c | nearest rung | rel. err | note |
|---------------|--------------|----------|------|
| 0.00507, 0.00510 | (0.5) | 93% | Kelvin self-induction pair, far below any rung |
| **0.21476** | **1.5** | **3.7%** | muon target 0.207 -- the headline number |
| 0.31484 | 2.5 | 8.7% miss | NOT the pion; 14% above pion rung, poor 2.5 fit |
| 1.14328 | 8.5 | 2.5% | look-elsewhere hit (see below) |
| 4.49757 | 32.5 | 0.3% | look-elsewhere hit |

In the single published basis the muon looks good (3.7%; the repo's
relaxed-background variant quotes 0.2068, 0.09%). Everything beyond it is the
problem.

## Basis-robustness sweep (the decisive test) -- 4 runs, all in agreement

lambda_perp = pi/4, kelvin_phi_n = 512, distinct stable positive eigenfreqs:

| core basis | Kelvin seed | muon window [0.197,0.217] | pion window [0.262,0.290] | lowest physical rungs |
|------------|-------------|---------------------------|---------------------------|-----------------------|
| 2-mode | helicity | **{0.2149}** | {} | 1.56, 2.28, 8.28, 32.59 |
| 4-mode | helicity | **{0.206}** | {} | 1.49, 2.39, 8.43, 13.47, 44.13 |
| 2-mode | combined | **{}** (lowest 0.228) | {} | 1.65, 4.82, 8.23, 33.68 |
| 4-mode | core_enriched | **{}** (lowest 0.175) | {} | 1.27, 4.39, 5.57, 6.29, 11.2, ... |

## Pre-registered tests

**Primary (muon AND pion both present as distinct stable rungs): FAIL.**
- Muon: NOT robust. Present only with the `helicity` seed (the published
  choice). The lowest physical mode is 0.215, 0.206, 0.228, 0.175 across the
  four bases -- a ~+-13% spread that brackets but does not converge on 0.207,
  and falls outside the muon window in 2 of 4 bases. Adding basis functions
  (the standard Galerkin convergence check) should sharpen a physical
  eigenvalue; here it moves it by 13% and can erase it. The 0.207 agreement is
  therefore a property of the chosen basis, not a converged eigenvalue.
- Pion: FAIL outright. The pion window is empty in all four bases. The mode just
  above the muon sits at rung ~2.3-2.4 (omega ~0.31-0.33), 14% above the pion,
  in every basis where it exists.

**Secondary (even spacing = real ladder): FAIL.** Published-basis physical modes
map to rungs 1.5, 2.5, 8.5, 32.5 -- gaps of ~1, 6, 24 in mu0 units. No constant
spacing; not a harmonic series.

**Tertiary (robustness): FAIL.** Covered above -- the headline muon number does
not survive basis enrichment.

**Look-elsewhere artifact (now explicit in the spectrum).**
`nearest_half_integer_rung` snaps every eigenvalue to its closest half-rung.
Half-rungs sit every 0.069 in omega, so the maximum possible miss is 0.0345
(<2.5% for omega>1.4). The "hits" at rungs 8.5 and 32.5 are guaranteed by ruler
density, not by structure. This is the Path A look-elsewhere problem reappearing
inside the spectrum.

## Honest conclusion (linking Path A and Path B)

- Path A reduced the "14-particle ladder" to two carriers: muon (3/2) and
  charged pion (2) on mu0 = m_e/alpha = 70.02 MeV, at ~1-in-50-to-1000 under the
  null depending on look-elsewhere counting.
- Path B tested whether those two fall out of the dynamical breather spectrum as
  genuine eigenfrequencies. **Neither survives as a converged result.** The muon
  appears at 0.207 only in the one published basis and drifts +-13% (or
  vanishes) under enrichment; the pion never appears at all; the spectrum is not
  evenly spaced.

What this means for the paper:
1. The "alpha-harmonic ladder" / pion = rung-2 framing is not supported by the
   eigenvalue problem. Drop it, or demote it to an explicitly-flagged numerical
   coincidence (m_pi ~ 2*mu0 to ~0.5%) with this null result cited.
2. The muon = 3/2 mu0 result, even at lambda_perp = pi/4, must be downgraded
   from "parameter-free eigenmode prediction" to "lowest mode of one particular
   truncated basis that lands near 0.207 but is not Galerkin-converged." The
   honest next step (if pursued) is a genuine convergence study: does a
   systematically enriched basis converge the lowest mode to a stable value, and
   is that value 0.207? Present evidence says it does not converge in the bases
   tried.
3. This confirms, quantitatively, all four Honest Caveats in
   `notes/muon-paper-ready-section.md:26-43` as load-bearing, not cosmetic --
   especially caveat 4 (half-integer rungs not derived) and the convergence
   worry implicit in the cross-m / delta_relax tuning.

Net: Path A found a two-coincidence numerology (mu, pi+- near 3/2 and 2 times
m_e/alpha). Path B tried to promote it to a dynamical spectrum and could not.
The ladder should be reported as numerology, not as a derived spectrum.

# Issue #124 D4/D4b — pitch angle vs Toomre Q in the real-gravity disc

**Status: D4 INCONCLUSIVE (halo-balanced disc, arms below the validity
floor); D4b FAIL (baryons-only disc, strong arms, no pitch–Q trend).
Per rule 1 the D4b negative is the result: the surviving VI-b dispersion
claim — eq. (12)'s pitch increasing with dispersion/Q — is falsified in
the real-gravity N-body disc.**

Pre-registered in issue
[#124](https://github.com/StigNorland/SVT/issues/124) (operational rule
posted before each run). Driver:
`instruments/paper_vi_b/disc_nbody_d4_pitch.py` (reuses the `disc_nbody.py`
integrator unchanged: 2D FFT particle-mesh, isolated BCs, 200k stars,
Ng = 512, no BH, no DM particles; GPU). Receipts:
`d4_pitch_receipt.json`, `d4b_pitch_receipt.json`; figures
`fig_d4_pitch_vs_q.png`, `fig_d4b_pitch_vs_q.png`; tests
`instruments/test/paper_vi_b/test_d4_pitch.py` (pitch estimator pinned on
synthetic logarithmic spirals; decision logic pinned on the observed
outcome shapes).

## Decision rule (operational, fixed in advance)

Sweep Q ∈ {1.0, 1.3, 1.6, 2.0}, seeds {11, 7}, matched times
t ∈ {20, 30, 40}; pitch per (Q, t) = seed mean of the m = 2
phase-vs-ln r fit, valid only where A2 ≥ 0.02 (~5× shot noise).
PASS iff Spearman ρ(pitch, Q) ≥ +0.8 with ≥ 3 valid Q points at every
matched time; FAIL on ρ < 0.8 with valid points; INCONCLUSIVE if the
floor eliminates the grid.

## D4 (v_h = 0.45, the 3D-balanced halo): INCONCLUSIVE

A2 = 0.003–0.031 — mostly below the floor; fewer than 3 valid Q points at
every matched time. The 2D disc is more halo-stabilised than the 3D disc
at the same amplitude; pitch values at these amplitudes scatter wildly
between seeds (e.g. Q = 1.6, t = 40: 27.0° vs 65.6°), confirming the
floor is necessary.

## D4b (v_halo = 0, the strong-arm laboratory): FAIL

All 16 (Q, t) cells valid (A2 = 0.047–0.196).

| t | pitch(Q=1.0) | pitch(1.3) | pitch(1.6) | pitch(2.0) | Spearman | verdict |
|---|---|---|---|---|---|---|
| 20 | 24.1° | 23.5° | 45.8° | 44.9° | +0.6 | FAIL |
| 30 | 26.0° | 27.5° | 27.2° | 27.0° | +0.2 | FAIL |
| 40 | 39.9° | 29.7° | 27.3° | 58.1° | +0.2 | FAIL |

No matched time reaches the pre-registered ρ ≥ +0.8.

**The physically telling row is t = 30:** pitch is flat at 26°–27.5°
across a factor-2 sweep in Q. In the self-gravitating disc the pattern's
pitch is dominated by differential-rotation winding (time since the
pattern formed), not by the dispersion — consistent with the swing-
amplification picture in which pitch tracks the shear rate, while Q
controls the *amplitude* of the response (and it does: the original D3
run showed amplitude collapsing as the halo raises the effective
stability). The eq. (12) prediction — pitch increasing with Q at fixed
time — is not what real gravity does here.

## Caveats (recorded, not used to soften the verdict)

- The m = 2 phase fit is contaminated by the bar at late times (values
  near 90°, e.g. 88.0° at Q = 2.0/seed 11/t = 40, are bar-dominated);
  the t = 30 row, between bar formation and strong winding, is the
  cleanest and it is the flattest.
- Two seeds; a larger ensemble could tighten the per-cell scatter
  (±5–15° at strong amplitude) but cannot manufacture a monotone trend
  from a flat row.

## Consequence for the VI-a/VI-b merge

With D4b negative, VI-b's surviving quantitative content shrinks to the
azimuthal-averaging smoothness argument; the dispersion relation's
pitch–Q corollary joins the CBH-overtone mechanism (D3, M33/corotation/
multipole arguments) as falsified-as-written. The merged Paper VI should
carry pitch as a winding/shear observable, not a dispersion dial.

# SSV VI — Galactic Dynamics

Single merged galactic-dynamics paper, replacing the former **SSV VI-a**
(*Galactic Standing Waves and Flat Rotation Curves*) and **SSV VI-b**
(*Galactic Morphology as Overtone Structure*). The merge was executed under
issue [#131](https://github.com/StigNorland/SVT/issues/131) after both
papers' central-black-hole mechanisms were falsified (#122: the flat-curve
amplitude is fitted, not predicted; #124: arms need no black hole — swing
amplification of the self-gravitating baryons supersedes the overtone
model).

Architecture of the merged paper: time-dilation-gradient framework
(v² = r dΦ/dr) + the measured intrinsic two-term defect source (#119
H7a/H8; core + circulation halo → ln r flat tail) + real-gravity N-body
phenomenology (#124 D1–D3, maximal-disc balance condition). The retired
mechanisms are kept as the falsification-record appendix (programme
rule 1); the full retired texts live in git history (commit `cc59d19` and
earlier, `papers/SSV-VI-a/`, `papers/SSV-VI-b/`).

- `main.tex` — the paper. Build: 2× `pdflatex main.tex` (after
  `python instruments/tools/gen_provenance.py SSV-VI`).
- `figures/`, `results/`, `data/` — consolidated from both former papers.
- Supporting computation: `instruments/paper_vi_a/` (rotation curve),
  `instruments/paper_vi_b/` (N-body disc); tests under
  `instruments/test/paper_vi_a|b/`.

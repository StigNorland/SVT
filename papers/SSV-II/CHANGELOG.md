# SSV-II — change record

The paper states **current status only**. Its history lives here.

---

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

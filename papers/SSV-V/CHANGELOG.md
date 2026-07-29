# SSV-V — change record

The paper states **current status only**. Its history lives here.

---

## 2026-07-29 — [#207](https://github.com/StigNorland/SVT/issues/207) · change records moved out of the paper

One passage of edit history removed from `main.tex` and recorded below.

## 2026-07 — [#187](https://github.com/StigNorland/SVT/issues/187) · the chemical-potential floor reverses

Machine-checked in `instruments/paper_v/ssv_v_remnant_audit_2026.py`.

Earlier versions argued remnant confinement from a **chemical-potential
floor**: they wrote `mu = -b[ln(rho/rho_0) + 1]` and observed that it "diverges
to `+infinity` as `rho -> 0`". That used the sign of the potential Paper I has
since rejected ([#183](https://github.com/StigNorland/SVT/issues/183)).

On the adopted branch `mu -> -infinity` as `rho -> 0`. There is **no
chemical-potential floor**, and the original mechanism does not merely weaken —
it *reverses*.

**The mechanism was wrong; the result stands on a different footing.**
Confinement follows from the pressure gradient `Delta P = b(rho_0 - rho)`
rather than from a divergent `mu`, and that argument is what the paper now
carries.

## 2026-07 — [#187](https://github.com/StigNorland/SVT/issues/187) E2 · `b` declared

`b` is declared a **frequency** at `main.tex:146`. It is an energy-per-mass in
Paper I and an energy in Paper VII-a — one letter, three dimensions across the
series, which is the subject of
[#205](https://github.com/StigNorland/SVT/issues/205).

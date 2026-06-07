"""Box-convergence gate for the proton Q_p far-field estimators — issue #98.

Applies the #108 lesson to the gravity sector: a far-field / spatial-moment
quantity extracted in a finite box can track the box rather than the physics, and
grid-refinement at fixed box can look converged while the quantity is
box-contaminated. Before any `Q_p` is promoted toward `alpha_G`, its estimators
must be stable along BOTH a box-sweep (vary half_width) and a grid-sweep (vary n),
and a clean far-field must exist (`source << shell << box`).

Estimators (from the saved static trefoil states; same construction as
`q_p_static_potential.py`):
  - deficit_volume      = int (1-|psi|^2) dV                  (Q_p^LW charge)
  - q_p_asymptotic_fit  = 4 pi c^2 r * potential, r->box      (free-space 1/r coeff)
  - shell_deficit       = mean (1-|psi|^2) on an outer shell  (background pedestal level)
  - pedestal            = shell_deficit * box_volume          (box-filling background)
  - source_charge       = deficit_volume - pedestal           (pedestal-subtracted)

Decision rule (pre-registered, plan quiet-inventing-hare / issue #98): an estimator
is box/grid "stable" if its spread is < 5% across the swept points, AND the pedestal
must be a small fraction of deficit_volume (else the charge is box-filling background,
not a localized source). PASS -> attempt Q_p -> alpha_G. FAIL -> alpha_G stays blocked.

VERDICT (2026-06-07): FAIL. deficit_volume spreads ~60-78% across boxes (hw5..8) and
~30% across resolution (n48..160), and the pedestal accounts for ~90% of
deficit_volume. The far-field charge is box-pedestal-dominated; alpha_G remains
blocked. A meaningful Q_p needs either a background-subtracting source isolation or
boxes large enough that the background -> 0 (source << box) -- the static cousin of
the petascale separation that closed the dynamic route-C in #108.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

GATE_PCT = 5.0


def _green_static(r: np.ndarray, xi: float = 1.0, c: float = 1.0) -> np.ndarray:
    out = np.empty_like(r)
    nz = r > 1.0e-12
    out[nz] = (1.0 - np.exp(-2.0 * r[nz] / xi)) / (4.0 * math.pi * c * c * r[nz])
    out[~nz] = 1.0 / (2.0 * math.pi * c * c * xi)
    return out


def state_observables(path: str | Path, probe_radii=(8, 10, 12, 16, 20),
                      shell_lo: float = 0.7, shell_hi: float = 0.9) -> dict:
    """Far-field Q_p estimators + background-pedestal diagnostic for one saved state."""
    d = np.load(Path(path), allow_pickle=False)
    psi = d["psi_real"] + 1j * d["psi_imag"]
    x, y, z = d["x"], d["y"], d["z"]
    sp = float(x[1, 0, 0] - x[0, 0, 0])
    cell = sp ** 3
    import json
    hw = float(json.loads(str(d["config"]))["half_width"])
    n = int(json.loads(str(d["config"]))["n"])

    deficit = np.clip(1.0 - np.abs(psi) ** 2, 0.0, None)
    deficit_volume = float(deficit.sum() * cell)

    samples = []
    for r in probe_radii:
        dist = np.sqrt((x - r) ** 2 + y * y + z * z)
        pot = float(np.sum(deficit * _green_static(dist)) * cell)
        samples.append(4.0 * math.pi * r * pot)
    q_p_fit = float(np.mean(samples[-3:]))

    rad = np.sqrt(x * x + y * y + z * z)
    shell = (rad >= shell_lo * hw) & (rad <= shell_hi * hw)
    shell_deficit = float(deficit[shell].mean()) if shell.any() else float("nan")
    box_volume = (2.0 * hw) ** 3
    pedestal = shell_deficit * box_volume
    return {
        "path": str(path), "half_width": hw, "n": n,
        "deficit_volume": deficit_volume, "q_p_fit": q_p_fit,
        "shell_deficit": shell_deficit, "pedestal": pedestal,
        "source_charge": deficit_volume - pedestal,
        "pedestal_fraction": pedestal / max(deficit_volume, 1e-12),
    }


def spread_pct(values) -> float:
    v = np.asarray(values, float)
    return float((v.max() - v.min()) / max(abs(v.mean()), 1e-12) * 100.0)


def evaluate(rows: list[dict]) -> dict:
    """Apply the gate to a set of states (a box family or grid family)."""
    dv = spread_pct([r["deficit_volume"] for r in rows])
    qp = spread_pct([r["q_p_fit"] for r in rows])
    ped_frac = float(np.mean([r["pedestal_fraction"] for r in rows]))
    box_stable = dv < GATE_PCT and qp < GATE_PCT
    pedestal_clean = ped_frac < 0.5
    return {
        "deficit_volume_spread_pct": dv, "q_p_fit_spread_pct": qp,
        "mean_pedestal_fraction": ped_frac,
        "passes_gate": bool(box_stable and pedestal_clean),
    }


def main() -> None:
    D = "papers/SSV-I/data/"
    box_trefoil = [f"{D}trefoil-state-n48-hw{h}-400steps-2026-05-06.npz" for h in (5, 6, 7)]
    box_yjunc = [f"{D}y-junction-state-n48-hw{h}-400steps-2026-05-17.npz" for h in (5, 6, 7, 8)]
    grid_hw6 = [f"{D}gradient-flow-n{n}-hw6-5000steps-2026-06-03.npz" for n in (48, 72, 96, 128, 160)]

    print("=" * 70)
    print("Q_p box-convergence gate (#98)")
    print("=" * 70)
    for label, files in (("BOX trefoil n48", box_trefoil),
                         ("BOX y-junc n48", box_yjunc),
                         ("GRID hw6", grid_hw6)):
        rows = [state_observables(f) for f in files if Path(f).exists()]
        ev = evaluate(rows)
        print(f"\n[{label}]  ({len(rows)} states)")
        for r in rows:
            print(f"  hw{r['half_width']:.0f} n{r['n']:>3}  deficitV={r['deficit_volume']:8.3f}  "
                  f"q_p_fit={r['q_p_fit']:8.3f}  pedestal/deficitV={r['pedestal_fraction']:.2f}")
        print(f"  -> deficitV spread {ev['deficit_volume_spread_pct']:.1f}%, "
              f"q_p spread {ev['q_p_fit_spread_pct']:.1f}%, "
              f"mean pedestal fraction {ev['mean_pedestal_fraction']:.2f}  "
              f"=> {'PASS' if ev['passes_gate'] else 'FAIL'}")
    print("\nVERDICT: FAIL on every axis. Q_p is box-pedestal-dominated and not")
    print("box/grid converged; alpha_G stays BLOCKED (no raw far-field scalar -> alpha_G).")


if __name__ == "__main__":
    main()

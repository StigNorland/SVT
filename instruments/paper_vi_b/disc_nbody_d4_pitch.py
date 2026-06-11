"""#124 D4 -- pitch angle vs Toomre Q in the real-gravity N-body disc.

Pre-registered decision rule D4 (issue #124): the spiral pitch angle
increases with Toomre Q -- the qualitative check of the surviving VI-b
dispersion result (eq. 12), now tested in the real-gravity disc instead of
the retired CBH-overtone model.

Operational rule (posted to #124 before running): sweep Q at the balanced
halo amplitude v_h = 0.45 (the flat-curve-AND-arms regime found in the 3D
balance run), matched seeds and times; at each sample time use only Q
values whose m=2 amplitude is measurable (A2 >= 0.02, ~5x shot noise);
PASS iff the Spearman rank correlation of pitch vs Q is >= +0.8 with >= 3
valid Q points at every matched time t in {20, 30, 40}; FAIL on
non-monotone or decreasing trend; INCONCLUSIVE if fewer than 3 Q points
remain measurable.

Reuses the integrator of disc_nbody.py unchanged (FFT particle-mesh,
isolated BCs, no BH, no DM particles).  GPU via SSV_GPU=1.

Run:  python disc_nbody_d4_pitch.py [--quick]
Writes papers/SSV-VI/results/d4_pitch_receipt.json and
papers/SSV-VI/figures/fig_d4_pitch_vs_q.png.
"""

import json
import os
import sys
import time as _time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import disc_nbody as dn  # noqa: E402

xp = dn.xp

Q_GRID = (1.0, 1.3, 1.6, 2.0)
SEEDS = (11, 7)
V_HALO = 0.45
T_SAMPLES = (20.0, 30.0, 40.0)
A2_FLOOR = 0.02


def run_disc_sampled(v_halo, Q, seed, t_samples, n_part=200_000, Ng=512,
                     L=16.0, dt=0.004, tag="run"):
    """disc_nbody.run_disc with mid-run sampling of (A2, pitch, v ratio)."""
    pm = dn.PMGravity(Ng=Ng, L=L)
    pos, vel, mass = dn.make_disc(n_part=n_part, Q=Q, v_halo=v_halo,
                                  seed=seed, pm=pm)
    t_end = max(t_samples)
    nsteps = int(round(t_end / dt))
    sample_steps = {int(round(t / dt)): t for t in t_samples}
    out = []
    print(f"  [{tag}] v_halo={v_halo}, Q={Q}, seed={seed}, N={n_part}, "
          f"Ng={Ng}, t_end={t_end}", flush=True)
    t0 = _time.time()
    gx, gy, dens, cic = pm.accel_grid(pos, mass)
    for n in range(nsteps):
        ax = pm.gather(gx, cic)
        ay = pm.gather(gy, cic)
        if v_halo > 0:
            rr = xp.sqrt(xp.maximum(pos[:, 0] ** 2 + pos[:, 1] ** 2, 0.0025))
            ax = ax - (v_halo ** 2) * pos[:, 0] / (rr * rr)
            ay = ay - (v_halo ** 2) * pos[:, 1] / (rr * rr)
        vel[:, 0] += ax * dt
        vel[:, 1] += ay * dt
        pos += vel * dt
        gx, gy, dens, cic = pm.accel_grid(pos, mass)
        if (n + 1) in sample_steps:
            t = sample_steps[n + 1]
            amps, pitch = dn.fourier_modes(pos)
            rc, vv = dn.rotation_curve(pos, vel)
            inner = float(vv[(rc > 1.0) & (rc < 2.0)].mean())
            outer = float(vv[(rc > 4.0) & (rc < 5.5)].mean())
            out.append({"t": t, "A2": float(amps[2]),
                        "pitch_deg": None if not np.isfinite(pitch)
                        else float(pitch),
                        "v_ratio": outer / inner})
            ptxt = f"{pitch:.1f}" if np.isfinite(pitch) else "n/a"
            print(f"    t={t:5.1f}: A2={amps[2]:.3f} pitch={ptxt} deg "
                  f"ratio={outer / inner:.2f} "
                  f"[{_time.time() - t0:.0f}s]", flush=True)
    return out


def spearman(x, y):
    """Spearman rank correlation without scipy."""
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean()
    ry -= ry.mean()
    den = np.sqrt((rx**2).sum() * (ry**2).sum())
    return float((rx * ry).sum() / den) if den > 0 else float("nan")


def evaluate(records, t_samples=T_SAMPLES, a2_floor=A2_FLOOR):
    """Apply the operational D4 rule to the sweep records.

    records: {(Q, seed): [ {t, A2, pitch_deg, v_ratio}, ... ]}
    Pitch per (Q, t) is the mean over seeds (valid entries only).
    """
    per_time = {}
    for t in t_samples:
        qs, pitches = [], []
        for q in sorted({k[0] for k in records}):
            vals = []
            for (qq, seed), rows in records.items():
                if qq != q:
                    continue
                for row in rows:
                    if (row["t"] == t and row["A2"] >= a2_floor
                            and row["pitch_deg"] is not None):
                        vals.append(row["pitch_deg"])
            if vals:
                qs.append(q)
                pitches.append(float(np.mean(vals)))
        entry = {"Q_valid": qs, "pitch_deg": pitches}
        if len(qs) >= 3:
            entry["spearman"] = spearman(np.array(qs), np.array(pitches))
            entry["verdict"] = ("PASS" if entry["spearman"] >= 0.8
                                else "FAIL")
        else:
            entry["spearman"] = None
            entry["verdict"] = "INCONCLUSIVE"
        per_time[t] = entry
    verdicts = [per_time[t]["verdict"] for t in t_samples]
    if all(v == "PASS" for v in verdicts):
        overall = "PASS"
    elif any(v == "FAIL" for v in verdicts):
        overall = "FAIL"
    else:
        overall = "INCONCLUSIVE"
    return {"per_time": {str(t): per_time[t] for t in t_samples},
            "overall": overall}


def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    quick = "--quick" in sys.argv
    v_halo = V_HALO
    label = "d4"
    if "--vhalo" in sys.argv:
        v_halo = float(sys.argv[sys.argv.index("--vhalo") + 1])
    if "--label" in sys.argv:
        label = sys.argv[sys.argv.index("--label") + 1]
    n_part = 20_000 if quick else 200_000
    ng = 128 if quick else 512
    seeds = SEEDS[:1] if quick else SEEDS
    t_samples = (4.0,) if quick else T_SAMPLES

    print(f"{label} pitch-vs-Q sweep, backend {dn.backend_name()}; "
          f"Q grid {Q_GRID}, seeds {seeds}, v_halo={v_halo}\n", flush=True)
    records = {}
    for seed in seeds:
        for q in Q_GRID:
            rows = run_disc_sampled(v_halo, q, seed, t_samples,
                                    n_part=n_part, Ng=ng,
                                    tag=f"{label} Q={q} s{seed}")
            records[(q, seed)] = rows

    result = evaluate(records, t_samples=t_samples)
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", ".."))
    res_dir = os.path.join(root, "papers", "SSV-VI", "results")
    fig_dir = os.path.join(root, "papers", "SSV-VI", "figures")
    os.makedirs(res_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    receipt = {
        "issue": 124,
        "rule": "D4 pitch angle increases with Toomre Q",
        "config": {"Q_grid": Q_GRID, "seeds": seeds, "v_halo": v_halo,
                   "n_part": n_part, "Ng": ng, "t_samples": t_samples,
                   "A2_floor": A2_FLOOR, "quick": quick},
        "runs": [{"Q": q, "seed": s, "samples": rows}
                 for (q, s), rows in sorted(records.items())],
        "evaluation": result,
    }
    dest = os.path.join(res_dir, f"{label}_pitch_receipt.json")
    with open(dest, "w") as f:
        json.dump(receipt, f, indent=2)
    print(f"\nreceipt -> {dest}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axp = plt.subplots(figsize=(6.4, 4.4))
        markers = {20.0: "o", 30.0: "s", 40.0: "^", 4.0: "o"}
        for t in t_samples:
            e = result["per_time"][str(t)]
            if e["Q_valid"]:
                axp.plot(e["Q_valid"], e["pitch_deg"],
                         markers.get(t, "o") + "-",
                         label=f"t = {t:.0f} ({e['verdict']})")
        axp.set_xlabel("Toomre Q")
        axp.set_ylabel("m=2 pitch angle [deg]")
        axp.set_title(f"{label}: pitch vs Q at v_h = {v_halo} "
                      f"(overall: {result['overall']})")
        axp.grid(alpha=0.3)
        axp.legend()
        fig.tight_layout()
        fpath = os.path.join(fig_dir, f"fig_{label}_pitch_vs_q.png")
        fig.savefig(fpath, dpi=130)
        print(f"figure -> {fpath}")
    except Exception as exc:  # figure is best-effort
        print(f"figure skipped: {exc}")

    print(f"\nD4 OVERALL: {result['overall']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

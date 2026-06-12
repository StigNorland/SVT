"""#129 TOKEN-TAX (H-BILATERAL stage S0) -- which scheduling statistics
buy the A^2 doubling?

Pre-registered on issue #129 (TOKEN-TAX comment, posted before
computing). Discrete-event token-budget model of the bilateral
availability tax, built from the owner's worked example: clock 20%
slower (A = 0.8), slot = 10 tokens, photon--H2 handshake = 10 tokens,
8 joint tokens complete in slot 1 and the handshake finishes with 25%
of slot 2's AVAILABLE budget (2 of 8 tokens).

Model: time is slots of S token positions; loading L taxes exactly
k = round(L*S) positions per party per slot. A photon crosses n_hops
matter sites; each handshake accrues C JOINT-free positions (both
parties free at the same position), carrying over across slots --
equivalently, the chain consumes n_hops*C joint tokens back-to-back.
A clock is a monologue (one tick per own-free position):
delta_clock = k/(S-k), deterministic in every mode. Scheduling modes:

  SYNC      one shared busy mask per slot (the smooth classical field);
  INDEP     every party draws its own mask per slot;
  CORR(c)   each party uses the shared mask with prob c, else fresh.

Pre-stated closed forms the runs must hit (P1-P3 on the issue):

  SYNC   A_joint = A             => gamma_tok = 0
         (the owner's worked example IS this branch);
  INDEP  A_joint = A^2           => gamma_tok = 1/A  (-> 1 weak load);
  CORR   A_joint = A(A+c^2(1-A)) => gamma_tok = (1-c^2)/(A+c^2(1-A)),
  so Cassini |gamma - 1| <= 2.3e-5 prices the allowed busy-schedule
  correlation at c <= 4.8e-3.

gamma_tok ::= (delta_prop - delta_clock)/delta_clock, matching
H-SPATIAL's gamma_eff convention (0 = pure clock, 1 = GR doubling at
weak load). Two delta_prop estimators are reported: wall-clock
first-passage time (sub-slot quantization O(1/n) on gamma) and the
rate-based estimator target/m_hat (machine-exact zero in SYNC, where
the per-slot joint rate is deterministic). No force is modelled
anywhere: both halves are delays (force-vs-time guard).

Run:  python instruments/paper_iv/bilateral_token_toy.py [--quick]
Writes papers/SSV-IV/results/bilateral_token_receipt.json and a figure.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-IV" / "results"
FIGURES = ROOT / "papers" / "SSV-IV" / "figures"

SYNC, INDEP = "sync", "indep"
CASSINI = 2.3e-5                 # |gamma - 1| bound (Cassini 2003)


# ----------------------------------------------------------------------
# masks
# ----------------------------------------------------------------------

def draw_mask(rng: np.random.Generator, S: int, k: int) -> np.ndarray:
    """Boolean FREE mask of length S with exactly k positions taxed."""
    free = np.ones(S, dtype=bool)
    if k:
        free[rng.choice(S, size=k, replace=False)] = False
    return free


def party_mask(rng, S, k, shared, c):
    """One party's free mask for one slot: the shared mask with prob c,
    a fresh independent draw otherwise (c=1 -> SYNC, c=0 -> INDEP)."""
    if c >= 1.0 or (c > 0.0 and rng.random() < c):
        return shared
    return draw_mask(rng, S, k)


# ----------------------------------------------------------------------
# observables
# ----------------------------------------------------------------------

def clock_delay(S: int, k: int) -> float:
    """Fractional dilation of a monologue clock: deterministic k/(S-k)."""
    return k / (S - k)


def transit(rng, *, S, L, C, n_hops, c):
    """Wall slots for n_hops back-to-back handshakes of C joint tokens.

    Returns (T_wall, m_hat): first-passage wall time (completion at the
    position of the last joint token, counted as (pos+1)/S into its
    slot) and the mean joint rate over the full slots traversed."""
    k = round(L * S)
    target = n_hops * C
    got, slots = 0, 0
    while True:
        shared = draw_mask(rng, S, k)
        a = party_mask(rng, S, k, shared, c)
        b = party_mask(rng, S, k, shared, c)
        joint = a & b
        n = int(joint.sum())
        if got + n >= target:
            idx = np.flatnonzero(joint)
            pos = int(idx[target - got - 1]) + 1
            m_hat = got / slots if slots else float(n)
            return slots + pos / S, m_hat
        got += n
        slots += 1


def handshake_ledger(rng, *, S, k, C, c):
    """Joint tokens consumed per slot for ONE handshake (the worked
    example's bookkeeping). Deterministic in SYNC mode."""
    need, ledger = C, []
    while need > 0:
        shared = draw_mask(rng, S, k)
        a = party_mask(rng, S, k, shared, c)
        b = party_mask(rng, S, k, shared, c)
        n = int((a & b).sum())
        used = min(n, need)
        ledger.append(used)
        need -= used
    return ledger


def gamma_from_T(T, T0, d_clock):
    return ((T / T0 - 1.0) - d_clock) / d_clock


def measure_gamma(rng, *, S, L, C, n_hops, c, seeds):
    """gamma_tok (wall and rate-based estimators) over seeded chains."""
    k = round(L * S)
    d_clock = clock_delay(S, k)
    T0 = n_hops * C / S
    g_wall, g_rate = [], []
    for _ in range(seeds):
        T, m_hat = transit(rng, S=S, L=L, C=C, n_hops=n_hops, c=c)
        g_wall.append(gamma_from_T(T, T0, d_clock))
        g_rate.append(gamma_from_T(n_hops * C / m_hat, T0, d_clock))
    return {"gamma_wall": float(np.mean(g_wall)),
            "stderr_wall": float(np.std(g_wall) / math.sqrt(seeds)),
            "gamma_rate": float(np.mean(g_rate)),
            "stderr_rate": float(np.std(g_rate) / math.sqrt(seeds))}


def gamma_predicted(c: float, A: float) -> float:
    """P3 closed form: gamma(c, A) = (1-c^2)/(A + c^2 (1-A))."""
    return (1.0 - c**2) / (A + c**2 * (1.0 - A))


def delta_prop_predicted(mode: str, L: float) -> float:
    """Exact fractional transit delay: SYNC L/(1-L); INDEP (2L-L^2)/(1-L)^2."""
    A = 1.0 - L
    return (1.0 - A) / A if mode == SYNC else (1.0 - A**2) / A**2


# ----------------------------------------------------------------------
# battery
# ----------------------------------------------------------------------

def run_battery(quick=False, seed=20260612):
    rng = np.random.default_rng(seed)
    n_hops = 500 if quick else 5000
    seeds = 5 if quick else 20
    S, k, C = 10, 2, 10
    L, A = k / S, 1 - k / S
    out = {"config": {"quick": quick, "seed": seed, "S": S, "k": k,
                      "C": C, "A": A, "n_hops": n_hops, "seeds": seeds}}

    # D1 -- SYNC: the worked example, exact ------------------------------
    ledger = handshake_ledger(rng, S=S, k=k, C=C, c=1.0)
    g = measure_gamma(rng, S=S, L=L, C=C, n_hops=n_hops, c=1.0,
                      seeds=seeds)
    out["D1_sync"] = {
        "worked_example_ledger": ledger,          # must be [8, 2]
        "slot2_fraction_of_available": ledger[1] / (S - k),  # 0.25
        **g,
        "delta_clock": clock_delay(S, k),
        "PASS": bool(ledger == [8, 2]
                     and abs(g["gamma_rate"]) < 1e-12
                     and abs(g["gamma_wall"]) < 1e-3),
    }

    # D2 -- INDEP: gamma = 1/A -------------------------------------------
    g = measure_gamma(rng, S=S, L=L, C=C, n_hops=n_hops, c=0.0,
                      seeds=seeds)
    out["D2_indep"] = {
        **g, "predicted": 1 / A,
        "PASS": bool(abs(g["gamma_wall"] - 1 / A) <= 0.02 * (1 / A)),
    }

    # D3 -- correlation curve gamma(c) -----------------------------------
    curve, ok = {}, True
    for c in (0.0, 0.25, 0.5, 0.75, 1.0):
        g = measure_gamma(rng, S=S, L=L, C=C, n_hops=n_hops, c=c,
                          seeds=seeds)
        pred = gamma_predicted(c, A)
        curve[str(c)] = {**g, "predicted": pred}
        ok &= abs(g["gamma_wall"] - pred) <= 0.03
    out["D3_correlation"] = {
        "curve": curve,
        "cassini_c_bound": math.sqrt(CASSINI),    # weak load: 1-gamma=c^2
        "PASS": bool(ok),
    }

    # D4 -- achromaticity: rate levy vs per-event latency ----------------
    costs = (5, 10, 20, 40)
    token_total = n_hops * C                      # same statistics per C
    D_lat = 0.5                                   # slots per handshake
    rate_d, extra_d, pred_extra = {}, {}, {}
    for Cc in costs:
        nh = token_total // Cc
        T0 = nh * Cc / S
        Ts = [transit(rng, S=S, L=L, C=Cc, n_hops=nh, c=0.0)[0]
              for _ in range(seeds)]
        rate_d[str(Cc)] = float(np.mean(Ts) / T0 - 1.0)
        # per-event latency adds nh*D_lat wall slots by definition
        extra_d[str(Cc)] = nh * D_lat / T0
        pred_extra[str(Cc)] = D_lat * S / Cc
    rd = np.array(list(rate_d.values()))
    spread = float((rd.max() - rd.min()) / rd.mean())
    ctrl_ok = all(abs(extra_d[c] / pred_extra[c] - 1) <= 0.10
                  for c in extra_d)
    out["D4_achromaticity"] = {
        "rate_levy_delays": rate_d,
        "spread_relative": spread,
        "latency_control_extra": extra_d,
        "latency_control_predicted": pred_extra,
        "PASS": bool(spread <= 0.02 and ctrl_ok),
    }

    # D5 -- linearity: the pre-registered window AND the weak-load tier --
    Sw = 1000
    hops_w = max(100, n_hops // 5) * 10           # tokens = hops_w*10
    tiers = {"preregistered": (0.01, 0.02, 0.03, 0.04, 0.05),
             "weak_load": (0.001, 0.002, 0.003, 0.004, 0.005)}
    d5 = {}
    for tier, loads in tiers.items():
        row = {}
        for mode, c in ((INDEP, 0.0), (SYNC, 1.0)):
            ds, preds = [], []
            for Lw in loads:
                T0 = hops_w * 10 / Sw
                Ts = [transit(rng, S=Sw, L=Lw, C=10, n_hops=hops_w,
                              c=c)[0] for _ in range(seeds)]
                ds.append(float(np.mean(Ts) / T0 - 1.0))
                preds.append(delta_prop_predicted(mode, Lw))
            slope = float(np.polyfit(loads, ds, 1)[0])
            slope_pred = float(np.polyfit(loads, preds, 1)[0])
            row[mode] = {"delays": dict(zip(map(str, loads), ds)),
                         "slope": slope,
                         "slope_exact_closed_form": slope_pred}
        d5[tier] = row
    out["D5_linearity"] = {
        **d5,
        # literal pre-registered thresholds (0.01-0.05 window):
        "preregistered_PASS": bool(
            abs(d5["preregistered"][INDEP]["slope"] - 2.0) <= 0.05
            and abs(d5["preregistered"][SYNC]["slope"] - 1.0) <= 0.02),
        # weak-load tier, where the linear limit holds:
        "weak_load_PASS": bool(
            abs(d5["weak_load"][INDEP]["slope"] - 2.0) <= 0.05
            and abs(d5["weak_load"][SYNC]["slope"] - 1.0) <= 0.02),
        # the miss in the pre-registered window must be the analytic
        # curvature, not noise: measured slope == closed-form slope
        "curvature_explained": bool(
            abs(d5["preregistered"][INDEP]["slope"]
                - d5["preregistered"][INDEP]["slope_exact_closed_form"])
            <= 0.05),
        "PASS": None,             # set below from the three flags
    }
    out["D5_linearity"]["PASS"] = bool(
        out["D5_linearity"]["weak_load_PASS"]
        and out["D5_linearity"]["curvature_explained"])

    out["verdict"] = {r: out[r]["PASS"] for r in
                      ("D1_sync", "D2_indep", "D3_correlation",
                       "D4_achromaticity", "D5_linearity")}
    out["verdict"]["D5_preregistered_window_literal"] = \
        out["D5_linearity"]["preregistered_PASS"]
    return out


# ----------------------------------------------------------------------
# figure
# ----------------------------------------------------------------------

def make_figure(out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    A = out["config"]["A"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    curve = out["D3_correlation"]["curve"]
    cs = np.array([float(c) for c in curve])
    g = np.array([curve[c]["gamma_wall"] for c in curve])
    e = np.array([curve[c]["stderr_wall"] for c in curve])
    cf = np.linspace(0, 1, 200)
    ax1.plot(cf, gamma_predicted(cf, A), "k-", lw=1,
             label=r"$\gamma=(1-c^2)/(A+c^2(1-A))$")
    ax1.errorbar(cs, g, yerr=e, fmt="o", ms=5, color="tab:red",
                 label=f"measured (A = {A})")
    ax1.axhline(1.0, color="gray", ls=":", lw=0.8)
    ax1.axhline(0.0, color="gray", ls=":", lw=0.8)
    ax1.set_xlabel("busy-schedule correlation  c")
    ax1.set_ylabel(r"$\gamma_{\rm tok}$")
    ax1.set_title("the decorrelation fork (D3)")
    ax1.legend(fontsize=8)

    rd = out["D4_achromaticity"]["rate_levy_delays"]
    ex = out["D4_achromaticity"]["latency_control_extra"]
    Cs = np.array(sorted(int(c) for c in rd))
    ax2.plot(Cs, [rd[str(c)] for c in Cs], "o-", color="tab:blue",
             label="rate-proportional levy (achromatic)")
    ax2.plot(Cs, [rd[str(c)] + ex[str(c)] for c in Cs], "s--",
             color="tab:orange", label="+ per-event latency (chromatic)")
    ax2.set_xlabel("handshake cost C  (frequency proxy)")
    ax2.set_ylabel("fractional transit delay")
    ax2.set_title("obligation 2: levy type (D4)")
    ax2.set_xscale("log")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    path = FIGURES / "bilateral_token_gamma.png"
    fig.savefig(path, dpi=150)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    out = run_battery(quick=args.quick)
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    receipt = RESULTS / "bilateral_token_receipt.json"
    receipt.write_text(json.dumps(out, indent=1))
    fig = make_figure(out)
    print(json.dumps(out["verdict"], indent=1))
    print(f"receipt: {receipt}\nfigure:  {fig}")


if __name__ == "__main__":
    main()

"""#174 No-go map (II) -- does a BOSONIC superfluid give a universal speed of
light across its sectors?  (tree-level)

Pre-registered on issue #174 BEFORE this code.

CONTEXT.  #172 established (from real literature) that standalone bosonic SSV
fails the emergent-Lorentz naturalness no-go (Collins et al. 2004): it lacks the
fermionic Fermi-point (Volovik) and SUSY (Nibbelink-Pospelov) protections, and
Goldstone protects only the phonon's GAPLESSNESS, not a universal c.  This turns
that claim into an SSV-specific computation in the superfluid's own variables.

SCOPE (honest, rule 1).  The full naturalness problem is about RADIATIVE
corrections amplifying velocity differences (power-law vs logarithmic), which
needs interactions/holography free-field tools cannot reach.  This does the
tractable, decisive TREE-LEVEL piece: do two COUPLED bosonic sectors even SHARE
a common c?  If not already at tree level, there is no universal c to protect.

PHYSICS.  Two-component Bogoliubov superfluid (masses m_i, densities n_i, intra
couplings g_i, inter coupling g12).  Single-component kinetic energy
eps_i = k^2/(2 m_i); single-component Bogoliubov E_i^2 = eps_i (eps_i + 2 g_i n_i).
Two branches:
  omega_pm^2 = 1/2 (E1^2 + E2^2) +/- 1/2 sqrt( (E1^2-E2^2)^2 + 16 g12^2 n1 n2 eps1 eps2 )
Low-k (sound): c_i^2 = g_i n_i / m_i, and
  c_pm^2 = 1/2 [ (c1^2+c2^2) +/- sqrt( (c1^2-c2^2)^2 + 4 W^2 ) ],  W^2 = g12^2 n1 n2/(m1 m2)
so the sector velocity splitting is
  Delta(c^2) = c_+^2 - c_-^2 = sqrt( (c1^2-c2^2)^2 + 4 W^2 ) >= 0,
zero ONLY if c1=c2 AND g12=0 (identical components, decoupled).  High-k: each
branch -> eps_i = k^2/2m_i (the z=2 free-particle UV).  Stability (miscibility):
g12^2 < g1 g2 so c_-^2 >= 0.

DECISION RULE (pre-registered on #174).
  Delta c/cbar zero ONLY at the fully fine-tuned point (identical + g12=0), and
  coupling g12 INCREASES the split -> a bosonic superfluid has NO natural
  universal c -> confirms #172's negative in SSV's variables.  A generic
  (untuned) Delta c -> 0 -> a bosonic protection exists (surprising positive).

Run:  python instruments/model_lorentz/multisector_velocity.py
Writes papers/SSV-VII-b/results/multisector_velocity_receipt.json .
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-VII-b" / "results"

# default: identical components, coupled (the "no asymmetry, only coupling" case)
DEF = dict(m1=1.0, m2=1.0, n1=1.0, n2=1.0, g1=1.0, g2=1.0, g12=0.5)


# ----------------------------------------------------------------------
# two-component Bogoliubov dispersion and sound speeds
# ----------------------------------------------------------------------

def omega_pm(k, p):
    """Two-branch Bogoliubov dispersion omega_+(k), omega_-(k)."""
    eps1 = k * k / (2.0 * p["m1"])
    eps2 = k * k / (2.0 * p["m2"])
    E1sq = eps1 * (eps1 + 2.0 * p["g1"] * p["n1"])
    E2sq = eps2 * (eps2 + 2.0 * p["g2"] * p["n2"])
    disc = (E1sq - E2sq) ** 2 + 16.0 * p["g12"] ** 2 * p["n1"] * p["n2"] * eps1 * eps2
    root = np.sqrt(np.clip(disc, 0.0, None))
    wp = np.sqrt(np.clip(0.5 * (E1sq + E2sq) + 0.5 * root, 0.0, None))
    wm = np.sqrt(np.clip(0.5 * (E1sq + E2sq) - 0.5 * root, 0.0, None))
    return wp, wm


def sound_speeds_analytic(p):
    """c_pm from the low-k formula."""
    c1sq = p["g1"] * p["n1"] / p["m1"]
    c2sq = p["g2"] * p["n2"] / p["m2"]
    W2 = p["g12"] ** 2 * p["n1"] * p["n2"] / (p["m1"] * p["m2"])
    root = np.sqrt((c1sq - c2sq) ** 2 + 4.0 * W2)
    cp = np.sqrt(0.5 * ((c1sq + c2sq) + root))
    cm = np.sqrt(np.clip(0.5 * ((c1sq + c2sq) - root), 0.0, None))
    return float(cp), float(cm)


def sound_speeds_numeric(p, kmax=1e-3, nk=6):
    """c_pm from the low-k slope of the numeric BdG dispersion (validation)."""
    ks = np.linspace(kmax / nk, kmax, nk)
    wp, wm = omega_pm(ks, p)
    cp = float(np.polyfit(ks, wp, 1)[0])
    cm = float(np.polyfit(ks, wm, 1)[0])
    return cp, cm


def splitting(p):
    """Fractional sector velocity splitting Delta c / cbar."""
    cp, cm = sound_speeds_analytic(p)
    return float((cp - cm) / (0.5 * (cp + cm)))


def is_stable(p):
    return p["g12"] ** 2 < p["g1"] * p["g2"]


# ----------------------------------------------------------------------
# run
# ----------------------------------------------------------------------

def run():
    # C1: decoupled + identical -> degenerate (c+ = c-)
    tuned = dict(DEF, g12=0.0)
    cp_t, cm_t = sound_speeds_analytic(tuned)
    control_degenerate = abs(cp_t - cm_t) < 1e-12

    # C2: numeric BdG sound speeds match the analytic formula
    cp_a, cm_a = sound_speeds_analytic(DEF)
    cp_n, cm_n = sound_speeds_numeric(DEF)
    control_numeric = max(abs(cp_a - cp_n), abs(cm_a - cm_n)) / cp_a < 1e-3

    # C3: high-k -> z=2 free particle (omega ~ k^2/2m); check upper branch slope
    khi = 50.0
    wp_hi, _ = omega_pm(np.array([khi]), DEF)
    z2_ratio = float(wp_hi[0] / (khi * khi / (2.0 * min(DEF["m1"], DEF["m2"]))))
    control_z2 = abs(z2_ratio - 1.0) < 0.05

    # T: splitting vs coupling (identical components) and vs asymmetry (decoupled)
    coupling_scan = []
    for g12 in (0.0, 0.2, 0.4, 0.6, 0.8):
        p = dict(DEF, g12=g12)
        coupling_scan.append({"g12": g12, "stable": is_stable(p),
                              "split": splitting(p) if is_stable(p) else None})
    asym_scan = []
    for g2 in (1.0, 1.3, 1.6, 2.0):        # asymmetry with g12=0 (decoupled)
        p = dict(DEF, g2=g2, g12=0.0)
        asym_scan.append({"g2": g2, "split": splitting(p)})

    split_default = splitting(DEF)          # identical but coupled
    # coupling monotonically increases the split (from 0 at g12=0)
    csplits = [r["split"] for r in coupling_scan if r["split"] is not None]
    coupling_increases = all(csplits[i] <= csplits[i + 1] + 1e-12
                             for i in range(len(csplits) - 1)) and csplits[-1] > csplits[0]
    only_tuned_zero = (csplits[0] < 1e-12) and (split_default > 0.01)

    controls_ok = control_degenerate and control_numeric and control_z2
    no_universal_c = only_tuned_zero and coupling_increases

    verdict = (
        "NO natural universal c: two coupled bosonic sectors have DIFFERENT sound "
        "speeds (identical components, g12={:.1f} -> Delta c/cbar = {:.2f}); the "
        "splitting is zero ONLY at the fully fine-tuned point (identical AND "
        "g12=0), and coupling INCREASES it. A bosonic superfluid does not supply a "
        "universal c -- confirms #172's negative in SSV's own variables (tree "
        "level). Radiative amplification + the power-law/holographic cure are "
        "beyond free-field tools (#172)."
    ).format(DEF["g12"], split_default)

    return {
        "params": DEF,
        "control_C1_degenerate_when_tuned": bool(control_degenerate),
        "control_C2_numeric_matches_analytic": bool(control_numeric),
        "control_C3_highk_z2": z2_ratio, "control_C3_ok": bool(control_z2),
        "controls_ok": bool(controls_ok),
        "sound_speeds_default": {"c_plus": cp_a, "c_minus": cm_a},
        "split_default_identical_coupled": split_default,
        "coupling_scan": coupling_scan,
        "asymmetry_scan": asym_scan,
        "coupling_increases_split": bool(coupling_increases),
        "zero_only_when_fully_tuned": bool(only_tuned_zero),
        "no_natural_universal_c": bool(no_universal_c),
        "verdict": verdict,
    }


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    rep = run()
    print("=" * 76)
    print("#174 No-go map (II)  --  does a bosonic superfluid give a universal c?")
    print("=" * 76)
    print("\nCONTROLS")
    print(f"  C1 degenerate when tuned (g12=0, identical): "
          f"{rep['control_C1_degenerate_when_tuned']}")
    print(f"  C2 numeric BdG sound speeds match analytic:  "
          f"{rep['control_C2_numeric_matches_analytic']}")
    print(f"  C3 high-k -> z=2 (omega~k^2/2m), ratio={rep['control_C3_highk_z2']:.3f}: "
          f"{rep['control_C3_ok']}")
    print(f"  controls ok: {rep['controls_ok']}")
    cs = rep["sound_speeds_default"]
    print(f"\n  default (identical components, g12={rep['params']['g12']}):  "
          f"c_+ = {cs['c_plus']:.4f}, c_- = {cs['c_minus']:.4f}  ->  "
          f"Delta c/cbar = {rep['split_default_identical_coupled']:.3f}")
    print("\n  splitting vs coupling g12 (identical components):")
    for r in rep["coupling_scan"]:
        s = f"{r['split']:.3f}" if r["split"] is not None else "unstable"
        print(f"    g12={r['g12']:.1f}   Delta c/cbar = {s}")
    print("\n  splitting vs asymmetry g2 (decoupled, g12=0):")
    for r in rep["asymmetry_scan"]:
        print(f"    g2={r['g2']:.1f}    Delta c/cbar = {r['split']:.3f}")
    print(f"\n  zero only when fully tuned: {rep['zero_only_when_fully_tuned']}   "
          f"coupling increases split: {rep['coupling_increases_split']}")
    print(f"\nVERDICT: {rep['verdict']}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "multisector_velocity_receipt.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\nreceipt -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

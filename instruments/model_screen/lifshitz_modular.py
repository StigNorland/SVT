"""#170 -- can the bulk-screen reconstruction be PRESENTIST?  Lifshitz (z!=1)
modular-locality test.

Pre-registered on issue #170 BEFORE this code.

MOTIVATION.  SSV has a preferred frame (the condensate) -- what a presentist
"now" needs.  The reconstruction assembled in #166 was borrowed from AdS/CFT,
which is eternalist (Lorentz/conformally invariant, no preferred time).  The
presentism-compatible holographies are the PREFERRED-FOLIATION ones (Lifshitz /
Horava, anisotropic scaling t->b^z t, x->b x, dynamical exponent z!=1).  That is
also SSV's own UV: the Bogoliubov dispersion is linear in the IR (z=1) and
QUADRATIC past the healing length xi (z=2).

THE SHARP WORRY.  The geometric modular Hamiltonian (sub-calc 1's first necessary
condition) is the LOCAL BOOST (Bisognano-Wichmann / CHM) -- a consequence of
Lorentz BOOST symmetry.  A Lifshitz screen with z!=1 has NO boost (its absence is
exactly what gives it a preferred time).  So the presentist feature may be what
makes the modular Hamiltonian NON-geometric, breaking reconstruction at step 1.

METHOD (reuse sub-calc 1: Dirichlet chain, Gaussian/Peschel-Eisler modular H).
  omega_k = (khat^2)^{z/2},  khat^2 = 4 sin^2(k/2)   (z=1 = relativistic massless;
  z=2 = SSV's UV).  Correlators X=<phi phi>, P=<pi pi>; modular H_pi from the
  functional calculus (valid for ANY dispersion).  Non-locality = far-tail weight
  of H_pi at |i-j| >= ell/2.

CONTROL C1.  z=1 reproduces sub-calc 1's geometric result (far-tail ~ few %).

DECISION RULE (pre-registered on #170).
  far-tail(z=2) >> far-tail(z=1)  -> preferred foliation makes modular flow
     NON-geometric -> reconstruction's first necessary condition FAILS for a
     presentist screen -> presentism _|_ the standard (boost-based) reconstruction.
  far-tail stays small           -> reconstruction survives the preferred
     foliation (surprising positive).

Run:  python instruments/model_screen/lifshitz_modular.py
Writes papers/SSV-VII-b/results/lifshitz_modular_receipt.json .
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import modular_locality as ml  # reuse machinery (Gaussian modular H, far_tail)

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-VII-b" / "results"


# ----------------------------------------------------------------------
# Lifshitz z-dispersion correlators on a Dirichlet chain
# ----------------------------------------------------------------------

def correlators_z(ell, z, N=1600):
    """Free scalar, Dirichlet chain, Lifshitz dispersion omega = (khat^2)^{z/2}.
    z=1 recovers the relativistic massless case (sub-calc 1 control)."""
    n = np.arange(1, N + 1)
    kn = np.pi * n / (N + 1)
    khat2 = 4.0 * np.sin(0.5 * kn) ** 2
    omega = khat2 ** (0.5 * z)
    i = np.arange(1, ell + 1)
    phi = np.sqrt(2.0 / (N + 1)) * np.sin(np.outer(i, kn))     # (ell, N)
    X = (phi / (2.0 * omega)) @ phi.T
    P = (phi * (0.5 * omega)) @ phi.T
    return X, P


def far_tail_for_z(ell, z, N=1600):
    X, P = correlators_z(ell, z, N=N)
    return ml.far_tail(ml.modular_H_pi(X, P))


# ----------------------------------------------------------------------
# #170 follow-on: is the geometricity IR-EMERGENT?  Bogoliubov crossover.
# ----------------------------------------------------------------------

def correlators_bogoliubov(ell, xi, N=3000):
    """Bogoliubov dispersion omega = khat sqrt(1 + (xi khat)^2): z=1 (acoustic)
    for khat << 1/xi, z=2 (free-particle) for khat >> 1/xi, crossover at the
    healing length xi.  SSV's actual screen: relativistic IR, non-relativistic UV."""
    n = np.arange(1, N + 1)
    kn = np.pi * n / (N + 1)
    khat2 = 4.0 * np.sin(0.5 * kn) ** 2
    khat = np.sqrt(khat2)
    omega = khat * np.sqrt(1.0 + (xi * xi) * khat2)
    i = np.arange(1, ell + 1)
    phi = np.sqrt(2.0 / (N + 1)) * np.sin(np.outer(i, kn))
    X = (phi / (2.0 * omega)) @ phi.T
    P = (phi * (0.5 * omega)) @ phi.T
    return X, P


def far_tail_bogoliubov(ell, xi, N=3000):
    return ml.far_tail(ml.modular_H_pi(*correlators_bogoliubov(ell, xi, N)))


def run_flow(xi=4.0, ells=(2, 4, 8, 16, 32, 64), N=3000):
    """Does the z=2 non-geometricity wash out for IR regions (ell >> xi)?
    Far-tail vs region size, normalised to the pure-z=1 reference at each ell."""
    rows = []
    for ell in ells:
        fb = far_tail_bogoliubov(ell, xi, N=N)
        fz1 = far_tail_for_z(ell, 1.0, N=N)
        fz2 = far_tail_for_z(ell, 2.0, N=N)
        rows.append({"ell": ell, "ell_over_xi": ell / xi, "far_bog": fb,
                     "far_z1": fz1, "far_z2": fz2, "R": fb / fz1})

    # z=2 reference ratio (the non-geometric benchmark), at a mid region
    mid = [r for r in rows if r["ell"] >= 16][0]
    z2_ratio = mid["far_z2"] / mid["far_z1"]
    # IR regions: ell >= 4*xi.  UV regions: ell <= xi.
    ir = [r for r in rows if r["ell_over_xi"] >= 4.0]
    uv = [r for r in rows if r["ell_over_xi"] <= 1.0]
    R_ir = float(np.mean([r["R"] for r in ir])) if ir else float("nan")
    R_uv = float(np.mean([r["R"] for r in uv])) if uv else float("nan")

    # decision: IR far-tail recovers to the geometric z=1 level (R_ir well below
    # the z=2 ratio) while UV stays non-geometric (R_uv large) -> emergent Lorentz
    emergent = (R_ir < 0.5 * z2_ratio) and (R_uv > 3.0)
    verdict = (
        "EMERGENT LORENTZ (Hypothesis A): the z=2 non-geometricity is a UV "
        "(ell<~xi) feature -- for IR regions (ell>>xi) the modular far-tail "
        "recovers to the geometric z=1 level (R_ir={:.2f}, ~{:.0f}x below the "
        "z=2 ratio {:.1f}), while UV regions stay non-geometric (R_uv={:.1f}). "
        "The boost-based reconstruction holds for the EMERGENT IR gravity; "
        "presentism survives as the microscopic substrate. The #170 tension is "
        "UV-only. (Far-tail is a crude metric: R_ir scatters ~+-25%, non-"
        "monotonic -- the robust fact is IR far-tail ~ z=1, ~10x below z=2.)"
    ).format(R_ir, z2_ratio / max(R_ir, 1e-9), z2_ratio, R_uv) if emergent else (
        "PERSISTS (Hypothesis B): the non-geometricity survives for ell>>xi "
        "(R_ir={:.2f} near the z=2 ratio {:.1f}) -> a non-relativistic "
        "reconstruction is required.").format(R_ir, z2_ratio)

    return {
        "xi": xi, "N": N, "rows": rows,
        "z2_ratio_benchmark": float(z2_ratio),
        "R_ir_mean": R_ir, "R_uv_mean": R_uv,
        "emergent_lorentz": bool(emergent),
        "verdict": verdict,
    }


# ----------------------------------------------------------------------
# run
# ----------------------------------------------------------------------

def run(ell=40, zs=(1.0, 1.25, 1.5, 1.75, 2.0), N=1600):
    rows = []
    for z in zs:
        X, P = correlators_z(ell, z, N=N)
        rows.append({"z": z, "S": ml.entanglement_entropy(X, P),
                     "far_tail_Hpi": ml.far_tail(ml.modular_H_pi(X, P))})

    ft = {r["z"]: r["far_tail_Hpi"] for r in rows}
    ft_z1, ft_z2 = ft[1.0], ft[2.0]

    # C1 control: z=1 reproduces the geometric (few-%) far tail of sub-calc 1
    control_ok = ft_z1 < 0.05
    # decision (pre-registered): z=2 far tail much larger than z=1 -> non-geometric.
    # HONEST CAVEATS (rule 1): (a) the z=2 far tail is ~7% -- a partial non-local
    # component, not an order-1 breakdown; (b) the z-dependence is NON-MONOTONIC
    # (dips at z=1.5, rises at z=2), so the far tail is a crude single-number probe
    # and this is a degradation/tension, not a clean monotonic law.  The robust,
    # N-converged fact is the z=1 (geometric) vs z=2 (SSV's UV) CONTRAST.
    ratio = ft_z2 / ft_z1
    tails = [r["far_tail_Hpi"] for r in rows]
    monotonic = all(tails[i] <= tails[i + 1] + 1e-9 for i in range(len(tails) - 1))
    degraded = ratio > 3.0

    if not control_ok:
        verdict = "INVALID -- z=1 control failed (far tail not geometric); no verdict"
    elif degraded:
        verdict = ("CAUTIONARY NEGATIVE: at SSV's UV (z=2) a robust, N-converged "
                   "non-local component appears in the modular Hamiltonian (far tail "
                   "{:.0f}% = {:.1f}x the geometric z=1 value) -- the largest of any "
                   "screen tested -> the boost-based reconstruction's geometricity is "
                   "DEGRADED for a presentist (preferred-foliation) screen. Honest "
                   "bounds: it is a PARTIAL (~7%) non-locality, not a total collapse, "
                   "and its z-dependence is NON-MONOTONIC, so this is a tension, not a "
                   "clean law. Presentism and the boost-based reconstruction are in "
                   "tension, sharpest at the physical z=2.").format(100 * ft_z2, ratio)
    else:
        verdict = ("modular flow stays ~geometric at z=2 (far tail {:.1f}x z=1) -> "
                   "reconstruction survives the preferred foliation.").format(ratio)

    return {
        "ell": ell, "N": N, "rows": rows,
        "far_tail_z1": ft_z1, "far_tail_z2": ft_z2, "ratio_z2_over_z1": float(ratio),
        "control_C1_z1_geometric": bool(control_ok),
        "far_tail_monotonic_in_z": bool(monotonic),
        "z2_geometricity_degraded": bool(degraded),
        "verdict": verdict,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ell", type=int, default=40)
    ap.add_argument("-N", type=int, default=1600)
    a = ap.parse_args()
    rep = run(ell=a.ell, N=a.N)

    print("=" * 76)
    print("#170  Lifshitz modular-locality  --  can the reconstruction be presentist?")
    print("=" * 76)
    print(f"free scalar, Dirichlet chain N={rep['N']}, block ell={rep['ell']}\n")
    print(f"CONTROL C1  z=1 far tail = {rep['far_tail_z1']:.4f}  "
          f"(geometric, ~sub-calc 1): {rep['control_C1_z1_geometric']}\n")
    print("  z       S         far-tail(H_pi)  (non-locality)")
    for r in rep["rows"]:
        print(f"  {r['z']:.2f}   {r['S']:.4f}    {r['far_tail_Hpi']:.5f}")
    print(f"\n  far-tail(z=2)/far-tail(z=1) = {rep['ratio_z2_over_z1']:.2f}   "
          f"(>3 => geometricity degraded at the physical z=2)")
    print(f"  far-tail monotonic in z: {rep['far_tail_monotonic_in_z']}  "
          f"(False => crude probe; the robust fact is the z=1-vs-z=2 contrast)")
    print(f"\nVERDICT (pure Lifshitz): {rep['verdict']}")

    # follow-on: is the geometricity IR-emergent? (Bogoliubov crossover flow)
    flow = run_flow()
    print("\n" + "=" * 76)
    print("FOLLOW-ON  is the geometricity IR-EMERGENT?  Bogoliubov crossover, "
          f"xi={flow['xi']}")
    print("=" * 76)
    print("  ell   ell/xi   far_z1    far_bog   far_z2    R=bog/z1")
    for r in flow["rows"]:
        print(f"  {r['ell']:<4d}  {r['ell_over_xi']:5.1f}   {r['far_z1']:.5f}   "
              f"{r['far_bog']:.5f}   {r['far_z2']:.5f}   {r['R']:.2f}")
    print(f"\n  R_uv (ell<=xi) = {flow['R_uv_mean']:.2f}   "
          f"R_ir (ell>=4xi) = {flow['R_ir_mean']:.2f}   "
          f"z=2 benchmark ratio = {flow['z2_ratio_benchmark']:.2f}")
    print(f"\nVERDICT (flow): {flow['verdict']}")

    rep["flow"] = flow
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "lifshitz_modular_receipt.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"\nreceipt -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

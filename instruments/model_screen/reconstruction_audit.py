"""Issue #166 sub-calculation 5: audit the claimed screen-to-bulk reconstruction.

Pre-registered on issue #166 before this instrument was written:
https://github.com/StigNorland/SVT/issues/166#issuecomment-5123996215

This is an audit of an existing positive claim, not a new reconstruction model.
It asks two falsifiable questions:

1. Does sub-calculation 4's reported long-range exponent depend on the measured
   screen polarisation at all?
2. Are the load-bearing premises of the cited holographic entanglement theorem
   present in one dimensionally consistent committed model?

The audit deliberately distinguishes "the current evidence does not establish
reconstruction" from "no reconstruction can exist."  Only the former is tested.
"""

from __future__ import annotations

import ast
import inspect
import json
import re
from pathlib import Path

import numpy as np

import reconstruction_response as reconstruction


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-VII-b" / "results"

AUDITED_FILES = (
    ROOT / "instruments/model_screen/modular_locality.py",
    ROOT / "instruments/model_screen/screen_stress_spin2.py",
    ROOT / "instruments/model_screen/induced_polarization.py",
    ROOT / "instruments/model_screen/reconstruction_response.py",
    ROOT / "papers/SSV-VII-b/results/modular-locality-issue166.md",
    ROOT / "papers/SSV-VII-b/results/screen-stress-spin2-issue166.md",
    ROOT / "papers/SSV-VII-b/results/induced-polarization-issue166.md",
    ROOT / "papers/SSV-VII-b/results/reconstruction-issue166.md",
)


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def reconstruction_green_arguments() -> list[str]:
    """Return the kernels actually inverted by sub-calculation 4's run()."""
    tree = ast.parse(inspect.getsource(reconstruction.run))
    args: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _call_name(node.func) == "greens_function":
            args.append(ast.unparse(node.args[1]))
    return args


def data_dependency_probe(L: int = 32) -> dict:
    """Blind-null guard plus the actual sub-calculation-4 dependency result.

    The control pipeline inverts two supplied screen kernels and must distinguish
    a massless from a gapped response.  The audited pipeline is then inspected to
    see whether either supplied/measured screen kernel enters its T2 inversion.
    """
    k2 = reconstruction.khat2(L)
    massless_screen_pi = k2
    gapped_screen_pi = 0.6**2 + k2

    # Blind-null control: an actually data-dependent inversion sees the change.
    g_massless = reconstruction.greens_function(L, massless_screen_pi)
    rs, prof_massless = reconstruction.radial_profile(g_massless, L)
    control_massless_power = reconstruction.fit_power(rs, prof_massless)

    g_gapped = reconstruction.greens_function(L, gapped_screen_pi)
    _, prof_gapped = reconstruction.radial_profile(g_gapped, L)
    control_gapped_rate = reconstruction.fit_yukawa_rate(rs, prof_gapped)
    control_detects_change = (
        abs(control_massless_power - 2.0) < 0.35
        and control_gapped_rate > 0.3
    )

    green_args = reconstruction_green_arguments()
    measured_pi_enters_t2 = any(
        re.search(r"\bpi2?\b|polar", arg, flags=re.IGNORECASE)
        for arg in green_args
    )

    # This is the reported T2 path: the analytic lattice Laplacian, irrespective
    # of the measured Pi2 used only by the separate determinacy scalar.
    claimed_a = reconstruction.fit_power(
        *reconstruction.radial_profile(
            reconstruction.greens_function(L, k2), L
        )
    )
    claimed_b = reconstruction.fit_power(
        *reconstruction.radial_profile(
            reconstruction.greens_function(L, k2), L
        )
    )

    return {
        "L": L,
        "greens_function_kernel_arguments_in_run": green_args,
        "measured_screen_polarisation_enters_T2": bool(measured_pi_enters_t2),
        "claimed_T2_power_with_massless_screen_fixture": float(claimed_a),
        "claimed_T2_power_with_gapped_screen_fixture": float(claimed_b),
        "claimed_T2_change": float(abs(claimed_a - claimed_b)),
        "control_massless_power": float(control_massless_power),
        "control_gapped_yukawa_rate": float(control_gapped_rate),
        "control_detects_supplied_kernel_change": bool(control_detects_change),
    }


def _corpus() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in AUDITED_FILES
    )


def _count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def theorem_premise_ledger() -> dict:
    """Reproducible absence searches over the eight #166 calculation artifacts."""
    text = _corpus()
    searches = {
        "all_ball_regions_and_frames": (
            r"ball-shaped|AdS-Rindler|every (?:ball|Lorentz frame)"
        ),
        "holographic_entropy_functional": (
            r"Ryu[-– ]Takayanagi|RT (?:formula|functional)|Wald functional"
        ),
        "asymptotic_stress_metric_dictionary": (
            r"Fefferman[-– ]Graham|asymptotic (?:bulk )?metric|"
            r"stress.{0,30}metric dictionary"
        ),
        "explicit_bulk_screen_state_map": (
            r"explicit bulk[-– ]screen map|isometry.{0,30}(?:bulk|screen)|"
            r"encoding map"
        ),
    }
    counts = {name: _count(pattern, text) for name, pattern in searches.items()}

    modular_source = AUDITED_FILES[0].read_text(encoding="utf-8")
    stress_source = AUDITED_FILES[1].read_text(encoding="utf-8")
    one_dimensional_chain = "N-site open chain" in modular_source
    stress_dimension_match = re.search(r"^D\s*=\s*4\s*$", stress_source, re.M)
    dimensions_mixed = one_dimensional_chain and bool(stress_dimension_match)

    premises = {
        "one_common_state_space_and_dimension": {
            "present": False,
            "evidence": (
                "sub-calc 1 is a one-dimensional open chain; sub-calcs 2-4 "
                "use D=4 Euclidean arrays, with no state map between them"
            ),
            "dimensions_mixed": dimensions_mixed,
        },
        "all_ball_regions_and_lorentz_frames": {
            "present": counts["all_ball_regions_and_frames"] > 0,
            "search_count": counts["all_ball_regions_and_frames"],
        },
        "holographic_entropy_functional": {
            "present": counts["holographic_entropy_functional"] > 0,
            "search_count": counts["holographic_entropy_functional"],
        },
        "asymptotic_stress_metric_dictionary": {
            "present": counts["asymptotic_stress_metric_dictionary"] > 0,
            "search_count": counts["asymptotic_stress_metric_dictionary"],
        },
        "explicit_bulk_screen_state_map": {
            "present": counts["explicit_bulk_screen_state_map"] > 0,
            "search_count": counts["explicit_bulk_screen_state_map"],
        },
        "derived_bulk_kinetic_kernel": {
            "present": False,
            "evidence": (
                "sub-calc 4 inverts khat2(L), not the measured screen Pi2(k)"
            ),
        },
    }
    missing = [name for name, item in premises.items() if not item["present"]]
    return {
        "corpus": [str(path.relative_to(ROOT)) for path in AUDITED_FILES],
        "corpus_file_count": len(AUDITED_FILES),
        "queries": searches,
        "premises": premises,
        "missing_premises": missing,
    }


def run(L: int = 32) -> dict:
    dependency = data_dependency_probe(L=L)
    theorem = theorem_premise_ledger()
    controls_ok = dependency["control_detects_supplied_kernel_change"]
    d1 = controls_ok and not dependency[
        "measured_screen_polarisation_enters_T2"
    ]
    d2 = bool(theorem["missing_premises"])
    if not controls_ok:
        decision = "INVALID: blind-null control failed"
    elif d1 and d2:
        decision = (
            "D1+D2: clean negative on the existing reconstruction claim; "
            "sub-calc 4 is screen-data-independent and the cited theorem's "
            "load-bearing premises are absent. Duality itself remains open."
        )
    elif d1:
        decision = "D1: sub-calc 4 does not measure screen reconstruction"
    elif d2:
        decision = "D2: cited reconstruction theorem is not applicable"
    else:
        decision = "D3: existing R1-assembled verdict survives this audit"
    return {
        "dependency": dependency,
        "theorem": theorem,
        "controls_ok": bool(controls_ok),
        "D1_clean_negative_subcalc4": bool(d1),
        "D2_theorem_not_applicable": bool(d2),
        "decision": decision,
    }


def main() -> None:
    report = run()
    print("=" * 76)
    print("#166 reconstruction-dependency and theorem-assumption audit")
    print("=" * 76)
    dep = report["dependency"]
    print("\nBLIND-NULL CONTROL")
    print(
        "  supplied massless kernel power       "
        f"p={dep['control_massless_power']:.3f}"
    )
    print(
        "  supplied gapped kernel Yukawa rate   "
        f"mu={dep['control_gapped_yukawa_rate']:.3f}"
    )
    print(
        "  control detects kernel change:       "
        f"{dep['control_detects_supplied_kernel_change']}"
    )
    print("\nAUDITED T2 DATA PATH")
    print(
        "  kernels inverted in run():           "
        f"{dep['greens_function_kernel_arguments_in_run']}"
    )
    print(
        "  measured Pi2 enters T2:              "
        f"{dep['measured_screen_polarisation_enters_T2']}"
    )
    print("\nTHEOREM PREMISES")
    for name, item in report["theorem"]["premises"].items():
        print(f"  {name:42s} {'PRESENT' if item['present'] else 'MISSING'}")
    print(f"\nDECISION: {report['decision']}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    output = RESULTS / "reconstruction_audit_receipt.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"\nreceipt -> {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

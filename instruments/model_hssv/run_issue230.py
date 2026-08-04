"""Run issue #230 and serialize its focused audit artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import matched_dwarf_audit


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers/H-SSV/results/issue-230"
PROTOCOL = RESULTS / "00-exploratory-protocol.md"
INVENTORY = RESULTS / "01-data-provenance-and-eligibility.md"
RECEIPT = RESULTS / "receipt.json"


def _json(value: Any) -> Any:
    return json.dumps(value, sort_keys=True) if isinstance(value, (list, dict)) else value


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _json(row.get(field)) for field in fields})


def write_tables(report: dict[str, Any]) -> None:
    matches_by_control: dict[str, list[str]] = {}
    for pair in report["matches"]:
        matches_by_control.setdefault(pair["control"], []).append(pair["udg"])
    sample_rows = []
    for row in report["summary_rows"]:
        sample_rows.append({
            **row,
            "matched_udgs": sorted(matches_by_control.get(row["name"], [])),
            "named_anchor": row["name"] == "DDO154",
        })
    write_csv(
        RESULTS / "matched-sample.csv", sample_rows,
        [
            "name", "source_class", "robust", "named_anchor", "matched_udgs", "quality_note",
            "distance_mpc", "distance_error_mpc", "rdisk_kpc", "inclination_deg",
            "inclination_error_deg", "vcirc_kms", "vcirc_error_kms", "rout_kpc",
            "mstar_msun", "mhi_msun", "mgas_msun", "mbar_msun", "fgas",
            "gamma_dyn_gyr_inv", "gamma_gas_gyr_inv", "sigma_bar_msun_kpc2",
            "dout", "log10_dout", "sigma_log10_dout",
        ],
    )
    write_csv(
        RESULTS / "matched-pairs.csv", report["matches"],
        ["udg", "control", "rank", "matching_distance"],
    )

    proxy_rows = []
    for suite, fits in report["proxy_suites"].items():
        sample, variant = suite.split(":", 1)
        proxy_rows.extend({"sample": sample, "geometry_variant": variant, **fit} for fit in fits)
    write_csv(
        RESULTS / "proxy-comparison.csv", proxy_rows,
        [
            "sample", "geometry_variant", "model", "features", "parameter_count",
            "coefficients", "standard_errors", "rank", "full_rank", "condition_number",
            "chi2", "minus_two_log_likelihood", "aicc", "bic", "loo_rmse",
            "class_holdout_rmse", "loo_rmse_ratio_to_intercept",
            "class_holdout_rmse_ratio_to_intercept", "support_threshold_pass",
        ],
    )
    write_csv(
        RESULTS / "proxy-predictions.csv", report["proxy_predictions"],
        [
            "sample", "model", "name", "source_class", "observed_log10_dout",
            "loo_predicted_log10_dout", "loo_residual",
        ],
    )
    write_csv(
        RESULTS / "model-comparison.csv", report["radial_fits"],
        [
            "galaxy", "scenario", "model", "family", "points", "parameter_count",
            "chi2", "chi2_reduced", "aicc", "delta_aicc", "bic", "delta_bic",
            "parameters_dimensionless", "boundary_parameters", "rank", "practical_rank",
            "condition_number", "maximum_absolute_correlation", "optimizer_success",
        ],
    )


def write_result_note(report: dict[str, Any]) -> None:
    primary = report["proxy_suites"]["robust_five:fiducial"]
    baseline = next(row for row in primary if row["model"] == "intercept")
    best = min((row for row in primary if row["model"] != "intercept"), key=lambda row: row["loo_rmse"])
    primary_radial = [row for row in report["radial_summary"] if row["scenario"] == "primary"]
    winners = Counter(row["aicc_winner"] for row in primary_radial)
    ddo = next(row for row in primary_radial if row["galaxy"] == "DDO154")
    udg_dout = [row["dout"] for row in report["summary_rows"] if row["source_class"] == "UDG" and row["robust"]]
    sparc_dout = [row["dout"] for row in report["summary_rows"] if row["source_class"] == "SPARC"]
    note = f"""# Issue #230 — matched dwarf result and status report

## Decision

**UNSUPPORTED.** The audit does not identify an internal-update source and does
not activate the host/shared-screen model. This is a completed negative audit,
not evidence that galaxies lack screens under the H-SSV ontology.

## What was actually comparable

The frozen matching rule selected {len(report['controls'])} unique SPARC controls
(including the named DDO154 anchor) for the five robust UDG summaries. The robust
UDGs have outer dynamical-to-baryonic summary ratios spanning
`{min(udg_dout):.3g}`--`{max(udg_dout):.3g}`; the matched SPARC controls span
`{min(sparc_dout):.3g}`--`{max(sparc_dout):.3g}`. This restates the viewed
contrast in a common summary statistic; it is not a radial decomposition.

Gate A fails for the stronger comparison. SPARC publishes reusable radial
velocities, errors, and gas/disc/bulge contributions. The homogeneous six-UDG
paper publishes two-ring kinematics as one circular-speed summary per galaxy.
The resolved AGC 114905 paper shows five nearly independent rings and baryonic
curves, but its source archive has no numeric radial table and states that data
are available from the author on request. Plot digitization was excluded by the
protocol. Thus NFW, pISO, cored-log, and retained LogSVT reductions could not be
fitted to both classes under one radial likelihood.

## Internal-proxy diagnostic

The best non-null frozen proxy model by leave-one-galaxy-out RMSE was
`{best['model']}`: RMSE `{best['loo_rmse']:.4f}` dex versus `{baseline['loo_rmse']:.4f}`
dex for the intercept (ratio `{best['loo_rmse_ratio_to_intercept']:.3f}`). Its
UDG-versus-SPARC class-holdout ratio was
`{best['class_holdout_rmse_ratio_to_intercept']:.3f}`. Proxy threshold passes in
the primary suite: `{report['gate_B']['candidate_proxy_threshold_passes']}`.
Even a numerical pass could not earn support because the same radial data
contract is absent; the viewed sample also cannot be confirmation. Geometry and
AGC 749290 sensitivities are retained in `proxy-comparison.csv`.

Gas turbulence and SFR surface density could not be used as homogeneous matched
predictors: four UDG dispersions are upper limits, SPARC has no corresponding
catalogue field here, and the source table does not print individual SFRs.

## SPARC-only radial control fits

The common radial baseline was executable only for the controls. Under primary
baryons its AICc winners were `{dict(sorted(winners.items()))}`. For DDO154 the
winner was `{ddo['aicc_winner']}` with confidence set
`{ddo['aicc_confidence_set']}`. These fits verify that a mass-discrepant slow
dwarf can prefer an extra radial response within the frozen candidate set. They
cannot tell why the UDG class differs, because no corresponding UDG fits were
possible. Full scores, covariance diagnostics, boundary flags, optimizer status,
and light/heavy baryon sensitivities are in `model-comparison.csv`.

## Shared-state gate

Gate C was not activated. The six UDGs were selected to be fairly isolated and
the inspected sources do not supply true host membership, relative velocity,
or orbital-history metadata. Projected proximity would violate the frozen rule.
No group latent, host covariance, anisotropy, backsplash memory, or
active-versus-quiescent host test was therefore fitted. There is no evidence for
a shared screen and no quantum-entanglement claim.

## Conventional alternatives and limitations

The primary papers already identify inclination as the dominant AGC 114905
systematic and flag AGC 749290's oversampling. They discuss regular rotation,
small asymmetric-drift corrections, isolation, long dynamical times, and low
turbulence, but selection, geometry, disc non-axisymmetry, disequilibrium, and
mass-profile uncertainty remain conventional explanations that this summary
audit cannot eliminate. DF2/DF4 remain in a separate future Jeans/tracer track.

## Status report

- Gate A provenance, eligibility, matching, quality exclusions, and DF2/DF4
  separation: complete.
- Gate B dimensionally valid proxies, deterministic prediction, geometry
  sensitivity, SPARC radial baselines, covariance/boundary/optimizer reporting:
  complete to the available-data boundary.
- Gate C: correctly not activated; required host metadata are absent and the
  discovery sample is isolated.
- Decision: source hypothesis unsupported on current reusable data. No paper,
  universal-screen, or entanglement claim is promoted.
"""
    (RESULTS / "result-note.md").write_text(note)


def run_all() -> dict[str, Any]:
    report = matched_dwarf_audit.run(include_radial=True)
    report["protocol_sha256"] = hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
    report["inventory_sha256"] = hashlib.sha256(INVENTORY.read_bytes()).hexdigest()
    report["instrument_sha256"] = hashlib.sha256(
        (ROOT / "instruments/model_hssv/matched_dwarf_audit.py").read_bytes()
    ).hexdigest()
    return report


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    report = run_all()
    write_tables(report)
    write_result_note(report)
    RECEIPT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "decision": report["decision"], "controls": report["controls"],
        "gate_A": report["gate_A"], "gate_B": report["gate_B"], "gate_C": report["gate_C"],
    }, indent=2, sort_keys=True))
    print(f"Wrote {RECEIPT}")


if __name__ == "__main__":
    main()


"""Issue #230 matched-dwarf internal/shared-screen audit.

The module implements the protocol frozen in
``papers/H-SSV/results/issue-230/00-exploratory-protocol.md``.  It keeps the
cross-class summary diagnostic separate from SPARC-only radial fits because the
homogeneous six-UDG publication does not provide a reusable radial baryonic
decomposition.
"""

from __future__ import annotations

import hashlib
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from instruments.model_screen.logsvt_piso_audit import (
    BOUND_SCHEMES,
    MODEL_BY_NAME,
    fit_model,
)
from instruments.paper_vi.sparc_halo_fit import parse_mass_models


SPARC_TABLE = ROOT / "papers/SSV-VI/data/SPARC/SPARC_Lelli2016c.mrt"
SPARC_CURVES = ROOT / "papers/SSV-VI/data/SPARC/MassModels_Lelli2016c.mrt"
G_KPC = 4.30091e-6  # kpc (km/s)^2 / Msun
KMS_PER_KPC_TO_GYR_INV = 1.022712165

MASS_TO_LIGHT = {
    "primary": (0.5, 0.7),
    "light": (0.3, 0.5),
    "heavy": (0.7, 0.9),
}

RADIAL_MODELS = (
    "baryons", "NFW", "pISO", "cored_log",
    "k2", "k2_Q", "k2_L", "C_L", "k2_L_Q",
)


@dataclass(frozen=True)
class UDG:
    name: str
    distance_mpc: float
    distance_error_mpc: float
    rdisk_kpc: float
    rdisk_error_kpc: float
    log_mstar: float
    log_mstar_error: float
    log_mhi: float
    log_mhi_error: float
    inclination_deg: float
    inclination_error_deg: float
    vcirc_kms: float
    vcirc_error_low_kms: float
    vcirc_error_high_kms: float
    sigma_hi_kms: float
    sigma_is_upper_limit: bool
    rout_kpc: float
    robust: bool


# Mancera Piña et al. (2020), table 1.  The four ``<=4`` dispersion entries
# are represented as 4 km/s with an explicit upper-limit flag.
UDGS = (
    UDG("AGC114905", 76, 5, 1.79, 0.04, 8.30, 0.17, 9.03, 0.08, 33, 5, 19, 4, 6, 4, True, 8.02, True),
    UDG("AGC122966", 90, 5, 4.15, 0.19, 7.73, 0.12, 9.07, 0.05, 34, 5, 37, 5, 6, 7, False, 10.80, True),
    UDG("AGC219533", 96, 5, 2.35, 0.20, 8.04, 0.12, 9.21, 0.18, 42, 5, 37, 6, 5, 4, True, 9.78, True),
    UDG("AGC248945", 84, 5, 2.08, 0.07, 8.52, 0.17, 8.78, 0.08, 66, 5, 27, 3, 3, 4, True, 8.55, True),
    UDG("AGC334315", 73, 5, 3.76, 0.14, 7.93, 0.12, 9.10, 0.10, 45, 5, 25, 5, 5, 7, False, 8.49, True),
    UDG("AGC749290", 97, 5, 2.38, 0.14, 8.32, 0.13, 8.98, 0.08, 39, 5, 26, 6, 6, 4, True, 8.47, False),
)


def _data_lines(path: Path):
    lines = path.read_text().splitlines()
    last_rule = max(index for index, line in enumerate(lines) if line.startswith("-----"))
    for line in lines[last_rule + 1:]:
        if line.strip():
            yield line


def parse_sparc_table(path: Path = SPARC_TABLE) -> dict[str, dict[str, float | int]]:
    """Parse all fields needed for matching and geometry sensitivity."""
    output: dict[str, dict[str, float | int]] = {}
    for line in _data_lines(path):
        fields = line.split()
        if len(fields) not in (18, 19):
            raise ValueError(f"unexpected SPARC row: {line!r}")
        output[fields[0]] = {
            "T": int(fields[1]), "D": float(fields[2]), "eD": float(fields[3]),
            "Inc": float(fields[5]), "eInc": float(fields[6]),
            "L36": float(fields[7]), "eL36": float(fields[8]),
            "Rdisk": float(fields[11]), "MHI": float(fields[13]),
            "Vflat": float(fields[15]), "eVflat": float(fields[16]),
            "Q": int(fields[17]),
        }
    return output


def baryonic_quantities(mstar: float, mhi: float, rdisk: float) -> dict[str, float]:
    mgas = 1.33 * mhi
    mbar = mstar + mgas
    fgas = mgas / mbar
    gamma_dyn = math.sqrt(G_KPC * mbar / rdisk**3) * KMS_PER_KPC_TO_GYR_INV
    return {
        "mstar_msun": mstar,
        "mhi_msun": mhi,
        "mgas_msun": mgas,
        "mbar_msun": mbar,
        "fgas": fgas,
        "gamma_dyn_gyr_inv": gamma_dyn,
        "gamma_gas_gyr_inv": fgas * gamma_dyn,
        "sigma_bar_msun_kpc2": mbar / (2.0 * math.pi * rdisk**2),
    }


def udg_quantities(galaxy: UDG) -> dict[str, float]:
    return baryonic_quantities(10.0**galaxy.log_mstar, 10.0**galaxy.log_mhi, galaxy.rdisk_kpc)


def sparc_quantities(row: dict[str, float | int]) -> dict[str, float]:
    return baryonic_quantities(
        0.5 * float(row["L36"]) * 1.0e9,
        float(row["MHI"]) * 1.0e9,
        float(row["Rdisk"]),
    )


def candidate_controls(
    table: dict[str, dict[str, float | int]], curves: dict[str, dict[str, np.ndarray]]
) -> list[str]:
    udg_masses = [udg_quantities(galaxy)["mbar_msun"] for galaxy in UDGS]
    lo = math.log10(min(udg_masses)) - 0.25
    hi = math.log10(max(udg_masses)) + 0.25
    return sorted(
        name for name, row in table.items()
        if name in curves
        and int(row["T"]) >= 8
        and int(row["Q"]) <= 2
        and float(row["Inc"]) >= 30.0
        and float(row["Vflat"]) > 0.0
        and len(curves[name]["R"]) >= 8
        and lo <= math.log10(sparc_quantities(row)["mbar_msun"]) <= hi
    )


def matching_distance(udg: UDG, sparc: dict[str, float | int]) -> float:
    left = udg_quantities(udg)
    right = sparc_quantities(sparc)
    terms = (
        (math.log10(left["mbar_msun"]) - math.log10(right["mbar_msun"])) / 0.30,
        (math.log10(udg.rdisk_kpc) - math.log10(float(sparc["Rdisk"]))) / 0.30,
        (left["fgas"] - right["fgas"]) / 0.20,
    )
    return float(math.sqrt(sum(value * value for value in terms)))


def select_controls(
    table: dict[str, dict[str, float | int]], curves: dict[str, dict[str, np.ndarray]]
) -> tuple[list[str], list[dict[str, Any]]]:
    candidates = candidate_controls(table, curves)
    pairs: list[dict[str, Any]] = []
    selected: set[str] = {"DDO154"}
    for galaxy in (item for item in UDGS if item.robust):
        ranked = sorted((matching_distance(galaxy, table[name]), name) for name in candidates)
        for rank, (distance, name) in enumerate(ranked[:2], start=1):
            selected.add(name)
            pairs.append({
                "udg": galaxy.name, "control": name,
                "rank": rank, "matching_distance": distance,
            })
    return sorted(selected), pairs


def _mass_log_error(mstar: float, log_star_error: float, mgas: float, log_gas_error: float) -> float:
    mbar = mstar + mgas
    sigma = math.sqrt((mstar * log_star_error) ** 2 + (mgas * log_gas_error) ** 2)
    return sigma / mbar


def _summary_row(
    *, name: str, source_class: str, distance: float, distance_error: float,
    rdisk: float, inclination: float, inclination_error: float,
    vcirc: float, vcirc_error: float, rout: float,
    quantities: dict[str, float], log_mass_error: float,
    robust: bool, quality_note: str,
) -> dict[str, Any]:
    dout = vcirc**2 * rout / (G_KPC * quantities["mbar_msun"])
    sigma_log_dout = math.sqrt(
        (2.0 * vcirc_error / max(vcirc, 1.0) / math.log(10.0)) ** 2
        + log_mass_error**2
        + (distance_error / max(distance, 1.0) / math.log(10.0)) ** 2
    )
    return {
        "name": name, "source_class": source_class, "robust": robust,
        "quality_note": quality_note, "distance_mpc": distance,
        "distance_error_mpc": distance_error, "rdisk_kpc": rdisk,
        "inclination_deg": inclination, "inclination_error_deg": inclination_error,
        "vcirc_kms": vcirc, "vcirc_error_kms": vcirc_error, "rout_kpc": rout,
        **quantities, "dout": dout, "log10_dout": math.log10(dout),
        "sigma_log10_dout": max(sigma_log_dout, 0.03),
    }


def build_summary_rows(
    controls: list[str], table: dict[str, dict[str, float | int]],
    curves: dict[str, dict[str, np.ndarray]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for galaxy in UDGS:
        q = udg_quantities(galaxy)
        log_error = _mass_log_error(
            q["mstar_msun"], galaxy.log_mstar_error,
            q["mgas_msun"], galaxy.log_mhi_error,
        )
        rows.append(_summary_row(
            name=galaxy.name, source_class="UDG", distance=galaxy.distance_mpc,
            distance_error=galaxy.distance_error_mpc, rdisk=galaxy.rdisk_kpc,
            inclination=galaxy.inclination_deg,
            inclination_error=galaxy.inclination_error_deg,
            vcirc=galaxy.vcirc_kms,
            vcirc_error=(galaxy.vcirc_error_low_kms + galaxy.vcirc_error_high_kms) / 2.0,
            rout=galaxy.rout_kpc, quantities=q, log_mass_error=log_error,
            robust=galaxy.robust,
            quality_note=("two independent rings" if galaxy.robust else "rings oversampled by factor 1.7"),
        ))
    for name in controls:
        metadata = table[name]
        q = sparc_quantities(metadata)
        mstar = q["mstar_msun"]
        stellar_error = 0.5 * float(metadata["eL36"]) * 1.0e9
        log_error = stellar_error / q["mbar_msun"] / math.log(10.0)
        curve = curves[name]
        rows.append(_summary_row(
            name=name, source_class="SPARC", distance=float(metadata["D"]),
            distance_error=float(metadata["eD"]), rdisk=float(metadata["Rdisk"]),
            inclination=float(metadata["Inc"]), inclination_error=float(metadata["eInc"]),
            vcirc=float(metadata["Vflat"]), vcirc_error=float(metadata["eVflat"]),
            rout=float(curve["R"][-1]), quantities=q, log_mass_error=log_error,
            robust=True, quality_note=f"SPARC Q={int(metadata['Q'])}; {len(curve['R'])} radial rows",
        ))
    return rows


PROXY_FEATURES: dict[str, tuple[str, ...]] = {
    "intercept": (),
    "gamma_dyn": ("log10_gamma_dyn",),
    "gamma_gas": ("log10_gamma_gas",),
    "gamma_dyn_plus_fgas": ("log10_gamma_dyn", "fgas"),
}


def feature_value(row: dict[str, Any], name: str) -> float:
    if name == "log10_gamma_dyn":
        return math.log10(row["gamma_dyn_gyr_inv"])
    if name == "log10_gamma_gas":
        return math.log10(row["gamma_gas_gyr_inv"])
    return float(row[name])


def design_matrix(rows: list[dict[str, Any]], features: tuple[str, ...]) -> np.ndarray:
    return np.asarray([[1.0, *(feature_value(row, name) for name in features)] for row in rows])


def fit_wls(rows: list[dict[str, Any]], features: tuple[str, ...]) -> dict[str, Any]:
    x = design_matrix(rows, features)
    y = np.asarray([row["log10_dout"] for row in rows])
    sigma = np.asarray([row["sigma_log10_dout"] for row in rows])
    weighted = x / sigma[:, None]
    target = y / sigma
    beta, _, rank, singular = np.linalg.lstsq(weighted, target, rcond=None)
    prediction = x @ beta
    residual = y - prediction
    chi2 = float(np.sum((residual / sigma) ** 2))
    minus_two_log_likelihood = float(np.sum((residual / sigma) ** 2 + np.log(2.0 * math.pi * sigma**2)))
    count = x.shape[1]
    points = x.shape[0]
    aicc = (
        minus_two_log_likelihood + 2.0 * count
        + 2.0 * count * (count + 1) / (points - count - 1)
        if points > count + 1 else math.inf
    )
    gram = weighted.T @ weighted
    covariance = np.linalg.pinv(gram, rcond=1.0e-12)
    standard = np.sqrt(np.clip(np.diag(covariance), 0.0, None))
    condition = float(singular[0] / singular[-1]) if singular[-1] > 0.0 else math.inf
    return {
        "features": list(features), "parameter_count": count,
        "coefficients": beta.tolist(), "standard_errors": standard.tolist(),
        "rank": int(rank), "full_rank": int(rank) == count,
        "condition_number": condition, "chi2": chi2,
        "minus_two_log_likelihood": minus_two_log_likelihood,
        "aicc": aicc, "bic": minus_two_log_likelihood + count * math.log(points),
        "predictions": prediction.tolist(),
    }


def _rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def predictive_diagnostics(
    rows: list[dict[str, Any]], features: tuple[str, ...]
) -> tuple[dict[str, float], list[dict[str, Any]]]:
    observed = np.asarray([row["log10_dout"] for row in rows])
    loo = np.empty(len(rows))
    prediction_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        training = rows[:index] + rows[index + 1:]
        fit = fit_wls(training, features)
        beta = np.asarray(fit["coefficients"])
        loo[index] = float(design_matrix([row], features)[0] @ beta)
        prediction_rows.append({
            "name": row["name"], "source_class": row["source_class"],
            "observed_log10_dout": row["log10_dout"],
            "loo_predicted_log10_dout": loo[index],
            "loo_residual": row["log10_dout"] - loo[index],
        })

    class_predictions = np.empty(len(rows))
    for held_out in ("UDG", "SPARC"):
        training = [row for row in rows if row["source_class"] != held_out]
        testing_indices = [i for i, row in enumerate(rows) if row["source_class"] == held_out]
        fit = fit_wls(training, features)
        beta = np.asarray(fit["coefficients"])
        for index in testing_indices:
            class_predictions[index] = float(design_matrix([rows[index]], features)[0] @ beta)
    return {
        "loo_rmse": _rmse(observed, loo),
        "class_holdout_rmse": _rmse(observed, class_predictions),
    }, prediction_rows


def fit_proxy_suite(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []
    predictions: list[dict[str, Any]] = []
    for model, features in PROXY_FEATURES.items():
        fit = fit_wls(rows, features)
        predictive, model_predictions = predictive_diagnostics(rows, features)
        results.append({"model": model, **fit, **predictive})
        predictions.extend({"model": model, **row} for row in model_predictions)
    baseline = next(row for row in results if row["model"] == "intercept")
    for result in results:
        result["loo_rmse_ratio_to_intercept"] = result["loo_rmse"] / baseline["loo_rmse"]
        result["class_holdout_rmse_ratio_to_intercept"] = (
            result["class_holdout_rmse"] / baseline["class_holdout_rmse"]
        )
        result["support_threshold_pass"] = bool(
            result["model"] != "intercept"
            and result["full_rank"]
            and np.isfinite(result["condition_number"])
            and result["loo_rmse_ratio_to_intercept"] <= 0.90
            and result["class_holdout_rmse_ratio_to_intercept"] <= 0.90
        )
    return results, predictions


def geometry_variant(rows: list[dict[str, Any]], variant: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for original in rows:
        row = dict(original)
        factor = 1.0
        if variant in {"inclination_low", "inclination_high"}:
            sign = -1.0 if variant == "inclination_low" else 1.0
            shifted = np.clip(
                row["inclination_deg"] + sign * row["inclination_error_deg"], 5.0, 85.0
            )
            velocity_factor = math.sin(math.radians(row["inclination_deg"])) / math.sin(math.radians(shifted))
            factor = velocity_factor**2
        elif variant in {"distance_low", "distance_high"}:
            sign = -1.0 if variant == "distance_low" else 1.0
            shifted = max(row["distance_mpc"] + sign * row["distance_error_mpc"], 0.1)
            factor = row["distance_mpc"] / shifted
        elif variant != "fiducial":
            raise ValueError(f"unknown geometry variant {variant}")
        row["dout"] = original["dout"] * factor
        row["log10_dout"] = math.log10(row["dout"])
        output.append(row)
    return output


def radial_fits(
    controls: list[str], curves: dict[str, dict[str, np.ndarray]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    scheme = BOUND_SCHEMES["primary"]
    for galaxy_index, name in enumerate(controls):
        galaxy = curves[name]
        for scenario_index, (scenario, (ups_disk, ups_bulge)) in enumerate(MASS_TO_LIGHT.items()):
            bundle: list[dict[str, Any]] = []
            for model_index, model_name in enumerate(RADIAL_MODELS):
                spec = MODEL_BY_NAME[model_name]
                fit = fit_model(
                    galaxy, spec, ups_disk, ups_bulge, scheme,
                    seed=230_000 + galaxy_index * 1000 + scenario_index * 100 + model_index,
                )
                bundle.append({
                    "galaxy": name, "scenario": scenario, "model": model_name,
                    "family": spec.family, "points": len(galaxy["R"]),
                    "parameter_count": fit["parameter_count"], "chi2": fit["chi2"],
                    "chi2_reduced": fit["chi2_reduced"], "aicc": fit["aicc"],
                    "bic": fit["bic"], "parameters_dimensionless": fit["parameters_dimensionless"],
                    "boundary_parameters": fit["boundary_parameters"],
                    "rank": fit["covariance"]["rank"],
                    "practical_rank": fit["covariance"]["practical_rank"],
                    "condition_number": fit["covariance"]["condition_number"],
                    "maximum_absolute_correlation": fit["covariance"]["maximum_absolute_correlation"],
                    "optimizer_success": fit["optimizer_success"],
                })
            minimum_aicc = min(row["aicc"] for row in bundle)
            minimum_bic = min(row["bic"] for row in bundle)
            for row in bundle:
                row["delta_aicc"] = row["aicc"] - minimum_aicc
                row["delta_bic"] = row["bic"] - minimum_bic
            rows.extend(bundle)
    return rows


def summarize_radial(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    keys = sorted({(row["scenario"], row["galaxy"]) for row in rows})
    for scenario, galaxy in keys:
        bundle = [row for row in rows if row["scenario"] == scenario and row["galaxy"] == galaxy]
        best = min(bundle, key=lambda row: row["aicc"])
        output.append({
            "scenario": scenario, "galaxy": galaxy, "aicc_winner": best["model"],
            "aicc_confidence_set": [row["model"] for row in bundle if row["delta_aicc"] <= 2.0],
            "all_optimizers_succeeded": all(row["optimizer_success"] for row in bundle),
            "rank_deficient_fit_count": sum(
                row["practical_rank"] < row["parameter_count"] for row in bundle
            ),
            "boundary_fit_count": sum(bool(row["boundary_parameters"]) for row in bundle),
        })
    return output


def run(include_radial: bool = True) -> dict[str, Any]:
    table = parse_sparc_table()
    curves = parse_mass_models(SPARC_CURVES)
    controls, matches = select_controls(table, curves)
    summary_rows = build_summary_rows(controls, table, curves)

    proxy_suites: dict[str, list[dict[str, Any]]] = {}
    prediction_rows: list[dict[str, Any]] = []
    for sample_name, sample in {
        "robust_five": [row for row in summary_rows if row["source_class"] == "SPARC" or row["robust"]],
        "all_six": summary_rows,
    }.items():
        for variant in ("fiducial", "inclination_low", "inclination_high", "distance_low", "distance_high"):
            key = f"{sample_name}:{variant}"
            fits, predictions = fit_proxy_suite(geometry_variant(sample, variant))
            proxy_suites[key] = fits
            if variant == "fiducial":
                prediction_rows.extend({"sample": sample_name, **row} for row in predictions)

    primary_proxy = proxy_suites["robust_five:fiducial"]
    candidate_passes = [row["model"] for row in primary_proxy if row["support_threshold_pass"]]
    sensitivity_pass = all(
        any(row["support_threshold_pass"] for row in proxy_suites[key])
        for key in (
            "all_six:fiducial", "robust_five:inclination_low", "robust_five:inclination_high",
            "robust_five:distance_low", "robust_five:distance_high",
        )
    )

    radial = radial_fits(controls, curves) if include_radial else []
    radial_summary = summarize_radial(radial)
    source_hashes = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (SPARC_TABLE, SPARC_CURVES)
    }
    common_radial_contract = False
    internal_support = bool(candidate_passes and sensitivity_pass and common_radial_contract)
    return {
        "issue": 230,
        "status": "UNSUPPORTED",
        "evidence_boundary": "retrospective discovery audit; no held-out confirmation",
        "source_hashes": source_hashes,
        "gate_A": {
            "sparc_radial_contract": True,
            "homogeneous_udg_radial_contract": False,
            "common_radial_contract": common_radial_contract,
            "resolved_agc114905_numeric_table_in_source": False,
            "df2_df4_excluded_to_future_jeans_track": True,
        },
        "gate_B": {
            "candidate_proxy_threshold_passes": candidate_passes,
            "all_required_sensitivities_pass": sensitivity_pass,
            "same_data_contract": common_radial_contract,
            "internal_update_support": internal_support,
        },
        "gate_C": {
            "activated": False,
            "reason": "six-UDG sample is fairly isolated and no true host-membership catalogue is supplied",
            "shared_screen_support": False,
        },
        "controls": controls,
        "matches": matches,
        "summary_rows": summary_rows,
        "proxy_suites": proxy_suites,
        "proxy_predictions": prediction_rows,
        "radial_fits": radial,
        "radial_summary": radial_summary,
        "decision": "UNSUPPORTED",
        "decision_reason": (
            "No proxy can earn support without a common radial data contract; "
            "the shared-state gate is ineligible for an isolated sample without host metadata."
        ),
    }

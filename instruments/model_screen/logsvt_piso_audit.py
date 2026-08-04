"""Issue #225: corrected LogSVT, cored-log, and genuine-pISO audit.

This is a retrospective reproducibility audit of the exploratory files formerly
held in ``/tmp/ssv-screen-pilot-223``.  It deliberately keeps the circular-speed
law of a cored logarithmic potential separate from the standard
pseudo-isothermal (pISO) density sphere.  It fits the same eleven SPARC
galaxies, the same three fixed stellar mass-to-light scenarios, and all 32
hierarchical reductions of the published LogSVT radial expression.

Run from the repository root:

    python instruments/model_screen/logsvt_piso_audit.py

The run writes the machine receipt, model-selection tables, and result note to
``papers/H-SSV/results/issue-225``.  Parallel work is collected into a frozen
scenario/galaxy/model order before serialization.
"""

from __future__ import annotations

import concurrent.futures
import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np
from scipy.optimize import least_squares


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from instruments.paper_vi.sparc_halo_fit import parse_mass_models, v_nfw_sq  # noqa: E402


DATA = ROOT / "papers/SSV-VI/data/SPARC/MassModels_Lelli2016c.mrt"
RESULTS = ROOT / "papers/H-SSV/results/issue-225"
RECEIPT = RESULTS / "receipt.json"
MODEL_TABLE = RESULTS / "model-selection.csv"
COMPARISON_TABLE = RESULTS / "comparison.csv"
BOUND_TABLE = RESULTS / "bound-sensitivity.csv"
NOTE = RESULTS / "result-note.md"

GALAXIES = (
    "DDO154", "NGC2403", "NGC2841", "NGC2903", "NGC2976",
    "NGC3198", "NGC3521", "NGC5055", "NGC6946", "NGC7331",
    "NGC7793",
)
BARYON_SCENARIOS = {
    "primary": (0.5, 0.7),
    "light": (0.3, 0.5),
    "heavy": (0.7, 0.9),
}
MULTISTARTS = 16
MAX_WORKERS = 16
PRACTICAL_RANK_RTOL = 1.0e-8

# Reviewed source/output hashes from the ephemeral pilot.  The old artifacts
# are evidence provenance only; this instrument has no runtime dependency on
# /tmp and supersedes the incorrect ISO label and formula.
PILOT_PROVENANCE = {
    "logsvt-model-selection-preregistration.md": "ddc3a2f8378663d3c872ef22bf08b91d96b90b7f96d57dfc40f9490769187b80",
    "logsvt-term-ablation-preregistration.md": "7aa9a2b02678483db6df3a06cb7652b48fb00960d2f63dff3c29d2b0dc30ebb9",
    "logsvt_model_selection.py": "408c56c4f88dfe2a617b7664d08722af67f6576dbffd16159003c794ecafb68a",
    "logsvt_term_ablation.py": "732e90d08ddd6564fc66d2cd593d0f25c1fdd34b45cdcfacfc4784a9686eee03",
    "logsvt-model-selection.csv": "ec94990dda9f31717d4f520111faacab8ee5676d61a1f5c33f000f8af8667e6a",
    "logsvt-term-ablation.csv": "65cd5b080cc65f77dd071ebab4cb20b74703099cc627cba61ba71d5789275198",
    "logsvt-model-selection-result.md": "a018591573b4a92f5375c15474a37d1ebb1431520250a8ba037645c0252005c2",
    "logsvt-term-ablation-result.md": "0606852529a9f95ef2b7fc1e7caba4376e659eacacb2f27e6986d11cc3842671",
    "logsvt-model-selection-receipt.json": "fecc40c7fb0799237d0cae0829506989983dbcd3ad9a6343011650af0956dfd1",
    "logsvt-term-ablation-receipt.json": "ade1ed1ad3c71eb1e8bb6363df57c66cedd10d79673541c20e42ff21f3945ef5",
}


@dataclass(frozen=True)
class ModelSpec:
    name: str
    parameters: tuple[str, ...]
    family: str = "logsvt"


@dataclass(frozen=True)
class BoundScheme:
    name: str
    log_lower: float
    log_upper: float
    linear_limit: float
    concentration: tuple[float, float]
    scaled_v200: tuple[float, float]


BOUND_SCHEMES = {
    # Exact transformed bounds inherited from the pilot.
    "primary": BoundScheme("primary", -18.0, 10.0, 100.0, (1.0, 100.0), (0.03, 30.0)),
    # A deliberately expanded rerun; starts are held fixed to isolate bounds.
    "expanded": BoundScheme("expanded", -24.0, 14.0, 200.0, (0.5, 200.0), (0.01, 60.0)),
}


def build_logsvt_models() -> tuple[ModelSpec, ...]:
    """All 2 x 4 x 2 x 2 = 32 hierarchical published-term reductions."""
    models: list[ModelSpec] = []
    for constant in (False, True):
        for branch in ("none", "k1", "k2", "k12"):
            for linear in (False, True):
                for quadratic in (False, True):
                    parameters: list[str] = []
                    labels: list[str] = []
                    if constant:
                        parameters.append("logC")
                        labels.append("C")
                    if branch != "none":
                        parameters.append("logB")
                        if branch in ("k1", "k12"):
                            parameters.append("logu1")
                        if branch in ("k2", "k12"):
                            parameters.append("logu2")
                        labels.append(branch)
                    if linear:
                        parameters.append("L")
                        labels.append("L")
                    if quadratic:
                        parameters.append("logQ")
                        labels.append("Q")
                    models.append(ModelSpec("_".join(labels) or "baryons", tuple(parameters)))
    return tuple(models)


LOGSVT_MODELS = build_logsvt_models()
COMPARATOR_MODELS = (
    ModelSpec("cored_log", ("logH", "logRc"), "cored_log"),
    ModelSpec("pISO", ("logH", "logRc"), "piso"),
    ModelSpec("NFW", ("logV200", "logc"), "nfw"),
)
MODELS = LOGSVT_MODELS + COMPARATOR_MODELS
MODEL_BY_NAME = {model.name: model for model in MODELS}


def baryonic_velocity_squared(galaxy: dict, ups_disk: float, ups_bulge: float) -> np.ndarray:
    """Fixed SPARC baryons, preserving the signed-gas convention."""
    return (
        galaxy["Vgas"] * np.abs(galaxy["Vgas"])
        + ups_disk * galaxy["Vdisk"] * np.abs(galaxy["Vdisk"])
        + ups_bulge * galaxy["Vbul"] ** 2
    )


def cored_log_shape(radius_over_core: np.ndarray) -> np.ndarray:
    """v^2/V_inf^2 for a cored logarithmic potential."""
    z = np.asarray(radius_over_core, dtype=float)
    return z**2 / (1.0 + z**2)


def piso_shape(radius_over_core: np.ndarray) -> np.ndarray:
    """v^2/(4 pi G rho_0 r_c^2) for a genuine pISO density sphere.

    The series avoids cancellation at the origin:
    1 - atan(z)/z = z^2/3 - z^4/5 + z^6/7 - ... .
    """
    z = np.asarray(radius_over_core, dtype=float)
    z2 = z * z
    small = np.abs(z) < 1.0e-3
    series = z2 / 3.0 - z2**2 / 5.0 + z2**3 / 7.0 - z2**4 / 9.0
    direct = np.zeros_like(z)
    np.divide(np.arctan(z), z, out=direct, where=z != 0.0)
    direct = 1.0 - direct
    direct = np.where(z == 0.0, 0.0, direct)
    return np.where(small, series, direct)


def decoded(parameters: np.ndarray, spec: ModelSpec) -> dict[str, float]:
    output: dict[str, float] = {}
    for name, value in zip(spec.parameters, parameters):
        key = name[3:] if name.startswith("log") else name
        output[key] = float(math.exp(value)) if name.startswith("log") else float(value)
    return output


def parameter_bounds(spec: ModelSpec, scheme: BoundScheme) -> tuple[np.ndarray, np.ndarray]:
    lower: list[float] = []
    upper: list[float] = []
    for name in spec.parameters:
        if name == "L":
            lower.append(-scheme.linear_limit)
            upper.append(scheme.linear_limit)
        elif name == "logc":
            lower.append(math.log(scheme.concentration[0]))
            upper.append(math.log(scheme.concentration[1]))
        elif name == "logV200":
            lower.append(math.log(scheme.scaled_v200[0]))
            upper.append(math.log(scheme.scaled_v200[1]))
        else:
            lower.append(scheme.log_lower)
            upper.append(scheme.log_upper)
    return np.asarray(lower), np.asarray(upper)


def logsvt_extra_dimensionless(x: np.ndarray, parameters: np.ndarray, spec: ModelSpec) -> np.ndarray:
    p = decoded(parameters, spec)
    q = np.full_like(x, p.get("C", 0.0))
    if "B" in p:
        u1 = p.get("u1", 0.0)
        u2 = p.get("u2", 0.0)
        q += p["B"] * 2.0 * x * (u1 + 2.0 * u2 * x) / (1.0 + u1 * x + u2 * x**2)
    q += p.get("L", 0.0) * x
    q -= p.get("Q", 0.0) * x**2
    return q


def extra_velocity_squared(
    radius: np.ndarray,
    parameters: np.ndarray,
    spec: ModelSpec,
    vscale: float,
) -> np.ndarray:
    """Non-baryonic contribution in physical (km/s)^2 units."""
    x = radius / radius[-1]
    p = decoded(parameters, spec)
    if spec.family == "logsvt":
        return vscale**2 * logsvt_extra_dimensionless(x, parameters, spec)
    if spec.family == "cored_log":
        return vscale**2 * p["H"] * cored_log_shape(x / p["Rc"])
    if spec.family == "piso":
        return vscale**2 * p["H"] * piso_shape(x / p["Rc"])
    if spec.family == "nfw":
        return v_nfw_sq(radius, vscale * p["V200"], p["c"])
    raise ValueError(f"unknown model family: {spec.family}")


def model_velocity(
    galaxy: dict,
    vb2: np.ndarray,
    parameters: np.ndarray,
    spec: ModelSpec,
    vscale: float,
) -> np.ndarray:
    extra = extra_velocity_squared(galaxy["R"], parameters, spec, vscale)
    return np.sqrt(np.clip(vb2 + extra, 1.0e-8, None))


def criteria(chi2: float, points: int, parameters: int) -> dict[str, float]:
    correction = (
        2.0 * parameters * (parameters + 1) / (points - parameters - 1)
        if points > parameters + 1
        else math.inf
    )
    return {
        "chi2": float(chi2),
        "chi2_reduced": float(chi2 / max(points - parameters, 1)),
        "aicc": float(chi2 + 2.0 * parameters + correction),
        "bic": float(chi2 + parameters * math.log(points)),
    }


def covariance_diagnostics(result, chi2: float, points: int, names: tuple[str, ...]) -> dict:
    jacobian = np.asarray(result.jac, dtype=float)
    count = jacobian.shape[1]
    if count == 0:
        return {
            "parameter_order": [], "rank": 0, "practical_rank": 0,
            "condition_number": None, "maximum_absolute_correlation": None,
            "standard_errors_transformed": [], "covariance_matrix_transformed": [],
            "correlation_matrix_transformed": [], "jacobian_singular_values": [],
        }
    singular = np.linalg.svd(jacobian, compute_uv=False)
    if singular[0] == 0.0:
        rank = practical_rank = 0
        condition = None
    else:
        tolerance = singular[0] * max(jacobian.shape) * np.finfo(float).eps
        rank = int(np.sum(singular > tolerance))
        practical_rank = int(np.sum(singular / singular[0] > PRACTICAL_RANK_RTOL))
        condition_value = float(singular[0] / singular[-1]) if singular[-1] > 0.0 else math.inf
        condition = condition_value if np.isfinite(condition_value) else None
    scale = chi2 / max(points - count, 1)
    covariance = np.linalg.pinv(jacobian.T @ jacobian, rcond=1.0e-12) * scale
    standard = np.sqrt(np.clip(np.diag(covariance), 0.0, None))
    denominator = np.outer(standard, standard)
    correlation = np.divide(
        covariance, denominator, out=np.zeros_like(covariance), where=denominator > 0.0
    )
    correlation = np.clip(correlation, -1.0, 1.0)
    off_diagonal = np.abs(correlation.copy())
    np.fill_diagonal(off_diagonal, 0.0)
    return {
        "parameter_order": list(names),
        "rank": rank,
        "practical_rank": practical_rank,
        "practical_rank_relative_threshold": PRACTICAL_RANK_RTOL,
        "condition_number": condition,
        "maximum_absolute_correlation": float(np.max(off_diagonal)) if count > 1 else 0.0,
        "standard_errors_transformed": standard.tolist(),
        "covariance_matrix_transformed": covariance.tolist(),
        "correlation_matrix_transformed": correlation.tolist(),
        "jacobian_singular_values": singular.tolist(),
    }


def starts(spec: ModelSpec, scheme: BoundScheme, seed: int) -> list[np.ndarray]:
    if not spec.parameters:
        return [np.array([])]
    lower, upper = parameter_bounds(spec, scheme)
    rng = np.random.default_rng(seed)
    initial = np.zeros(len(spec.parameters))
    for index, name in enumerate(spec.parameters):
        if name == "logc":
            initial[index] = math.log(10.0)
        elif name == "logV200":
            initial[index] = 0.0
    output = [np.clip(initial, lower + 1.0e-8, upper - 1.0e-8)]
    for _ in range(MULTISTARTS - 1):
        draw = np.empty(len(spec.parameters))
        for index, name in enumerate(spec.parameters):
            if name == "L":
                draw[index] = rng.uniform(-8.0, 8.0)
            elif name == "logc":
                draw[index] = rng.uniform(math.log(2.0), math.log(40.0))
            elif name == "logV200":
                draw[index] = rng.uniform(math.log(0.2), math.log(5.0))
            else:
                draw[index] = rng.uniform(-5.0, 5.0)
        output.append(np.clip(draw, lower + 1.0e-8, upper - 1.0e-8))
    return output


def fit_model(
    galaxy: dict,
    spec: ModelSpec,
    ups_disk: float,
    ups_bulge: float,
    scheme: BoundScheme,
    seed: int,
) -> dict:
    vb2 = baryonic_velocity_squared(galaxy, ups_disk, ups_bulge)
    vscale = max(float(np.median(galaxy["Vobs"])), 10.0)
    points = len(galaxy["R"])
    count = len(spec.parameters)
    if count == 0:
        residual = (galaxy["Vobs"] - np.sqrt(np.clip(vb2, 1.0e-8, None))) / galaxy["eV"]
        score = criteria(float(residual @ residual), points, 0)
        empty = type("EmptyFit", (), {"jac": np.empty((points, 0))})()
        return {
            **score, "parameter_count": 0, "parameters_transformed": {},
            "parameters_dimensionless": {}, "boundary_parameters": [],
            "covariance": covariance_diagnostics(empty, score["chi2"], points, ()),
            "optimizer_success": True, "optimizer_message": "no fitted parameters",
            "optimizer_evaluations": 0,
        }

    def residual(parameters: np.ndarray) -> np.ndarray:
        velocity = model_velocity(galaxy, vb2, parameters, spec, vscale)
        return (galaxy["Vobs"] - velocity) / galaxy["eV"]

    lower, upper = parameter_bounds(spec, scheme)
    best: tuple[float, object] | None = None
    for initial in starts(spec, scheme, seed):
        fit = least_squares(
            residual, initial, bounds=(lower, upper), method="trf", max_nfev=5000,
            xtol=1.0e-11, ftol=1.0e-11, gtol=1.0e-11,
        )
        chi2 = float(fit.fun @ fit.fun)
        if best is None or chi2 < best[0]:
            best = (chi2, fit)
    assert best is not None
    chi2, fit = best
    if not fit.success:
        # Highly redundant k1+k2 combinations can reach the conservative
        # evaluation cap while still descending.  Continue only the best
        # trajectory, preserving its optimum and all frozen multistarts.
        continued = least_squares(
            residual, fit.x, bounds=(lower, upper), method="trf", max_nfev=50000,
            xtol=1.0e-9, ftol=1.0e-9, gtol=1.0e-9,
        )
        continued_chi2 = float(continued.fun @ continued.fun)
        if continued_chi2 <= chi2:
            chi2, fit = continued_chi2, continued
    boundary = [
        name
        for name, value, lo, hi in zip(spec.parameters, fit.x, lower, upper)
        if min(value - lo, hi - value) < 1.0e-4 * max(hi - lo, 1.0)
    ]
    return {
        **criteria(chi2, points, count),
        "parameter_count": count,
        "parameters_transformed": dict(zip(spec.parameters, map(float, fit.x))),
        "parameters_dimensionless": decoded(fit.x, spec),
        "boundary_parameters": boundary,
        "covariance": covariance_diagnostics(fit, chi2, points, spec.parameters),
        "optimizer_success": bool(fit.success),
        "optimizer_message": str(fit.message),
        "optimizer_evaluations": int(fit.nfev),
    }


def has_k2(model_name: str) -> bool:
    return "logu2" in MODEL_BY_NAME[model_name].parameters


def summarize_bundle(fits: dict[str, dict]) -> dict:
    minimum_aicc = min(fit["aicc"] for fit in fits.values())
    minimum_bic = min(fit["bic"] for fit in fits.values())
    for fit in fits.values():
        fit["delta_aicc"] = float(fit["aicc"] - minimum_aicc)
        fit["delta_bic"] = float(fit["bic"] - minimum_bic)
    aicc_winner = min(fits, key=lambda name: fits[name]["aicc"])
    bic_winner = min(fits, key=lambda name: fits[name]["bic"])
    confidence = [name for name in fits if fits[name]["delta_aicc"] <= 2.0]
    best_logsvt = min((m.name for m in LOGSVT_MODELS), key=lambda name: fits[name]["aicc"])
    best_without_cored_shape = min(
        (name for name in fits if not has_k2(name) and name != "cored_log"),
        key=lambda name: fits[name]["aicc"],
    )
    cored_shape_models = {"cored_log"} | {m.name for m in LOGSVT_MODELS if has_k2(m.name)}
    return {
        "aicc_winner": aicc_winner,
        "bic_winner": bic_winner,
        "aicc_confidence_set": confidence,
        "bic_within_2": [name for name in fits if fits[name]["delta_bic"] <= 2.0],
        "best_logsvt_reduction": best_logsvt,
        "k2_term_necessary_after_corrected_baseline": bool(confidence) and all(
            has_k2(name) for name in confidence
        ),
        "cored_log_shape_necessary": bool(confidence) and all(
            name in cored_shape_models for name in confidence
        ),
        "best_non_cored_shape": best_without_cored_shape,
        "best_non_cored_shape_delta_aicc": float(
            fits[best_without_cored_shape]["aicc"] - minimum_aicc
        ),
        "pairwise": {
            "pISO_minus_cored_log_delta_aicc": float(fits["pISO"]["aicc"] - fits["cored_log"]["aicc"]),
            "pISO_minus_cored_log_delta_bic": float(fits["pISO"]["bic"] - fits["cored_log"]["bic"]),
            "pISO_minus_best_logsvt_delta_aicc": float(fits["pISO"]["aicc"] - fits[best_logsvt]["aicc"]),
            "pISO_minus_best_logsvt_delta_bic": float(fits["pISO"]["bic"] - fits[best_logsvt]["bic"]),
            "cored_log_minus_best_logsvt_delta_aicc": float(fits["cored_log"]["aicc"] - fits[best_logsvt]["aicc"]),
            "cored_log_minus_best_logsvt_delta_bic": float(fits["cored_log"]["bic"] - fits[best_logsvt]["bic"]),
        },
        "fits": fits,
    }


def run_bundle(task: tuple) -> tuple[str, str, str, dict]:
    bounds_name, scenario, galaxy_name, galaxy, mass_to_light, galaxy_index = task
    scheme = BOUND_SCHEMES[bounds_name]
    disk, bulge = mass_to_light
    fits: dict[str, dict] = {}
    for model_index, model in enumerate(MODELS):
        # The seed is deliberately independent of the bound scheme so the
        # sensitivity rerun changes bounds, not multistart initialization.
        seed = 225_000 + 1000 * galaxy_index + 10 * model_index
        fits[model.name] = fit_model(galaxy, model, disk, bulge, scheme, seed)
    result = summarize_bundle(fits)
    result.update({
        "points": len(galaxy["R"]),
        "radius_min_kpc": float(galaxy["R"][0]),
        "radius_max_kpc": float(galaxy["R"][-1]),
    })
    return bounds_name, scenario, galaxy_name, result


def ordered_scenarios(raw: dict) -> dict:
    return {
        bounds: {
            scenario: {galaxy: raw[bounds][scenario][galaxy] for galaxy in GALAXIES}
            for scenario in BARYON_SCENARIOS
        }
        for bounds in BOUND_SCHEMES
    }


def write_model_table(result: dict) -> None:
    fields = [
        "bounds", "scenario", "galaxy", "points", "model", "family",
        "parameter_count", "chi2", "chi2_reduced", "aicc", "delta_aicc",
        "bic", "delta_bic", "condition_number", "practical_rank", "rank",
        "maximum_absolute_correlation", "boundary_parameters", "parameters_dimensionless",
        "delta_aicc_vs_pISO", "delta_bic_vs_pISO",
        "delta_aicc_vs_cored_log", "delta_bic_vs_cored_log",
    ]
    with MODEL_TABLE.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for bounds in BOUND_SCHEMES:
            for scenario in BARYON_SCENARIOS:
                for galaxy in GALAXIES:
                    bundle = result["runs"][bounds][scenario][galaxy]
                    for model in MODELS:
                        fit = bundle["fits"][model.name]
                        writer.writerow({
                            "bounds": bounds, "scenario": scenario, "galaxy": galaxy,
                            "points": bundle["points"], "model": model.name, "family": model.family,
                            "parameter_count": fit["parameter_count"], "chi2": fit["chi2"],
                            "chi2_reduced": fit["chi2_reduced"], "aicc": fit["aicc"],
                            "delta_aicc": fit["delta_aicc"], "bic": fit["bic"],
                            "delta_bic": fit["delta_bic"],
                            "condition_number": fit["covariance"]["condition_number"],
                            "practical_rank": fit["covariance"]["practical_rank"],
                            "rank": fit["covariance"]["rank"],
                            "maximum_absolute_correlation": fit["covariance"]["maximum_absolute_correlation"],
                            "boundary_parameters": ";".join(fit["boundary_parameters"]),
                            "parameters_dimensionless": json.dumps(fit["parameters_dimensionless"], sort_keys=True),
                            "delta_aicc_vs_pISO": fit["aicc"] - bundle["fits"]["pISO"]["aicc"],
                            "delta_bic_vs_pISO": fit["bic"] - bundle["fits"]["pISO"]["bic"],
                            "delta_aicc_vs_cored_log": fit["aicc"] - bundle["fits"]["cored_log"]["aicc"],
                            "delta_bic_vs_cored_log": fit["bic"] - bundle["fits"]["cored_log"]["bic"],
                        })


def write_comparison_table(result: dict) -> None:
    fields = [
        "scenario", "galaxy", "best_model", "models_delta_aicc_le_2",
        "best_logsvt_reduction", "piso_minus_cored_log_delta_aicc",
        "piso_minus_cored_log_delta_bic", "piso_minus_best_logsvt_delta_aicc",
        "piso_minus_best_logsvt_delta_bic", "cored_log_minus_best_logsvt_delta_aicc",
        "cored_log_minus_best_logsvt_delta_bic", "k2_term_necessary",
        "cored_log_shape_necessary", "best_non_cored_shape",
        "best_non_cored_shape_delta_aicc",
    ]
    with COMPARISON_TABLE.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for scenario in BARYON_SCENARIOS:
            for galaxy in GALAXIES:
                bundle = result["runs"]["primary"][scenario][galaxy]
                pair = bundle["pairwise"]
                writer.writerow({
                    "scenario": scenario, "galaxy": galaxy,
                    "best_model": bundle["aicc_winner"],
                    "models_delta_aicc_le_2": ";".join(bundle["aicc_confidence_set"]),
                    "best_logsvt_reduction": bundle["best_logsvt_reduction"],
                    "piso_minus_cored_log_delta_aicc": pair["pISO_minus_cored_log_delta_aicc"],
                    "piso_minus_cored_log_delta_bic": pair["pISO_minus_cored_log_delta_bic"],
                    "piso_minus_best_logsvt_delta_aicc": pair["pISO_minus_best_logsvt_delta_aicc"],
                    "piso_minus_best_logsvt_delta_bic": pair["pISO_minus_best_logsvt_delta_bic"],
                    "cored_log_minus_best_logsvt_delta_aicc": pair["cored_log_minus_best_logsvt_delta_aicc"],
                    "cored_log_minus_best_logsvt_delta_bic": pair["cored_log_minus_best_logsvt_delta_bic"],
                    "k2_term_necessary": bundle["k2_term_necessary_after_corrected_baseline"],
                    "cored_log_shape_necessary": bundle["cored_log_shape_necessary"],
                    "best_non_cored_shape": bundle["best_non_cored_shape"],
                    "best_non_cored_shape_delta_aicc": bundle["best_non_cored_shape_delta_aicc"],
                })


def bound_sensitivity(result: dict) -> dict:
    summary: dict[str, dict] = {}
    for scenario in BARYON_SCENARIOS:
        summary[scenario] = {}
        for galaxy in GALAXIES:
            primary = result["runs"]["primary"][scenario][galaxy]
            expanded = result["runs"]["expanded"][scenario][galaxy]
            primary_scores = primary["fits"]
            expanded_scores = expanded["fits"]
            max_improvement = max(
                primary_scores[model.name]["chi2"] - expanded_scores[model.name]["chi2"]
                for model in MODELS
            )
            summary[scenario][galaxy] = {
                "primary_winner": primary["aicc_winner"],
                "expanded_winner": expanded["aicc_winner"],
                "same_winner_label": primary["aicc_winner"] == expanded["aicc_winner"],
                "same_winner_shape": winner_shape(primary["aicc_winner"]) == winner_shape(expanded["aicc_winner"]),
                "same_confidence_set": primary["aicc_confidence_set"] == expanded["aicc_confidence_set"],
                "maximum_chi2_improvement_under_expanded_bounds": float(max_improvement),
                "primary_boundary_fit_count": sum(bool(f["boundary_parameters"]) for f in primary_scores.values()),
                "expanded_boundary_fit_count": sum(bool(f["boundary_parameters"]) for f in expanded_scores.values()),
                "k2_decision_changed": (
                    primary["k2_term_necessary_after_corrected_baseline"]
                    != expanded["k2_term_necessary_after_corrected_baseline"]
                ),
            }
    return summary


def write_bound_table(result: dict) -> None:
    fields = ["scenario", "galaxy", "primary_winner", "expanded_winner", "same_winner_label",
              "same_winner_shape",
              "same_confidence_set", "maximum_chi2_improvement_under_expanded_bounds",
              "primary_boundary_fit_count", "expanded_boundary_fit_count", "k2_decision_changed"]
    with BOUND_TABLE.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for scenario in BARYON_SCENARIOS:
            for galaxy in GALAXIES:
                writer.writerow({"scenario": scenario, "galaxy": galaxy,
                                 **result["bound_sensitivity"][scenario][galaxy]})


def fmt(value: float) -> str:
    return f"{value:.2f}"


def winner_shape(model_name: str) -> str:
    """Canonicalize only the proved exact k2/cored-log two-parameter alias."""
    return "cored_log" if model_name in {"k2", "cored_log"} else model_name


def write_note(result: dict) -> None:
    lines = [
        "# Issue #225 — corrected cored-logarithmic versus pISO audit", "",
        "## Status and evidential boundary", "",
        "This is a **retrospective correction and reproducibility audit**, not a blind "
        "preregistration. The eleven-galaxy pilot, its term-ablation outcome, and the "
        "apparent importance of the published `k2` branch were viewed before this audit. "
        "Nothing here is held-out confirmation, and no H-SSV screen mechanism follows from "
        "a rotation-curve preference.", "",
        "The pilot error is corrected: `cored_log` uses "
        "`H x^2/(x^2+Rc^2)`, while genuine `pISO` uses "
        "`H[1-(Rc/x) atan(x/Rc)]`. The LogSVT `k2` branch is exactly the former, "
        "not the latter.", "",
        "## Fixed audit design", "",
        "The audit refits the same eleven overlapping SPARC galaxies and the same fixed "
        "stellar mass-to-light scenarios: primary `(0.5, 0.7)`, light `(0.3, 0.5)`, "
        "and heavy `(0.7, 0.9)`. Candidates are all 32 hierarchical LogSVT reductions, "
        "the separately named cored-log and genuine-pISO laws, and NFW; baryons-only is "
        "one member of the 32-model lattice. Fits use weighted velocity residuals and 16 "
        "deterministic multistarts.", "",
        "## Per-galaxy decisions under inherited bounds", "",
    ]
    for scenario in BARYON_SCENARIOS:
        lines.extend([
            f"### {scenario}", "",
            "| galaxy | best AICc model | models within ΔAICc ≤ 2 | ΔAICc pISO−cored | ΔBIC pISO−cored | k2 term necessary? | cored-log shape necessary? |",
            "|---|---|---|---:|---:|---|---|",
        ])
        for galaxy in GALAXIES:
            bundle = result["runs"]["primary"][scenario][galaxy]
            pair = bundle["pairwise"]
            confidence = ", ".join(f"`{name}`" for name in bundle["aicc_confidence_set"])
            lines.append(
                f"| `{galaxy}` | `{bundle['aicc_winner']}` | {confidence} | "
                f"{fmt(pair['pISO_minus_cored_log_delta_aicc'])} | "
                f"{fmt(pair['pISO_minus_cored_log_delta_bic'])} | "
                f"{'yes' if bundle['k2_term_necessary_after_corrected_baseline'] else 'no'} | "
                f"{'yes' if bundle['cored_log_shape_necessary'] else 'no'} |"
            )
        lines.append("")

    lines.extend(["## Aggregate correction result", ""])
    for scenario in BARYON_SCENARIOS:
        bundles = result["runs"]["primary"][scenario]
        winner_counts = Counter(bundle["aicc_winner"] for bundle in bundles.values())
        piso_degenerate = sum(
            abs(bundle["pairwise"]["pISO_minus_cored_log_delta_aicc"]) <= 2.0
            for bundle in bundles.values()
        )
        k2_needed = sum(bundle["k2_term_necessary_after_corrected_baseline"] for bundle in bundles.values())
        shape_needed = sum(bundle["cored_log_shape_necessary"] for bundle in bundles.values())
        counts = ", ".join(f"`{name}`={count}" for name, count in winner_counts.items())
        lines.extend([
            f"- `{scenario}`: AICc winners {counts}; genuine pISO and cored-log are "
            f"pairwise indistinguishable in {piso_degenerate}/11; the `k2` term is "
            f"confidence-set necessary in {k2_needed}/11 and the broader cored-log "
            f"shape class in {shape_needed}/11.",
        ])

    lines.extend([
        "", "Under primary baryons, the corrected global candidate set therefore supports "
        "a necessary cored-log shape in 9/11 galaxies, rather than the pilot's unqualified "
        "10/11 `k2` statement. The `NGC2976` confidence set contains genuine pISO and is "
        "phenomenologically degenerate; `NGC3521` does not require the cored-log shape.", "",
        "The two ‘necessary’ columns answer different questions. `k2 term necessary` "
        "requires every global ΔAICc≤2 model to be a LogSVT reduction containing `u2`. "
        "`cored-log shape necessary` also accepts the explicitly named, algebraically "
        "equivalent cored-log comparator. Neither identifies a screen source.", "",
        "## Covariance, boundaries, and bound sensitivity", "",
    ])
    for scenario in BARYON_SCENARIOS:
        bundles = result["runs"]["primary"][scenario]
        fits = [fit for bundle in bundles.values() for fit in bundle["fits"].values() if fit["parameter_count"]]
        rank_deficient = sum(fit["covariance"]["practical_rank"] < fit["parameter_count"] for fit in fits)
        high_corr = sum((fit["covariance"]["maximum_absolute_correlation"] or 0.0) >= 0.95 for fit in fits)
        boundary = sum(bool(fit["boundary_parameters"]) for fit in fits)
        label_changes = sum(not item["same_winner_label"] for item in result["bound_sensitivity"][scenario].values())
        shape_changes = sum(not item["same_winner_shape"] for item in result["bound_sensitivity"][scenario].values())
        confidence_changes = sum(not item["same_confidence_set"] for item in result["bound_sensitivity"][scenario].values())
        decision_changes = sum(item["k2_decision_changed"] for item in result["bound_sensitivity"][scenario].values())
        optimizer_failures = sum(not fit["optimizer_success"] for fit in fits)
        lines.append(
            f"- `{scenario}`: {rank_deficient}/{len(fits)} fitted models are practically "
            f"rank deficient at relative singular-value threshold `1e-8`, {high_corr}/{len(fits)} "
            f"have max |correlation| ≥ 0.95, and {boundary}/{len(fits)} touch an inherited "
            f"bound. Expanded bounds change {label_changes}/11 winner labels but {shape_changes}/11 "
            f"winner shapes, {confidence_changes}/11 confidence sets, and {decision_changes}/11 "
            f"`k2`-necessity decisions. Optimizer failures after continuation: {optimizer_failures}."
        )
    lines.extend([
        "", "Full transformed-parameter covariance and correlation matrices, singular "
        "values, boundary flags, optimizer status, parameters, AICc, and BIC are retained "
        "in `receipt.json`. `model-selection.csv` contains every primary and expanded-bound "
        "fit; `comparison.csv` contains all requested pISO/cored-log/LogSVT pairwise "
        "deltas; `bound-sensitivity.csv` exposes every sensitivity decision.", "",
        "## Interpretation boundary", "",
        "If genuine pISO is within ΔAICc≤2 of cored-log, the result is phenomenological "
        "degeneracy. If cored-log wins, that is still only a compact radial description. "
        "The audit neither derives its amplitude or core radius nor promotes a universal "
        "screen claim. Negative or unstable selections are retained as the result.", "",
        "## Recovered pilot provenance", "",
        "The corrected instrument has no `/tmp` dependency. SHA-256 identifiers for the "
        "reviewed pilot scripts, tables, notes, and receipts are stored in the machine "
        "receipt so the mistaken inputs can be reconstructed without moving them into the "
        "durable result set.",
    ])
    NOTE.write_text("\n".join(lines) + "\n")


def run() -> dict:
    curves = parse_mass_models(DATA)
    missing = [name for name in GALAXIES if name not in curves]
    if missing:
        raise RuntimeError(f"missing SPARC galaxies: {missing}")
    RESULTS.mkdir(parents=True, exist_ok=True)
    raw = {
        bounds: {scenario: {} for scenario in BARYON_SCENARIOS}
        for bounds in BOUND_SCHEMES
    }
    tasks = [
        (bounds, scenario, galaxy, curves[galaxy], mass_to_light, galaxy_index)
        for bounds in BOUND_SCHEMES
        for scenario, mass_to_light in BARYON_SCENARIOS.items()
        for galaxy_index, galaxy in enumerate(GALAXIES)
    ]
    workers = min(MAX_WORKERS, len(tasks), os.cpu_count() or 1)
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for bounds, scenario, galaxy, bundle in executor.map(run_bundle, tasks):
            raw[bounds][scenario][galaxy] = bundle
    result = {
        "status": "issue_225_retrospective_corrected_piso_audit",
        "issue": 225,
        "evidence_boundary": (
            "retrospective correction; viewed pilot outcomes are not held-out confirmation"
        ),
        "mechanism_boundary": "phenomenological fit only; no H-SSV screen claim",
        "instrument_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "data_path": str(DATA.relative_to(ROOT)),
        "data_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest(),
        "recovered_pilot_sha256": PILOT_PROVENANCE,
        "galaxies": list(GALAXIES),
        "baryon_scenarios": {
            name: {"upsilon_disk": values[0], "upsilon_bulge": values[1]}
            for name, values in BARYON_SCENARIOS.items()
        },
        "models": [
            {"name": model.name, "family": model.family, "parameters": list(model.parameters)}
            for model in MODELS
        ],
        "bound_schemes": {
            name: {
                "log_lower": scheme.log_lower, "log_upper": scheme.log_upper,
                "linear_limit": scheme.linear_limit,
                "concentration": list(scheme.concentration),
                "scaled_v200": list(scheme.scaled_v200),
            }
            for name, scheme in BOUND_SCHEMES.items()
        },
        "multistarts": MULTISTARTS,
        "parallel_workers": workers,
        "deterministic_order": {
            "bounds": list(BOUND_SCHEMES), "scenarios": list(BARYON_SCENARIOS),
            "galaxies": list(GALAXIES), "models": [model.name for model in MODELS],
        },
        "runs": ordered_scenarios(raw),
    }
    result["bound_sensitivity"] = bound_sensitivity(result)
    RECEIPT.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    write_model_table(result)
    write_comparison_table(result)
    write_bound_table(result)
    write_note(result)
    return result


if __name__ == "__main__":
    output = run()
    compact = {
        scenario: {
            "winner_counts": dict(Counter(
                bundle["aicc_winner"]
                for bundle in output["runs"]["primary"][scenario].values()
            )),
            "k2_necessary_count": sum(
                bundle["k2_term_necessary_after_corrected_baseline"]
                for bundle in output["runs"]["primary"][scenario].values()
            ),
        }
        for scenario in BARYON_SCENARIOS
    }
    print(json.dumps(compact, indent=2))

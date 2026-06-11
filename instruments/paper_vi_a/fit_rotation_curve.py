"""Fit the SSV-VI-a axisymmetric rotation-curve model to M31.

Data provenance
---------------
The script downloads the arXiv source for Chemin, Carignan & Foster (2009),
``H I Kinematics and Dynamics of Messier 31`` (arXiv:0909.3846), and parses
Table 4 from the LaTeX source.  That table lists the tilted-ring H I rotation
curve, uncertainties, H I surface density, inclination, and position angle.

The fit intentionally reports a modest, reproducible result rather than the old
unreceipted 7.5 km/s claim:

* SSV axisymmetric model: v = vf sqrt((1 - exp(-r/rt)) (1 + eps J0(pi r/dr)))
* smooth ablation: same central rise, eps fixed to 0
* NFW-shape comparison: halo-only circular-speed shape

By default the reported comparison uses r >= 4 kpc, excluding the strongly
perturbed inner warp/bar region discussed by Chemin et al.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
from scipy.optimize import curve_fit
from scipy.special import j0


ARXIV_EPRINT_URL = "https://arxiv.org/e-print/0909.3846"
DEFAULT_CACHE = Path("papers/SSV-VI/data/chemin2009_table4_m31_rotation_curve.csv")
DEFAULT_JSON = Path("papers/SSV-VI/results/m31_rotation_fit_receipt.json")
DEFAULT_SVG = Path("papers/SSV-VI/figures/fig_m31_rotation_fit_receipt.svg")

M31_BLACK_HOLE_MASS_MSUN = 1.4e8
C_KPC_MSUN = 1.8e9
DELTA_R_KPC = C_KPC_MSUN / M31_BLACK_HOLE_MASS_MSUN


@dataclass(frozen=True)
class FitResult:
    name: str
    params: dict[str, float]
    rms_kms: float
    wrms_kms: float
    aic: float


def _parse_float(cell: str) -> float | None:
    if "nodata" in cell or not cell.strip():
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?", cell)
    return float(match.group()) if match else None


def fetch_chemin_table() -> list[dict[str, float | None]]:
    with urllib.request.urlopen(ARXIV_EPRINT_URL, timeout=30) as response:
        payload = response.read()

    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        tex = archive.extractfile("lc1.tex")
        if tex is None:
            raise RuntimeError("lc1.tex not found in arXiv source archive")
        source = tex.read().decode("latin-1")

    label = source.find(r"\label{tab:rotcur}")
    start = source.rfind(r"\startdata", 0, label)
    end = source.find(r"\enddata", start)
    if min(label, start, end) < 0:
        raise RuntimeError("Could not locate Table 4 rotation-curve data")

    rows: list[dict[str, float | None]] = []
    for raw_line in source[start:end].splitlines()[1:]:
        line = raw_line.split(r"\\")[0].strip()
        if not line:
            continue
        cells = [part.strip() for part in line.split("&")]
        if len(cells) < 11:
            continue
        values = [_parse_float(cell) for cell in cells[:11]]
        rows.append(
            {
                "radius_arcmin": values[0],
                "radius_kpc": values[1],
                "pa_deg": values[2],
                "pa_err_deg": values[3],
                "pa_adopted_deg": values[4],
                "inclination_deg": values[5],
                "inclination_err_deg": values[6],
                "inclination_adopted_deg": values[7],
                "vrot_kms": values[8],
                "vrot_err_kms": values[9],
                "sigma_hi_msun_pc2": values[10],
            }
        )
    return rows


def write_cache(rows: list[dict[str, float | None]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_cache(path: Path) -> list[dict[str, float | None]]:
    rows: list[dict[str, float | None]] = []
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append({key: (float(value) if value else None) for key, value in row.items()})
    return rows


def load_rows(cache: Path, refresh: bool) -> list[dict[str, float | None]]:
    if refresh or not cache.exists():
        rows = fetch_chemin_table()
        write_cache(rows, cache)
        return rows
    return read_cache(cache)


def arrays_from_rows(rows: list[dict[str, float | None]], r_min: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    triples = [
        (row["radius_kpc"], row["vrot_kms"], row["vrot_err_kms"])
        for row in rows
        if row["radius_kpc"] is not None and row["vrot_kms"] is not None and row["radius_kpc"] >= r_min
    ]
    radius = np.array([item[0] for item in triples], dtype=float)
    velocity = np.array([item[1] for item in triples], dtype=float)
    error = np.array([item[2] if item[2] is not None and item[2] > 0 else 10.0 for item in triples], dtype=float)
    return radius, velocity, error


def ssv_model(radius: np.ndarray, v_flat: float, r_transition: float, epsilon: float) -> np.ndarray:
    k = math.pi / DELTA_R_KPC
    envelope = 1.0 - np.exp(-radius / r_transition)
    wave = 1.0 + epsilon * j0(k * radius)
    return v_flat * np.sqrt(np.maximum(envelope * wave, 1.0e-12))


def smooth_model(radius: np.ndarray, v_flat: float, r_transition: float) -> np.ndarray:
    envelope = 1.0 - np.exp(-radius / r_transition)
    return v_flat * np.sqrt(np.maximum(envelope, 1.0e-12))


def nfw_shape_model(radius: np.ndarray, v_scale: float, r_scale: float) -> np.ndarray:
    x = np.maximum(radius / r_scale, 1.0e-12)
    shape = (np.log1p(x) - x / (1.0 + x)) / x
    return v_scale * np.sqrt(np.maximum(shape, 1.0e-12))


def fit_model(
    name: str,
    func: Callable[..., np.ndarray],
    radius: np.ndarray,
    velocity: np.ndarray,
    error: np.ndarray,
    p0: tuple[float, ...],
    bounds: tuple[tuple[float, ...], tuple[float, ...]],
    param_names: tuple[str, ...],
) -> tuple[FitResult, np.ndarray]:
    best_params, _ = curve_fit(
        func,
        radius,
        velocity,
        p0=p0,
        bounds=bounds,
        sigma=error,
        absolute_sigma=False,
        maxfev=50_000,
    )
    predicted = func(radius, *best_params)
    residual = predicted - velocity
    rms = float(np.sqrt(np.mean(residual**2)))
    wrms = float(np.sqrt(np.mean((residual / error) ** 2)) * np.mean(error))
    rss = float(np.sum(residual**2))
    n = len(radius)
    k_params = len(best_params)
    aic = float(n * math.log(max(rss / n, 1.0e-30)) + 2 * k_params)
    return (
        FitResult(
            name=name,
            params={param_names[i]: float(best_params[i]) for i in range(k_params)},
            rms_kms=rms,
            wrms_kms=wrms,
            aic=aic,
        ),
        predicted,
    )


def make_svg(path: Path, radius: np.ndarray, velocity: np.ndarray, curves: dict[str, np.ndarray]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = 900, 520
    left, right, top, bottom = 70, 24, 24, 58
    xmin, xmax = float(np.min(radius)), float(np.max(radius))
    ymin, ymax = 180.0, 285.0

    def sx(x: float) -> float:
        return left + (x - xmin) / (xmax - xmin) * (width - left - right)

    def sy(y: float) -> float:
        return top + (ymax - y) / (ymax - ymin) * (height - top - bottom)

    def polyline(y_values: np.ndarray) -> str:
        points = " ".join(f"{sx(float(x)):.1f},{sy(float(y)):.1f}" for x, y in zip(radius, y_values))
        return points

    colors = {"SSV": "#1f5fbf", "smooth": "#777777", "NFW shape": "#c53b3b"}
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#222"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#222"/>',
        f'<text x="{width/2}" y="{height-16}" text-anchor="middle" font-family="sans-serif" font-size="16">Radius (kpc)</text>',
        f'<text x="18" y="{height/2}" transform="rotate(-90 18 {height/2})" text-anchor="middle" font-family="sans-serif" font-size="16">v_rot (km/s)</text>',
    ]
    for tick in range(5, 40, 5):
        elements.append(f'<line x1="{sx(tick):.1f}" y1="{height-bottom}" x2="{sx(tick):.1f}" y2="{height-bottom+5}" stroke="#222"/>')
        elements.append(f'<text x="{sx(tick):.1f}" y="{height-bottom+22}" text-anchor="middle" font-family="sans-serif" font-size="12">{tick}</text>')
    for tick in range(200, 281, 20):
        elements.append(f'<line x1="{left-5}" y1="{sy(tick):.1f}" x2="{left}" y2="{sy(tick):.1f}" stroke="#222"/>')
        elements.append(f'<text x="{left-10}" y="{sy(tick)+4:.1f}" text-anchor="end" font-family="sans-serif" font-size="12">{tick}</text>')
        elements.append(f'<line x1="{left}" y1="{sy(tick):.1f}" x2="{width-right}" y2="{sy(tick):.1f}" stroke="#eee"/>')

    for x, y in zip(radius, velocity):
        elements.append(f'<circle cx="{sx(float(x)):.1f}" cy="{sy(float(y)):.1f}" r="2.6" fill="#111" opacity="0.75"/>')

    for name, y_values in curves.items():
        elements.append(
            f'<polyline points="{polyline(y_values)}" fill="none" stroke="{colors[name]}" stroke-width="2.5"/>'
        )

    legend_x, legend_y = 690, 44
    elements.append(f'<rect x="{legend_x-18}" y="{legend_y-24}" width="188" height="86" fill="white" stroke="#ccc"/>')
    legend = [("data", "#111"), ("SSV", colors["SSV"]), ("smooth", colors["smooth"]), ("NFW shape", colors["NFW shape"])]
    for i, (name, color) in enumerate(legend):
        y = legend_y + i * 19
        if name == "data":
            elements.append(f'<circle cx="{legend_x}" cy="{y}" r="3" fill="{color}"/>')
        else:
            elements.append(f'<line x1="{legend_x-8}" y1="{y}" x2="{legend_x+8}" y2="{y}" stroke="{color}" stroke-width="3"/>')
        elements.append(f'<text x="{legend_x+18}" y="{y+4}" font-family="sans-serif" font-size="13">{name}</text>')
    elements.append("</svg>")
    path.write_text("\n".join(elements) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--refresh-data", action="store_true")
    parser.add_argument("--r-min", type=float, default=4.0)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--svg-out", type=Path, default=DEFAULT_SVG)
    args = parser.parse_args()

    rows = load_rows(args.cache, args.refresh_data)
    radius, velocity, error = arrays_from_rows(rows, args.r_min)

    ssv_fit, ssv_pred = fit_model(
        "SSV",
        ssv_model,
        radius,
        velocity,
        error,
        p0=(250.0, 1.2, -0.25),
        bounds=((100.0, 0.05, -0.8), (400.0, 20.0, 0.8)),
        param_names=("v_flat_kms", "r_transition_kpc", "epsilon"),
    )
    smooth_fit, smooth_pred = fit_model(
        "smooth",
        smooth_model,
        radius,
        velocity,
        error,
        p0=(250.0, 2.0),
        bounds=((100.0, 0.05), (400.0, 20.0)),
        param_names=("v_flat_kms", "r_transition_kpc"),
    )
    nfw_fit, nfw_pred = fit_model(
        "NFW shape",
        nfw_shape_model,
        radius,
        velocity,
        error,
        p0=(550.0, 7.0),
        bounds=((1.0, 0.1), (1000.0, 200.0)),
        param_names=("v_scale_kms", "r_scale_kpc"),
    )

    results = {
        "source": {
            "paper": "Chemin, Carignan & Foster (2009), ApJ 705, 1395",
            "arxiv": "0909.3846",
            "table": "Table 4",
            "cache": str(args.cache),
        },
        "fit_domain": {"r_min_kpc": args.r_min, "r_max_kpc": float(np.max(radius)), "n_points": int(len(radius))},
        "fixed_parameters": {
            "m31_black_hole_mass_msun": M31_BLACK_HOLE_MASS_MSUN,
            "c_kpc_msun": C_KPC_MSUN,
            "delta_r_kpc": DELTA_R_KPC,
        },
        "fits": [fit.__dict__ for fit in (ssv_fit, smooth_fit, nfw_fit)],
        "deltas": {
            "ssv_minus_smooth_rms_kms": ssv_fit.rms_kms - smooth_fit.rms_kms,
            "ssv_minus_nfw_shape_rms_kms": ssv_fit.rms_kms - nfw_fit.rms_kms,
            "ssv_minus_smooth_aic": ssv_fit.aic - smooth_fit.aic,
            "ssv_minus_nfw_shape_aic": ssv_fit.aic - nfw_fit.aic,
        },
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(results, indent=2) + "\n")
    make_svg(args.svg_out, radius, velocity, {"SSV": ssv_pred, "smooth": smooth_pred, "NFW shape": nfw_pred})

    print("SSV-VI-a M31 rotation-curve receipt")
    print("=" * 72)
    print(f"Source: Chemin et al. 2009 arXiv:0909.3846 Table 4")
    print(f"Fit domain: r >= {args.r_min:.2f} kpc, n = {len(radius)}")
    print(f"Fixed Delta r: {DELTA_R_KPC:.3f} kpc")
    for fit in (ssv_fit, smooth_fit, nfw_fit):
        params = ", ".join(f"{key}={value:.4g}" for key, value in fit.params.items())
        print(f"{fit.name:<10} RMS={fit.rms_kms:6.2f} km/s  AIC={fit.aic:7.2f}  {params}")
    print(f"Wrote {args.json_out}")
    print(f"Wrote {args.svg_out}")


if __name__ == "__main__":
    main()

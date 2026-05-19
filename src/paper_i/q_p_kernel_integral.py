"""Compute the long-wavelength Q_p kernel integral from saved static trefoil states.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1, longitudinal speed c = 1
Primary observables: deficit-volume kernel integral and its (a_p / xi)^3 suppression
Primary role: evaluate the analytic Q_p object that the current static branch can honestly resolve
Key limitation: this script computes the long-wavelength kernel limit only; sub-grain corrections below the grid scale are not yet resolved.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from trefoil_observables import deficit_volume


DEFAULT_AP_OVER_XI = 1.0 / 1836.15267343


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute the long-wavelength Q_p kernel integral from saved trefoil states.")
    parser.add_argument("states", nargs="+", type=Path, help="Saved .npz states from trefoil_breather_static.py")
    parser.add_argument(
        "--ap-over-xi",
        type=float,
        default=DEFAULT_AP_OVER_XI,
        help="Cross-defect scale ratio a_p / xi. Default uses m_e / m_p.",
    )
    parser.add_argument(
        "--window",
        choices=("full_support",),
        default="full_support",
        help="Resolved proton-support window. Only full_support is currently implemented.",
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def relative_drift(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-12)


def metric_span(values: list[float]) -> dict[str, float]:
    if not values:
        return {"min": 0.0, "max": 0.0, "span": 0.0, "relative_span": 0.0}
    v_min = min(values)
    v_max = max(values)
    span = v_max - v_min
    scale = max(abs(v_min), abs(v_max), 1.0e-12)
    return {"min": v_min, "max": v_max, "span": span, "relative_span": span / scale}


def load_state(path: Path, ap_over_xi: float, window: str) -> dict[str, float]:
    data = np.load(path, allow_pickle=False)
    psi = data["psi_real"] + 1j * data["psi_imag"]
    x = data["x"]
    config = json.loads(str(data["config"]))
    summary = json.loads(str(data["summary"]))

    spacing = float(x[1, 0, 0] - x[0, 0, 0]) if x.shape[0] > 1 else 0.0
    delta_v = deficit_volume(psi, spacing)

    if window != "full_support":
        raise ValueError(f"Unsupported window: {window}")

    kernel_prefactor = ap_over_xi**3
    q_p_kernel = kernel_prefactor * delta_v

    return {
        "state": path.as_posix(),
        "n": int(config["n"]),
        "half_width": float(config["half_width"]),
        "steps_completed": int(summary["steps_completed"]),
        "residual_norm": float(summary["residual_norm"]),
        "shell_mean_density": float(1.0 - summary["far_field_shell_deficit"]),
        "shell_mean_deficit": float(summary["far_field_shell_deficit"]),
        "deficit_volume": float(delta_v),
        "kernel_prefactor": float(kernel_prefactor),
        "q_p_kernel_long_wavelength": float(q_p_kernel),
    }


def main() -> None:
    args = parse_args()
    rows = [load_state(path, args.ap_over_xi, args.window) for path in args.states]
    rows.sort(key=lambda row: (row["n"], row["half_width"], row["steps_completed"]))

    by_n: dict[int, list[dict[str, float]]] = {}
    by_half_width: dict[float, list[dict[str, float]]] = {}
    for row in rows:
        by_n.setdefault(int(row["n"]), []).append(row)
        by_half_width.setdefault(float(row["half_width"]), []).append(row)

    by_n_summary = {
        str(n): {
            "half_width_values": [float(row["half_width"]) for row in entries],
            "deficit_volume": metric_span([float(row["deficit_volume"]) for row in entries]),
            "q_p_kernel_long_wavelength": metric_span([float(row["q_p_kernel_long_wavelength"]) for row in entries]),
            "shell_mean_density": metric_span([float(row["shell_mean_density"]) for row in entries]),
        }
        for n, entries in sorted(by_n.items())
    }

    cross_resolution = {}
    for half_width, entries in sorted(by_half_width.items()):
        if len(entries) < 2:
            continue
        entries = sorted(entries, key=lambda row: row["n"])
        coarse = entries[0]
        fine = entries[-1]
        cross_resolution[str(half_width)] = {
            "coarse_n": int(coarse["n"]),
            "fine_n": int(fine["n"]),
            "deficit_volume": {
                "coarse": float(coarse["deficit_volume"]),
                "fine": float(fine["deficit_volume"]),
                "relative_drift": relative_drift(float(coarse["deficit_volume"]), float(fine["deficit_volume"])),
            },
            "q_p_kernel_long_wavelength": {
                "coarse": float(coarse["q_p_kernel_long_wavelength"]),
                "fine": float(fine["q_p_kernel_long_wavelength"]),
                "relative_drift": relative_drift(
                    float(coarse["q_p_kernel_long_wavelength"]), float(fine["q_p_kernel_long_wavelength"])
                ),
            },
            "shell_mean_density": {
                "coarse": float(coarse["shell_mean_density"]),
                "fine": float(fine["shell_mean_density"]),
                "relative_drift": relative_drift(float(coarse["shell_mean_density"]), float(fine["shell_mean_density"])),
            },
            "residual_norm": {
                "coarse": float(coarse["residual_norm"]),
                "fine": float(fine["residual_norm"]),
                "relative_drift": relative_drift(float(coarse["residual_norm"]), float(fine["residual_norm"])),
            },
        }

    payload = {
        "ap_over_xi": float(args.ap_over_xi),
        "window": args.window,
        "rows": rows,
        "by_n": by_n_summary,
        "cross_resolution": cross_resolution,
        "interpretation": {
            "purpose": "Compute the long-wavelength Q_p kernel integral Q_p = deltaV * (a_p / xi)^3 from saved static proton states.",
            "carrier_scale": "xi is the electron healing length of the surrounding medium, not the proton grain length a_p.",
            "warning": "This is the long-wavelength kernel limit only. Any sub-grain operator beyond this limit is unresolved on the current grid.",
        },
    }

    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

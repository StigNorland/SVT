"""Compare radial far-field profiles from saved static trefoil states.

Status: candidate
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1
Primary observables: per-bin differences in mean density and mean deficit
Primary role: compare outer-profile sensitivity across saved prototype states for issue #13
Key limitation: assumes profiles were binned compatibly; it is a diagnostic comparator, not a physics result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two saved trefoil far-field profile JSON files.")
    parser.add_argument("profile_a", type=Path)
    parser.add_argument("profile_b", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def load_profile(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compare_profiles(profile_a: dict, profile_b: dict) -> dict[str, object]:
    rows_a = profile_a["profile"]
    rows_b = profile_b["profile"]
    if len(rows_a) != len(rows_b):
        raise ValueError("Profiles have different bin counts.")

    rows = []
    density_diffs = []
    deficit_diffs = []
    r_max_a = max(row["r_outer"] for row in rows_a) if rows_a else 1.0
    r_max_b = max(row["r_outer"] for row in rows_b) if rows_b else 1.0
    for idx, (row_a, row_b) in enumerate(zip(rows_a, rows_b)):
        density_diff = row_b["mean_density"] - row_a["mean_density"]
        deficit_diff = row_b["mean_deficit"] - row_a["mean_deficit"]
        density_diffs.append(abs(density_diff))
        deficit_diffs.append(abs(deficit_diff))
        rows.append(
            {
                "bin_index": idx,
                "r_mid": row_a["r_mid"],
                "r_mid_a": row_a["r_mid"],
                "r_mid_b": row_b["r_mid"],
                "r_frac_a": row_a["r_mid"] / r_max_a if r_max_a else 0.0,
                "r_frac_b": row_b["r_mid"] / r_max_b if r_max_b else 0.0,
                "density_a": row_a["mean_density"],
                "density_b": row_b["mean_density"],
                "density_diff": density_diff,
                "deficit_a": row_a["mean_deficit"],
                "deficit_b": row_b["mean_deficit"],
                "deficit_diff": deficit_diff,
            }
        )

    return {
        "max_abs_density_diff": max(density_diffs) if density_diffs else 0.0,
        "max_abs_deficit_diff": max(deficit_diffs) if deficit_diffs else 0.0,
        "mean_abs_density_diff": sum(density_diffs) / len(density_diffs) if density_diffs else 0.0,
        "mean_abs_deficit_diff": sum(deficit_diffs) / len(deficit_diffs) if deficit_diffs else 0.0,
        "rows": rows,
    }


def main() -> None:
    args = parse_args()
    profile_a = load_profile(args.profile_a)
    profile_b = load_profile(args.profile_b)
    comparison = compare_profiles(profile_a, profile_b)
    payload = {
        "profile_a": str(args.profile_a),
        "profile_b": str(args.profile_b),
        "comparison": comparison,
    }
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

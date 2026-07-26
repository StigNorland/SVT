"""Literal Paper-I SSV target audit for issue #180.

Problem type
------------
Analytic/symbolic validation of the printed nonrelativistic LogSE.  This is
not a replacement model and it performs no fit.

Conventions
-----------
The target equation is written

    i hbar d_t psi = -hbar^2 nabla^2 psi/(2m) - B ln(n/n0) psi,

where B = b*rho0 > 0 in Paper I and the homogeneous target background has
n/n0 = 1.  Natural units are optional; functions retain hbar explicitly.

Reported diagnostics
--------------------
* exact Bogoliubov dispersion of the printed equation;
* its modulational-instability band;
* comparison with the positive dispersion printed in Paper I;
* thermodynamic pressure derived from the printed potential;
* a minimal dimensional-consistency ledger.

Run
---
    python instruments/model_hssv/ssv_target_audit.py --write
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "papers" / "H-SSV" / "results" / "issue-180" / "receipt.json"


def nls_bdg_omega2(k: float | np.ndarray, m: float, B: float,
                   hbar: float = 1.0) -> float | np.ndarray:
    """Exact omega^2 for the printed uniform-background LogSE.

    With epsilon_k = hbar^2 k^2/(2m),

        hbar^2 omega^2 = epsilon_k (epsilon_k - 2B).

    Thus B>0 is focusing and the uniform state is modulationally unstable.
    """
    epsilon = hbar * hbar * np.asarray(k) ** 2 / (2.0 * m)
    result = epsilon * (epsilon - 2.0 * B) / (hbar * hbar)
    if np.ndim(result) == 0:
        return float(result)
    return result


def instability_band_edge(m: float, B: float, hbar: float = 1.0) -> float:
    """Largest unstable wavenumber for B>0; zero when B<=0."""
    if B <= 0:
        return 0.0
    return 2.0 * math.sqrt(m * B) / hbar


def actual_longwave_c2(m: float, B: float) -> float:
    """Coefficient lim_{k->0} omega^2/k^2 of the printed equation."""
    return -B / m


def paper_claimed_c2(m: float, B: float) -> float:
    """Paper-I claim c_s^2 = 2 b rho0/m = 2B/m."""
    return 2.0 * B / m


def paper_claimed_xi(m: float, B: float, hbar: float = 1.0) -> float:
    """Paper-I claim xi = hbar/sqrt(2mB)."""
    return hbar / math.sqrt(2.0 * m * B)


def paper_claimed_omega2(k: float | np.ndarray, m: float, B: float,
                         hbar: float = 1.0) -> float | np.ndarray:
    """Dispersion printed in Paper I using its c_s and xi definitions."""
    k_arr = np.asarray(k)
    c2 = paper_claimed_c2(m, B)
    xi = paper_claimed_xi(m, B, hbar)
    result = c2 * k_arr * k_arr * (1.0 + k_arr * k_arr * xi * xi)
    if np.ndim(result) == 0:
        return float(result)
    return result


def pressure_from_printed_potential(rho: float, b: float,
                                    vacuum_constant: float = 0.0) -> float:
    """Thermodynamic P=rho V'(rho)-V for Paper-I's printed potential.

    V = -b rho[ln(rho/rhobar)-1] + V0 gives P = -b rho - V0.
    The derivative dP/drho=-b is negative for the declared b>0.
    """
    return -b * rho - vacuum_constant


def symbolic_dispersion() -> sp.Expr:
    """Return the determinant-derived hbar^2 omega^2 expression."""
    eps, B = sp.symbols("epsilon B", positive=True, real=True)
    return sp.factor(eps * (eps - 2 * B))


def printed_dimensions_ledger() -> dict[str, Any]:
    """Minimal normalization audit under Paper I's |Psi|^2=rho/rho0.

    The printed relation b*rho0 ~ energy makes each displayed term readable
    as an energy per reference element.  It does not, however, uniquely define
    a local action density to integrate over physical d^3x: that reading needs
    a common density/volume normalization.  This ambiguity does not affect the
    EOM sign or the instability result, so it is recorded but not used as the
    decisive failure.
    """
    return {
        "psi_dimensionless": True,
        "rho_is_physical_density_in_paper": True,
        "time_term_with_printed_prefactor": "energy",
        "gradient_term_with_printed_prefactor": "energy",
        "potential_with_b_rho0_as_energy": "energy",
        "terms_consistent_as_energy_per_reference_element": True,
        "physical_action_density_normalization_specified": False,
        "unique_physical_action_normalization": False,
    }


def run() -> dict[str, Any]:
    m, B, hbar = 1.0, 0.1, 1.0
    k_edge = instability_band_edge(m, B, hbar)
    probes = np.array([0.1, 0.25, 0.5, 0.9 * k_edge])
    actual = nls_bdg_omega2(probes, m, B, hbar)
    claimed = paper_claimed_omega2(probes, m, B, hbar)
    return {
        "issue": 180,
        "instrument": "ssv_target_audit",
        "status": "closure-grade",
        "target": {
            "equation_coefficient": "-B ln(n/n0)",
            "declared_sign": "B=b*rho0>0",
        },
        "symbolic": {
            "hbar2_omega2": "epsilon_k*(epsilon_k-2*B)",
            "actual_longwave_c2": "-B/m",
            "paper_claimed_c2": "2*B/m",
            "unstable_for": "0<k<2*sqrt(m*B)/hbar",
            "pressure": "-b*rho-V0",
            "dP_drho": "-b",
        },
        "control_point": {
            "m": m,
            "B": B,
            "hbar": hbar,
            "k_edge": k_edge,
            "k": probes.tolist(),
            "actual_omega2": np.asarray(actual).tolist(),
            "paper_claimed_omega2": np.asarray(claimed).tolist(),
        },
        "dimensions": printed_dimensions_ledger(),
        "gates": {
            "P0_action_normalization_unique": False,
            "P0_uniform_background_stable": False,
        },
        "verdict": (
            "FAIL: the literal B>0 printed LogSE has a long-wavelength "
            "modulational instability and does not yield the claimed positive "
            "sound cone. The action-density normalization is also under-"
            "specified, but that ambiguity is not needed for the failure."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true",
                        help="write/update the issue-180 machine receipt")
    args = parser.parse_args()
    report = run()
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.write:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"Wrote {RECEIPT}")


if __name__ == "__main__":
    main()

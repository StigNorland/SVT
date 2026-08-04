"""Issue #227: Newtonian-to-galactic response audit for the C4 screen.

No galaxy data are loaded.  The instrument checks the preregistered transport
controls and the saturated-patch/min-cut construction, including the exact C4
availability map and the unresolved regulator/dynamical closures.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, pi, sqrt
from typing import Any

import numpy as np

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
M_SUN = 1.98847e30
AU = 149_597_870_700.0
A_COMPARISON = 1.2e-10


@dataclass(frozen=True)
class Dim:
    mass: int = 0
    length: int = 0
    time: int = 0

    def __mul__(self, other: "Dim") -> "Dim":
        return Dim(
            self.mass + other.mass,
            self.length + other.length,
            self.time + other.time,
        )

    def __truediv__(self, other: "Dim") -> "Dim":
        return Dim(
            self.mass - other.mass,
            self.length - other.length,
            self.time - other.time,
        )

    def __pow__(self, exponent: int) -> "Dim":
        return Dim(
            self.mass * exponent,
            self.length * exponent,
            self.time * exponent,
        )


ONE = Dim()
MASS = Dim(mass=1)
LENGTH = Dim(length=1)
TIME = Dim(time=1)
VELOCITY = LENGTH / TIME
ACCELERATION = LENGTH / TIME**2
G_DIM = LENGTH**3 / MASS / TIME**2


def dimensional_audit() -> dict[str, Any]:
    ell = LENGTH
    m_site = MASS
    nu = ONE / TIME
    tau = TIME
    c = VELOCITY
    G = G_DIM
    radius = ell  # sqrt(M/m_site) is dimensionless.
    a_service = c**2 * tau * nu / ell
    a_capacity = G * m_site / ell**2
    velocity_sq = a_service * radius
    return {
        "core_radius": [radius.mass, radius.length, radius.time],
        "service_acceleration": [
            a_service.mass,
            a_service.length,
            a_service.time,
        ],
        "capacity_acceleration": [
            a_capacity.mass,
            a_capacity.length,
            a_capacity.time,
        ],
        "velocity_squared": [
            velocity_sq.mass,
            velocity_sq.length,
            velocity_sq.time,
        ],
        "accelerations_match": a_service == ACCELERATION
        and a_capacity == ACCELERATION,
        "velocity_squared_matches": velocity_sq == VELOCITY**2,
    }


def local_3d_acceleration(mass: float, radius: float, G: float = G_NEWTON) -> float:
    if mass <= 0 or radius <= 0 or G <= 0:
        raise ValueError("mass, radius and G must be positive")
    return G * mass / radius**2


def local_flux_control(mass: float = 7.0, eta: float = 3.0, radius: float = 2.0) -> dict[str, Any]:
    if mass <= 0 or eta <= 0 or radius <= 0:
        raise ValueError("mass, eta and radius must be positive")
    demand = eta * mass
    flux = demand / (4.0 * pi * radius**2)
    return {
        "demand": demand,
        "flux": flux,
        "gauss_reconstruction": 4.0 * pi * radius**2 * flux,
        "conserved": np.isclose(
            4.0 * pi * radius**2 * flux, demand, atol=1.0e-12, rtol=0
        ),
        "radial_power": -2,
        "G_status": "INPUT unless kappa_3 and eta are independently known",
    }


def linear_2d_velocity_squared(mass: np.ndarray | float, coupling: float = 1.0):
    if coupling <= 0 or np.any(np.asarray(mass) <= 0):
        raise ValueError("mass and coupling must be positive")
    return coupling * np.asarray(mass, dtype=float)


def matched_capacity_scales(
    mass: np.ndarray | float,
    a_star: float,
    G: float = G_NEWTON,
) -> tuple[np.ndarray, np.ndarray]:
    masses = np.asarray(mass, dtype=float)
    if np.any(masses <= 0) or a_star <= 0 or G <= 0:
        raise ValueError("mass, a_star and G must be positive")
    core_radius = np.sqrt(G * masses / a_star)
    velocity_squared = np.sqrt(G * masses * a_star)
    return core_radius, velocity_squared


def microscopic_capacity_scales(
    mass: float,
    ell_site: float,
    mass_site: float,
    nu_site: float,
    response_time: float,
    G: float = G_NEWTON,
) -> dict[str, Any]:
    values = (mass, ell_site, mass_site, nu_site, response_time, G)
    if any(value <= 0 for value in values):
        raise ValueError("all microscopic capacity inputs must be positive")
    core_radius = ell_site * sqrt(mass / (pi * mass_site))
    cut_size = 2.0 * pi * core_radius / ell_site
    cut_throughput = nu_site * cut_size
    a_service = C_LIGHT**2 * response_time * nu_site / ell_site
    a_capacity = pi * G * mass_site / ell_site**2
    velocity_squared = a_service * core_radius
    return {
        "core_radius": core_radius,
        "cut_size": cut_size,
        "cut_throughput": cut_throughput,
        "a_service": a_service,
        "a_capacity": a_capacity,
        "closure_ratio_a_service_over_a_capacity": a_service / a_capacity,
        "velocity_squared": velocity_squared,
        "btfr_acceleration": velocity_squared**2 / (G * mass),
    }


def mass_scaling_audit() -> dict[str, Any]:
    masses = np.logspace(7, 12, 51)
    v2_linear = linear_2d_velocity_squared(masses)
    _, v2_mincut = matched_capacity_scales(masses, a_star=1.0, G=1.0)
    v_linear = np.sqrt(v2_linear)
    v_mincut = np.sqrt(v2_mincut)
    slope_v_linear = float(np.polyfit(np.log10(masses), np.log10(v_linear), 1)[0])
    slope_v_mincut = float(np.polyfit(np.log10(masses), np.log10(v_mincut), 1)[0])
    return {
        "linear_2d_velocity_mass_exponent": slope_v_linear,
        "linear_2d_M_vs_V_slope": 1.0 / slope_v_linear,
        "mincut_velocity_mass_exponent": slope_v_mincut,
        "mincut_M_vs_V_slope": 1.0 / slope_v_mincut,
        "observational_acceptance_interval": [3.5, 4.0],
        "linear_2d_fails_btfr": not 3.5 <= 1.0 / slope_v_linear <= 4.0,
        "mincut_passes_btfr_exponent": bool(
            np.isclose(1.0 / slope_v_mincut, 4.0, atol=1.0e-12, rtol=0)
        ),
    }


def cored_log_kernel(radius: np.ndarray, core_radius: float) -> np.ndarray:
    return core_radius**2 / (pi * (radius**2 + core_radius**2) ** 2)


def gaussian_kernel(radius: np.ndarray, core_radius: float) -> np.ndarray:
    return np.exp(-(radius / core_radius) ** 2) / (pi * core_radius**2)


def cored_log_acceleration(radius: np.ndarray | float, core_radius: float, v2: float):
    radii = np.asarray(radius, dtype=float)
    if core_radius <= 0 or v2 <= 0 or np.any(radii < 0):
        raise ValueError("radii must be non-negative; core_radius and v2 positive")
    return v2 * radii / (radii**2 + core_radius**2)


def gaussian_core_acceleration(radius: np.ndarray | float, core_radius: float, v2: float):
    radii = np.asarray(radius, dtype=float)
    if core_radius <= 0 or v2 <= 0 or np.any(radii < 0):
        raise ValueError("radii must be non-negative; core_radius and v2 positive")
    result = np.zeros_like(radii)
    nonzero = radii > 0
    result[nonzero] = v2 * (
        1.0 - np.exp(-(radii[nonzero] / core_radius) ** 2)
    ) / radii[nonzero]
    return result


def regulator_nonuniqueness_audit(core_radius: float = 2.0, v2: float = 3.0) -> dict[str, Any]:
    if core_radius <= 0 or v2 <= 0:
        raise ValueError("core_radius and v2 must be positive")
    # Log-spaced integration to 1e4 r_c resolves both normalized kernels.
    radii = np.concatenate(
        ([0.0], np.logspace(-7, 4, 200_000) * core_radius)
    )
    norm_cl = float(
        np.trapezoid(2.0 * pi * radii * cored_log_kernel(radii, core_radius), radii)
    )
    norm_gauss = float(
        np.trapezoid(2.0 * pi * radii * gaussian_kernel(radii, core_radius), radii)
    )
    at_core_cl = float(cored_log_acceleration(core_radius, core_radius, v2))
    at_core_gauss = float(gaussian_core_acceleration(core_radius, core_radius, v2))
    small = 1.0e-6 * core_radius
    large = 1.0e6 * core_radius
    return {
        "cored_log_kernel_norm": norm_cl,
        "gaussian_kernel_norm": norm_gauss,
        "cored_log_acceleration_at_core": at_core_cl,
        "gaussian_acceleration_at_core": at_core_gauss,
        "relative_difference_at_core": abs(at_core_gauss - at_core_cl) / at_core_cl,
        "both_linear_at_origin": np.isclose(
            float(cored_log_acceleration(small, core_radius, v2)) / small,
            float(gaussian_core_acceleration(small, core_radius, v2)) / small,
            rtol=1.0e-4,
            atol=0,
        ),
        "both_flat_curve_asymptote": (
            np.isclose(
                float(cored_log_acceleration(large, core_radius, v2)) * large,
                v2,
                rtol=1.0e-10,
            )
            and np.isclose(
                float(gaussian_core_acceleration(large, core_radius, v2)) * large,
                v2,
                rtol=1.0e-10,
            )
        ),
        "C4_does_not_select_regulator": True,
    }


def exact_availability_audit(
    radius: float = 3.0,
    core_radius: float = 2.0,
    outer_radius: float = 100.0,
    v2: float = 4.0e10,
    c: float = C_LIGHT,
) -> dict[str, Any]:
    if not (0 <= radius < outer_radius) or min(core_radius, v2, c) <= 0:
        raise ValueError("invalid availability-domain inputs")
    potential = 0.5 * v2 * log(
        (radius**2 + core_radius**2) / (outer_radius**2 + core_radius**2)
    )
    availability = exp(potential / c**2)
    load = 1.0 - availability
    acceleration = float(cored_log_acceleration(radius, core_radius, v2))
    return {
        "potential": potential,
        "availability": availability,
        "load": load,
        "acceleration": acceleration,
        "potential_nonpositive": potential <= 0.0,
        "availability_valid": 0.0 < availability <= 1.0,
        "load_valid": 0.0 <= load < 1.0,
        "exact_C4_identity": np.isclose(availability, 1.0 - load, atol=1e-15),
    }


def conditional_solar_audit(a_star: float = A_COMPARISON) -> dict[str, Any]:
    if a_star <= 0:
        raise ValueError("a_star must be positive")
    core_radius, v2 = matched_capacity_scales(M_SUN, a_star)
    core = float(core_radius)
    velocity_sq = float(v2)
    rows = {}
    for name, radius in {"Earth": AU, "Saturn": 9.58 * AU}.items():
        g_screen = float(cored_log_acceleration(radius, core, velocity_sq))
        g_newton = local_3d_acceleration(M_SUN, radius)
        rows[name] = {
            "radius_AU": radius / AU,
            "g_screen_m_s2": g_screen,
            "g_newton_m_s2": g_newton,
            "screen_fraction": g_screen / g_newton,
        }
    return {
        "comparison_only_a_star_m_s2": a_star,
        "solar_core_radius_AU": core / AU,
        "rows": rows,
        "external_field_Q2_prediction": None,
        "external_field_reason": (
            "C4/T3 does not define how the Galactic shared patch changes the "
            "Solar-System remote marginal or tidal field"
        ),
    }


def dynamic_constraint_audit() -> dict[str, Any]:
    return {
        "C4_speed_statement": "c_screen <= c",
        "GW170817_required_fractional_interval": [-3.0e-15, 7.0e-16],
        "speed_equality_derived": False,
        "binary_radiation_action_supplied": False,
        "binary_orbital_decay_prediction_supplied": False,
        "polarization_prediction_supplied": False,
        "preferred_frame": "none in C4 causal partial order",
        "G6_pass": False,
    }


GATES: dict[str, dict[str, str]] = {
    "T0_local_3d_flux": {
        "G1": "PASS CONDITIONALLY -- inverse square from 3D Gauss flux; G imported",
        "G2": "FAIL -- no transition or galactic core",
        "G3": "FAIL -- no flat-curve asymptote",
        "G4": "PASS STATIC ONLY -- conservative central field",
        "G5": "FAIL -- no galactic population law",
        "G6": "FAIL -- no complete dynamic/local response",
    },
    "T1_linear_2d_flux": {
        "G1": "FAIL -- 1/r acceleration at local scales",
        "G2": "FAIL -- logarithmic at every scale and no derived core",
        "G3": "FAIL -- V^4 proportional to M^2",
        "G4": "PASS STATIC ONLY -- conservative potential",
        "G5": "FAIL -- wrong population exponent",
        "G6": "FAIL -- local limit already wrong",
    },
    "T2_linear_dimensional_crossover": {
        "G1": "PASS CONDITIONALLY -- T0 local branch with imported G",
        "G2": "PARTIAL -- dimension crossover supplies shapes but not its scale",
        "G3": "FAIL -- linear 2D charge still gives V^4 proportional to M^2",
        "G4": "PASS STATIC ONLY -- no dynamic radiation closure",
        "G5": "FAIL -- transition and amplitude remain free",
        "G6": "FAIL -- dynamic/local constraints not closed",
    },
    "T3_saturated_patch_mincut": {
        "G1": "PASS CONDITIONALLY -- 3D Gauss branch, universal mass-energy charge, G input",
        "G2": "FAIL DERIVATION -- r_c proportional sqrt(M) follows, exact positive regulator does not",
        "G3": "PASS FORMALLY -- saturated 2D min-cut gives V^4 = G M a_* after closure",
        "G4": "FAIL DYNAMIC -- static field is conservative, radiation/orbital transfer unspecified",
        "G5": "FAIL -- a_* and regulator lack independent pre-galaxy determination",
        "G6": "FAIL -- external-field, binary radiation and c_g equality are not derived",
    },
}


def run() -> dict[str, Any]:
    checks = {
        "dimensions": dimensional_audit(),
        "local_3d_flux": local_flux_control(),
        "mass_scaling": mass_scaling_audit(),
        "regulator_nonuniqueness": regulator_nonuniqueness_audit(),
        "exact_availability": exact_availability_audit(),
        "conditional_solar": conditional_solar_audit(),
        "dynamic_constraints": dynamic_constraint_audit(),
    }
    survivors = [
        candidate
        for candidate, gates in GATES.items()
        if all(status.startswith("PASS") for status in gates.values())
    ]
    return _native({
        "issue": 227,
        "status": "closure-grade",
        "decision": "PROCEED" if survivors else "PHENOMENOLOGY ONLY",
        "survivors": survivors,
        "gates": GATES,
        "checks": checks,
        "input_vs_derived": {
            "inputs": [
                "measured G",
                "C4 local causal gates and positive capacities",
                "two-dimensional spatial antichain connectivity",
            ],
            "T3_added_global_constants": ["ell_*", "m_*", "nu_*", "tau_R"],
            "derived_if_T3_closure_is_imposed": [
                "r_c = sqrt(G M/a_*)",
                "V_inf^4 = G M a_*",
                "positive sqrt(M) cut throughput",
            ],
            "not_derived": [
                "a_s = a_c closure",
                "cored-log rather than Gaussian positive regulator",
                "numerical a_* independent of galaxies",
                "dynamic radiation and orbital-loss law",
                "external-field mapping",
                "c_screen = c to GW170817 precision",
            ],
        },
    })


def _native(value: Any) -> Any:
    """Convert NumPy scalars/containers into JSON-native receipt values."""
    if isinstance(value, dict):
        return {key: _native(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_native(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))

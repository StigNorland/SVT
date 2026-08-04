"""Issue #228 invariant screen-redshift and identifiability audit.

The instrument is intentionally structural.  It loads no cosmological outcome
data because the preregistered candidate ladder fails before likelihood
activation: energy-only redshift lacks time stretching, while the completed
optical response is rank-deficient between geometry and wake.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isclose, sqrt
from typing import Any

import numpy as np


@dataclass(frozen=True)
class Dim:
    mass: int = 0
    length: int = 0
    time: int = 0

    def __mul__(self, other: "Dim") -> "Dim":
        return Dim(self.mass + other.mass, self.length + other.length, self.time + other.time)

    def __truediv__(self, other: "Dim") -> "Dim":
        return Dim(self.mass - other.mass, self.length - other.length, self.time - other.time)

    def __pow__(self, exponent: int) -> "Dim":
        return Dim(self.mass * exponent, self.length * exponent, self.time * exponent)


ONE = Dim()
MASS = Dim(mass=1)
LENGTH = Dim(length=1)
TIME = Dim(time=1)
VELOCITY = LENGTH / TIME
ENERGY = MASS * LENGTH**2 / TIME**2
ENERGY_DENSITY = ENERGY / LENGTH**3
G_DIM = LENGTH**3 / MASS / TIME**2


def dimensional_audit() -> dict[str, Any]:
    kappa = ONE / LENGTH
    gamma = ONE / TIME
    flux = ENERGY_DENSITY * VELOCITY
    rate_from_density = (G_DIM * ENERGY_DENSITY / VELOCITY**2)
    return {
        "path_coefficient": [kappa.mass, kappa.length, kappa.time],
        "wake_rate": [gamma.mass, gamma.length, gamma.time],
        "energy_flux": [flux.mass, flux.length, flux.time],
        "G_u_over_c2": [rate_from_density.mass, rate_from_density.length, rate_from_density.time],
        "sqrt_G_u_over_c2_is_rate": rate_from_density == ONE / TIME**2,
        "energy_flux_is_not_write_rate": flux != ONE / TIME,
        "write_conversion_requires_energy_per_write_and_cell_area": True,
    }


def lapse_only_audit(a_emission: float = 0.7, a_observation: float = 1.3) -> dict[str, Any]:
    if a_emission <= 0 or a_observation <= 0:
        raise ValueError("lapse values must be positive")
    return {
        "a_emission": a_emission,
        "a_observation": a_observation,
        "proper_time_redefinition": "d_tau = A(t) d_t",
        "endpoint_redshift": 0.0,
        "one_plus_z": 1.0,
        "coordinate_removable": True,
        "C1_pass": False,
    }


def energy_only_path_loss(distance: float, kappa: float) -> dict[str, Any]:
    if distance < 0 or kappa < 0:
        raise ValueError("distance and kappa must be non-negative")
    y = exp(kappa * distance)
    d_angular = distance
    d_luminosity = distance * sqrt(y)
    eta = 1.0 if y == 1 else d_luminosity / (y**2 * d_angular)
    return {
        "one_plus_z": y,
        "frequency_ratio_observed_over_emitted": 1.0 / y,
        "duration_ratio_observed_over_emitted": 1.0,
        "achromatic_fractional_shift": True,
        "ray_blur_in_ideal_limit": 0.0,
        "D_A": d_angular,
        "D_L": d_luminosity,
        "distance_duality_eta": eta,
        "surface_brightness_exponent": -1,
        "C3_pass": isclose(y, 1.0),
        "kappa_status": "phenomenological input",
    }


def coherent_wavepacket_dilation(y: float, distance: float = 1.0) -> dict[str, Any]:
    if y < 1 or distance <= 0:
        raise ValueError("y must be >= 1 and distance positive")
    d_angular = distance
    d_luminosity = distance * y
    return {
        "one_plus_z": y,
        "frequency_ratio_observed_over_emitted": 1.0 / y,
        "duration_ratio_observed_over_emitted": y,
        "wavepacket_norm_ratio": 1.0,
        "photon_number_conserved": True,
        "ray_blur_in_ideal_limit": 0.0,
        "D_A": d_angular,
        "D_L": d_luminosity,
        "distance_duality_eta": d_luminosity / (y**2 * d_angular),
        "surface_brightness_exponent": -2,
        "C3_pass": True,
        "spatial_completion_required": not isclose(y, 1.0),
    }


def photon_screen_energy_ledger(photon_energy: float, y: float) -> dict[str, Any]:
    if photon_energy <= 0 or y < 1:
        raise ValueError("photon_energy must be positive and y >= 1")
    final = photon_energy / y
    screen_gain = photon_energy - final
    return {
        "photon_energy_initial": photon_energy,
        "photon_energy_final": final,
        "screen_energy_gain": screen_gain,
        "total_energy_initial": photon_energy,
        "total_energy_final": final + screen_gain,
        "scalar_energy_closes": isclose(final + screen_gain, photon_energy, rel_tol=0, abs_tol=1e-14),
        "screen_hamiltonian_derived": False,
        "frequency_record_decoherence_control_derived": False,
        "C2_pass": False,
    }


def spatial_metric_response(
    b_emission: float,
    b_observation: float,
    a_emission: float = 1.0,
    a_observation: float = 1.0,
) -> dict[str, Any]:
    if min(b_emission, b_observation, a_emission, a_observation) <= 0:
        raise ValueError("metric factors must be positive")
    y = b_observation / b_emission
    return {
        "one_plus_z": y,
        "duration_ratio": y,
        "lapse_endpoint_ratio": a_observation / a_emission,
        "redshift_independent_of_lapse": True,
        "distance_duality_eta": 1.0,
        "surface_brightness_exponent": -4,
        "C1_pass": True,
        "C3_pass": True,
        "status": "ordinary optical/FLRW form unless B dynamics are independently screen-derived",
    }


def blackbody_mapping(temperature_emitted: float, y: float) -> dict[str, Any]:
    if temperature_emitted <= 0 or y < 1:
        raise ValueError("temperature must be positive and y >= 1")
    temperature_observed = temperature_emitted / y
    # h*nu/(k*T) is invariant when both nu and T scale by 1/y.
    return {
        "temperature_emitted": temperature_emitted,
        "temperature_observed": temperature_observed,
        "frequency_ratio": 1.0 / y,
        "planck_dimensionless_frequency_invariant": True,
        "blackbody_shape_preserved_conditionally": True,
        "condition": "coherent universal frequency dilation with phase-space occupation preserved",
    }


def information_area_redshift(records_emitted: float, records_observed: float) -> dict[str, Any]:
    if records_emitted <= 0 or records_observed <= 0:
        raise ValueError("record occupancies must be positive")
    y = sqrt(records_observed / records_emitted)
    return {
        "records_emitted": records_emitted,
        "records_observed": records_observed,
        "one_plus_z": y,
        "duration_ratio": y,
        "B_ratio": y,
        "area_per_record_status": "new constitutive input",
        "record_growth_law_derived": False,
        "global_entropy_interpretation_allowed": False,
        "record_interpretation": "reduced-state persistent occupancy or latent-site activation",
    }


def information_area_kinematics(records: float, record_rate: float, record_acceleration: float) -> dict[str, Any]:
    if records <= 0 or record_rate <= 0:
        raise ValueError("records and positive record_rate are required")
    h_screen = 0.5 * record_rate / records
    acceleration_ratio = 0.5 * record_acceleration / records - 0.25 * (record_rate / records) ** 2
    q_screen = -acceleration_ratio / h_screen**2
    return {
        "H_screen": h_screen,
        "B_ddot_over_B": acceleration_ratio,
        "q_screen": q_screen,
        "decelerating": acceleration_ratio < 0,
        "deceleration_condition": "2 N N_ddot < N_dot^2",
        "constant_record_rate": isclose(record_acceleration, 0.0, rel_tol=0, abs_tol=1e-15),
    }


def power_law_record_kinematics(exponent_p: float) -> dict[str, Any]:
    if exponent_p <= 0:
        raise ValueError("record-growth exponent must be positive")
    q_screen = 2.0 / exponent_p - 1.0
    return {
        "record_exponent_p": exponent_p,
        "screen_scale_exponent": exponent_p / 2.0,
        "q_screen": q_screen,
        "decelerating": q_screen > 0,
        "coasting": isclose(q_screen, 0.0, rel_tol=0, abs_tol=1e-15),
        "accelerating": q_screen < 0,
    }


def identifiability_audit() -> dict[str, Any]:
    # Redshift, durations, distances and drift all depend on H_geom + Gamma_wake
    # in the completed product-only optical model.  Their normalized derivative
    # columns are therefore identical.
    weights = np.array([1.0, 0.7, 1.4, 0.3, 2.0])
    jacobian = np.column_stack((weights, weights))
    singular = np.linalg.svd(jacobian, compute_uv=False)
    rank = int(np.linalg.matrix_rank(jacobian, tol=1e-12))

    b = np.array([0.8, 0.9, 1.0, 1.2])
    w = np.array([1.0, 1.05, 1.1, 1.25])
    f = np.array([0.1, -0.2, 0.3, -0.1])
    product = b * w
    transformed = (b * np.exp(f)) * (w * np.exp(-f))
    return {
        "jacobian": jacobian.tolist(),
        "singular_values": singular.tolist(),
        "rank": rank,
        "parameters": 2,
        "full_rank": rank == 2,
        "null_direction": [1.0, -1.0],
        "BW_gauge_invariance": bool(np.allclose(product, transformed, atol=1e-14, rtol=0)),
        "redshift_drift_breaks_degeneracy_without_new_coupling": False,
        "C6_pass": False,
    }


def redshift_drift(y: float, h_effective_observer: float, h_effective_emitter: float) -> float:
    if y <= 0:
        raise ValueError("y must be positive")
    return y * h_effective_observer - h_effective_emitter


GATES: dict[str, dict[str, str]] = {
    "R0_lapse_only": {
        "C1": "FAIL -- homogeneous lapse is removable and gives z=0",
        "C2": "PASS VACUOUSLY -- no interaction",
        "C3": "FAIL -- no redshift or stretching",
        "C4": "FAIL -- no distance law",
        "C5": "FAIL -- no cosmological observables",
        "C6": "FAIL -- no nonzero component",
        "C7": "BLOCKED",
    },
    "R1_energy_only_path_loss": {
        "C1": "PASS CONDITIONALLY -- physical path/congruence must be added",
        "C2": "FAIL -- scalar energy ledger is not a photon-screen Hamiltonian",
        "C3": "FAIL -- duration factor is 1 rather than 1+z",
        "C4": "FAIL -- reciprocity eta=(1+z)^(-3/2)",
        "C5": "FAIL -- surface-brightness exponent is -1",
        "C6": "FAIL -- kappa is phenomenological and not C4-derived",
        "C7": "BLOCKED",
    },
    "R2_coherent_temporal_dilation": {
        "C1": "PASS CONDITIONALLY -- ideal dilation channel is physical input",
        "C2": "FAIL DERIVATION -- reservoir Hamiltonian/coherence control absent",
        "C3": "PASS FORMALLY -- duration and frequency share 1+z",
        "C4": "FAIL -- reciprocity eta=(1+z)^(-1) without spatial response",
        "C5": "FAIL -- surface-brightness exponent is -2",
        "C6": "FAIL -- dilation magnitude and dynamics are not C4-derived",
        "C7": "BLOCKED",
    },
    "R3_optical_spatial_completion": {
        "C1": "PASS FORMALLY -- invariant optical scale S=BW",
        "C2": "FAIL DERIVATION -- no C4 metric/interaction Hamiltonian",
        "C3": "PASS FORMALLY -- duration factor equals 1+z",
        "C4": "PASS FORMALLY -- metric reciprocity and independent likelihoods definable",
        "C5": "PARTIAL FORM -- standard propagation identities recovered; dynamics absent",
        "C6": "FAIL UNDERDETERMINED -- all ideal observables depend only on H_geom+Gamma_wake",
        "C7": "BLOCKED -- no age or size inference",
    },
    "R4_information_area_expansion": {
        "C1": "PASS FORMALLY -- B=sqrt(N/N0) gives invariant metric redshift",
        "C2": "FAIL DERIVATION -- record persistence, cell area and area-growth energy are absent",
        "C3": "PASS FORMALLY -- wavepacket duration scales with B_o/B_e",
        "C4": "PASS FORMALLY -- metric candle/ruler likelihoods are definable",
        "C5": "FAIL CURRENT PURE DECELERATION -- late-time SN acceleration sign conflicts under registered assumptions",
        "C6": "FAIL MECHANISM -- optical data measure B, not whether screen records caused it",
        "C7": "BLOCKED -- N(t) and a viable joint cosmology are not derived",
    },
}


def _native(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _native(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_native(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def run() -> dict[str, Any]:
    checks = {
        "dimensions": dimensional_audit(),
        "lapse_only": lapse_only_audit(),
        "energy_only_at_y2": energy_only_path_loss(1.0, np.log(2.0)),
        "coherent_dilation_at_y2": coherent_wavepacket_dilation(2.0),
        "energy_ledger_at_y2": photon_screen_energy_ledger(1.0, 2.0),
        "spatial_metric_at_y2": spatial_metric_response(1.0, 2.0, 0.7, 1.3),
        "blackbody_at_y2": blackbody_mapping(5.45, 2.0),
        "information_area_at_y2": information_area_redshift(1.0, 4.0),
        "constant_record_rate_kinematics": information_area_kinematics(10.0, 2.0, 0.0),
        "power_law_record_kinematics": {
            "p1": power_law_record_kinematics(1.0),
            "p2": power_law_record_kinematics(2.0),
            "p3": power_law_record_kinematics(3.0),
        },
        "identifiability": identifiability_audit(),
        "redshift_drift_sum_control": {
            "first_decomposition": redshift_drift(2.0, 0.7 + 0.3, 1.1 + 0.4),
            "second_decomposition": redshift_drift(2.0, 0.2 + 0.8, 0.6 + 0.9),
        },
    }
    survivors = [
        candidate
        for candidate, gates in GATES.items()
        if all(status.startswith("PASS") for status in gates.values())
    ]
    return _native({
        "issue": 228,
        "status": "closure-grade",
        "decision": "UNDERDETERMINED",
        "strongest_candidate": "R3_optical_spatial_completion",
        "survivors": survivors,
        "gates": GATES,
        "checks": checks,
        "likelihood_activated": False,
        "likelihood_stop_reason": (
            "No candidate passes C1-C3 and C6: R1 lacks stretching, R2 lacks "
            "spatial reciprocity, and R3 is rank-deficient between geometry and wake."
        ),
        "age_size_calculation_activated": False,
        "input_vs_derived": {
            "inherited": ["C4 global state", "local causal gates", "closed global ledger"],
            "candidate_inputs_not_derived": ["kappa", "wavepacket dilation channel", "B(t)", "W(t)", "screen reservoir Hamiltonian", "record-area law", "N(t)"],
            "derived_controls": ["lapse-only z=0", "R1 duration factor 1", "R2 reciprocity eta=1/(1+z)", "R3 BW gauge degeneracy", "R4 constant-write q=1"],
            "prohibited_outputs": ["cosmic age", "lookback time", "horizon", "universe size", "wake redshift fraction"],
        },
    })


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))

"""Executable analytic controls for H-SSV-I / GitHub issue #226.

The instrument does not fit data.  It checks the frozen candidate ladder in
``papers/H-SSV/results/issue-226/00-preregistration.md`` and records the one
gate that the strongest candidate cannot satisfy.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isclose, sqrt
from typing import Any


@dataclass(frozen=True)
class Dim:
    """SI base-dimension exponents (mass, length, time)."""

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

    def __pow__(self, power: int) -> "Dim":
        return Dim(self.mass * power, self.length * power, self.time * power)


ONE = Dim()
MASS = Dim(mass=1)
LENGTH = Dim(length=1)
TIME = Dim(time=1)
ENERGY = MASS * LENGTH**2 / TIME**2
SURFACE_ENERGY = ENERGY / LENGTH**2


def dimensional_audit() -> dict[str, Any]:
    """Check the q equation and the four distinct information quantities."""

    q = ONE
    inertia = MASS
    damping = MASS / TIME
    tension = ENERGY
    stiffness = SURFACE_ENERGY
    source = SURFACE_ENERGY
    q_tt = q / TIME**2
    q_t = q / TIME
    lap_q = q / LENGTH**2

    equation_terms = {
        "inertia": inertia * q_tt,
        "damping": damping * q_t,
        "tension": tension * lap_q,
        "potential": stiffness * q,
        "source": source,
    }
    target = SURFACE_ENERGY
    equation_consistent = all(dim == target for dim in equation_terms.values())

    capacity_density = ONE / LENGTH**2
    content_density = ONE / LENGTH**2
    write_rate_density = ONE / LENGTH**2 / TIME
    memory_density = ONE / LENGTH**2
    distinct = {
        "capacity_density": capacity_density,
        "content_density": content_density,
        "write_rate_density": write_rate_density,
        "memory_density": memory_density,
    }
    memory_law_consistent = (
        memory_density / TIME == write_rate_density
        and memory_density / TIME == memory_density / TIME
    )
    return {
        "equation_consistent": equation_consistent,
        "equation_terms": {
            key: [value.mass, value.length, value.time]
            for key, value in equation_terms.items()
        },
        "information_dimensions": {
            key: [value.mass, value.length, value.time]
            for key, value in distinct.items()
        },
        "memory_law_consistent": memory_law_consistent,
        "capacity_is_not_rate": capacity_density != write_rate_density,
    }


def characteristic_audit(
    inertia: float = 4.0, tension: float = 1.0, light_speed: float = 1.0
) -> dict[str, Any]:
    """Return the principal screen cone for positive coefficients."""

    if inertia <= 0 or tension <= 0 or light_speed <= 0:
        raise ValueError("inertia, tension and light_speed must be positive")
    screen_speed = sqrt(tension / inertia)
    return {
        "screen_speed": screen_speed,
        "light_speed": light_speed,
        "hyperbolic": True,
        "subluminal": screen_speed <= light_speed,
    }


def resonant_control(
    inertia: float = 2.0, stiffness: float = 8.0, forcing: float = 3.0
) -> dict[str, Any]:
    """Undamped C1 response at resonance; its envelope grows linearly."""

    omega_0 = sqrt(stiffness / inertia)
    slope = abs(forcing) / (2.0 * inertia * omega_0)
    return {
        "omega_0": omega_0,
        "envelope_slope": slope,
        "amplitude_at_t10": 10.0 * slope,
        "amplitude_at_t20": 20.0 * slope,
        "secular": slope > 0.0,
    }


def damped_response_audit(
    inertia: float = 2.0,
    damping: float = 0.7,
    stiffness: float = 8.0,
    forcing: float = 3.0,
    omega: float = 2.0,
) -> dict[str, Any]:
    """Static and periodic transfer amplitudes for C2/C3."""

    if min(inertia, damping, stiffness) <= 0:
        raise ValueError("inertia, damping and stiffness must be positive")
    denominator_sq = (stiffness - inertia * omega**2) ** 2 + (
        damping * omega
    ) ** 2
    periodic_amplitude = abs(forcing) / sqrt(denominator_sq)
    static_amplitude = forcing / stiffness
    return {
        "denominator_sq": denominator_sq,
        "periodic_amplitude": periodic_amplitude,
        "static_amplitude": static_amplitude,
        "bounded_periodic": denominator_sq > 0.0,
        "bounded_static": stiffness > 0.0,
    }


def conservation_ledger_audit() -> dict[str, Any]:
    """Check the local q + reservoir + matter energy identity.

    For
        I q_tt + Gamma q_t - T lap(q) + V'(q) = s,
    the screen balance is
        d_t e_q + div(S_q) = s q_t - Gamma q_t^2.
    The reservoir receives ``Gamma q_t^2`` and matter loses ``s q_t``.
    """

    inertia = 1.7
    damping = 0.4
    tension = 2.3
    stiffness = 0.9
    quartic = 0.2
    q = 0.6
    q_t = -0.35
    grad_q = 0.7
    grad_q_t = -0.11
    lap_q = 0.23
    source = 0.8
    potential_prime = stiffness * q + quartic * q**3
    q_tt = (
        source - damping * q_t + tension * lap_q - potential_prime
    ) / inertia

    energy_rate = (
        inertia * q_t * q_tt
        + tension * grad_q * grad_q_t
        + potential_prime * q_t
    )
    flux_divergence = -tension * (
        grad_q_t * grad_q + q_t * lap_q
    )
    reservoir_rate = damping * q_t**2
    matter_rate = -source * q_t
    total_rate = energy_rate + flux_divergence + reservoir_rate + matter_rate
    return {
        "screen_energy_rate": energy_rate,
        "screen_flux_divergence": flux_divergence,
        "reservoir_rate": reservoir_rate,
        "matter_rate": matter_rate,
        "total_rate": total_rate,
        "closes": abs(total_rate) <= 1.0e-12,
        "damping_without_reservoir_closes": abs(
            energy_rate + flux_divergence + matter_rate
        )
        <= 1.0e-12,
    }


def memory_audit(
    capacity: float = 5.0,
    write_rate: float = 1.25,
    relaxation_time: float = 3.0,
    initial: float = 0.4,
) -> dict[str, Any]:
    """Exact constant-source solution of the saturating memory law."""

    if capacity <= 0 or write_rate < 0 or relaxation_time <= 0:
        raise ValueError("invalid memory parameters")
    if not 0 <= initial <= capacity:
        raise ValueError("initial memory must lie inside capacity")
    decay_rate = write_rate / capacity + 1.0 / relaxation_time
    equilibrium = write_rate / decay_rate

    def value(time: float) -> float:
        return equilibrium + (initial - equilibrium) * exp(-decay_rate * time)

    samples = [value(float(time)) for time in range(101)]
    return {
        "equilibrium": equilibrium,
        "analytic_equilibrium": (
            capacity * write_rate * relaxation_time
            / (capacity + write_rate * relaxation_time)
        ),
        "minimum_sample": min(samples),
        "maximum_sample": max(samples),
        "bounded": all(0.0 <= sample <= capacity for sample in samples),
        "converged": abs(samples[-1] - equilibrium) <= 1.0e-12,
    }


def _boost_velocity(velocity: float, boost: float) -> float:
    if abs(velocity) >= 1.0 or abs(boost) >= 1.0:
        raise ValueError("velocities use c=1 and must be subluminal")
    return (velocity - boost) / (1.0 - velocity * boost)


def _relative_gamma(first: float, second: float) -> float:
    gamma_first = 1.0 / sqrt(1.0 - first**2)
    gamma_second = 1.0 / sqrt(1.0 - second**2)
    return gamma_first * gamma_second * (1.0 - first * second)


def observer_audit() -> dict[str, Any]:
    """Contrast coordinate speed with the physical screen-relative scalar."""

    matter_velocity = 0.35
    screen_velocity = -0.2
    passive_boost = 0.4
    boosted_matter = _boost_velocity(matter_velocity, passive_boost)
    boosted_screen = _boost_velocity(screen_velocity, passive_boost)

    coordinate_source = abs(matter_velocity)
    boosted_coordinate_source = abs(boosted_matter)
    relative_gamma = _relative_gamma(matter_velocity, screen_velocity)
    boosted_relative_gamma = _relative_gamma(boosted_matter, boosted_screen)
    return {
        "coordinate_source": coordinate_source,
        "boosted_coordinate_source": boosted_coordinate_source,
        "coordinate_source_invariant": isclose(
            coordinate_source, boosted_coordinate_source, abs_tol=1.0e-12
        ),
        "relative_gamma": relative_gamma,
        "boosted_relative_gamma": boosted_relative_gamma,
        "relative_gamma_invariant": isclose(
            relative_gamma, boosted_relative_gamma, rel_tol=0.0, abs_tol=1.0e-12
        ),
        "preferred_structure_remains": True,
        "preferred_structure_reason": (
            "gamma_US is coordinate invariant only after a physical screen "
            "four-velocity u_S is supplied; H-SSV does not define or bound it"
        ),
    }


def sign_and_prediction_audit() -> dict[str, Any]:
    """Positive sources add, and relocation predicts a preferred-frame signal."""

    rest_energies = [2.0, 3.5, 1.25]
    relative_speeds = [0.0, 0.2, -0.35]
    relocation_coupling = 0.8
    contributions = [
        energy
        * (
            1.0
            + relocation_coupling
            * (1.0 / sqrt(1.0 - velocity**2) - 1.0)
        )
        for energy, velocity in zip(rest_energies, relative_speeds, strict=True)
    ]
    return {
        "contributions": contributions,
        "sum": sum(contributions),
        "all_positive": all(value > 0.0 for value in contributions),
        "phase_cancellation_possible": False,
        "universal_clock_map": "A(q) = exp(-alpha q), alpha > 0",
        "independent_prediction": (
            "at fixed rest content, relocation relative to u_S increases the "
            "load source by +(g_r/2) v_rel^2/c^2 at small speed"
        ),
        "relocation_coupling_g_r": relocation_coupling,
        "leading_quadratic_coefficient_per_g_r": 0.5,
        "null_result_falsifies_relocation_loading_if_g_r_positive": True,
    }


GATES: dict[str, dict[str, str]] = {
    "C0_coordinate_speed": {
        "F1": "PASS -- dimensioned hyperbolic response can be supplied",
        "F2": "PASS -- conservative coupling can be supplied",
        "F3": "FAIL -- |coordinate velocity| changes under a passive boost",
        "F4": "FAIL -- the undamped control has resonant secular growth",
        "F5": "PASS -- absolute-speed contributions are sign definite",
        "F6": "PASS -- it predicts a coordinate-dependent effect, which is a falsifier",
    },
    "C1_conservative_undamped": {
        "F1": "PASS -- positive inertia/tension give a causal hyperbolic cone",
        "F2": "PASS -- the local action has a conserved stress-energy ledger",
        "F3": "FAIL -- u_S and K remain undefined preferred structure",
        "F4": "FAIL -- periodic forcing at an eigenfrequency grows secularly",
        "F5": "PASS -- positive scalar sources add and one clock map is fixed",
        "F6": "PASS -- positive quadratic screen-relative boost response",
    },
    "C2_damped_no_reservoir": {
        "F1": "PASS -- damping does not change the principal cone",
        "F2": "FAIL -- Gamma q_t removes energy with no receiving sector",
        "F3": "FAIL -- u_S and K remain undefined preferred structure",
        "F4": "PASS -- positive damping/stiffness bound stationary and periodic response",
        "F5": "PASS -- positive scalar sources add and one clock map is fixed",
        "F6": "PASS -- positive quadratic screen-relative boost response",
    },
    "C3_carrier_screen_reservoir": {
        "F1": "PASS -- local carrier and screen characteristics are <= c",
        "F2": "PASS -- matter, carrier, screen and reservoir ledger closes",
        "F3": (
            "FAIL -- covariance conditional on postulated u_S and K is not an "
            "operational definition or preferred-frame bound"
        ),
        "F4": "PASS -- relaxation and saturation bound q and m",
        "F5": "PASS -- source is positive and A=exp(-alpha q) is universal",
        "F6": "PASS -- fixed-sign O(v_rel^2/c^2) preferred-frame prediction",
    },
}


def _passes(status: str) -> bool:
    return status.startswith("PASS")


def run() -> dict[str, Any]:
    checks = {
        "dimensions": dimensional_audit(),
        "characteristics": characteristic_audit(),
        "undamped_resonance": resonant_control(),
        "damped_response": damped_response_audit(),
        "conservation": conservation_ledger_audit(),
        "memory": memory_audit(),
        "observer": observer_audit(),
        "sign_and_prediction": sign_and_prediction_audit(),
    }
    survivors = [
        candidate
        for candidate, gates in GATES.items()
        if all(_passes(gates[f"F{index}"]) for index in range(1, 7))
    ]
    return {
        "issue": 226,
        "status": "closure-grade",
        "decision": "PROCEED" if survivors else "REVISE",
        "survivors": survivors,
        "checks": checks,
        "gates": GATES,
        "blocking_result": (
            None
            if survivors
            else {
                "gate": "F3",
                "candidate": "C3_carrier_screen_reservoir",
                "reason": (
                    "the physical screen flow u_S and the normalized retarded "
                    "bulk-to-screen map K are postulates with no operational "
                    "definition or bounded preferred-frame phenomenology"
                ),
            }
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))

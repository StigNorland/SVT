from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Nondimensionalisation:
    """Default static-branch nondimensionalisation.

    Current shared convention:
    - length unit: healing length xi
    - density unit: background density rho0
    - velocity unit: longitudinal mode speed c
    """

    xi: float = 1.0
    rho0: float = 1.0
    c: float = 1.0


@dataclass(frozen=True)
class GridSpec:
    """Basic Cartesian grid specification for static-branch prototypes."""

    n: int
    half_width: float

    @property
    def spacing(self) -> float:
        return 2.0 * self.half_width / self.n


@dataclass(frozen=True)
class RelaxationControls:
    """Common static relaxation controls."""

    step_size: float
    max_steps: int
    tolerance: float


@dataclass(frozen=True)
class StaticDiagnostics:
    """Minimum diagnostics expected from a static-branch run."""

    energy_monotonicity: bool
    residual_norm: float
    grid_sensitivity_checked: bool = False
    box_sensitivity_checked: bool = False
    topology_tracking_checked: bool = False

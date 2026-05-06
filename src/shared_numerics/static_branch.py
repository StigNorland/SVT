from __future__ import annotations

from dataclasses import dataclass
import math


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


def grid_step_scale(spacing: float, reference_spacing: float) -> float:
    """Scale explicit relaxation steps with the square of grid spacing.

    For the present prototype gradient flow, the Laplacian term is the stiff part
    of the update, so a simple `dx^2` scaling is a reasonable first stabilisation
    rule when moving between coarse and fine Cartesian grids.
    """

    if reference_spacing <= 0.0:
        return 1.0
    ratio = max(spacing / reference_spacing, 1.0e-12)
    return ratio * ratio


@dataclass(frozen=True)
class RelaxationControls:
    """Common static relaxation controls."""

    step_size: float
    max_steps: int
    tolerance: float
    min_step_size: float = 1.0e-5
    max_step_size: float = 5.0e-2
    check_interval: int = 10
    patience_intervals: int = 3
    energy_tol: float = 1.0e-9
    reference_spacing: float | None = None


@dataclass(frozen=True)
class StaticDiagnostics:
    """Minimum diagnostics expected from a static-branch run."""

    energy_monotonicity: bool
    residual_norm: float
    grid_sensitivity_checked: bool = False
    box_sensitivity_checked: bool = False
    topology_tracking_checked: bool = False

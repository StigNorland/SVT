"""Shared dataclasses for dynamic-branch (time-dependent) numerical runs.

Mirrors :mod:`shared_numerics.static_branch` for the dynamic side of the
``L + L_perp`` closure programme.  The minimum-diagnostic list crystallised
here matches ``docs/numerical-conventions.md`` -- the "Dynamic-Branch
Minimum Diagnostics" subsection.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeStepControls:
    """Common dynamic-branch time-integration controls.

    Conventions:
    - ``dt`` is a dimensionless step (in units of ``xi/c``).
    - ``steps`` is the total integrator step count.
    - ``snapshots`` is how many state slices to save along the path.
    - Split-step methods (Strang) use ``order = 2`` by default; higher
      orders are reserved for production runs that justify the cost.
    """

    dt: float
    steps: int
    snapshots: int = 17
    order: int = 2


@dataclass(frozen=True)
class DynamicDiagnostics:
    """Minimum diagnostics expected from a dynamic-branch run.

    Crystallises the "Dynamic-Branch Minimum Diagnostics" list from
    ``docs/numerical-conventions.md`` so dynamic scripts can advertise
    machine-readably which checks they actually performed.
    """

    total_energy_drift_checked: bool
    norm_drift_checked: bool
    reconnection_markers_recorded: bool
    cap_extraction_method: str
    timestep_sensitivity_checked: bool = False
    resolution_sensitivity_checked: bool = False
    initial_condition_sensitivity_checked: bool = False


@dataclass(frozen=True)
class DynamicObservables:
    """Standard dynamic-branch observables, as scalars from a single run.

    These names align with ``papers/SSV-II/data/runA_*`` and the existing
    ``reconnection_supplement.py`` CSV columns.  Production runs may add
    fields, but should not rename these.
    """

    saddle_index: int
    saddle_excess: float
    cap_radius: float
    cos_phi: float

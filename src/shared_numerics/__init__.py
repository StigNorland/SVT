"""Shared numerical helpers for the SSV closure programme.

This package is the initial repo artifact for issue #12:
build the shared numerical core for the `L + L_perp` computations.

The current scope is intentionally small:

- shared status labels for numerical outputs
- shared static-branch configuration dataclasses

It is not yet a production solver layer.
"""

from .static_branch import GridSpec, Nondimensionalisation, RelaxationControls, StaticDiagnostics, grid_step_scale
from .status import OutputStatus, ScriptMetadata

__all__ = [
    "GridSpec",
    "Nondimensionalisation",
    "RelaxationControls",
    "StaticDiagnostics",
    "grid_step_scale",
    "OutputStatus",
    "ScriptMetadata",
]

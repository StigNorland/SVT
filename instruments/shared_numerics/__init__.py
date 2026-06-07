"""Shared numerical helpers for the SSV closure programme.

This package is the repo artifact for issue #12: build the shared numerical
core for the ``L + L_perp`` computations.  It is intentionally small.  It
codifies the canonical conventions of ``docs/numerical-conventions.md`` as
dataclasses, so that scripts on both the static and dynamic branches share
the same vocabulary for nondimensionalisation, controls, diagnostics, and
status labels.

What this layer is
------------------

- Canonical conventions in code form (one place to read and import).
- Machine-readable status / metadata for individual scripts
  (``ScriptMetadata`` + ``OutputStatus``), so a script's prototype /
  validation / candidate / closure-grade status is queryable, not just
  documented in a header comment.
- A short list of minimum-diagnostic dataclasses (``StaticDiagnostics``,
  ``DynamicDiagnostics``) that scripts can use to advertise which of the
  conventions-doc minimum checks they actually performed.

What this layer is **not** (yet)
--------------------------------

- A production solver layer.  No solver state, no integrator, no grid
  primitives.  The existing per-script solvers stay where they are.
- A drop-in replacement for the per-script ``Config`` dataclasses in
  ``trefoil_breather_*.py`` or ``reconnection_supplement.py``.  Those keep
  their own input dataclasses; this module just lets them tag their
  outputs and diagnostics with a shared vocabulary.

What later computations are expected to import
----------------------------------------------

The roadmap (``docs/numerical-minimisation-roadmap.md``) puts the
closure-grade work under Workstreams 2 (static 3D breather minimisation,
issue #13) and 4 (dynamic 3D reconnection minimisation, issue #15).  When
those workstreams move to closure-grade runs, they should import:

- ``Nondimensionalisation`` -- to declare the run's unit system and so
  catch unit mismatches between collaborating scripts;
- ``GridSpec`` -- the basic Cartesian grid description used by every
  static-branch prototype script in ``instruments/paper_i/``;
- ``RelaxationControls`` -- the static gradient-flow controls including
  the topology-preservation knobs that were the key #13 development;
- ``StaticDiagnostics`` / ``DynamicDiagnostics`` -- to advertise which
  minimum-diagnostic checks the run performed (refinement, box size,
  timestep sensitivity, topology tracking, etc.);
- ``OutputStatus`` and ``ScriptMetadata`` -- to declare per-script status
  in a machine-readable way that the paper text and the closure-tracking
  GitHub issues can both query.

This is the contract the closure runs use; new scripts on either branch
should import the dataclasses above instead of re-defining equivalents.
"""

from .dynamic_branch import (
    DynamicDiagnostics,
    DynamicObservables,
    TimeStepControls,
)
from .static_branch import (
    GridSpec,
    Nondimensionalisation,
    RelaxationControls,
    StaticDiagnostics,
    grid_step_scale,
)
from .status import OutputStatus, ScriptMetadata

__all__ = [
    # static-branch
    "GridSpec",
    "Nondimensionalisation",
    "RelaxationControls",
    "StaticDiagnostics",
    "grid_step_scale",
    # dynamic-branch
    "DynamicDiagnostics",
    "DynamicObservables",
    "TimeStepControls",
    # status / metadata
    "OutputStatus",
    "ScriptMetadata",
]

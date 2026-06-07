from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class OutputStatus(str, Enum):
    """Shared status labels from docs/numerical-conventions.md."""

    PROTOTYPE = "prototype"
    VALIDATION = "validation"
    CANDIDATE = "candidate"
    CLOSURE_GRADE = "closure-grade"


@dataclass(frozen=True)
class ScriptMetadata:
    """Minimal machine-readable metadata for numerical scripts."""

    problem_type: str
    status: OutputStatus
    nondimensionalisation: str
    observables: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    issue_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    notes: tuple[str, ...] = field(default_factory=tuple)

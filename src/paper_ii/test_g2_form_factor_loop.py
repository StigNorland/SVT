"""Regression tests for the issue #33 g-2 form-factor calculation."""

from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path

from scipy.integrate import IntegrationWarning

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from paper_ii.g2_form_factor_loop import (
    ALPHA,
    F2_constant,
    SCHWINGER,
    evaluate_family,
    evaluate_modified,
    evaluate_schwinger_normalization,
)


def test_contact_vertex_recovers_schwinger_normalization():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", IntegrationWarning)
        integral, error = evaluate_schwinger_normalization()
    a_e = (3.0 * ALPHA / math.pi) * integral

    assert error < 1e-8
    assert math.isclose(integral, 1.0 / 6.0, rel_tol=0.0, abs_tol=5e-10)
    assert math.isclose(a_e, SCHWINGER, rel_tol=5e-10, abs_tol=0.0)


def test_classical_ring_form_factor_removes_schwinger_term():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", IntegrationWarning)
        integral, _error = evaluate_modified(1.0 / ALPHA)

    a_e = (3.0 * ALPHA / math.pi) * integral
    ratio = a_e / SCHWINGER

    assert math.isclose(ratio, 0.004646, rel_tol=5e-3, abs_tol=0.0)
    assert ratio < 0.005


def test_constant_topological_vertex_is_scale_independent():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", IntegrationWarning)
        results = tuple(
            evaluate_family(r_tilde, F2_constant)
            for r_tilde in (0.0, 1.0, 10.0, 1.0 / ALPHA)
        )

    for integral, _error in results:
        a_e = (3.0 * ALPHA / math.pi) * integral
        assert math.isclose(a_e, SCHWINGER, rel_tol=5e-10, abs_tol=0.0)

"""Focused analytic and numerical checks for issue #225."""

import numpy as np

import logsvt_piso_audit as audit


def test_model_lattice_is_complete_and_unique():
    assert len(audit.LOGSVT_MODELS) == 32
    assert len({model.name for model in audit.LOGSVT_MODELS}) == 32
    assert audit.MODEL_BY_NAME["baryons"].parameters == ()
    assert len(audit.MODEL_BY_NAME["C_k12_L_Q"].parameters) == 6


def test_genuine_piso_origin_series_and_asymptote():
    z = np.array([0.0, 1.0e-5, 1.0e-3, 1.0, 1.0e6])
    shape = audit.piso_shape(z)
    assert shape[0] == 0.0
    assert np.isclose(shape[1], z[1] ** 2 / 3.0, rtol=1.0e-9)
    assert np.isclose(shape[2], 1.0 - np.arctan(z[2]) / z[2], rtol=1.0e-8)
    assert np.isclose(shape[-1], 1.0, rtol=2.0e-6)


def test_piso_and_cored_log_are_analytically_distinct():
    z = np.array([0.2, 0.5, 1.0, 2.0, 5.0])
    p_iso = audit.piso_shape(z)
    cored = audit.cored_log_shape(z)
    assert not np.allclose(p_iso, cored)
    # With a common asymptotic amplitude, pISO has one third the central
    # quadratic coefficient of the cored-log law.
    ratio = audit.piso_shape(np.array([1.0e-5]))[0] / audit.cored_log_shape(np.array([1.0e-5]))[0]
    assert np.isclose(ratio, 1.0 / 3.0, rtol=1.0e-9)


def test_curvature_matched_piso_still_differs_at_finite_radius():
    z = np.linspace(0.05, 5.0, 100)
    curvature_matched_piso = 3.0 * audit.piso_shape(z)
    assert not np.allclose(curvature_matched_piso, audit.cored_log_shape(z), rtol=1.0e-3)


def test_logsvt_k2_is_exactly_cored_log_not_piso():
    x = np.linspace(0.001, 1.0, 100)
    B, u2 = 1.7, 3.4
    spec = audit.MODEL_BY_NAME["k2"]
    k2 = audit.logsvt_extra_dimensionless(x, np.log([B, u2]), spec)
    cored = 4.0 * B * audit.cored_log_shape(x * np.sqrt(u2))
    piso = 4.0 * B * audit.piso_shape(x * np.sqrt(u2))
    assert np.allclose(k2, cored, rtol=1.0e-12, atol=1.0e-12)
    assert not np.allclose(k2, piso)


def test_information_criteria_formula():
    score = audit.criteria(20.0, points=30, parameters=3)
    assert np.isclose(score["aicc"], 20.0 + 6.0 + 24.0 / 26.0)
    assert np.isclose(score["bic"], 20.0 + 3.0 * np.log(30.0))


def test_primary_sample_exists_in_vendored_sparc_data():
    curves = audit.parse_mass_models(audit.DATA)
    assert set(audit.GALAXIES) <= set(curves)


def test_expanded_bounds_contain_every_primary_bound():
    primary = audit.BOUND_SCHEMES["primary"]
    expanded = audit.BOUND_SCHEMES["expanded"]
    for model in audit.MODELS:
        primary_lower, primary_upper = audit.parameter_bounds(model, primary)
        expanded_lower, expanded_upper = audit.parameter_bounds(model, expanded)
        assert np.all(expanded_lower <= primary_lower)
        assert np.all(expanded_upper >= primary_upper)


def test_only_proved_exact_alias_is_shape_canonicalized():
    assert audit.winner_shape("k2") == audit.winner_shape("cored_log")
    assert audit.winner_shape("k2_L") != audit.winner_shape("cored_log")
    assert audit.winner_shape("pISO") != audit.winner_shape("cored_log")

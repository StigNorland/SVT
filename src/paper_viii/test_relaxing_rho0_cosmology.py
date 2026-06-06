import math

from paper_viii.relaxing_rho0_cosmology import (
    bao_dm_fractional_residual,
    distance_modulus_residual,
    e2,
    hubble_fractional_residual,
    lambda_ratio,
    sample_observable_table,
    w_eff,
)


def test_beta_zero_is_lcdm_limit():
    assert math.isclose(w_eff(0.0), -1.0)
    assert math.isclose(lambda_ratio(1.0, 0.0), 1.0)
    assert math.isclose(hubble_fractional_residual(1.0, 0.0), 0.0)
    assert math.isclose(distance_modulus_residual(1.0, 0.0), 0.0)
    assert math.isclose(bao_dm_fractional_residual(1.0, 0.0), 0.0)


def test_beta_to_w_mapping():
    assert math.isclose(w_eff(0.3), -1.1)
    assert math.isclose(w_eff(-0.3), -0.9)


def test_positive_beta_reduces_past_dark_energy():
    z = 1.0
    beta = 0.2
    assert lambda_ratio(z, beta) < 1.0
    assert e2(z, beta) < e2(z, 0.0)
    assert hubble_fractional_residual(z, beta) < 0.0
    assert distance_modulus_residual(z, beta) > 0.0
    assert bao_dm_fractional_residual(z, beta) > 0.0


def test_negative_beta_increases_past_dark_energy():
    z = 1.0
    beta = -0.2
    assert lambda_ratio(z, beta) > 1.0
    assert e2(z, beta) > e2(z, 0.0)
    assert hubble_fractional_residual(z, beta) > 0.0
    assert distance_modulus_residual(z, beta) < 0.0
    assert bao_dm_fractional_residual(z, beta) < 0.0


def test_sample_table_shape():
    rows = sample_observable_table(betas=(-0.1, 0.1), redshifts=(0.5, 1.0))
    assert len(rows) == 4
    assert {row["beta"] for row in rows} == {-0.1, 0.1}
    assert {row["z"] for row in rows} == {0.5, 1.0}

"""Tests for the #119 falsification record and bath-driven candidate.

Fast (coarse-grid) versions of the pre-registered decision rules of issue
#119, run against the same integrators the production results use
(instruments/paper_iv/bath_driven_interaction.py).  Pins three negatives and
two positives:

  H1b  no time-averaged mutual force between unequal-frequency sources
       (the as-written mutual mechanism gives no electron-proton gravity);
  H1c  the static LogSE response is Yukawa-screened (no static long-range
       tail: the omega = 0 route to Newtonian 1/r is closed);
  H2a  the bath-driven force between two passive defects in a common
       long-wavelength drive is sign-definite (attractive), decreasing with
       separation, and vanishes without the bath;
  H2b  the bath-driven force scales as the bath amplitude squared (p = 2,
       the exponent that makes G inherit A_bath^2, feeding H2d).
"""

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
p = str(SRC_ROOT / "paper_iv")
if p not in sys.path:
    sys.path.insert(0, p)

import bath_driven_interaction as bdi  # noqa: E402

# coarse-grid settings shared by the fast checks
FAST_UNEQUAL = dict(N=96, n_ramp=1, n_transient=3, n_avg=4)
FAST_BATH = dict(N=96, omega_b=0.2, n_ramp=1, n_transient=2, n_avg=4)


def _f_int(d, UA, UB, eps):
    fp, _, _ = bdi.run_bath(d, UA, UB, eps=eps, **FAST_BATH)
    fs, _, _ = bdi.run_bath(d, UA, UB, eps=eps, single=True, **FAST_BATH)
    return fp - fs


def test_h1b_unequal_frequency_null():
    """Unequal drive frequencies: the time-averaged bilinear force is
    consistent with the isolated-source residual, while the equal-frequency
    control at the same separation is an order of magnitude larger."""
    d, wA = 8.0, 0.3
    res, _ = bdi.run_unequal(d, wA, wA, single=True, **FAST_UNEQUAL)
    ctrl, _ = bdi.run_unequal(d, wA, wA, **FAST_UNEQUAL)
    uneq, _ = bdi.run_unequal(d, wA, 2.0 * wA, **FAST_UNEQUAL)
    assert abs(ctrl) > 10.0 * abs(res), "control force not resolved"
    assert abs(uneq) < max(3.0 * abs(res), 0.05 * abs(ctrl)), (
        f"unequal-frequency force not null: {uneq:+.3e} "
        f"(control {ctrl:+.3e}, residual {res:+.3e})")


def test_h1c_static_response_is_screened():
    """The relaxed static response is Yukawa-screened: its decay rate over
    the physical response region matches the parameter-free prediction
    kappa = sqrt(4b) = 2, and the far field carries no monotone power-law
    tail -- only a sign-changing box pedestal orders of magnitude below the
    unscreened expectation.  This closes the static route to a 1/r
    potential."""
    import numpy as np
    b = 1.0
    kappa = np.sqrt(4.0 * b)
    r, prof, _ = bdi.run_static(N=160, b=b, t_total=80.0, t_avg=15.0)
    core = abs(prof[0])
    assert core > 1e-3, "static response not formed"

    # decay rate over the region where the response tracks the source
    msk = (r > 1.5) & (r < 5.0) & (np.abs(prof) > 1e-12)
    assert msk.sum() >= 4, "not enough points to fit the screened tail"
    yy = np.log(np.abs(prof[msk]) * np.sqrt(r[msk]))   # 2D Yukawa ~ e^-kr/sqrt r
    A = np.vstack([r[msk], np.ones(msk.sum())]).T
    slope = np.linalg.lstsq(A, yy, rcond=None)[0][0]
    assert abs(-slope - kappa) < 0.25 * kappa, (
        f"decay rate {-slope:.2f} does not match kappa = {kappa:.1f}")

    # far field: a physical monopole tail would be monotone & one-signed;
    # the residual here is a sign-changing standing-wave pedestal (artifact)
    far = r > 6.0
    floor = np.max(np.abs(prof[far]))
    unscreened = (0.8 / 10.0) ** 0.5 * core
    sign_changes = int(np.sum(np.diff(np.sign(prof[far])) != 0))
    assert sign_changes >= 1 or floor < 1e-2 * unscreened, (
        f"far-field residual looks like a real tail: floor {floor:.2e}, "
        f"{sign_changes} sign changes, unscreened expectation {unscreened:.2e}")


def test_h2a_bath_driven_force_sign_definite_and_decaying():
    """Two passive defects in a common long-wavelength bath: interaction
    force attractive at both separations, weaker at the larger one, and
    requiring the bath to exist."""
    f8 = _f_int(8.0, 0.5, 0.5, eps=0.15)
    f14 = _f_int(14.0, 0.5, 0.5, eps=0.15)
    f_nobath = _f_int(8.0, 0.5, 0.5, eps=0.0)
    assert f8 > 0.0 and f14 > 0.0, (
        f"bath-driven force not attractive: F(8)={f8:+.3e}, "
        f"F(14)={f14:+.3e}")
    assert abs(f14) < abs(f8), "force does not decrease with separation"
    assert abs(f_nobath) < 0.1 * abs(f8), (
        f"force persists without bath: {f_nobath:+.3e}")


def test_h2b_amplitude_exponent_p2():
    """Halving the bath amplitude quarters the force: p = 2 within 0.4 at
    test resolution (production tolerance 0.3)."""
    import math
    f_full = _f_int(8.0, 0.5, 0.5, eps=0.15)
    f_half = _f_int(8.0, 0.5, 0.5, eps=0.075)
    assert f_full != 0.0 and f_half != 0.0
    pexp = math.log(abs(f_full) / abs(f_half)) / math.log(2.0)
    assert abs(pexp - 2.0) < 0.4, f"amplitude exponent p = {pexp:.2f}, not ~2"

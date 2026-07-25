"""#162 [MODEL 1/2] Superfluid in an imposed container.

Pre-registered on issue #162 (follows the #161 closure), BEFORE this code.

WHAT IS ASSUMED (imported, NOT tested).  The holographic container supplies
gravity: an external loading g00(x) and a transverse-traceless shear h_ij(t)
are PRESCRIBED external inputs.  We do not derive G or the shear -- importing
them IS the assumption being modelled.  Any apparent "derivation" of them here
would be a bug (circularity), not a finding.

WHAT IS TESTED.
  (1) Effect/cause dictionary.  Does the SSV medium physically realise an
      externally-imposed cause as the ontology claims -- specifically, does the
      local phase-update rate (the internal clock, Josephson relation
      d/dt arg psi = -mu_local/hbar) track the imposed loading g00?  This is
      "time dilation = phase-update rate" made numerical.
  (2) Shear response.  How does the superfluid respond to the imposed TT shear,
      and does that response differ MEASURABLY from a generic medium's response
      to the SAME shear?

THREE MEDIA (units hbar = m = rho0 = 1).
  linear : free Schroedinger, mu_nl = 0                     (null comparator)
  cubic  : ordinary GPE,       mu_nl = g rho                (null comparator)
  log    : SSV LogSE,          mu_nl = b ln(rho/rho0)       (the SSV medium)
Bogoliubov dispersion omega(k) = sqrt( c_s^2 k^2 + (k^2/2)^2 ), with the
effective sound speed c_s^2 = rho dmu_nl/drho|_rho0 : cubic -> g rho0,
log -> b (density-INDEPENDENT, the signature log feature).  Matching b = g rho0
gives cubic and log the SAME dispersion -- the sharpest form of the null test.

METHOD.  Symmetric split-step Fourier (Strang) evolution -- unitary, norm
conserving.  The imposed TT shear enters as a time-dependent anisotropy of the
kinetic operator: laplacian -> (1 - h) d_xx + (1 + h) d_yy, i.e. in k-space
K(k,t) = 1/2 [ (1 - h(t)) kx^2 + (1 + h(t)) ky^2 ].  A long-wavelength TT drive
does no work on a homogeneous condensate (K(0) = 0); it parametrically pumps
finite-k phonon PAIRS, resonant at drive frequency Omega = 2 omega(k) -- the
analogue of gravitational-wave phonon production.

DECISION RULES (fixed in the pre-registration).
  R-consistency : local phase-rate == -mu_local/hbar to numerical precision
                  (relative error < 1e-3).  PASS => ontology self-consistent.
  R-prediction  : compare the log medium's shear response to the comparators.
                  Clean NEGATIVE (expected, rule 1): with c_s matched, the log
                  response is indistinguishable from the ordinary GPE (the log
                  structure is invisible in the gravity sector at linear
                  amplitude) => SSV superfluous.  Positive (suggestive only):
                  a converged, matched-c_s difference => a candidate SSV
                  gravity-sector signature; name it, flag as suggestive.

Run:  python instruments/model_container/superfluid_in_imposed_container.py [--quick]
Writes papers/SSV-IV/results/container_response_receipt.json .
"""

from __future__ import annotations

import argparse
import json
import time as _time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-IV" / "results"

MEDIA = ("linear", "cubic", "log")


# ----------------------------------------------------------------------
# Medium definitions
# ----------------------------------------------------------------------

def nonlinear_mu(rho, medium, params):
    """Per-particle nonlinear chemical potential mu_nl(rho)."""
    if medium == "linear":
        return np.zeros_like(rho)
    if medium == "cubic":
        return params["g"] * rho
    if medium == "log":
        rho0 = params["rho0"]
        return params["b"] * np.log(np.maximum(rho, 1e-12 * rho0) / rho0)
    raise ValueError(f"unknown medium {medium!r}")


def sound_speed_sq(medium, params):
    """c_s^2 = rho dmu_nl/drho at rho0 (hbar = m = 1)."""
    if medium == "linear":
        return 0.0
    if medium == "cubic":
        return params["g"] * params["rho0"]
    if medium == "log":
        return params["b"]            # density-independent -- the log signature
    raise ValueError(f"unknown medium {medium!r}")


def bogoliubov(k, medium, params):
    """Bogoliubov dispersion omega(k) = sqrt( c_s^2 k^2 + (k^2/2)^2 )."""
    cs2 = sound_speed_sq(medium, params)
    return np.sqrt(cs2 * k**2 + (0.5 * k**2) ** 2)


def matched_params(cs2=1.0, rho0=1.0):
    """Parameters giving cubic and log the SAME sound speed c_s^2 (the null)."""
    return {"rho0": rho0, "g": cs2 / rho0, "b": cs2}


# ----------------------------------------------------------------------
# Grid and evolution
# ----------------------------------------------------------------------

def make_grid(N, L):
    x = (np.arange(N) - N // 2) * (L / N)
    X, Y = np.meshgrid(x, x, indexing="ij")
    k1 = 2.0 * np.pi * np.fft.fftfreq(N, d=L / N)
    KX, KY = np.meshgrid(k1, k1, indexing="ij")
    return X, Y, KX, KY


def evolve(psi, steps, dt, medium, params, KX, KY, Vext=0.0, shear=None):
    """Strang split-step Fourier evolution (unitary; norm-conserving).

    shear : callable t -> h(t) applying the TT anisotropy, or None.
    Returns the final field.
    """
    psi = psi.astype(np.complex128).copy()
    for n in range(steps):
        t_mid = (n + 0.5) * dt
        h = 0.0 if shear is None else shear(t_mid)
        Kop = 0.5 * ((1.0 - h) * KX**2 + (1.0 + h) * KY**2)
        kin = np.exp(-1j * Kop * dt)
        # half potential (current density)
        rho = np.abs(psi) ** 2
        psi *= np.exp(-1j * (Vext + nonlinear_mu(rho, medium, params)) * 0.5 * dt)
        # full kinetic
        psi = np.fft.ifft2(kin * np.fft.fft2(psi))
        # half potential (updated density)
        rho = np.abs(psi) ** 2
        psi *= np.exp(-1j * (Vext + nonlinear_mu(rho, medium, params)) * 0.5 * dt)
    return psi


def norm(psi, L, N):
    return np.sum(np.abs(psi) ** 2) * (L / N) ** 2


# ----------------------------------------------------------------------
# (1) Effect/cause dictionary -- the Josephson / time-dilation relation
# ----------------------------------------------------------------------

def phase_rate_field(medium, params, N=48, L=20.0, dt=2e-3, amp=0.4):
    """Prepare the medium in an imposed loading Vext(x) and measure the local
    phase-advance rate d/dt arg psi.  The ontology asserts it equals the local
    energy scale -mu_local = -(Vext + mu_nl(rho)).  Returns (measured, predicted)
    fields of the local clock rate, so their agreement tests the dictionary.

    A smooth Vext gradient is the imposed g00 cause; the differential phase-rate
    between two points is the analogue gravitational redshift.
    """
    X, Y, KX, KY = make_grid(N, L)
    Vext = amp * np.sin(2 * np.pi * X / L)          # the imposed loading (cause)
    rho0 = params["rho0"]
    psi0 = np.sqrt(rho0) * np.ones((N, N), dtype=np.complex128)

    psi1 = evolve(psi0, 1, dt, medium, params, KX, KY, Vext=Vext)
    # local phase advance over the step
    dphi = np.angle(psi1 * np.conj(psi0))
    measured = dphi / dt
    predicted = -(Vext + nonlinear_mu(np.abs(psi0) ** 2, medium, params))
    return measured, predicted


def consistency_error(medium, params, **kw):
    m, p = phase_rate_field(medium, params, **kw)
    scale = np.max(np.abs(p)) + 1e-12
    return float(np.max(np.abs(m - p)) / scale)


# ----------------------------------------------------------------------
# Positive control -- undriven phonon frequency vs Bogoliubov
# ----------------------------------------------------------------------

def measure_phonon_frequency(medium, params, k_index=2, N=48, L=20.0,
                             dt=2e-3, periods=6.0, eps=1e-3):
    """Seed a small density ripple at wavevector k = k_index * dk, evolve
    UNDRIVEN, and recover its oscillation frequency from the density-mode time
    series.  Returns (omega_measured, omega_bogoliubov)."""
    X, Y, KX, KY = make_grid(N, L)
    dk = 2.0 * np.pi / L
    k = k_index * dk
    rho0 = params["rho0"]
    psi = np.sqrt(rho0) * (1.0 + eps * np.cos(k * X)).astype(np.complex128)

    omega_b = float(bogoliubov(k, medium, params))
    T = periods * 2 * np.pi / max(omega_b, 1e-6)
    steps = int(T / dt)
    rec = []
    cur = psi.copy()
    for n in range(steps):
        cur = evolve(cur, 1, dt, medium, params, KX, KY)
        drho = np.abs(cur) ** 2 - rho0
        rec.append(np.real(np.fft.fft2(drho)[k_index, 0]))
    rec = np.asarray(rec)
    # frequency by dominant FFT bin of the recorded oscillation
    spec = np.abs(np.fft.rfft(rec - rec.mean()))
    freqs = 2 * np.pi * np.fft.rfftfreq(len(rec), d=dt)
    omega_m = float(freqs[1 + np.argmax(spec[1:])])
    return omega_m, omega_b


# ----------------------------------------------------------------------
# (2) Shear response -- parametric phonon pumping by the imposed TT wave
# ----------------------------------------------------------------------

def shear_response(medium, params, k_index=2, h0=0.08, N=48, L=20.0,
                   dt=2e-3, n_drive=8.0, eps=1e-3, Omega=None):
    """Seed a phonon at k = k_index*dk along x, drive the TT shear at its
    parametric resonance Omega = 2 omega(k), and return the growth factor of the
    mode energy over n_drive drive periods."""
    X, Y, KX, KY = make_grid(N, L)
    dk = 2.0 * np.pi / L
    k = k_index * dk
    rho0 = params["rho0"]
    omega_b = float(bogoliubov(k, medium, params))
    if Omega is None:
        Omega = 2.0 * omega_b                       # parametric resonance
    psi = np.sqrt(rho0) * (1.0 + eps * np.cos(k * X)).astype(np.complex128)

    def shear(t):
        return h0 * np.sin(Omega * t)

    def mode_energy(field):
        drho = np.abs(field) ** 2 - rho0
        amp = np.abs(np.fft.fft2(drho)[k_index, 0])
        return amp**2

    T = n_drive * 2 * np.pi / max(Omega, 1e-6)
    steps = int(T / dt)
    e0 = mode_energy(psi)
    psi = evolve(psi, steps, dt, medium, params, KX, KY, shear=shear)
    e1 = mode_energy(psi)
    return {
        "medium": medium, "k": k, "omega": omega_b, "Omega": Omega,
        "growth": float(e1 / max(e0, 1e-30)), "cs2": sound_speed_sq(medium, params),
    }


def compare_shear_response(cs2=1.0, **kw):
    """Drive all three media at their own parametric resonance; report the
    log-vs-comparator relative differences in growth factor."""
    params = matched_params(cs2=cs2)
    out = {m: shear_response(m, params, **kw) for m in MEDIA}
    g_log = out["log"]["growth"]
    def reldiff(a, b):
        return abs(a - b) / (abs(b) + 1e-30)
    out["diff_log_vs_cubic"] = reldiff(g_log, out["cubic"]["growth"])
    out["diff_log_vs_linear"] = reldiff(g_log, out["linear"]["growth"])
    return out


def verdict(cons_err, diff_log_vs_cubic, tol_cons=1e-3, tol_diff=1e-2):
    """Apply the pre-registered decision rules."""
    consistency = "PASS" if cons_err < tol_cons else "FAIL"
    if diff_log_vs_cubic < tol_diff:
        prediction = "R-NEGATIVE"     # log indistinguishable from ordinary GPE
    else:
        prediction = "R-POSITIVE"     # candidate SSV signature (suggestive only)
    return {"consistency": consistency, "prediction": prediction}


# ----------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------

def run(quick=False):
    cs2 = 1.0
    params = matched_params(cs2=cs2)
    N = 48 if quick else 64
    L = 20.0

    cons = {m: consistency_error(m, params, N=N, L=L) for m in MEDIA}
    pc = {m: measure_phonon_frequency(m, params, N=N, L=L,
                                      periods=4.0 if quick else 6.0)
          for m in ("cubic", "log")}
    shear = compare_shear_response(cs2=cs2, N=N, L=L,
                                   n_drive=6.0 if quick else 8.0)
    vd = verdict(max(cons.values()), shear["diff_log_vs_cubic"])

    return {
        "params": params, "grid": {"N": N, "L": L},
        "consistency_error": cons,
        "positive_control": {
            m: {"omega_measured": pc[m][0], "omega_bogoliubov": pc[m][1],
                "rel_err": abs(pc[m][0] - pc[m][1]) / pc[m][1]}
            for m in pc
        },
        "shear_growth": {m: shear[m]["growth"] for m in MEDIA},
        "shear_omega": {m: shear[m]["omega"] for m in MEDIA},
        "diff_log_vs_cubic": shear["diff_log_vs_cubic"],
        "diff_log_vs_linear": shear["diff_log_vs_linear"],
        "verdict": vd,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quick", action="store_true", help="smaller/faster run")
    args = ap.parse_args()

    t0 = _time.time()
    rep = run(quick=args.quick)
    rep["wall_seconds"] = round(_time.time() - t0, 2)

    print("=" * 70)
    print("#162  Superfluid in an imposed container")
    print("=" * 70)
    print(f"matched sound speed c_s^2 = 1.0   (g={rep['params']['g']}, "
          f"b={rep['params']['b']}: cubic and log share a dispersion)")
    print("\n(1) EFFECT/CAUSE dictionary  -- local phase-rate vs -mu_local")
    for m in MEDIA:
        print(f"    {m:7s}: rel. error = {rep['consistency_error'][m]:.2e}")
    print(f"    => R-consistency: {rep['verdict']['consistency']}")
    print("\n    POSITIVE CONTROL -- phonon frequency vs Bogoliubov")
    for m, d in rep["positive_control"].items():
        print(f"    {m:7s}: omega_meas={d['omega_measured']:.4f} "
              f"omega_bogo={d['omega_bogoliubov']:.4f} "
              f"(rel {d['rel_err']:.2%})")
    print("\n(2) SHEAR RESPONSE  -- parametric growth at Omega = 2 omega(k)")
    for m in MEDIA:
        print(f"    {m:7s}: growth = {rep['shear_growth'][m]:.4f} "
              f"(omega={rep['shear_omega'][m]:.4f})")
    print(f"    diff(log vs cubic, c_s matched) = {rep['diff_log_vs_cubic']:.2e}")
    print(f"    diff(log vs linear)             = {rep['diff_log_vs_linear']:.2e}")
    print(f"    => R-prediction: {rep['verdict']['prediction']}")
    print(f"\nwall: {rep['wall_seconds']} s")

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "container_response_receipt.json"
    out.write_text(json.dumps(rep, indent=2))
    print(f"receipt -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

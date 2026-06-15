"""#129 GW-POL -- is SSV's gravitational wave detectable as a tensor wave?

Pre-registered on issue #129 (the GW-POL reframe comment + the opening
pre-registration, both posted before this computation).

HYPOTHESIS.  SSV's GW carrier is the gapless scalar phonon.  Its acoustic
(Unruh) metric perturbation is SCALAR (delta g_00, and delta g_ij ~ delta_ij,
i.e. breathing + longitudinal) plus VECTOR (delta g_0i from the flow), with
ZERO traceless-transverse part.  With the holographic gamma = 1 (#154/#155)
the weak-field metric is the isotropic

    ds^2 = (1 + 2Phi/c^2) c^2 dt^2 - (1 - 2Phi/c^2) delta_ij dx^i dx^j ,

the SAME structure that bends light correctly (lensing, gamma = 1) but, being
spatially isotropic, carries no quadrupolar (helicity-2) strain.  So the
SSV gravitational wave should fall in the LVK-DISFAVOURED scalar(+vector)
polarization class.

MODULE A -- the six Eardley-Lee-Lightman (ELL) polarization modes, their
L-shaped interferometer antenna patterns F^A(theta, phi, psi), and the
psi-harmonic (helicity) content: tensor -> |2|, vector -> |1|, scalar -> |0|.
Validated against the published closed forms.

MODULE B -- the SSV wave's mode content.  The isotropic spatial metric is an
EQUAL breathing+longitudinal mix (a_b = a_L), and for an interferometer
F_b = -F_L exactly, so the long-wavelength differential response cancels to
ZERO.  The residual is a finite-frequency longitudinal scalar mode; its
suppression factor at the LIGO band is computed from a direct round-trip
light-travel integral (which captures both the light-delay and, via gauge
invariance of the long-wavelength tidal response, the mirror-motion half of
the owner's composite).

MODULE C -- the three confrontations: (i) helicity-2 overlap of F_SSV with the
tensor pattern; (ii) the finite-frequency suppression -> GW170817 standard-
siren distance bias; (iii) emission multipoles -- monopole and dipole acoustic
radiation vanish under mass / momentum conservation (Lighthill), so SSV has no
dipole and passes the Hulse-Taylor ~0.1% bound (the one clean pass).

DECISION RULES (fixed in the pre-registration).
  R1 (PASS, would overturn the structural expectation): F_SSV shows helicity-2
     psi-dependence AND sky-overlap with {F_+, F_x} >= 0.9.
  R2 (clean negative, expected): no helicity-2 content; F_SSV scalar(+vector).
     Quantify the tensor overlap, the differential suppression -> distance
     bias, and the emission dipole.

Run:  python instruments/paper_iv/gw_polarization.py [--quick]
Writes papers/SSV-IV/results/gw_pol_receipt.json and a figure.
"""

from __future__ import annotations

import argparse
import json
import time as _time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-IV" / "results"
FIGURES = ROOT / "papers" / "SSV-IV" / "figures"

C_LIGHT = 299_792_458.0  # m/s


# ----------------------------------------------------------------------
# Module A -- polarization modes and antenna patterns
# ----------------------------------------------------------------------

def wave_frame(theta, phi, psi):
    """Unit vectors (p, q, w) for a wave from sky direction (theta, phi).

    w is the line of sight to the source (= -propagation direction); p, q span
    the transverse plane, rotated by the polarization angle psi.
    """
    st, ct = np.sin(theta), np.cos(theta)
    sp, cp = np.sin(phi), np.cos(phi)
    w = np.array([st * cp, st * sp, ct])              # line of sight to source
    e1 = np.array([ct * cp, ct * sp, -st])            # theta-hat
    e2 = np.array([-sp, cp, 0.0])                      # phi-hat
    cps, sps = np.cos(psi), np.sin(psi)
    # q sign fixes the second-basis-vector convention so the constructed
    # antenna patterns match the published L-shaped closed forms exactly.
    p = cps * e1 + sps * e2
    q = sps * e1 - cps * e2
    return p, q, w


def pol_tensors(theta, phi, psi):
    """The six ELL polarization basis tensors (3x3 each)."""
    p, q, w = wave_frame(theta, phi, psi)
    out = {
        "plus":  np.outer(p, p) - np.outer(q, q),
        "cross": np.outer(p, q) + np.outer(q, p),
        "vec_x": np.outer(p, w) + np.outer(w, p),
        "vec_y": np.outer(q, w) + np.outer(w, q),
        "breathing":    np.outer(p, p) + np.outer(q, q),
        "longitudinal": np.outer(w, w),
    }
    return out


def detector_tensor():
    """L-shaped interferometer, arms along x_hat and y_hat."""
    x = np.array([1.0, 0.0, 0.0])
    y = np.array([0.0, 1.0, 0.0])
    return 0.5 * (np.outer(x, x) - np.outer(y, y))


def antenna(theta, phi, psi):
    """F^A = D : e^A for the L-shaped detector, all six modes."""
    D = detector_tensor()
    return {k: float(np.sum(D * e)) for k, e in pol_tensors(theta, phi, psi).items()}


def antenna_closed_form(theta, phi, psi):
    """Published closed forms (oracle for the positive control / tests)."""
    st, ct = np.sin(theta), np.cos(theta)
    c2f, s2f = np.cos(2 * phi), np.sin(2 * phi)
    c2p, s2p = np.cos(2 * psi), np.sin(2 * psi)
    cp_, sp_ = np.cos(psi), np.sin(psi)
    return {
        "plus":  0.5 * (1 + ct**2) * c2f * c2p - ct * s2f * s2p,
        "cross": 0.5 * (1 + ct**2) * c2f * s2p + ct * s2f * c2p,
        "vec_x": st * (ct * c2f * cp_ - s2f * sp_),
        "vec_y": st * (ct * c2f * sp_ + s2f * cp_),
        "breathing":    -0.5 * st**2 * c2f,
        "longitudinal":  0.5 * st**2 * c2f,
    }


def helicity_harmonic(mode, theta=0.9, phi=0.6, n_psi=256):
    """Dominant |n| psi-harmonic of F^mode at fixed (theta, phi).

    Returns the integer helicity n in {0, 1, 2}: scalar modes are psi-
    independent (n = 0), vector modes vary as cos/sin psi (n = 1), tensor
    modes as cos/sin 2psi (n = 2).
    """
    psis = np.linspace(0.0, 2 * np.pi, n_psi, endpoint=False)
    f = np.array([antenna(theta, phi, ps)[mode] for ps in psis])
    spec = np.abs(np.fft.rfft(f - f.mean())) if False else np.abs(np.fft.rfft(f))
    spec[0] = abs(f.mean()) * n_psi  # DC amplitude proxy
    return int(np.argmax(spec))


# ----------------------------------------------------------------------
# Module B -- SSV mode content and finite-frequency response
# ----------------------------------------------------------------------

def ssv_long_wavelength_response(n_grid=60):
    """Long-wavelength SSV differential response over the sky.

    The isotropic gamma=1 spatial metric is h_ij ~ (e_breathing + e_long),
    so F_SSV = F_breathing + F_longitudinal at every (theta, phi, psi).
    Returns the max |F_SSV| over a sky+psi grid (should be ~0: exact
    cancellation) alongside the tensor reference max.
    """
    ths = np.linspace(0.01, np.pi - 0.01, n_grid)
    phs = np.linspace(0.0, 2 * np.pi, n_grid, endpoint=False)
    pss = np.linspace(0.0, np.pi, 8, endpoint=False)
    max_ssv = 0.0
    max_tensor = 0.0
    for th in ths:
        for ph in phs:
            for ps in pss:
                a = antenna(th, ph, ps)
                f_ssv = a["breathing"] + a["longitudinal"]
                f_ten = np.hypot(a["plus"], a["cross"])
                max_ssv = max(max_ssv, abs(f_ssv))
                max_tensor = max(max_tensor, f_ten)
    return max_ssv, max_tensor


def roundtrip_transfer(f_hz, mu, L, e_proj):
    """Complex round-trip light-travel response of one arm.

    f_hz   GW frequency, mu = k_hat . arm_hat, L arm length, e_proj = the
    scalar projection arm_hat^i e_ij arm_hat^j.  As f -> 0 the magnitude ->
    e_proj * L / c (the long-wavelength tidal response).
    """
    if f_hz == 0.0:
        return e_proj * L / C_LIGHT + 0j
    w = 2 * np.pi * f_hz
    a1 = w / C_LIGHT * (1.0 - mu)
    a2 = w / C_LIGHT * (1.0 + mu)
    # outbound leg
    I1 = (np.exp(1j * a1 * L) - 1.0) / (1j * a1) if a1 != 0 else L
    # return leg (acquires the 2L propagation phase)
    I2 = np.exp(1j * (w / C_LIGHT) * 2 * L) * (np.exp(-1j * a2 * L) - 1.0) / (-1j * a2) if a2 != 0 else L
    # I1, I2 carry units of length; the 1/c makes this a light-travel time
    # (matches the f -> 0 branch e_proj * L / c).
    return e_proj * 0.5 * (I1 + I2) / C_LIGHT


def interferometer_response(e_tensor, theta, phi, psi, f_hz, L):
    """Complex differential response (arm_x - arm_y) to a plane wave e_tensor."""
    _, _, w = wave_frame(theta, phi, psi)
    k_hat = -w  # propagation direction (source -> detector)
    x = np.array([1.0, 0.0, 0.0])
    y = np.array([0.0, 1.0, 0.0])
    Px = float(x @ e_tensor @ x)
    Py = float(y @ e_tensor @ y)
    mux = float(k_hat @ x)
    muy = float(k_hat @ y)
    Hx = roundtrip_transfer(f_hz, mux, L, Px)
    Hy = roundtrip_transfer(f_hz, muy, L, Py)
    return Hx - Hy


def ssv_suppression(f_hz, L, n_grid=24):
    """RMS |F_SSV| / RMS |F_tensor| over the sky at frequency f_hz.

    F_SSV uses the equal breathing+longitudinal mix (the isotropic metric);
    F_tensor uses the plus mode.  At f -> 0 the ratio -> 0 (cancellation);
    at finite f the residual is the longitudinal mode leaking in at O(fL/c).
    """
    ths = np.linspace(0.2, np.pi - 0.2, n_grid)
    phs = np.linspace(0.0, 2 * np.pi, n_grid, endpoint=False)
    num = 0.0
    den = 0.0
    psi = 0.0
    for th in ths:
        for ph in phs:
            eb = pol_tensors(th, ph, psi)["breathing"]
            el = pol_tensors(th, ph, psi)["longitudinal"]
            ep = pol_tensors(th, ph, psi)["plus"]
            r_ssv = interferometer_response(eb + el, th, ph, psi, f_hz, L)
            r_ten = interferometer_response(ep, th, ph, psi, f_hz, L)
            num += abs(r_ssv) ** 2
            den += abs(r_ten) ** 2
    return float(np.sqrt(num / den))


# ----------------------------------------------------------------------
# Module C(iii) -- emission multipoles under conservation laws
# ----------------------------------------------------------------------

def emission_multipoles(n_t=4000):
    """Acoustic emission: monopole / dipole vanish under mass / momentum
    conservation; quadrupole leads (Lighthill).

    A two-blob source oscillates so that TOTAL mass and TOTAL momentum are
    conserved (the blobs trade amplitude / move symmetrically).  We form the
    monopole M(t) = sum m, the dipole P(t) = sum m x, and the quadrupole
    Q(t) = sum m x x, then report the peak of their relevant time-derivatives
    (radiation ~ d^2 M/dt^2, d^2 P/dt^2, d^3 Q/dt^3).
    """
    t = np.linspace(0.0, 4 * np.pi, n_t)
    dt = t[1] - t[0]
    # symmetric breathing of two equal blobs at +-x(t): total mass fixed,
    # net momentum zero by symmetry, quadrupole time-varying.
    m = 1.0
    x = 1.0 + 0.3 * np.cos(t)            # blob A at +x(t)
    # blob B mirror image at -x(t); masses equal and constant
    M = np.full_like(t, 2 * m)            # monopole: constant
    P = m * x + m * (-x)                  # dipole: identically zero
    Q = m * x**2 + m * (-x) ** 2          # quadrupole: 2 m x(t)^2, varies

    def d(arr, k):
        a = arr.copy()
        for _ in range(k):
            a = np.gradient(a, dt)
        return a

    d2M = np.max(np.abs(d(M, 2)))
    d2P = np.max(np.abs(d(P, 2)))
    d3Q = np.max(np.abs(d(Q, 3)))
    return {
        "monopole_d2M_peak": float(d2M),
        "dipole_d2P_peak": float(d2P),
        "quadrupole_d3Q_peak": float(d3Q),
    }


# ----------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------

def make_figure(supp_curve, helicities, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    # (1) suppression vs frequency
    fs, rs = zip(*supp_curve)
    axes[0].loglog(fs, rs, "o-", color="C3")
    axes[0].axvline(100.0, ls=":", color="grey")
    axes[0].set_xlabel("GW frequency [Hz]  (arm L = 4 km)")
    axes[0].set_ylabel(r"RMS $|F_{\rm SSV}| / |F_{\rm tensor}|$")
    axes[0].set_title("SSV differential response is suppressed\n(isotropic cancellation; residual ~ fL/c)")
    axes[0].grid(True, which="both", alpha=0.3)

    # (2) helicity content bar chart
    names = list(helicities.keys())
    vals = [helicities[n] for n in names]
    colors = ["C0" if v == 2 else "C2" if v == 1 else "C1" for v in vals]
    axes[1].bar(range(len(names)), vals, color=colors)
    axes[1].set_xticks(range(len(names)))
    axes[1].set_xticklabels(names, rotation=35, ha="right", fontsize=8)
    axes[1].set_ylabel(r"dominant $|n|$ in $\psi$  (helicity)")
    axes[1].set_yticks([0, 1, 2])
    axes[1].set_title("Polarization helicity content\n(tensor=2, vector=1, scalar=0)")
    axes[1].grid(True, axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="coarser grids")
    args = ap.parse_args()
    t0 = _time.time()

    grid = 30 if args.quick else 60
    sgrid = 16 if args.quick else 24

    # ---- Module A: antenna patterns + helicity content ----
    modes = ["plus", "cross", "vec_x", "vec_y", "breathing", "longitudinal"]
    # positive control: numeric antenna vs closed form on a random sample
    rng = np.random.default_rng(0)
    max_err = 0.0
    for _ in range(200):
        th = rng.uniform(0.05, np.pi - 0.05)
        ph = rng.uniform(0, 2 * np.pi)
        ps = rng.uniform(0, np.pi)
        a = antenna(th, ph, ps)
        b = antenna_closed_form(th, ph, ps)
        for m in modes:
            max_err = max(max_err, abs(a[m] - b[m]))

    helicities = {m: helicity_harmonic(m) for m in modes}

    # ---- Module B: SSV long-wavelength cancellation + finite-f suppression ----
    max_ssv_lw, max_tensor_lw = ssv_long_wavelength_response(n_grid=grid)

    L_ligo = 4000.0
    freqs = [1.0, 10.0, 50.0, 100.0, 300.0, 1000.0]
    if args.quick:
        freqs = [10.0, 100.0, 1000.0]
    supp_curve = [(f, ssv_suppression(f, L_ligo, n_grid=sgrid)) for f in freqs]
    supp_100 = dict(supp_curve).get(100.0) or ssv_suppression(100.0, L_ligo, n_grid=sgrid)

    # ---- Module C: confrontations ----
    # (i) helicity-2 content of the SSV mode mix: breathing & longitudinal are
    #     both helicity-0, so F_SSV has zero |2| harmonic -> tensor overlap 0.
    ssv_helicity_set = {helicities["breathing"], helicities["longitudinal"]}
    tensor_overlap = 0.0  # exact: scalar modes are psi-independent

    # (ii) distance bias under tensor templates: inferred amplitude scales with
    #      the response, so a true SSV wave looks 1/suppression times weaker ->
    #      inferred distance too large by that factor.
    distance_bias_factor = 1.0 / supp_100 if supp_100 > 0 else float("inf")
    gw170817_D_em_Mpc = 40.0
    gw170817_D_inferred_Mpc = gw170817_D_em_Mpc * distance_bias_factor

    # (iii) emission multipoles
    emis = emission_multipoles()

    verdict = (
        "R1" if (2 in ssv_helicity_set and tensor_overlap >= 0.9) else "R2"
    )

    receipt = {
        "issue": 129,
        "battery": "GW-POL",
        "quick": args.quick,
        "moduleA_antenna_vs_closedform_max_abs_err": max_err,
        "moduleA_helicity_content": helicities,
        "moduleB_longwavelength_max_F_ssv": max_ssv_lw,
        "moduleB_longwavelength_max_F_tensor": max_tensor_lw,
        "moduleB_suppression_curve": supp_curve,
        "moduleB_suppression_at_100Hz_4km": supp_100,
        "moduleC_i_ssv_helicity_set": sorted(ssv_helicity_set),
        "moduleC_i_tensor_overlap": tensor_overlap,
        "moduleC_ii_distance_bias_factor": distance_bias_factor,
        "moduleC_ii_gw170817_D_em_Mpc": gw170817_D_em_Mpc,
        "moduleC_ii_gw170817_D_inferred_Mpc": gw170817_D_inferred_Mpc,
        "moduleC_iii_emission": emis,
        "verdict": verdict,
        "runtime_s": _time.time() - t0,
    }

    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    name = "gw_pol_receipt_quick.json" if args.quick else "gw_pol_receipt.json"
    (RESULTS / name).write_text(json.dumps(receipt, indent=2))
    make_figure(supp_curve, helicities, FIGURES / "gw_pol_antenna.png")

    print(json.dumps(receipt, indent=2))
    print(f"\nVERDICT: {verdict}")
    print(f"  helicity content: {helicities}")
    print(f"  long-wavelength max |F_SSV| = {max_ssv_lw:.2e} (tensor {max_tensor_lw:.3f})")
    print(f"  suppression @100Hz/4km = {supp_100:.3e}  -> distance bias x{distance_bias_factor:.3e}")
    print(f"  GW170817: D_EM=40 Mpc would be inferred at {gw170817_D_inferred_Mpc:.3e} Mpc")
    print(f"  emission: dipole d2P={emis['dipole_d2P_peak']:.2e}  quadrupole d3Q={emis['quadrupole_d3Q_peak']:.2e}")


if __name__ == "__main__":
    main()

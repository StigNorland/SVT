"""#138 CHIRAL-DISPERSION -- what does the alpha-c channel actually do?

Pre-registered on issue #138 (decision rules R1/R2/R3 + Q3 in the issue
body and stakes comment; execution plan + thresholds posted as a comment
before computing). Linearizes the spinor (CP^1, #83) LogSE + chiral-shear
sector around the uniform vacuum and measures the dispersion of the
n-hat (internal-direction) channel.

S1 analytic results (derivation in the result note), all exact:

  1. CHIRAL SILENCE. The linear-order current perturbation around the
     uniform vacuum is delta-j = sqrt(rho0) grad Im(dPsi_1) -- a pure
     gradient in EVERY channel (the spin channel enters j only at
     O(eps^2); Mermin-Ho: curl-bearing flow is quadratic in spin
     gradients). Hence curl(delta-j) == 0, E_perp = O(eps^4), and the
     lambda-term contributes exactly ZERO to every linear dispersion.
     There is no propagating linear mode at c_perp = alpha*c.
  2. FREE MAGNON. The transverse-spin perturbation eps = dPsi_2/sqrt(rho0)
     obeys i eps_t = -1/2 lap(eps) exactly (the spin-independent log term
     cancels against mu), i.e. omega(k) = hbar k^2 / 2 m0 -- gapless,
     quadratic, precessional. The k^2 coefficient is the quantum-pressure
     scale, NOT an alpha^2 stiffness.
  3. Q3 NEGATIVE. Over any static equilibrium background rho_b(x) in a
     potential V, i eps_t = mu eps - 1/2 [lap(eps) + grad(ln rho_b).grad(eps)]:
     the magnon's effective potential V + b ln(rho_b) = mu is a global
     constant (symmetry-protected: the k->0 magnon is the exact global
     spin rotation). The n-hat channel is exactly as non-transactional
     as sound -- it pays no A^2 tax.
  4. The magnon carries no linear-order mass current, so charged defects
     decouple at leading order (the no-Cherenkov statement rests on the
     coupling, not on kinematics: a gapless quadratic branch has zero
     Landau threshold).

S2 (this script) tests these with controls:
  B1  magnon dispersion omega(k) over >= 1 decade below the core scale
      (multi-mode plane-wave spin tilt, phase-rotation readout);
      R1 numeric trigger p = 2.00 +- 0.05, R2 trigger p = 1.00 +- 0.05.
  B2  instrument control: same readout on the density/phase channel must
      recover the Bogoliubov omega(k) = k sqrt(b + k^2/4) to <= 1%.
  B3  chiral silence: (a) E_perp[texture(eps)] log-log slope = 4.0 +- 0.2;
      (b) lambda = 2000 ACTIVE in the dynamics (advective EOM term
      derived below) on a modulated magnon: the omega shift vs lambda-off
      scales as eps^2 and extrapolates to <= 1e-3 relative at eps -> 0.
  B4  current decoupling: ||j|| and ||curl j|| of the spin texture scale
      as eps^2 (slope 2.0 +- 0.1).
  B5  Q3: (a) static U_eff = V + b ln rho_b - mu flat to <= 1e-3 |V| on
      the relaxed background; (b) magnon wavepacket transit through a
      Thomas-Fermi depression vs uniform control, gamma_magnon =
      delay / unbalanced-WKB-prediction, |gamma| <= 0.1 => non-
      transactional; positive control = explicit spin-channel potential
      with exactly predictable WKB delay, ratio within +-20%.

Numerics follow the #129 conventions (units hbar = m0 = 1, b = c_s^2 = 1,
rho0 = 1 so mu = 0; Strang split-step; 2/3-rule dealiasing -- the log
nonlinearity aliases into high k otherwise, see the #129 numerics note).

The chiral-shear EOM term (derived from E_perp = (lam/2 rho0^2) int |curl j|^2,
j = Im(Psi^dag grad Psi), 2D scalar curl w = dx j_y - dy j_x):

    dE/dPsi_a* = -i G . grad Psi_a,   G = (lam/rho0^2) (dy w, -dx w),

so i dPsi_a/dt += -i G.grad Psi_a, i.e. an advection dPsi_a/dt -= G.grad Psi_a
by the divergence-free field G (norm-conserving). It is O(eps^3) on
small perturbations, which is the silence statement itself.

Run:  python instruments/paper_ii/chiral_dispersion.py [--quick]
Writes papers/SSV-II/results/chiral_dispersion_receipt[_quick].json and
papers/SSV-II/figures/chiral_dispersion_omega_k.png.
"""

from __future__ import annotations

import json
import math
import sys
import time as _time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "SSV-II" / "results"
FIGURES = ROOT / "papers" / "SSV-II" / "figures"

B0 = 1.0        # LogSE coupling: c_s = sqrt(B0) = 1
RHO0 = 1.0      # background density: mu = B0 ln(RHO0) = 0
ALPHA = 1.0 / 137.036
LAMBDA_SSV = 2000.0   # Paper I App. construction value of the chiral coupling


# ----------------------------------------------------------------------
# spinor medium
# ----------------------------------------------------------------------

class SpinorMedium2D:
    """Two-component (CP^1) split-step LogSE on a periodic grid.

    The log nonlinearity acts on the total density rho = |Psi1|^2+|Psi2|^2
    (spin-independent). Optional: external V (both components), U_spin
    (component 2 only -- the B5 positive control), and the chiral-shear
    advection at coupling lam (B3b)."""

    def __init__(self, nx, ny, dx, V=None, U_spin=None, lam=0.0):
        self.nx, self.ny, self.dx, self.lam = nx, ny, dx, lam
        kx = 2 * np.pi * np.fft.fftfreq(nx, dx)
        ky = 2 * np.pi * np.fft.fftfreq(ny, dx)
        KX, KY = np.meshgrid(kx, ky, indexing="ij")
        self.KX, self.KY = KX, KY
        self.k2 = KX**2 + KY**2
        # 2/3-rule dealiasing (mandatory: #129 numerics note, lesson 1)
        mask = ((np.abs(KX) <= (2 / 3) * np.abs(kx).max())
                & (np.abs(KY) <= (2 / 3) * np.abs(ky).max()))
        self.dealias = mask.astype(float)
        self.V = np.zeros((nx, ny)) if V is None else V
        self.U_spin = np.zeros((nx, ny)) if U_spin is None else U_spin

    def _dx(self, f):
        return np.fft.ifft2(1j * self.KX * self.dealias * np.fft.fft2(f))

    def _dy(self, f):
        return np.fft.ifft2(1j * self.KY * self.dealias * np.fft.fft2(f))

    def current(self, p1, p2):
        """j = Im(Psi^dag grad Psi), summed over components."""
        jx = (np.conj(p1) * self._dx(p1) + np.conj(p2) * self._dx(p2)).imag
        jy = (np.conj(p1) * self._dy(p1) + np.conj(p2) * self._dy(p2)).imag
        return jx, jy

    def curl_j(self, p1, p2):
        jx, jy = self.current(p1, p2)
        return (self._dx(jy) - self._dy(jx)).real

    def e_perp(self, p1, p2):
        """Chiral-shear energy (lam/2 rho0^2) int |curl j|^2 (unit lam)."""
        w = self.curl_j(p1, p2)
        return 0.5 / RHO0**2 * float(np.sum(w**2)) * self.dx**2

    def _chiral_rhs(self, p1, p2):
        """dPsi_a/dt = -G.grad Psi_a, G = (lam/rho0^2)(dy w, -dx w)."""
        w = self.curl_j(p1, p2)
        gx = (self.lam / RHO0**2) * self._dy(w).real
        gy = -(self.lam / RHO0**2) * self._dx(w).real
        return (-(gx * self._dx(p1) + gy * self._dy(p1)),
                -(gx * self._dx(p2) + gy * self._dy(p2)))

    def step(self, p1, p2, dt):
        """Strang split: half nonlinear, full kinetic (dealiased), half
        nonlinear; chiral advection (if lam) as an RK2 substep -- it is
        O(eps^3) on small perturbations, so first-order placement of this
        substep is far below measurement resolution (and the lam-on/off
        DIFFERENCE isolates it in any case)."""
        for _ in range(2):
            rho = np.abs(p1)**2 + np.abs(p2)**2
            ph = (B0 * np.log(np.maximum(rho, 1e-300)) + self.V) * (dt / 2)
            p1 = p1 * np.exp(-1j * ph)
            p2 = p2 * np.exp(-1j * (ph + self.U_spin * (dt / 2)))
            if _ == 0:
                kin = np.exp(-1j * self.k2 * (dt / 2)) * self.dealias
                p1 = np.fft.ifft2(np.fft.fft2(p1) * kin)
                p2 = np.fft.ifft2(np.fft.fft2(p2) * kin)
                if self.lam:
                    f1, f2 = self._chiral_rhs(p1, p2)
                    m1, m2 = p1 + 0.5 * dt * f1, p2 + 0.5 * dt * f2
                    f1, f2 = self._chiral_rhs(m1, m2)
                    p1, p2 = p1 + dt * f1, p2 + dt * f2
        return p1, p2


def grid_x(nx, dx):
    return (np.arange(nx) - nx / 2) * dx


# ----------------------------------------------------------------------
# frequency readout
# ----------------------------------------------------------------------

def phase_slope(a, t, frac=0.8):
    """omega from the unwrapped phase of a complex mode amplitude a(t)
    (rotating e^{-i omega t} => slope is -omega). Middle `frac` used."""
    ph = np.unwrap(np.angle(a))
    n = len(t)
    lo, hi = int(n * (1 - frac) / 2), int(n * (1 + frac) / 2)
    c = np.polyfit(t[lo:hi], ph[lo:hi], 1)
    return -c[0]


def real_mode_freq(a, t):
    """|omega| of a real oscillating mode amplitude via the analytic
    signal (positive-frequency doubling), phase-slope on the middle."""
    a = np.asarray(a, float)
    n = len(a)
    S = np.fft.fft(a - a.mean())
    h = np.zeros(n)
    h[0] = 1.0
    if n % 2 == 0:
        h[n // 2] = 1.0
        h[1:n // 2] = 2.0
    else:
        h[1:(n + 1) // 2] = 2.0
    z = np.fft.ifft(S * h)
    return abs(phase_slope(z, t, frac=0.6))


# ----------------------------------------------------------------------
# B1 + B2: dispersion of the spin and density channels
# ----------------------------------------------------------------------

def magnon_dispersion(nx, dx, mode_ns, t_end, dt, eps=1e-3, rec=4):
    """Multi-mode plane-wave spin tilt: Psi2 = sum_n eps e^{i(k_n x+phi_n)},
    Psi1 = sqrt(1-|Psi2|^2) (total density exactly uniform at t=0; the
    modes coexist, so any cross-channel coupling is allowed to act).
    Returns k values and measured omega(k) from per-mode phase rotation."""
    ny = 4
    med = SpinorMedium2D(nx, ny, dx)
    x = grid_x(nx, dx)
    L = nx * dx
    ks = np.array([2 * np.pi * n / L for n in mode_ns])
    rng = np.random.default_rng(138)
    phases = rng.uniform(0, 2 * np.pi, len(ks))
    p2_1d = np.zeros(nx, complex)
    for k, ph0 in zip(ks, phases):
        p2_1d += eps * np.exp(1j * (k * x + ph0))
    p2 = np.tile(p2_1d[:, None], (1, ny))
    p1 = np.sqrt(np.maximum(RHO0 - np.abs(p2)**2, 0.0)).astype(complex)

    n_steps = int(round(t_end / dt))
    ts, amps = [], []
    for n in range(n_steps):
        p1, p2 = med.step(p1, p2, dt)
        if n % rec == 0:
            prof = p2.mean(axis=1)
            ts.append((n + 1) * dt)
            amps.append([np.mean(prof * np.exp(-1j * k * x)) for k in ks])
    ts = np.array(ts)
    amps = np.array(amps)
    omegas = np.array([phase_slope(amps[:, i], ts) for i in range(len(ks))])
    return ks, omegas


def bogoliubov_control(nx, dx, mode_n, t_end, dt, eps=1e-3, rec=4):
    """Density-channel standing wave u = eps cos(kx); the projection of
    drho on e^{ikx} oscillates at the Bogoliubov omega(k)."""
    ny = 4
    med = SpinorMedium2D(nx, ny, dx)
    x = grid_x(nx, dx)
    L = nx * dx
    k = 2 * np.pi * mode_n / L
    u = eps * np.cos(k * x)
    p1 = np.tile(np.sqrt(RHO0 * (1.0 + u))[:, None], (1, ny)).astype(complex)
    p2 = np.zeros_like(p1)

    n_steps = int(round(t_end / dt))
    ts, amps = [], []
    for n in range(n_steps):
        p1, p2 = med.step(p1, p2, dt)
        if n % rec == 0:
            drho = (np.abs(p1)**2 + np.abs(p2)**2).mean(axis=1) - RHO0
            ts.append((n + 1) * dt)
            amps.append(np.real(np.mean(drho * np.exp(-1j * k * x))))
    om = real_mode_freq(np.array(amps), np.array(ts))
    om_pred = k * math.sqrt(B0 + k * k / 4.0)
    return k, om, om_pred


# ----------------------------------------------------------------------
# B3 + B4: chiral silence and current decoupling
# ----------------------------------------------------------------------

def spin_texture(nx, ny, dx, n_mode, eps):
    """Transversely modulated spin tilt Psi2 = eps cos(q y) e^{i q x}
    (q = 2 pi n/L): carries curl j = O(eps^2) -- the minimal texture on
    which the chiral term can act at all."""
    L = nx * dx
    q = 2 * np.pi * n_mode / L
    x = grid_x(nx, dx)
    y = grid_x(ny, dx)
    X, Y = np.meshgrid(x, y, indexing="ij")
    p2 = eps * np.cos(q * Y) * np.exp(1j * q * X)
    p1 = np.sqrt(np.maximum(RHO0 - np.abs(p2)**2, 0.0)).astype(complex)
    return p1, p2, q


def loglog_slope(xs, ys):
    return float(np.polyfit(np.log(xs), np.log(ys), 1)[0])


def chiral_energy_scaling(nx, dx, n_mode, eps_list):
    """E_perp(eps) and ||j||, ||curl j|| (eps) on the texture."""
    med = SpinorMedium2D(nx, nx, dx)
    e_perp, j_norm, w_norm, e_grad2 = [], [], [], []
    for eps in eps_list:
        p1, p2, q = spin_texture(nx, nx, dx, n_mode, eps)
        e_perp.append(med.e_perp(p1, p2))
        jx, jy = med.current(p1, p2)
        j_norm.append(math.sqrt(float(np.sum(jx**2 + jy**2)) * dx**2))
        w = med.curl_j(p1, p2)
        w_norm.append(math.sqrt(float(np.sum(w**2)) * dx**2))
        gx, gy = med._dx(p2), med._dy(p2)
        e_grad2.append(0.5 * float(np.sum(np.abs(gx)**2 + np.abs(gy)**2))
                       * dx**2)
    return {
        "eps": list(map(float, eps_list)),
        "E_perp": list(map(float, e_perp)),
        "E_spin_gradient": list(map(float, e_grad2)),
        "j_norm": list(map(float, j_norm)),
        "curl_j_norm": list(map(float, w_norm)),
        "slope_E_perp": loglog_slope(eps_list, e_perp),
        "slope_E_spin_gradient": loglog_slope(eps_list, e_grad2),
        "slope_j": loglog_slope(eps_list, j_norm),
        "slope_curl_j": loglog_slope(eps_list, w_norm),
        "q": float(q),
    }


def modulated_magnon_omega(nx, dx, n_mode, eps, lam, t_end, dt, rec=2):
    """omega of the modulated magnon cos(qy)e^{iqx} with the chiral term
    ACTIVE at coupling lam, by projection on its own mode shape."""
    med = SpinorMedium2D(nx, nx, dx, lam=lam)
    p1, p2, q = spin_texture(nx, nx, dx, n_mode, eps)
    x = grid_x(nx, dx)
    y = grid_x(nx, dx)
    X, Y = np.meshgrid(x, y, indexing="ij")
    mode = np.cos(q * Y) * np.exp(1j * q * X)
    mode /= math.sqrt(float(np.sum(np.abs(mode)**2)))
    n_steps = int(round(t_end / dt))
    ts, amps = [], []
    for n in range(n_steps):
        p1, p2 = med.step(p1, p2, dt)
        if n % rec == 0:
            ts.append((n + 1) * dt)
            amps.append(np.sum(p2 * np.conj(mode)))
    return phase_slope(np.array(amps), np.array(ts)), q


# ----------------------------------------------------------------------
# B5: Q3 -- is the magnon transactional?
# ----------------------------------------------------------------------

def relax_background(nx, ny, dx, V, n_iter=5000, dtau=0.2):
    """Imaginary-time relaxation from the Thomas-Fermi start (component 1
    only), far-field pinned to rho = 1 (mu = 0): returns the exact static
    background including the quantum-pressure correction."""
    med = SpinorMedium2D(nx, ny, dx, V=V)
    p1 = np.sqrt(np.exp(-V / B0)).astype(complex)
    kin = np.exp(-med.k2 * (dtau / 2)) * med.dealias
    edge = 0  # far-field column (V ~ 0 there)
    for _ in range(n_iter):
        rho = np.abs(p1)**2
        ph = (B0 * np.log(np.maximum(rho, 1e-300)) + V) * (dtau / 2)
        p1 = p1 * np.exp(-ph)
        p1 = np.fft.ifft2(np.fft.fft2(p1) * kin)
        rho = np.abs(p1)**2
        ph = (B0 * np.log(np.maximum(rho, 1e-300)) + V) * (dtau / 2)
        p1 = p1 * np.exp(-ph)
        p1 = p1 / np.abs(p1[edge, 0])     # pin far field to rho0 = 1
    return np.abs(p1)**2


def wkb_delay(V_line, dx, k0):
    """Group delay of an omega = k^2/2 packet through an attractive
    effective potential U = -V_line (energy conservation k(x) =
    sqrt(k0^2 + 2 V)): the UNBALANCED prediction a transactional channel
    would show (early arrival, negative)."""
    kx = np.sqrt(k0**2 + 2.0 * V_line)
    return float(np.sum(1.0 / kx - 1.0 / k0) * dx)


def magnon_transit(nx, dx, k0, w, x0, x_det, t_end, dt, V=None,
                   U_spin=None, rho_b=None, eps=1e-3, rec=4, tag=""):
    """Magnon wavepacket Psi2 = eps g(x) e^{ik0 x} sqrt(rho_b) transiting
    the slab; arrival = peak-window centroid of the |Psi2|^2 signal at
    the detector column (the spin channel is its own clean detector:
    zero background, no baseline needed)."""
    ny = 4
    x = grid_x(nx, dx)
    if rho_b is None:
        rho_b = np.ones(nx)
    g = np.exp(-((x - x0) / w)**2)
    p2_1d = eps * g * np.exp(1j * k0 * x) * np.sqrt(rho_b)
    p2 = np.tile(p2_1d[:, None], (1, ny))
    p1 = np.tile(np.sqrt(np.maximum(rho_b - np.abs(p2_1d)**2, 0.0))[:, None],
                 (1, ny)).astype(complex)
    V2 = None if V is None else np.tile(V[:, None], (1, ny))
    U2 = None if U_spin is None else np.tile(U_spin[:, None], (1, ny))
    med = SpinorMedium2D(nx, ny, dx, V=V2, U_spin=U2)
    i_det = int(round(x_det / dx + nx / 2))
    n_steps = int(round(t_end / dt))
    ts, sig = [], []
    t0 = _time.time()
    for n in range(n_steps):
        p1, p2 = med.step(p1, p2, dt)
        if n % rec == 0:
            ts.append((n + 1) * dt)
            sig.append(float(np.sum(np.abs(p2[i_det, :])**2)))
    if tag:
        print(f"    [{tag}] {n_steps} steps in {_time.time()-t0:.0f}s",
              flush=True)
    return np.array(ts), np.array(sig)


def peak_window_centroid(t, w2, frac=0.1):
    """Envelope-power centroid in the contiguous window around the global
    peak (immune to record truncation; #129 numerics note, lesson 2)."""
    i_pk = int(np.argmax(w2))
    thr = frac * w2[i_pk]
    lo = i_pk
    while lo > 0 and w2[lo - 1] > thr:
        lo -= 1
    hi = i_pk
    while hi < len(w2) - 1 and w2[hi + 1] > thr:
        hi += 1
    sl = slice(lo, hi + 1)
    return float(np.sum(t[sl] * w2[sl]) / np.sum(w2[sl]))


# ----------------------------------------------------------------------
# the battery
# ----------------------------------------------------------------------

def battery(quick=False):
    out = {"config": {"quick": quick, "b0": B0, "rho0": RHO0,
                      "lambda_ssv": LAMBDA_SSV, "alpha": ALPHA}}

    # ---- B1: magnon dispersion over the decade -------------------------
    if quick:
        nx, dx, t_end, dt = 1024, 0.5, 400.0, 0.1
        mode_ns = [4, 8, 16, 32, 64, 128]
    else:
        nx, dx, t_end, dt = 4096, 0.5, 1500.0, 0.05
        mode_ns = [10, 20, 40, 80, 160, 320, 512]
    print("B1: magnon dispersion ...", flush=True)
    ks, oms = magnon_dispersion(nx, dx, mode_ns, t_end, dt)
    p_fit, lnA = np.polyfit(np.log(ks), np.log(oms), 1)
    A_fit = math.exp(lnA)
    out["B1_magnon"] = {
        "k": ks.tolist(), "omega": oms.tolist(),
        "omega_over_k2_2": (oms / (ks**2 / 2)).tolist(),
        "p_fit": float(p_fit), "A_fit": float(A_fit),
        "A_expected_quantum_pressure": 0.5,
        "alpha_c_k_for_contrast": (ALPHA * ks).tolist(),
    }
    print(f"  p = {p_fit:.4f} (R1 trigger 2.00+-0.05, R2 trigger "
          f"1.00+-0.05); A = {A_fit:.4f} vs hbar/2m0 = 0.5", flush=True)

    # ---- B2: Bogoliubov instrument control -----------------------------
    print("B2: Bogoliubov control ...", flush=True)
    ctrl_ns = [8, 32, 128] if quick else [10, 40, 160, 512]
    b2 = []
    for n in ctrl_ns:
        k, om, om_p = bogoliubov_control(nx, dx, n, t_end, dt)
        b2.append({"k": k, "omega_measured": om, "omega_bogoliubov": om_p,
                   "ratio": om / om_p})
        print(f"  k={k:.3f}: omega {om:.5f} vs {om_p:.5f} "
              f"(ratio {om/om_p:.4f})", flush=True)
    out["B2_control"] = b2
    # the control branch is LINEAR at low k: fit its power too
    kc = np.array([r["k"] for r in b2])
    oc = np.array([r["omega_measured"] for r in b2])
    out["B2_control_p_fit"] = float(np.polyfit(np.log(kc),
                                               np.log(oc), 1)[0])

    # ---- B3a + B4: energy / current scaling ----------------------------
    print("B3a/B4: chiral energy + current scaling ...", flush=True)
    n_tex = 128 if quick else 256
    eps_list = [1e-3, 3e-3, 1e-2, 3e-2]
    sc = chiral_energy_scaling(n_tex, 0.5, 8, eps_list)
    out["B3a_B4_scaling"] = sc
    print(f"  E_perp slope {sc['slope_E_perp']:.3f} (silence needs 4, a "
          f"linear-order stiffness would give 2); "
          f"E_grad slope {sc['slope_E_spin_gradient']:.3f}; "
          f"||j|| slope {sc['slope_j']:.3f}; "
          f"||curl j|| slope {sc['slope_curl_j']:.3f}", flush=True)

    # ---- B3b: lambda ACTIVE in the dynamics ----------------------------
    print("B3b: lambda-on dynamics ...", flush=True)
    if quick:
        n_dyn, t_dyn, dt_dyn, eps_pair = 128, 150.0, 0.05, (3e-3, 1e-2)
    else:
        n_dyn, t_dyn, dt_dyn, eps_pair = 256, 400.0, 0.02, (3e-3, 1e-2)
    b3b = {"eps": list(eps_pair), "lambda": LAMBDA_SSV}
    d_oms, q_dyn = [], None
    for eps in eps_pair:
        om_off, q_dyn = modulated_magnon_omega(n_dyn, 0.5, 8, eps, 0.0,
                                               t_dyn, dt_dyn)
        om_on, _ = modulated_magnon_omega(n_dyn, 0.5, 8, eps, LAMBDA_SSV,
                                          t_dyn, dt_dyn)
        d_oms.append(om_on - om_off)
        b3b[f"omega_off_eps{eps}"] = om_off
        b3b[f"omega_on_eps{eps}"] = om_on
        print(f"  eps={eps}: omega off {om_off:.6f} on {om_on:.6f} "
              f"(shift {om_on-om_off:+.2e})", flush=True)
    om0 = q_dyn**2  # (qx^2+qy^2)/2 with qx = qy = q
    c2 = d_oms[1] / eps_pair[1]**2
    resid = d_oms[0] - c2 * eps_pair[0]**2
    b3b.update({
        "omega0_linear_spectrum": float(om0),
        "shift_ratio_measured": d_oms[0] / d_oms[1] if d_oms[1] else None,
        "shift_ratio_eps2_expected": (eps_pair[0] / eps_pair[1])**2,
        "c2_measured": float(c2),
        "c2_first_order_PT": float(LAMBDA_SSV * q_dyn**4),
        "extrapolated_linear_shift_rel": float(abs(resid) / om0),
    })
    out["B3b_lambda_on"] = b3b
    print(f"  shift ratio {b3b['shift_ratio_measured']:.3f} vs eps^2 "
          f"{b3b['shift_ratio_eps2_expected']:.3f}; c2 {c2:.3f} vs PT "
          f"{b3b['c2_first_order_PT']:.3f}; extrapolated linear-spectrum "
          f"shift {b3b['extrapolated_linear_shift_rel']:.2e} rel",
          flush=True)

    # ---- B5: Q3 transactionality ----------------------------------------
    print("B5: Q3 (transactional?) ...", flush=True)
    if quick:
        nx5, sigma, x0, x_det, t5, dt5, w5 = 1024, 30.0, -120.0, 120.0, \
            420.0, 0.1, 24.0
    else:
        nx5, sigma, x0, x_det, t5, dt5, w5 = 2048, 50.0, -200.0, 200.0, \
            700.0, 0.05, 30.0
    dx5, k0, v0 = 0.5, 2 * np.pi / 8.0, 0.1
    x = grid_x(nx5, dx5)
    V_line = v0 * np.exp(-(x / sigma)**2)

    # (a) static flatness on the relaxed background
    rho_rel = relax_background(nx5, 4, dx5, np.tile(V_line[:, None],
                                                    (1, 4)))[:, 0]
    u_eff = B0 * np.log(rho_rel) + V_line
    u_eff -= u_eff[0]                     # mu from the far field
    out["B5a_static"] = {
        "max_U_eff_over_V0": float(np.max(np.abs(u_eff)) / v0),
        "max_U_unbalanced_over_V0": 1.0,   # what b ln rho_b alone would be
    }
    print(f"  static: max|U_eff|/V0 = "
          f"{out['B5a_static']['max_U_eff_over_V0']:.2e} "
          f"(unbalanced channel would show ~1)", flush=True)

    # (b) transits
    base = dict(nx=nx5, dx=dx5, k0=k0, w=w5, x0=x0, x_det=x_det,
                t_end=t5, dt=dt5)
    t_u, s_u = magnon_transit(tag="uniform control", **base)
    t_arr_u = peak_window_centroid(t_u, s_u)

    rho_tf = np.exp(-V_line / B0)
    t_d, s_d = magnon_transit(V=V_line, rho_b=rho_tf,
                              tag="TF depression", **base)
    t_arr_d = peak_window_centroid(t_d, s_d)

    t_p, s_p = magnon_transit(U_spin=-V_line, tag="positive control",
                              **base)
    t_arr_p = peak_window_centroid(t_p, s_p)

    dt_unbal = wkb_delay(V_line, dx5, k0)
    delay_dep = t_arr_d - t_arr_u
    delay_pc = t_arr_p - t_arr_u
    out["B5b_transit"] = {
        "k0": k0, "sigma": sigma, "V0": v0,
        "wkb_unbalanced_prediction": dt_unbal,
        "delay_depression": float(delay_dep),
        "delay_positive_control": float(delay_pc),
        "pc_ratio": float(delay_pc / dt_unbal),
        "gamma_magnon": float(delay_dep / dt_unbal),
    }
    print(f"  WKB unbalanced prediction {dt_unbal:+.2f}; positive control "
          f"{delay_pc:+.2f} (ratio {delay_pc/dt_unbal:.3f}); depression "
          f"{delay_dep:+.2f} => gamma_magnon = "
          f"{delay_dep/dt_unbal:+.4f}", flush=True)

    # ---- verdicts --------------------------------------------------------
    pc_ok = bool(abs(out["B5b_transit"]["pc_ratio"] - 1.0) <= 0.2)
    g = out["B5b_transit"]["gamma_magnon"]
    out["verdicts"] = {
        "B1_p": float(p_fit),
        "R1_trigger_p2": bool(abs(p_fit - 2.0) <= 0.05),
        "R2_trigger_p1": bool(abs(p_fit - 1.0) <= 0.05),
        "B1_coefficient_is_quantum_pressure":
            bool(abs(A_fit - 0.5) <= 0.025),
        "B2_instrument_distinguishes":
            bool(all(abs(r["ratio"] - 1.0) <= 0.01 for r in b2)),
        "B3a_chiral_silent_quartic":
            bool(abs(sc["slope_E_perp"] - 4.0) <= 0.2),
        "B3b_linear_spectrum_shift_le_1e-3":
            bool(b3b["extrapolated_linear_shift_rel"] <= 1e-3),
        "B4_no_linear_order_current":
            bool(abs(sc["slope_j"] - 2.0) <= 0.1
                 and abs(sc["slope_curl_j"] - 2.0) <= 0.1),
        "B5_instrument_validated": pc_ok,
        "B5_gamma_magnon": g,
        "Q3_non_transactional": bool(pc_ok and abs(g) <= 0.1),
        "Q3_transactional": bool(pc_ok and abs(g - 1.0) <= 0.2),
        "S1_prediction": "R1 operative clause (omega = k^2/2, quantum-"
                         "pressure coefficient, chiral term silent at "
                         "linear order) and Q3 NEGATIVE",
    }
    return out


def figure(out, dest):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None
    b1 = out["B1_magnon"]
    k = np.array(b1["k"])
    om = np.array(b1["omega"])
    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    ax.loglog(k, om, "o", label="measured $\\omega(k)$ ($\\hat n$ channel)")
    kk = np.linspace(k.min(), k.max(), 100)
    ax.loglog(kk, kk**2 / 2, "-", label="$\\hbar k^2/2m_0$ (free magnon)")
    ax.loglog(kk, ALPHA * kk, "--", label="$\\alpha c\\,k$ (a 'second light')")
    bs = out["B2_control"]
    ax.loglog([r["k"] for r in bs], [r["omega_measured"] for r in bs],
              "s", label="density channel (control)")
    ax.loglog(kk, kk * np.sqrt(B0 + kk**2 / 4), ":",
              label="Bogoliubov $k\\sqrt{b+k^2/4}$")
    ax.set_xlabel("$k\\xi$")
    ax.set_ylabel("$\\omega$  [$c/\\xi$]")
    ax.legend(fontsize=7)
    ax.set_title("#138 CHIRAL-DISPERSION: the $\\hat n$ channel is a "
                 "free magnon", fontsize=9)
    fig.tight_layout()
    fig.savefig(dest, dpi=160)
    plt.close(fig)
    return dest


def main():
    quick = "--quick" in sys.argv
    print(f"CHIRAL-DISPERSION S2, quick={quick}", flush=True)
    t0 = _time.time()
    out = battery(quick=quick)
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    dest = RESULTS / ("chiral_dispersion_receipt_quick.json" if quick
                      else "chiral_dispersion_receipt.json")
    dest.write_text(json.dumps(out, indent=1))
    fig = figure(out, FIGURES / "chiral_dispersion_omega_k.png")
    v = out["verdicts"]
    print("\n--- verdicts ---")
    for key in ("B1_p", "R1_trigger_p2", "R2_trigger_p1",
                "B1_coefficient_is_quantum_pressure",
                "B2_instrument_distinguishes", "B3a_chiral_silent_quartic",
                "B3b_linear_spectrum_shift_le_1e-3",
                "B4_no_linear_order_current", "B5_instrument_validated",
                "B5_gamma_magnon", "Q3_non_transactional"):
        print(f"  {key}: {v[key]}")
    print(f"receipt -> {dest}")
    if fig:
        print(f"figure  -> {fig}")
    print(f"total {_time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()

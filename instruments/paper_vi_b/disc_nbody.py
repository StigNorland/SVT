"""
SSV VI-b -- N-body galaxy disc with REAL gravity (issue #124)
=============================================================

A 2D-in-plane N-body stellar disc with genuine Newtonian self-gravity:
softened 1/r^2 forces computed by an FFT particle-mesh solver with ISOLATED
(zero-padded, Hockney--Eastwood) boundary conditions -- real gravity, not an
ansatz.  No central black hole (M33-like).  No dark-matter particles.

The only SSV ingredient is optional: the *measured* intrinsic circulation
halo of issue #119 (H7a/H8: a topological defect carries an isothermal
1/r^2 energy density, whose Poisson integral is the logarithmic potential)
applied as an external term

    Phi_halo = v_h^2 ln(r)      =>      a_halo = -v_h^2 / r  (inward).

Pre-registered decision rules (#124):
  D1 baryons-only: rotation curve declines beyond the disc;
  D2 + halo:       rotation curve flat at large r;
  D3 arms form WITHOUT a BH: m=2-4 Fourier amplitudes >= 10% within a few
     rotations at Q ~ 1.2-1.5 (swing amplification of the baryons);
  D4 pitch angle increases with Toomre Q.

Units: G = 1, M_disc = 1, R_d (exponential scale length) = 1.

Run:  python disc_nbody.py            (both configs, GPU via SSV_GPU=1)
"""

import os
import sys
import time as _time

import numpy as np

_GPU = os.environ.get("SSV_GPU", "") not in ("", "0", "false", "False")
if _GPU:
    import cupy as xp
    import cupyx

    def _to(a):
        return xp.asarray(a)

    def _host(a):
        return xp.asnumpy(a)

    def _scatter_add(arr, iy, ix, w):
        cupyx.scatter_add(arr, (iy, ix), w)
else:
    xp = np

    def _to(a):
        return a

    def _host(a):
        return np.asarray(a)

    def _scatter_add(arr, iy, ix, w):
        np.add.at(arr, (iy, ix), w)


def backend_name():
    return "cupy/GPU" if _GPU else "numpy/CPU"


# --------------------------------------------------------------------------
# particle-mesh gravity: softened 3D-Newtonian kernel, isolated BCs
# --------------------------------------------------------------------------
class PMGravity:
    """FFT particle-mesh on an Ng x Ng grid spanning [-L/2, L/2)^2 with
    zero-padding to 2Ng for isolated boundaries.  Potential kernel
    -G/sqrt(r^2 + eps^2) (a 3D point mass confined to the plane; eps plays
    the role of disc thickness)."""

    def __init__(self, Ng=512, L=16.0, eps=0.25, G=1.0):
        self.Ng, self.L, self.eps, self.G = Ng, L, eps, G
        self.h = L / Ng
        n2 = 2 * Ng
        # kernel on the padded grid, distances with periodic wrap of the pad
        ax = np.arange(n2) * self.h
        ax = np.minimum(ax, n2 * self.h - ax)
        XX, YY = np.meshgrid(ax, ax, indexing="ij")
        ker = -G / np.sqrt(XX * XX + YY * YY + eps * eps)
        self.ker_hat = _to(np.fft.rfft2(ker))
        self.n2 = n2

    def accel_grid(self, pos, mass):
        """CIC deposit -> FFT Poisson (isolated) -> central-difference
        forces; returns (gx, gy) grids and the density grid."""
        Ng, h, L = self.Ng, self.h, self.L
        gx_idx = (pos[:, 0] + L / 2.0) / h
        gy_idx = (pos[:, 1] + L / 2.0) / h
        i0 = xp.floor(gx_idx).astype(xp.int32)
        j0 = xp.floor(gy_idx).astype(xp.int32)
        fx = gx_idx - i0
        fy = gy_idx - j0
        ok = (i0 >= 0) & (i0 < Ng - 1) & (j0 >= 0) & (j0 < Ng - 1)
        i0c = xp.where(ok, i0, 0)
        j0c = xp.where(ok, j0, 0)
        w = xp.where(ok, mass, 0.0)
        dens = xp.zeros((Ng, Ng))
        _scatter_add(dens, i0c, j0c, w * (1 - fx) * (1 - fy))
        _scatter_add(dens, i0c + 1, j0c, w * fx * (1 - fy))
        _scatter_add(dens, i0c, j0c + 1, w * (1 - fx) * fy)
        _scatter_add(dens, i0c + 1, j0c + 1, w * fx * fy)
        dens = dens / (h * h)                      # surface density

        pad = xp.zeros((self.n2, self.n2))
        pad[:Ng, :Ng] = dens * h * h               # mass per cell
        phi = xp.fft.irfft2(xp.fft.rfft2(pad) * self.ker_hat,
                            s=(self.n2, self.n2))[:Ng, :Ng]
        gx = xp.zeros_like(phi)
        gy = xp.zeros_like(phi)
        gx[1:-1, :] = -(phi[2:, :] - phi[:-2, :]) / (2 * h)
        gy[:, 1:-1] = -(phi[:, 2:] - phi[:, :-2]) / (2 * h)
        return gx, gy, dens, (i0c, j0c, fx, fy, ok)

    def gather(self, grid, cic):
        i0, j0, fx, fy, ok = cic
        v = (grid[i0, j0] * (1 - fx) * (1 - fy)
             + grid[i0 + 1, j0] * fx * (1 - fy)
             + grid[i0, j0 + 1] * (1 - fx) * fy
             + grid[i0 + 1, j0 + 1] * fx * fy)
        return xp.where(ok, v, 0.0)


# --------------------------------------------------------------------------
# disc setup and evolution
# --------------------------------------------------------------------------
def make_disc(n_part=200_000, Rd=1.0, Rmax=6.0, Q=1.3, v_halo=0.0,
              seed=11, pm=None):
    """Exponential disc, velocities from the MEASURED total acceleration
    (self-gravity + halo), Toomre-Q-controlled radial dispersion."""
    rng = np.random.default_rng(seed)
    r = rng.gamma(2.0, Rd, n_part)                 # PDF ~ r exp(-r/Rd)
    r = np.where(r > Rmax, rng.uniform(0.2, Rmax, n_part), r)
    th = rng.uniform(0, 2 * np.pi, n_part)
    pos = np.stack([r * np.cos(th), r * np.sin(th)], axis=1)
    mass = np.full(n_part, 1.0 / n_part)

    pos_d = _to(pos)
    mass_d = _to(mass)
    gx, gy, dens, cic = pm.accel_grid(pos_d, mass_d)
    ax = pm.gather(gx, cic)
    ay = pm.gather(gy, cic)
    r_d = _to(r)
    th_d = _to(th)
    a_r = -(ax * xp.cos(th_d) + ay * xp.sin(th_d))   # inward positive
    a_r = a_r + (v_halo ** 2) / xp.maximum(r_d, 0.05)
    vc2 = xp.maximum(r_d * a_r, 1e-6)
    vc = xp.sqrt(vc2)

    # Toomre-Q dispersion: sigma_r = Q * 3.36 G Sigma / kappa,
    # kappa ~ sqrt(2) vc / r (flat-curve approximation)
    Sigma = _to(np.exp(-r / Rd) / (2 * np.pi * Rd * Rd))
    kappa = xp.sqrt(2.0) * vc / xp.maximum(r_d, 0.05)
    sig_r = Q * 3.36 * Sigma / xp.maximum(kappa, 1e-3)
    sig_r = xp.minimum(sig_r, 0.5 * vc)
    noise = _to(rng.standard_normal((n_part, 2)))
    vr = noise[:, 0] * sig_r
    vt = vc + noise[:, 1] * sig_r * 0.71

    vel = xp.stack([vr * xp.cos(th_d) - vt * xp.sin(th_d),
                    vr * xp.sin(th_d) + vt * xp.cos(th_d)], axis=1)
    return pos_d, vel, mass_d


def rotation_curve(pos, vel, nbins=24, rmax=6.0):
    """Mean tangential velocity in radial bins (host arrays)."""
    p = _host(pos)
    v = _host(vel)
    r = np.hypot(p[:, 0], p[:, 1])
    vt = (-v[:, 0] * p[:, 1] + v[:, 1] * p[:, 0]) / np.maximum(r, 1e-9)
    edges = np.linspace(0.25, rmax, nbins + 1)
    rc, vv = [], []
    for i in range(nbins):
        m = (r >= edges[i]) & (r < edges[i + 1])
        if m.sum() > 50:
            rc.append(0.5 * (edges[i] + edges[i + 1]))
            vv.append(vt[m].mean())
    return np.array(rc), np.array(vv)


def fourier_modes(pos, rlo=1.0, rhi=4.0, mmax=4):
    """Global m-mode amplitudes A_m/A_0 and the m=2 phase-vs-ln r pitch."""
    p = _host(pos)
    r = np.hypot(p[:, 0], p[:, 1])
    phi = np.arctan2(p[:, 1], p[:, 0])
    sel = (r > rlo) & (r < rhi)
    amps = {}
    for m in range(1, mmax + 1):
        amps[m] = float(np.abs(np.exp(1j * m * phi[sel]).mean()))
    # pitch from m=2 phase drift across ln r
    nb = 8
    edges = np.exp(np.linspace(np.log(rlo), np.log(rhi), nb + 1))
    ph, lr = [], []
    for i in range(nb):
        m = (r >= edges[i]) & (r < edges[i + 1])
        if m.sum() > 200:
            ph.append(np.angle(np.exp(2j * phi[m]).mean()))
            lr.append(np.log(0.5 * (edges[i] + edges[i + 1])))
    pitch = np.nan
    if len(ph) >= 4:
        ph = np.unwrap(np.array(ph))
        s = np.polyfit(np.array(lr), ph, 1)[0]
        if abs(s) > 1e-3:
            pitch = float(np.degrees(np.arctan(2.0 / abs(s))))
    return amps, pitch


def run_disc(v_halo=0.0, Q=1.3, n_part=200_000, Ng=512, L=16.0,
             t_end=40.0, dt=0.004, tag="run", report_at=(10.0, 20.0, 40.0)):
    pm = PMGravity(Ng=Ng, L=L)
    pos, vel, mass = make_disc(n_part=n_part, Q=Q, v_halo=v_halo, pm=pm)
    nsteps = int(round(t_end / dt))
    rep_steps = {int(round(t / dt)) for t in report_at}
    print(f"  [{tag}] v_halo={v_halo}, Q={Q}, N={n_part}, Ng={Ng}, "
          f"t_end={t_end} (~{t_end / 12.0:.1f} rotations at r=2)")
    t0 = _time.time()
    gx, gy, dens, cic = pm.accel_grid(pos, mass)
    for n in range(nsteps):
        ax = pm.gather(gx, cic)
        ay = pm.gather(gy, cic)
        r2 = pos[:, 0] ** 2 + pos[:, 1] ** 2
        rr = xp.sqrt(xp.maximum(r2, 0.0025))
        if v_halo > 0:
            ax = ax - (v_halo ** 2) * pos[:, 0] / (rr * rr)
            ay = ay - (v_halo ** 2) * pos[:, 1] / (rr * rr)
        vel[:, 0] += ax * dt
        vel[:, 1] += ay * dt
        pos += vel * dt
        gx, gy, dens, cic = pm.accel_grid(pos, mass)
        if (n + 1) in rep_steps:
            t = (n + 1) * dt
            rc, vv = rotation_curve(pos, vel)
            amps, pitch = fourier_modes(pos)
            inner = vv[(rc > 1.0) & (rc < 2.0)].mean()
            outer = vv[(rc > 4.0) & (rc < 5.5)].mean()
            ptxt = f"{pitch:.0f} deg" if np.isfinite(pitch) else "n/a"
            print(f"    t={t:5.1f}: v(1-2)={inner:.3f} v(4-5.5)={outer:.3f} "
                  f"ratio={outer / inner:.2f} | A1={amps[1]:.3f} "
                  f"A2={amps[2]:.3f} A3={amps[3]:.3f} A4={amps[4]:.3f} "
                  f"| pitch~{ptxt} [{_time.time() - t0:.0f}s]")
    # final snapshot for the figure
    return pos, vel, dens


def save_figure(runs, fname):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, len(runs), figsize=(6 * len(runs), 11))
    if len(runs) == 1:
        axes = axes.reshape(2, 1)
    for k, (tag, pos, vel) in enumerate(runs):
        p = _host(pos)
        axes[0, k].hexbin(p[:, 0], p[:, 1], gridsize=240, bins="log",
                          cmap="inferno", extent=(-6, 6, -6, 6))
        axes[0, k].set_title(tag)
        axes[0, k].set_aspect("equal")
        rc, vv = rotation_curve(pos, vel)
        axes[1, k].plot(rc, vv, "o-")
        axes[1, k].set_xlabel("r / Rd")
        axes[1, k].set_ylabel("v_c")
        axes[1, k].set_ylim(0, None)
        axes[1, k].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(fname, dpi=110)
    print(f"  figure -> {fname}")


def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    print(f"N-body galaxy disc with REAL gravity, backend {backend_name()}")
    print("FFT particle-mesh, isolated BCs, softened 1/r^2; no BH, no DM "
          "particles.\n")
    runs = []
    # D1: baryons only
    pos1, vel1, _ = run_disc(v_halo=0.0, tag="D1 baryons-only")
    runs.append(("baryons only (real gravity)", pos1, vel1))
    # D2/D3: + measured SSV circulation halo
    pos2, vel2, _ = run_disc(v_halo=0.65, tag="D2 +SSV halo")
    runs.append(("+ SSV circulation halo (ln r)", pos2, vel2))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "_logs")
    os.makedirs(out, exist_ok=True)
    save_figure(runs, os.path.join(out, "disc_nbody.png"))
    print("\nDISC COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

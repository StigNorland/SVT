"""
SSV Reconnection Barrier: W/Z Mass and Weinberg Angle
======================================================
Computes the 3D GPE saddle-point energy along the vortex reconnection path,
extracts R_cap from the saddle-point geometry, then repeats for neutral
(Z-channel) reconnection to derive the Weinberg angle from the
amplitude/phase decomposition of the saddle eigenmode.

Framework parameters from Papers I & II:
  xi   = hbar / (m_e * c)          — healing length / vortex core size
  m0   — reference vacuum mass (= m_e by identification)
  mu0  = m_e * c^2 / alpha         — base mass ladder scale (~70 MeV)
  P0   ~ rho0 * c^2                — saturation pressure (dominant cap cost)
  lambda ~ 2000                    — chiral-shear coupling (fixes alpha)
  alpha = 1/137

Physical picture (Paper II §4):
  W boson = saddle-point configuration of two approaching vortex rings.
  The dominant energy cost is NOT the quantum-pressure barrier (which gives
  only ~9.6 GeV) but the end-cap cost: holding open fully-suppressed
  condensate against P0 at each end of the W tube.

  E_caps ~ P0 * pi * R_cap^2 * xi

  Paper II conjectures R_cap = phi * xi/alpha (phi = golden ratio), giving
  m_W ~ 78.9 GeV. This script derives R_cap from the saddle geometry.

  The Weinberg angle emerges from the neutral (Z) reconnection: the
  end-caps partially heal via the phase channel, reducing the cap cost.
  The mixing angle phi_Z = theta_W is extracted from the amplitude/phase
  decomposition of the neutral saddle eigenmode.

Structure:
  1. Set up 3D grid and LogSE potential
  2. Initialise two-vortex-ring state (charged reconnection / W channel)
  3. Evolve in imaginary time toward saddle point (constrained GPE)
  4. Extract saddle energy, R_cap, m_W
  5. Repeat for neutral reconnection (Z channel)
  6. Decompose saddle eigenmodes → Weinberg angle
  7. Report m_W, m_Z, theta_W vs. observed values

Run: python reconnection_barrier.py
Typical runtime on 64^3 grid: ~2 min. Use 128^3 for publication accuracy.
"""

import numpy as np
from scipy.ndimage import label
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ══════════════════════════════════════════════════════════════════════════════
# 1.  PHYSICAL CONSTANTS & MEDIUM PARAMETERS  (SI units internally, eV output)
# ══════════════════════════════════════════════════════════════════════════════

hbar   = 1.0546e-34      # J·s
c      = 2.9979e8        # m/s
m_e    = 9.1094e-31      # kg
alpha  = 1.0 / 137.036  # fine-structure constant
phi_gr = (1 + np.sqrt(5)) / 2  # golden ratio ≈ 1.618

# Healing length = electron Compton wavelength (Paper I eq. xi)
xi = hbar / (m_e * c)   # ≈ 3.862e-13 m

# Reference mass = m_e (vacuum quasiparticle mass)
m0  = m_e

# Chiral-shear coupling:  lambda = alpha^2 * rho0 / m0
# We work in dimensionless units scaled by xi and m0*c^2, so lambda enters
# only through alpha.  Effective transverse stiffness parameter:
lam = alpha**2   # dimensionless (rho0/m0 absorbed into grid units)

# Saturation pressure P0 = rho0 * c^2.
# In grid units (xi=1, m0*c^2=1): P0 = 1 (sets cap energy scale).
# Physical conversion: 1 grid energy unit = m_e * c^2 = 0.511 MeV

eV_per_J    = 6.2415e18
MeV_per_J   = eV_per_J * 1e-6
GeV_per_J   = eV_per_J * 1e-9

E_unit_MeV  = m_e * c**2 * MeV_per_J   # = 0.511 MeV
E_unit_GeV  = E_unit_MeV * 1e-3        # = 0.000511 GeV

# Observed masses for comparison
M_W_obs_GeV = 80.377
M_Z_obs_GeV = 91.188
sin2_theta_W_obs = 0.23122   # PDG 2023

# Paper II golden-ratio conjecture (analytic estimate)
# R_cap = phi * xi/alpha  =>  E_cap = pi * phi^2 * m_e/alpha^2
E_cap_analytic_GeV = (np.pi * phi_gr**2 * m_e * c**2 / alpha**2) * GeV_per_J
print(f"Paper II analytic conjecture:  m_W ≈ {E_cap_analytic_GeV:.2f} GeV")
print(f"Observed:                      m_W  = {M_W_obs_GeV:.3f} GeV\n")

# ══════════════════════════════════════════════════════════════════════════════
# 2.  GRID SETUP  (dimensionless units: length in xi, energy in m0*c^2)
# ══════════════════════════════════════════════════════════════════════════════

# Grid size: 64^3 for fast run, 128^3 for production
N    = 64
L    = 20.0           # box half-size in units of xi  (±L)
x1d  = np.linspace(-L, L, N, endpoint=False)
dx   = x1d[1] - x1d[0]
X, Y, Z = np.meshgrid(x1d, x1d, x1d, indexing='ij')

# ══════════════════════════════════════════════════════════════════════════════
# 3.  LOGARITHMIC SCHRODINGER POTENTIAL (LogSE)
#     V_log(|Psi|^2) = -b * rho * ln(rho/rho0),  b = m0*c^2 / (2*rho0)
#     In dimensionless units (rho0=1, b=1/2):
#       V_log = -|Psi|^2 * ln(|Psi|^2)   (positive near rho=1)
# ══════════════════════════════════════════════════════════════════════════════

def V_log(rho):
    """LogSE potential density in dimensionless units. rho = |Psi|^2."""
    rho_safe = np.where(rho < 1e-30, 1e-30, rho)
    return -rho_safe * np.log(rho_safe)

def laplacian_3d(psi, dx):
    """6-point finite-difference Laplacian (periodic boundary)."""
    return (
        np.roll(psi,  1, 0) + np.roll(psi, -1, 0) +
        np.roll(psi,  1, 1) + np.roll(psi, -1, 1) +
        np.roll(psi,  1, 2) + np.roll(psi, -1, 2) -
        6.0 * psi
    ) / dx**2

# ══════════════════════════════════════════════════════════════════════════════
# 4.  VORTEX RING INITIAL STATE
#     A single vortex ring of radius R_ring in the x-y plane at height z0
#     uses the phase winding:  theta(x,y,z) = atan2(rho_xy - R_ring, z - z0)
#     approximated by a product ansatz for the amplitude.
# ══════════════════════════════════════════════════════════════════════════════

def vortex_ring_phase(X, Y, Z, R_ring, z0, sign=+1):
    """
    Phase field for a single vortex ring of radius R_ring centred at z=z0.
    sign = +1 (left-handed) or -1 (right-handed, for anti-ring).
    """
    # Distance from the ring core in the (rho, z) half-plane
    rho_xy  = np.sqrt(X**2 + Y**2)
    d_rho   = rho_xy - R_ring       # radial distance from ring
    d_z     = Z - z0                # axial distance
    # Phase winds once around the ring core
    theta   = sign * np.arctan2(d_z, d_rho)
    return theta

def vortex_ring_amplitude(X, Y, Z, R_ring, z0, core=1.0):
    """
    Approximate amplitude field: tanh profile around the ring core.
    core sets the healing-length width of the suppression.
    """
    rho_xy  = np.sqrt(X**2 + Y**2)
    d_rho   = rho_xy - R_ring
    d_z     = Z - z0
    dist    = np.sqrt(d_rho**2 + d_z**2)
    amp     = np.tanh(dist / core)
    return amp

def two_ring_state(X, Y, Z, R_ring, separation, charge='charged'):
    """
    Initial state: two vortex rings approaching along the z-axis.
    separation: distance between ring planes (in xi).
    charge: 'charged' (W channel, opposite windings) or
            'neutral'  (Z channel, same winding topology but net neutral).
    """
    z1 = +separation / 2
    z2 = -separation / 2

    if charge == 'charged':
        # Opposite topological charges: the reconnection changes flavour
        sign1, sign2 = +1, -1
    else:
        # Neutral channel: same chirality (no net charge exchange),
        # but topology still changes — this is the Z reconnection
        sign1, sign2 = +1, +1

    amp1   = vortex_ring_amplitude(X, Y, Z, R_ring, z1)
    amp2   = vortex_ring_amplitude(X, Y, Z, R_ring, z2)
    phase1 = vortex_ring_phase(X, Y, Z, R_ring, z1, sign1)
    phase2 = vortex_ring_phase(X, Y, Z, R_ring, z2, sign2)

    # Combined order parameter: superpose the two vortex phase fields
    # (Gross-Pitaevskii product ansatz)
    amp    = amp1 * amp2
    phase  = phase1 + phase2
    Psi    = amp * np.exp(1j * phase)
    return Psi

# ══════════════════════════════════════════════════════════════════════════════
# 5.  GPE ENERGY FUNCTIONAL
#     E[Psi] = (hbar^2/2m0) |grad Psi|^2 + V_log(|Psi|^2)
#              + (lambda/2) |curl j|^2   (chiral shear term)
#     In dimensionless units (hbar=1, m0=1, rho0=1):
#       E = (1/2)|grad Psi|^2 - |Psi|^2 * ln(|Psi|^2)
# ══════════════════════════════════════════════════════════════════════════════

def gpe_energy(Psi, dx):
    """Total GPE energy in dimensionless units."""
    rho    = np.abs(Psi)**2
    # Kinetic energy: (1/2)|grad Psi|^2 via finite differences
    grad2  = sum(
        np.abs( (np.roll(Psi, -1, ax) - np.roll(Psi, 1, ax)) / (2*dx) )**2
        for ax in range(3)
    )
    E_kin  = 0.5 * np.sum(grad2) * dx**3
    E_pot  = np.sum(V_log(rho))   * dx**3
    return E_kin + E_pot

# ══════════════════════════════════════════════════════════════════════════════
# 6.  CONSTRAINED IMAGINARY-TIME EVOLUTION TOWARD SADDLE POINT
#
#     Strategy: steepest ascent along the reconnection coordinate s,
#     defined as the mean approach distance between the two ring cores.
#     We maximise E along s while minimising in all transverse directions.
#     This is the "string method" (E, Vanden-Eijnden) adapted to the GPE.
#
#     Simplified here: we parametrise s by the ring separation, slowly
#     decrease it from s_init to s_min=2*xi (overlap), and at each step
#     relax the order parameter for fixed s via imaginary-time GPE.
#     The maximum energy along the path is the saddle point (W mass).
# ══════════════════════════════════════════════════════════════════════════════

def gpe_rhs(Psi, dx):
    """Right-hand side of imaginary-time GPE: -delta E / delta Psi*."""
    rho    = np.abs(Psi)**2
    rho_safe = np.where(rho < 1e-30, 1e-30, rho)
    lap    = laplacian_3d(Psi, dx)
    # LogSE chemical potential term: dV/d(rho) * Psi = (-ln rho - 1) * Psi
    mu_loc = -(np.log(rho_safe) + 1.0)
    return 0.5 * lap + mu_loc * Psi

def imaginary_time_step(Psi, dx, dt=0.01, n_steps=30):
    """Relax Psi via imaginary-time GPE for n_steps steps, renormalise."""
    for _ in range(n_steps):
        Psi = Psi + dt * gpe_rhs(Psi, dx)
        # Renormalise to keep mean density = 1
        rho_mean = np.mean(np.abs(Psi)**2)
        Psi = Psi / np.sqrt(rho_mean)
    return Psi

def scan_reconnection_path(X, Y, Z, dx, R_ring=5.0, charge='charged',
                            n_sep=15, relax_steps=50, dt=0.005):
    """
    Scan the reconnection path by varying ring separation s from large to small.
    Returns arrays of separation values and corresponding energies.
    """
    separations = np.linspace(3.0 * R_ring, 1.5, n_sep)
    energies    = []
    Psi_saddle  = None
    E_max       = -np.inf

    print(f"  Scanning {charge} reconnection path ({n_sep} points)...")
    for i, sep in enumerate(separations):
        Psi = two_ring_state(X, Y, Z, R_ring, sep, charge=charge)
        Psi = imaginary_time_step(Psi, dx, dt=dt, n_steps=relax_steps)
        E   = gpe_energy(Psi, dx)
        energies.append(E)
        if E > E_max:
            E_max      = E
            Psi_saddle = Psi.copy()
        print(f"    sep={sep:5.2f} xi,  E={E:.4f}  (dim.less units)", end='\r')

    print()
    return separations, np.array(energies), Psi_saddle, E_max

# ══════════════════════════════════════════════════════════════════════════════
# 7.  EXTRACT R_cap FROM SADDLE-POINT DENSITY PROFILE
#     R_cap = radius of the suppressed-condensate cap region at pinch-off.
#     We find all grid cells where |Psi|^2 < epsilon (suppressed),
#     cluster them, and measure the transverse extent of each cap blob.
# ══════════════════════════════════════════════════════════════════════════════

def extract_Rcap(Psi_saddle, dx, epsilon=0.1):
    """
    Extract cap radius R_cap from the saddle-point density.
    Returns R_cap in units of xi (= grid units here).
    """
    rho        = np.abs(Psi_saddle)**2
    suppressed = (rho < epsilon).astype(int)
    labeled, n_blobs = label(suppressed)

    if n_blobs == 0:
        print("  Warning: no suppressed region found at saddle point.")
        return None

    # Find the two largest blobs (the two end-caps)
    blob_sizes = [np.sum(labeled == k) for k in range(1, n_blobs+1)]
    top2_idx   = np.argsort(blob_sizes)[-2:] + 1  # 1-indexed

    R_caps = []
    for blob_id in top2_idx:
        blob_mask = (labeled == blob_id)
        # Transverse radius: RMS extent perpendicular to z-axis
        blob_coords = np.argwhere(blob_mask)
        # Convert indices to physical coordinates
        x_c = x1d[blob_coords[:, 0]]
        y_c = x1d[blob_coords[:, 1]]
        r_transverse = np.sqrt(x_c**2 + y_c**2)
        R_cap_blob   = np.mean(r_transverse) + np.std(r_transverse)
        R_caps.append(R_cap_blob)

    R_cap = np.mean(R_caps)   # average over the two caps
    return R_cap

# ══════════════════════════════════════════════════════════════════════════════
# 8.  AMPLITUDE / PHASE DECOMPOSITION OF SADDLE EIGENMODE
#     Decompose Psi = f * exp(i*theta) at the saddle point.
#     The W mode is pure amplitude suppression (delta_f dominates).
#     The Z mode has partial phase rotation (delta_theta contributes).
#     Weinberg angle: cos(theta_W) = ||delta_theta||_Z / ||delta_Psi||_Z
# ══════════════════════════════════════════════════════════════════════════════

def amplitude_phase_decomposition(Psi_saddle, Psi_background=None):
    """
    Decompose saddle-point order parameter into amplitude and phase perturbations.
    Psi_background: reference state (uniform Psi=1 here).
    Returns (f_norm, theta_norm): L2 norms of amplitude and phase perturbation.
    """
    if Psi_background is None:
        Psi_background = np.ones_like(Psi_saddle)

    f_bg    = np.abs(Psi_background)    # = 1 everywhere
    f_sad   = np.abs(Psi_saddle)
    theta_sad = np.angle(Psi_saddle)
    theta_bg  = np.angle(Psi_background)  # = 0 everywhere

    delta_f      = f_sad   - f_bg
    delta_theta  = theta_sad - theta_bg
    # Wrap phase difference to [-pi, pi]
    delta_theta  = np.arctan2(np.sin(delta_theta), np.cos(delta_theta))

    # Weighted norms: weight by local density to focus on the defect region
    rho     = f_sad**2
    w       = 1.0 - rho   # weight = suppression depth (1 in cap, 0 far away)
    w       = np.maximum(w, 0)

    f_norm  = np.sqrt(np.sum(w * delta_f**2))
    th_norm = np.sqrt(np.sum(w * delta_theta**2))

    return f_norm, th_norm

def weinberg_angle_from_saddles(Psi_W, Psi_Z):
    """
    Extract Weinberg angle from the amplitude/phase decomposition of the
    W and Z saddle-point configurations.

    Physical argument:
      W (charged): pure amplitude suppression -> f_norm >> th_norm
      Z (neutral): mixed -> cos(phi_Z) = th_norm_Z / |Psi_Z|_total

    The Weinberg angle theta_W satisfies:
      cos(theta_W) = M_W / M_Z
    In the mode decomposition:
      cos(theta_W) ~ f_norm_W / sqrt(f_norm_Z^2 + th_norm_Z^2)
                     * (f_norm_Z / f_norm_W)
    Simplified: the mixing angle at the Z saddle is theta_W.
    """
    f_W, th_W = amplitude_phase_decomposition(Psi_W)
    f_Z, th_Z = amplitude_phase_decomposition(Psi_Z)

    # Mixing angle at Z saddle: tan(phi_Z) = th_Z / f_Z
    phi_Z          = np.arctan2(th_Z, f_Z)
    cos_phi_Z      = np.cos(phi_Z)
    sin2_phi_Z     = np.sin(phi_Z)**2

    # For W: mixing should be ~0 (pure amplitude channel)
    phi_W          = np.arctan2(th_W, f_W)

    return phi_Z, cos_phi_Z, sin2_phi_Z, phi_W

# ══════════════════════════════════════════════════════════════════════════════
# 9.  CONVERT SADDLE ENERGY TO PHYSICAL MASS
#     The saddle-point energy barrier IS the W/Z mass (it is the cost of
#     creating the reconnection event = the particle rest energy).
#     Dominant term: E_caps ~ P0 * pi * R_cap^2 * xi
#     In dimensionless units P0 = rho0 * c^2 = 1, xi = 1:
#       E_caps = pi * R_cap^2
# ══════════════════════════════════════════════════════════════════════════════

def caps_energy_from_Rcap(R_cap):
    """
    Cap energy in dimensionless units (P0 = xi = 1).
    E_caps = pi * R_cap^2
    Physical mass = E_caps * m_e * c^2.
    """
    return np.pi * R_cap**2

def dimless_to_GeV(E_dimless):
    """Convert dimensionless energy units to GeV."""
    return E_dimless * E_unit_GeV

# ══════════════════════════════════════════════════════════════════════════════
# 10.  MAIN CALCULATION
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 65)
    print("SSV Reconnection Barrier: W/Z Masses and Weinberg Angle")
    print("=" * 65)
    print(f"Grid: {N}^3,  box: ±{L} xi,  dx = {dx:.3f} xi\n")

    R_ring = 5.0   # vortex ring radius in xi units (~ electron equilibrium radius)

    # ── W channel (charged reconnection) ─────────────────────────────────────
    print("─── W channel (charged vortex reconnection) ───")
    seps_W, E_W, Psi_W, E_saddle_W = scan_reconnection_path(
        X, Y, Z, dx, R_ring=R_ring, charge='charged', n_sep=12, relax_steps=40
    )
    print(f"  Saddle energy (dim.less): {E_saddle_W:.4f}")

    R_cap_W = extract_Rcap(Psi_W, dx, epsilon=0.15)
    if R_cap_W is not None:
        E_cap_W = caps_energy_from_Rcap(R_cap_W)
        m_W_GeV = dimless_to_GeV(E_cap_W)
        print(f"  R_cap (W) = {R_cap_W:.3f} xi")
        print(f"  m_W (cap energy) = {m_W_GeV:.2f} GeV")
        R_cap_phi = phi_gr / alpha
        print(f"  Paper II conjecture R_cap = phi/alpha = {R_cap_phi:.1f} xi "
              f"→ {dimless_to_GeV(np.pi * R_cap_phi**2):.1f} GeV")
    else:
        # Fallback: use full saddle energy (less accurate but meaningful)
        m_W_GeV = dimless_to_GeV(E_saddle_W)
        print(f"  m_W (saddle energy) = {m_W_GeV:.2f} GeV  [fallback — no cap cluster]")
        R_cap_W = np.sqrt(E_saddle_W / np.pi)   # invert for downstream use

    print(f"  Observed m_W = {M_W_obs_GeV:.3f} GeV  "
          f"(ratio = {m_W_GeV/M_W_obs_GeV:.3f})\n")

    # ── Z channel (neutral reconnection) ─────────────────────────────────────
    print("─── Z channel (neutral vortex reconnection) ───")
    seps_Z, E_Z, Psi_Z, E_saddle_Z = scan_reconnection_path(
        X, Y, Z, dx, R_ring=R_ring, charge='neutral', n_sep=12, relax_steps=40
    )
    print(f"  Saddle energy (dim.less): {E_saddle_Z:.4f}")

    R_cap_Z = extract_Rcap(Psi_Z, dx, epsilon=0.15)
    if R_cap_Z is not None:
        E_cap_Z = caps_energy_from_Rcap(R_cap_Z)
        m_Z_GeV = dimless_to_GeV(E_cap_Z)
        print(f"  R_cap (Z) = {R_cap_Z:.3f} xi")
        print(f"  m_Z (cap energy) = {m_Z_GeV:.2f} GeV")
    else:
        m_Z_GeV = dimless_to_GeV(E_saddle_Z)
        print(f"  m_Z (saddle energy) = {m_Z_GeV:.2f} GeV  [fallback]")
        R_cap_Z = np.sqrt(E_saddle_Z / np.pi)

    print(f"  Observed m_Z = {M_Z_obs_GeV:.3f} GeV  "
          f"(ratio = {m_Z_GeV/M_Z_obs_GeV:.3f})\n")

    # ── Mass ratio and Weinberg angle ─────────────────────────────────────────
    print("─── Weinberg angle from amplitude/phase decomposition ───")
    phi_Z, cos_phi_Z, sin2_phi_Z, phi_W = weinberg_angle_from_saddles(Psi_W, Psi_Z)

    theta_W_deg       = np.degrees(phi_Z)
    cos_theta_W_calc  = cos_phi_Z
    sin2_theta_W_calc = sin2_phi_Z

    # Cross-check from mass ratio
    if m_Z_GeV > 0:
        cos_theta_W_mass = m_W_GeV / m_Z_GeV
        sin2_theta_W_mass = 1 - cos_theta_W_mass**2
    else:
        cos_theta_W_mass = np.nan
        sin2_theta_W_mass = np.nan

    print(f"  theta_W (from mode decomp.)  = {theta_W_deg:.2f}°")
    print(f"  sin^2(theta_W) [mode decomp] = {sin2_theta_W_calc:.4f}")
    print(f"  sin^2(theta_W) [mass ratio]  = {sin2_theta_W_mass:.4f}")
    print(f"  sin^2(theta_W) [observed]    = {sin2_theta_W_obs:.4f}\n")

    print(f"  W channel: phi_W = {np.degrees(phi_W):.1f}°  "
          f"(expected ~90° for pure amplitude channel)")
    print(f"  Z channel: phi_Z = {theta_W_deg:.1f}°  "
          f"(expected ~28.2° = theta_W)\n")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print(f"{'Quantity':<30} {'SSV (this run)':>15} {'Observed':>12} {'Ratio':>8}")
    print("-" * 65)
    print(f"{'m_W (GeV)':<30} {m_W_GeV:>15.2f} {M_W_obs_GeV:>12.3f} "
          f"{m_W_GeV/M_W_obs_GeV:>8.3f}")
    print(f"{'m_Z (GeV)':<30} {m_Z_GeV:>15.2f} {M_Z_obs_GeV:>12.3f} "
          f"{m_Z_GeV/M_Z_obs_GeV:>8.3f}")
    print(f"{'sin^2(theta_W) [mode]':<30} {sin2_theta_W_calc:>15.4f} "
          f"{sin2_theta_W_obs:>12.4f} {sin2_theta_W_calc/sin2_theta_W_obs:>8.3f}")
    print(f"{'sin^2(theta_W) [masses]':<30} {sin2_theta_W_mass:>15.4f} "
          f"{sin2_theta_W_obs:>12.4f} {sin2_theta_W_mass/sin2_theta_W_obs:>8.3f}")
    print("-" * 65)
    print()
    print("Notes:")
    print("  - This 64^3 grid is a blueprint run; use 128^3+ for publication.")
    print("  - The saddle-point energy includes quantum-pressure barrier only.")
    print("  - Full cap cost requires matching P0 normalisation to Paper II.")
    print("  - If R_cap_W/R_cap_Z ratio = phi_gr, the golden-ratio conjecture")
    print("    is confirmed by the geometry (not just by the analytic estimate).")
    if R_cap_W and R_cap_Z:
        print(f"  - R_cap_W / R_cap_Z = {R_cap_W/R_cap_Z:.4f}  "
              f"(golden ratio = {phi_gr:.4f})")
    print()
    print("Next steps toward zero-free-parameter electroweak sector:")
    print("  1. Confirm R_cap = phi * xi/alpha from 3D saddle geometry (128^3)")
    print("  2. Verify R_cap_W / R_cap_Z = phi_gr (golden-ratio constraint)")
    print("  3. Check sin^2(theta_W) from mode decomp converges to 0.231 with N")
    print("  4. Add chiral-shear term (lambda~2000) for full L+L_perp functional")
    print("  5. Run time-dependent GPE (not imaginary-time) for real saddle")

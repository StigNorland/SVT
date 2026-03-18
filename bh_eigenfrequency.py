"""
Topological Geometrodynamics - Central Black Hole Eigenfrequency Calculator
Computes the natural resonance frequency f_BH ∝ 1/M and wiggle spacing Δr ∝ 1/M_BH
for any galaxy. Anchored to proton Compton frequency.

Run: python bh_eigenfrequency.py
"""

import numpy as np

# ================== CONSTANTS (from the framework) ==================
f_proton = 2.27e23          # Hz  (proton Compton frequency)
M_proton_kg = 1.6726e-27    # kg
M_sun_kg = 1.989e30         # kg

# Calibration for wiggle spacing (Δr in kpc)
# For Andromeda (M_BH ≈ 1.4e8 Msun) typical observed spacing ~10-15 kpc
CALIB_CONSTANT = 1.8e9      # kpc * Msun  (tuned so M31 gives ~12.9 kpc)

def bh_eigenfrequency(M_BH_solar):
    """Compute eigenfrequency f_BH and wiggle spacing Δr for given M_BH in solar masses"""
    M_BH_kg = M_BH_solar * M_sun_kg
    f_BH = f_proton * (M_proton_kg / M_BH_kg)
    
    # Period in years (for intuition)
    T_years = 1 / (f_BH * 3.156e7)   # seconds per year
    
    # Expected wiggle spacing Δr ∝ 1/M_BH
    delta_r_kpc = CALIB_CONSTANT / M_BH_solar
    
    return f_BH, T_years, delta_r_kpc


# ====================== EXAMPLE: ANDROMEDA ======================
if __name__ == "__main__":
    print("Topological Geometrodynamics - BH Eigenfrequency Calculator\n")
    
    M_BH = 1.4e8                    # Andromeda central BH mass (solar masses)
    f, T, dr = bh_eigenfrequency(M_BH)
    
    print(f"Galaxy: Andromeda (M_BH = {M_BH:.1e} M☉)")
    print(f"Eigenfrequency f_BH     = {f:.3e} Hz")
    print(f"Fundamental period      = {T:.3e} years")
    print(f"Expected wiggle spacing = {dr:.1f} kpc\n")
    
    # Quick demo for a range of BH masses
    masses = np.logspace(6, 10, 5)
    print("M_BH (M☉)     f_BH (Hz)          Δr (kpc)")
    print("-" * 45)
    for m in masses:
        f, _, dr = bh_eigenfrequency(m)
        print(f"{m:10.1e}   {f:.3e}      {dr:6.1f}")
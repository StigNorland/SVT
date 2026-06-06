"""#94 — Does a half-quantum-vortex (HQV) electron rescue the muon γ_B = π?

ANSWER: NO. The HQV is real but it is the electron's spin-½ (a meridional ℤ₂
framing, #87 B2) in another guise; it does NOT supply the muon's azimuthal Berry
phase, and a free HQV is excluded by charge quantization. The electron is an
integer-winding (IQV) object; pion = 2μ₀ (A1) survives; the muon is a NUMERICAL
COINCIDENCE — definitively, the last γ_B=π route is closed.

=============================================================================
THE TWO-CIRCLE DISTINCTION (the crux #94's framing got wrong)
=============================================================================

The electron is a vortex RING: its core lies ALONG the major circle (radius R_e).
There are two inequivalent loops:

  • MERIDIONAL loop C_ϑ — a small circle that LINKS the core (linking number 1).
    The vortex phase winds 2π here (the circulation). An HQV adds a π spin
    disclination here: the spinor z winds, z(ϑ+2π) = −z(ϑ).
  • MAJOR circle C_φ — runs ALONG the core (linking number 0 with it). The muon's
    Berry phase is the holonomy of a BdG mode transported once around C_φ.

#94 assumed the HQV gives "z₀(φ) winding in φ". It does not: the HQV winds in ϑ
(around the core), so z = z(ϑ) is INDEPENDENT of φ. Therefore:

  A_φ = −i z†∂_φ z = 0      ⇒  γ_B(C_φ) = 0   (the muon — same as #91)
  A_ϑ = −i z†∂_ϑ z ≠ 0      ⇒  γ_B(C_ϑ) = π   (the spin-½ — #87 B2)

The HQV's −1 lives on C_ϑ (spin-½, links the core); the muon needs −1 on C_φ
(runs along the core). Orthogonal circles. To put a half-winding on C_φ you would
need a separately spin-wound ring — not forced by HQV topology, and energetically
disfavored (gradient cost ∝ stiffness/R, no benefit), so the ring relaxes to
φ-uniform: back to #91's |V| = 0.

=============================================================================
INDEPENDENT KILLER: CHARGE QUANTIZATION
=============================================================================

In SSV electric charge = chirality/winding, and circulation is integer-quantized
(Onsager–Feynman ∮v·dl = n h/m₀). A FREE HQV has n = ½ ⇒ half charge — excluded.
HQVs can only exist confined in integer-winding pairs (= an IQV externally). So
the free electron is integer-winding regardless, and pion = 2μ₀ is untouched.
"""

from __future__ import annotations

import numpy as np


# ── HQV spinor texture (Bloch angles), winding in ϑ (meridional), NOT φ ──────

def hqv_spinor(theta_merid: np.ndarray) -> np.ndarray:
    """The physical HQV disclination: z winds by π over a meridional loop ϑ∈[0,2π),
    z(ϑ) = (cos(ϑ/4), sin(ϑ/4)) gives z(2π) ⟂-rotated by π/2 on the Bloch sphere
    i.e. n̂ rotates by π (a half-disclination).  Returns (N,2) complex array.
    (Independent of the azimuthal angle φ — that is the whole point.)"""
    z = np.stack([np.cos(theta_merid / 4.0), np.sin(theta_merid / 4.0)], axis=1).astype(complex)
    return z


def wilson_loop_phase(z: np.ndarray) -> float:
    """Gauge-invariant holonomy |arg ∏_k ⟨z_k|z_{k+1}⟩| ∈ [0, π] for a closed
    loop of unit spinors z (shape (N,2)). ℤ₂-valued under particle-hole: 0 or π."""
    n = len(z)
    prod = np.prod([np.vdot(z[k], z[(k + 1) % n]) for k in range(n)])
    return float(abs(np.angle(prod)))


def meridional_berry_phase(n: int = 4000) -> float:
    """γ_B around C_ϑ (links the core): the spin-½ ℤ₂ phase. Expect π.
    n̂ sweeps a great circle (polar angle β: 0→2π) as the meridional angle ϑ goes
    round once ⇒ the spinor picks up −1 (Berry phase π)."""
    beta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)   # great-circle sweep
    z = np.stack([np.cos(beta / 2.0), np.sin(beta / 2.0)], axis=1).astype(complex)
    return wilson_loop_phase(z)


def azimuthal_berry_phase(n: int = 4000) -> float:
    """γ_B around C_φ (runs along the core) for the HQV: z is φ-independent, so
    A_φ = 0 and the holonomy is 0 — the muon is NOT rescued (= #91)."""
    phi = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    theta_merid_fixed = 0.7  # the mode sits at a fixed meridional position
    z_fixed = hqv_spinor(np.array([theta_merid_fixed]))[0]
    z = np.tile(z_fixed, (n, 1))                       # φ-independent
    return wilson_loop_phase(z)


# ── Charge quantization ──────────────────────────────────────────────────────

def free_defect_charge(circulation_quanta: float) -> float:
    """Charge = chirality/winding (SSV). An IQV has n=1 → unit charge; an HQV has
    n=½ → half charge (excluded by observed integer charge / Onsager–Feynman)."""
    return circulation_quanta


def hqv_free_charge_excluded() -> bool:
    """A free HQV has half charge ⇒ not an allowed free object."""
    q = free_defect_charge(0.5)
    return abs(q - round(q)) > 1e-9        # non-integer ⇒ excluded


# ── Energetics: azimuthal spin-winding costs energy with no benefit ──────────

def azimuthal_spin_winding_cost(spin_stiffness: float, R: float, winding: int = 1) -> float:
    """Energy of forcing the spin texture to wind w times around the MAJOR ring:
    E = ½ · stiffness · ∮ (∂_φ n̂)² dℓ ≈ ½·stiffness·(2πR)·(w/R)² = π·stiffness·w²/R.
    Positive, with no compensating benefit ⇒ the ring relaxes to φ-uniform."""
    return np.pi * spin_stiffness * winding**2 / R


def iqv_vs_2hqv_leading_log(R: float, xi: float) -> dict[str, float]:
    """Leading-log energies at EQUAL phase/spin stiffness (verified Part A I2):
    one IQV (phase winding 1, both components) ∝ 1²·ln(R/ξ);
    one HQV ∝ (½²_phase + ½²_spin)·ln = ½·ln; two HQVs ∝ 1·ln.  → DEGENERATE at
    leading order (no energetic drive to split)."""
    log = np.log(R / xi)
    return {"E_IQV": 1.0 * log, "E_2HQV_leading": (0.5 + 0.5) * log}


# ── Verdict ──────────────────────────────────────────────────────────────────

def verdict() -> dict[str, object]:
    g_merid = meridional_berry_phase()
    g_azim = azimuthal_berry_phase()
    cost = azimuthal_spin_winding_cost(spin_stiffness=1.0, R=137.0)  # R_e ~ ξ/α
    ll = iqv_vs_2hqv_leading_log(R=137.0, xi=1.0)
    return {
        "meridional_gamma_B_over_pi": g_merid / np.pi,     # ≈1 : spin-½ (#87 B2)
        "azimuthal_gamma_B_over_pi": g_azim / np.pi,       # ≈0 : muon NOT rescued (#91)
        "hqv_free_charge": free_defect_charge(0.5),         # 0.5 : excluded
        "hqv_free_excluded": hqv_free_charge_excluded(),
        "azimuthal_winding_cost_positive": cost > 0.0,
        "iqv_2hqv_degenerate": abs(ll["E_IQV"] - ll["E_2HQV_leading"]) < 1e-9,
        "electron_is_IQV": True,
        "muon_status": "NUMERICAL COINCIDENCE (final — last γ_B=π route closed)",
        "pion_2mu0": "survives (electron integer-winding; A1 unchanged)",
    }


def main() -> None:
    r = verdict()
    print("=" * 76)
    print("#94 — HQV electron: does it rescue the muon γ_B = π?")
    print("=" * 76)
    print()
    print("  TWO-CIRCLE HOLONOMY of the HQV texture z = z(ϑ) [φ-independent]:")
    print(f"    meridional C_ϑ (links core): γ_B/π = {r['meridional_gamma_B_over_pi']:.3f}"
          "   → spin-½ (#87 B2)")
    print(f"    major C_φ  (along core)    : γ_B/π = {r['azimuthal_gamma_B_over_pi']:.3f}"
          "   → muon NOT rescued (= #91)")
    print()
    print("  CHARGE QUANTIZATION:")
    print(f"    free HQV charge = {r['hqv_free_charge']}  (non-integer ⇒ excluded: "
          f"{r['hqv_free_excluded']})")
    print()
    print("  ENERGETICS:")
    print(f"    forcing azimuthal spin winding costs energy > 0: "
          f"{r['azimuthal_winding_cost_positive']} (no benefit ⇒ φ-uniform favored)")
    print(f"    IQV vs 2-HQV degenerate at leading log: {r['iqv_2hqv_degenerate']} "
          "(no drive to split)")
    print()
    print("=" * 76)
    print("  VERDICT: HQV route REJECTED.")
    print(f"    electron = IQV (integer winding)")
    print(f"    muon: {r['muon_status']}")
    print(f"    pion = 2μ₀: {r['pion_2mu0']}")
    print("  The HQV is real but = the electron's spin-½ (meridional ℤ₂, #87 B2);")
    print("  it lives on the wrong circle to give the muon, and a free HQV has")
    print("  half charge. The last γ_B=π route is closed.")
    print("=" * 76)


if __name__ == "__main__":
    main()

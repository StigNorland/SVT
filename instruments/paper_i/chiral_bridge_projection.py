from __future__ import annotations

import argparse
import math
from typing import Callable

from kelvin_augmented_bdg import AzimuthalMode, build_modes
from restricted_bdg_matrix import build_background
from toroidal_projection_integrals import ProjectionConfig


ComplexField = Callable[[float, float], complex]


def central_gradient(field: ComplexField, r: float, z: float, h: float) -> tuple[complex, complex]:
    return (
        (field(r + h, z) - field(r - h, z)) / (2.0 * h),
        (field(r, z + h) - field(r, z - h)) / (2.0 * h),
    )


def current_variation_m(bg, mode: AzimuthalMode, r: float, z: float, cfg: ProjectionConfig) -> tuple[complex, complex, complex]:
    psi = bg.psi0(r, z)
    phi = mode.field(r, z)
    grad_psi = central_gradient(bg.psi0, r, z, cfg.dr)
    grad_phi = central_gradient(mode.field, r, z, cfg.dr)

    # For a mode phi(r,z)e^{im varphi} on an axisymmetric background.
    dphi_dvarphi = 1j * mode.m_phi * phi
    prefactor = 1.0 / (2.0j)
    j_r = prefactor * (
        phi.conjugate() * grad_psi[0]
        + psi.conjugate() * grad_phi[0]
        - phi * grad_psi[0].conjugate()
        - psi * grad_phi[0].conjugate()
    )
    j_z = prefactor * (
        phi.conjugate() * grad_psi[1]
        + psi.conjugate() * grad_phi[1]
        - phi * grad_psi[1].conjugate()
        - psi * grad_phi[1].conjugate()
    )
    j_phi = prefactor * (psi.conjugate() * dphi_dvarphi - psi * dphi_dvarphi.conjugate()) / max(r, 1.0e-12)
    return j_r, j_phi, j_z


def curl_current_m(bg, mode: AzimuthalMode, r: float, z: float, cfg: ProjectionConfig) -> tuple[complex, complex, complex]:
    h = cfg.dr

    def jr(rr: float, zz: float) -> complex:
        return current_variation_m(bg, mode, rr, zz, cfg)[0]

    def jphi(rr: float, zz: float) -> complex:
        return current_variation_m(bg, mode, rr, zz, cfg)[1]

    def jz(rr: float, zz: float) -> complex:
        return current_variation_m(bg, mode, rr, zz, cfg)[2]

    j_r, j_phi, _ = current_variation_m(bg, mode, r, z, cfg)
    d_jphi_dz = (jphi(r, z + h) - jphi(r, z - h)) / (2.0 * h)
    d_jz_dvarphi = 1j * mode.m_phi * jz(r, z)
    curl_r = (d_jz_dvarphi - r * d_jphi_dz) / max(r, 1.0e-12)

    d_jr_dz = (jr(r, z + h) - jr(r, z - h)) / (2.0 * h)
    d_jz_dr = (jz(r + h, z) - jz(r - h, z)) / (2.0 * h)
    curl_phi = d_jr_dz - d_jz_dr

    d_rjphi_dr = ((r + h) * jphi(r + h, z) - (r - h) * jphi(r - h, z)) / (2.0 * h)
    d_jr_dvarphi = 1j * mode.m_phi * j_r
    curl_z = (d_rjphi_dr - d_jr_dvarphi) / max(r, 1.0e-12)
    return curl_r, curl_phi, curl_z


def chiral_overlap(bg, a: AzimuthalMode, b: AzimuthalMode, cfg: ProjectionConfig) -> complex:
    # The chiral energy density is phi-independent only when m_a == m_b.
    # The bridge we seek is the angular-momentum-changing part; here we compute
    # the raw local overlap without enforcing delta_m, to estimate its natural scale.
    total = 0.0j
    r_min = bg.r_e - cfg.half_width
    z_min = -cfg.half_width
    for i in range(cfg.n):
        r = r_min + (i + 0.5) * cfg.dr
        if r <= 0.0:
            continue
        for j in range(cfg.n):
            z = z_min + (j + 0.5) * cfg.dz
            ca = curl_current_m(bg, a, r, z, cfg)
            cb = curl_current_m(bg, b, r, z, cfg)
            dot = ca[0].conjugate() * cb[0] + ca[1].conjugate() * cb[1] + ca[2].conjugate() * cb[2]
            weight = 2.0 * math.pi * r * cfg.dr * cfg.dz
            total += weight * dot
    return total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project chiral current-curl overlaps between core and Kelvin modes.")
    parser.add_argument("--n", type=int, default=21)
    parser.add_argument("--half-width", type=float, default=4.0)
    parser.add_argument("--profile-n", type=int, default=800)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = ProjectionConfig(
        n=args.n,
        half_width=args.half_width,
        profile="numerical",
        profile_n=args.profile_n,
        chi_parity="sin",
    )
    bg = build_background(cfg.profile, cfg.profile_n, cfg.profile_x_max, (), ())
    modes = build_modes(bg, cfg, include_core_four=False, kelvin_seed="displacement")
    print("Chiral bridge current-curl projection")
    print(f"grid n        = {cfg.n}")
    print(f"half_width    = {cfg.half_width}")
    print(f"profile_n     = {cfg.profile_n}")
    print("mode_i mode_j overlap_real overlap_imag abs")
    for i, a in enumerate(modes):
        for j, b in enumerate(modes):
            if a.m_phi == 0 and abs(b.m_phi) == 1:
                value = chiral_overlap(bg, a, b, cfg)
                print(f"{a.name} {b.name} {value.real:.9e} {value.imag:.9e} {abs(value):.9e}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass


try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - command-line dependency guard
    raise SystemExit("kelvin_self_induction.py requires numpy") from exc


@dataclass(frozen=True)
class FilamentKelvinResult:
    m_phi: int
    helicity: int
    radius: float
    core_radius: float
    phi_n: int
    energy_0: float
    stiffness: float
    symplectic_scale: float
    omega_first_order: float
    omega_bdg_scale: float


def ring_curve(radius: float, phi: np.ndarray, amplitude: float, m_phi: int, helicity: int) -> np.ndarray:
    radial = np.stack((np.cos(phi), np.sin(phi), np.zeros_like(phi)), axis=1)
    vertical = np.zeros_like(radial)
    vertical[:, 2] = 1.0
    base = radius * radial
    displacement = amplitude * (np.cos(m_phi * phi)[:, None] * radial - helicity * np.sin(m_phi * phi)[:, None] * vertical)
    return base + displacement


def segment_vectors(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    next_points = np.roll(points, -1, axis=0)
    mids = 0.5 * (points + next_points)
    dl = next_points - points
    return mids, dl


def regularized_biot_savart_energy(points: np.ndarray, core_radius: float) -> float:
    mids, dl = segment_vectors(points)
    diff = mids[:, None, :] - mids[None, :, :]
    dist = np.sqrt(np.sum(diff * diff, axis=2) + core_radius * core_radius)
    dot = np.einsum("ik,jk->ij", dl, dl)
    return float(np.sum(dot / dist) / (8.0 * math.pi))


def kelvin_self_induction(
    radius: float,
    core_radius: float,
    m_phi: int,
    helicity: int,
    phi_n: int,
    amplitude: float,
) -> FilamentKelvinResult:
    phi = np.linspace(0.0, 2.0 * math.pi, phi_n, endpoint=False)
    e0 = regularized_biot_savart_energy(ring_curve(radius, phi, 0.0, m_phi, helicity), core_radius)
    ep = regularized_biot_savart_energy(ring_curve(radius, phi, amplitude, m_phi, helicity), core_radius)
    em = regularized_biot_savart_energy(ring_curve(radius, phi, -amplitude, m_phi, helicity), core_radius)
    stiffness = (ep + em - 2.0 * e0) / (amplitude * amplitude)

    # For a vortex filament, the Kelvin first-order symplectic form scales as
    # Gamma * int |eta|^2 ds. We set Gamma=1 in code units; the radius carries
    # the ring length, while the helicity displacement has unit amplitude.
    symplectic_scale = 2.0 * math.pi * radius
    omega_first_order = stiffness / max(symplectic_scale, 1.0e-30)
    omega_bdg_scale = math.sqrt(abs(omega_first_order))
    return FilamentKelvinResult(
        m_phi=m_phi,
        helicity=helicity,
        radius=radius,
        core_radius=core_radius,
        phi_n=phi_n,
        energy_0=e0,
        stiffness=stiffness,
        symplectic_scale=symplectic_scale,
        omega_first_order=omega_first_order,
        omega_bdg_scale=omega_bdg_scale,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Explicit azimuthal self-induction diagnostic for vortex-ring Kelvin waves.")
    parser.add_argument("--radius", type=float, default=137.035999084)
    parser.add_argument("--core-radius", type=float, default=1.0)
    parser.add_argument("--m-phi", type=int, default=1)
    parser.add_argument("--helicity", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--phi-n", type=int, default=512)
    parser.add_argument("--amplitude", type=float, default=1.0e-3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = kelvin_self_induction(
        radius=args.radius,
        core_radius=args.core_radius,
        m_phi=args.m_phi,
        helicity=args.helicity,
        phi_n=args.phi_n,
        amplitude=args.amplitude,
    )
    print("Vortex-ring Kelvin self-induction")
    print(f"radius                  = {result.radius:.12e}")
    print(f"core_radius             = {result.core_radius:.12e}")
    print(f"m_phi                   = {result.m_phi}")
    print(f"helicity                = {result.helicity}")
    print(f"phi_n                   = {result.phi_n}")
    print(f"energy_0                = {result.energy_0:.12e}")
    print(f"stiffness               = {result.stiffness:.12e}")
    print(f"symplectic_scale        = {result.symplectic_scale:.12e}")
    print(f"omega_first_order        = {result.omega_first_order:.12e}")
    print(f"omega_bdg_scale          = {result.omega_bdg_scale:.12e}")


if __name__ == "__main__":
    main()

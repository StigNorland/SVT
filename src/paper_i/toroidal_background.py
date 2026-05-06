"""Toroidal background helpers for the Paper I static branch.

Status: prototype
Problem type: static
Nondimensionalisation: xi = 1, background density rho0 = 1
Primary role: provide a reusable toroidal-ring background family for issue #13
Key limitation: this is an analytic / semi-analytic background helper, not a 3D relaxed trefoil solver
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math
from typing import Callable


ALPHA_INV = 137.035999084
ALPHA = 1.0 / ALPHA_INV


def default_f0(x: float) -> float:
    """Smooth straight-vortex-like core profile."""
    if x <= 0.0:
        return 0.0
    return math.tanh(x / math.sqrt(2.0))


def default_f0_prime(x: float) -> float:
    """Derivative of the default profile."""
    if x <= 0.0:
        return 1.0 / math.sqrt(2.0)
    y = x / math.sqrt(2.0)
    sech = 1.0 / math.cosh(y)
    return (sech * sech) / math.sqrt(2.0)


def curvature_basis_values(x: float) -> list[float]:
    scales = (1.0, 2.0, 4.0)
    return [(x * x) * math.exp(-x / scale) for scale in scales]


@dataclass(frozen=True)
class ToroidalBackground:
    xi: float = 1.0
    alpha: float = ALPHA
    f0: Callable[[float], float] = default_f0
    f0_prime: Callable[[float], float] = default_f0_prime

    @property
    def r_e(self) -> float:
        return self.xi / self.alpha

    def s(self, r: float, z: float, r_major: float | None = None) -> float:
        r_major = self.r_e if r_major is None else r_major
        return math.sqrt((r - r_major) ** 2 + z * z)

    def theta(self, r: float, z: float, r_major: float | None = None) -> float:
        r_major = self.r_e if r_major is None else r_major
        return math.atan2(z, r - r_major)

    def phase(self, r: float, z: float, r_major: float | None = None) -> complex:
        return cmath.exp(1j * self.theta(r, z, r_major))

    def psi0(self, r: float, z: float, r_major: float | None = None) -> complex:
        r_major = self.r_e if r_major is None else r_major
        s_val = self.s(r, z, r_major)
        return self.f0(s_val / self.xi) * self.phase(r, z, r_major)

    def dsdR(self, r: float, z: float, r_major: float | None = None) -> float:
        r_major = self.r_e if r_major is None else r_major
        s_val = self.s(r, z, r_major)
        if s_val == 0.0:
            return 0.0
        return -(r - r_major) / s_val

    def dthetadR(self, r: float, z: float, r_major: float | None = None) -> float:
        r_major = self.r_e if r_major is None else r_major
        denom = (r - r_major) ** 2 + z * z
        if denom == 0.0:
            return 0.0
        return z / denom

    def dpsi0_dR(self, r: float, z: float, r_major: float | None = None) -> complex:
        r_major = self.r_e if r_major is None else r_major
        s_val = self.s(r, z, r_major)
        theta_val = self.theta(r, z, r_major)
        phase = cmath.exp(1j * theta_val)
        if s_val == 0.0:
            return 0.0j

        x = s_val / self.xi
        amp_term = self.f0_prime(x) * self.dsdR(r, z, r_major) / self.xi
        phase_term = 1j * self.f0(x) * self.dthetadR(r, z, r_major)
        return phase * (amp_term + phase_term)

    def phi_R(self, r: float, z: float, r_major: float | None = None) -> complex:
        r_major = self.r_e if r_major is None else r_major
        return r_major * self.dpsi0_dR(r, z, r_major)

    def phi_chi(self, r: float, z: float, r_major: float | None = None) -> complex:
        r_major = self.r_e if r_major is None else r_major
        s_val = self.s(r, z, r_major)
        theta_val = self.theta(r, z, r_major)
        x = s_val / self.xi
        g_chi = x * math.exp(-x)
        return 1j * g_chi * math.cos(theta_val) * cmath.exp(1j * theta_val)

    def phi_chi_sin(self, r: float, z: float, r_major: float | None = None) -> complex:
        r_major = self.r_e if r_major is None else r_major
        s_val = self.s(r, z, r_major)
        theta_val = self.theta(r, z, r_major)
        x = s_val / self.xi
        g_chi = x * math.exp(-x)
        return 1j * g_chi * math.sin(theta_val) * cmath.exp(1j * theta_val)

    def phi_momentum(self, r: float, z: float, r_major: float | None = None) -> complex:
        """Localized phase/flow seed conjugate to major-radius breathing.

        Ring breathing changes the major radius along the local outward normal, whose
        meridional angular shape is cos(theta). The conjugate momentum is therefore
        represented as a localized phase deformation i p(s) cos(theta) Psi0.
        """
        r_major = self.r_e if r_major is None else r_major
        s_val = self.s(r, z, r_major)
        theta_val = self.theta(r, z, r_major)
        x = s_val / self.xi
        p = x * math.exp(-x)
        return 1j * p * math.cos(theta_val) * self.psi0(r, z, r_major)

    def phi_chi_momentum(self, r: float, z: float, r_major: float | None = None) -> complex:
        """Localized phase/flow seed conjugate to the sine chiral mode.

        The sine chiral coordinate is paired with the opposite meridional parity in
        the phase sector so that it is symplectically independent of P_R.
        """
        r_major = self.r_e if r_major is None else r_major
        s_val = self.s(r, z, r_major)
        theta_val = self.theta(r, z, r_major)
        x = s_val / self.xi
        p = x * math.exp(-x)
        return 1j * p * math.cos(2.0 * theta_val) * self.psi0(r, z, r_major)

    def dpsi0_dr(self, r: float, z: float, r_major: float | None = None) -> complex:
        h = 1.0e-3 * self.xi
        return (self.psi0(r + h, z, r_major) - self.psi0(r - h, z, r_major)) / (2.0 * h)

    def dpsi0_dz(self, r: float, z: float, r_major: float | None = None) -> complex:
        h = 1.0e-3 * self.xi
        return (self.psi0(r, z + h, r_major) - self.psi0(r, z - h, r_major)) / (2.0 * h)

    def phi_kelvin_radial(self, r: float, z: float, r_major: float | None = None) -> complex:
        """Centerline radial displacement seed: delta Psi = -delta r * partial_r Psi0."""
        return -self.dpsi0_dr(r, z, r_major)

    def phi_kelvin_vertical(self, r: float, z: float, r_major: float | None = None) -> complex:
        """Centerline vertical displacement seed: delta Psi = -delta z * partial_z Psi0."""
        return -self.dpsi0_dz(r, z, r_major)


@dataclass(frozen=True)
class CurvedToroidalBackground(ToroidalBackground):
    curvature_coeffs: tuple[float, ...] = ()
    phase_coeffs: tuple[float, ...] = ()

    def f1(self, x: float) -> float:
        return sum(c * b for c, b in zip(self.curvature_coeffs, curvature_basis_values(x)))

    def g1(self, x: float) -> float:
        return sum(c * b for c, b in zip(self.phase_coeffs, curvature_basis_values(x)))

    def psi0(self, r: float, z: float, r_major: float | None = None) -> complex:
        r_major = self.r_e if r_major is None else r_major
        s_val = self.s(r, z, r_major)
        theta_val = self.theta(r, z, r_major)
        x = s_val / self.xi
        amp = self.f0(x) + self.alpha * self.f1(x) * math.cos(theta_val)
        phase = theta_val + self.alpha * self.g1(x) * math.sin(theta_val)
        return amp * cmath.exp(1j * phase)

    def dpsi0_dR(self, r: float, z: float, r_major: float | None = None) -> complex:
        r_major = self.r_e if r_major is None else r_major
        eps = 1.0e-3 * self.xi
        return (self.psi0(r, z, r_major + eps) - self.psi0(r, z, r_major - eps)) / (2.0 * eps)

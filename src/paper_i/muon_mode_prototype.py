from __future__ import annotations

from dataclasses import dataclass
import argparse
import math


ALPHA_INV = 137.035999084
ALPHA = 1.0 / ALPHA_INV
M_E_MEV = 0.51099895
M_MU_OBS_MEV = 105.6583755


@dataclass(frozen=True)
class SSVScales:
    alpha: float = ALPHA
    m_e_mev: float = M_E_MEV
    m_mu_obs_mev: float = M_MU_OBS_MEV

    @property
    def mu0_mev(self) -> float:
        return self.m_e_mev / self.alpha

    @property
    def muon_ladder_mev(self) -> float:
        return 1.5 * self.mu0_mev

    @property
    def ring_ratio(self) -> float:
        return self.alpha * math.sqrt(math.log(1.0 / self.alpha))

    @property
    def muon_ratio_draft(self) -> float:
        return 0.207

    @property
    def enhancement_needed(self) -> float:
        return self.muon_ratio_draft / self.ring_ratio


@dataclass(frozen=True)
class TwoModeModel:
    m_r: float
    k_r: float
    m_chi: float
    k_chi: float
    g: float

    @property
    def omega_r_sq(self) -> float:
        return self.k_r / self.m_r

    @property
    def omega_chi_sq(self) -> float:
        return self.k_chi / self.m_chi

    def eigenvalues_sq(self) -> tuple[float, float]:
        trace = self.omega_r_sq + self.omega_chi_sq
        det_term = (self.omega_r_sq - self.omega_chi_sq) ** 2
        coupling_term = 4.0 * (self.g ** 2) / (self.m_r * self.m_chi)
        root = math.sqrt(det_term + coupling_term)
        omega_minus_sq = 0.5 * (trace - root)
        omega_plus_sq = 0.5 * (trace + root)
        return omega_minus_sq, omega_plus_sq

    def frequencies(self) -> tuple[float, float]:
        omega_minus_sq, omega_plus_sq = self.eigenvalues_sq()
        return math.sqrt(max(omega_minus_sq, 0.0)), math.sqrt(max(omega_plus_sq, 0.0))


def coupling_for_target_lower_root(
    omega_target: float,
    m_r: float,
    k_r: float,
    m_chi: float,
    k_chi: float,
) -> float:
    omega_r_sq = k_r / m_r
    omega_chi_sq = k_chi / m_chi
    lhs = (omega_r_sq - omega_target**2) * (omega_chi_sq - omega_target**2)
    if lhs < 0:
        raise ValueError(
            "No real coupling reaches this target on the lower branch with the chosen uncoupled frequencies."
        )
    return math.sqrt(lhs * m_r * m_chi)


def coupling_for_target_upper_root(
    omega_target: float,
    m_r: float,
    k_r: float,
    m_chi: float,
    k_chi: float,
) -> float:
    omega_r_sq = k_r / m_r
    omega_chi_sq = k_chi / m_chi
    lhs = (omega_r_sq - omega_target**2) * (omega_chi_sq - omega_target**2)
    if lhs < 0:
        raise ValueError(
            "No real coupling reaches this target on the upper branch with the chosen uncoupled frequencies."
        )
    return math.sqrt(lhs * m_r * m_chi)


def build_toy_model(omega_chi: float, omega_target: float, branch: str) -> TwoModeModel:
    m_r = 1.0
    m_chi = 1.0
    scales = SSVScales()
    omega_r = scales.ring_ratio
    k_r = omega_r**2 * m_r
    k_chi = omega_chi**2 * m_chi
    if branch == "lower":
        g = coupling_for_target_lower_root(
            omega_target=omega_target,
            m_r=m_r,
            k_r=k_r,
            m_chi=m_chi,
            k_chi=k_chi,
        )
    else:
        g = coupling_for_target_upper_root(
            omega_target=omega_target,
            m_r=m_r,
            k_r=k_r,
            m_chi=m_chi,
            k_chi=k_chi,
        )
    return TwoModeModel(m_r=m_r, k_r=k_r, m_chi=m_chi, k_chi=k_chi, g=g)


def summarize_model(model: TwoModeModel, scales: SSVScales, branch: str) -> str:
    omega_minus, omega_plus = model.frequencies()
    lines = [
        "SSV muon-mode prototype",
        f"alpha^-1                 = {1.0 / scales.alpha:.9f}",
        f"mu0                      = {scales.mu0_mev:.9f} MeV",
        f"muon ladder prediction   = {scales.muon_ladder_mev:.9f} MeV",
        f"observed muon mass       = {scales.m_mu_obs_mev:.7f} MeV",
        f"bare ring ratio          = {scales.ring_ratio:.9f}",
        f"target ratio (draft)     = {scales.muon_ratio_draft:.9f}",
        f"enhancement needed       = {scales.enhancement_needed:.9f}",
        "",
        "Toy two-mode model",
        f"omega_r                  = {math.sqrt(model.omega_r_sq):.9f}",
        f"omega_chi                = {math.sqrt(model.omega_chi_sq):.9f}",
        f"target branch            = {branch}",
        f"g                        = {model.g:.9f}",
        f"omega_minus              = {omega_minus:.9f}",
        f"omega_plus               = {omega_plus:.9f}",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prototype for the reduced two-mode muon calculation in the SSV framework."
    )
    parser.add_argument(
        "--omega-chi",
        type=float,
        default=0.18,
        help="Assumed uncoupled chiral-mode frequency in units of omega_c.",
    )
    parser.add_argument(
        "--omega-target",
        type=float,
        default=0.207,
        help="Target normal-mode frequency in units of omega_c.",
    )
    parser.add_argument(
        "--branch",
        choices=("lower", "upper"),
        default="upper",
        help="Which normal-mode branch to force to the target frequency.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scales = SSVScales()
    model = build_toy_model(
        omega_chi=args.omega_chi, omega_target=args.omega_target, branch=args.branch
    )
    print(summarize_model(model, scales, branch=args.branch))


if __name__ == "__main__":
    main()

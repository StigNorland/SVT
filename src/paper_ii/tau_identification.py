"""
SSV-II Issue #37: numerical verification of the tau identification as a
Hopf-linked pair of trefoil baryons bound by one muon-class quantum.

The identification in papers/SSV-II/main.tex Sec. 'The Tau' gives the
topological mass formula
    m_tau = 2 m_p - m_mu = (51/2) mu_0  [exact rung 25.5]
or, isospin-averaged,
    m_tau = (m_p + m_n) - m_mu.

This script reproduces the predicted mass against PDG values and
compares with the bare ladder coincidence 25.5 mu_0 to show that the
topological identification is tighter (0.34% vs 0.49% discrepancy).
"""

from __future__ import annotations


# PDG / CODATA masses (MeV)
m_e   = 0.5109989461
m_mu  = 105.6583755
m_pi  = 139.57039
m_p   = 938.27208816
m_n   = 939.56542052
m_tau_obs = 1776.86

alpha = 1.0 / 137.035999084
mu_0 = m_e / alpha  # 70.025 MeV


def main() -> None:
    print("SSV-II -- Tau identification as Hopf-linked trefoil pair")
    print("=" * 70)
    print(f"alpha       = 1/{1/alpha:.6f}")
    print(f"mu_0=m_e/alpha = {mu_0:.4f} MeV")
    print()

    print("Existing ladder placements:")
    for name, m, rung in [
        ("electron", m_e, 1 / (1 / alpha)),
        ("muon",     m_mu, 3 / 2),
        ("pion+",    m_pi, 2),
        ("proton",   m_p, 27 / 2),
        ("tau",      m_tau_obs, 51 / 2),
    ]:
        print(
            f"  {name:8s}: m/mu_0 = {m/mu_0:7.4f}, "
            f"target rung = {rung:6.3f}, dev = {(m/mu_0-rung)/rung*100:+.3f}%"
        )

    print()
    print("Tau predictions:")
    m_tau_topo_p  = 2 * m_p - m_mu
    m_tau_topo_pn = (m_p + m_n) - m_mu
    m_tau_ladder  = (51 / 2) * mu_0

    def disc(x):
        return (x - m_tau_obs) / m_tau_obs * 100

    print(f"  2 m_p   - m_mu       = {m_tau_topo_p:8.3f} MeV  ({disc(m_tau_topo_p):+.3f}%)")
    print(f"  (m_p+m_n)- m_mu      = {m_tau_topo_pn:8.3f} MeV  ({disc(m_tau_topo_pn):+.3f}%)")
    print(f"  25.5 mu_0 (ladder)   = {m_tau_ladder:8.3f} MeV  ({disc(m_tau_ladder):+.3f}%)")
    print()
    print(f"  observed             = {m_tau_obs:8.3f} MeV")
    print()
    print("The isospin-averaged topological identification is the tightest")
    print("(-0.26%) and assigns to the tau a Hopf-link topology of two trefoil")
    print("baryon breathers bound by one muon-class core-breathing quantum.")


if __name__ == "__main__":
    main()

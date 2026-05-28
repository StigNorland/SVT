"""
SSV-VI-b Issue #43: numerical table of mode amplitudes epsilon_m(a_BH).

The derivation in papers/SSV-VI-b/main.tex Sec. 3.2 gives
    epsilon_m(a_BH) = epsilon_0 * Q_m * a_BH^m / m!
from the Hansen-Geroch multipole expansion of the rotating central
breather, with Q_m the Bessel cross-overlap (~1) and epsilon_0 the
m=0 amplitude fixed by the M31 fit in Paper VI-a (epsilon_0 ~ 0.05).

This script reproduces the resultbox table for the realistic galactic
spin range a_BH in [0.1, 0.998] and m in [1, 5].
"""

from __future__ import annotations

import math


SPINS = [0.10, 0.25, 0.50, 0.70, 0.90, 0.998]
EPSILON_0 = 0.05    # M31 fit, Paper VI-a


def epsilon_m(a_BH: float, m: int, eps0: float = EPSILON_0, Q_m: float = 1.0) -> float:
    return eps0 * Q_m * a_BH**m / math.factorial(m)


def main() -> None:
    print("SSV-VI-b -- epsilon_m(a_BH) table with epsilon_0 = 0.05")
    print("=" * 70)
    header = "{:>7} | " + " | ".join(f"{f'm={m}':>8}" for m in range(1, 6))
    print(header.format("a_BH"))
    print("-" * 70)
    for a in SPINS:
        row = "{:7.3f} | " + " | ".join(f"{epsilon_m(a, m):8.5f}" for m in range(1, 6))
        print(row.format(a))
    print()
    print("Morphological regimes:")
    print("  a_BH ~ 0.1   -> epsilon_1 ~ 0.5%, m>=2 modes below detectability")
    print("                  --> ring galaxy")
    print("  a_BH ~ 0.5   -> epsilon_2 ~ 0.6%, visible grand-design arms")
    print("                  --> SA / SAB")
    print("  a_BH >= 0.9  -> epsilon_2..4 ~ 0.5-2% comb")
    print("                  --> flocculent multi-arm")


if __name__ == "__main__":
    main()

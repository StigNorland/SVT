"""Conventional-healing-length LogSE vortex profile for issue #218.

Status: corrected Paper I baseline
Problem type: static, 1D
Nondimensionalisation: x = r/xi with
``xi = hbar/(sqrt(2) m0 c_s)``

The corrected stable LogSE profile is

    f'' + f'/x - f/x^2 - f log(f^2) = 0.

The coefficient-two implementation in :mod:`vortex_profile` remains available
as a legacy control.  The equations are related exactly by

    f_corrected(x) = f_legacy(x/sqrt(2)).

The corrected solver is nevertheless integrated independently so this
rescaling can serve as a negative-capable numerical control rather than being
assumed by construction.
"""

from __future__ import annotations

import argparse

try:
    from .vortex_profile import VortexProfile
except ImportError:  # Standalone execution from instruments/paper_i.
    from vortex_profile import VortexProfile


class CorrectedVortexProfile(VortexProfile):
    """Coefficient-one profile in conventional healing-length units."""

    LOG_COEFFICIENT = 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Solve the corrected planar LogSE vortex profile."
    )
    parser.add_argument("--x-min", type=float, default=1.0e-4)
    parser.add_argument("--x-max", type=float, default=20.0)
    parser.add_argument("--n", type=int, default=2000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    profile = CorrectedVortexProfile.solve(
        x_min=args.x_min,
        x_max=args.x_max,
        n=args.n,
    )
    print("Corrected planar LogSE vortex profile")
    print(f"log coefficient = {profile.LOG_COEFFICIENT:g}")
    print(f"x_min           = {args.x_min}")
    print(f"x_max           = {args.x_max}")
    print(f"n               = {args.n}")
    print(f"slope           = {profile.slope:.12f}")
    for x in (0.1, 1.0, 5.0, 10.0, args.x_max):
        print(f"f({x:g})          = {profile.value(x):.12f}")


if __name__ == "__main__":
    main()

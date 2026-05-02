from __future__ import annotations

from dataclasses import dataclass
import argparse
import math


def vortex_rhs(x: float, f: float, fp: float) -> tuple[float, float]:
    """Planar LogSE vortex profile equation from Appendix C.

    The dimensionless equation is

        f'' + (1/x) f' - f/x^2 - 2 f log(f^2) = 0.

    This returns (f', f'').
    """
    safe_x = max(x, 1.0e-12)
    safe_f = max(abs(f), 1.0e-300)
    fpp = -(fp / safe_x) + (f / (safe_x * safe_x)) + 2.0 * f * math.log(safe_f * safe_f)
    return fp, fpp


def rk4_step(x: float, f: float, fp: float, h: float) -> tuple[float, float]:
    k1_f, k1_fp = vortex_rhs(x, f, fp)
    k2_f, k2_fp = vortex_rhs(x + 0.5 * h, f + 0.5 * h * k1_f, fp + 0.5 * h * k1_fp)
    k3_f, k3_fp = vortex_rhs(x + 0.5 * h, f + 0.5 * h * k2_f, fp + 0.5 * h * k2_fp)
    k4_f, k4_fp = vortex_rhs(x + h, f + h * k3_f, fp + h * k3_fp)
    next_f = f + (h / 6.0) * (k1_f + 2.0 * k2_f + 2.0 * k3_f + k4_f)
    next_fp = fp + (h / 6.0) * (k1_fp + 2.0 * k2_fp + 2.0 * k3_fp + k4_fp)
    return next_f, next_fp


def integrate_profile(
    slope: float,
    x_min: float,
    x_max: float,
    n: int,
) -> tuple[list[float], list[float], list[float]]:
    h = (x_max - x_min) / (n - 1)
    xs = [x_min + i * h for i in range(n)]
    fs = [0.0 for _ in range(n)]
    fps = [0.0 for _ in range(n)]

    # Core regularity: f ~ slope * x, f' ~ slope.
    f = slope * x_min
    fp = slope
    fs[0] = f
    fps[0] = fp

    for i in range(1, n):
        f, fp = rk4_step(xs[i - 1], f, fp, h)
        if not math.isfinite(f) or not math.isfinite(fp):
            f = float("nan")
            fp = float("nan")
        fs[i] = f
        fps[i] = fp
    return xs, fs, fps


def endpoint_residual(slope: float, x_min: float, x_max: float, n: int) -> float:
    _, fs, _ = integrate_profile(slope, x_min, x_max, n)
    f_end = fs[-1]
    if not math.isfinite(f_end):
        return float("inf")
    return f_end - 1.0


def find_bracket(x_min: float, x_max: float, n: int) -> tuple[float, float]:
    prev_slope = 0.01
    prev_res = endpoint_residual(prev_slope, x_min, x_max, n)
    slope = prev_slope
    for _ in range(80):
        slope *= 1.25
        res = endpoint_residual(slope, x_min, x_max, n)
        if math.isfinite(prev_res) and math.isfinite(res) and prev_res * res <= 0.0:
            return prev_slope, slope
        prev_slope = slope
        prev_res = res
    raise RuntimeError("Could not bracket the vortex shooting slope.")


def solve_shooting_slope(
    x_min: float = 1.0e-4,
    x_max: float = 20.0,
    n: int = 2000,
    iterations: int = 80,
) -> float:
    lo, hi = find_bracket(x_min, x_max, n)
    r_lo = endpoint_residual(lo, x_min, x_max, n)
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        r_mid = endpoint_residual(mid, x_min, x_max, n)
        if abs(r_mid) < 1.0e-12:
            return mid
        if r_lo * r_mid <= 0.0:
            hi = mid
        else:
            lo = mid
            r_lo = r_mid
    return 0.5 * (lo + hi)


@dataclass(frozen=True)
class VortexProfile:
    xs: tuple[float, ...]
    fs: tuple[float, ...]
    fps: tuple[float, ...]
    slope: float

    @classmethod
    def solve(
        cls,
        x_min: float = 1.0e-4,
        x_max: float = 20.0,
        n: int = 2000,
    ) -> "VortexProfile":
        slope = solve_shooting_slope(x_min=x_min, x_max=x_max, n=n)
        xs, fs, fps = integrate_profile(slope, x_min, x_max, n)
        return cls(xs=tuple(xs), fs=tuple(fs), fps=tuple(fps), slope=slope)

    def value(self, x: float) -> float:
        if x <= self.xs[0]:
            return self.slope * max(x, 0.0)
        if x >= self.xs[-1]:
            return 1.0
        i = self._index(x)
        x0 = self.xs[i]
        x1 = self.xs[i + 1]
        t = (x - x0) / (x1 - x0)
        return (1.0 - t) * self.fs[i] + t * self.fs[i + 1]

    def derivative(self, x: float) -> float:
        if x <= self.xs[0]:
            return self.slope
        if x >= self.xs[-1]:
            return 0.0
        i = self._index(x)
        x0 = self.xs[i]
        x1 = self.xs[i + 1]
        t = (x - x0) / (x1 - x0)
        return (1.0 - t) * self.fps[i] + t * self.fps[i + 1]

    def _index(self, x: float) -> int:
        lo = 0
        hi = len(self.xs) - 2
        while lo <= hi:
            mid = (lo + hi) // 2
            if self.xs[mid] <= x <= self.xs[mid + 1]:
                return mid
            if x < self.xs[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        return max(0, min(len(self.xs) - 2, lo))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Solve the planar LogSE vortex profile.")
    parser.add_argument("--x-min", type=float, default=1.0e-4)
    parser.add_argument("--x-max", type=float, default=20.0)
    parser.add_argument("--n", type=int, default=2000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    profile = VortexProfile.solve(x_min=args.x_min, x_max=args.x_max, n=args.n)
    print("Planar LogSE vortex profile")
    print(f"x_min       = {args.x_min}")
    print(f"x_max       = {args.x_max}")
    print(f"n           = {args.n}")
    print(f"slope       = {profile.slope:.12f}")
    for x in (0.1, 1.0, 5.0, 10.0, args.x_max):
        print(f"f({x:g})      = {profile.value(x):.12f}")
        print(f"Veff({x:g})   = {4.0 * (1.0 - profile.value(x) ** 2):.12f}")


if __name__ == "__main__":
    main()

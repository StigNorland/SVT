# SSV-VII-a — C-gate damage report

Status: **closure-grade** · Gate: **C-GATE PASS, but the section is voided by the D1 branch decision** (#189)

| # | Key | Claim | Verdict |
|---|---|---|---|
| C1 | `BialynickiBirula1976` | the LogSE admits an exact Gaussian stationary solution, the Gausson | **`OK`** as attribution — pre-arXiv, not retrieved, but this is unambiguously the BBM paper's result |

## The citation is fine; the section is not

Under the **branch decision of 2026-07-27** (SSV-I D1: stable vacuum, $b<0$) the
BBM Gausson **does not exist**. It is a solution only of the attractive branch,
which was rejected because it makes the uniform vacuum modulationally unstable
and therefore cannot support $c_s=c$.

So `eq:gausson` has no solution under the adopted theory, and
§"Saturation by the Gausson" must be withdrawn or explicitly relabelled as
belonging to the rejected branch.

## Independent concern — the $\hbar/2$ derivation may be circular

Flagged in the D1 E-gate and repeated here as this paper's own item. §295 ff.
claims the $\hbar/2$ prefactor is *"derived directly from the LogSE itself,
without importing it from the standard wave-packet calculation"*, and notes the
result is *"independent of the Gausson width $\sigma$ and therefore independent
of the LogSE coupling $b$"*.

But **every** Gaussian saturates $\Delta x\,\Delta p=\hbar/2$ — elementary
quantum mechanics. The width-independence the paper offers as evidence of
robustness is precisely the signal that the LogSE contributed nothing beyond
supplying *a* Gaussian; the computation performed (Gaussian moments $\to$
$\sigma^2/2$ and $\hbar^2/2\sigma^2$) **is** the standard wave-packet
calculation it claims not to import.

This holds independently of the sign decision. Both issues must be resolved
together when the section is rewritten.

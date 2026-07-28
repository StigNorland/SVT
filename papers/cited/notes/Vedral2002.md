# Vedral2002 — citation evidence

V. Vedral, *The role of relative entropy in quantum information theory*,
Rev. Mod. Phys. **74**, 197–234 (2002).

Primary source: arXiv:quant-ph/0102094 · DOI:
10.1103/RevModPhys.74.197 · local PDF sha256 `523d4be80d9bf10d`.

## SSV usage

SSV-III `main.tex:1018–1023` identifies monotonic decrease of relative
entropy under coarse-graining with the quantum data-processing inequality.
This follows an application of the same theorem to a proposed CPTP block map.

## Source result and explanation

In Sec. II.C, printed p. 209 (PDF p. 13), the review states:

> For any completely positive, trace preserving map \(\Phi\), given by
> \(\Phi\sigma=\sum_i V_i\sigma V_i^\dagger\) and
> \(\sum_i V_i^\dagger V_i=1\), we have that
> \(S(\Phi\sigma\Vert\Phi\rho)\leq S(\sigma\Vert\rho)\).

The following explanation represents a CP map as a unitary operation on an
extended Hilbert space followed by a partial trace: the unitary leaves
relative entropy unchanged, while tracing out the extension loses
information and cannot increase it.

**Verdict: `OK`.** This directly supports the data-processing statement.
Like Lindblad1975, it does not establish that SSV's specific block operation
is CPTP, that its reference state is fixed, or that SSV's \(dS/d\ln b\)
equals the corresponding relative-entropy decrease. Those are additional
premises of the SSV construction.

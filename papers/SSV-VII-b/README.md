# SSV VII-b

Working title: `Emergent Geometry and the Dissolution of Quantum Gravity`

Scope: geometry as a macroscopic limit of the medium and why the usual quantum-gravity problem is mis-posed in SSV.

Issue `#2` split role: receives the emergent-geometry and quantum-gravity material from the legacy unified `SSV V` draft and keeps it separate from QM and cosmogony.

## Draft status (aligned to outline — 6 sections + conclusion)

Structure matches the outline exactly:

1. **Introduction** — context from Papers I–V and VII-a; scope (out: full QM derivation → VII-a, BH ontology → V, cosmogony → VIII); roadmap.
2. **Why Quantizing the Metric Is the Wrong Level** — the dissolution argument; quantising the metric is like quantising the wake, not the fluid; resultbox.
3. **Emergent Metric Picture** — density as gravitational potential $\Phi = b\ln(\rho/\rho_0)$; time dilation; isotropic post-Newtonian metric $g_{\mu\nu}$ with $h_{ij} = h_{00}\delta_{ij}$; emergent metric resultbox.
4. **Weak-Field Correspondence** — Bjerknes force recap (Newton's constant from acoustic coupling); post-Newtonian gradient expansion; **factor-of-two horizon correction** resolved: spatial curvature $h_{ij}$ doubles effective potential, yields $r_H = 2GM/c^2$, $\kappa = c^4/(4GM)$, $T_H = \hbar c^3/(8\pi GMk_B)$; resultbox.
5. **Relation to General Relativity** — Jacobson 5-step acoustic-thermodynamic route; $G = c\xi/m_0$ from entropy density; cosmological constant as saturation pressure (no fine-tuning); Planck scale = healing length; gapbox for quantitative $G$.
6. **Discussion** — position in series; analogue-gravity comparison; four open problems (quantitative $G$, Kerr exterior, strong-field deviations, dark energy → VIII); **Success criteria for this paper** (§6.4): five positive criteria the paper meets within its stated scope, plus the explicit closure-grade upgrade condition for each open problem.
- **Conclusion** — five numbered results.

## Changes from previous draft

- Section structure fixed: 5 sections → 6 (matching outline).
- Old §3 "Gravity as Hydrodynamics: From Bjerknes to Einstein" split into:
  - §3 Emergent Metric Picture (density ↔ potential, time dilation, metric tensor)
  - §4 Weak-Field Correspondence (Bjerknes recap, post-Newtonian expansion, factor-of-two resolution)
  - §5 Relation to General Relativity (Jacobson route, cosmological constant, Planck scale)
- **Factor-of-two horizon discrepancy** (open in Papers IV and V) explicitly resolved in §4.3: spatial curvature $h_{ij}$ corrects the Newtonian-limit $r_H = GM/c^2$ to $r_H = 2GM/c^2$, closing both the factor-of-two and factor-of-four gaps.
- Old §4 "Discussion and Open Problems" → §6 "Discussion" (expanded: series position, analogue-gravity comparison, four open problems).
- Citation keys updated: ssv1/2/3/4 → SSV-I/II/III/IV; SSV-V and SSV-VIIa added; ssv4 description corrected (was "Galactic-Scale Resonances", now "Gravity as Update-Capacity Gradient").
- Stale OPH (observer-patch-holography) external reference removed.
- Duplicate `\end{document}` removed.
- Broken `\ref{eq:cont}`, `\ref{eq:Euler}`, `\ref{eq:Schrodinger}` replaced with correct inline descriptions or references to VII-a.
- `resultbox` tcolorbox environment added (was missing, only gapbox was defined).
- `\tableofcontents` added.
- Title formatting updated to match series style.
- Unruh1981 and Visser1998 references added for analogue-gravity context.

## Open gapboxes (deferred)

- Quantitative $G$ from $\{m_e, \alpha, \hbar, c\}$: $m_0 = m_P$ identification in entropy formula is the same problem as deriving $\alpha_G$ from Paper II proton breather geometry
- Full Kerr exterior and no-hair proof → companion analysis
- Strong-field validation beyond post-Newtonian expansion → numerical programme
- Dark energy / $\Lambda$ numerical value → Paper VIII

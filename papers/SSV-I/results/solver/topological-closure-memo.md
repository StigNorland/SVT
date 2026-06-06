# Topological Closure Memo

This note records the source-based conclusion reached after re-reading the Paper I proton section, the trefoil minimisation plan, and the units-audit draft.

## Question

What is the static proton branch actually supposed to preserve or close on?

## Source Read

The most relevant statements are:

- [main.tex](../../papers/SSV-I/main.tex:512) describes the proton as a stable spherical breather held open by an internal trefoil `Y`-junction skeleton.
- [main.tex](../../papers/SSV-I/main.tex:516) identifies the stabilising structure as three quantized vortex filaments meeting at a central node.
- [main.tex](../../papers/SSV-I/main.tex:525) says the filament legs carry fractions of the total topological charge.
- [main.tex](../../papers/SSV-I/main.tex:567) says the trefoil skeleton is topologically protected.
- [trefoil-breather-minimisation-plan.md](../../papers/SSV-I/trefoil-breather-minimisation-plan.md:49) requires phase winding to be fixed consistently on each branch.
- [trefoil-breather-minimisation-plan.md](../../papers/SSV-I/trefoil-breather-minimisation-plan.md:71) says the solver should track energy and topology through the relaxation.
- [trefoil-breather-minimisation-plan.md](../../papers/SSV-I/trefoil-breather-minimisation-plan.md:108) explicitly calls for a topology-preservation check.

The units-audit draft reinforces that the proton is a different defect topology, not just a different norm scale:

- [SSV-units-audit-draft-04.tex](../../notes/SSV-units-audit-draft-04.tex:1058) states that the proton breather uses `m_0 = m_p`.
- [SSV-units-audit-draft-04.tex](../../notes/SSV-units-audit-draft-04.tex:1071) frames the hierarchy problem as the same functional producing different scales from different topologies.

## Conclusion

The source material supports the following reading:

- the intended invariant is topological branch identity and winding content
- the intended closure is full 3D energy minimisation of that topological object
- a topology-preservation diagnostic belongs in the solver
- the current global interior `L2` constraint is numerically useful, but it is not source-derived as the fundamental proton invariant

## Immediate Numerical Consequence

The first topology-facing diagnostic should be modest and local:

- measure whether the relaxed field still carries approximately unit winding around the seeded trefoil centerline
- report that alongside energy, residual, and gravity-facing source quantities

This does not yet classify the full knot type. It is a first check that the solver is preserving the filament identity the paper text relies on.

## Next Step

Use the new winding-retention diagnostic to compare:

- unconstrained flow
- current global `L2`-constrained flow
- future alternative closure rules

The question is not just which branch is numerically stable. It is which branch preserves the intended proton topology while yielding a reproducible static source.

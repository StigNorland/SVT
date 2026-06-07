"""Tests for the issue #29 topology-import bookkeeping checks."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.append(str(SRC_ROOT))

from paper_ii.topology_import_checks import (
    SSV_LEPTON_CLASSES,
    VortexLinkSample,
    all_y_junction_permutations,
    charge_from_chiral_crossings,
    circular_core_curve,
    discrete_permutation_group_is_su3_derivation,
    has_mode_only_generation_step,
    is_phase_balanced,
    lepton_skeletons,
    graph_edge_crossing_numbers,
    extraction_diagnostic,
    framed_torus_ribbon_curves,
    projected_crossings,
    rounded_linking_number,
    extract_vortex_link_samples,
    signed_crossing_numbers,
    stitch_axis_aligned_vortex_curves,
    stitch_vortex_graph,
    stitch_vortex_graph_dual_lattice,
    synthetic_curve_vortex_field,
    synthetic_vortex_ring_field,
    standard_trefoil_curve,
    three_colour_phase_classes,
)


def _vortex_z_field(n: int, z_extent: int) -> object:
    x = np.arange(n) - (n - 1) / 2.0
    y = np.arange(n) - (n - 1) / 2.0
    x_grid, y_grid = np.meshgrid(x, y, indexing="ij")
    phase = np.arctan2(y_grid, x_grid)
    amp = np.tanh(np.sqrt(x_grid**2 + y_grid**2))
    field_2d = amp * np.exp(1j * phase)
    return np.stack([field_2d] * z_extent, axis=-1)


def _antivortex_z_field(n: int, z_extent: int) -> object:
    field = _vortex_z_field(n, z_extent)
    return np.conjugate(field)


def _samples_from_curve(curve: np.ndarray, winding: int = 1, axis: str = "z") -> tuple[VortexLinkSample, ...]:
    return tuple(
        VortexLinkSample(
            center=tuple(float(value) for value in point),
            axis=axis,
            winding=winding,
        )
        for point in curve
    )


def test_chiral_crossing_charge_units_reproduce_basic_sm_targets():
    assert charge_from_chiral_crossings([1]) == 1 / 3
    assert charge_from_chiral_crossings([1, 1]) == 2 / 3
    assert charge_from_chiral_crossings([-1, -1, -1]) == -1
    assert charge_from_chiral_crossings([1, 1, -1]) == 1 / 3


def test_neutral_composite_crossing_count_is_zero():
    assert charge_from_chiral_crossings([1, 1, 1, -1, -1, -1]) == 0


def test_uniform_field_extracts_no_vortex_link_samples():
    psi = np.ones((6, 6, 6), dtype=complex)
    assert extract_vortex_link_samples(psi) == ()


def test_straight_vortex_field_extracts_z_axis_link_samples():
    n = 8
    samples = extract_vortex_link_samples(_vortex_z_field(n, z_extent=n))
    assert len(samples) == n
    assert {sample.axis for sample in samples} == {"z"}
    assert {sample.winding for sample in samples} == {1}
    assert sorted(sample.center[2] for sample in samples) == list(range(n))


def test_straight_antivortex_flips_extracted_winding_sign():
    n = 8
    samples = extract_vortex_link_samples(_antivortex_z_field(n, z_extent=n))
    assert len(samples) == n
    assert {sample.axis for sample in samples} == {"z"}
    assert {sample.winding for sample in samples} == {-1}


def test_vortex_link_sample_coordinates_honor_dx_and_origin():
    n = 8
    dx = 0.5
    origin = (-2.0, -2.0, -1.0)
    samples = extract_vortex_link_samples(_vortex_z_field(n, z_extent=n), dx=dx, origin=origin)
    assert len(samples) == n
    assert sorted(sample.center[2] for sample in samples) == [origin[2] + k * dx for k in range(n)]


def test_straight_vortex_samples_stitch_to_one_ordered_curve():
    n = 8
    samples = extract_vortex_link_samples(_vortex_z_field(n, z_extent=n))
    curves = stitch_axis_aligned_vortex_curves(samples)
    assert len(curves) == 1
    curve = curves[0]
    assert curve.axis == "z"
    assert curve.winding == 1
    assert len(curve.points) == n
    assert tuple(point[2] for point in curve.points) == tuple(range(n))


def test_straight_antivortex_samples_stitch_with_negative_winding():
    n = 8
    samples = extract_vortex_link_samples(_antivortex_z_field(n, z_extent=n))
    curves = stitch_axis_aligned_vortex_curves(samples)
    assert len(curves) == 1
    assert curves[0].axis == "z"
    assert curves[0].winding == -1


def test_two_parallel_vortex_groups_stitch_to_two_curves():
    samples = (
        *[
            VortexLinkSample(axis="z", winding=1, center=(0.5, 0.5, float(k)))
            for k in range(4)
        ],
        *[
            VortexLinkSample(axis="z", winding=1, center=(2.5, 0.5, float(k)))
            for k in range(4)
        ],
    )
    curves = stitch_axis_aligned_vortex_curves(samples)
    assert len(curves) == 2
    assert sorted(len(curve.points) for curve in curves) == [4, 4]


def test_graph_stitcher_extracts_one_open_edge_from_straight_vortex():
    n = 8
    samples = extract_vortex_link_samples(_vortex_z_field(n, z_extent=n))
    graph = stitch_vortex_graph(samples, max_distance=1.01)
    assert graph.dropped_samples == 0
    assert graph.ambiguous_components == 0
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1
    assert not graph.edges[0].closed
    assert len(graph.edges[0].points) == n


def test_graph_stitcher_keeps_two_parallel_chains_separate():
    samples = (
        *[
            VortexLinkSample(axis="z", winding=1, center=(0.0, 0.0, float(k)))
            for k in range(4)
        ],
        *[
            VortexLinkSample(axis="z", winding=1, center=(3.0, 0.0, float(k)))
            for k in range(4)
        ],
    )
    graph = stitch_vortex_graph(samples, max_distance=1.01)
    assert graph.ambiguous_components == 0
    assert len(graph.edges) == 2
    assert sorted(len(edge.points) for edge in graph.edges) == [4, 4]


def test_graph_stitcher_extracts_closed_loop_from_circle_fixture():
    curve = circular_core_curve(samples=48)
    samples = _samples_from_curve(curve)
    graph = stitch_vortex_graph(samples, max_distance=0.2)
    assert graph.dropped_samples == 0
    assert graph.ambiguous_components == 0
    assert len(graph.nodes) == 0
    assert len(graph.edges) == 1
    assert graph.edges[0].closed


def test_graph_stitched_trefoil_edge_feeds_projected_crossing_counter():
    curve = standard_trefoil_curve(samples=180)
    samples = _samples_from_curve(curve)
    graph = stitch_vortex_graph(samples, max_distance=0.25)
    assert graph.ambiguous_components == 0
    assert len(graph.edges) == 1
    assert graph.edges[0].closed
    signs = graph_edge_crossing_numbers(graph)
    assert len(signs) == 3
    assert set(signs) == {-1}


def test_graph_stitcher_flags_trefoil_when_neighbor_radius_creates_shortcuts():
    curve = standard_trefoil_curve(samples=180)
    samples = _samples_from_curve(curve)
    graph = stitch_vortex_graph(samples, max_distance=0.35)
    assert graph.edges == ()
    assert graph.ambiguous_components == 1


def test_graph_stitcher_extracts_trivalent_y_fixture():
    samples = (
        VortexLinkSample(axis="x", winding=1, center=(0.0, 0.0, 0.0)),
        VortexLinkSample(axis="x", winding=1, center=(1.0, 0.0, 0.0)),
        VortexLinkSample(axis="x", winding=1, center=(2.0, 0.0, 0.0)),
        VortexLinkSample(axis="y", winding=1, center=(0.0, 1.0, 0.0)),
        VortexLinkSample(axis="y", winding=1, center=(0.0, 2.0, 0.0)),
        VortexLinkSample(axis="z", winding=1, center=(0.0, 0.0, 1.0)),
        VortexLinkSample(axis="z", winding=1, center=(0.0, 0.0, 2.0)),
    )
    graph = stitch_vortex_graph(samples, max_distance=1.01)
    assert graph.ambiguous_components == 0
    assert len(graph.edges) == 3
    assert len([node for node in graph.nodes if node.kind == "junction"]) == 1
    assert len([node for node in graph.nodes if node.kind == "endpoint"]) == 3


def test_synthetic_vortex_ring_field_stitches_as_one_closed_loop():
    psi, dx, origin = synthetic_vortex_ring_field(n=48, half_width=6.0, radius=2.0)
    diagnostic = extraction_diagnostic(
        "ring",
        psi,
        dx=dx,
        origin=origin,
        max_distance=1.01 * dx,
        require_same_winding=False,
    )
    assert diagnostic.status == "ok"
    assert diagnostic.sample_count == 64
    assert diagnostic.edge_count == 1
    assert diagnostic.closed_edges == 1
    assert diagnostic.crossing_signs == ((),)


def test_framed_torus_ribbon_linking_tracks_integer_twist():
    core, untwisted = framed_torus_ribbon_curves(twist=0)
    assert rounded_linking_number(core, untwisted) == 0

    core, once_twisted = framed_torus_ribbon_curves(twist=1)
    assert rounded_linking_number(core, once_twisted) == -1

    core, twice_twisted = framed_torus_ribbon_curves(twist=2)
    assert rounded_linking_number(core, twice_twisted) == -2


def test_synthetic_trefoil_field_is_not_yet_cleanly_stitched_to_target_knot():
    curve = standard_trefoil_curve(samples=240)
    psi, dx, origin = synthetic_curve_vortex_field(curve, n=56, half_width=5.0, core_radius=0.8)
    diagnostic = extraction_diagnostic(
        "trefoil-field",
        psi,
        dx=dx,
        origin=origin,
        max_distance=1.01 * dx,
        require_same_winding=False,
    )
    assert diagnostic.status == "ambiguous"
    assert diagnostic.ambiguous_components > 0


def test_dual_lattice_trefoil_field_exposes_main_loop_and_secondary_artifact():
    curve = standard_trefoil_curve(samples=240)
    psi, dx, origin = synthetic_curve_vortex_field(curve, n=56, half_width=5.0, core_radius=0.8)
    diagnostic = extraction_diagnostic(
        "trefoil-field-dual",
        psi,
        dx=dx,
        origin=origin,
        max_distance=0.0,
        stitching="dual",
        require_same_winding=False,
        crossing_smooth_window=2,
        crossing_smooth_iterations=2,
    )
    assert diagnostic.status == "ok"
    assert diagnostic.sample_count == 382
    assert diagnostic.edge_count == 2
    assert diagnostic.closed_edges == 2
    assert diagnostic.crossing_signs == ((-1, -1, -1), ())


def test_dual_lattice_trefoil_field_dominant_centerline_recovers_target_knot():
    curve = standard_trefoil_curve(samples=240)
    psi, dx, origin = synthetic_curve_vortex_field(curve, n=56, half_width=5.0, core_radius=0.8)
    diagnostic = extraction_diagnostic(
        "trefoil-field-dominant",
        psi,
        dx=dx,
        origin=origin,
        max_distance=0.0,
        stitching="dual",
        require_same_winding=False,
        keep_largest_component=True,
        crossing_smooth_window=2,
        crossing_smooth_iterations=2,
    )
    assert diagnostic.status == "ok"
    assert diagnostic.sample_count == 382
    assert diagnostic.edge_count == 1
    assert diagnostic.closed_edges == 1
    assert diagnostic.dropped_samples == 128
    assert diagnostic.crossing_signs == ((-1, -1, -1),)


def test_dual_lattice_stitcher_collapses_trivalent_y_junction_cluster():
    samples = (
        VortexLinkSample(axis="x", winding=1, center=(0.5, 0.0, 0.0)),
        VortexLinkSample(axis="x", winding=1, center=(1.5, 0.0, 0.0)),
        VortexLinkSample(axis="y", winding=1, center=(0.0, 0.5, 0.0)),
        VortexLinkSample(axis="y", winding=1, center=(0.0, 1.5, 0.0)),
        VortexLinkSample(axis="z", winding=1, center=(0.0, 0.0, 0.5)),
        VortexLinkSample(axis="z", winding=1, center=(0.0, 0.0, 1.5)),
    )
    graph = stitch_vortex_graph_dual_lattice(samples, dx=1.0)
    assert graph.ambiguous_components == 0
    assert len(graph.edges) == 3
    assert len([node for node in graph.nodes if node.kind == "junction"]) == 1
    assert len([node for node in graph.nodes if node.kind == "endpoint"]) == 3


def test_planar_circle_fixture_has_no_projected_crossings():
    crossings = projected_crossings(circular_core_curve())
    assert crossings == ()


def test_standard_trefoil_fixture_has_three_same_sign_crossings():
    signs = signed_crossing_numbers(standard_trefoil_curve())
    assert len(signs) == 3
    assert set(signs) == {-1}


def test_mirror_trefoil_flips_crossing_signs():
    curve = standard_trefoil_curve()
    mirrored = curve.copy()
    mirrored[:, 2] *= -1.0
    assert signed_crossing_numbers(mirrored) == (1, 1, 1)


def test_trefoil_crossing_count_maps_to_unit_charge_target():
    signs = signed_crossing_numbers(standard_trefoil_curve())
    assert charge_from_chiral_crossings(signs) == -1


def test_three_colour_phase_classes_are_balanced():
    classes = three_colour_phase_classes()
    assert len(classes) == 3
    assert all(is_phase_balanced(phases) for phases in classes)


def test_y_junction_permutations_preserve_phase_balance():
    phases = three_colour_phase_classes()[0]
    permutations = all_y_junction_permutations(phases)
    assert len(permutations) == 6
    assert all(is_phase_balanced(perm) for perm in permutations)


def test_y_junction_permutations_are_not_su3_derivation_by_themselves():
    phases = three_colour_phase_classes()[0]
    permutations = all_y_junction_permutations(phases)
    assert not discrete_permutation_group_is_su3_derivation(len(permutations))


def test_ssv_lepton_ladder_has_three_named_classes():
    assert tuple(lepton.name for lepton in SSV_LEPTON_CLASSES) == (
        "electron",
        "muon",
        "tau",
    )


def test_ssv_muon_is_mode_step_not_skeleton_step():
    skeletons = lepton_skeletons()
    assert skeletons[0] == skeletons[1] == "closed_torus"
    assert SSV_LEPTON_CLASSES[0].internal_mode is None
    assert SSV_LEPTON_CLASSES[1].internal_mode == "core_breathing_kelvin_hybrid"
    assert has_mode_only_generation_step()


def test_tau_is_topological_composite_step():
    tau = SSV_LEPTON_CLASSES[2]
    assert tau.skeleton == "hopf_linked_trefoils"
    assert tau.composite == "trefoil_pair"
    assert tau.internal_mode == "shared_muon_class_mode"

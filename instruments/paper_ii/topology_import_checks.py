"""Small algebraic checks for issue #29 topology-import claims.

These helpers are intentionally lightweight.  They encode the bookkeeping
claims from ``papers/SSV-II/topology-import-from-strand-model.md`` so the
paper note has executable guardrails:

- Schiller's ``e/3 per chiral crossing`` rule is a charge-count target.
- SSV's Y-junction phase balance gives three colour labels.
- Discrete Y-junction permutations are not, by themselves, a derivation of
  continuous local SU(3).
- The SSV lepton ladder currently mixes skeleton topology with internal modes.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from math import pi, tau
from typing import Iterable

import numpy as np


CHARGE_UNIT = 1.0 / 3.0


@dataclass(frozen=True)
class ProjectedCrossing:
    """One crossing in a projected oriented space curve."""

    first_segment: int
    second_segment: int
    sign: int
    over_segment: int


@dataclass(frozen=True)
class VortexLinkSample:
    """One oriented lattice plaquette pierced by a vortex line."""

    center: tuple[float, float, float]
    axis: str
    winding: int


@dataclass(frozen=True)
class StitchedVortexCurve:
    """Ordered curve reconstructed from compatible vortex-link samples."""

    axis: str
    winding: int
    points: tuple[tuple[float, float, float], ...]


@dataclass(frozen=True)
class VortexGraphNode:
    """Endpoint, junction, or representative node in a stitched vortex graph."""

    index: int
    point: tuple[float, float, float]
    degree: int
    kind: str


@dataclass(frozen=True)
class VortexGraphEdge:
    """Ordered polyline edge in a stitched vortex graph."""

    index: int
    points: tuple[tuple[float, float, float], ...]
    winding: int
    start_node: int | None = None
    end_node: int | None = None
    closed: bool = False


@dataclass(frozen=True)
class VortexGraph:
    """Conservative graph reconstruction from vortex-link samples."""

    nodes: tuple[VortexGraphNode, ...]
    edges: tuple[VortexGraphEdge, ...]
    dropped_samples: int = 0
    ambiguous_components: int = 0


@dataclass(frozen=True)
class ExtractionDiagnostic:
    """End-to-end status for field -> samples -> graph -> crossings."""

    label: str
    sample_count: int
    node_count: int
    edge_count: int
    closed_edges: int
    ambiguous_components: int
    dropped_samples: int
    crossing_signs: tuple[tuple[int, ...], ...]
    status: str


def charge_from_chiral_crossings(crossings: Iterable[int]) -> float:
    """Return electric charge in units of e from signed chiral crossings.

    The Schiller-side rule being tested in #29 is one signed outer crossing
    per e/3.  This helper is only bookkeeping; it does not decide which SSV
    defects possess which effective crossings.
    """

    return CHARGE_UNIT * sum(crossings)


def coordinate_grid(
    n: int,
    half_width: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, tuple[float, float, float]]:
    """Cell-centred Cartesian grid used by the synthetic field fixtures."""

    dx = 2.0 * half_width / n
    axis = (np.arange(n) + 0.5) * dx - half_width
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    origin = (-half_width + 0.5 * dx, -half_width + 0.5 * dx, -half_width + 0.5 * dx)
    return x, y, z, dx, origin


def synthetic_vortex_ring_field(
    *,
    n: int = 48,
    half_width: float = 6.0,
    radius: float = 2.0,
    z0: float = 0.0,
    circulation: int = 1,
    core_radius: float = 1.0,
) -> tuple[np.ndarray, float, tuple[float, float, float]]:
    """Synthetic closed torus/ring vortex field."""

    x, y, z, dx, origin = coordinate_grid(n, half_width)
    rho = np.sqrt(x * x + y * y)
    distance = np.sqrt((rho - radius) ** 2 + (z - z0) ** 2)
    theta = np.arctan2(z - z0, rho - radius)
    amp = np.tanh(distance / (np.sqrt(2.0) * core_radius))
    return (amp * np.exp(1j * circulation * theta)).astype(np.complex128), dx, origin


def synthetic_curve_vortex_field(
    curve: np.ndarray,
    *,
    n: int = 48,
    half_width: float = 6.0,
    core_radius: float = 1.0,
) -> tuple[np.ndarray, float, tuple[float, float, float]]:
    """Synthetic vortex field around a sampled closed curve.

    This mirrors the trefoil initial-state product ansatz: nearest curve point,
    local normal/binormal frame by finite differences, tanh core, and local
    azimuthal phase around the curve.
    """

    x, y, z, dx, origin = coordinate_grid(n, half_width)
    points = np.stack((x, y, z), axis=-1)
    curve = np.asarray(curve, dtype=float)
    tangent = np.gradient(curve, axis=0, edge_order=2)
    tangent = tangent / np.maximum(np.linalg.norm(tangent, axis=1, keepdims=True), 1e-12)
    radial_hint = curve.copy()
    radial_hint[:, 2] = 0.0
    radial_hint_norm = np.linalg.norm(radial_hint, axis=1, keepdims=True)
    fallback = np.tile(np.array([1.0, 0.0, 0.0]), (len(curve), 1))
    radial_hint = np.where(radial_hint_norm > 1e-12, radial_hint / np.maximum(radial_hint_norm, 1e-12), fallback)
    normal = radial_hint - np.sum(radial_hint * tangent, axis=1, keepdims=True) * tangent
    normal = normal / np.maximum(np.linalg.norm(normal, axis=1, keepdims=True), 1e-12)
    binormal = np.cross(tangent, normal)
    binormal = binormal / np.maximum(np.linalg.norm(binormal, axis=1, keepdims=True), 1e-12)

    offsets = points[None, ...] - curve[:, None, None, None, :]
    nearest = np.argmin(np.sum(offsets * offsets, axis=-1), axis=0)
    nearest_offset = points - curve[nearest]
    radial_n = np.sum(nearest_offset * normal[nearest], axis=-1)
    radial_b = np.sum(nearest_offset * binormal[nearest], axis=-1)
    distance = np.sqrt(radial_n * radial_n + radial_b * radial_b)
    theta = np.arctan2(radial_b, radial_n)
    amp = np.tanh(distance / (np.sqrt(2.0) * core_radius))
    return (amp * np.exp(1j * theta)).astype(np.complex128), dx, origin


def _wrap_phase(dphi: np.ndarray) -> np.ndarray:
    """Wrap phase differences to (-pi, pi]."""

    return (dphi + np.pi) % (2.0 * np.pi) - np.pi


def extract_vortex_link_samples(
    psi: np.ndarray,
    *,
    dx: float = 1.0,
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
    threshold: float = np.pi,
) -> tuple[VortexLinkSample, ...]:
    """Extract oriented vortex-link samples from a 3D complex field.

    Each returned sample corresponds to one plaquette with phase circulation
    above ``threshold``.  The sample center is the plaquette center in physical
    coordinates, and ``axis`` is the approximate vortex tangent direction
    normal to that plaquette.

    This is a field-to-skeleton bridge, not a full curve stitcher.  It gives
    the point cloud that a later curve-reconstruction pass can order into
    continuous vortex filaments.
    """

    field = np.asarray(psi)
    if field.ndim != 3:
        raise ValueError("psi must be a 3D complex field")

    phi = np.angle(field)
    dphi_dx = _wrap_phase(np.diff(phi, axis=0))
    dphi_dy = _wrap_phase(np.diff(phi, axis=1))
    dphi_dz = _wrap_phase(np.diff(phi, axis=2))

    wz = dphi_dx[:, :-1, :] + dphi_dy[1:, :, :] - dphi_dx[:, 1:, :] - dphi_dy[:-1, :, :]
    wy = dphi_dx[:, :, :-1] + dphi_dz[1:, :, :] - dphi_dx[:, :, 1:] - dphi_dz[:-1, :, :]
    wx = dphi_dy[:, :, :-1] + dphi_dz[:, 1:, :] - dphi_dy[:, :, 1:] - dphi_dz[:, :-1, :]

    ox, oy, oz = origin
    samples: list[VortexLinkSample] = []

    for i, j, k in np.argwhere(np.abs(wz) > threshold):
        samples.append(
            VortexLinkSample(
                center=(ox + (i + 0.5) * dx, oy + (j + 0.5) * dx, oz + k * dx),
                axis="z",
                winding=int(np.sign(wz[i, j, k])),
            )
        )

    for i, j, k in np.argwhere(np.abs(wy) > threshold):
        samples.append(
            VortexLinkSample(
                center=(ox + (i + 0.5) * dx, oy + j * dx, oz + (k + 0.5) * dx),
                axis="y",
                winding=int(np.sign(wy[i, j, k])),
            )
        )

    for i, j, k in np.argwhere(np.abs(wx) > threshold):
        samples.append(
            VortexLinkSample(
                center=(ox + i * dx, oy + (j + 0.5) * dx, oz + (k + 0.5) * dx),
                axis="x",
                winding=int(np.sign(wx[i, j, k])),
            )
        )

    return tuple(samples)


def stitch_axis_aligned_vortex_curves(
    samples: Iterable[VortexLinkSample],
    *,
    tolerance: float = 1e-9,
) -> tuple[StitchedVortexCurve, ...]:
    """Stitch simple axis-aligned vortex-link samples into ordered curves.

    This first-pass stitcher is intentionally conservative: it groups samples
    only when they share axis, winding, and transverse coordinates.  It handles
    straight extracted vortex fixtures and leaves curved knots / Y-junctions to
    a later graph-based stitcher.
    """

    grouped: dict[tuple[str, int, int, int], list[VortexLinkSample]] = {}
    axis_index = {"x": 0, "y": 1, "z": 2}

    for sample in samples:
        if sample.axis not in axis_index:
            raise ValueError(f"unknown vortex-link axis {sample.axis!r}")
        longitudinal = axis_index[sample.axis]
        transverse = [idx for idx in range(3) if idx != longitudinal]
        key = (
            sample.axis,
            sample.winding,
            round(sample.center[transverse[0]] / tolerance),
            round(sample.center[transverse[1]] / tolerance),
        )
        grouped.setdefault(key, []).append(sample)

    curves: list[StitchedVortexCurve] = []
    for (axis, winding, _t0, _t1), group in grouped.items():
        longitudinal = axis_index[axis]
        ordered = tuple(
            sample.center
            for sample in sorted(group, key=lambda item: item.center[longitudinal])
        )
        curves.append(StitchedVortexCurve(axis=axis, winding=winding, points=ordered))

    return tuple(sorted(curves, key=lambda curve: (curve.axis, curve.winding, curve.points[0])))


def _point_array(samples: tuple[VortexLinkSample, ...]) -> np.ndarray:
    return np.asarray([sample.center for sample in samples], dtype=float)


def build_vortex_sample_adjacency(
    samples: Iterable[VortexLinkSample],
    *,
    max_distance: float,
    require_same_winding: bool = True,
) -> dict[int, set[int]]:
    """Build an undirected neighbor graph between nearby vortex samples."""

    sample_tuple = tuple(samples)
    points = _point_array(sample_tuple)
    adjacency = {idx: set() for idx in range(len(sample_tuple))}

    for i in range(len(sample_tuple)):
        for j in range(i + 1, len(sample_tuple)):
            if require_same_winding and sample_tuple[i].winding != sample_tuple[j].winding:
                continue
            if float(np.linalg.norm(points[i] - points[j])) <= max_distance:
                adjacency[i].add(j)
                adjacency[j].add(i)
    return adjacency


def _dual_edge_endpoints(
    sample: VortexLinkSample,
    *,
    dx: float,
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    center = np.asarray(sample.center, dtype=float)
    half_step = 0.5 * dx
    if sample.axis == "x":
        delta = np.array([half_step, 0.0, 0.0])
    elif sample.axis == "y":
        delta = np.array([0.0, half_step, 0.0])
    elif sample.axis == "z":
        delta = np.array([0.0, 0.0, half_step])
    else:
        raise ValueError(f"unknown vortex-link axis {sample.axis!r}")
    return tuple(center - delta), tuple(center + delta)


def build_vortex_dual_adjacency(
    samples: Iterable[VortexLinkSample],
    *,
    dx: float,
    require_same_winding: bool = False,
    tolerance: float = 1e-6,
) -> dict[int, set[int]]:
    """Build adjacency by joining dual-lattice vortex edges at endpoints.

    A winding plaquette is dual to a short vortex-line edge normal to that
    plaquette.  For generated curved fields this is a better skeleton graph
    than raw Euclidean proximity: it follows the lattice line through shared
    dual vertices and avoids shortcut edges across nearby strands.
    """

    sample_tuple = tuple(samples)
    adjacency = {idx: set() for idx in range(len(sample_tuple))}
    scale = 1.0 / max(dx * tolerance, 1e-15)
    vertex_to_samples: dict[tuple[int, int, int], list[int]] = {}

    for idx, sample in enumerate(sample_tuple):
        for endpoint in _dual_edge_endpoints(sample, dx=dx):
            key = tuple(int(round(value * scale)) for value in endpoint)
            vertex_to_samples.setdefault(key, []).append(idx)

    for incident in vertex_to_samples.values():
        for pos, first in enumerate(incident):
            for second in incident[pos + 1:]:
                if require_same_winding and sample_tuple[first].winding != sample_tuple[second].winding:
                    continue
                adjacency[first].add(second)
                adjacency[second].add(first)
    return adjacency


def _connected_components(adjacency: dict[int, set[int]]) -> list[set[int]]:
    unseen = set(adjacency)
    components: list[set[int]] = []
    while unseen:
        root = unseen.pop()
        component = {root}
        stack = [root]
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        components.append(component)
    return components


def _classify_node_kind(degree: int) -> str:
    if degree <= 0:
        return "isolated"
    if degree == 1:
        return "endpoint"
    if degree == 2:
        return "interior"
    if degree == 3:
        return "junction"
    return "ambiguous"


def _order_open_chain(component: set[int], adjacency: dict[int, set[int]], start: int) -> list[int]:
    ordered = [start]
    previous: int | None = None
    current = start
    while True:
        candidates = [idx for idx in adjacency[current] if idx in component and idx != previous]
        if not candidates:
            return ordered
        if len(candidates) > 1 and previous is not None:
            return ordered
        next_idx = candidates[0]
        ordered.append(next_idx)
        previous, current = current, next_idx


def _order_closed_loop(component: set[int], adjacency: dict[int, set[int]]) -> list[int]:
    start = min(component)
    neighbors = sorted(adjacency[start])
    if len(neighbors) != 2:
        return [start]

    ordered = [start, neighbors[0]]
    previous, current = start, neighbors[0]
    while current != start:
        candidates = [idx for idx in sorted(adjacency[current]) if idx != previous]
        if not candidates:
            break
        next_idx = candidates[0]
        if next_idx == start:
            break
        if next_idx in ordered:
            break
        ordered.append(next_idx)
        previous, current = current, next_idx
    return ordered


def stitch_vortex_graph(
    samples: Iterable[VortexLinkSample],
    *,
    max_distance: float = 1.1,
    min_edge_samples: int = 2,
    require_same_winding: bool = True,
) -> VortexGraph:
    """Stitch vortex-link samples into a conservative graph representation.

    This graph stitcher handles clean synthetic components:
    - open chains with two degree-1 endpoints;
    - closed loops where all samples have degree 2;
    - one trivalent Y component with one degree-3 junction and three endpoints.

    More complicated components are preserved as ambiguous diagnostics rather
    than forced into a possibly false topology.
    """

    sample_tuple = tuple(samples)
    adjacency = build_vortex_sample_adjacency(
        sample_tuple,
        max_distance=max_distance,
        require_same_winding=require_same_winding,
    )
    return _stitch_vortex_graph_from_adjacency(
        sample_tuple,
        adjacency,
        min_edge_samples=min_edge_samples,
    )


def stitch_vortex_graph_dual_lattice(
    samples: Iterable[VortexLinkSample],
    *,
    dx: float,
    min_edge_samples: int = 2,
    min_component_samples: int = 2,
    keep_largest_component: bool = False,
    require_same_winding: bool = False,
) -> VortexGraph:
    """Stitch generated-field samples using their dual-lattice connectivity."""

    sample_tuple = tuple(samples)
    adjacency = build_vortex_dual_adjacency(
        sample_tuple,
        dx=dx,
        require_same_winding=require_same_winding,
    )
    return _stitch_vortex_graph_from_adjacency(
        sample_tuple,
        adjacency,
        min_edge_samples=min_edge_samples,
        min_component_samples=min_component_samples,
        keep_largest_component=keep_largest_component,
    )


def _stitch_vortex_graph_from_adjacency(
    sample_tuple: tuple[VortexLinkSample, ...],
    adjacency: dict[int, set[int]],
    *,
    min_edge_samples: int,
    min_component_samples: int = 2,
    keep_largest_component: bool = False,
) -> VortexGraph:
    """Shared conservative graph stitching once adjacency has been chosen."""

    if not sample_tuple:
        return VortexGraph(nodes=(), edges=())

    components = _connected_components(adjacency)
    if keep_largest_component and components:
        largest = max(components, key=len)
        ignored = sum(len(component) for component in components if component is not largest)
        components = [largest]
    else:
        ignored = 0

    points = _point_array(sample_tuple)

    nodes: list[VortexGraphNode] = []
    edges: list[VortexGraphEdge] = []
    dropped = ignored
    ambiguous = 0

    def add_node(sample_idx: int, kind: str | None = None) -> int:
        node_id = len(nodes)
        degree = len(adjacency[sample_idx])
        nodes.append(
            VortexGraphNode(
                index=node_id,
                point=sample_tuple[sample_idx].center,
                degree=degree,
                kind=kind or _classify_node_kind(degree),
            )
        )
        return node_id

    def add_node_from_point(
        point: tuple[float, float, float],
        *,
        degree: int,
        kind: str,
    ) -> int:
        node_id = len(nodes)
        nodes.append(
            VortexGraphNode(
                index=node_id,
                point=point,
                degree=degree,
                kind=kind,
            )
        )
        return node_id

    for component in components:
        degrees = {idx: len(adjacency[idx] & component) for idx in component}
        endpoints = sorted(idx for idx, degree in degrees.items() if degree == 1)
        junctions = sorted(idx for idx, degree in degrees.items() if degree >= 3)

        if (
            len(component) < min_edge_samples
            or len(component) < min_component_samples
            or all(degree == 0 for degree in degrees.values())
        ):
            dropped += len(component)
            continue

        if len(endpoints) == 2 and not junctions:
            ordered = _order_open_chain(component, adjacency, endpoints[0])
            if len(ordered) < min_edge_samples:
                dropped += len(component)
                continue
            start_node = add_node(ordered[0], "endpoint")
            end_node = add_node(ordered[-1], "endpoint")
            winding = int(np.sign(sum(sample_tuple[idx].winding for idx in ordered)))
            edges.append(
                VortexGraphEdge(
                    index=len(edges),
                    points=tuple(tuple(points[idx]) for idx in ordered),
                    winding=winding,
                    start_node=start_node,
                    end_node=end_node,
                    closed=False,
                )
            )
            continue

        if not endpoints and not junctions and all(degree == 2 for degree in degrees.values()):
            ordered = _order_closed_loop(component, adjacency)
            if len(ordered) < min_edge_samples:
                dropped += len(component)
                continue
            winding = int(np.sign(sum(sample_tuple[idx].winding for idx in ordered)))
            edges.append(
                VortexGraphEdge(
                    index=len(edges),
                    points=tuple(tuple(points[idx]) for idx in ordered),
                    winding=winding,
                    closed=True,
                )
            )
            continue

        if len(junctions) == 1 and len(endpoints) == 3:
            junction = junctions[0]
            junction_node = add_node(junction, "junction")
            for endpoint in endpoints:
                ordered = _order_open_chain(component, adjacency, endpoint)
                if ordered[-1] != junction:
                    ordered.append(junction)
                if len(ordered) < min_edge_samples:
                    continue
                endpoint_node = add_node(endpoint, "endpoint")
                winding = int(np.sign(sum(sample_tuple[idx].winding for idx in ordered)))
                edges.append(
                    VortexGraphEdge(
                        index=len(edges),
                        points=tuple(tuple(points[idx]) for idx in ordered),
                        winding=winding,
                        start_node=endpoint_node,
                        end_node=junction_node,
                        closed=False,
                    )
                )
            continue

        if len(junctions) > 1 and len(endpoints) == 3:
            junction_set = set(junctions)
            junction_adjacency = {
                idx: adjacency[idx] & junction_set
                for idx in junction_set
            }
            if len(_connected_components(junction_adjacency)) != 1:
                ambiguous += 1
                continue

            junction_point_array = points[junctions]
            junction_point = tuple(np.mean(junction_point_array, axis=0))
            junction_node = add_node_from_point(
                junction_point,
                degree=3,
                kind="junction",
            )
            extracted_edges = 0
            for endpoint in endpoints:
                ordered = [endpoint]
                previous: int | None = None
                current = endpoint
                while current not in junction_set:
                    candidates = [
                        idx
                        for idx in adjacency[current] & component
                        if idx != previous
                    ]
                    if len(candidates) != 1:
                        ordered = []
                        break
                    next_idx = candidates[0]
                    ordered.append(next_idx)
                    previous, current = current, next_idx
                if len(ordered) < min_edge_samples:
                    continue
                endpoint_node = add_node(endpoint, "endpoint")
                winding = int(np.sign(sum(sample_tuple[idx].winding for idx in ordered)))
                edge_points = [tuple(points[idx]) for idx in ordered]
                edge_points.append(junction_point)
                edges.append(
                    VortexGraphEdge(
                        index=len(edges),
                        points=tuple(edge_points),
                        winding=winding,
                        start_node=endpoint_node,
                        end_node=junction_node,
                        closed=False,
                    )
                )
                extracted_edges += 1
            if extracted_edges == 3:
                continue

            ambiguous += 1
            continue

        ambiguous += 1

    return VortexGraph(
        nodes=tuple(nodes),
        edges=tuple(edges),
        dropped_samples=dropped,
        ambiguous_components=ambiguous,
    )


def graph_edge_crossing_numbers(graph: VortexGraph, edge_index: int = 0, **kwargs: object) -> tuple[int, ...]:
    """Return projected crossing signs for one stitched graph edge."""

    edge = graph.edges[edge_index]
    return signed_crossing_numbers(np.asarray(edge.points, dtype=float), **kwargs)


def smooth_closed_curve(
    curve: np.ndarray,
    *,
    window: int = 2,
    iterations: int = 2,
) -> np.ndarray:
    """Cyclic moving-average smoothing for lattice-extracted closed curves."""

    points = np.asarray(curve, dtype=float)
    if window <= 0 or iterations <= 0 or len(points) < 3:
        return points.copy()

    smoothed = points.copy()
    for _ in range(iterations):
        accumulator = np.zeros_like(smoothed)
        for shift in range(-window, window + 1):
            accumulator += np.roll(smoothed, shift, axis=0)
        smoothed = accumulator / float(2 * window + 1)
    return smoothed


def extraction_diagnostic(
    label: str,
    psi: np.ndarray,
    *,
    dx: float,
    origin: tuple[float, float, float],
    max_distance: float,
    require_same_winding: bool = True,
    stitching: str = "distance",
    min_component_samples: int = 2,
    keep_largest_component: bool = False,
    crossing_smooth_window: int = 0,
    crossing_smooth_iterations: int = 0,
) -> ExtractionDiagnostic:
    """Run the current extraction stack on one complex field."""

    samples = extract_vortex_link_samples(psi, dx=dx, origin=origin)
    if stitching == "distance":
        graph = stitch_vortex_graph(
            samples,
            max_distance=max_distance,
            require_same_winding=require_same_winding,
        )
    elif stitching == "dual":
        graph = stitch_vortex_graph_dual_lattice(
            samples,
            dx=dx,
            require_same_winding=require_same_winding,
            min_component_samples=min_component_samples,
            keep_largest_component=keep_largest_component,
        )
    else:
        raise ValueError(f"unknown stitching mode {stitching!r}")

    crossing_signs = tuple(
        signed_crossing_numbers(
            smooth_closed_curve(
                np.asarray(edge.points, dtype=float),
                window=crossing_smooth_window,
                iterations=crossing_smooth_iterations,
            )
        )
        for edge in graph.edges
        if edge.closed and len(edge.points) >= 4
    )
    if graph.ambiguous_components:
        status = "ambiguous"
    elif not graph.edges:
        status = "no_edges"
    else:
        status = "ok"
    return ExtractionDiagnostic(
        label=label,
        sample_count=len(samples),
        node_count=len(graph.nodes),
        edge_count=len(graph.edges),
        closed_edges=sum(1 for edge in graph.edges if edge.closed),
        ambiguous_components=graph.ambiguous_components,
        dropped_samples=graph.dropped_samples,
        crossing_signs=crossing_signs,
        status=status,
    )


def standard_trefoil_curve(samples: int = 300) -> np.ndarray:
    """Return a standard right/left-handed trefoil fixture.

    This is a synthetic calibration curve for the projected crossing counter,
    not the relaxed SSV proton curve.  Its xy projection has three crossings
    with the same sign.
    """

    t = np.linspace(0.0, tau, samples, endpoint=False)
    return np.stack(
        (
            np.sin(t) + 2.0 * np.sin(2.0 * t),
            np.cos(t) - 2.0 * np.cos(2.0 * t),
            -np.sin(3.0 * t),
        ),
        axis=1,
    )


def circular_core_curve(samples: int = 300) -> np.ndarray:
    """Return a planar circle, the zero-crossing skeleton fixture."""

    t = np.linspace(0.0, tau, samples, endpoint=False)
    return np.stack((np.cos(t), np.sin(t), np.zeros_like(t)), axis=1)


def framed_torus_ribbon_curves(
    *,
    twist: int,
    samples: int = 600,
    radius: float = 2.0,
    tube_radius: float = 0.25,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a torus core curve and a nearby framed ribbon edge.

    The second curve is displaced in a rotating normal frame around the
    circular core.  Its Gauss linking number with the core is the integer
    framing diagnostic used for the R1/twist bookkeeping tests.
    """

    t = np.linspace(0.0, tau, samples, endpoint=False)
    core = np.stack(
        (
            radius * np.cos(t),
            radius * np.sin(t),
            np.zeros_like(t),
        ),
        axis=1,
    )
    radial = np.stack((np.cos(t), np.sin(t), np.zeros_like(t)), axis=1)
    vertical = np.stack((np.zeros_like(t), np.zeros_like(t), np.ones_like(t)), axis=1)
    framed = core + tube_radius * (
        np.cos(twist * t)[:, None] * radial
        + np.sin(twist * t)[:, None] * vertical
    )
    return core, framed


def gauss_linking_number(curve_a: np.ndarray, curve_b: np.ndarray) -> float:
    """Approximate the Gauss linking integral for two closed polygonal curves."""

    a = np.asarray(curve_a, dtype=float)
    b = np.asarray(curve_b, dtype=float)
    if a.ndim != 2 or b.ndim != 2 or a.shape[1] < 3 or b.shape[1] < 3:
        raise ValueError("curves must have shape (N, >=3)")
    if len(a) < 3 or len(b) < 3:
        raise ValueError("closed linking curves need at least three samples")

    delta_a = np.roll(a, -1, axis=0) - a
    delta_b = np.roll(b, -1, axis=0) - b
    midpoint_a = 0.5 * (a + np.roll(a, -1, axis=0))
    midpoint_b = 0.5 * (b + np.roll(b, -1, axis=0))

    total = 0.0
    for idx in range(len(a)):
        separation = midpoint_a[idx] - midpoint_b
        distance_cubed = np.linalg.norm(separation, axis=1) ** 3
        numerator = np.einsum(
            "ij,ij->i",
            np.cross(delta_a[idx], delta_b),
            separation,
        )
        total += float(np.sum(numerator / distance_cubed))
    return total / (4.0 * pi)


def rounded_linking_number(
    curve_a: np.ndarray,
    curve_b: np.ndarray,
    *,
    tolerance: float = 5e-3,
) -> int:
    """Return an integer linking number when the quadrature is near one."""

    value = gauss_linking_number(curve_a, curve_b)
    rounded = round(value)
    if abs(value - rounded) > tolerance:
        raise ValueError(f"linking estimate {value:.6g} is not near an integer")
    return int(rounded)


def _cross2(a: np.ndarray, b: np.ndarray) -> float:
    return float(a[0] * b[1] - a[1] * b[0])


def _segment_intersection_parameters(
    p0: np.ndarray,
    p1: np.ndarray,
    q0: np.ndarray,
    q1: np.ndarray,
    *,
    tolerance: float,
) -> tuple[float, float] | None:
    """Return interior-intersection parameters for two projected segments."""

    r = p1 - p0
    s = q1 - q0
    denominator = _cross2(r, s)
    if abs(denominator) <= tolerance:
        return None

    qp = q0 - p0
    u = _cross2(qp, r) / denominator
    t = _cross2(qp, s) / denominator
    if tolerance < t < 1.0 - tolerance and tolerance < u < 1.0 - tolerance:
        return t, u
    return None


def projected_crossings(
    curve: np.ndarray,
    *,
    projection_axes: tuple[int, int] = (0, 1),
    height_axis: int = 2,
    closed: bool = True,
    adjacent_skip: int = 2,
    tolerance: float = 1e-9,
) -> tuple[ProjectedCrossing, ...]:
    """Count signed crossings in a generic projection of a polygonal curve.

    The sign convention is the projected tangent orientation multiplied by
    the over/under height sign.  This is sufficient for the #29 synthetic
    chirality tests; field-extracted SSV defects will need a separate curve
    extraction stage before using this counter.
    """

    points = np.asarray(curve, dtype=float)
    if points.ndim != 2 or points.shape[1] < 3:
        raise ValueError("curve must be an array with shape (N, >=3)")
    if len(points) < 4:
        return ()

    n_points = len(points)
    n_segments = n_points if closed else n_points - 1
    xy = points[:, projection_axes]
    z = points[:, height_axis]
    crossings: list[ProjectedCrossing] = []

    for i in range(n_segments):
        i_next = (i + 1) % n_points
        for j in range(i + 1, n_segments):
            j_next = (j + 1) % n_points
            separation = abs(i - j)
            if separation <= adjacent_skip:
                continue
            if closed and separation >= n_segments - adjacent_skip:
                continue

            params = _segment_intersection_parameters(
                xy[i],
                xy[i_next],
                xy[j],
                xy[j_next],
                tolerance=tolerance,
            )
            if params is None:
                continue

            t, u = params
            z_i = (1.0 - t) * z[i] + t * z[i_next]
            z_j = (1.0 - u) * z[j] + u * z[j_next]
            if abs(z_i - z_j) <= tolerance:
                continue

            tangent_i = xy[i_next] - xy[i]
            tangent_j = xy[j_next] - xy[j]
            orientation = np.sign(_cross2(tangent_i, tangent_j))
            over_under = np.sign(z_i - z_j)
            sign = int(orientation * over_under)
            over_segment = i if z_i > z_j else j
            crossings.append(
                ProjectedCrossing(
                    first_segment=i,
                    second_segment=j,
                    sign=sign,
                    over_segment=over_segment,
                )
            )

    return tuple(crossings)


def signed_crossing_numbers(curve: np.ndarray, **kwargs: object) -> tuple[int, ...]:
    """Return only the signed crossing numbers for a projected curve."""

    return tuple(crossing.sign for crossing in projected_crossings(curve, **kwargs))


def three_colour_phase_classes() -> tuple[tuple[float, float, float], ...]:
    """Canonical SSV Y-junction phase-balanced colour classes.

    The three classes are cyclic rotations of phases separated by 2pi/3.
    Each row satisfies theta_1 + theta_2 + theta_3 = 0 mod 2pi.
    """

    base = (0.0, tau / 3.0, 2.0 * tau / 3.0)
    return (
        base,
        (base[1], base[2], base[0]),
        (base[2], base[0], base[1]),
    )


def is_phase_balanced(phases: Iterable[float], *, tolerance: float = 1e-12) -> bool:
    """Check the Y-junction balance condition sum(theta_i) = 0 mod 2pi."""

    phase_sum = sum(phases) % tau
    return min(phase_sum, tau - phase_sum) < tolerance


def all_y_junction_permutations(phases: tuple[float, float, float]) -> set[tuple[float, float, float]]:
    """All distinct permutations of a trivalent phase assignment."""

    return set(permutations(phases, 3))


@dataclass(frozen=True)
class LeptonClass:
    """SSV charged-lepton class for the generation audit."""

    name: str
    skeleton: str
    internal_mode: str | None = None
    composite: str | None = None


SSV_LEPTON_CLASSES = (
    LeptonClass(name="electron", skeleton="closed_torus"),
    LeptonClass(
        name="muon",
        skeleton="closed_torus",
        internal_mode="core_breathing_kelvin_hybrid",
    ),
    LeptonClass(
        name="tau",
        skeleton="hopf_linked_trefoils",
        internal_mode="shared_muon_class_mode",
        composite="trefoil_pair",
    ),
)


def lepton_skeletons(classes: Iterable[LeptonClass] = SSV_LEPTON_CLASSES) -> tuple[str, ...]:
    """Return the skeleton labels of the SSV lepton classes."""

    return tuple(lepton.skeleton for lepton in classes)


def has_mode_only_generation_step(classes: Iterable[LeptonClass] = SSV_LEPTON_CLASSES) -> bool:
    """True when at least one generation step changes mode without changing skeleton."""

    by_skeleton: dict[str, set[str | None]] = {}
    for lepton in classes:
        by_skeleton.setdefault(lepton.skeleton, set()).add(lepton.internal_mode)
    return any(len(modes) > 1 for modes in by_skeleton.values())


def discrete_permutation_group_is_su3_derivation(permutation_count: int) -> bool:
    """Return whether a finite permutation count can by itself derive SU(3).

    This intentionally returns False for all finite permutation groups.  It is
    a guard against accidentally promoting the Y-junction's three labels or six
    permutations to a continuous eight-generator local SU(3) derivation.
    """

    _ = permutation_count
    return False

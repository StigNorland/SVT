"""Tests for the C4 global-state/local-causality screen formulation."""

import os
import sys

import pytest

SRC = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "model_hssv"
)
sys.path.insert(0, os.path.abspath(SRC))

import quantum_causal_screen_audit as audit  # noqa: E402


def test_causal_network_has_no_superluminal_edges():
    result = audit.causal_edge_audit()
    assert result["all_edges_causal"]
    assert result["maximum_speed"] <= 1.0
    assert result["global_state_is_not_a_signal"]


def test_local_operation_changes_correlation_not_remote_marginal():
    result = audit.no_signaling_audit()
    assert result["remote_unchanged"]
    assert result["global_correlation_changed"]
    assert result["zz_before"] == pytest.approx(1.0)
    assert result["zz_after"] == pytest.approx(-1.0)


def test_spacelike_gate_order_is_foliation_independent():
    result = audit.foliation_independence_audit()
    assert result["spacelike_gates_commute"]
    assert result["orders_match"]
    assert result["commutator_norm"] <= audit.TOL
    assert not result["preferred_linear_extension_required"]


def test_swap_write_closes_componentwise_four_momentum_ledger():
    result = audit.momentum_ledger_audit()
    assert result["swap_is_unitary"]
    assert result["four_momentum_conserved"]
    assert result["bilateral_transfer_closes"]
    assert result["occupation_before"] == {"matter": 1.0, "screen": 0.0}
    assert result["occupation_after"] == {"matter": 0.0, "screen": 1.0}


def test_reduced_memory_is_bounded_while_global_information_is_conserved():
    result = audit.reduced_state_memory_audit()
    assert result["gate_is_unitary"]
    assert result["gate_commutes_with_energy"]
    assert result["global_information_conserved"]
    assert result["reduced_entropy_bounded"]
    assert result["reduced_entropy_after"] == pytest.approx(
        result["one_cell_capacity_nats"]
    )


def test_positive_record_load_cannot_be_phase_cancelled():
    result = audit.phase_positive_load_audit()
    assert result["positive"]
    assert result["phase_independent"]
    assert result["plus_phase_load"] == pytest.approx(1.0)
    assert result["minus_phase_load"] == pytest.approx(1.0)
    assert result["universal_response"].startswith("A = 1 - q")


def test_topological_site_and_particles_share_bilateral_update_capacity():
    result = audit.bilateral_update_capacity_audit()
    assert result["bilateral_counts_match"]
    assert result["particle_caps_respected"]
    assert result["site_cap_respected"]
    assert result["availability_bounded"]
    assert result["below_capacity_is_additive"]
    assert result["above_capacity_saturates"]
    assert result["particle_ledger_total"] == pytest.approx(
        result["screen_ledger_total"]
    )


@pytest.mark.parametrize(
    "requests,capacity",
    [({"p": -1.0}, 1.0), ({"p": 1.0}, 0.0)],
)
def test_capacity_allocator_rejects_unphysical_inputs(requests, capacity):
    with pytest.raises(ValueError):
        audit.allocate_shared_site(requests, capacity)


def test_repeated_isolated_drive_is_bounded_not_secular():
    result = audit.repeated_drive_bound_audit()
    assert result["load_bounded_by_one_cell"]
    assert result["entropy_bounded_by_one_cell"]
    assert not result["secular_growth"]
    assert result["minimum_load"] == pytest.approx(0.0)
    assert result["maximum_load"] == pytest.approx(1.0)


def test_repeated_drive_requires_positive_cycle_count():
    with pytest.raises(ValueError):
        audit.repeated_drive_bound_audit(cycles=0)


def test_c4_survives_all_six_foundation_gates():
    report = audit.run()
    assert report["status"] == "PASS"
    assert report["survives_all_six_gates"]
    assert set(report["gates"]) == {"F1", "F2", "F3", "F4", "F5", "F6"}
    assert all(status.startswith("PASS") for status in report["gates"].values())

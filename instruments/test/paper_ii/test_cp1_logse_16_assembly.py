"""Regression tests for #80 Pass 5: assembling SSV labels into the SO(10) 16."""

from math import comb

from cp1_logse_16_assembly import (
    FIELD_BY_SECTOR,
    anomaly_sums,
    bL_equals_colour_trace,
    binomial_multiplicity,
    b_minus_L,
    colour_minus,
    electric_charge,
    even_parity_weights,
    field_of,
    hypercharge_Y,
    multiplicity_table,
    odd_parity_weights,
    parity_is_correlated,
    ssv_bit_inventory,
    weak_T3,
    weak_minus,
)


def test_weight_counts():
    assert len(even_parity_weights()) == 16
    assert len(odd_parity_weights()) == 16
    assert len(even_parity_weights()) + len(odd_parity_weights()) == 32


def test_multiplicities_match_one_generation():
    assert multiplicity_table() == {"Q": 6, "u^c": 3, "d^c": 3, "L": 2, "e^c": 1, "nu^c": 1}
    assert sum(multiplicity_table().values()) == 16


def test_multiplicities_are_binomial():
    mult = multiplicity_table()
    for (nc, nw), field in FIELD_BY_SECTOR.items():
        assert mult[field] == binomial_multiplicity(nc, nw) == comb(3, nc) * comb(2, nw)


def test_charges_match_standard_branching():
    # spot-check each field's (T3, Y, B-L, Q) against the known SM values
    expected = {
        "nu^c": (0.0, 0.0, +1.0, 0.0),
        "u^c":  (0.0, -2 / 3, -1 / 3, -2 / 3),
        "e^c":  (0.0, +1.0, +1.0, +1.0),
        "d^c":  (0.0, +1 / 3, -1 / 3, +1 / 3),
    }
    seen = {}
    for w in even_parity_weights():
        f = field_of(w)
        if f in expected and f not in seen and abs(weak_T3(w)) < 1e-9:
            seen[f] = (weak_T3(w), hypercharge_Y(w), b_minus_L(w), electric_charge(w))
    for f, vals in expected.items():
        for got, exp in zip(seen[f], vals):
            assert abs(got - exp) < 1e-12, f"{f}: {seen[f]} != {vals}"


def test_doublets_have_half_integer_T3():
    # Q and L are weak doublets: members carry T3 = +/-1/2; singlets have T3 = 0
    for w in even_parity_weights():
        if field_of(w) in ("Q", "L"):
            assert abs(abs(weak_T3(w)) - 0.5) < 1e-12   # (w1-w2)/4 = +/-1/2
        else:
            assert abs(weak_T3(w)) < 1e-12              # u^c,d^c,e^c,nu^c are weak singlets


def test_all_anomalies_cancel():
    for name, val in anomaly_sums().items():
        assert abs(val) < 1e-12, f"{name} = {val}"


def test_b_minus_L_is_colour_trace():
    # the decisive Pati-Salam fact: B-L is not independent, it is the 4th colour
    assert bL_equals_colour_trace()


def test_b_minus_L_separates_quarks_and_leptons():
    for w in even_parity_weights():
        coloured = colour_minus(w) in (1, 2)
        if coloured:
            assert abs(abs(b_minus_L(w)) - 1 / 3) < 1e-12
        else:
            assert abs(abs(b_minus_L(w)) - 1.0) < 1e-12


def test_chirality_requires_parity_correlation():
    # the obstruction: the 16 ties colour-parity to weak-parity
    checks = parity_is_correlated()
    assert all(checks.values())
    # explicit: every 16 weight has colour-parity == weak-parity
    for w in even_parity_weights():
        assert (w[0] * w[1] * w[2]) == (w[3] * w[4])
    # every 16bar weight has them opposite
    for w in odd_parity_weights():
        assert (w[0] * w[1] * w[2]) == -(w[3] * w[4])


def test_ssv_inventory_flags_the_two_demands():
    inv = ssv_bit_inventory()
    statuses = [b.status for b in inv]
    assert "NEEDS-ENLARGEMENT" in statuses   # B-L = 4th colour -> SU(4)
    assert "NOT-FORCED" in statuses          # parity link -> chirality
    assert statuses.count("PRESENT") == 1    # only the SU(3) rank-2 colour
    assert len(inv) == 5

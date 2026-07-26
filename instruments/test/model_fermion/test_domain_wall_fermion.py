"""Tests for #176 No-go map (III) -- the domain-wall chiral zero mode (H-SSV).

Validates the mechanism:
  (i)   kink+antikink -> exactly two near-zero modes, one per wall;
  (ii)  the two carry OPPOSITE chirality (the doubling, spatially separated);
  (iii) the modes are localized at the walls and the bulk is gapped;
  (iv)  a single open wall -> wall mode + partner EXILED to the boundary;
  (v)   the run-level verdict (chirality survives on the wall) holds.
"""

import os
import sys

import numpy as np

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "model_fermion")
sys.path.insert(0, os.path.abspath(SRC))

import domain_wall_fermion as d  # noqa: E402


def test_two_zero_modes_one_per_wall():
    rep = d.run(N=120, w=3.0)
    pair = rep["kink_antikink_modes"]
    assert len(pair) == 2
    assert all(abs(p["E"]) < 1e-8 for p in pair)          # zero energy
    assert abs(pair[0]["center"] - 30) < 4 and abs(pair[1]["center"] - 90) < 4


def test_opposite_chirality_at_walls():
    rep = d.run(N=120, w=3.0)
    p = rep["kink_antikink_modes"]
    assert p[0]["chirality"] * p[1]["chirality"] < 0      # opposite
    assert min(abs(p[0]["chirality"]), abs(p[1]["chirality"])) > 0.9


def test_localized_and_gapped():
    rep = d.run(N=120, w=3.0)
    assert rep["modes_localized"] is True
    assert rep["bulk_gap"] > 0.3                          # bulk is gapped


def test_single_wall_partner_exiled_to_boundary():
    rep = d.run(N=120, w=3.0)
    assert rep["single_wall_partner_exiled"] is True


def test_verdict_chirality_survives():
    rep = d.run(N=120, w=3.0)
    assert rep["controls_ok"] is True
    assert rep["two_opposite_at_walls"] is True
    assert "chirality SURVIVES" in rep["verdict"]

"""Canonical observed constants shared by two or more SSV papers (#213).

This module is deliberately small.  It is the numerical source used by
``instruments/tools/gen_values.py::SHARED``; papers do not copy these values
and instruments do not need to import a paper's LaTeX-facing registry.

The SI constants are CODATA-2018 values already used by the repository.  The
particle rest energies are the PDG/CODATA values already transcribed in
``instruments/paper_ii/tau_identification.py``.  Centralising that existing
input is not a derivation: these remain observed inputs, and the generated
comments label them as such.
"""

from __future__ import annotations

import math

# CODATA-2018 / exact SI definitions.
HBAR = 1.054_571_817e-34       # J s
C = 299_792_458.0             # m s^-1, exact
ELECTRON_VOLT = 1.602_176_634e-19  # J, exact
ELECTRON_MASS_KG = 9.109_383_7015e-31
PROTON_MASS_KG = 1.672_621_923_69e-27
INVERSE_FINE_STRUCTURE = 137.035_999_084

# Observed rest energies in MeV.  These are inputs, not SSV predictions.
# Charged-pion source: PDG 2024 summary table,
# https://pdg.lbl.gov/2024/tables/rpp2024-sum-mesons.pdf
ELECTRON_MASS_MEV = 0.510_998_9461
MUON_MASS_MEV = 105.658_3755
CHARGED_PION_MASS_MEV = 139.570_39
CHARGED_PION_MASS_UNCERTAINTY_MEV = 0.000_18
PROTON_MASS_MEV = 938.272_088_16
TAU_MASS_MEV = 1776.86


def inverse_fine_structure() -> float:
    return INVERSE_FINE_STRUCTURE


def proton_electron_mass_ratio() -> float:
    return PROTON_MASS_KG / ELECTRON_MASS_KG


def electron_mass_mev() -> float:
    return ELECTRON_MASS_MEV


def muon_mass_mev() -> float:
    return MUON_MASS_MEV


def charged_pion_mass_mev() -> float:
    return CHARGED_PION_MASS_MEV


def proton_mass_mev() -> float:
    return PROTON_MASS_MEV


def tau_mass_mev() -> float:
    return TAU_MASS_MEV


def proton_reduced_compton_wavelength() -> float:
    """Reduced proton Compton wavelength, ``bar(lambda)_p``."""
    return HBAR / (PROTON_MASS_KG * C)


def proton_compton_wavelength() -> float:
    """Ordinary proton Compton wavelength, ``2 pi bar(lambda)_p``."""
    return 2.0 * math.pi * proton_reduced_compton_wavelength()

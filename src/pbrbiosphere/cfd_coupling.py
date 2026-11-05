"""Conservative unit and source-term bridge for future CFD/biology coupling.

This module prepares cell-local PBR-02 source terms in OpenFOAM SI units.
It does not read/write OpenFOAM fields or perform spatial interpolation.
"""
from __future__ import annotations
import numpy as np
from .config import ModelParameters


def mmol_l_day_to_mol_m3_s(rate):
    """Convert mmol/L/day to mol/m3/s (the concentration units are equivalent)."""
    values = np.asarray(rate, dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("source rates must be finite")
    return values / 86400.0


def g_l_day_to_kg_m3_s(rate):
    """Convert g/L/day to kg/m3/s (the mass-concentration units are equivalent)."""
    values = np.asarray(rate, dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("biomass source rates must be finite")
    return values / 86400.0


def pbr02_cell_sources(biomass_g_l, mu_per_day, parameters=None):
    """Return PBR-02 fixed-quota local sources in OpenFOAM SI units.

    Inputs are cell arrays; biomass is gDW/L and mu is 1/day. Returned fields
    are volumetric source densities: biomass kg/m3/s; DIC, O2, N and P
    mol/m3/s. Decay/respiration closure follows the existing reduced model.
    """
    p = parameters or ModelParameters()
    p.validate()
    x = np.asarray(biomass_g_l, dtype=float)
    mu = np.asarray(mu_per_day, dtype=float)
    if x.shape != mu.shape:
        raise ValueError("biomass and growth-rate arrays must have identical shapes")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(mu)):
        raise ValueError("biomass and growth-rate arrays must be finite")
    if np.any(x < 0) or np.any(mu < 0):
        raise ValueError("biomass and growth rate must be non-negative")

    fixation = mu * x
    respiration = p.respiration * x
    net_biomass = (mu - p.decay) * x
    dic = -fixation * p.q_c + respiration * p.respiratory_quotient
    oxygen = fixation * p.q_c * p.photosynthetic_quotient - respiration * p.respiratory_quotient
    nitrogen = -fixation * p.q_n
    phosphorus = -fixation * p.q_p
    return {
        "biomass_kg_m3_s": g_l_day_to_kg_m3_s(net_biomass),
        "dic_mol_m3_s": mmol_l_day_to_mol_m3_s(dic),
        "oxygen_mol_m3_s": mmol_l_day_to_mol_m3_s(oxygen),
        "nitrogen_mol_m3_s": mmol_l_day_to_mol_m3_s(nitrogen),
        "phosphorus_mol_m3_s": mmol_l_day_to_mol_m3_s(phosphorus),
        "units": "OpenFOAM SI volumetric source densities",
        "model": "PBR-02 fixed-quota reduced kinetics",
        "validation": "UNVALIDATED",
    }


def integrate_source(source_density, cell_volumes_m3):
    """Integrate cell source density to total rate (kg/s or mol/s)."""
    source = np.asarray(source_density, dtype=float)
    volume = np.asarray(cell_volumes_m3, dtype=float)
    if source.shape != volume.shape:
        raise ValueError("source and cell-volume arrays must have identical shapes")
    if not np.all(np.isfinite(source)) or not np.all(np.isfinite(volume)):
        raise ValueError("source and cell volumes must be finite")
    if np.any(volume <= 0):
        raise ValueError("cell volumes must be strictly positive")
    return float(np.sum(source * volume))

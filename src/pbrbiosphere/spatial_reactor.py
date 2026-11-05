"""One-dimensional finite-volume photobioreactor model.

Distributed engineering model, not 3-D CFD. State basis: biomass gDW/L;
DIC, O2, N, P mmol/L; temperature K; PAR umol photons/m2/s.
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy.integrate import solve_ivp
from .config import ModelParameters


@dataclass(frozen=True)
class SpatialReactorConfig:
    length_m: float = 1.0
    cross_section_m2: float = 0.01
    cells: int = 20
    flow_m3_s: float = 1e-5
    axial_dispersion_m2_s: float = 1e-5
    optical_path_m: float = 0.05
    biomass_absorption_m2_g: float = 8.0
    incident_par_umol_m2_s: float = 150.0
    kLa_o2_s: float = 0.0
    oxygen_saturation_mmol_l: float = 0.25
    wall_heat_transfer_w_m2_k: float = 0.0
    wall_area_per_volume_m2_m3: float = 0.0
    coolant_temperature_k: float = 298.15
    volumetric_heat_capacity_j_m3_k: float = 4.18e6
    thermal_diffusivity_m2_s: float = 1.4e-7

    def validate(self):
        for name in ("length_m", "cross_section_m2", "optical_path_m", "volumetric_heat_capacity_j_m3_k"):
            v = getattr(self, name)
            if not math.isfinite(v) or v <= 0:
                raise ValueError(f"{name} must be finite and > 0")
        for name in ("flow_m3_s", "axial_dispersion_m2_s", "biomass_absorption_m2_g",
                     "incident_par_umol_m2_s", "kLa_o2_s", "oxygen_saturation_mmol_l",
                     "wall_heat_transfer_w_m2_k", "wall_area_per_volume_m2_m3",
                     "thermal_diffusivity_m2_s"):
            v = getattr(self, name)
            if not math.isfinite(v) or v < 0:
                raise ValueError(f"{name} must be finite and >= 0")
        if self.cells < 3:
            raise ValueError("cells must be >= 3")
        if self.coolant_temperature_k <= 0 or not math.isfinite(self.coolant_temperature_k):
            raise ValueError("coolant_temperature_k must be finite and > 0")


@dataclass(frozen=True)
class SpatialInitialState:
    biomass_g_l: float = 0.1
    dic_mmol_l: float = 2.0
    oxygen_mmol_l: float = 0.2
    nitrogen_mmol_l: float = 1.0
    phosphorus_mmol_l: float = 0.1
    temperature_k: float = 298.15

    def validate(self):
        for name, value in vars(self).items():
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and >= 0")
        if self.temperature_k <= 0:
            raise ValueError("temperature_k must be > 0")


@dataclass
class SpatialReactorResult:
    time_s: np.ndarray
    x_m: np.ndarray
    biomass_g_l: np.ndarray
    dic_mmol_l: np.ndarray
    oxygen_mmol_l: np.ndarray
    nitrogen_mmol_l: np.ndarray
    phosphorus_mmol_l: np.ndarray
    temperature_k: np.ndarray
    par_umol_m2_s: np.ndarray
    solver_message: str
    success: bool
    metadata: dict


def _transport(field, velocity, dispersion, dx, inlet_value):
    """Finite-volume upwind advection and central dispersion.

    Positive-flow Danckwerts inlet concentration; zero-gradient convective
    outlet. Face fluxes are shared by adjacent cells, preserving internal
    conservation. The inlet diffusive gradient uses a half-cell distance.
    """
    if velocity < 0:
        raise ValueError("negative flow is not supported by this inlet convention")
    n = field.size
    flux = np.zeros(n + 1)
    flux[0] = velocity * inlet_value
    if dispersion > 0:
        flux[0] -= dispersion * (field[0] - inlet_value) / (0.5 * dx)
    flux[1:n] = velocity * field[:-1]
    flux[n] = velocity * field[-1]
    flux[1:n] -= dispersion * (field[1:] - field[:-1]) / dx
    return -(flux[1:] - flux[:-1]) / dx


def simulate_spatial_reactor(duration_s, output_points, config=None, initial=None,
                             parameters=None, inlet=None, rtol=1e-6, atol=1e-9):
    """Solve 1-D axial transport/reaction using method-of-lines and BDF.

    Biology inherits PBR-02 per-day kinetics and fixed quotas. PAR is photon
    flux; its use as the PBR-02 light-response input is an uncalibrated proxy.
    """
    cfg = config or SpatialReactorConfig()
    init = initial or SpatialInitialState()
    feed = inlet or init
    p = parameters or ModelParameters()
    cfg.validate()
    init.validate()
    feed.validate()
    p.validate()
    if not math.isfinite(duration_s) or duration_s <= 0:
        raise ValueError("duration_s must be finite and > 0")
    if output_points < 2:
        raise ValueError("output_points must be >= 2")
    if not 0 < rtol < 1 or not 0 < atol < 1:
        raise ValueError("solver tolerances must be between 0 and 1")

    n = cfg.cells
    dx = cfg.length_m / n
    velocity = cfg.flow_m3_s / cfg.cross_section_m2
    x = (np.arange(n) + 0.5) * dx
    y0 = np.concatenate([
        np.full(n, init.biomass_g_l), np.full(n, init.dic_mmol_l),
        np.full(n, init.oxygen_mmol_l), np.full(n, init.nitrogen_mmol_l),
        np.full(n, init.phosphorus_mmol_l), np.full(n, init.temperature_k),
    ])
    feed_values = np.array([feed.biomass_g_l, feed.dic_mmol_l, feed.oxygen_mmol_l,
                            feed.nitrogen_mmol_l, feed.phosphorus_mmol_l, feed.temperature_k])

    def rhs(_t, state):
        fields = [np.maximum(state[i*n:(i+1)*n], 0.0) for i in range(6)]
        biomass, dic, oxygen, nitrogen, phosphorus, temp = fields
        par = cfg.incident_par_umol_m2_s * np.exp(
            -cfg.biomass_absorption_m2_g * biomass * cfg.optical_path_m)
        light = par / (p.k_light + par)
        fn = nitrogen / (p.k_n + nitrogen)
        fp = phosphorus / (p.k_p + phosphorus)
        fc = dic / (p.k_c + dic)
        mu = p.mu_max * light * np.minimum(fn, fp) * fc
        net_growth_s = ((mu - p.decay) * biomass) / 86400.0
        fixation = np.maximum(mu * biomass, 0.0)
        respiration = p.respiration * biomass
        dic_rxn = (-fixation * p.q_c + respiration) / 86400.0
        o2_rxn = (fixation * p.q_c * p.photosynthetic_quotient
                  - respiration * p.respiratory_quotient) / 86400.0
        n_rxn = -fixation * p.q_n / 86400.0
        p_rxn = -fixation * p.q_p / 86400.0
        o2_transfer = cfg.kLa_o2_s * (cfg.oxygen_saturation_mmol_l - oxygen)
        wall_heat = (cfg.wall_heat_transfer_w_m2_k * cfg.wall_area_per_volume_m2_m3
                     * (cfg.coolant_temperature_k - temp)
                     / cfg.volumetric_heat_capacity_j_m3_k)
        derivs = [
            _transport(biomass, velocity, cfg.axial_dispersion_m2_s, dx, feed_values[0]) + net_growth_s,
            _transport(dic, velocity, cfg.axial_dispersion_m2_s, dx, feed_values[1]) + dic_rxn,
            _transport(oxygen, velocity, cfg.axial_dispersion_m2_s, dx, feed_values[2]) + o2_rxn + o2_transfer,
            _transport(nitrogen, velocity, cfg.axial_dispersion_m2_s, dx, feed_values[3]) + n_rxn,
            _transport(phosphorus, velocity, cfg.axial_dispersion_m2_s, dx, feed_values[4]) + p_rxn,
            _transport(temp, velocity, cfg.thermal_diffusivity_m2_s, dx, feed_values[5]) + wall_heat,
        ]
        return np.concatenate(derivs)

    times = np.linspace(0, duration_s, output_points)
    sol = solve_ivp(rhs, (0, duration_s), y0, method="BDF", t_eval=times, rtol=rtol, atol=atol)
    values = sol.y.reshape(6, n, -1).transpose(2, 1, 0)
    values[:, :, :5] = np.maximum(values[:, :, :5], 0.0)
    par = cfg.incident_par_umol_m2_s * np.exp(
        -cfg.biomass_absorption_m2_g * values[:, :, 0] * cfg.optical_path_m)
    return SpatialReactorResult(
        time_s=sol.t, x_m=x, biomass_g_l=values[:, :, 0], dic_mmol_l=values[:, :, 1],
        oxygen_mmol_l=values[:, :, 2], nitrogen_mmol_l=values[:, :, 3],
        phosphorus_mmol_l=values[:, :, 4], temperature_k=values[:, :, 5],
        par_umol_m2_s=par, solver_message=sol.message, success=sol.success,
        metadata={
            "model_id": "PBR-SPATIAL-1D-001", "version": "0.1.0",
            "fidelity_tier": 2, "validation": "UNVALIDATED",
            "method": "method-of-lines; SciPy solve_ivp BDF",
            "spatial_dimension": 1, "cells": n, "dx_m": dx,
            "flow_velocity_m_s": velocity,
            "assumptions": [
                "1-D axial advection-dispersion; no radial flow or turbulence closure",
                "transverse Beer-Lambert attenuation; no scattering or spectral optics",
                "PBR-02 Monod/Liebig kinetics and fixed elemental quotas",
                "optional oxygen kLa uses fixed saturation; no bubble-resolved gas phase",
                "thermal advection/diffusion and lumped wall exchange; reaction heat omitted",
                "CO2 transfer and carbonate chemistry are not coupled",
            ],
            "warnings": [
                "Not 3-D CFD and not experimentally validated.",
                "PAR-to-growth mapping is provisional and requires calibration.",
                "Reported concentrations are clipped at zero after integration.",
            ],
        },
    )

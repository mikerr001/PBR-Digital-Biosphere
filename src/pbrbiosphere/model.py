"""Coupled well-mixed culture model (liquid phase only; no gas transfer)."""
import numpy as np
from .config import Environment, ModelParameters
from .biology import growth_rate
from .irradiance import square_wave_irradiance

# State order: X [gDW/L], C [mmol C/L], O [mmol O2/L], N [mmol N/L], P [mmol P/L]


def rhs(t: float, y: np.ndarray, p: ModelParameters, env: Environment) -> np.ndarray:
    x, c, o, n, phos = y
    x, c, o, n, phos = [max(0.0, float(v)) for v in (x, c, o, n, phos)]
    light = square_wave_irradiance(t, env.irradiance,
                                   env.photoperiod_hours, env.day_hours)
    mu = growth_rate(x, c, n, phos, light, env.temperature_c, p)

    # These conversions are explicit model parameters, not universal constants.
    carbon_fixed = mu * x * p.yield_c  # mmol C/L/day incorporated into biomass
    oxygen_consumed = p.respiration * x  # mmol O2/L/day
    carbon_from_respiration = oxygen_consumed * p.respiratory_quotient
    gross_oxygen = carbon_fixed * p.photosynthetic_quotient

    # Illustrative biomass elemental quotas; replace with measured composition.
    nitrogen_uptake = mu * x * 8.0
    phosphorus_uptake = mu * x * 0.8

    dX = (mu - p.decay) * x
    dC = -carbon_fixed + carbon_from_respiration
    dO = gross_oxygen - oxygen_consumed
    dN = -nitrogen_uptake
    dP = -phosphorus_uptake
    return np.array([dX, dC, dO, dN, dP], dtype=float)

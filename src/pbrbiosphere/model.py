"""Coupled well-mixed culture model (liquid phase only; no gas transfer)."""
import numpy as np
from .config import Environment, ModelParameters
from .biology import growth_rate
from .irradiance import square_wave_irradiance

# State order: X [gDW/L], C [mmol C/L], O [mmol O2/L], N [mmol N/L], P [mmol P/L]


def rhs(t: float, y: np.ndarray, p: ModelParameters, env: Environment) -> np.ndarray:
    x, c, o, n, phos = y
    # Reject materially invalid states; tiny solver excursions are clipped for rate evaluation.
    x, c, o, n, phos = [max(0.0, float(v)) for v in (x, c, o, n, phos)]
    light = square_wave_irradiance(t, env.irradiance,
                                   env.photoperiod_hours, env.day_hours)
    mu = growth_rate(x, c, n, phos, light, env.temperature_c, p)

    # Growth-linked carbon incorporation is a simplified stoichiometric sink.
    # yield_c is an explicitly illustrative carbon requirement per gDW formed.
    carbon_fix = mu * x * p.yield_c  # mmol C/L/day
    # Respiration is a simplified biomass-specific oxygen demand.
    respiration = p.respiration * x  # mmol O2/L/day
    # Gross O2 is coupled to carbon fixation at a placeholder 1:1 molar ratio.
    # Replace with organism/condition-specific measured photosynthetic quotient.
    gross_o2 = carbon_fix

    # Nutrient uptake is represented by fixed biomass composition coefficients.
    # These are placeholders and must be replaced by measured biomass elemental data.
    n_uptake = mu * x * 8.0
    p_uptake = mu * x * 0.8

    dX = (mu - p.decay) * x
    dC = -carbon_fix + respiration
    dO = gross_o2 - respiration
    dN = -n_uptake
    dP = -p_uptake
    return np.array([dX, dC, dO, dN, dP], dtype=float)

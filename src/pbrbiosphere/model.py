"""Reduced, well-mixed culture model; no gas headspace or kLa transfer."""
import numpy as np
from .config import Environment, ModelParameters
from .biology import growth_rate
from .irradiance import square_wave_irradiance
from .respiration import oxygen_consumption
from .photosynthesis import gross_oxygen_from_carbon
from .nutrients import net_nutrient_change

# State: X [gDW/L], C [mmol C/L], O [mmol O2/L], N [mmol N/L], P [mmol P/L].


def rhs(t: float, y: np.ndarray, p: ModelParameters, env: Environment) -> np.ndarray:
    p.validate()
    env.validate()
    x, c, o, n, phos = map(float, y)
    if min(x, c, o, n, phos) < -1e-8:
        raise ValueError("state contains a materially negative concentration")
    x, c, o, n, phos = [max(0.0, v) for v in (x, c, o, n, phos)]
    light = square_wave_irradiance(t, env.irradiance, env.photoperiod_hours, env.day_hours)
    mu = growth_rate(x, c, n, phos, light, env.temperature_c, p)

    growth_biomass = mu * x
    decay_biomass = p.decay * x
    d_x = growth_biomass - decay_biomass

    # Reduced carbon bookkeeping: fixed biomass quota and complete decay return.
    o2_resp = oxygen_consumption(x, p.respiration)
    c_resp = o2_resp * p.respiratory_quotient
    c_biomass_net = p.q_c * d_x
    c_gross_fix = max(0.0, c_biomass_net + c_resp)
    o2_gross = gross_oxygen_from_carbon(c_gross_fix, p.photosynthetic_quotient)

    # The reduced carbon pool closes exactly with the fixed biomass carbon quota:
    # d(DIC + qC*X)/dt = 0. This is a simplifying closure, not a full cell model.
    d_c = -p.q_c * d_x
    d_o = o2_gross - o2_resp
    d_n = net_nutrient_change(mu, p.decay, x, p.q_n)
    d_p = net_nutrient_change(mu, p.decay, x, p.q_p)

    # Prevent further uptake once a dissolved nutrient pool is depleted.
    if n <= 1e-12 and d_n < 0:
        d_n = 0.0
    if phos <= 1e-12 and d_p < 0:
        d_p = 0.0
    if c <= 1e-12 and d_c < 0:
        d_c = 0.0
    return np.array([d_x, d_c, d_o, d_n, d_p], dtype=float)

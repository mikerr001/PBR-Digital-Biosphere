"""Reduced physiological response functions; all factors are dimensionless."""
import math
from .config import ModelParameters


def light_fraction(irradiance: float, k_light: float) -> float:
    """Monod-type light saturation; does not represent photoinhibition."""
    if irradiance < 0 or k_light <= 0:
        raise ValueError("irradiance must be >= 0 and k_light must be > 0")
    return irradiance / (k_light + irradiance)


def nutrient_fraction(concentration: float, half_saturation: float) -> float:
    """Monod nutrient limitation."""
    if concentration < 0 or half_saturation <= 0:
        raise ValueError("concentration must be >= 0 and K must be > 0")
    return concentration / (half_saturation + concentration)


def temperature_fraction(temperature_c: float) -> float:
    """Neutral placeholder until organism-specific thermal data are fitted."""
    if not math.isfinite(temperature_c):
        raise ValueError("temperature must be finite")
    return 1.0


def growth_rate(x: float, dic: float, nitrogen: float, phosphorus: float,
                irradiance: float, temperature_c: float,
                p: ModelParameters) -> float:
    """Potential specific growth rate (day-1), before decay.

    Liebig minimum is used for N/P co-limitation. The DIC Monod term is a
    provisional lumped-pool approximation, not carbonate chemistry.
    """
    if x < 0:
        raise ValueError("biomass cannot be negative")
    f_i = light_fraction(irradiance, p.k_light)
    f_n = nutrient_fraction(nitrogen, p.k_n)
    f_p = nutrient_fraction(phosphorus, p.k_p)
    f_c = nutrient_fraction(dic, p.k_c)
    return p.mu_max * f_i * min(f_n, f_p) * f_c * temperature_fraction(temperature_c)

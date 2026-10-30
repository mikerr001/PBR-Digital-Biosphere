"""Photosynthesis-irradiance response functions."""
import math


def platt_relative(irradiance: float, alpha: float, pmax: float, beta: float) -> float:
    """Platt P-I response divided by Pmax; dimensionless.

    Coefficients must share a consistent irradiance/rate convention.
    """
    if irradiance < 0 or alpha <= 0 or pmax <= 0 or beta < 0:
        raise ValueError("I >= 0, alpha > 0, Pmax > 0 and beta >= 0 required")
    return (1.0 - math.exp(-alpha * irradiance / pmax)) * math.exp(-beta * irradiance / pmax)


def gross_oxygen_from_carbon(carbon_fixation_mmol_l_day: float,
                             photosynthetic_quotient: float) -> float:
    """Convert gross C fixation to gross O2 evolution using a sourced PQ."""
    if carbon_fixation_mmol_l_day < 0 or photosynthetic_quotient <= 0:
        raise ValueError("carbon fixation must be >= 0 and PQ must be > 0")
    return carbon_fixation_mmol_l_day * photosynthetic_quotient

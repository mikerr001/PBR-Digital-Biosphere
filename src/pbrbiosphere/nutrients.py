"""Nutrient limitation and uptake/remineralisation bookkeeping."""
from .biology import nutrient_fraction


def nutrient_limitation(nitrogen: float, phosphorus: float, k_n: float, k_p: float) -> float:
    """Liebig minimum of Monod N and P limitation."""
    return min(nutrient_fraction(nitrogen, k_n), nutrient_fraction(phosphorus, k_p))


def net_nutrient_change(growth_rate_day: float, decay_rate_day: float,
                        biomass_gdw_l: float, quota_mmol_gdw: float) -> float:
    """Dissolved nutrient change with complete return from decayed biomass."""
    if min(growth_rate_day, decay_rate_day, biomass_gdw_l, quota_mmol_gdw) < 0:
        raise ValueError("rates, biomass and quota must be non-negative")
    return quota_mmol_gdw * biomass_gdw_l * (decay_rate_day - growth_rate_day)

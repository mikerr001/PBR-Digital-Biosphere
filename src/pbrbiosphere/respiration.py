"""Respiration rate functions, separate from gross photosynthesis."""
def oxygen_consumption(x_gdw_l: float, specific_rate_mmol_gdw_day: float) -> float:
    """Return O2 consumption in mmol O2 L-1 day-1."""
    if x_gdw_l < 0 or specific_rate_mmol_gdw_day < 0:
        raise ValueError("biomass and respiration rate must be non-negative")
    return x_gdw_l * specific_rate_mmol_gdw_day

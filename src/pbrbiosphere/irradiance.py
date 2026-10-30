"""Externally prescribed light schedules."""
import math


def square_wave_irradiance(t_days: float, peak: float, photoperiod_hours: float = 12.0,
                           day_hours: float = 24.0) -> float:
    """Idealised light-dark schedule; t is elapsed days."""
    if peak < 0 or not 0 <= photoperiod_hours <= day_hours or day_hours <= 0:
        raise ValueError("invalid irradiance or photoperiod")
    hour = (t_days * 24.0) % day_hours
    return peak if hour < photoperiod_hours else 0.0


def constant_irradiance(t_days: float, peak: float) -> float:
    if peak < 0 or not math.isfinite(t_days):
        raise ValueError("invalid irradiance or time")
    return peak

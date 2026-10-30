"""Evidence-backed observations for Synechococcus elongatus PCC 7942.

Values below are source observations, not universal species constants.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    name: str
    value: float
    unit: str
    uncertainty: float | None
    temperature_c: float
    irradiance_umol_m2_s: float
    medium: str
    acclimation_hours: float
    doi: str


SOURCE_DOI = "10.1016/j.ymben.2018.11.001"
STRAIN = "PCC 7942"
ORGANISM = "Synechococcus elongatus"

OBSERVATIONS = (
    Observation("growth_rate_low_light", 0.047, "h-1", 0.004, 30.0, 60.0,
                "BG-11", 72.0, SOURCE_DOI),
    Observation("growth_rate_high_light", 0.081, "h-1", 0.015, 30.0, 600.0,
                "BG-11", 72.0, SOURCE_DOI),
    Observation("dark_respiration_low_light", 0.15, "mmol O2 gDW-1 h-1", None,
                30.0, 60.0, "BG-11", 72.0, SOURCE_DOI),
    Observation("dark_respiration_high_light", 0.41, "mmol O2 gDW-1 h-1", None,
                30.0, 600.0, "BG-11", 72.0, SOURCE_DOI),
)


def rate_per_day(value_per_hour: float) -> float:
    """Convert an hourly rate to a daily rate; preserves the quantity basis."""
    return value_per_hour * 24.0

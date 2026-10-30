"""Typed model configuration. Defaults are software-demo assumptions, not biology data."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelParameters:
    """Reduced-model parameters; replace demo values with sourced organism data.

    Rates are per day. Concentrations are mmol/L; X is g dry weight/L.
    q_c/n/p are biomass elemental quotas in mmol element per g dry biomass.
    """
    mu_max: float = 0.35
    decay: float = 0.01
    k_light: float = 100.0
    k_n: float = 0.10
    k_p: float = 0.01
    k_c: float = 0.20
    respiration: float = 0.50       # mmol O2 gDW-1 day-1
    respiratory_quotient: float = 1.0  # mmol C released / mmol O2 consumed
    photosynthetic_quotient: float = 1.0  # mmol O2 / mmol C fixed
    q_c: float = 35.0               # mmol C / gDW; demo assumption
    q_n: float = 8.0                # mmol N / gDW; demo assumption
    q_p: float = 0.8                # mmol P / gDW; demo assumption

    def validate(self) -> None:
        positive = ("mu_max", "k_light", "k_n", "k_p", "k_c",
                    "respiratory_quotient", "photosynthetic_quotient",
                    "q_c", "q_n", "q_p")
        nonnegative = ("decay", "respiration")
        for name in positive:
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be > 0")
        for name in nonnegative:
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")


@dataclass(frozen=True)
class InitialState:
    """X: gDW/L; DIC: mmol C/L; O: mmol O2/L; N/P: mmol element/L."""
    biomass: float = 0.10
    dic: float = 2.0
    oxygen: float = 0.20
    nitrogen: float = 1.0
    phosphorus: float = 0.10

    def validate(self) -> None:
        for name, value in vars(self).items():
            if value < 0:
                raise ValueError(f"initial {name} must be >= 0")


@dataclass(frozen=True)
class Environment:
    temperature_c: float = 25.0
    irradiance: float = 100.0
    photoperiod_hours: float = 12.0
    day_hours: float = 24.0

    def validate(self) -> None:
        if self.irradiance < 0:
            raise ValueError("irradiance must be >= 0")
        if self.day_hours <= 0:
            raise ValueError("day_hours must be > 0")
        if not 0 <= self.photoperiod_hours <= self.day_hours:
            raise ValueError("photoperiod_hours must be between 0 and day_hours")

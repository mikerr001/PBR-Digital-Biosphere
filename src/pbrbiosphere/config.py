"""Typed model configuration. Defaults are software-demo assumptions, not biology data."""
from dataclasses import dataclass
import math


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
    respiration: float = 0.50
    respiratory_quotient: float = 1.0
    photosynthetic_quotient: float = 1.0
    q_c: float = 35.0
    q_n: float = 8.0
    q_p: float = 0.8

    def validate(self) -> None:
        positive = ("mu_max", "k_light", "k_n", "k_p", "k_c",
                    "respiratory_quotient", "photosynthetic_quotient",
                    "q_c", "q_n", "q_p")
        nonnegative = ("decay", "respiration")
        for name in positive:
            value = getattr(self, name)
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and > 0")
        for name in nonnegative:
            value = getattr(self, name)
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and >= 0")


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
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"initial {name} must be finite and >= 0")


@dataclass(frozen=True)
class Environment:
    temperature_c: float = 25.0
    irradiance: float = 100.0
    photoperiod_hours: float = 12.0
    day_hours: float = 24.0

    def validate(self) -> None:
        values = (self.temperature_c, self.irradiance,
                  self.photoperiod_hours, self.day_hours)
        if not all(math.isfinite(v) for v in values):
            raise ValueError("environment values must be finite")
        if self.irradiance < 0:
            raise ValueError("irradiance must be >= 0")
        if self.day_hours <= 0:
            raise ValueError("day_hours must be > 0")
        if not 0 <= self.photoperiod_hours <= self.day_hours:
            raise ValueError("photoperiod_hours must be between 0 and day_hours")

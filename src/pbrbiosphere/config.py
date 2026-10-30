"""Configuration objects and explicitly labelled starter parameters."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelParameters:
    """Illustrative parameters; NOT an organism-validated parameter set.

    Units:
      mu_max, decay: 1/day
      k_light: umol photons m-2 s-1
      k_n, k_p, k_c: mmol/L
      respiration: mmol O2 gDW-1 day-1
      yield_c: mmol C gDW-1 formed
      photosynthetic_quotient: mmol O2 evolved / mmol C fixed
      respiratory_quotient: mmol C released / mmol O2 consumed
    """
    mu_max: float = 0.35
    decay: float = 0.01
    k_light: float = 100.0
    k_n: float = 0.10
    k_p: float = 0.01
    k_c: float = 0.20
    respiration: float = 0.50
    yield_c: float = 35.0
    photosynthetic_quotient: float = 1.0
    respiratory_quotient: float = 1.0


@dataclass(frozen=True)
class InitialState:
    """State units: X gDW/L; C,O,N,P mmol/L."""
    biomass: float = 0.10
    dic: float = 2.0
    oxygen: float = 0.20
    nitrogen: float = 1.0
    phosphorus: float = 0.10


@dataclass(frozen=True)
class Environment:
    temperature_c: float = 25.0
    irradiance: float = 100.0
    photoperiod_hours: float = 12.0
    day_hours: float = 24.0

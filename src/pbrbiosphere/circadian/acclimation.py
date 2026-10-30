"""Independent phenomenological light-acclimation state.

This is a provisional first-order state model, not a fitted molecular model.
It is deliberately not coupled to growth or oxygen production until calibrated.
"""
from dataclasses import dataclass
import math
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AcclimationParameters:
    half_saturation_irradiance: float = 100.0
    tau_increase_hours: float = 12.0
    tau_decrease_hours: float = 24.0
    initial_state: float = 0.5

    def validate(self) -> None:
        values = (self.half_saturation_irradiance, self.tau_increase_hours,
                  self.tau_decrease_hours, self.initial_state)
        if not all(math.isfinite(v) for v in values):
            raise ValueError("acclimation parameters must be finite")
        if self.half_saturation_irradiance <= 0 or self.tau_increase_hours <= 0 or self.tau_decrease_hours <= 0:
            raise ValueError("irradiance half-saturation and time constants must be > 0")
        if not 0.0 <= self.initial_state <= 1.0:
            raise ValueError("initial acclimation state must be in [0, 1]")


def simulate_light_acclimation(time_hours, irradiance_umol_m2_s,
                               parameters: AcclimationParameters | None = None) -> pd.DataFrame:
    """Integrate a bounded acclimation state from piecewise-linear irradiance.

    Input arrays must share a strictly increasing time grid. The target state
    is I/(I+K); separate time constants permit asymmetric adjustment. This
    state is a generic light-history descriptor, not a measured pigment or
    photosystem quantity and not a productivity multiplier.
    """
    p = parameters or AcclimationParameters()
    p.validate()
    times = np.asarray(time_hours, dtype=float)
    light = np.asarray(irradiance_umol_m2_s, dtype=float)
    if times.ndim != 1 or light.ndim != 1 or len(times) != len(light) or len(times) < 2:
        raise ValueError("time and irradiance must be equal-length 1D arrays with at least two points")
    if not np.all(np.isfinite(times)) or not np.all(np.isfinite(light)):
        raise ValueError("time and irradiance values must be finite")
    if times[0] < 0 or np.any(np.diff(times) <= 0):
        raise ValueError("time grid must be nonnegative and strictly increasing")
    if np.any(light < 0):
        raise ValueError("irradiance must be nonnegative")

    state = p.initial_state
    rows = [(times[0], light[0], state, light[0] / (light[0] + p.half_saturation_irradiance))]
    for i in range(1, len(times)):
        dt = times[i] - times[i - 1]
        # Midpoint forcing approximates the piecewise-linear input over this step.
        irradiance = 0.5 * (light[i - 1] + light[i])
        target = irradiance / (irradiance + p.half_saturation_irradiance)
        tau = p.tau_increase_hours if target > state else p.tau_decrease_hours
        state = target + (state - target) * math.exp(-dt / tau)
        state = min(1.0, max(0.0, state))
        rows.append((times[i], light[i], state,
                     light[i] / (light[i] + p.half_saturation_irradiance)))
    return pd.DataFrame(rows, columns=["time_hours", "irradiance_umol_m2_s",
                                       "acclimation_state", "target_state"])

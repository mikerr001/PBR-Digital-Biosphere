"""Reduced phase-oscillator model for KaiABC entrainment.

This is deliberately NOT a molecular KaiA/KaiB/KaiC phosphorylation ODE.
It represents experimentally measurable phase dynamics using an explicit,
periodic phase-response curve (PRC). PRC entries must ultimately be fitted
from organism/condition-specific data. Zero-valued default PRCs mean that
light transitions do not reset the clock until calibrated.
"""
from dataclasses import dataclass
import math
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class LightTransition:
    """An environmental transition at absolute culture time (hours)."""
    time_hours: float
    light_on: bool

    def validate(self) -> None:
        if not math.isfinite(self.time_hours) or self.time_hours < 0:
            raise ValueError("transition time must be finite and >= 0")


@dataclass(frozen=True)
class CircadianParameters:
    """Phase model parameters; all PRC values are phase shifts in hours.

    PRCs are periodic lookup tables at equally spaced circadian phases.
    The defaults are neutral (no entrainment), not claimed biological fits.
    """
    intrinsic_period_hours: float = 24.0
    initial_phase_hours: float = 6.0
    prc_bins: int = 8
    light_prc_hours: tuple[float, ...] = (0.0,) * 8
    dark_prc_hours: tuple[float, ...] = (0.0,) * 8
    morning_output_start_hours: float = 4.0
    morning_output_end_hours: float = 10.0
    output_transition_hours: float = 0.5

    def validate(self) -> None:
        if not math.isfinite(self.intrinsic_period_hours) or self.intrinsic_period_hours <= 0:
            raise ValueError("intrinsic period must be finite and > 0")
        if not math.isfinite(self.initial_phase_hours):
            raise ValueError("initial phase must be finite")
        if self.prc_bins < 4:
            raise ValueError("PRC requires at least four phase bins")
        if len(self.light_prc_hours) != self.prc_bins or len(self.dark_prc_hours) != self.prc_bins:
            raise ValueError("light and dark PRCs must each match prc_bins")
        if not all(math.isfinite(v) for v in (*self.light_prc_hours, *self.dark_prc_hours)):
            raise ValueError("PRC values must be finite")
        if not (0 <= self.morning_output_start_hours < self.morning_output_end_hours <= self.intrinsic_period_hours):
            raise ValueError("morning output window must lie within one intrinsic period")
        if not math.isfinite(self.output_transition_hours) or self.output_transition_hours <= 0:
            raise ValueError("output transition width must be finite and > 0")


def _periodic_prc(phase_hours: float, values: tuple[float, ...], period: float) -> float:
    """Linear interpolation on a periodic phase grid."""
    phase = (phase_hours % period) / period
    xp = np.linspace(0.0, 1.0, len(values) + 1)
    fp = np.asarray((*values, values[0]), dtype=float)
    return float(np.interp(phase, xp, fp))


def _smooth_window(phase_hours: float, start: float, end: float, width: float) -> float:
    """Bounded smooth morning output window; not a sinusoidal clock surrogate."""
    def sigmoid(x: float) -> float:
        if x >= 0:
            z = math.exp(-min(x, 700.0))
            return 1.0 / (1.0 + z)
        z = math.exp(max(x, -700.0))
        return z / (1.0 + z)
    return sigmoid((phase_hours - start) / width) * sigmoid((end - phase_hours) / width)


def simulate_circadian(duration_hours: float, transitions: list[LightTransition],
                       parameters: CircadianParameters | None = None,
                       sample_interval_hours: float = 0.25) -> pd.DataFrame:
    """Simulate free-running phase with instantaneous light/dark PRC resets.

    A transition at t=0 establishes the initial light state but does not apply
    a phase reset. Each later transition applies its matching PRC evaluated at
    the phase immediately before that transition. Phase is retained in an
    unwrapped hour coordinate; phase_hours is wrapped to one clock period.
    """
    p = parameters or CircadianParameters()
    p.validate()
    if not math.isfinite(duration_hours) or duration_hours <= 0:
        raise ValueError("duration_hours must be finite and > 0")
    if not math.isfinite(sample_interval_hours) or sample_interval_hours <= 0:
        raise ValueError("sample interval must be finite and > 0")
    ordered = sorted(transitions, key=lambda item: item.time_hours)
    for item in ordered:
        item.validate()
    if len({item.time_hours for item in ordered}) != len(ordered):
        raise ValueError("only one light transition is allowed at a given time")
    if any(item.time_hours > duration_hours for item in ordered):
        raise ValueError("transition occurs after simulation end")

    sample_times = np.arange(0.0, duration_hours, sample_interval_hours)
    if len(sample_times) == 0 or not math.isclose(sample_times[-1], duration_hours):
        sample_times = np.append(sample_times, duration_hours)
    phase_unwrapped = p.initial_phase_hours
    current_time = 0.0
    transition_map = {item.time_hours: item for item in ordered if item.time_hours > 0}
    records = []
    for t in sample_times:
        while current_time < t - 1e-12:
            next_transition = min((v for v in transition_map if current_time < v <= t), default=None)
            stop = next_transition if next_transition is not None else t
            phase_unwrapped += (stop - current_time)
            current_time = stop
            if next_transition is not None:
                item = transition_map[next_transition]
                phase = phase_unwrapped % p.intrinsic_period_hours
                prc = p.light_prc_hours if item.light_on else p.dark_prc_hours
                phase_unwrapped += _periodic_prc(phase, prc, p.intrinsic_period_hours)
                del transition_map[next_transition]
        phase = phase_unwrapped % p.intrinsic_period_hours
        records.append((t, phase_unwrapped, phase,
                        _smooth_window(phase, p.morning_output_start_hours,
                                       p.morning_output_end_hours,
                                       p.output_transition_hours)))
    return pd.DataFrame(records, columns=["time_hours", "phase_unwrapped_hours",
                                           "phase_hours", "morning_output_proxy"])

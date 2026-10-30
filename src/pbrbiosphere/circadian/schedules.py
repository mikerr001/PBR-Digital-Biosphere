"""Reproducible illumination schedules for circadian entrainment experiments."""
from .model import LightTransition


def daily_light_dark(days: float, photoperiod_hours: float = 12.0,
                     day_hours: float = 24.0, dawn_hours: float = 0.0) -> list[LightTransition]:
    if days <= 0 or day_hours <= 0 or not 0 <= photoperiod_hours <= day_hours:
        raise ValueError("invalid duration or photoperiod")
    events = []
    cycle = 0
    while cycle * day_hours < days * 24.0:
        dawn = cycle * day_hours + dawn_hours
        dusk = dawn + photoperiod_hours
        if 0 <= dawn <= days * 24.0:
            events.append(LightTransition(dawn, True))
        if 0 <= dusk <= days * 24.0:
            events.append(LightTransition(dusk, False))
        cycle += 1
    return sorted(events, key=lambda event: event.time_hours)


def shifted_schedule(days: float, photoperiod_hours: float = 12.0,
                     day_hours: float = 24.0, shift_day: int = 2,
                     shift_hours: float = 6.0) -> list[LightTransition]:
    """One abrupt dawn/dusk shift, then the shifted schedule remains in force."""
    if shift_day < 1:
        raise ValueError("shift_day must be >= 1")
    events = daily_light_dark(days, photoperiod_hours, day_hours)
    boundary = shift_day * day_hours
    shifted = []
    for event in events:
        if event.time_hours < boundary:
            shifted.append(event)
        else:
            shifted.append(LightTransition(event.time_hours + shift_hours, event.light_on))
    return sorted((e for e in shifted if e.time_hours <= days * 24.0),
                  key=lambda event: event.time_hours)


def irregular_schedule(days: float) -> list[LightTransition]:
    """Deterministic deliberately irregular light pulses for stress testing."""
    if days <= 0:
        raise ValueError("days must be > 0")
    pattern = [(0, True), (8, False), (14, True), (19, False),
               (24, True), (35, False), (42, True), (51, False),
               (60, True), (68, False), (77, True), (84, False)]
    return [LightTransition(float(t), state) for t, state in pattern if t <= days * 24.0]

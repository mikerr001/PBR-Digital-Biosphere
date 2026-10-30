"""Standard circadian entrainment experiments (simulations, not measurements)."""
from .model import CircadianParameters, simulate_circadian
from .schedules import daily_light_dark, irregular_schedule, shifted_schedule


def run_circadian_suite(days: float = 5.0,
                        parameters: CircadianParameters | None = None,
                        sample_interval_hours: float = 0.25):
    """Run matched forcing cases from one common clock initial phase."""
    if days <= 0:
        raise ValueError("days must be > 0")
    cases = {
        "free_running": [],
        "regular_12_12": daily_light_dark(days, 12.0, 24.0),
        "shifted_12_12": shifted_schedule(days, 12.0, 24.0),
        "irregular_light": irregular_schedule(days),
    }
    return {
        name: simulate_circadian(days * 24.0, events, parameters,
                                 sample_interval_hours)
        for name, events in cases.items()
    }

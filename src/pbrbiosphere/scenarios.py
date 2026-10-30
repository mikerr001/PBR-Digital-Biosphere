"""Named engineering scenarios; outputs are model experiments, not lab results."""
from .config import Environment, InitialState, ModelParameters
from .simulate import run_simulation


def run_standard_scenarios(days: float = 5.0, points: int = 501,
                           params: ModelParameters | None = None,
                           initial: InitialState | None = None):
    """Run a controlled light schedule comparison using the same initial state."""
    schedules = {
        "dark": Environment(irradiance=0.0, photoperiod_hours=0.0),
        "constant_light": Environment(irradiance=100.0, photoperiod_hours=24.0),
        "light_dark_12_12": Environment(irradiance=100.0, photoperiod_hours=12.0),
        "low_light_12_12": Environment(irradiance=60.0, photoperiod_hours=12.0),
        "high_light_12_12": Environment(irradiance=600.0, photoperiod_hours=12.0),
    }
    return {
        name: run_simulation(days, points, params=params, initial=initial, environment=env)
        for name, env in schedules.items()
    }

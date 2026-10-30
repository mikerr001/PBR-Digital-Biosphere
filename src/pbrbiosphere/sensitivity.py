"""One-at-a-time parameter sensitivity for exploratory screening."""
from dataclasses import replace
import pandas as pd
from .config import Environment, InitialState, ModelParameters
from .simulate import run_simulation


def one_at_a_time(parameter_name: str, values, metric_column: str = "biomass_gDW_L",
                  days: float = 5.0, points: int = 201,
                  base: ModelParameters | None = None,
                  initial: InitialState | None = None,
                  environment: Environment | None = None) -> pd.DataFrame:
    """Vary one ModelParameters field and record terminal metric.

    This is screening, not global sensitivity analysis or parameter inference.
    """
    base = base or ModelParameters()
    if not hasattr(base, parameter_name):
        raise AttributeError(f"unknown model parameter: {parameter_name}")
    rows = []
    for value in values:
        candidate = replace(base, **{parameter_name: float(value)})
        frame = run_simulation(days, points, candidate, initial, environment)
        rows.append({"parameter": parameter_name, "value": float(value),
                     f"final_{metric_column}": float(frame[metric_column].iloc[-1])})
    return pd.DataFrame(rows)

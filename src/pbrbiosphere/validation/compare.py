"""Compare a model series with an independent observation table."""
from pathlib import Path
import pandas as pd
from .metrics import mae, rmse, r_squared


def compare_csv(observation_csv: str, observed_column: str,
                predicted_csv: str, predicted_column: str,
                output_csv: str | None = None) -> dict:
    """Compare paired rows; datasets must already share time and unit basis.

    This helper deliberately does not interpolate or silently align timestamps.
    """
    obs = pd.read_csv(observation_csv)
    pred = pd.read_csv(predicted_csv)
    if observed_column not in obs or predicted_column not in pred:
        raise KeyError("requested observation or prediction column is missing")
    if len(obs) != len(pred):
        raise ValueError("observation and prediction files must have equal row counts")
    if "time_days" in obs and "time_days" in pred:
        if not obs["time_days"].equals(pred["time_days"]):
            raise ValueError("time_days columns must match exactly; align explicitly first")
    result = {
        "n": int(len(obs)),
        "mae": mae(obs[observed_column], pred[predicted_column]),
        "rmse": rmse(obs[observed_column], pred[predicted_column]),
    }
    try:
        result["r_squared"] = r_squared(obs[observed_column], pred[predicted_column])
    except ValueError:
        result["r_squared"] = None
    if output_csv:
        pd.DataFrame([result]).to_csv(Path(output_csv), index=False)
    return result

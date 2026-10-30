"""Metrics for comparing model predictions with independent observations."""
import numpy as np


def _paired(observed, predicted):
    obs = np.asarray(observed, dtype=float)
    pred = np.asarray(predicted, dtype=float)
    if obs.shape != pred.shape or obs.size == 0:
        raise ValueError("observed and predicted must have the same non-empty shape")
    if not np.isfinite(obs).all() or not np.isfinite(pred).all():
        raise ValueError("observed and predicted values must be finite")
    return obs.ravel(), pred.ravel()


def mae(observed, predicted) -> float:
    obs, pred = _paired(observed, predicted)
    return float(np.mean(np.abs(obs - pred)))


def rmse(observed, predicted) -> float:
    obs, pred = _paired(observed, predicted)
    return float(np.sqrt(np.mean((obs - pred) ** 2)))


def r_squared(observed, predicted) -> float:
    obs, pred = _paired(observed, predicted)
    denominator = float(np.sum((obs - np.mean(obs)) ** 2))
    if denominator == 0:
        raise ValueError("R-squared is undefined when observations are constant")
    return float(1.0 - np.sum((obs - pred) ** 2) / denominator)

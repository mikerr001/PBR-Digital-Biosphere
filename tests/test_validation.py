import numpy as np
import pytest
from pbrbiosphere.validation.metrics import mae, rmse, r_squared


def test_error_metrics_on_exact_predictions():
    observed = [1, 2, 3]
    predicted = [1, 2, 3]
    assert mae(observed, predicted) == 0
    assert rmse(observed, predicted) == 0
    assert r_squared(observed, predicted) == 1


def test_error_metrics_reject_shape_mismatch():
    with pytest.raises(ValueError):
        mae([1, 2], [1])


def test_r_squared_rejects_constant_observations():
    with pytest.raises(ValueError):
        r_squared([2, 2, 2], [2, 2, 2])

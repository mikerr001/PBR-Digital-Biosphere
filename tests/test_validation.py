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

from pbrbiosphere.validation.compare import compare_csv


def test_compare_csv_uses_exact_matching_time_grid(tmp_path):
    observed = tmp_path / "observed.csv"
    predicted = tmp_path / "predicted.csv"
    observed.write_text("time_days,biomass_gDW_L\\n0,1\\n1,2\\n", encoding="utf-8")
    predicted.write_text("time_days,biomass_gDW_L\\n0,1.1\\n1,1.9\\n", encoding="utf-8")
    result = compare_csv(str(observed), "biomass_gDW_L",
                         str(predicted), "biomass_gDW_L")
    assert result["n"] == 2
    assert result["mae"] == pytest.approx(0.1)


def test_compare_csv_rejects_misaligned_times(tmp_path):
    observed = tmp_path / "observed.csv"
    predicted = tmp_path / "predicted.csv"
    observed.write_text("time_days,value\\n0,1\\n1,2\\n", encoding="utf-8")
    predicted.write_text("time_days,value\\n0,1\\n2,2\\n", encoding="utf-8")
    with pytest.raises(ValueError):
        compare_csv(str(observed), "value", str(predicted), "value")

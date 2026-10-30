import pytest
from pbrbiosphere.sensitivity import one_at_a_time


def test_one_at_a_time_returns_parameter_sweep():
    result = one_at_a_time("mu_max", [0.1, 0.2], days=0.5, points=11)
    assert list(result["value"]) == [0.1, 0.2]
    assert len(result) == 2


def test_one_at_a_time_rejects_unknown_parameter():
    with pytest.raises(AttributeError):
        one_at_a_time("not_a_parameter", [1.0], days=0.5, points=11)

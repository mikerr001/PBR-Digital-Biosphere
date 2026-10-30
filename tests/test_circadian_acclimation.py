import numpy as np
import pytest
from pbrbiosphere.circadian.acclimation import (
    AcclimationParameters, simulate_light_acclimation,
)


def test_acclimation_moves_toward_high_light_target():
    result = simulate_light_acclimation([0, 1, 2, 3], [0, 300, 300, 300])
    assert result.acclimation_state.iloc[-1] > result.acclimation_state.iloc[0]


def test_dark_input_reduces_acclimation_state():
    result = simulate_light_acclimation([0, 12, 24, 48], [300, 0, 0, 0])
    assert result.acclimation_state.iloc[-1] < result.acclimation_state.iloc[0]


def test_state_is_bounded():
    result = simulate_light_acclimation(np.arange(0, 100), np.tile([0, 500], 50))
    assert result.acclimation_state.between(0, 1).all()


@pytest.mark.parametrize("times, light", [
    ([0, 1], [-1, 2]), ([0, 0], [1, 2]), ([0], [1]),
    ([0, float("nan")], [1, 2]),
])
def test_invalid_acclimation_inputs_rejected(times, light):
    with pytest.raises(ValueError):
        simulate_light_acclimation(times, light)


def test_invalid_parameters_rejected():
    with pytest.raises(ValueError):
        AcclimationParameters(tau_increase_hours=0).validate()

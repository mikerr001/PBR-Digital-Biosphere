import numpy as np
import pytest
from pbrbiosphere.circadian.model import (
    CircadianParameters, LightTransition, simulate_circadian,
)
from pbrbiosphere.circadian.schedules import (
    daily_light_dark, irregular_schedule, shifted_schedule,
)


def test_free_running_clock_keeps_24_hour_intrinsic_period_without_prc():
    result = simulate_circadian(72, [], CircadianParameters(), 1.0)
    assert result.iloc[-1]["phase_unwrapped_hours"] == pytest.approx(78.0)
    assert result.iloc[-1]["phase_hours"] == pytest.approx(6.0)


@pytest.mark.parametrize("period, expected", [(24.0, 78.0), (25.0, 76.08), (22.0, 84.5454545455)])
def test_intrinsic_period_controls_phase_velocity(period, expected):
    p = CircadianParameters(intrinsic_period_hours=period)
    result = simulate_circadian(72, [], p, 1.0)
    assert result.iloc[-1]["phase_unwrapped_hours"] == pytest.approx(expected)


def test_zero_prc_means_light_does_not_artificially_reset_clock():
    events = daily_light_dark(3)
    result = simulate_circadian(72, events, sample_interval_hours=1)
    assert result.iloc[-1]["phase_unwrapped_hours"] == pytest.approx(78.0)


def test_phase_response_curve_resets_phase_at_transition():
    p = CircadianParameters(light_prc_hours=(1,)*8, dark_prc_hours=(0,)*8)
    result = simulate_circadian(30, [LightTransition(0, True),
                                     LightTransition(12, False),
                                     LightTransition(24, True)], p, 1)
    assert result.loc[result.time_hours == 24, "phase_unwrapped_hours"].iloc[0] == pytest.approx(31.0)


def test_phase_and_output_are_bounded():
    result = simulate_circadian(48, daily_light_dark(2), sample_interval_hours=0.5)
    assert result.phase_hours.between(0, 24, inclusive="left").all()
    assert result.morning_output_proxy.between(0, 1).all()


def test_shifted_and_irregular_schedules_are_deterministic():
    assert shifted_schedule(4, shift_day=2, shift_hours=6)
    assert irregular_schedule(4)


@pytest.mark.parametrize("bad", [0, -1, float("nan")])
def test_invalid_duration_rejected(bad):
    with pytest.raises(ValueError):
        simulate_circadian(bad, [])


def test_invalid_prc_dimensions_rejected():
    with pytest.raises(ValueError):
        CircadianParameters(prc_bins=4).validate()


def test_transition_after_end_rejected():
    with pytest.raises(ValueError):
        simulate_circadian(10, [LightTransition(11, True)])

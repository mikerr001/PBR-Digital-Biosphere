from pbrbiosphere.circadian.experiments import run_circadian_suite


def test_standard_circadian_suite_returns_matched_cases():
    result = run_circadian_suite(days=2, sample_interval_hours=1)
    assert set(result) == {"free_running", "regular_12_12",
                           "shifted_12_12", "irregular_light"}
    assert all(len(frame) == 49 for frame in result.values())
    assert all(frame.iloc[0].phase_hours == 6.0 for frame in result.values())

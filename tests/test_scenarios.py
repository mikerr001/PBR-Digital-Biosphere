from pbrbiosphere.scenarios import run_standard_scenarios


def test_standard_scenario_suite_has_expected_cases():
    result = run_standard_scenarios(days=0.5, points=11)
    assert set(result) == {"dark", "constant_light", "light_dark_12_12",
                           "low_light_12_12", "high_light_12_12"}
    assert all(len(frame) == 11 for frame in result.values())

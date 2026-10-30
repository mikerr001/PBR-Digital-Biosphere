from pbrbiosphere.organisms.synechococcus_7942 import OBSERVATIONS, rate_per_day
from pbrbiosphere.organisms import phaeodactylum


def test_synechococcus_observations_preserve_source_conditions():
    assert len(OBSERVATIONS) == 4
    assert all(item.temperature_c == 30.0 for item in OBSERVATIONS)
    assert all(item.acclimation_hours == 72.0 for item in OBSERVATIONS)


def test_hour_to_day_conversion():
    assert rate_per_day(0.05) == 1.2


def test_phaeodactylum_not_assigned_kaiabc():
    assert phaeodactylum.CLOCK_MODEL is None

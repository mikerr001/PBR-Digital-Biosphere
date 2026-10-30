import pytest
from pbrbiosphere.biology import light_fraction, nutrient_fraction, growth_rate
from pbrbiosphere.config import ModelParameters
from pbrbiosphere.photosynthesis import platt_relative, gross_oxygen_from_carbon
from pbrbiosphere.nutrients import nutrient_limitation


def test_zero_light_gives_zero_growth():
    assert growth_rate(0.1, 2, 1, 0.1, 0, 25, ModelParameters()) == 0


def test_light_fraction_bounds():
    assert light_fraction(0, 100) == 0
    assert 0 < light_fraction(100, 100) < 1


def test_nutrient_fraction_bounds():
    assert nutrient_fraction(0, 1) == 0
    assert 0 < nutrient_fraction(1, 1) < 1


def test_invalid_light_rejected():
    with pytest.raises(ValueError):
        light_fraction(-1, 10)


def test_platt_response_zero_at_darkness_and_positive_in_light():
    assert platt_relative(0, alpha=0.02, pmax=10, beta=0.001) == 0
    assert platt_relative(100, alpha=0.02, pmax=10, beta=0.001) > 0


def test_platt_rejects_invalid_coefficients():
    with pytest.raises(ValueError):
        platt_relative(100, alpha=-1, pmax=10, beta=0)


def test_gross_oxygen_conversion():
    assert gross_oxygen_from_carbon(2.0, 1.1) == pytest.approx(2.2)


def test_liebig_minimum_nutrient_limitation():
    assert nutrient_limitation(100, 0, 0.1, 0.1) == 0

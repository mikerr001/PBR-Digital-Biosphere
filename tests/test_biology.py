import pytest
from pbrbiosphere.biology import light_fraction, nutrient_fraction
from pbrbiosphere.config import ModelParameters
from pbrbiosphere.biology import growth_rate


def test_zero_light_gives_zero_growth():
    p = ModelParameters()
    assert growth_rate(0.1, 2, 1, 0.1, 0, 25, p) == 0


def test_light_fraction_bounds():
    assert light_fraction(0, 100) == 0
    assert 0 < light_fraction(100, 100) < 1


def test_nutrient_fraction_bounds():
    assert nutrient_fraction(0, 1) == 0
    assert 0 < nutrient_fraction(1, 1) < 1


def test_invalid_light_rejected():
    with pytest.raises(ValueError):
        light_fraction(-1, 10)

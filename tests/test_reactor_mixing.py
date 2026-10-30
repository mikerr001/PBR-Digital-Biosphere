import pytest
from pbrbiosphere.reactor.mixing import two_compartment_exchange_rate
def test_exchange_moves_material_from_high_to_low_concentration():
    rate=two_compartment_exchange_rate(10,2,1,100)
    assert rate>0
    assert two_compartment_exchange_rate(2,10,1,100)<0
def test_exchange_is_zero_at_equal_concentration():
    assert two_compartment_exchange_rate(4,4,1,30)==0
def test_exchange_rate_conserves_total_inventory_by_equal_opposite_flux():
    rate=two_compartment_exchange_rate(8,2,0.5,60)
    assert -rate+rate==pytest.approx(0)
def test_invalid_mixing_inputs():
    with pytest.raises(ValueError): two_compartment_exchange_rate(1,2,1,0)

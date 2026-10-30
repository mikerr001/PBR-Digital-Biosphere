import pytest
from pbrbiosphere.habitat import HabitatInputs,HabitatState,habitat_rhs,simulate_habitat

def test_habitat_gas_balances_signs():
    i=HabitatInputs(o2_human_consumption_mmol_day=100,co2_human_generation_mmol_day=90,
                    o2_algae_net_mmol_day=120,co2_algae_net_mmol_day=-80)
    d=habitat_rhs(0,[1000,1000,500,100,10],i)
    assert d[0]==20 and d[1]==10

def test_habitat_integrates_inventory():
    s=HabitatState(1000,500,100,100,10)
    i=HabitatInputs(o2_human_consumption_mmol_day=10,o2_algae_net_mmol_day=15,
                    co2_human_generation_mmol_day=8,co2_algae_net_mmol_day=-7,
                    water_net_l_day=-1)
    r=simulate_habitat(2,3,s,i)
    assert r.iloc[-1].oxygen_mmol==pytest.approx(1010)
    assert r.iloc[-1].carbon_dioxide_mmol==pytest.approx(502)
    assert r.iloc[-1].water_l==pytest.approx(98)

def test_inventory_depletion_is_not_silently_clipped():
    s=HabitatState(5,5,5,5,5)
    i=HabitatInputs(o2_human_consumption_mmol_day=10)
    with pytest.raises(ValueError,match="exhausts"):
        simulate_habitat(1,10,s,i)

def test_invalid_negative_human_rate_rejected():
    with pytest.raises(ValueError):
        HabitatInputs(o2_human_consumption_mmol_day=-1).validate()

def test_fifteen_person_scaling_is_explicit():
    from pbrbiosphere.habitat import scale_per_person_rate
    assert scale_per_person_rate(12.5,15)==pytest.approx(187.5)
def test_occupant_scaling_rejects_invalid_count():
    from pbrbiosphere.habitat import scale_per_person_rate
    with pytest.raises(ValueError): scale_per_person_rate(12.5,-1)

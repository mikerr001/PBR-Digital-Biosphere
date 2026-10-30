import pytest
from pbrbiosphere.control import ControlLimits, SensorSnapshot, decide

@pytest.fixture
def limits():
    return ControlLimits(20,30,0.5,3.0,50,500,max_light_fraction=.8,max_gas_flow_fraction=.7,max_cooling_fraction=.6)

def snap(t=25,o=1.5,par=200,age=1,valid=True,alarm=False):
    return SensorSnapshot(t,o,par,age,valid,alarm)

def test_normal_measurements_produce_bounded_recommendations(limits):
    d=decide(snap(),limits)
    assert d.mode=="NORMAL" and all(0<=v<=1 for v in d.actions.values())
    assert d.automatic_actuation_permitted is False

def test_stale_or_invalid_sensor_fails_closed(limits):
    for s in (snap(age=99),snap(valid=False),snap(alarm=True),snap(o=None)):
        d=decide(s,limits); assert d.mode=="DEGRADED_HOLD"
        assert all(v is None for v in d.actions.values())

def test_high_temperature_suspends_light_and_requests_cooling(limits):
    d=decide(snap(t=31),limits); assert d.actions["light_fraction"]==0 and d.actions["cooling_fraction"]==.6

def test_high_oxygen_suspends_light_and_requests_exchange(limits):
    d=decide(snap(o=3.2),limits); assert d.actions["light_fraction"]==0 and d.actions["gas_flow_fraction"]==.7

def test_low_oxygen_requests_exchange(limits):
    assert decide(snap(o=.4),limits).actions["gas_flow_fraction"]==.7

def test_excess_par_suspends_additional_illumination(limits):
    assert decide(snap(par=600),limits).actions["light_fraction"]==0

def test_invalid_configuration_rejected(limits):
    with pytest.raises(ValueError): ControlLimits(30,20,.5,3,50,500).validate()

def test_nan_sensor_data_rejected(limits):
    with pytest.raises(ValueError): decide(snap(t=float("nan")),limits)

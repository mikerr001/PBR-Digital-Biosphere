import numpy as np
import pytest
from pbrbiosphere.reactor import (FlatPanelGeometry,calculate_light_field,GasTransferParameters,
 gas_transfer_rates,ideal_gas_partial_pressure_bar,ThermalParameters,thermal_temperature_rate,
 ReactorState,ReactorEnvironment,reactor_rates)
def test_geometry_closure():
 g=FlatPanelGeometry(.2,.5,.02,2,.5); assert g.calculated_liquid_volume_l==pytest.approx(2); assert g.volume_closure_relative_error==pytest.approx(0)
def test_two_sided_area():
 assert FlatPanelGeometry(.2,.5,.02,2,.5,2).illuminated_area_m2==pytest.approx(.2)
def test_optical_attenuation_profile():
 f=calculate_light_field(500,.1,1,10,.2,101)
 assert np.all(np.diff(f.irradiance_umol_m2_s)<0)
 assert f.irradiance_umol_m2_s[-1]==pytest.approx(500*np.exp(-1.02))
def test_no_attenuation_uniform():
 f=calculate_light_field(200,.1,.5,0,0)
 assert f.average_irradiance_umol_m2_s==pytest.approx(200)
def test_ideal_gas_and_transfer_direction():
 assert ideal_gas_partial_pressure_bar(100,1,298.15)==pytest.approx(2.478,rel=.01)
 p=GasTransferParameters(2,2,1,1); r=gas_transfer_rates(2,1,0,0,1,1,298.15,p)
 assert r["o2_liquid_to_gas_mmol_day"]>0 and r["co2_liquid_to_gas_mmol_day"]>0
def test_transfer_equilibrium_zero():
 amount=1/(.001*.083144626*298.15); p=GasTransferParameters(3,3,1,1)
 r=gas_transfer_rates(1,1,amount,amount,1,1,298.15,p)
 assert r["o2_liquid_to_gas_mmol_day"]==pytest.approx(0,abs=1e-10)
 assert r["co2_liquid_to_gas_mmol_day"]==pytest.approx(0,abs=1e-10)
def test_transfer_rate_units_include_liquid_volume():
 r=gas_transfer_rates(2,1,0,0,2,1,298.15,GasTransferParameters(2,3,1,1))
 assert r["o2_liquid_to_gas_mmol_day"]==pytest.approx(4)
 assert r["co2_liquid_to_gas_mmol_day"]==pytest.approx(6)
def test_thermal_directions_and_scaling():
 p=ThermalParameters(absorbed_fraction=.2)
 a=thermal_temperature_rate(25,25,100,1,10,p)
 assert a>0
 assert thermal_temperature_rate(30,25,0,1,10,ThermalParameters(overall_heat_transfer_w_k=5))<0
 assert thermal_temperature_rate(25,25,100,2,20,p)==pytest.approx(a)
def test_assembled_physics_outputs():
 g=FlatPanelGeometry(.2,.5,.02,2,.5)
 r=reactor_rates(ReactorState(.5,1,.5,10,5,25),ReactorEnvironment(300,150,22),g,GasTransferParameters(1,1,1,1),ThermalParameters(absorbed_fraction=.2),8)
 assert r["light_field"].average_irradiance_umol_m2_s<300
 assert r["temperature_rate_k_day"]>0
 assert r["mixing_dynamics_implemented"] is False
def test_invalid_geometry_or_optics_rejected():
 with pytest.raises(ValueError): FlatPanelGeometry(0,1,.1,1,1).validate()
 with pytest.raises(ValueError): calculate_light_field(-1,.1,1,1)
def test_invalid_thermal_input_rejected():
 with pytest.raises(ValueError): thermal_temperature_rate(25,20,-1,1,1,ThermalParameters())
def test_invalid_gas_input_rejected():
 with pytest.raises(ValueError): ideal_gas_partial_pressure_bar(-1,1,298)

import numpy as np
import pytest
from pbrbiosphere.config import Environment, InitialState, ModelParameters
from pbrbiosphere.integration import CoupledInitialState, run_coupled_simulation
from pbrbiosphere.reactor import FlatPanelGeometry, GasTransferParameters, ThermalParameters

def run(**kwargs):
    args = dict(days=1.0, points=51, geometry=FlatPanelGeometry(.2,.5,.02,2.0,.5),
        gas=GasTransferParameters(2.0,0.0,1.0,1.0), thermal=ThermalParameters(),
        biomass_attenuation_m2_kgdw=0.0, incident_irradiance_w_m2=0.0,
        ambient_temperature_c=25.0, params=ModelParameters(decay=0.0,respiration=0.0),
        initial=CoupledInitialState(InitialState(),0.0,25.0), environment=Environment())
    args.update(kwargs)
    return run_coupled_simulation(**args)

def test_coupled_outputs_are_finite_and_report_path_average_par():
    df=run(); assert np.isfinite(df.to_numpy()).all()
    assert (df.biomass_gDW_L >= 0).all()
    assert df.path_average_PAR_umol_m2_s.iloc[0] == pytest.approx(100.0)

def test_oxygen_phase_transfer_conserves_combined_inventory_without_biology_flux():
    df=run(gas=GasTransferParameters(3.0,0.0,1.0,1.0),
        initial=CoupledInitialState(InitialState(oxygen=2.0),0.0,25.0),
        environment=Environment(irradiance=0.0))
    assert df.total_o2_inventory_mmol.iloc[-1] == pytest.approx(df.total_o2_inventory_mmol.iloc[0],rel=2e-6,abs=2e-7)
    assert df.headspace_oxygen_mmol.iloc[-1] > 0

def test_biomass_attenuation_reduces_path_average_par():
    clear=run(biomass_attenuation_m2_kgdw=0.0)
    attenuated=run(biomass_attenuation_m2_kgdw=100.0)
    assert attenuated.path_average_PAR_umol_m2_s.iloc[0] < clear.path_average_PAR_umol_m2_s.iloc[0]

def test_geometry_mismatch_is_rejected():
    with pytest.raises(ValueError,match="volume closure"):
        run(geometry=FlatPanelGeometry(.2,.5,.03,2.0,.5))

def test_negative_physical_parameter_is_rejected():
    with pytest.raises(ValueError): run(biomass_attenuation_m2_kgdw=-1)

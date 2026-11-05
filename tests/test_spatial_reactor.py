import numpy as np
import pytest
from pbrbiosphere.spatial_reactor import (
    SpatialInitialState, SpatialReactorConfig, simulate_spatial_reactor,
)


def test_spatial_result_has_space_time_fields():
    r = simulate_spatial_reactor(60, 3, SpatialReactorConfig(cells=4, flow_m3_s=0,
                                      incident_par_umol_m2_s=0))
    assert r.success
    assert r.biomass_g_l.shape == (3, 4)
    assert r.temperature_k.shape == (3, 4)
    assert r.metadata["fidelity_tier"] == 2
    assert r.metadata["validation"] == "UNVALIDATED"


def test_dark_oxygen_does_not_increase():
    r = simulate_spatial_reactor(60, 3, SpatialReactorConfig(cells=4, flow_m3_s=0,
                                      incident_par_umol_m2_s=0),
                                 SpatialInitialState(oxygen_mmol_l=0.2))
    assert np.all(r.oxygen_mmol_l[-1] <= r.oxygen_mmol_l[0] + 1e-10)


def test_biomass_attenuates_par():
    cfg = SpatialReactorConfig(cells=3, flow_m3_s=0)
    low = simulate_spatial_reactor(10, 2, cfg, SpatialInitialState(biomass_g_l=0.1))
    high = simulate_spatial_reactor(10, 2, cfg, SpatialInitialState(biomass_g_l=1.0))
    assert np.all(high.par_umol_m2_s < low.par_umol_m2_s)


def test_invalid_mesh_size_rejected():
    with pytest.raises(ValueError, match="cells"):
        simulate_spatial_reactor(60, 2, SpatialReactorConfig(cells=2))


def test_zero_duration_rejected():
    with pytest.raises(ValueError, match="duration"):
        simulate_spatial_reactor(0, 2)

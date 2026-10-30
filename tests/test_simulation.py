import numpy as np
import pytest
from pbrbiosphere.config import InitialState, ModelParameters, Environment
from pbrbiosphere.simulate import run_simulation
from pbrbiosphere.model import rhs


def test_simulation_returns_finite_nonnegative_states():
    df = run_simulation(days=2, points=51)
    values = df.drop(columns=["time_days"]).to_numpy()
    assert np.isfinite(values).all()
    assert (values >= 0).all()


def test_zero_biomass_has_no_biomass_dependent_fluxes():
    initial = InitialState(biomass=0.0)
    df = run_simulation(days=1, points=11, initial=initial)
    assert np.allclose(df["biomass_gDW_L"], 0.0)
    assert np.allclose(df["oxygen_mmol_L"], initial.oxygen)


def test_zero_light_has_no_gross_oxygen_evolution():
    p = ModelParameters()
    env = Environment(irradiance=0.0)
    state = np.array([0.1, 2.0, 0.2, 1.0, 0.1])
    derivative = rhs(0.0, state, p, env)
    expected_respiration = p.respiration * state[0]
    assert derivative[2] == pytest.approx(-expected_respiration)


def test_zero_light_has_no_growth_when_decay_is_zero():
    env = Environment(irradiance=0.0)
    initial = InitialState()
    p = ModelParameters(decay=0.0, respiration=0.0)
    df = run_simulation(days=1, points=11, environment=env, initial=initial, params=p)
    assert np.allclose(df["biomass_gDW_L"], initial.biomass)


def test_initial_state_rejects_negative_values():
    with pytest.raises(ValueError):
        run_simulation(initial=InitialState(dic=-1))


def test_parameter_validation_rejects_invalid_quotient():
    with pytest.raises(ValueError):
        run_simulation(params=ModelParameters(photosynthetic_quotient=0))


def test_carbon_inventory_closes_in_reduced_model():
    p, s = ModelParameters(), InitialState()
    df = run_simulation(days=1, points=101, params=p, initial=s)
    total = df["dic_mmolC_L"] + p.q_c * df["biomass_gDW_L"]
    assert np.allclose(total, total.iloc[0], rtol=2e-6, atol=2e-7)


def test_nitrogen_and_phosphorus_remain_nonnegative():
    s = InitialState(nitrogen=0.001, phosphorus=0.0001)
    df = run_simulation(days=3, points=101, initial=s)
    assert (df["nitrogen_mmol_L"] >= 0).all()
    assert (df["phosphorus_mmol_L"] >= 0).all()


def test_nitrogen_and_phosphorus_inventories_close():
    p, s = ModelParameters(), InitialState()
    df = run_simulation(days=1, points=101, params=p, initial=s)
    total_n = df["nitrogen_mmol_L"] + p.q_n * df["biomass_gDW_L"]
    total_p = df["phosphorus_mmol_L"] + p.q_p * df["biomass_gDW_L"]
    assert np.allclose(total_n, total_n.iloc[0], rtol=2e-6, atol=2e-7)
    assert np.allclose(total_p, total_p.iloc[0], rtol=2e-6, atol=2e-7)


def test_light_dark_boundaries_are_integrated():
    df = run_simulation(days=3, points=301, environment=Environment(photoperiod_hours=12))
    assert np.isfinite(df.to_numpy()).all()
    assert df["time_days"].iloc[-1] == pytest.approx(3.0)

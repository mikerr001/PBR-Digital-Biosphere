import numpy as np
from pbrbiosphere.config import InitialState, ModelParameters, Environment
from pbrbiosphere.simulate import run_simulation


def test_simulation_returns_finite_nonnegative_states():
    df = run_simulation(days=2, points=51)
    values = df.drop(columns=["time_days"]).to_numpy()
    assert np.isfinite(values).all()
    assert (values >= 0).all()


def test_zero_biomass_stays_zero():
    initial = InitialState(biomass=0.0)
    df = run_simulation(days=1, points=11, initial=initial)
    assert np.allclose(df["biomass_gDW_L"], 0.0)


def test_zero_light_has_no_gross_growth():
    env = Environment(irradiance=0.0)
    initial = InitialState()
    p = ModelParameters(decay=0.0)
    df = run_simulation(days=1, points=11, environment=env, initial=initial, params=p)
    assert np.allclose(df["biomass_gDW_L"], initial.biomass)

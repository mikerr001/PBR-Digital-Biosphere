import numpy as np
import pytest
from pbrbiosphere.cfd_coupling import (
    integrate_source, mmol_l_day_to_mol_m3_s, pbr02_cell_sources,
)


def test_concentration_rate_conversion_uses_si_seconds():
    assert mmol_l_day_to_mol_m3_s(86400.0) == pytest.approx(1.0)


def test_source_bridge_preserves_fixed_quota_stoichiometry():
    from pbrbiosphere.config import ModelParameters
    p = ModelParameters(mu_max=0.2, decay=0.01, respiration=0.05)
    biomass = np.array([0.1, 0.2])
    growth = np.array([0.1, 0.1])
    src = pbr02_cell_sources(biomass, growth, p)
    expected_dic = (-growth * biomass * p.q_c
                    + p.respiration * biomass * p.respiratory_quotient) / 86400
    expected_n = -(growth * biomass * p.q_n) / 86400
    assert np.allclose(src["dic_mol_m3_s"], expected_dic)
    assert np.allclose(src["nitrogen_mol_m3_s"], expected_n)
    assert src["validation"] == "UNVALIDATED"


def test_integrated_source_is_volume_weighted_and_conservative():
    total = integrate_source(np.array([1.0, -2.0]), np.array([0.5, 0.25]))
    assert total == pytest.approx(0.0)


def test_invalid_cell_volumes_rejected():
    with pytest.raises(ValueError):
        integrate_source(np.array([1.0]), np.array([0.0]))

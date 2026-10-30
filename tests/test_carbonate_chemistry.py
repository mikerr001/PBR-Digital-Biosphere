import pytest
from pbrbiosphere.chemistry import CarbonateConstants,carbonate_speciation,co2_gas_transfer_rate
C=CarbonateConstants(4.45e-7,4.69e-11,1e-14,0.033)
def test_species_close_to_dic():
 r=carbonate_speciation(2.0,2.0,C)
 assert r["co2_mmol_l"]+r["bicarbonate_mmol_l"]+r["carbonate_mmol_l"]==pytest.approx(2.0)
 assert r["pH"]==pytest.approx(8.3,abs=0.3)
def test_co2_transfer():
 r=co2_gas_transfer_rate(1,0,2,1,298.15,0.5,C)
 assert r["co2_liquid_to_gas_mmol_day"]==pytest.approx(1.0)
def test_invalid_dic():
 with pytest.raises(ValueError): carbonate_speciation(0,1,C)
def test_invalid_alkalinity():
 with pytest.raises(ValueError): carbonate_speciation(1,-1,C)

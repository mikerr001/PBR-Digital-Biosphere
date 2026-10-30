"""Two-phase dissolved/headspace gas transfer."""
from dataclasses import dataclass
import math
@dataclass(frozen=True)
class GasTransferParameters:
    kla_o2_per_day: float
    kla_co2_per_day: float
    henry_o2_mmol_l_bar: float
    henry_co2_mmol_l_bar: float
    def validate(self):
        for n,v in vars(self).items():
            if not math.isfinite(v) or v<0: raise ValueError(f"{n} must be finite and >= 0")
def ideal_gas_partial_pressure_bar(gas_amount_mmol,headspace_volume_l,temperature_k):
    if not all(math.isfinite(v) for v in (gas_amount_mmol,headspace_volume_l,temperature_k)): raise ValueError("gas state must be finite")
    if gas_amount_mmol<0 or headspace_volume_l<=0 or temperature_k<=0: raise ValueError("invalid gas inventory, volume or temperature")
    return gas_amount_mmol*0.001*0.083144626*temperature_k/headspace_volume_l
def gas_transfer_rates(dissolved_o2_mmol_l,dissolved_co2_mmol_l,headspace_o2_mmol,headspace_co2_mmol,
                       liquid_volume_l,headspace_volume_l,temperature_k,parameters):
    """Positive rate means liquid-to-headspace transfer; units mmol/day."""
    parameters.validate()
    vals=(dissolved_o2_mmol_l,dissolved_co2_mmol_l,headspace_o2_mmol,headspace_co2_mmol,liquid_volume_l,headspace_volume_l,temperature_k)
    if not all(math.isfinite(v) for v in vals): raise ValueError("gas-transfer state must be finite")
    if min(vals[:4])<0 or liquid_volume_l<=0 or headspace_volume_l<=0 or temperature_k<=0: raise ValueError("invalid gas-transfer state")
    po=ideal_gas_partial_pressure_bar(headspace_o2_mmol,headspace_volume_l,temperature_k)
    pc=ideal_gas_partial_pressure_bar(headspace_co2_mmol,headspace_volume_l,temperature_k)
    co=parameters.henry_o2_mmol_l_bar*po
    cc=parameters.henry_co2_mmol_l_bar*pc
    no=parameters.kla_o2_per_day*(dissolved_o2_mmol_l-co)*liquid_volume_l
    nc=parameters.kla_co2_per_day*(dissolved_co2_mmol_l-cc)*liquid_volume_l
    return {"o2_liquid_to_gas_mmol_day":no,"co2_liquid_to_gas_mmol_day":nc,
            "o2_equilibrium_mmol_l":co,"co2_equilibrium_mmol_l":cc,
            "o2_partial_pressure_bar":po,"co2_partial_pressure_bar":pc}

"""Instantaneous physical-rate assembly; not coupled to biological sources."""
from dataclasses import dataclass
import math
from .geometry import FlatPanelGeometry
from .optics import calculate_light_field
from .gas_transfer import GasTransferParameters,gas_transfer_rates
from .thermal import ThermalParameters,thermal_temperature_rate
@dataclass(frozen=True)
class ReactorState:
    biomass_gdw_l: float
    dissolved_o2_mmol_l: float
    dissolved_co2_mmol_l: float
    headspace_o2_mmol: float
    headspace_co2_mmol: float
    temperature_c: float
@dataclass(frozen=True)
class ReactorEnvironment:
    surface_irradiance_umol_m2_s: float
    incident_irradiance_w_m2: float
    ambient_temperature_c: float
def reactor_rates(state,environment,geometry,gas,thermal,biomass_attenuation_m2_gdw,
                  background_attenuation_m=0.0,optical_cells=51):
    if not all(math.isfinite(v) for v in (*vars(state).values(),*vars(environment).values())): raise ValueError("reactor inputs must be finite")
    if state.biomass_gdw_l<0 or min(state.dissolved_o2_mmol_l,state.dissolved_co2_mmol_l,state.headspace_o2_mmol,state.headspace_co2_mmol)<0: raise ValueError("inventories must be nonnegative")
    if environment.surface_irradiance_umol_m2_s<0 or environment.incident_irradiance_w_m2<0: raise ValueError("irradiance must be nonnegative")
    geometry.validate()
    light=calculate_light_field(environment.surface_irradiance_umol_m2_s,geometry.optical_path_m,state.biomass_gdw_l,biomass_attenuation_m2_gdw,background_attenuation_m,optical_cells)
    transfer=gas_transfer_rates(state.dissolved_o2_mmol_l,state.dissolved_co2_mmol_l,state.headspace_o2_mmol,state.headspace_co2_mmol,geometry.liquid_volume_l,geometry.headspace_volume_l,state.temperature_c+273.15,gas)
    dtemp=thermal_temperature_rate(state.temperature_c,environment.ambient_temperature_c,environment.incident_irradiance_w_m2,geometry.illuminated_area_m2,geometry.liquid_volume_l,thermal)
    return {"light_field":light,**transfer,"temperature_rate_k_day":dtemp,
            "geometry_volume_closure_relative_error":geometry.volume_closure_relative_error,
            "mixing_dynamics_implemented":False}

"""Lumped liquid thermal balance."""
from dataclasses import dataclass
import math
@dataclass(frozen=True)
class ThermalParameters:
    liquid_density_kg_m3: float=997.0
    liquid_heat_capacity_j_kg_k: float=4180.0
    overall_heat_transfer_w_k: float=0.0
    absorbed_fraction: float=0.0
    metabolic_heat_w: float=0.0
    def validate(self):
        for n,v in vars(self).items():
            if not math.isfinite(v): raise ValueError(f"{n} must be finite")
        if self.liquid_density_kg_m3<=0 or self.liquid_heat_capacity_j_kg_k<=0: raise ValueError("density and heat capacity must be > 0")
        if self.overall_heat_transfer_w_k<0 or self.metabolic_heat_w<0: raise ValueError("heat terms must be >= 0")
        if not 0<=self.absorbed_fraction<=1: raise ValueError("absorbed_fraction must be in [0,1]")
def thermal_temperature_rate(temperature_c,ambient_temperature_c,incident_irradiance_w_m2,
                             illuminated_area_m2,liquid_volume_l,parameters):
    """Return dT/dt in K/day. Wall gradients and evaporation are omitted."""
    parameters.validate()
    vals=(temperature_c,ambient_temperature_c,incident_irradiance_w_m2,illuminated_area_m2,liquid_volume_l)
    if not all(math.isfinite(v) for v in vals): raise ValueError("thermal inputs must be finite")
    if incident_irradiance_w_m2<0 or illuminated_area_m2<=0 or liquid_volume_l<=0: raise ValueError("invalid heat input, area or volume")
    volume_m3=liquid_volume_l/1000
    capacity=parameters.liquid_density_kg_m3*volume_m3*parameters.liquid_heat_capacity_j_kg_k
    solar=incident_irradiance_w_m2*illuminated_area_m2*parameters.absorbed_fraction
    loss=parameters.overall_heat_transfer_w_k*(temperature_c-ambient_temperature_c)
    return (solar+parameters.metabolic_heat_w-loss)*86400/capacity

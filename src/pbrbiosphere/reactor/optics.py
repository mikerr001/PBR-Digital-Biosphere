"""One-dimensional Beer-Lambert light attenuation."""
from dataclasses import dataclass
import math
import numpy as np
@dataclass(frozen=True)
class LightField:
    depth_m: np.ndarray
    irradiance_umol_m2_s: np.ndarray
    average_irradiance_umol_m2_s: float
    transmitted_fraction: float
def calculate_light_field(surface_irradiance_umol_m2_s,optical_path_m,biomass_gdw_l,
                          biomass_attenuation_m2_kgdw,background_attenuation_m=0.0,cells=51):
    vals=(surface_irradiance_umol_m2_s,optical_path_m,biomass_gdw_l,biomass_attenuation_m2_kgdw,background_attenuation_m)
    if not all(math.isfinite(v) for v in vals): raise ValueError("optical inputs must be finite")
    if surface_irradiance_umol_m2_s<0 or optical_path_m<=0 or biomass_gdw_l<0: raise ValueError("invalid light, path or biomass")
    if biomass_attenuation_m2_kgdw<0 or background_attenuation_m<0: raise ValueError("attenuation must be >= 0")
    if not isinstance(cells,int) or cells<2: raise ValueError("cells must be integer >= 2")
    z=np.linspace(0,optical_path_m,cells)
    k=biomass_attenuation_m2_kgdw*biomass_gdw_l+background_attenuation_m
    light=surface_irradiance_umol_m2_s*np.exp(-k*z)
    avg=float(np.trapz(light,z)/optical_path_m)
    trans=float(light[-1]/surface_irradiance_umol_m2_s) if surface_irradiance_umol_m2_s>0 else math.exp(-k*optical_path_m)
    return LightField(z,light,avg,trans)

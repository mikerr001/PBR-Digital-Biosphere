"""Freshwater carbonate equilibrium for a DIC/alkalinity state."""
from dataclasses import dataclass
import math
from scipy.optimize import brentq

@dataclass(frozen=True)
class CarbonateConstants:
    """Condition-specific constants supplied for the culture conditions."""
    k1_mol_l: float
    k2_mol_l: float
    kw_mol2_l2: float
    henry_co2_mmol_l_bar: float
    def validate(self):
        for name,value in vars(self).items():
            if not math.isfinite(value) or value<=0: raise ValueError(f"{name} must be finite and > 0")

def _species(dic,h,k1,k2):
    den=h*h+k1*h+k1*k2
    return dic*h*h/den,dic*k1*h/den,dic*k1*k2/den

def carbonate_speciation(dic_mmol_l,alkalinity_mmol_eq_l,constants):
    """Solve pH using carbonate-only freshwater alkalinity.

    Excludes phosphate, silicate, borate, ammonia, organic alkalinity,
    activity corrections, salinity effects, ion pairing and kinetic hydration.
    """
    constants.validate()
    if not math.isfinite(dic_mmol_l) or dic_mmol_l<=0: raise ValueError("DIC must be finite and > 0 mmol/L")
    if not math.isfinite(alkalinity_mmol_eq_l) or alkalinity_mmol_eq_l<0: raise ValueError("alkalinity must be finite and >= 0")
    k1,k2,kw=constants.k1_mol_l,constants.k2_mol_l,constants.kw_mol2_l2
    def residual(ph):
        h=10.0**(-ph); _,b,c=_species(dic_mmol_l,h,k1,k2)
        return b+2*c+(kw/h-h)*1000-alkalinity_mmol_eq_l
    lo,hi=2.0,12.0
    if residual(lo)*residual(hi)>0: raise ValueError("DIC/alkalinity pair has no pH root in range 2–12")
    ph=brentq(residual,lo,hi,xtol=1e-12)
    co2,bicarb,carb=_species(dic_mmol_l,10.0**(-ph),k1,k2)
    return {"pH":ph,"co2_mmol_l":co2,"bicarbonate_mmol_l":bicarb,
            "carbonate_mmol_l":carb,"dic_reconstructed_mmol_l":co2+bicarb+carb,
            "scope":"carbonate-only freshwater equilibrium"}

def co2_gas_transfer_rate(co2_mmol_l,headspace_co2_mmol,liquid_volume_l,headspace_volume_l,temperature_k,kla_per_day,constants):
    """Signed molecular CO2 transfer; positive is liquid to gas, mmol/day."""
    constants.validate()
    v=(co2_mmol_l,headspace_co2_mmol,liquid_volume_l,headspace_volume_l,temperature_k,kla_per_day)
    if not all(math.isfinite(x) for x in v): raise ValueError("inputs must be finite")
    if co2_mmol_l<0 or headspace_co2_mmol<0 or kla_per_day<0: raise ValueError("concentrations and kLa must be >= 0")
    if liquid_volume_l<=0 or headspace_volume_l<=0 or temperature_k<=0: raise ValueError("volumes and absolute temperature must be > 0")
    pressure=headspace_co2_mmol*0.001*0.083144626*temperature_k/headspace_volume_l
    equilibrium=constants.henry_co2_mmol_l_bar*pressure
    return {"co2_liquid_to_gas_mmol_day":kla_per_day*(co2_mmol_l-equilibrium)*liquid_volume_l,
            "co2_equilibrium_mmol_l":equilibrium,"co2_partial_pressure_bar":pressure}

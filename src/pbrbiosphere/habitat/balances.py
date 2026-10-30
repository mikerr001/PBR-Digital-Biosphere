"""Lumped regenerative-habitat inventory balances.

All gas rates are mmol/day for the entire habitat. Crop/algal fluxes are
signed net transfers into the habitat atmosphere. Human/microbial demands
are positive consumption or generation rates. No oxygen safety claim follows
from these equations; physiological demand, mixing, leakage and sensor error
must be independently specified and validated.
"""
from dataclasses import dataclass
import math
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

@dataclass(frozen=True)
class HabitatState:
    oxygen_mmol: float
    carbon_dioxide_mmol: float
    water_l: float
    nitrogen_mmol: float
    phosphorus_mmol: float
    def validate(self):
        for k,v in vars(self).items():
            if not math.isfinite(v) or v < 0: raise ValueError(f"{k} must be finite and >= 0")

@dataclass(frozen=True)
class HabitatInputs:
    """Explicit whole-habitat rates; no per-person defaults are embedded.

    o2_human_consumption_mmol_day and co2_human_generation_mmol_day are
    aggregate occupant rates supplied by the study designer. Crop/algal
    gas rates are signed net atmospheric fluxes: positive adds O2 or CO2.
    Water/nutrient rates are net inventory changes in L/day and mmol/day.
    """
    o2_human_consumption_mmol_day: float = 0.0
    co2_human_generation_mmol_day: float = 0.0
    o2_microbe_consumption_mmol_day: float = 0.0
    co2_microbe_generation_mmol_day: float = 0.0
    o2_crop_net_mmol_day: float = 0.0
    co2_crop_net_mmol_day: float = 0.0
    o2_algae_net_mmol_day: float = 0.0
    co2_algae_net_mmol_day: float = 0.0
    o2_leak_loss_mmol_day: float = 0.0
    co2_leak_loss_mmol_day: float = 0.0
    water_net_l_day: float = 0.0
    nitrogen_net_mmol_day: float = 0.0
    phosphorus_net_mmol_day: float = 0.0
    def validate(self):
        for k,v in vars(self).items():
            if not math.isfinite(v): raise ValueError(f"{k} must be finite")
        for k in ("o2_human_consumption_mmol_day","co2_human_generation_mmol_day",
                  "o2_microbe_consumption_mmol_day","co2_microbe_generation_mmol_day",
                  "o2_leak_loss_mmol_day","co2_leak_loss_mmol_day"):
            if getattr(self,k)<0: raise ValueError(f"{k} must be >= 0")

def habitat_rhs(_t, y, inputs):
    """State derivatives: mmol/day for gases/nutrients; L/day for water."""
    inputs.validate()
    o2,co2,water,n,p=y
    d_o2=(inputs.o2_crop_net_mmol_day+inputs.o2_algae_net_mmol_day
          -inputs.o2_human_consumption_mmol_day-inputs.o2_microbe_consumption_mmol_day
          -inputs.o2_leak_loss_mmol_day)
    d_co2=(inputs.co2_crop_net_mmol_day+inputs.co2_algae_net_mmol_day
           +inputs.co2_human_generation_mmol_day+inputs.co2_microbe_generation_mmol_day
           -inputs.co2_leak_loss_mmol_day)
    return np.array([d_o2,d_co2,inputs.water_net_l_day,
                     inputs.nitrogen_net_mmol_day,inputs.phosphorus_net_mmol_day],dtype=float)

def simulate_habitat(days, points, initial, inputs):
    """Integrate a constant-flux scenario; not a closed-loop ecosystem model."""
    if not math.isfinite(days) or days<=0 or not isinstance(points,int) or points<2:
        raise ValueError("days must be finite > 0 and points integer >= 2")
    initial.validate(); inputs.validate()
    y0=np.array([initial.oxygen_mmol,initial.carbon_dioxide_mmol,initial.water_l,
                 initial.nitrogen_mmol,initial.phosphorus_mmol],dtype=float)
    t=np.linspace(0,days,points)
    sol=solve_ivp(lambda tt,yy:habitat_rhs(tt,yy,inputs),(0,days),y0,t_eval=t,
                  method="RK45",rtol=1e-9,atol=1e-10)
    if not sol.success: raise RuntimeError(sol.message)
    if np.any(sol.y < -1e-7): raise ValueError("scenario exhausts an inventory; model cannot continue with negative stock")
    a=np.maximum(sol.y,0)
    return pd.DataFrame({"time_days":sol.t,"oxygen_mmol":a[0],"carbon_dioxide_mmol":a[1],
                         "water_l":a[2],"nitrogen_mmol":a[3],"phosphorus_mmol":a[4]})

def scale_per_person_rate(per_person_rate, occupants):
    """Scale a sourced per-person flux; no default physiological rate is assumed."""
    if not math.isfinite(per_person_rate): raise ValueError("per_person_rate must be finite")
    if not isinstance(occupants,int) or occupants<0: raise ValueError("occupants must be an integer >= 0")
    return per_person_rate*occupants

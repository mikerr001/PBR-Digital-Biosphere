"""Dynamic PBR-02/PBR-04 coupling with explicit phase and unit boundaries.

CO2 gas transfer is deliberately not coupled: PBR-02 stores lumped DIC,
whereas PBR-04 uses molecular dissolved CO2. Equating them without carbonate
speciation and alkalinity would be chemically incorrect.
"""
from dataclasses import dataclass
import math
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from ..config import Environment, InitialState, ModelParameters
from ..model import rhs as biology_rhs
from ..simulate import _forcing_boundaries
from ..reactor.geometry import FlatPanelGeometry
from ..reactor.optics import calculate_light_field
from ..reactor.gas_transfer import GasTransferParameters, gas_transfer_rates
from ..reactor.thermal import ThermalParameters, thermal_temperature_rate

@dataclass(frozen=True)
class CoupledInitialState:
    """PBR-02 initial pools plus headspace oxygen and liquid temperature."""
    biology: InitialState = InitialState()
    headspace_oxygen_mmol: float = 0.0
    temperature_c: float = 25.0
    def validate(self):
        self.biology.validate()
        if not math.isfinite(self.headspace_oxygen_mmol) or self.headspace_oxygen_mmol < 0:
            raise ValueError("headspace_oxygen_mmol must be finite and >= 0")
        if not math.isfinite(self.temperature_c) or self.temperature_c <= -273.15:
            raise ValueError("temperature_c must be finite and above absolute zero")

def run_coupled_simulation(days: float, points: int, geometry: FlatPanelGeometry,
    gas: GasTransferParameters, thermal: ThermalParameters,
    biomass_attenuation_m2_kgdw: float, incident_irradiance_w_m2: float,
    ambient_temperature_c: float, *, background_attenuation_m: float = 0.0,
    geometry_tolerance: float = 0.05, params: ModelParameters | None = None,
    initial: CoupledInitialState | None = None,
    environment: Environment | None = None) -> pd.DataFrame:
    """Integrate biology with path-average PAR, O2 phase transfer and heat.

    Time is days; PAR is umol photons m-2 s-1; gas transfer is mmol/day.
    Carbon gas transfer is intentionally disabled pending carbonate chemistry.
    """
    if not math.isfinite(days) or days <= 0 or not isinstance(points, int) or points < 2:
        raise ValueError("days must be finite and > 0; points must be integer >= 2")
    checks = (("geometry_tolerance", geometry_tolerance, 0),
              ("biomass_attenuation_m2_kgdw", biomass_attenuation_m2_kgdw, 0),
              ("background_attenuation_m", background_attenuation_m, 0),
              ("incident_irradiance_w_m2", incident_irradiance_w_m2, 0))
    for name, value, minimum in checks:
        if not math.isfinite(value) or value < minimum:
            raise ValueError(f"{name} must be finite and >= {minimum}")
    if not math.isfinite(ambient_temperature_c) or ambient_temperature_c <= -273.15:
        raise ValueError("ambient_temperature_c must be finite and above absolute zero")
    p, s, env = params or ModelParameters(), initial or CoupledInitialState(), environment or Environment()
    p.validate(); s.validate(); env.validate(); geometry.validate(); gas.validate(); thermal.validate()
    if geometry.volume_closure_relative_error > geometry_tolerance:
        raise ValueError("geometry volume closure exceeds configured tolerance")
    vl = geometry.liquid_volume_l
    # X, lumped DIC, dissolved O2, N, P, headspace O2, liquid temperature.
    y0 = np.array([s.biology.biomass, s.biology.dic, s.biology.oxygen,
        s.biology.nitrogen, s.biology.phosphorus, s.headspace_oxygen_mmol,
        s.temperature_c], dtype=float)

    def evaluate(t, y):
        x, dic, o2l, n, phos, o2g, temp = map(float, y)
        if min(x, dic, o2l, n, phos, o2g) < -1e-7:
            raise ValueError("coupled state contains a materially negative inventory")
        if temp <= -273.15:
            raise ValueError("integrated temperature reached absolute zero")
        x, dic, o2l, n, phos, o2g = [max(0.0, v) for v in (x, dic, o2l, n, phos, o2g)]
        hour = (t * 24.0) % env.day_hours
        incident_par = env.irradiance if hour < env.photoperiod_hours else 0.0
        light = calculate_light_field(incident_par, geometry.optical_path_m, x,
            biomass_attenuation_m2_kgdw, background_attenuation_m)
        local_env = Environment(temp, light.average_irradiance_umol_m2_s,
            env.photoperiod_hours, env.day_hours)
        bio = biology_rhs(t, np.array([x, dic, o2l, n, phos]), p, local_env)
        transfer = gas_transfer_rates(o2l, 0.0, o2g, 0.0, vl,
            geometry.headspace_volume_l, temp + 273.15, gas)
        no2 = transfer["o2_liquid_to_gas_mmol_day"]
        dtemp = thermal_temperature_rate(temp, ambient_temperature_c,
            incident_irradiance_w_m2, geometry.illuminated_area_m2, vl, thermal)
        dy = np.array([bio[0], bio[1], bio[2] - no2 / vl, bio[3], bio[4], no2, dtemp])
        return dy, light.average_irradiance_umol_m2_s, no2

    def fun(t, y): return evaluate(t, y)[0]
    sample = np.linspace(0.0, days, points)
    all_t, all_y, current = [], [], y0.copy()
    for left, right in zip(_forcing_boundaries(days, env)[:-1], _forcing_boundaries(days, env)[1:]):
        local = sample[(sample >= left - 1e-12) & (sample <= right + 1e-12)]
        if len(local) == 0 or abs(local[0] - left) > 1e-10: local = np.insert(local, 0, left)
        if abs(local[-1] - right) > 1e-10: local = np.append(local, right)
        sol = solve_ivp(fun, (left, right), current, t_eval=local, method="RK45",
            rtol=1e-8, atol=1e-10, max_step=max((right-left)/20.0, 1e-6))
        if not sol.success: raise RuntimeError(sol.message)
        if np.any(sol.y[:6] < -1e-7): raise RuntimeError("integration produced a materially negative inventory")
        segment = sol.y.copy(); segment[:6] = np.maximum(segment[:6], 0.0)
        start = 1 if all_t and abs(all_t[-1] - sol.t[0]) < 1e-10 else 0
        all_t.extend(sol.t[start:].tolist()); all_y.extend(segment[:, start:].T.tolist())
        current = segment[:, -1].copy()
    raw = pd.DataFrame(all_y, columns=["biomass_gDW_L", "dic_mmolC_L",
        "dissolved_oxygen_mmol_L", "nitrogen_mmol_L", "phosphorus_mmol_L",
        "headspace_oxygen_mmol", "temperature_C"])
    raw.insert(0, "time_days", all_t); raw = raw.drop_duplicates("time_days").sort_values("time_days")
    result = {"time_days": sample}
    for col in raw.columns[1:]: result[col] = np.interp(sample, raw["time_days"], raw[col])
    df = pd.DataFrame(result)
    light_values, transfer_values = [], []
    for row in df.itertuples(index=False):
        state = np.array([row.biomass_gDW_L, row.dic_mmolC_L, row.dissolved_oxygen_mmol_L,
            row.nitrogen_mmol_L, row.phosphorus_mmol_L, row.headspace_oxygen_mmol, row.temperature_C])
        _, lv, tv = evaluate(row.time_days, state); light_values.append(lv); transfer_values.append(tv)
    df["path_average_PAR_umol_m2_s"] = light_values
    df["o2_liquid_to_gas_mmol_day"] = transfer_values
    df["total_o2_inventory_mmol"] = df["dissolved_oxygen_mmol_L"] * vl + df["headspace_oxygen_mmol"]
    df["geometry_volume_closure_relative_error"] = geometry.volume_closure_relative_error
    return df

"""Deterministic, bounded supervisory controller for bench-scale PBR experiments.

This is not model-predictive control, a safety interlock, or an actuator driver.
It produces auditable recommendations from measured values and user-supplied
operating bands. No default biological setpoints are asserted as universal.
"""
from dataclasses import dataclass, asdict
from typing import Optional
import math

@dataclass(frozen=True)
class ControlLimits:
    """Experiment-specific bands and actuator limits; user must source these."""
    temperature_low_c: float
    temperature_high_c: float
    dissolved_o2_low_mmol_l: float
    dissolved_o2_high_mmol_l: float
    par_low_umol_m2_s: float
    par_high_umol_m2_s: float
    max_light_fraction: float = 1.0
    max_gas_flow_fraction: float = 1.0
    max_cooling_fraction: float = 1.0
    deadband_fraction: float = 0.05
    max_sensor_age_s: float = 30.0
    def validate(self):
        vals=asdict(self)
        if not all(math.isfinite(v) for v in vals.values()): raise ValueError("all control limits must be finite")
        if self.temperature_low_c >= self.temperature_high_c: raise ValueError("temperature band is inverted")
        if self.dissolved_o2_low_mmol_l < 0 or self.dissolved_o2_low_mmol_l >= self.dissolved_o2_high_mmol_l: raise ValueError("invalid dissolved oxygen band")
        if self.par_low_umol_m2_s < 0 or self.par_low_umol_m2_s >= self.par_high_umol_m2_s: raise ValueError("invalid PAR band")
        for n in ("max_light_fraction","max_gas_flow_fraction","max_cooling_fraction"):
            if not 0 <= getattr(self,n) <= 1: raise ValueError(f"{n} must be in [0,1]")
        if not 0 <= self.deadband_fraction < .5: raise ValueError("deadband_fraction must be in [0,0.5)")
        if self.max_sensor_age_s <= 0: raise ValueError("max_sensor_age_s must be > 0")

@dataclass(frozen=True)
class SensorSnapshot:
    """Single synchronized measurement set; age is measured at decision time."""
    temperature_c: Optional[float]
    dissolved_o2_mmol_l: Optional[float]
    par_umol_m2_s: Optional[float]
    age_s: float
    valid: bool = True
    alarm: bool = False

@dataclass(frozen=True)
class ControlDecision:
    mode: str
    actions: dict
    reasons: tuple[str, ...]
    requires_operator_confirmation: bool = True
    automatic_actuation_permitted: bool = False

def _finite_or_none(v): return v is None or math.isfinite(v)

def decide(snapshot: SensorSnapshot, limits: ControlLimits) -> ControlDecision:
    """Return bounded recommendations; fail closed on stale, missing or bad data.

    The controller does not actuate. Values are dimensionless 0..1 fractions,
    not calibrated device commands. CO2 dosing is intentionally not controlled.
    """
    limits.validate()
    vals=(snapshot.temperature_c,snapshot.dissolved_o2_mmol_l,snapshot.par_umol_m2_s)
    if not math.isfinite(snapshot.age_s) or snapshot.age_s < 0 or not all(_finite_or_none(v) for v in vals):
        raise ValueError("sensor age and supplied readings must be finite")
    missing=[n for n,v in zip(("temperature","dissolved_oxygen","PAR"),vals) if v is None]
    if not snapshot.valid or snapshot.alarm or snapshot.age_s > limits.max_sensor_age_s or missing:
        why=[]
        if not snapshot.valid: why.append("sensor quality flag is invalid")
        if snapshot.alarm: why.append("sensor alarm is active")
        if snapshot.age_s > limits.max_sensor_age_s: why.append("sensor snapshot is stale")
        if missing: why.append("missing readings: "+", ".join(missing))
        return ControlDecision("DEGRADED_HOLD", {"light_fraction":None,"gas_flow_fraction":None,"cooling_fraction":None}, tuple(why))
    if snapshot.dissolved_o2_mmol_l < 0 or snapshot.par_umol_m2_s < 0 or snapshot.temperature_c <= -273.15:
        return ControlDecision("DEGRADED_HOLD", {"light_fraction":None,"gas_flow_fraction":None,"cooling_fraction":None}, ("physically invalid sensor value",))
    actions={"light_fraction":limits.max_light_fraction,"gas_flow_fraction":0.0,"cooling_fraction":0.0}
    reasons=[]
    t=snapshot.temperature_c; o=snapshot.dissolved_o2_mmol_l; par=snapshot.par_umol_m2_s
    t_margin=(limits.temperature_high_c-limits.temperature_low_c)*limits.deadband_fraction
    o_margin=(limits.dissolved_o2_high_mmol_l-limits.dissolved_o2_low_mmol_l)*limits.deadband_fraction
    p_margin=(limits.par_high_umol_m2_s-limits.par_low_umol_m2_s)*limits.deadband_fraction
    if t >= limits.temperature_high_c:
        actions["light_fraction"]=0.0; actions["cooling_fraction"]=limits.max_cooling_fraction
        reasons.append("temperature at/above upper limit: suspend illumination and request configured cooling")
    elif t > limits.temperature_high_c-t_margin:
        actions["light_fraction"]=min(actions["light_fraction"],.5*limits.max_light_fraction); actions["cooling_fraction"]=limits.max_cooling_fraction
        reasons.append("temperature approaching upper limit: reduce illumination and request cooling")
    elif t <= limits.temperature_low_c:
        actions["light_fraction"]=0.0; reasons.append("temperature at/below lower limit: suspend illumination; no heater is assumed")
    elif t < limits.temperature_low_c+t_margin:
        actions["light_fraction"]=min(actions["light_fraction"],.5*limits.max_light_fraction)
        reasons.append("temperature approaching lower limit: limit illumination pending thermal review")
    if o <= limits.dissolved_o2_low_mmol_l:
        actions["gas_flow_fraction"]=limits.max_gas_flow_fraction; reasons.append("dissolved O2 at/below lower limit: request configured gas exchange")
    elif o < limits.dissolved_o2_low_mmol_l+o_margin:
        actions["gas_flow_fraction"]=.5*limits.max_gas_flow_fraction; reasons.append("dissolved O2 approaching lower limit: request moderate gas exchange")
    elif o >= limits.dissolved_o2_high_mmol_l:
        actions["light_fraction"]=0.0; actions["gas_flow_fraction"]=limits.max_gas_flow_fraction
        reasons.append("dissolved O2 at/above upper limit: suspend illumination and request gas exchange")
    elif o > limits.dissolved_o2_high_mmol_l-o_margin:
        actions["light_fraction"]=min(actions["light_fraction"],.5*limits.max_light_fraction); actions["gas_flow_fraction"]=.5*limits.max_gas_flow_fraction
        reasons.append("dissolved O2 approaching upper limit: reduce illumination and request moderate gas exchange")
    if par > limits.par_high_umol_m2_s+p_margin:
        actions["light_fraction"]=0.0; reasons.append("PAR exceeds upper band: suspend additional illumination and inspect source")
    elif par > limits.par_high_umol_m2_s:
        actions["light_fraction"]=min(actions["light_fraction"],.5*limits.max_light_fraction); reasons.append("PAR above configured band: reduce illumination")
    elif par < limits.par_low_umol_m2_s-p_margin:
        reasons.append("PAR below configured band: inspect sensor, optics and source before increasing light")
    if not reasons: reasons.append("measurements within configured bands; maintain current measured settings")
    mode="LIMIT" if actions["light_fraction"]==0.0 or actions["cooling_fraction"]>0 else "NORMAL"
    return ControlDecision(mode,actions,tuple(reasons))

"""Numerical integration and result export."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from .config import Environment, InitialState, ModelParameters
from .model import rhs


def run_simulation(days: float = 5.0, points: int = 501,
                   params: ModelParameters | None = None,
                   initial: InitialState | None = None,
                   environment: Environment | None = None) -> pd.DataFrame:
    if days <= 0 or points < 2:
        raise ValueError("days must be > 0 and points must be >= 2")
    p = params or ModelParameters()
    s = initial or InitialState()
    env = environment or Environment()
    y0 = [s.biomass, s.dic, s.oxygen, s.nitrogen, s.phosphorus]
    times = np.linspace(0.0, days, points)
    sol = solve_ivp(lambda t, y: rhs(t, y, p, env), (0.0, days), y0,
                    t_eval=times, method="RK45", rtol=1e-7, atol=1e-9)
    if not sol.success:
        raise RuntimeError(sol.message)
    if np.any(sol.y < -1e-7):
        raise RuntimeError("Integration produced a materially negative state")
    data = {"time_days": sol.t}
    for i, name in enumerate(("biomass_gDW_L", "dic_mmolC_L", "oxygen_mmol_L",
                              "nitrogen_mmol_L", "phosphorus_mmol_L")):
        data[name] = np.maximum(sol.y[i], 0.0)
    return pd.DataFrame(data)


def save_results(df: pd.DataFrame, directory: str = "results") -> Path:
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "baseline_simulation.csv"
    df.to_csv(csv_path, index=False)
    return csv_path

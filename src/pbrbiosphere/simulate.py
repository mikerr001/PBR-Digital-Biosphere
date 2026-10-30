"""Numerical integration with light-transition segmentation and CSV export."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from .config import Environment, InitialState, ModelParameters
from .model import rhs


def _forcing_boundaries(days: float, env: Environment) -> list[float]:
    """Return day/night discontinuities so the solver does not step across them."""
    cycle = env.day_hours / 24.0
    light_duration = env.photoperiod_hours / 24.0
    boundaries = {0.0, days}
    cycle_index = 0
    while cycle_index * cycle < days:
        start = cycle_index * cycle
        for point in (start + light_duration, start + cycle):
            if 0.0 < point < days:
                boundaries.add(point)
        cycle_index += 1
    return sorted(boundaries)


def run_simulation(days: float = 5.0, points: int = 501,
                   params: ModelParameters | None = None,
                   initial: InitialState | None = None,
                   environment: Environment | None = None) -> pd.DataFrame:
    if days <= 0 or points < 2:
        raise ValueError("days must be > 0 and points must be >= 2")
    p, s, env = params or ModelParameters(), initial or InitialState(), environment or Environment()
    p.validate()
    s.validate()
    env.validate()
    y0 = np.array([s.biomass, s.dic, s.oxygen, s.nitrogen, s.phosphorus], dtype=float)
    sample_times = np.linspace(0.0, days, points)
    all_t, all_y = [], []
    current = y0.copy()
    boundaries = _forcing_boundaries(days, env)

    for left, right in zip(boundaries[:-1], boundaries[1:]):
        local = sample_times[(sample_times >= left - 1e-12) & (sample_times <= right + 1e-12)]
        if len(local) == 0 or abs(local[0] - left) > 1e-10:
            local = np.insert(local, 0, left)
        if abs(local[-1] - right) > 1e-10:
            local = np.append(local, right)
        sol = solve_ivp(lambda t, y: rhs(t, y, p, env), (left, right), current,
                        t_eval=local, method="RK45", rtol=1e-8, atol=1e-10,
                        max_step=max((right - left) / 20.0, 1e-6))
        if not sol.success:
            raise RuntimeError(sol.message)
        if np.any(sol.y < -1e-7):
            raise RuntimeError("Integration produced a materially negative state")
        segment_y = np.maximum(sol.y, 0.0)
        start = 1 if all_t and abs(all_t[-1] - sol.t[0]) < 1e-10 else 0
        all_t.extend(sol.t[start:].tolist())
        all_y.extend(segment_y[:, start:].T.tolist())
        current = segment_y[:, -1].copy()

    raw = pd.DataFrame(all_y, columns=["biomass_gDW_L", "dic_mmolC_L", "oxygen_mmol_L",
                                       "nitrogen_mmol_L", "phosphorus_mmol_L"])
    raw.insert(0, "time_days", all_t)
    raw = raw.drop_duplicates("time_days").sort_values("time_days")
    output = {"time_days": sample_times}
    for column in raw.columns[1:]:
        output[column] = np.interp(sample_times, raw["time_days"], raw[column])
    return pd.DataFrame(output)


def save_results(df: pd.DataFrame, directory: str = "results") -> Path:
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "baseline_simulation.csv"
    df.to_csv(path, index=False)
    return path

"""Plot simulation outputs."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def plot_results(df: pd.DataFrame, directory: str = "results/figures") -> list[Path]:
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    columns = [
        ("biomass_gDW_L", "Biomass (g dry weight / L)", "biomass.png"),
        ("oxygen_mmol_L", "Dissolved oxygen (mmol / L)", "oxygen.png"),
        ("dic_mmolC_L", "Dissolved inorganic carbon (mmol C / L)", "dic.png"),
    ]
    paths = []
    for col, ylabel, filename in columns:
        fig, ax = plt.subplots()
        ax.plot(df["time_days"], df[col])
        ax.set_xlabel("Time (days)")
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        path = out / filename
        fig.savefig(path, dpi=160)
        plt.close(fig)
        paths.append(path)
    return paths

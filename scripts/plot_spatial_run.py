#!/usr/bin/env python3
"""Plot spatial PBR run profiles and space-time heatmaps."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


FIELDS = [
    ("biomass_g_l", "Biomass", "g dry weight / L"),
    ("dic_mmol_l", "Dissolved inorganic carbon", "mmol C / L"),
    ("oxygen_mmol_l", "Dissolved oxygen", "mmol O2 / L"),
    ("nitrogen_mmol_l", "Nitrogen", "mmol N / L"),
    ("phosphorus_mmol_l", "Phosphorus", "mmol P / L"),
    ("temperature_k", "Temperature", "K"),
]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Run directory containing fields.npz")
    parser.add_argument("--output-dir", type=Path, help="Output directory (defaults to run directory)")
    args = parser.parse_args(argv)
    source = args.run_dir / "fields.npz"
    if not source.is_file():
        parser.error(f"Missing {source}")
    out = args.output_dir or args.run_dir
    out.mkdir(parents=True, exist_ok=True)
    with np.load(source, allow_pickle=False) as data:
        x, time = data["x_m"], data["time_s"]
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        fig.suptitle(f"PBR Digital Biosphere — spatial profiles ({time[-1] / 3600:.2f} h)")
        for ax, (key, title, unit) in zip(axes.flat, FIELDS):
            field = data[key]
            ax.plot(x, field[0], "--", label="Initial")
            ax.plot(x, field[-1], label="Final")
            ax.set(title=title, xlabel="Axial position (m)", ylabel=unit)
            ax.grid(True, alpha=0.3)
            ax.legend()
        fig.tight_layout()
        profiles = out / "spatial_profiles.png"
        fig.savefig(profiles, dpi=160, bbox_inches="tight")
        plt.close(fig)

        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        fig.suptitle("PBR Digital Biosphere — space-time fields")
        for ax, (key, title, unit) in zip(axes.flat, FIELDS):
            mesh = ax.pcolormesh(x, time / 3600, data[key], shading="auto")
            ax.set(title=title, xlabel="Axial position (m)", ylabel="Time (h)")
            fig.colorbar(mesh, ax=ax, label=unit)
        fig.tight_layout()
        heatmaps = out / "space_time_heatmaps.png"
        fig.savefig(heatmaps, dpi=160, bbox_inches="tight")
        plt.close(fig)
    print(f"Saved: {profiles}")
    print(f"Saved: {heatmaps}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

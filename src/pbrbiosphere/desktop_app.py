"""Lightweight desktop interface for the 1-D spatial photobioreactor model."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .config import ModelParameters
from .run_artifacts import write_spatial_result
from .spatial_reactor import (
    SpatialInitialState, SpatialReactorConfig, simulate_spatial_reactor,
)
from .organisms.registry import get_organism, require_executable_organism


class SimulatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("PBR Digital Biosphere — Spatial Reactor Simulator")
        root.geometry("1180x790")
        root.minsize(940, 650)
        self.vars = {
            "duration_h": tk.StringVar(value="24"),
            "output_points": tk.StringVar(value="49"),
            "cells": tk.StringVar(value="20"),
            "length_m": tk.StringVar(value="1.0"),
            "cross_section_m2": tk.StringVar(value="0.01"),
            "flow_m3_s": tk.StringVar(value="0.00001"),
            "dispersion_m2_s": tk.StringVar(value="0.00001"),
            "incident_par": tk.StringVar(value="150"),
            "optical_path_m": tk.StringVar(value="0.05"),
            "kLa_o2_s": tk.StringVar(value="0.00002"),
            "biomass": tk.StringVar(value="0.1"),
            "dic": tk.StringVar(value="2.0"),
            "oxygen": tk.StringVar(value="0.2"),
            "nitrogen": tk.StringVar(value="1.0"),
            "phosphorus": tk.StringVar(value="0.1"),
            "temperature_k": tk.StringVar(value="298.15"),
        }
        self.organism_var = tk.StringVar(value="generic_reduced_demo")
        self._build()
        self._set_status("Ready. Values are illustrative; this model is not experimentally validated.")

    def _build(self):
        outer = ttk.Frame(self.root, padding=10)
        outer.pack(fill="both", expand=True)
        title = ttk.Label(outer, text="PBR DIGITAL BIOSPHERE", font=("Segoe UI", 17, "bold"))
        title.pack(anchor="w")
        ttk.Label(
            outer,
            text="Tier-2 1-D spatial reactor • advection/dispersion • reduced biology • optical attenuation",
        ).pack(anchor="w", pady=(0, 8))

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True)
        controls = ttk.LabelFrame(body, text="Reactor and operating conditions", padding=10)
        controls.pack(side="left", fill="y", padx=(0, 10))
        plot_frame = ttk.LabelFrame(body, text="Simulation results", padding=6)
        plot_frame.pack(side="left", fill="both", expand=True)

        ttk.Label(controls, text="Organism model").grid(row=0, column=0, sticky="w", pady=2)
        organism_box = ttk.Combobox(
            controls, textvariable=self.organism_var, state="readonly", width=27,
            values=("generic_reduced_demo", "synechococcus_elongatus_pcc7942", "phaeodactylum_tricornutum"),
        )
        organism_box.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=2)
        organism_box.bind("<<ComboboxSelected>>", self._organism_changed)

        fields = [
            ("duration_h", "Duration (h)"),
            ("output_points", "Output time points"),
            ("cells", "Axial cells"),
            ("length_m", "Length (m)"),
            ("cross_section_m2", "Cross-section (m²)"),
            ("flow_m3_s", "Flow (m³/s)"),
            ("dispersion_m2_s", "Axial dispersion (m²/s)"),
            ("incident_par", "Incident PAR (µmol/m²/s)"),
            ("optical_path_m", "Optical path (m)"),
            ("kLa_o2_s", "O₂ kLa (1/s)"),
            ("biomass", "Initial biomass (g/L)"),
            ("dic", "Initial DIC (mmol/L)"),
            ("oxygen", "Initial O₂ (mmol/L)"),
            ("nitrogen", "Initial nitrogen (mmol/L)"),
            ("phosphorus", "Initial phosphorus (mmol/L)"),
            ("temperature_k", "Initial temperature (K)"),
        ]
        for row, (key, label) in enumerate(fields):
            ttk.Label(controls, text=label).grid(row=row + 1, column=0, sticky="w", pady=2)
            ttk.Entry(controls, textvariable=self.vars[key], width=15).grid(
                row=row + 1, column=1, sticky="ew", padx=(8, 0), pady=2
            )
        controls.columnconfigure(1, weight=1)
        self.run_button = ttk.Button(controls, text="Run simulation", command=self.run)
        self.run_button.grid(row=len(fields) + 2, column=0, columnspan=2, sticky="ew", pady=(12, 4))
        ttk.Button(controls, text="Open results folder", command=self.open_results).grid(
            row=len(fields) + 1, column=0, columnspan=2, sticky="ew"
        )

        self.figure = Figure(figsize=(8.5, 6.4), dpi=90)
        self.axes = self.figure.subplots(2, 3)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self._draw_empty()

        footer = ttk.Frame(outer)
        footer.pack(fill="x", pady=(8, 0))
        self.status = ttk.Label(footer, text="", wraplength=1050)
        self.status.pack(anchor="w")

    def _organism_changed(self, _event=None):
        profile = get_organism(self.organism_var.get())
        if profile.executable:
            self._set_status("Generic reduced-model demonstration selected. Outputs are illustrative, not species-specific.")
        else:
            self._set_status(f"{profile.display_name}: evidence profile only; executable species kinetics are not yet available.")

    def _draw_empty(self):
        for ax in self.axes.flat:
            ax.clear()
            ax.text(0.5, 0.5, "Run a simulation to view results",
                    ha="center", va="center", transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def _set_status(self, message):
        self.status.configure(text=message)

    def _number(self, key):
        try:
            value = float(self.vars[key].get())
        except ValueError as exc:
            raise ValueError(f"{key} must be numeric") from exc
        return value

    def run(self):
        self.run_button.configure(state="disabled")
        self.root.update_idletasks()
        try:
            organism = require_executable_organism(self.organism_var.get())
            duration_s = self._number("duration_h") * 3600
            output_points = int(self._number("output_points"))
            config = SpatialReactorConfig(
                cells=int(self._number("cells")),
                length_m=self._number("length_m"),
                cross_section_m2=self._number("cross_section_m2"),
                flow_m3_s=self._number("flow_m3_s"),
                axial_dispersion_m2_s=self._number("dispersion_m2_s"),
                incident_par_umol_m2_s=self._number("incident_par"),
                optical_path_m=self._number("optical_path_m"),
                kLa_o2_s=self._number("kLa_o2_s"),
            )
            initial = SpatialInitialState(
                biomass_g_l=self._number("biomass"),
                dic_mmol_l=self._number("dic"),
                oxygen_mmol_l=self._number("oxygen"),
                nitrogen_mmol_l=self._number("nitrogen"),
                phosphorus_mmol_l=self._number("phosphorus"),
                temperature_k=self._number("temperature_k"),
            )
            config.validate()
            initial.validate()
            result = simulate_spatial_reactor(
                duration_s, output_points, config=config, initial=initial
            )
            if not result.success:
                raise RuntimeError(result.solver_message)
            run_id = datetime.now(timezone.utc).strftime("desktop-%Y%m%dT%H%M%SZ")
            output = Path("results") / run_id
            manifest = {
                "schema_version": "1.0.0",
                "run_id": run_id,
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "model": {
                    "id": "PBR-SPATIAL-1D-001", "version": "0.1.0",
                    "fidelity_tier": 2, "validation_status": "UNVALIDATED",
                    "organism_profile": organism.organism_id,
                    "organism_model_status": organism.model_status,
                },
                "geometry": {"source": "desktop-user-input", "units": "m"},
                "inputs": {
                    "config": vars(config), "initial": vars(initial),
                    "parameters": vars(ModelParameters()),
                },
                "numerics": {
                    "method": "SciPy solve_ivp BDF / method-of-lines",
                    "mesh_cells": config.cells,
                    "output_points": output_points,
                    "converged": bool(result.success),
                },
                "provenance": {
                    "parameter_register_revision": "demo-defaults",
                    "datasets": [],
                    "operator_notes": "User inputs and illustrative defaults; not calibrated.",
                    "organism_limitations": list(organism.limitations),
                },
            }
            write_spatial_result(result, output, manifest)
            self._plot(result)
            final = {
                "biomass_g_l": float(result.biomass_g_l[-1].mean()),
                "dic_mmol_l": float(result.dic_mmol_l[-1].mean()),
                "oxygen_mmol_l": float(result.oxygen_mmol_l[-1].mean()),
                "temperature_k": float(result.temperature_k[-1].mean()),
            }
            self._set_status(
                f"Run complete: {output} | Tier 2 | UNVALIDATED | {organism.display_name} | "
                f"Final spatial means: {json.dumps(final)}"
            )
        except Exception as exc:
            messagebox.showerror("Simulation failed", str(exc))
            self._set_status(f"Run failed: {exc}")
        finally:
            self.run_button.configure(state="normal")

    def _plot(self, result):
        items = [
            ("biomass_g_l", "Biomass", "gDW/L"),
            ("dic_mmol_l", "Dissolved inorganic carbon", "mmol/L"),
            ("oxygen_mmol_l", "Dissolved oxygen", "mmol/L"),
            ("nitrogen_mmol_l", "Nitrogen", "mmol/L"),
            ("phosphorus_mmol_l", "Phosphorus", "mmol/L"),
            ("temperature_k", "Temperature", "K"),
        ]
        for ax, (key, label, unit) in zip(self.axes.flat, items):
            ax.clear()
            field = getattr(result, key)
            ax.plot(result.x_m, field[0], "--", label="Initial")
            ax.plot(result.x_m, field[-1], label="Final")
            ax.set_title(label)
            ax.set_xlabel("Axial position (m)")
            ax.set_ylabel(unit)
            ax.grid(True, alpha=0.25)
            ax.legend(fontsize=8)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def open_results(self):
        import os
        import subprocess
        import sys
        path = Path("results").resolve()
        path.mkdir(exist_ok=True)
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])


def main():
    root = tk.Tk()
    SimulatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

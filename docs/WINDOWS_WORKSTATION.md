# Windows workstation simulator

## Requirements

- Windows 10/11 x64
- Python 3.10–3.12 (Python 3.12 recommended)
- Git
- 4 GB RAM minimum for small reduced-order runs; 8 GB or more recommended
- No GPU, WSL, Docker or CFD installation is required for the Python simulator

## One-time setup

From Command Prompt in the repository root:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Launch the desktop simulator

Double-click `start_simulator.bat`, or run:

```bat
.venv\\Scripts\\python.exe -m pbrbiosphere.desktop_app
```

The desktop interface lets you change reactor length, cross-section, axial cell count, flow, dispersion, incident PAR, optical path, oxygen kLa, initial biomass, DIC, oxygen, nitrogen, phosphorus and temperature. It displays initial/final axial profiles and writes a timestamped run archive plus manifest under `results/`. The interface is a front end to the same Tier-2 numerical model; it does not add CFD or experimental validation.

## Run the complete local workflow

Double-click `run_windows_demo.bat`, or run it from Command Prompt:

```bat
run_windows_demo.bat
```

The script runs the test suite, executes a 24-hour illustrative Tier-2 spatial reactor case, checks run-file integrity and numerical structure, then writes profile and space-time plots.

Outputs:

- `results/windows-demo/fields.npz`: numerical space-time arrays
- `results/windows-demo/run-manifest.json`: input and provenance manifest plus SHA-256
- `results/windows-demo/validation-report.json`: integrity and structural diagnostics
- `results/windows-demo/spatial_profiles.png`: initial/final axial profiles
- `results/windows-demo/space_time_heatmaps.png`: space-time field plots

## Custom runs

Copy `examples/configs/flat_panel_demo.json`, edit the geometry, operating conditions and model parameters, then run:

```bat
python -m pbrbiosphere.cli --config examples/configs/flat_panel_demo.json --duration-s 86400 --output-points 49 --output results/my-run
python scripts/validate_spatial_run.py results/my-run
python scripts/plot_spatial_run.py results/my-run
```

To compare a coarse run with a finer spatial grid, create two config files with identical physical inputs and output times, changing only `config.cells`. Run both and compare:

```bat
python scripts/validate_spatial_run.py results/coarse --compare results/fine
```

The comparison linearly maps the coarse-grid fields onto the finer grid and reports relative L2 differences. This is a grid-sensitivity diagnostic, not a formal Grid Convergence Index (GCI) and not proof of physical accuracy.

## Opening the project in VS Code

VS Code is useful but not required. It is the development environment for editing the Python source, inspecting the project, running tests and debugging; the desktop simulator itself can run without VS Code. From the repository root:

```bat
code .
```

If the `code` command is not on PATH, open VS Code, choose **File → Open Folder**, and select the `PBR-Digital-Biosphere-Windows` directory. Select the interpreter at `.venv\Scripts\python.exe` using **Ctrl+Shift+P → Python: Select Interpreter**. Use the integrated terminal to run the same commands above. The repository also includes VS Code tasks: open **Terminal → Run Task** and choose **PBR: Launch desktop simulator**, **PBR: Run tests**, or **PBR: Full Windows demo**.

## Fidelity and limits

The current spatial solver is a one-dimensional finite-volume method-of-lines model (Tier 2). It includes axial advection/dispersion, reduced biological source terms, biomass-dependent Beer-Lambert attenuation, optional lumped oxygen transfer and lumped wall heat exchange. It is not 3-D CFD. The example parameter values are illustrative and must not be interpreted as a calibrated strain-specific operating point.

Integrity and structural checks verify that output files match their manifest, arrays are finite and correctly shaped, coordinates are ordered, and concentrations are non-negative. They do not test every elemental conservation balance, validate the biological kinetics, or establish predictive accuracy.

The optional Gmsh/OpenFOAM pipeline is separate and requires an actual CAD-exported fluid volume plus a compatible OpenFOAM runtime. The existing CAD mesher has not yet been validated against a real ToubkalCAD export. Do not describe the current simulator as an experimentally validated digital twin.

This is research software only. It must not be used to design, operate or certify human life-support systems, breathable atmospheres, underwater habitats or pressure vessels.

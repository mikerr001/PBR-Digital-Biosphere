# PBR Digital Biosphere — PBR-08 engineering workbench

PBR Digital Biosphere is a research simulator for photobioreactor and
regenerative-biosphere engineering. PBR-08 adds a spatial 1-D reactor model,
reproducible run artifacts, a command-line interface, an OpenFOAM starter
benchmark, and a reduced plant-level Modelica model.

## Current runnable software slice

Install from the repository root:

```bash
python -m pip install -e ".[dev]"
pytest -q
```

Run a small default spatial simulation:

```bash
pbr-run-spatial --duration-s 3600 --output-points 25 --output results/demo
```

Optional JSON input:

```json
{
  "config": {
    "length_m": 1.0,
    "cross_section_m2": 0.01,
    "cells": 20,
    "flow_m3_s": 0.00001,
    "axial_dispersion_m2_s": 0.00001,
    "incident_par_umol_m2_s": 150.0
  },
  "initial": {
    "biomass_g_l": 0.1,
    "dic_mmol_l": 2.0,
    "oxygen_mmol_l": 0.2,
    "nitrogen_mmol_l": 1.0,
    "phosphorus_mmol_l": 0.1
  }
}
```

The CLI writes `fields.npz` and `run-manifest.json`. The manifest records
model fidelity, numerical method, run inputs, solver status and a SHA-256
hash of the field archive.

## Engineering modules

- `src/pbrbiosphere/spatial_reactor.py`: Tier-2 1-D finite-volume
  method-of-lines model with advection, dispersion, biological source terms,
  Beer-Lambert attenuation, optional oxygen transfer and thermal exchange.
- `src/pbrbiosphere/run_artifacts.py`: reproducible field and manifest output.
- `src/pbrbiosphere/cli.py`: runnable command-line entry point.
- `openfoam/rectangular-reactor`: 3-D single-phase flow starter case for
  OpenFOAM Foundation v10.
- `openfoam/channel-laminar`: planar channel solver smoke-test case.
- `modelica/PBRPlant.mo`: reduced pump/pipe/tank and thermal inventory models.
- `docs/MULTIPHYSICS_ROADMAP.md`: architecture, fidelity tiers and validation
  gates.
- `docs/SIMULATION_RUN_MANIFEST.schema.json`: machine-readable run schema.

## Optional CAD-to-CFD mesh hand-off

Install the optional meshing dependency:

```bash
python -m pip install -e ".[cfd]"
```

Export a single watertight fluid-domain STEP from ToubkalCAD, then create a
boundary manifest based on the actual CAD dimensions and face locations:

```bash
python scripts/generate_cad_mesh.py --step fluid-domain.step --manifest examples/cad/pbr-boundaries.example.json --output fluid.msh --mesh-size-m 0.01
gmshToFoam fluid.msh
checkMesh -allTopology -allGeometry
```

The example manifest is only a template. Replace its plane coordinates and
boundary groups; curved or ambiguous faces require explicit CAD face labels.
The script rejects overlapping or unassigned surfaces. A generated mesh is
not automatically a validated mesh.

The local source-term contract is available through
`pbrbiosphere.cfd_coupling.pbr02_cell_sources`. It emits SI volumetric source
densities and `integrate_source` checks volume-weighted totals. This is an
interface foundation, not a live OpenFOAM field exchange or coupled solver.

See `docs/CAD_TO_CFD_PIPELINE.md`, `docs/CFD_CASE_EXECUTION.md` and
`docs/CFD_BIOLOGY_COUPLING.md` before attempting a CFD run.

## Fidelity and limitations

The Python distributed reactor is Tier 2 (one-dimensional), UNVALIDATED.
The OpenFOAM directories are solver input cases, not executed CFD results.
The Modelica coefficients are illustrative. The software does not yet provide
CAD-to-mesh automation, fully coupled 3-D CFD/biology, bubble-resolved
multiphase flow, spectral radiative transfer, validated carbonate chemistry,
or experimentally calibrated system dynamics.

This repository is research software, not certified life-support,
pressure-vessel, medical or habitat engineering software. No simulation
result should be used as an operational safety limit.

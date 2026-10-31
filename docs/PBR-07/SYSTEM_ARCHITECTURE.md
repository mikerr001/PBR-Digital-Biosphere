# PBR-07 — Physics-Based Digital Twin: System Architecture
**Status:** Design baseline v0.1  
**Date:** 2026-10-31  
**Primary UI:** 3D engineering environment  
**Default configuration:** Hybrid underwater-inspired regenerative biosphere  
**Implementation status:** Not yet implemented

## 1. Purpose

PBR-07 turns the existing PBR-Digital-Biosphere biological models into a spatially explicit engineering digital-twin environment. The user constructs and edits a 3D habitat/reactor assembly, defines materials and operating conditions, runs numerical models, and inspects computed fields in the 3D scene.

The 3D engineering workspace is the primary application. A scientific control room is secondary and may be opened as a docked panel or separate route.

This is a research simulator. It is not a certified pressure-vessel design tool, a validated life-support system, or evidence that a habitat can safely support people.

## 2. Adopt-and-adapt strategy

Do not write a CAD editor from scratch. The preferred starting point is a fork of **ToubkalCAD** (MIT; https://github.com/ToubkalCAD/ToubkalCAD), subject to a clean fork and build audit.

Why this base:
- Existing browser CAD application rather than a blank Three.js canvas.
- OpenCascade compiled to WebAssembly for boundary-representation solid modelling.
- Three.js viewport and geometry rendering.
- React UI, Zustand scene state, Dockview panels.
- Parametric feature history, recomputation, assemblies, measurements, STEP/IGES exchange.
- MIT license permits modification and redistribution subject to preserving notices.

Do not fork or vendor blindly. Preserve upstream history and notices, inspect dependency licenses, record the exact upstream commit, and isolate PBR-specific modules. The GitHub connector used for this design session does not expose a repository-fork action; no fork is claimed to have been created. The actual fork must be created in GitHub before code integration.

## 3. System context

```text
                 PBR-07 Engineering Workspace
        ┌──────────────────────────────────────────┐
        │ CAD viewport │ Model tree │ Properties   │
        │ Component library │ Solver controls      │
        └──────────────────────┬───────────────────┘
                               │
                     Canonical project document
                               │
                ┌──────────────┴──────────────┐
                │ Geometry + material model  │
                └──────────────┬──────────────┘
                               │
                     Simulation orchestrator
           ┌───────────┬───────┼────────┬──────────┐
           │           │       │        │          │
         Fluid       Thermal  Optical  Structural  Biology
         model       model    model    model       model
           └───────────┴───────┼────────┴──────────┘
                               │
                     Coupling / data exchange
                               │
                 Results fields + time histories
                               │
              3D overlays, plots, tables, reports
                               │
                  Calibration / validation store
```

## 4. Top-level subsystems

### 4.1 CAD and geometry
- Start from the upstream CAD application; retain its geometry kernel, viewport, selection, feature history, assembly tree, measurement and export workflows.
- Add a PBR component catalogue: transparent pressure shell, inner culture vessel, crop module, pipe, elbow, valve, pump, sparger, heat exchanger, lamp, sensor, support frame, anchor and cable.
- Each PBR component is a parametric feature with stable ID, dimensions, material, ports and metadata.
- Geometry is authoritative for shape and topology. Simulation meshes are derived artifacts and must never replace the editable CAD model.
- Units are SI internally. UI may display convenient units, but every value carries a unit and conversion.

### 4.2 Project document
The project document is the canonical, versioned source of truth:
- project metadata and schema version;
- CAD feature graph and component instances;
- component properties and materials;
- ports and connection graph;
- environmental boundary conditions;
- biological model selection and parameter provenance;
- solver configuration and run metadata;
- results references, validation datasets and uncertainty notes.

Use JSON for the portable project manifest. Large meshes and field arrays are separate files referenced by content hash. Never serialize WASM kernel objects.

### 4.3 Physical environment
Default scenario is a submerged external environment around a hybrid habitat. It is a selectable scenario, not a fixed assumption:
- water depth and hydrostatic pressure;
- external water temperature and salinity;
- current velocity and direction;
- ambient pressure and water density;
- incident solar spectrum/irradiance and orientation;
- wave loading as a later optional boundary condition.

The internal habitat is partitioned into fluid domains: external water, internal liquid culture, gas headspace, and crop/habitat air volumes. Do not treat these phases as one homogeneous fluid.

### 4.4 Solver services
Solvers are separate, replaceable backends. The orchestrator owns run configuration, dependency ordering, cancellation, status, logs, output validation and provenance.

A solver must declare:
- supported physics and dimensionality;
- inputs and outputs with units;
- assumptions and validity range;
- numerical method and version;
- mesh/time-step requirements;
- convergence and failure criteria;
- fidelity classification.

### 4.5 Existing biological package
Keep PBR-02, PBR-03, PBR-04, PBR-04A, PBR-05 and PBR-06 as separately testable Python modules. Expose stable adapters rather than porting their equations into TypeScript.

- PBR-02: reduced algal state dynamics.
- PBR-03: phase/acclimation analysis; do not imply molecular KaiABC kinetics.
- PBR-04: reduced optics, gas transfer and thermal model; current limitations remain explicit.
- PBR-04A: provenance, calibration and independent-dataset comparison.
- PBR-05: advisory supervisor only; automatic actuation remains disabled.
- PBR-06: explicit inventory/flux bookkeeping; no default human metabolic inputs.

The browser sends a versioned simulation request to a Python service or local Python runtime. The adapter validates the request, executes the selected model, and returns typed results. A lightweight browser-only preview may be offered, but it must not silently substitute for the authoritative Python model.

## 5. Data and interface contracts

### 5.1 Component contract
Every component instance has:
- `id`: stable UUID;
- `type`: registered component type;
- `name`;
- `transform`: position, orientation and scale in SI;
- `geometry_parameters`: typed, bounded values;
- `material_id`;
- `ports[]`: port IDs, domain type, position, direction and nominal diameter;
- `simulation_roles[]`: e.g. fluid_boundary, heat_transfer_surface, light_source;
- `provenance`: source/version of component definition.

### 5.2 Port and network contract
Connections are explicit graph edges. A connection must match domain type and compatible port dimensions. Fluid networks cannot be inferred solely from visual proximity. Every pipe network must be topologically connected or report disconnected components.

### 5.3 Field contract
A field result contains:
- field ID and name;
- physical quantity and SI unit;
- domain and mesh ID;
- time coordinate;
- values and association (cell, point, face or region);
- min/max and validity mask;
- solver and model version;
- run ID and fidelity label.

### 5.4 Simulation run contract
A run records immutable input snapshot, geometry hash, mesh hash, solver version, numerical settings, parameter provenance, start/end time, status, warnings, convergence data and output hashes. Re-running a changed project creates a new run; it never mutates historical results.

## 6. Numerical architecture and coupling order

Initial coupled solve is sequential with conservative data exchange; fully coupled monolithic solving is not a first milestone.

1. Validate project, geometry, units, ports and parameter provenance.
2. Generate or load computational meshes for relevant domains.
3. Solve external environment and internal fluid fields at selected fidelity.
4. Solve thermal transport using fluid fields and heat-transfer boundaries.
5. Solve optical transport from source spectrum, geometry, absorption and scattering assumptions.
6. Derive volume-averaged or spatially resolved biological inputs (PAR, temperature, mixing/mass transfer).
7. Integrate PBR biological ODEs over time.
8. Exchange biological heat/gas/nutrient source terms back to physics models where supported.
9. Iterate outer coupling until declared residual criteria are met, or stop and report non-convergence.
10. Store results and render fields.

A one-way coupling run is labelled one-way. It must not be described as fully coupled.

## 7. Fidelity tiers

| Tier | Description | Permitted label |
|---|---|---|
| 0 | Geometry-only, no numerical field solution | CAD / visualization |
| 1 | Analytical or lumped balances and reduced ODEs | Reduced-order simulation |
| 2 | Spatial discretization on a simplified domain | Reduced spatial numerical model |
| 3 | Verified external solver (e.g. OpenFOAM/FEniCSx) with mesh and convergence studies | CFD / FEA only for the physics actually solved |
| 4 | Independently benchmarked and experimentally validated model over stated operating range | Validated model within stated range |

The UI must display the tier, assumptions, model status and validation state beside every result. No decorative heatmap may be presented as a solved field.

## 8. Runtime and deployment
- 3D CAD client: browser-based React/TypeScript.
- Numerical API: Python package and a small API service; keep existing PBR package importable and independently testable.
- Solver workers: separate processes/containers for long-running jobs; do not run expensive solvers on the browser main thread.
- Local development: Node.js for the CAD client; Python 3.10–3.12 for the existing scientific package.
- Colab: useful for model experiments and small reduced-order runs, not the production solver host.
- Static frontend hosting: requires cross-origin isolation headers if the selected CAD kernel uses SharedArrayBuffer.
- Heavy CFD/FEA: optional remote or workstation backend; phone browser is a viewer/editor, not the target compute engine.

## 9. Safety and scientific integrity
- No human occupancy, breathable-air, pressure-vessel safety or life-support claims from this simulator.
- Pressure-shell results require material properties, boundary conditions, mesh convergence and independent validation before engineering interpretation.
- Missing, stale or invalid input produces a visible unavailable/degraded state, never invented results.
- Default parameters are labelled illustrative or estimated unless sourced.
- Preserve unit checks, conservation checks, uncertainty and residual reporting.
- Biological model limitations remain visible; circadian phase is not proof of increased productivity.

## 10. Design acceptance criteria
The design is ready for implementation when:
- canonical project schema is versioned;
- component/port/domain ontology is defined;
- coordinate and unit conventions are fixed;
- solver contracts and fidelity labels are fixed;
- coupling graph and exchange quantities are explicit;
- upstream CAD fork and license audit are recorded;
- verification/validation plan exists;
- first vertical slice is scoped without pretending to deliver full CFD/FEA.

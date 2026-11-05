# Multiphysics engineering roadmap

## Fidelity contract
Tier 0: bookkeeping/static geometry. Tier 1: lumped and network models.
Tier 2: spatially distributed reduced-order models. Tier 3: resolved 2-D/3-D
numerical physics. Tier 4: experimentally calibrated and independently
validated integrated digital twin.

The current spatial reactor is Tier 2, one-dimensional method-of-lines.
It is not CFD. The platform is research software, not certified life-support,
pressure-vessel, medical or habitat engineering software.

## Target architecture
1. ToubkalCAD/OpenCascade remains parametric geometry authority.
2. Export STEP plus stable component/port manifest; OpenUSD may serve as
   downstream scene exchange, not parametric CAD source.
3. Generate a separately validated mesh with named boundary patches.
4. Use OpenFOAM for 3-D single-phase flow first, then thermal/species transport.
5. Use OpenModelica for plant-scale pumps, valves and control loops, exchanging
   explicit boundary conditions with CFD.
6. Use Python/SciPy for biological source terms and reduced-order models.
7. Orchestrate versioned runs with geometry hash, mesh, solver version,
   parameters, conditions, residuals and conservation errors.
8. Render solver outputs in Three.js; visualisation must not invent physics.

## Implemented spatial model
The new spatial model resolves axial advection and dispersion; local biomass,
DIC, dissolved oxygen, N, P and temperature; biomass-dependent Beer-Lambert
attenuation; PBR-02 growth kinetics and fixed quotas; optional lumped oxygen
kLa; thermal transport and wall exchange. It uses SciPy BDF.

Limitations: no radial flow, turbulence, recirculation, free surface, spectral
optics, photoinhibition, bubble population balance, gas holdup, carbonate
chemistry, CO2 transfer, reaction heat or structural mechanics. PAR-to-growth
mapping remains provisional. Defaults are illustrative.

## Validation gates
- Mesh/time refinement, tolerance sensitivity, positivity and conservation.
- Laminar pipe pressure drop against Hagen-Poiseuille; turbulent friction
  against independent Moody/Colebrook calculations.
- Advection-dispersion against analytical solutions.
- Heat transfer against transient conduction benchmarks.
- Optical transmission against measured attenuation.
- kLa against controlled reoxygenation experiments.
- Strain/medium-specific biological calibration with independent holdout runs.
- Report bias, MAE, RMSE, uncertainty and model discrepancy.

## Roadmap
1. Build an OpenFOAM 3-D single-phase flow benchmark and CAD-to-mesh transfer.
2. Add conjugate heat transfer and passive scalar transport.
3. Add oxygen/carbon species transport with measured transfer coefficients.
4. Couple biological kinetics using conservative source terms.
5. Add Eulerian gas-liquid modelling only after bubble-size and gas-holdup
   data are available.
6. Integrate plant-level equipment/control models and experimental time series.
7. Promote fidelity only after each validation gate passes.

A Tier-4 integrated twin cannot be completed in software alone: it requires
physical measurements and independent experiments.

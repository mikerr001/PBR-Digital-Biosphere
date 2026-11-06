# PBR Digital Biosphere — engineering release status

**Release designation:** research software prototype / not experimentally validated.

## Implemented in the current engineering branch

- PBR-02 reduced algal physiology and lumped C/O2/N/P state model.
- PBR-03 circadian scaffold and supporting experiment/schedule utilities.
- PBR-04 flat-panel geometry, light attenuation, gas-transfer and thermal helper models.
- PBR-02/PBR-04 reduced-order dynamic coupling for biomass, dissolved/headspace O2 and temperature.
- PBR-04A carbonate-equilibrium prototype and CO2 transfer helper, with explicit freshwater/carbonate-only assumptions.
- PBR-05 supervisory recommendations with conservative fail-closed behaviour and operator confirmation.
- PBR-06 habitat inventory ledger with explicit user-supplied fluxes.
- Tier-2 one-dimensional axial spatial reactor solver.
- Windows Tkinter desktop interface, run archives, SHA-256 integrity checks, spatial-grid sensitivity diagnostics and Windows CI workflow.
- Multi-organism evidence catalogue with explicit readiness gates for *Synechococcus elongatus* PCC 7942 and *Phaeodactylum tricornutum*.

## Computationally tested

The automated test suite exercises individual modules, data contracts, integration paths, validation utilities and run-artifact integrity. The Windows CI workflow is configured to install the package, compile/import the desktop application, execute tests, run the 1-D flat-panel example, validate the run archive and generate plots.

A passing CI run establishes software execution under that CI environment only. It does not establish physical correctness, parameter identifiability or biological validity. The current branch's latest CI result must be checked on GitHub before release tagging.

## Not yet implemented as a validated end-to-end capability

- 3-D multiphase CFD coupled to species-resolved reaction source terms.
- Verified CAD-to-mesh-to-CFD workflow for a production flat-panel geometry.
- Coupled DIC/alkalinity/pH/carbonate chemistry and CO2 transfer in the spatial reactor.
- Species-specific executable kinetics for the two named organisms.
- Full crop, waste, water recovery and atmosphere chemistry models for an integrated regenerative biosphere.
- Automatic controller actuation or process-safety interlocks.
- Formal mesh/time-step uncertainty quantification and model-discrepancy analysis.
- Empirical calibration and independent experimental validation.

## Research validation evidence required

At minimum, obtain condition-matched time-series measurements of biomass, dissolved inorganic carbon, pH/alkalinity, dissolved oxygen, gas-phase CO2/O2, temperature, irradiance/transmittance, nutrient concentrations and gas/liquid flow. Record the exact strain, medium recipe, salinity, inoculum, acclimation, geometry, sensor calibration and measurement uncertainty.

Split experiments into calibration and independent holdout sets before fitting. Freeze the model and acceptance criteria before the holdout comparison. Report bias, MAE, RMSE, uncertainty coverage, conservation residuals, sensitivity/identifiability and validity-domain limits.

## Safety boundary

This software is not certified life-support software. It must not be used to design, operate or certify occupied underwater habitats, spacecraft atmospheres, oxygen supply, pressure vessels or human-occupancy limits.

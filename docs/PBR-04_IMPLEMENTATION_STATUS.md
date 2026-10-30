# PBR-04 Implementation Status
## Implemented
- Flat-panel dimensions, illuminated area and geometric liquid-volume closure diagnostic.
- One-dimensional Beer–Lambert irradiance profile, path-average and transmitted fraction.
- Separate dissolved/headspace O₂ and molecular CO₂ equilibrium/transfer rates.
- Ideal-gas headspace partial pressures.
- Lumped liquid thermal rate with explicit unit conversion.
- Instantaneous physical-rate assembly API.
- Two-compartment signed exchange helper parameterised by measured mixing time.
- Automated tests for geometry, optical attenuation, transfer direction/equilibrium, heat direction/scaling and validation.

## Not implemented
- CFD, bubble hydrodynamics, circulation or integrated time-dependent compartment mixing.
- Spectral radiative transfer, scattering or photoinhibition.
- Carbonate chemistry, total DIC speciation, pH or alkalinity.
- Gas venting, leakage, pressure regulation or compressor dynamics.
- Spatial photosynthesis, biomass distribution or biological O₂/CO₂ source terms.
- Dynamic coupling to PBR-02 and experimental calibration.

## Interpretation
PBR-04 is an executable physical-submodel foundation. CI verifies software behaviour only; this is not an experimentally validated photobioreactor digital twin.

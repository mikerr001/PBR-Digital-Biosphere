# PBR-02 Data Dictionary v0.1

## State variables
| Symbol | Code name | Unit | Meaning |
|---|---|---|---|
| X | biomass_gDW_L | g dry biomass L-1 | Biomass concentration |
| C | dic_mmolC_L | mmol C L-1 | Lumped dissolved inorganic carbon; not yet carbonate speciation |
| O | oxygen_mmol_L | mmol O2 L-1 | Dissolved oxygen concentration |
| N | nitrogen_mmol_L | mmol N L-1 | Modelled available nitrogen pool |
| P | phosphorus_mmol_L | mmol P L-1 | Modelled available phosphorus pool |

## Time and forcing
- Solver time: days in the current scaffold.
- Irradiance: µmol photons m-2 s-1; spectral distribution not yet represented.
- Temperature: °C.
- Photoperiod: hours per model day.

## Rate conventions
- Specific growth rate: day-1 internally; source values may be h-1 and must be converted explicitly by multiplying by 24 only when converting rate units (not when changing reported experiment duration).
- Biomass-specific oxygen rates: mmol O2 gDW-1 h-1 or day-1. Never mix without explicit conversion.
- Chlorophyll-normalised oxygen rates: e.g. µmol O2 mg Chl a-1 h-1. Do not compare directly to dry-weight-normalised rates.
- Cell-specific rates: preserve per-cell basis unless measured cell dry mass is available for conversion.

## Evidence metadata required for every parameter
Organism, strain, parameter name, value, unit, uncertainty, temperature, irradiance and spectrum, medium, pH where reported, acclimation history, assay method, source DOI, evidence class and notes.

## Important distinction
A literature value is not a universal species constant. It is a measurement under specified conditions. The model parameter key should include condition/acclimation metadata whenever the experiment shows condition dependence.

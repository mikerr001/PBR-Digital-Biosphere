# CFD ↔ biology source-term contract

The current 1-D biology model is not yet spatially coupled to a 3-D OpenFOAM
solution. `pbrbiosphere.cfd_coupling` defines the unit-safe local reaction
source interface that such a coupling can consume.

## Units

- Liquid concentrations in the biology model: mmol/L.
- OpenFOAM SI concentration basis: mol/m³. These concentration units are
  numerically equal: 1 mmol/L = 1 mol/m³.
- Rates per day are divided by 86,400 to obtain per-second source densities.
- Biomass: 1 g/L = 1 kg/m³; the same per-day to per-second conversion applies.

## Implemented interface

`pbr02_cell_sources(biomass_g_l, mu_per_day, parameters)` returns local
volumetric source densities for biomass, DIC, dissolved O2, N and P. It applies
the existing fixed-quota PBR-02 bookkeeping. `integrate_source` performs
volume-weighted cell integration so global source/sink totals can be checked.

## What this does not do

It does not interpolate between meshes, read OpenFOAM fields, solve pH,
calculate CO2 gas transfer, model bubble populations, or advance a coupled
CFD/biology time step. It does not supply a validated local light field:
PAR mapping and biological kinetics remain uncalibrated. A production coupling
must use actual CFD cell volumes, enforce positivity, exchange fields at a
documented coupling interval, and compare integrated source terms with the
change in liquid and biomass inventories at every exchange.

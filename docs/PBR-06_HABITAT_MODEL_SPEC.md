# PBR-06 — Regenerative Habitat Inventory Model

## Purpose and boundary
PBR-06 introduces a transparent, lumped inventory ledger for a hypothetical habitat. It connects human, microbial, crop and algal gas fluxes with water and nutrient inventories. It is not a closed-loop ecosystem model, a human life-support design, or evidence that any population can be sustained.

## Implemented state
- Total habitat oxygen inventory (mmol)
- Total habitat carbon-dioxide inventory (mmol)
- Recoverable water inventory (L)
- Nitrogen inventory (mmol element)
- Phosphorus inventory (mmol element)

The current implementation treats each inventory as a well-mixed scalar. It does not calculate partial pressure, gas composition, ventilation, humidity, temperature, local gradients, dissolved/gas partitioning, crop water transpiration, or nutrient chemical speciation.

## Flux contract
All rates are whole-habitat rates. Human and microbial oxygen consumption and CO2 generation are positive magnitudes. Crop/algal O2 and CO2 terms are signed net transfers to the habitat atmosphere: positive adds to the atmosphere, negative removes from it. Leakage terms are positive losses. Water and nutrient terms are signed net inventory rates.

The API deliberately has no embedded human metabolic defaults. Any occupancy scenario must state its population, activity, body-mass/physiology basis, duration, uncertainty and source. A nominal 15-person scenario is a scaling exercise only; no capacity or safety conclusion can be drawn from this model.

## Governing balances
dM_O2/dt = F_O2,crop + F_O2,algae - R_O2,human - R_O2,microbe - L_O2

dM_CO2/dt = G_CO2,human + G_CO2,microbe + F_CO2,crop + F_CO2,algae - L_CO2

dV_water/dt = F_water,net

dN_inventory/dt = F_N,net

dP_inventory/dt = F_P,net

These equations conserve the chosen lumped inventories for the supplied fluxes; they do not model the underlying biological conversion pathways. No water or nutrient recovery efficiency is assumed.

## Integration and limits
The current version integrates constant fluxes over a finite interval and rejects a run when an inventory becomes materially negative. It does not automatically close crop/algae/human nutrient loops or derive gas fluxes from biomass production. Fluxes are external inputs until coupled to separately validated component models.

## Required next work
1. Add atmosphere volume, temperature, humidity and pressure to derive partial pressures and gas concentrations.
2. Add spatial mixing/ventilation and leakage models.
3. Add crop growth, harvest, edible fraction, water demand and transpiration with source-derived parameters.
4. Add human metabolic demand as activity-dependent distributions, not one universal per-person constant.
5. Add microbial decomposition, waste streams, nutrient mineralisation and recovery efficiencies.
6. Add water purification, storage, losses and quality states.
7. Couple algal and crop gas exchange through validated carbon/oxygen stoichiometry and measured transfer rates.
8. Run uncertainty propagation and fault scenarios; validate each component independently before whole-system integration.

## Validation and safety gates
No independent habitat dataset has been used. PBR-06 is currently a software scaffold for mass-balance accounting only. It must not be used to claim oxygen sufficiency, breathable atmosphere, safe human occupancy, underwater endurance, or life-support reliability. Such claims require validated physiological requirements, gas composition/pressure controls, redundancy, monitoring, independent safety engineering and physical testing by qualified teams.

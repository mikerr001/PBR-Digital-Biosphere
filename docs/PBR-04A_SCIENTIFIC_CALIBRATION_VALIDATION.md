# PBR-04A — Scientific Calibration and Validation Framework

## Purpose
Strengthen PBR-02 through PBR-05 before habitat-scale expansion. This milestone adds parameter provenance checks, a bounded carbonate-equilibrium calculation, experimental-data conventions and independent holdout metrics. It does not claim biological or physical validation.

## Parameter identification
Each parameter record should preserve organism/strain, definition, value/unit, temperature, irradiance, medium, salinity where relevant, cultivation mode, measurement basis, uncertainty, source and extraction notes. Evidence classes are measured, literature_derived, fitted, estimated and unknown. Never pool Synechococcus elongatus PCC 7942 and Phaeodactylum tricornutum evidence or convert per-cell, chlorophyll, protein and dry-mass bases without a source-backed conversion. Preserve replicate count and uncertainty. The validator checks fields only; it does not verify sources or identifiability.

## Carbonate chemistry
PBR-02 stores total dissolved inorganic carbon; the former PBR-04 Henry-law calculation represents molecular dissolved CO2. They are not interchangeable. The new routine solves pH from DIC and total alkalinity using DIC=[CO2*]+[HCO3-]+[CO3--] and carbonate-only TA=[HCO3-]+2[CO3--]+[OH-]-[H+]. It returns molecular CO2 for Henry-law transfer. Constants must match temperature, ionic strength and salinity. This is a carbonate-only freshwater approximation: phosphate, silicate, borate, ammonia, organic alkalinity, activity corrections, ion pairing and kinetic hydration are omitted. These omissions may matter in BG-11 and marine media. Do not couple to the simulator until medium chemistry is characterised.

## Experimental data contract
Keep raw observations immutable and separate from model outputs. Record dataset ID, DOI/URL, source table/figure/supplement, extraction date, organism/strain, medium, temperature, salinity, pH, cultivation mode, light spectrum, photoperiod, incident and in-reactor PAR, reactor geometry, optical path, volume, mixing, gas composition/flow, time, variable, value/unit, normalisation basis, replicate count, uncertainty, method, detection limit, exclusions and transformation history. Missing metadata stays missing. Converted data must be separate, versioned derived datasets.

## Independent validation
Partition by experiment or publication, not random rows from one time series. Fit only on training data; freeze parameters and model version; evaluate against an independent experiment not used for fitting or model selection. The comparison utility requires exact time-grid matches and refuses implicit interpolation. Report bias, MAE, RMSE, maximum absolute error and, when uncertainty exists, normalised error and fraction within one standard uncertainty. Software tests are not experimental validation.

## Validation sequence
1. Audit every current parameter value, DOI, strain, units and conditions. Existing register entries remain provisional until checked.
2. Extract light-response and respiration observations with replicate uncertainty.
3. Characterise medium-specific carbonate constants and non-carbonate alkalinity; validate against independent DIC, TA and pH.
4. Identify O2/CO2 kLa from abiotic transfer experiments.
5. Validate growth and gross/net O2 against independent matched biological datasets.
6. Validate optics and thermal transients against physical measurements.
7. Publish uncertainty and model-discrepancy ranges before PBR-06.

Research simulator only; no result establishes safe oxygen delivery, underwater habitat performance or human occupancy suitability.

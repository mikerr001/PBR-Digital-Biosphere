# PBR-02 Validation Dataset Schema

A validation CSV must contain:
- `time_days`: elapsed time from a declared experiment origin.
- At least one observed variable, e.g. `biomass_gDW_L` or `oxygen_mmol_L`.
- Values must use the same normalisation basis and units as the corresponding model output.

A sidecar metadata record must declare:
- Organism and exact strain.
- Culture medium and nutrient recipe.
- Temperature, irradiance and spectral distribution.
- Photoperiod and acclimation history.
- pH, alkalinity and inorganic-carbon supply where reported.
- Sampling and assay methods.
- Source DOI and whether the data were used for calibration.

The comparison helper requires identical row counts and exact time-grid equality. It does not interpolate, convert units or infer missing data. Align and convert explicitly before comparison.

Report MAE and RMSE. R² is omitted when observations are constant. Never use calibration data as independent validation data.

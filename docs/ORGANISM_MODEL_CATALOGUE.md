# Organism model catalogue and readiness

## Purpose

The multi-organism architecture separates three things that must not be conflated:

1. **Organism identity** — taxon and strain.
2. **Evidence profile** — traceable observations, including the original measurement basis and experimental conditions.
3. **Executable kinetic model** — a complete, internally consistent parameterisation with a stated validity domain.

A literature observation does not by itself make a species model executable.

## Current catalogue

| Profile ID | Organism | Current status | Executable? |
|---|---|---|---|
| `synechococcus_elongatus_pcc7942` | *Synechococcus elongatus* PCC 7942 | Evidence profile only | No |
| `phaeodactylum_tricornutum` | *Phaeodactylum tricornutum* | Evidence profile only; strain-specific extraction open | No |
| `generic_reduced_demo` | Generic reduced-model demonstration | Illustrative, uncalibrated | Yes, for software demonstration only |

The source-observation records in `organisms/synechococcus_7942.py` preserve the reported light conditions, temperature, medium, acclimation and units. The Phaeodactylum module intentionally contains evidence metadata but no cross-strain numeric parameter defaults.

## Why the species profiles are not yet runnable

The current reduced PBR-02 model requires a compatible set of maximum growth rate, light response, nutrient half-saturation constants, carbon response, decay/respiration, photosynthetic and respiratory quotients, and C/N/P biomass quotas. Those values must be matched to the same strain, medium, temperature, illumination spectrum/intensity, acclimation and biomass basis. Combining unrelated literature maxima into one synthetic parameter set would create a plausible-looking but scientifically invalid organism model.

The registry therefore fails closed when either named species is selected as a simulation model. This is intentional. The generic demonstration model remains available for software and numerical development, but its output must not be described as a prediction for either organism.

## Acceptance gates for an executable organism model

- Strain and culture-medium identity fixed.
- Parameter register records source DOI, exact table/figure/page, assay method, conditions, units, uncertainty and biomass basis.
- No silent conversions between cell-, chlorophyll-, protein- and dry-weight-normalised rates.
- Identifiability analysis establishes which parameters the available experiments can estimate.
- Calibration data and independent holdout data are separated before fitting.
- Growth, gross/net O2, carbon uptake, respiration and elemental composition are reconciled with a documented stoichiometric convention.
- Model predictions pass predeclared error and uncertainty criteria on independent experiments.
- Validity domain and extrapolation warnings are emitted in every run manifest.

## Status vocabulary

- **Implemented:** code exists and is integrated.
- **Computationally tested:** automated software/numerical tests pass.
- **Calibrated:** parameters fitted against identified experimental data.
- **Experimentally validated:** independent measurements support predictions within predeclared uncertainty/error limits.

The first two statuses do not imply the last two.

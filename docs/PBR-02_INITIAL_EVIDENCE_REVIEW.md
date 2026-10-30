# Initial PBR-02 Evidence Extraction (v0.1)

## 1. *Synechococcus elongatus* PCC 7942

### Broddrick et al. (2019)
J.T. Broddrick et al., “Predicting the metabolic capabilities of Synechococcus elongatus PCC 7942 adapted to different light regimes,” Metabolic Engineering 52 (2019), 42–56. DOI: https://doi.org/10.1016/j.ymben.2018.11.001. Open full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6407710/

Conditions: wild-type PCC 7942, 30°C, BG-11 medium, cultures acclimated 72 h at 60 (low light) or 600 (high light) µmol photons m−2 s−1; continuous illumination during culture.

Directly reported growth rates:
- Low light: 0.047 ± 0.004 h−1.
- High light: 0.081 ± 0.015 h−1.

Directly reported dark respiration:
- Low-light-acclimated culture: 0.15 mmol O2 gDW−1 h−1.
- High-light-acclimated culture: 0.41 mmol O2 gDW−1 h−1.

Interpretation: acclimation history changes both growth and maintenance oxygen demand. A single universal respiration coefficient is not supported by these observations. These rates are measured under the study's assay conditions; do not extrapolate them uncritically to another temperature, medium, culture density or reactor.

The authors fit oxygen evolution against photon flux with a Platt photosynthesis-irradiance equation. Their table includes cell-specific photon flux and oxygen evolution rates. Keep those units intact; conversion to gDW-specific rates requires the paper's cell dry-weight measurements and careful unit conversion.

## 2. *Phaeodactylum tricornutum*

### Schellenberger Costa et al. (2013)
B. Schellenberger Costa et al., “Blue light is essential for high light acclimation and photoprotection in the diatom Phaeodactylum tricornutum,” Journal of Experimental Botany 64(2), 483–493. DOI: https://doi.org/10.1093/jxb/ers340. Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC3542041/

Finding: under the tested conditions, light quality influenced photoacclimation. Blue and white light supported stronger high-light acclimation/photoprotection than red light. This is a mechanistic warning against modelling marine diatom light response using irradiance magnitude alone when spectral composition changes. The paper's Pmax values are chlorophyll-normalised and must not be treated as dry-biomass-specific without conversion data.

### Heydarizadeh et al. (2019)
P. Heydarizadeh et al., “Carbon Orientation in the Diatom Phaeodactylum tricornutum: The Effects of Carbon Limitation and Photon Flux Density,” Frontiers in Plant Science 10:471. DOI: https://doi.org/10.3389/fpls.2019.00471. Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6477932/

Methods: oxygen evolution was measured at 21°C; dark respiration was measured after light oxygen evolution. Gross photosynthesis was calculated as net photosynthesis plus respiration, assuming dark respiration represented respiration during illumination. That is a stated methodological assumption, not a universal identity. The study also examines carbon limitation and photon flux density.

## 3. What is not yet extracted

- Full numeric Platt coefficients with exact unit conventions for both species.
- Species-specific oxygen evolution in a common biomass-normalised unit.
- Light respiration versus dark respiration.
- Photosynthetic and respiratory quotients under relevant culture conditions.
- Biomass C/N/P elemental quotas under matched conditions.
- Nutrient half-saturation constants for the exact strains and media.
- pH, alkalinity, DIC speciation and gas-transfer parameters.

## 4. Model implementation implications

1. Preserve source units and normalise only through explicit, reviewable conversions.
2. Store acclimation condition as part of the parameter key.
3. Do not use the 60/600 light acclimation growth rates as universal maximum growth rates.
4. Do not substitute chlorophyll-normalised rates for dry-weight-normalised rates.
5. Do not infer closed carbon/oxygen stoichiometry from gross oxygen evolution alone.
6. The first implementation should support separate light-acclimation parameter sets and mark unsupported inputs as unavailable.

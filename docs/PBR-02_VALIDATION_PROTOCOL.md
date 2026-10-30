# PBR-02 Verification and Validation Protocol v0.1

## Scope
This protocol separates software verification (does the implementation solve its stated equations?) from biological validation (do those equations reproduce independent observations?).

## A. Software verification
1. Unit audit: every state, parameter and rate carries a declared unit.
2. Limiting case: X=0 must yield zero biomass-dependent photosynthesis and respiration.
3. Limiting case: I=0 must yield zero light-driven gross photosynthesis.
4. Limiting case: no nutrients must suppress growth in the chosen limitation formulation.
5. Solver convergence: repeat with tighter relative/absolute tolerances and compare trajectories.
6. Reproducibility: identical version, inputs and solver settings produce identical tabular output within numerical tolerance.
7. Positivity: do not silently clip large negative solver states; detect and report them.
8. Conservation: test only after every relevant pool and flux is represented. A partial liquid-only model cannot claim total-system conservation.

## B. Biological validation
1. Select one organism, strain and culture protocol per validation dataset.
2. Record temperature, irradiance and spectrum, photoperiod, medium, pH, CO2 supply, culture age, density and acclimation history.
3. Split calibration and validation data before fitting.
4. Fit only parameters that are identifiable from the calibration observations.
5. Compare predicted and observed growth and oxygen rates on matching bases (cell, chlorophyll, protein or dry biomass).
6. Report MAE, RMSE, residual plots, parameter uncertainty and prediction intervals where supported.
7. Do not call a dataset independent if it was used to choose or tune the model structure/parameters.

## C. Initial benchmark candidates
- Broddrick et al. (2019), DOI 10.1016/j.ymben.2018.11.001: *S. elongatus* PCC 7942, low/high light acclimation, growth and oxygen-related physiology.
- Heydarizadeh et al. (2019), DOI 10.3389/fpls.2019.00471: *P. tricornutum*, carbon limitation and photon-flux density, oxygen evolution and respiration methods.
- Schellenberger Costa et al. (2013), DOI 10.1093/jxb/ers340: *P. tricornutum*, spectral quality and high-light photoacclimation; useful for model structure, not yet a complete numeric validation dataset.

## D. Validation status
Not yet validated. Candidate datasets have been identified, but raw numeric time-series and compatible normalisation have not yet been extracted. This document defines the procedure; it does not assert a successful validation.

# PBR-03 Validation Plan

## Evidence record requirements
For every dataset record organism/strain, genotype, temperature, irradiance and spectrum, photoperiod, pulse duration/timing, phase reference, sampling interval, replicate count, assay, uncertainty and culture conditions.

## Minimum datasets
1. KaiC phosphorylation time series in continuous light and continuous darkness.
2. Phase shifts after light-on and light-off pulses at multiple circadian phases.
3. Clock-output time series (for example, kai promoter reporter or RpaA-associated output).
4. Light-history acclimation time series with a clearly named measured trait (for example, pigment content, photosystem abundance or P-I response), including both upward and downward light transitions.
5. Metabolite/glycogen time series under light-dark cycles for wild type and clock-disrupted controls.
6. Independent validation series not used to fit model parameters.

## Analysis
- Fit light and dark PRCs independently; preserve phase convention and uncertainty.
- Quantify intrinsic-period error, phase error, entrainment success and phase stability.
- Fit acclimation half-saturation and directional time constants only to a declared measured trait; compare first-order response against alternatives.
- Compare free-running, entrained, shifted and irregular forcing.
- Separate direct light-driven responses from clock-dependent residual rhythms using constant-condition and clock-disrupted controls.
- Do not infer oxygen productivity from clock-output amplitude without direct matched oxygen measurements.

## Acceptance gates
- Full numerical test matrix passes.
- PRCs have traceable primary-source provenance and compatible experimental conditions.
- Predicted phase/period reproduce independent clock time series within predeclared tolerances.
- Acclimation state reproduces an independent light-history dataset for its declared trait.
- Any metabolic coupling is supported by an independently measured pathway-specific response.
- Clock-on/off comparisons use identical PBR-02 baseline parameters and forcing.

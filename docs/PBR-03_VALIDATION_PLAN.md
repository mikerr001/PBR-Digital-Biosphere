# PBR-03 Validation Plan

## Evidence required
For each dataset record organism/strain, genotype, temperature, irradiance and spectrum, photoperiod, pulse duration, phase reference, sampling interval, replicate count, assay and uncertainty.

## Minimum datasets
1. KaiC phosphorylation time series under continuous light and continuous darkness.
2. Phase shifts after light-on and light-off pulses at multiple circadian phases.
3. Clock-output (for example, kai promoter or RpaA-associated reporter) time series.
4. Metabolite/glycogen time series under light-dark cycles for wild type and clock-disrupted controls.
5. Independent validation series not used to fit PRCs.

## Analysis
- Fit light and dark PRCs independently; preserve phase convention and uncertainty.
- Quantify phase error, period error, entrainment success and phase stability.
- Compare free-running, entrained, shifted and irregular forcing.
- Distinguish direct light-driven metabolic responses from clock-dependent residual rhythms using constant-condition and clock-disrupted controls.
- Do not infer oxygen productivity from clock-output amplitude without direct matched oxygen measurements.

## Acceptance gates
- All numerical tests pass.
- PRCs have traceable primary-source provenance and compatible experimental conditions.
- Predicted phase and period reproduce independent clock time series within predeclared tolerances.
- Any metabolic coupling is supported by an independently measured pathway-specific response.
- Clock-on and clock-off comparisons use identical PBR-02 baseline parameters and forcing.

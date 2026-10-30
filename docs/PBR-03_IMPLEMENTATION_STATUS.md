# PBR-03 Implementation Status

## Implemented
- Organism-scoped circadian module for *Synechococcus elongatus* PCC 7942.
- Reduced phase oscillator with unwrapped and wrapped phase.
- Separate light-on and light-off periodic phase-response curves.
- Periodic PRC interpolation and instantaneous transition updates.
- Bounded morning-output proxy for downstream analysis.
- Daily, shifted and irregular light schedules.
- Validation of parameter dimensions, transition times and simulation inputs.
- Regression tests for free-running phase, neutral PRCs and phase resetting.

## Not yet implemented
- Molecular KaiABC phosphorylation/complex kinetics.
- ATP/ADP- and redox-dependent biochemical input model.
- SasA/CikA/RpaA signalling kinetics.
- Evidence-fitted in-vivo PRCs.
- Empirically calibrated output waveform/phase windows.
- Clock-dependent glycogen/metabolite allocation.
- Coupling to PBR-02 growth, photosynthesis or oxygen balances.
- Independent validation against measured time-series.

## Decision
Keep the clock subsystem independent until organism- and condition-matched data support a specific coupling mechanism. A passing software test suite validates code behaviour, not circadian biology.

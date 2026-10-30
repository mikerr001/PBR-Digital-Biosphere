# PBR-03 Circadian Regulation Model Specification v0.1

## Purpose and scope
PBR-03 adds a separately testable circadian timing subsystem for *Synechococcus elongatus* PCC 7942. It does not replace PBR-02 physiology and does not yet alter growth, carbon fixation or oxygen production. PBR-02 remains the no-clock physiological baseline.

*Phaeodactylum tricornutum* remains a separate marine comparison. No KaiABC equations or cyanobacterial parameters are transferred to this diatom.

## Biological basis
The primary organism has a post-translational KaiABC oscillator. KaiA promotes KaiC phosphorylation; KaiB antagonises KaiA activity as the oscillator progresses through phosphorylation/dephosphorylation states. KaiC timing communicates with output pathways including SasA/CikA and the response regulator RpaA. Light-dependent energy/redox state can influence clock timing through metabolic inputs. Clock output can influence metabolic timing, including morning metabolite partitioning.

The literature also shows that light-dark cycles can generate metabolic rhythms independently of the clock. Therefore observed daily oscillations must not automatically be attributed to circadian control.

## Implemented mathematical representation
PBR-03 v0.1 implements a **reduced phase oscillator with empirical phase-response curves (PRCs)**:
- Unwrapped phase advances at the intrinsic period between environmental transitions.
- Light-on and light-off transitions apply separate phase shifts.
- Each PRC is a periodic lookup table indexed by clock phase, with linear interpolation.
- A bounded morning-output proxy represents a candidate phase-gated clock output window. It is an output feature for analysis only; it is not a validated RpaA biochemical activity equation.

This phase model is deliberately not presented as a molecular KaiABC phosphorylation ODE. It avoids inventing kinetic constants for KaiA, KaiB, KaiC, SasA, CikA or RpaA when matched biochemical data have not yet been curated.

## Default parameter status
The intrinsic period and initial phase defaults are simulation scaffolding. PRCs default to zero phase shift, which means the default clock free-runs and does not entrain. This neutral default is intentional: it prevents fabricated entrainment. Experimental PRC values must be extracted for the correct strain, temperature, light intensity, pulse duration and phase convention before enabling a biological entrainment claim.

The morning output window and transition width are illustrative analysis settings, not experimentally calibrated transcriptional thresholds.

## Scenarios
- Free-running clock with no transitions.
- Repeated 12:12 light-dark schedule.
- Abruptly shifted light schedule.
- Irregular light-pulse schedule.
- User-supplied light transition sequence.

## Required comparisons
1. Environment-driven rhythm with clock disabled.
2. Clock phase model with zero PRC (free run).
3. Clock phase model with experimentally measured PRCs.
4. Phase-gated output proxy against measured clock-output/metabolite time series.

PBR-03 must not apply a generic sinusoidal multiplier to PBR-02 growth or oxygen rates. Coupling is deferred until a named metabolic pathway, measured response function and compatible time-series dataset are identified.

## Limitations and validation gates
- No explicit KaiC phosphorylation states (S/T sites), KaiA/KaiB complex kinetics or ATP/ADP-dependent kinase rates.
- No explicit SasA/CikA/RpaA biochemical network.
- No fitted in-vivo PRCs or organism-specific phase-response datasets yet.
- No metabolic feedback from glycogen/ATP/ADP/redox to the oscillator.
- No coupling to biomass growth, carbon fixation or oxygen balances.
- No validated Phaeodactylum clock model.
- No biological or experimental validation completed by this software milestone.

Before PBR-03 can be called biologically parameterised: curate primary-source phase-response data, define phase zero consistently, fit/interpolate PRCs, test entrainment range and phase stability, and compare predicted clock-output/metabolite timing with independent observations.

# PBR-03 Circadian and Acclimation Model Specification v0.2

## Purpose and organism boundary
PBR-03 adds separately testable timing and light-history states for *Synechococcus elongatus* PCC 7942. PBR-02 remains the physiological baseline. PBR-03 does not yet change growth, carbon fixation or oxygen production. *Phaeodactylum tricornutum* remains a separate marine comparison; no KaiABC equations or cyanobacterial parameters are transferred to it.

## Biological basis
The primary organism has a post-translational KaiABC oscillator. KaiA promotes KaiC phosphorylation; KaiB antagonises KaiA activity as the cycle progresses. Timing communicates with output pathways including SasA/CikA and RpaA. Cellular energy/redox state can influence clock timing, and clock output can influence metabolic timing. Direct light-driven metabolic responses can also generate daily rhythms without clock control; daily periodicity alone is not evidence of circadian causation.

## Implemented phase representation
A reduced phase oscillator represents clock timing using an unwrapped clock-hour coordinate. Its velocity is 24/tau clock-hours per elapsed culture-hour, where tau is the intrinsic period. Light-on and light-off events apply separate periodic phase-response curves (PRCs), interpolated linearly between equally spaced phase bins. Default PRCs are zero, so the clock free-runs until evidence-derived PRCs are supplied. The bounded morning-output window is an analysis proxy, not a biochemical RpaA activity equation.

This is not a molecular KaiABC phosphorylation ODE. It does not invent kinetic constants for KaiA, KaiB, KaiC, SasA, CikA or RpaA.

## Separate light-acclimation representation
A second, independent state describes generic light-history acclimation. Its target is I/(I+K), with separate first-order time constants for increasing and decreasing acclimation. It is driven by an irradiance time series and remains bounded in [0,1]. This is a phenomenological state descriptor, not a measured pigment, photosystem, enzyme or cell-volume variable. Its parameters are provisional and it is not coupled to photosynthetic productivity, growth or oxygen evolution.

The clock phase and acclimation state are intentionally separate: entrainment is not acclimation, and neither is assumed to improve productivity.

## Scenario suite
- Free-running phase, regular 12:12, shifted 12:12 and deterministic irregular light.
- Independent light-acclimation response to user-supplied irradiance histories.
- Comparisons should distinguish direct environmental responses from clock-dependent residual rhythms.

## Parameter status and limitations
Intrinsic period, initial phase, PRCs, output window, acclimation half-saturation and acclimation time constants are simulation scaffolding until matched experimental evidence is curated. There are no molecular KaiABC or SasA/CikA/RpaA kinetics; no ATP/ADP/redox feedback; no fitted in-vivo PRCs; no validated transcriptional output waveform; no glycogen/metabolite allocation model; and no coupling to PBR-02 carbon, growth or oxygen balances. No validated *Phaeodactylum* clock model is included.

## Required validation
Record strain/genotype, temperature, irradiance and spectrum, photoperiod, pulse timing/duration, phase convention, sampling interval, replicates, assay and uncertainty. Fit light/dark PRCs independently and report uncertainty. Validate free-running period and phase against independent time series. Validate acclimation kinetics against measured light-history-dependent traits before interpreting its state biologically. Use clock-disrupted controls and constant-condition experiments to separate circadian effects from direct light response. Any claim about oxygen productivity requires direct, matched oxygen measurements.

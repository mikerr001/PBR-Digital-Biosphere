# PBR-05 Supervisory Control Specification v0.1

## Scope
PBR-05 implements a deterministic supervisory decision layer that converts a synchronized, quality-checked sensor snapshot into bounded operator recommendations. It is deliberately not model-predictive control (MPC), not a safety interlock, and not an actuator driver. The integrated PBR-02/PBR-04 model is not experimentally validated, so its predictions cannot authorize automatic actuation.

## Inputs
Liquid temperature (°C), dissolved oxygen (mmol/L), measured PAR (µmol photons m⁻² s⁻¹), snapshot age, sensor validity/alarm flags, experiment-specific operating bands and maximum dimensionless actuator fractions. No universal biological setpoints are embedded. The operator must supply justified bands for the organism, medium, reactor geometry and measurement basis.

## Decision logic
1. Validate configuration and measurement finiteness.
2. If a required sensor is missing, invalid, alarming or older than the configured age, enter DEGRADED_HOLD and emit no actuator recommendation.
3. Temperature excursions take priority: suspend illumination at configured upper/lower limits; request cooling only within a configured maximum.
4. Dissolved oxygen excursions can request bounded gas exchange and reduce/suspend illumination at the configured upper band.
5. PAR above the configured band requests light reduction/suspension; low PAR prompts inspection rather than blindly increasing intensity.
6. In-band measurements maintain current settings.

Actions are dimensionless fractions in [0,1], not device-specific commands. Every decision requires operator confirmation. automatic_actuation_permitted is always false. CO2 dosing is excluded until DIC/CO2 carbonate chemistry and gas-transfer coupling are validated.

## Safety and limitations
- Research supervisory software, not a certified process-safety system.
- No redundant sensor voting, actuator feedback, interlocks, watchdog, emergency power or independent shutdown circuit.
- No dynamic state estimator, fault diagnosis, uncertainty propagation, MPC, optimisation or biological phase-aware scheduling.
- Temperature control has no heater model; low temperature causes illumination hold, not a heating command.
- Gas-flow advice assumes a configured gas-exchange actuator and does not model oxygen stripping, CO2 enrichment or mixing side-effects.
- Sensor age/validity is supplied by the caller; no sensor driver exists.
- Thresholds must be set from organism- and reactor-specific evidence, not copied from demonstration tests.
- Not for human oxygen supply, habitat operation, underwater life support or unattended biological operation.

## Verification and validation
Unit tests verify bounded outputs, fail-closed handling, threshold directionality and invalid configuration rejection. These are software verification only. Experimental validation requires calibrated sensor traces, independently justified operating bands, actuator response tests, disturbance/recovery datasets and blind holdout comparisons. Operator confirmation remains mandatory until these tests and an independent safety review are complete.

## PBR-05 exit criteria
1. Traceable operating bands for one organism/reactor/medium configuration.
2. Sensor calibration, synchronization, stale-data and fault-injection tests.
3. Characterized actuator response and safe-state behaviour on hardware-in-the-loop.
4. Disturbance and recovery tests against independent reactor measurements.
5. Model discrepancy bounds and independent process-safety review before closed-loop automation.

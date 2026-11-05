within ;
package PBRPlant
  model PumpPipeLoop
    "Lumped plant model; illustrative coefficients require calibration"
    parameter Real rho(unit="kg/m3") = 997;
    parameter Real g(unit="m/s2") = 9.80665;
    parameter Real pumpShutoffHead(unit="m") = 2.0;
    parameter Real pumpCurveCoefficient(unit="s2/m5") = 2.0e8;
    parameter Real pipeLinearResistance(unit="Pa.s/m3") = 2.0e7;
    parameter Real pipeQuadraticResistance(unit="Pa.s2/m6") = 1.0e9;
    parameter Real vesselArea(unit="m2") = 0.01;
    parameter Real initialLevel(unit="m") = 0.5;
    parameter Real outletFlow(unit="m3/s") = 0;
    Real flow(unit="m3/s", start=1e-5, min=0);
    Real pumpPressure(unit="Pa");
    Real pipePressure(unit="Pa");
    Real level(unit="m", start=initialLevel);
    Real volume(unit="m3");
  equation
    pumpPressure = rho*g*pumpShutoffHead
                   - pumpCurveCoefficient*flow*flow;
    pipePressure = pipeLinearResistance*flow
                   + pipeQuadraticResistance*flow*abs(flow);
    pumpPressure = pipePressure;
    volume = vesselArea*level;
    der(level) = (flow-outletFlow)/vesselArea;
    annotation(Documentation(info="
      Reduced plant-scale pump/pipe/tank model. Coefficients are placeholders,
      not manufacturer pump curves or measured hydraulic resistance. This is
      not a pressure-vessel or safety design model.
    "));
  end PumpPipeLoop;

  model ThermalInventory
    "Lumped thermal inventory with a controllable heat input"
    parameter Real mass(unit="kg") = 10;
    parameter Real cp(unit="J/(kg.K)") = 4180;
    parameter Real ua(unit="W/K") = 5;
    parameter Real ambientTemperature(unit="K") = 298.15;
    parameter Real initialTemperature(unit="K") = 298.15;
    input Real heaterPower(unit="W");
    Real temperature(unit="K", start=initialTemperature);
  equation
    mass*cp*der(temperature) =
      heaterPower - ua*(temperature-ambientTemperature);
  end ThermalInventory;
end PBRPlant;

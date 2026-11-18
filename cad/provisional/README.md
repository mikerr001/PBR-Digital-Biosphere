# Provisional flat-panel reactor CAD

**Status:** concept geometry for engineering iteration. Not a fabrication drawing, pressure-vessel design, validated reactor, or certified component.

## Coordinate system and envelope

- X: panel length, 300 mm.
- Y: panel height, 200 mm.
- Z: panel depth, 40 mm.
- Origin: geometric centre of the external rectangular body.
- Nominal wall thickness: 3 mm on all six faces.
- Nominal internal cavity: 294 × 194 × 34 mm.
- Gross rectangular body envelope: 2.400 L.
- Approximate rectangular internal cavity: 1.939 L, before port intrusions, fittings, headspace, internals or manufacturing tolerances.
- Overall model bounding dimensions including the 10 mm port bosses: 300 × 210 × 50 mm.

The internal volume is calculated from the nominal cavity dimensions, not inferred from the external envelope. The usable liquid volume must be determined later from the actual port/fitting geometry, required gas headspace, internal hardware and operating fill level.

## Port layout — provisional

Six ports are included in both CAD implementations:

| Group | Quantity | Position / orientation | Nominal bore | Boss outside diameter |
|---|---:|---|---:|---:|
| Sensor access | 4 | Rear Z face, axes normal to panel | 8 mm | 16 mm |
| Gas connections | 2 | Top Y face, axes normal to panel | 8 mm | 16 mm |

Sensor port centres are at X = −75/+75 mm and Y = −50/+50 mm, on the rear face (Z = −20 mm). Gas port centres are at X = −75/+75 mm and Z = 0 mm, on the top face (Y = +100 mm). Boss projection is 10 mm beyond the external face. These positions and dimensions are provisional placeholders, not a completed instrumentation or gas-distribution design.

## Files

- `flat_panel_reactor.scad`: OpenSCAD parametric solid model.
- `flat_panel_reactor.py`: CadQuery parametric solid model; exports STEP and STL.
- [Validation record](VALIDATION.md): local CAD-kernel and mesh checks.
- Both source files use the same nominal dimensions, coordinate system, port centres, bore sizes and boss geometry.

## Run

### OpenSCAD

Open `flat_panel_reactor.scad` in OpenSCAD, press F5 to preview and F6 to render. Use **File → Export → Export as STL** for a mesh. OpenSCAD is a separate CAD implementation; it does not require Python.

### CadQuery

Use a Python environment with CadQuery installed, then run:

```bash
python flat_panel_reactor.py --step flat_panel_reactor.step --stl flat_panel_reactor.stl
```

The script exports the shell-and-port solid in STEP and STL formats. See [VALIDATION.md](VALIDATION.md) for the checks completed on this provisional geometry.

## Engineering limitations and next gates

1. Confirm whether the vessel is intended to be a closed, sealed panel or an open serviceable assembly; the current model is a closed six-wall shell with six penetrations.
2. Confirm the actual sensor types, insertion depths, thread/connector standards, seals and cable glands. No threads, O-rings, flanges or fittings are modelled.
3. Define gas inlet/outlet functions, flow rates, diffuser geometry, liquid level and required headspace.
4. Add internal flow distribution, baffles, drainage, cleaning access, mounting features and optical-window details only after requirements are fixed.
5. Check wall thickness, material compatibility, fabrication method, tolerances and inspection access.
6. For CFD, export and verify the *fluid domain* separately. The existing repository Gmsh hand-off expects a single fluid volume and explicit boundary manifest; this shell model is not itself a CFD-ready fluid domain.

**Safety boundary:** this provisional geometry has no structural analysis, hydrostatic/external-pressure assessment, fatigue analysis, material qualification, seal design or experimental leak testing. Do not use it as a pressure vessel, occupied underwater component or life-support component.

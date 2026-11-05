# OpenFOAM case execution protocol

Target the OpenFOAM Foundation v10 cases already in `openfoam/`. Run in an
environment where that exact distribution is installed and sourced.

## 2-D channel smoke test

```bash
cd openfoam/channel-laminar
blockMesh | tee log.blockMesh
checkMesh -allTopology -allGeometry | tee log.checkMesh
icoFoam | tee log.icoFoam
```

## 3-D rectangular case

```bash
cd openfoam/rectangular-reactor
blockMesh | tee log.blockMesh
checkMesh -allTopology -allGeometry | tee log.checkMesh
icoFoam | tee log.icoFoam
```

A run is successful only if every command exits zero, the solver reaches its
configured end time, no fatal error appears, continuity errors remain bounded,
and inlet/outlet mass fluxes balance within a stated tolerance. The current
cases are smoke-test inputs, not yet analytically benchmarked CFD.

## Export and validation record

Preserve the full logs, OpenFOAM build/version, case hash, mesh statistics,
solver settings, convergence history, inlet/outlet fluxes, pressure drop and
mesh-refinement comparison. Do not label a case BENCHMARKED until it has been
compared with an independent analytical or experimental reference.

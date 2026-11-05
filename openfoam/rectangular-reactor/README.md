# 3-D single-phase reactor flow benchmark

This is a deliberately simple rectangular 3-D water-domain case for testing
OpenFOAM integration, mesh quality and field export. It is not the final CAD
photobioreactor and does not represent a bubble column.

Target: OpenFOAM Foundation v10, icoFoam. From this directory run:
    blockMesh
    checkMesh
    icoFoam

The domain is 0.30 m x 0.10 m x 0.10 m. The inlet is a low-speed uniform
velocity, outlet fixed pressure, remaining walls no-slip. Water kinematic
viscosity is 1e-6 m2/s. The nominal inlet Reynolds number based on 0.10 m
hydraulic scale is 100. The case is laminar by construction.

Acceptance: blockMesh and checkMesh complete with no fatal errors; icoFoam
converges to a steady solution; mass imbalance is small; refine the mesh and
compare centreline velocity and pressure drop before promotion to BENCHMARKED.

No CFD output is claimed until this case is executed in an OpenFOAM runtime.

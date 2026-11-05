# OpenFOAM laminar channel benchmark (starter case)

This case is a solver-integration smoke test for incompressible, single-phase
flow. It is deliberately a 2-D planar channel, not a photobioreactor and not
a substitute for the eventual CAD-derived vessel mesh.

Target: OpenFOAM Foundation v10 with icoFoam. Run from this directory:
1. blockMesh
2. icoFoam
3. postProcess -func 'patchAverage(name=outlet,p=p)' (if supported by local build)

The geometry is 1 m long, 0.1 m high, one-cell thick in z (empty front/back).
No-slip walls, uniform inlet velocity and fixed-pressure outlet. The mesh and
boundary conditions are a numerical smoke test only; compare the solution to
the laminar plane-Poiseuille analytical profile before calling it benchmarked.

Do not infer photobioreactor flow performance from this channel case.

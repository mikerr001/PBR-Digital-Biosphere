# PBR-07 — Upstream Platform Selection
**Status:** Provisional architecture decision (ADR-001)  
**Date:** 2026-10-31

## Decision

Use **ToubkalCAD** as the preferred upstream CAD application to fork and adapt for the PBR-07 3D engineering workspace.

Repository: https://github.com/ToubkalCAD/ToubkalCAD  
License observed in upstream LICENSE: MIT  
Upstream default branch observed: main  
Upstream repository size observed during review: approximately 94 MB (GitHub repository size metric; not a checkout size).

This is a candidate selection, not a completed fork. The available GitHub connection exposed read and repository-content write operations but no fork-creation operation. No fork or copied upstream source has been created by this decision.

## Why ToubkalCAD

The upstream project already provides:
- Browser-based parametric solid and surface CAD.
- OpenCascade.js compiled to WebAssembly.
- Three.js viewport.
- React 18 UI, Zustand scene state and Dockview panels.
- Feature history and recomputation.
- Sketch constraints, extrusion, revolve, loft, sweep and Boolean operations.
- Assemblies, measurements, STEP and IGES exchange.
- A documented geometry registry and WASM memory ownership pattern.

This is substantially closer to the desired 3D engineering editor than creating a new viewer or a generic Three.js scene.

## Important constraints discovered in upstream documentation

- Node.js 20.19+ and npm 10+ are listed as requirements.
- OpenCascade WASM is approximately 48 MB and requires SharedArrayBuffer.
- COOP and COEP cross-origin isolation headers are mandatory.
- Upstream documentation states the CAD kernel currently runs on the main thread. Long-running geometry operations can block the UI.
- Geometry kernel objects have explicit WASM memory lifetimes. PBR features must use the upstream registry/service pattern rather than storing kernel objects in Zustand.
- Upstream is actively developed; APIs and file behavior may change. Pin a specific commit before modifying.

These constraints make a direct phone-only build unrealistic. The development target should be a hosted GitHub/CI build with browser testing; the phone can inspect the hosted result and make lightweight edits where practical.

## Alternatives considered

### Chili3D — https://github.com/xiangechen/chili3d
Browser CAD built with TypeScript, OpenCascade/WASM and Three.js. It is a credible alternative, but its current feature/API fit and license details were not fully audited in this review. Do not combine two full CAD editors.

### JumpStart 3D — https://github.com/MaxSikorski/jumpstart-3d
A capable browser CAD project with a compact standalone option. Its community version is AGPL-3.0-only from build 24 onward, which imposes source-sharing obligations when operating a modified version for users. This is a less suitable default if the project wants a permissive license.

### Three.js Editor
Useful as a scene editor, but it does not provide the same parametric solid CAD foundation and engineering feature history as ToubkalCAD.

## Fork and adaptation procedure

1. Create a GitHub fork of ToubkalCAD under the project owner's account. Preserve the upstream repository relationship and commit history.
2. Record the exact upstream commit SHA, license text, third-party notices and dependency lockfile.
3. Create a PBR integration branch; do not immediately replace the upstream UI or CAD core.
4. Build and test the unmodified fork first.
5. Add PBR modules as isolated packages/features: component catalogue, physical domains, ports, project manifest, solver adapter, results viewer.
6. Keep upstream CAD kernel ownership, geometry registry and memory-management invariants intact.
7. Add a documented upstream sync policy and test every merge.
8. Only after the CAD shell is stable, connect the existing Python PBR-Digital-Biosphere package.

## License and attribution requirements

The upstream ToubkalCAD repository declares MIT. Preserve the original copyright and license notice in substantial copies or derivatives. Retain all third-party notices and audit every dependency and asset separately. This note is not legal advice.

## Go/no-go gates

- **Gate A — license:** confirm current upstream LICENSE and third-party notices at the exact fork commit.
- **Gate B — build:** unmodified fork builds in GitHub Actions and launches in a browser with required headers.
- **Gate C — geometry:** create, edit, save, reopen and export a simple vessel assembly without WASM leaks or corruption.
- **Gate D — PBR schema:** PBR component parameters and ports survive save/reopen and schema migration.
- **Gate E — simulation:** solver input is derived from a frozen CAD project snapshot and produces reproducible run metadata.

Do not begin PBR physics integration until Gates A–C pass.

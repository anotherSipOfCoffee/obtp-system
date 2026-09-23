# System direction — WikiHouse adoption
Decision recorded 2026-09-23 from the owner's explicit choice to adopt the WikiHouse structural system.

## Active direction
Use WikiHouse Skylark components and their documented connections together. The previous independent frame with non-load-bearing panels is superseded. LT080, bespoke research-joint modelling and mixed commercial connector selection are parked. Do not transplant WikiHouse joints into the former post/beam geometry.

Archive: branch `archive/independent-frame-v02`, commit `f284e74548bc68d81bc5d2b8995ba153d52ba117`. It preserves the old model, tests, rules and source research. The owner requested replacement of the active catalogue with WikiHouse objects. The main dist/ page now lists W-S as its first imported wall block and exposes its seven source parts. The previous provisional objects and assemblies are absent from the active app; their code and tests remain available in the archive branch. This is a source-geometry catalogue, not a validated building system.

## Source baseline
Repository: https://github.com/wikihouseproject/Skylark
Pinned commit: `6581cc1de0f4daef81a6b5c5a2eaed3c537d1d8f`
README calls this Skylark v1.0. The current blocks page links to skylark_v1, which GitHub redirects to main. Use the pinned commit, not a moving branch, for geometry and quantities.

The inspected tree contains SKYLARK150 and Test, with 58 .3dm and 517 .dxf files, and no .gh/.ghx definitions. These are file counts, not a validated block count. The website labels Skylark 150 beta and Skylark 200 files in progress. Older 200/250 guides must not supply dimensions or capacities without a demonstrated match to this release.
https://www.wikihouse.cc/blocks

## First candidate
Inspect the existing W-S wall block, rather than inventing a component. See `WIKIHOUSE_SOURCE_LOCK.json` for exact file paths and blob hashes. The .3dm, CNC DXFs and production CSV exist; the uploaded .3dm has been hash-verified and inspected. Seven valid solid Breps form one instance; all faces have saved render meshes. CNC files have not been geometrically matched to those parts. Start with one block and its parts, then a documented adjacent-block connection.

Preserve original units, source part IDs, shape, materials and connection arrangement. Do not offer arbitrary resize sliders. Keep display mesh simplification separate from authoritative CAD.

## Licence and attribution
The repository README specifies CC BY-SA 4.0 and credits the WikiHouse team at Open Systems Lab. Retain source notices and attribution with any imported/derived geometry and mark changes. Review per-folder terms before importing. OBTP is not endorsed by WikiHouse. Do not relabel the entire existing codebase under the geometry licence automatically.

## Rhino to web
Reuse the existing offline export/assembly approach in the v74 package:
`04_SHARED/RHINO8_OFFLINE_PILOT/`.
Its user export records 125 assets, two variants and Rhino 8.34 runtime metadata. That is prior workflow evidence for architectural geometry, not validation of these new blocks.
Import the official .3dm in Rhino 8, audit objects and units, export meshes from those source objects, and compare web geometry against Rhino. Any new Grasshopper definition is an OBTP import/export wrapper unless official parametric source is found. Do not claim WikiHouse supplies GH definitions in this snapshot.

## Limits and next work
1. Materialize and inspect the pinned W-S .3dm and CNC files through supported tools.
2. Establish source part counts, units, solids/meshes, joinery and per-file notices.
3. Adapt the existing export/viewer contract while preserving part identity.
4. Add exploded/section inspection and a documented connection example.
5. Complete Rhino and browser visual verification. The owner explicitly requested catalogue replacement before those remaining checks; do not describe the new catalogue as fabrication-ready.

W-S source render meshes are imported. Read WS_GEOMETRY_AUDIT.json and WS_CHECKPOINT.md for validation limits. Research/testing on another WikiHouse generation does not automatically validate these blocks. Missing source details remain unresolved. Studio and Architecture are unchanged. Drive v74 has not been updated.

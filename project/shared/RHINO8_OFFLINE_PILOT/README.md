# OBTP offline component pilot 0.1

Prepared 23 September 2026. No real Rhino/GH solve has been run here. No .gh, .3dm or real exported mesh is included. The native builder must run in your installed Windows Rhino/Grasshopper. Confirm Rhino version before setup troubleshooting.

## Accepted direction
- Customer dimensions adjustable in fixed increments; the actual step and dimensional range remain open.
- Browser assembly from reusable components, without requiring a continuously running Rhino server.
- Architectural geometry first: walls, openings, rooms, roof. Supplier assemblies, structural review and fabrication detail follow later.
- PC available now. Rhino version not yet confirmed.

## What this first pilot proves
Two existing supported reference cases (15 m with 3 bedrooms; 18 m with 4 bedrooms, both 7.2 m wide) are decomposed into exact local shape assets and translated component instances. Across them there are 125 distinct shapes; 72 occur in both houses. Instance counts are 465 and 545. Many are display details, not manufactured parts. This is computational reuse, not a validated physical building kit.

Grasshopper generates each unique shape once as a Brep and mesh. The browser places those exported meshes by identity and translation. It never stretches a wall mesh to invent a new size. The .3dm architectural references retain Breps separately from the web meshes. All current component dimensions remain provisional and the wall/roof objects are study primitives, not detailed assemblies.

This pilot does NOT yet support intermediate house sizes. After the reuse path passes, define an increment and range, adjust the planning rules, generate required size-specific assets and validate legal combinations. Do not market a 300 mm grid, or any other grid, as approved. An increment is not automatically a structural bay or panel size.

## Local run (requires Windows Rhino + Grasshopper + legacy GhPython)
1. Extract the entire ZIP to one folder. Open Rhino and run `Grasshopper` once to load it.
2. In Rhino, run `RunPythonScript` and select `grasshopper/build_offline_definition.py`.
3. When asked, select the included `grasshopper/house_mesh.py`.
4. Choose a NEW output filename for `obtp_component_library.gh` in an empty test folder. Use new names on retries to preserve earlier results.
5. Success writes a native .gh, a raw reference mesh JSON, two .3dm reference houses and `.gh.offline-kit.json`. If the legacy component or an API is unavailable, report the exact error; do not treat partially written files as a passed run.
6. Open the two .3dm files in separate Rhino documents. Their units are metres. Check overall dimensions, openings, roof and component names. GH preview overlays local assets at the origin; that preview is not an assembled house.
7. Close Rhino. Open `viewer/index.html` in Edge/Chrome, choose the generated `.offline-kit.json`, switch houses and toggle Inside. The camera stays at 45 degrees horizontally with constant elevation/framing.

No Node installation, Compute server, API key or network request is required for these run steps. `make_catalogue.cjs` is a development provenance script referencing the earlier sibling foundation source; it is not a user setup requirement.

## Pass conditions
- Actual GH output is produced without solve errors, with all expected asset IDs.
- Both CAD reference houses open with correct metres and nominal dimensions.
- Browser assembles the correct component count and dimensions for both cases.
- Switching works after Rhino is closed and network access is disabled.
- Doors/openings visually correspond between CAD and mesh. Roof-off mesh clipping is display-only and is not a capped construction section.
- Save the exact error or success result, Rhino version and screenshots. A successful run validates this export/assembly route only, not supplier or engineering correctness.

The file's producer string is a provenance record, not cryptographic proof of an authentic Rhino solve. Only use exports you generated or reviewed. Current viewer restricts the pilot format and mesh sizes; it is a local test harness, not a hardened public upload service.

## Next architecture batch
Define which dimensions can change, their increments and bounds; retain room/function constraints; add versioned assembly rules and valid connection interfaces; expand the catalogue only for supported cases. Consider a browser rule assembler after the two explicit manifests pass. Live generation remains optional for future exceptional inputs.

## Verification performed here
Python syntax; local-coordinate decomposition and reconstruction against original component coordinates; synthetic mesh fixture assembly; invalid identity/index/unit rejection. Synthetic fixtures never enter the deliverable viewer as claimed Rhino geometry. Real Rhino API execution, real browser/device QA and professional validation remain outstanding.

Existing Drive package and published website were not updated by this separate working test kit.

## Source references
- Rhino script runner: https://developer.rhino3d.com/guides/rhinopython/python-running-scripts/
- Compute alternative (not required here): https://developer.rhino3d.com/guides/compute/compute-faq/
- Prior primary-source study: https://www.shapediver.com/blog/desktop-vs-cloud-computation-time-explained
- Display-format background: https://www.khronos.org/gltf/

Pilot uses the existing mesh JSON contract to minimize new dependencies; GLB optimization can follow after geometry parity. Plain JSON does not replace the CAD source.

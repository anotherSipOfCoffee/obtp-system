# W-S source geometry checkpoint — 2026-09-23

## Delivered
- The user requested full replacement of the active object catalogue. Root System now displays Wall blocks → W-S and its seven selectable parts. `dist/ws/` remains a direct link to the same viewer. The old frame objects and assemblies are removed from the active application and preserved on `archive/independent-frame-v02`.
- Seven source parts, assembled and exploded viewing, orbit/zoom, standard views, selection, isolation and horizontal uncapped clipping.
- `dist/ws/model.json`, `WS_GEOMETRY_AUDIT.json`, reproducible `tools/export_ws.py`, and `tools/verify_ws_rhino8.py`.
- Source attribution and original CNC-folder terms retained in `dist/ws/`.

## Source evidence
Uploaded W-S.3dm is 7,373,621 bytes and exactly matches official Git blob `932338ca81fdc2acdd345cd0fc9df09d2a9888b2`. Official source commit is in WIKIHOUSE_SOURCE_LOCK.json.
Seven valid, solid Breps are definition objects in one block definition, used by one instance. The instance reflects Z. It is applied once; definition objects are not duplicated as scene objects.
All 1,478 Brep faces have saved render meshes. Converted packet contains 23,482 coordinate-welded vertices and 47,038 triangles before renderer removal of any degenerate triangles. Coordinates remain in millimetres, rounded to six decimals.
Mesh envelope is approximately 600 × 186 × 2100 mm. Brep topology vertex bounds differ from mesh bounds by at most 0.0010991 mm. Conservative Brep bounding boxes extend beyond trimmed faces; those loose boxes are retained in the audit but are not substituted for physical part dimensions. This bounds comparison does not measure surface deviation or establish manufacturing accuracy.

## Reuse of v74 workflow
Retains the offline CAD → identified mesh assets → browser display architecture from `04_SHARED/RHINO8_OFFLINE_PILOT/`. Existing pilot renderer was used for a local geometry preview. New browser rendering uses WebGL for the denser W-S geometry.
`obtp-source-mesh/1` is a separate packet contract: millimetres, cached-source-mesh provenance, source lock and one assembly. It is deliberately not passed to the old pilot validator, which requires metre units, RhinoCommon/GH provenance and two house variants. No new GH definition is claimed, and no Rhino 8 execution is claimed.
The source IDs are retained. P01–P07, descriptive names, colours and display explosion offsets are OBTP additions, not official CNC labels, materials certification or assembly instructions.

## Verification and remaining limits
- Passed source SHA, source units, seven valid solids, all cached meshes present, transformed topology-bound comparison and coordinate rounding checks.
- Passed `node tests/ws.cjs` (finite coordinates, valid triangle indices, identity, counts, reflection and audit limits).
- Passed JavaScript syntax check.
- Browser visual/interaction QA not completed: Playwright browser installation failed because its downloads were unavailable/truncated. Treat the new page as a validation preview.
- Rhino 8 comparison not run. Run `tools/verify_ws_rhino8.py` in Rhino 8 Windows ScriptEditor (Python 3), select original W-S.3dm and downloaded model.json, then save the report. It checks validity and Rhino bounds without changing your open document. Inspect the source and web view visually as well.
- CNC labels/quantities not mapped to these seven solids. Adjacent-block connection and assembly order are not yet established. No engineering or fabrication validation.
- Studio, Architecture and Drive v74 are unchanged.

## Continuation options
1. Recommended: Rhino 8 comparison and browser review; resolve any mismatch before expanding.
2. Map official CNC labels and drawings to the seven source IDs.
3. Trace and model an official adjacent-block connection from the same pinned release.

## Pages routing
Both branch-based Pages and the custom dist/ workflow were observed on this commit. Root index.html and ws/index.html redirect into dist/ for branch publishing. The custom workflow serves dist/ directly. This preserves the same entry links with either deployment; choosing GitHub Actions as the sole Pages source would remove the duplicate deployment jobs.

## Catalogue replacement verification
User-authorized replacement includes the root page, object list and source viewer. Legacy dist/app.js, dist/kit.js and their two tests are removed from main, with the archive branch retaining them. Source meshes are unchanged. Geometry checks, JS syntax and local asset/link resolution pass. The viewer resolves model.json relative to its script, so both root and /ws/ routes load the same geometry. Browser rendering and Rhino 8 comparison remain pending.

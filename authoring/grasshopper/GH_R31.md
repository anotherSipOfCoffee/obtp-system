# R31 — layout-driven box, foundation and detailed roof

Extract the complete ZIP to a fresh folder. In Rhino 8, open a millimetre document and Grasshopper, then run `CREATE_ROOM_CONFIGURATOR.py` with Python 3. This creates and saves a new timestamped GH definition; already-open definitions remain untouched. Do not use the historical `CREATE_GRASSHOPPER.py` for this workflow.

Separate definitions remain available through `CREATE_LAYOUT_GRASSHOPPER.py`, `CREATE_STRUCTURE_GRASSHOPPER.py` and `CREATE_DETAILING_GRASSHOPPER.py`. Use their JSON handoffs or wire outputs directly on one canvas. `TIDY_GRASSHOPPER.py` rearranges only owned OBTP groups.

## Changes

- B1 Box generates cassette timber and panels from physical wall runs, room bounds, openings and levels. It does not call preset selection or replay preset member commands. Presets are upstream layout generators; architectural fixtures and finishes remain downstream.
- B2 Foundation and B3 Roof are separately inspectable and replaceable. B4 checks that all three inputs reference the same plan and compatible dimensions. Terrace Yes/No now belongs upstream and feeds both foundation and roof to prevent inconsistent support and roof extents.
- The detailed canonical roof is restored: bearing framing, backing sheets, edge closures; the sloped metal roof also includes counter-battens and seams. The simplified R30 roof generator is removed.
- Preview offers Structure + panels, Building without facade system, Complete with cladding, and Skeleton only / no panels. Cladding attachments follow facade visibility. These are display filters; quantities do not change.
- Floor-plan preview uses native Custom Preview. Selected drawing sheets also appear below the building in model space, with text tags. Use Zoom Extents. Turn the drawing preview off when concentrating on the building.
- Successful native exports create paper-space layouts and a separately named MODEL SHEETS layer in Rhino model space. The same drawing recipe drives both. Six sets remain: parts, assembly, loose layout, simplified project, CNC review and material costs.
- All export text writes explicitly use UTF-8, fixing the reported Windows charmap failure on Lithuanian characters. Rate files accept UTF-8 BOM.
- Package includes only the current generated review artifacts; historical source workflows remain available.

## Compatibility and limits

Regenerate the Layout handoff in R31: old R30 files containing stored construction commands are rejected explicitly. Custom plan inputs remain supported within the documented rectangular, single-row domain, 1200 mm depth coordination and supported physical wall sections. This is not a general arbitrary-polygon structural solver. Detail contexts for preset-specific fixtures must agree with the plan footprint.

Connected wall drawings are assembly explanations, not certified lifting units. Spans, foundations, connections, header bearings, weather layers, supplier compatibility and lifting capacity remain engineering holds. CNC sheets are review documents, not verified toolpaths. Material cost sheets require supplier rates and do not include labour or certify a quote.

## Verification

152 automated tests passed, including changed wall geometry driving framing, no preset calls during box generation, detailed roof equivalence, stale branch rejection, facade/skeleton preview filtering, open-edge header clash checks and simulated Windows encoding during native-export orchestration.

Portable review artifacts cover Sauna M with extension, Studio M with and without extension, and a Living Studio study. The Studio extension sample uses the detailed single-slope roof. Reopen checks confirmed four solid 3DMs and all 24 PDFs (289 readable pages). Representative plan, connected-wall erection and detailed roof assembly pages were rendered and visually inspected. The focused 30 room-pipeline tests passed again after final preview changes. See `review-r31/index.html` and `summary.json`.

Native Rhino/Grasshopper is unavailable in the cloud environment. Component creation, Text Tag 3D display, model-space baking and Rhino FilePdf output still require native acceptance. The reported encoding cause is regression-tested; portable PDF proofs do not substitute for native PDF execution.

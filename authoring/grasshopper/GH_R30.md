# R30 — presets, quiet canvases and model-linked documents

Extract the **complete ZIP**. Open a millimetre Rhino document and Grasshopper. Run one creator using Rhino 8 Python 3:

- `CREATE_LAYOUT_GRASSHOPPER.py`: preset and plan preview.
- `CREATE_STRUCTURE_GRASSHOPPER.py`: plan input, cassette, roof, foundation and skeleton preview.
- `CREATE_DETAILING_GRASSHOPPER.py`: skeleton input, finishes, assembly preview and exports.
- `CREATE_ROOM_CONFIGURATOR.py`: these same stages connected in one document.

Each adds a fresh document while leaving other definitions open. `CREATE_GRASSHOPPER.py` and `CREATE_RESEARCH_GRASSHOPPER.py` remain older independent workflows; use the four files above for R30. Native `.gh` files are generated on your Rhino installation, not pre-generated in this cloud environment.

## Controls

Layout has Sauna, Studio and Living Studio study; S/M/L; Extension Yes/No; and two window choices. No room-function lists, relationship editors or dimension sliders are on this canvas. The underlying custom-plan generator remains callable by replacement components.

- Sauna reuses the earlier canonical plan dimensions and integrated extension geometry: storage, outdoor shower and bench.
- Studio Extension Yes retains workspace, central passage and the second preparation block. Sliding enclosures are included and shown open by default.
- Studio Extension No removes the preparation block. The retained central room has opposing fixed windows instead of sliders. A west-end external entrance is added to maintain access; the workspace-to-centre door remains. This is an architectural adjustment, not an unchanged old no-storage preset. Review the supplied plan before adopting it.
- Living Studio is the previous living/sleeping, bathroom and kitchenette **study**. S/L are bounded one-cell variants. Extension No removes the kitchenette zone and shortens the plan; it is not a complete dwelling specification. Equipment, access and residential suitability require further design.
- Window choices are 580 mm frame / nominal 900 host, or 1180 mm frame / nominal 1800 host. The installation opening adds 20 mm; structural jambs and terminal constraints are resolved separately. Actual host extents can span adjacent cells. These are geometric candidates, not supplier-approved products.
- Structure retains cassette, flat/single-slope roof and foundation choices.
- Detailing has Terrace Yes/No (1200 mm depth) and panel build-up. Vertical timber façade is always included. Sauna extension owns its shower/bench; they are no longer independent terrace decorations.

## Replaceable stages

The handoffs remain `obtp-room-config/1` plan and skeleton, then `obtp-room-scene/1`. File envelopes are `obtp-handoff/1`; dimensions are mm. Direct component wires and file import/export both work. Live input wins; invalid data never falls back to an old file.

Preset generation is in `obtp/room_presets.py`. It is **not called by structure or detailing**. A custom component may emit a supported room plan using `room_config.programme`, `rules` and `solve`, or an explicit cassette blueprint with context and wall/member commands. Blueprint plans store wall runs derived from those commands; the adapter verifies agreement. IDs and hashes must be regenerated after changes. Checksums establish consistency, not engineering validity.

The supported domain remains single-level rectangular strips with explicit supported wall/opening commands. A new input source does not automatically add support for arbitrary curves, multi-storey geometry or unsupported topology. Replacing a skeleton component must supply parts, deferred panels/cover, openings, dimensions and required detailing interfaces; the tests verify edited skeleton members reach detailing.

See GH_R29.md for the file-handoff procedure. Keep generated definitions beside the bundled Python modules. Restart Rhino after modifying cached source modules in place.

## Canvas organisation

Creators arrange owned groups into consistent control / processing / result columns. `TIDY_GRASSHOPPER.py` applies the same arrangement to the active definition's `OBTP / ` groups. It changes positions, not wires or values; unrelated groups are ignored. Other open definitions are untouched. Native pixel-level placement still needs Rhino acceptance.

## Documents

In Detailing (or the combined definition), set **destination** and **rates_path** in E / DOCUMENTS. Turn **Generate layouts + PDF** on once. Turn it off before another export. The rising-edge guard prevents repeated layouts during unrelated recomputation.

Six sets are generated from the same scene:

1. Parts: core structure, panels and insulation; per-type axonometrics and IDs.
2. Assembly: connected walls laid flat, raised and installed. No certified lifting units.
3. Separate loose-parts layout.
4. Supaprastintas projektas **review drawings**: plan, sections and elevations with missing site/engineering scope stated. Not a completed statutory project.
5. CNC review: dimensioned plywood sheets, supplier instructions, quantities, instance IDs and 1:1 DXF outlines for non-sloped rectangular sheets. No nesting, toolpaths, holes or tolerances are invented. Sloped sheets stay scheduled but require a separately resolved manufacturing route.
6. Approximate materials costs, with an editable `material-rates.json`.

Parts and assembly omit only façade cladding; separate cladding quantities are written to JSON. The complete model retains cladding. Costs reconcile all modelled pieces, with façade boards labelled separately. Three sourced price proxies are provided; unpriced materials remain explicit and the displayed sum is a **partial priced subtotal**. VAT conversion and waste allowance are stated assumptions. Timber grades, sheet grades and supplier suitability are unverified. Labour, CNC machining, delivery and unmodelled fasteners are excluded.

In Rhino, layouts are created in the **active Rhino document** and PDFs/recipes/DXFs are saved under the chosen destination. Save that Rhino document to retain editable layouts. Native printing uses Rhino, without ReportLab or external Python dependencies. If printing fails, the receipt reports failure; it never reports a successful PDF instead.

`review-r30/index.html` contains portable examples, PDF proofs and geometry-only 3DM files. Portable PDFs are explicitly labelled as not Rhino printouts. Geometry-only 3DM files do not contain Rhino layouts.

## Validation

The existing 139-test suite passed. Seven new R30 tests passed, covering all 36 preset choices, extension geometry, independent custom plans, replacement skeleton propagation, remaining controls, document reconciliation, valid DXFs and invalid inputs. Four example models and all six document sets were regenerated. All 24 PDFs reopened with readable page text; all four 3DMs reopened with matching piece counts and solid geometry. Representative PDF pages were visually reviewed. Native Rhino/GH execution and native layout/PDF printing remain untested here.

No website, Studio, Architecture or Drive changes. Existing GitHub PR remains unmerged.

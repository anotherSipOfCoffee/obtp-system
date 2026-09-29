# R24 — Sauna preset → layout → cassette → 3D

28 September 2026. Main scope is Sauna and cassette only. Neither website is changed.

## Start

Extract the complete package into a new writable folder. In Rhino 8 Python 3, with Grasshopper open, run `CREATE_GRASSHOPPER.py`. This creates a new `OBTP_Sauna_Cassette_R24_1_*.gh`. Keep the generated definition beside the bundled folders. Native Rhino/GH is unavailable here: the package contains the generator, not a pre-generated or host-tested binary definition.

The canvas runs left to right:

1. **Sauna preset / programme** — exactly S without storage, S with storage, M without storage, M with storage, L without storage, L with storage, **Custom**. Default: M without storage.
2. **Layout plan** — resolves the selected room programme and relationships. Outputs room planning geometry and a checked JSON document. It does not generate a hidden building.
3. **Cassette construction** — consumes that resolved document. Cassette is fixed; no system dropdown or optional planning switch.
4. **3D model** — existing material/core preview and connected-wall assembly animation. Drawings, model export, quantities and analysis preparation use the same cassette scene.

The plan preview is at Y = −7500 mm; the building stays at its existing origin. Zoom Extents in Rhino. Native Text Tag 3D is wired when its recognised input ports are available; label outputs/panel are always present.

## Saved presets versus Custom

Saved presets load the established room sizes, storage state, relationships and original order. Inputs labelled **Custom** stay visible for editing but are ignored until the seventh option is selected. There is no additional “use custom” switch. Roof, window frame width, wall height and foundation settings apply to every preset, as in the existing model. Sauna entrances remain 900 mm and partitions 90 mm in this bounded adapter; do not infer arbitrary opening design from the room graph.

**Custom** uses the visible room toggles, lengths in 900 mm cells, depth in 1200 mm cells, relationship selectors and arrangement index. Activation and relationships remain separate: disconnecting rooms does not delete them. Invalid graphs or unavailable arrangement indices produce an error; no alternative plan is substituted silently.

Saved no-storage presets retain their original exterior shower fixtures, despite having no dedicated outdoor/storage room zone. This preserves the six worked-out models exactly. In Custom, explicitly switching the whole outdoor zone off also omits its three shower pieces. This is a programme change, not a part-standardization saving.

## Current construction boundary

The existing sauna–entrance strip arrangement, optionally followed by the outdoor/storage zone, can produce construction. Other active-room sets/orderings can be inspected as plans, but construction output stops with **PLAN ONLY**. No stale, default or previous model is substituted. The future step is to implement those additional topology/opening/envelope rules; this release does not claim an unrestricted floor-plan-to-building solver.

The new construction component receives only the resolved layout document. Before producing parts it revalidates that document and checks resulting footprint, finished room dimensions and passage positions. Editing coordinates inside its JSON without resolving them again is rejected. The current cassette recipes remain the construction engine; they are not independent duplicated geometry pipelines.

## Preserved research and exports

Studio, WikiHouse and B are removed from the main canvas, not deleted from the project. Run **CREATE_RESEARCH_GRASSHOPPER.py** separately for the preserved R23 research canvas. Its original presets, systems, inspection controls and optional planning experiment remain historical/research tools. It does not drive the new main definition.

Existing 3D preview, assembly progress, unique-type colours, part IDs, drawing/model export, loose-part documentation recipes and analysis preparation are retained. Existing Studio PDFs are bundled as previous references; this release does not enable new Sauna PDF actions. The original GH export action continues to state that PDF generation is disabled.

`review-r24/review.html` shows all seven selections. `EXPORT_SAUNA_WORKFLOW.py` regenerates these diagrams from the same workflow. `tools/package-gh.py` bundles the current package. B remains an interpreted, unengineered research concept, not a certified CompassWood building system.

## Validation

Focused tests verify exact saved-preset geometry/drawings over twelve preset/roof cases; ignored custom inputs on saved presets; active custom dimensions; no construction before the layout stage; no fallback on unsupported custom layouts; stale-document rejection; invalid settings; and absence of obsolete generators/selectors on the main canvas. The complete portable suite remains enabled.

Native GH canvas creation, text tags, slider interaction and native preview/export execution still require testing in Rhino. Structural capacities, fastening, handling, wet-area details and supplier compatibility remain unresolved as before.

## R24.1 — Rhino component creation compatibility

Removed a redundant `SetSource` call from both canvas creators. Source is supplied to `Python3Component.Create(name, code)` before configuring ports. This fixes the reported missing-method exception without changing geometry, parameters or the sequential workflow. A regression executes both actual component factories against an API double with no `SetSource`, checking source, ports, access and maintenance. Native Rhino execution remains outstanding. Extract R24.1 into a fresh folder and run its creator.

# GH R22 — three-system comparison

27 September 2026. GH-only review release. Neither website is changed.

## Start

Extract the **whole ZIP** into a new writable folder. Open Rhino 8 and Grasshopper. In Rhino's Python 3 ScriptEditor run `CREATE_GRASSHOPPER.py`. It creates a timestamped R22 native `.gh` next to its bundled `obtp`, `components` and `comparison_data` folders. Keep these together. The package supplies the generator, not a pre-generated native GH binary: a licensed Rhino/Grasshopper host was unavailable for this release.

Existing building controls, normal/material preview, progress/core sliders, connected-wall erection layout, loose-part layout and PDF export remain on their original pipeline. New group **F** adds an independent comparison preview 18 m along X; Zoom Extents if needed. Disable the original Custom Preview if you want only the comparison visible. Model source is frozen at Studio's canonical System commit `724c70c4165bbed23f0ce0dc811466bff15c9987`.

| System selector | Geometry and controls |
|---|---|
| 1 / WikiHouse | Original pinned Skylark meshes, 1–8 bays, fixed 600 mm pitch and 4572 mm span. Objects, connections, cumulative layers and explosion follow the System library. |
| 2 / Studio cassette | Latest shared building scene, including storage, openings, niche/terrace fixes and connected-wall work. Uses the existing building controls. Does not use the System website's older 600 mm cassette. |
| 3 / B plate ribs | New independent open-ended LVL plate-rib chassis, insulation cut around actual solids, paired knee cheeks and backed deck seams. 600/900/1200 pitch, bay count, span, height, thickness and depth are study inputs. |

New inspection selector: assembly / object / connection. Object index selects the catalogue row (zero-based). For the cassette, objects are actual assembly groups and connection context is a connected wall run; no fastening certification is implied. Out-of-range indices show an explicit error and clear geometry rather than silently select something else. The original building preview is unaffected.

Panels, insulation and foundation are display filters; they never change source counts. WikiHouse source geometry has no optional insulation/foundation recipe, so those toggles do not alter it. B has no foundation design. The B panel switch includes knee cheek plates: panels-off is an inspection view, not a viable structural system. Core colours group manufacturing candidate types; these are not material-grade certification. Cumulative layers and explosion are inspection controls, distinct from the original assembly-progress animation.

## Contents and reproducibility

- `obtp/plate_ribs.py`: single B geometry/quantity source, millimetres.
- `obtp/system_comparison.py` and `components/comparison.py`: source selection, display and reports.
- `comparison_data/`: bundled original WikiHouse geometry, placements and attribution; no download or COMPAS installation required.
- `EXPORT_SYSTEM_COMPARISON.py`: creates five 3DMs, source-driven axonometrics, schedules and an offline `review-r22/review.html`. Requires `rhino3dm==8.35.0`, `numpy` and `pillow`.
- `RESEARCH_B_R01.md`: evidence, alternatives, numerical pitch screen and design holds.
- `EXPORT_STUDIO_M_PDFS.py`: unchanged three existing Studio PDF recipes; PDFs concern the existing cassette, not B.
- Repository `tools/package-gh-r22.py`: reproducible ZIP builder. Archive contains checksums.

WikiHouse display copies omit zero-area triangles in the existing reconstructed tie meshes; original asset coordinates and source files remain unchanged. The source open R-S Brep remains explicitly unresolved. Source meshes are not CNC-ready geometry. Attribution and CC BY-SA terms are in `comparison_data/WIKIHOUSE_NOTICE.md`.

## Validation and limits

Portable CPython/rhino3dm checks cover solid validity, dimensions, non-overlap at representative B limits, insulation volume, stable IDs/counts under visibility changes, unchanged cassette scene, source mesh transforms, all three selector modes and invalid input handling. All five review 3DMs are reopened and object counts reconciled. RhinoCommon component construction, actual native GH canvas wiring/slider interaction and Rhino PDF export remain host acceptance checks: not executed here.

No capacity, fastener specification, supplier compatibility, wind/water/fire performance, manual lifting mass or construction approval is claimed. B is a comparison chassis, not an insulated finished building or a replacement Studio design. End walls, doors, windows, weather layers, hold-downs and foundation are deliberately outside its bounded scope; their absence must not be described as a reduction against a complete building.

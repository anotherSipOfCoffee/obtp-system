# R14 — integrated 900 × 1200 cell system

The owner explicitly requested full integration and comparison with the previous system after selecting the simpler seam-based approach. This is an implementation release candidate, not another standalone grid study.

## Canonical model

`parameters()` now resolves the cell system by default. `legacy_parameters()` explicitly selects the preserved previous placement rules for historical regression and before/after comparison. The same `build()` serves Python/GH, browser meshes, sections, plans and Rhino exports. Studio adds presentation only.

Sauna sizes use 3 cells for the sauna, 2/3/4 for the hall, and 3 along the depth. Optional storage adds one X cell, with its three depth zones divided at 1200 and 2400. Studio sizes use 3/4/5 cells for the left room, 2 for the centre and 2 for preparation, with a 2-cell depth. These are deliberate new layouts, not equal-area substitutions for the previous S/M/L sizes.

The implemented reference convention is the outer structural frame envelope plus grid-aligned internal wall near faces, with explicit terminal deductions. It does not implement the unaccepted centre-line/finished-face alternatives explored in the research documents. Nominal bays are not finished room dimensions. Material sections and layer thicknesses remain existing provisional studies; changing the grid does not provide new engineering validation.

Ordinary wall panels divide on global 900 mm X / 1200 mm Y axes. Openings consume a whole adjoining bay envelope large enough for the retained candidate aperture and jamb zones. Window joinery follows the resolved aperture, not its old centre. Terminal assemblies absorb explicit corner deductions. No arbitrary face-junction rule is introduced.

Floor/ceiling cassette divisions repeat at 900 mm without the previous residual bay. Weather-roof and finish submembers retain their own manufacturing spacings. These are not additional planning cells or foundation nodes.

The platform has a rectangular 900 × 1200 support lattice across building and terrace with a shared origin. No edge-fit supports are inserted. Joists and deck packing are resolved to it. This intentionally increases supports in some variants. Soil, pile sizes, grillage sections, connections and cantilevers remain unengineered. Terrace finish clearances mean a 1200 mm front reference bay has 1096 mm geometric deck depth; the model and UI distinguish them.

## Comparison

`compare_cells.py` regenerates both systems from matching programme/size/storage options and records footprint, wall assemblies, physical wood parts, orientation-normalized geometric types and support counts. It does not equate geometric signatures with certified interchangeable manufactured parts. Website exports include the same comparison for every selected variant and an actual previous-model SVG plan.

The representative M results show why no universal savings claim is made: Sauna M grows from 4590 × 2190 to 5400 × 3600; Studio M changes from 7380 × 2790 to 7200 × 2400. Part-count differences must be read alongside these footprint changes. No costs, timings, weight rankings or capacity claims are inferred.

## Preserved behaviour

PDF generation stays disabled by default. Gable remains absent from website exports; flat and single-slope remain. Lithuanian remains default, existing choice controls and white model appearance remain. Studio v1 and WikiHouse assets are untouched. Supplier alternatives remain unavailable. Native Rhino/GH acceptance, engineering holds and paused wind/snow analysis remain distinct from software validation. Drive and Architecture are not updated.

## Validation scope

The new cell suite checks all 216 website configurations, true Cartesian support repetition, finite positive geometry, opening clearance, sheet-stock dimensions, unique IDs and model/drawing hashes. Representative variants also receive pairwise structural collision checks. Historical suites explicitly select `legacy_parameters()` so old dimensional contracts continue to be tested rather than silently replaced.

Rhino files are generated with the pinned rhino3dm dependency. This is portable export validation, not native Rhino execution. The GH download retains its historical R12 filename for link compatibility; its bundled source and scene version identify R14.

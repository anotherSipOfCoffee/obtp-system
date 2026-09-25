# R03 source-first workflow

Read CANONICAL_WORKFLOW.md before any geometry edit. Website and GH share this Python core. Facade selector has one option: vertical timber. R02 research notes are retained as historical rationale; R03 window placement/defaults supersede them.

# OBTP Grasshopper / Rhino R03

Local review package. Owner authorized publishing this R03 update. These are construction and layout studies, not an approved construction release.

## Start
1. Extract this entire package to a fresh writable folder.
2. In Rhino 8 ScriptEditor, run `CHECK_RHINO.py` using Python 3. It writes `diagnostics/<timestamp>/rhino-check.json`; send this report if it fails. It does not modify your active Rhino model.
3. Open a millimetre Rhino document and Grasshopper. Place a native Python 3 Script component once to load its plugin.
4. Run `CREATE_GRASSHOPPER.py` using Rhino Python 3. It creates a timestamped native `.gh` in this folder. Keep the GH definition with the `obtp` and `components` folders.
5. Choose one of six saved layouts. Roof, terrace and window controls work on saved layouts too. Custom activates the other dimension controls.
6. Preview with Panels/Cut/Explode. Export false → true creates a new review snapshot, including Rhino volume audit. It never publishes anything.

The Rhino/GH host scripts have not been executed here. Portable CPython/rhino3dm geometry checks pass. The earlier TypeHints.Select overload dependency is removed; input conversion failures clear model output.

## Inspect without running scripts
- `exports/OBTP_Sauna_All_Six_R03.3dm`: all six saved layouts, default single-slope roof, 1200 mm terrace.
- `exports/sauna-*.3dm`: individual saved layouts.
- `roof-studies/`: M models with 1200 mm terrace and each roof form.
- `previews/R02-roofs-and-interior.png`: geometry render, including cut views.
- `references/`: unchanged owner plan linework, not updated to endorse these proposals.

## New controls and geometry
- Roof: flat membrane (1:40 design fall), single slope metal (8°), gable metal (25°).
- Terrace: 600/1200 mm (default 1200), along the whole entrance side including annex. Flat/single-slope roof follows it; gable leaves it uncovered. Beam/post supports are studies.
- Window: 600/900/1200 mm wide (default 1200); rough-opening top and bottom match the door. New opening centred within the sauna room on the entrance façade.
- Facade: vertical timber only. Counter-battens and battens separate it from structural sheathing.
- Interior: horizontal sauna lining, battens and ceiling lining. Bench length/position allow for finishes; exposed short ends have slatted covers.

S/M/L still extend length at fixed nominal inside structural depth 1800 mm. Storage remains externally accessed, with shower/storage/seat zones. Additional custom controls cover room lengths/depth, door dimensions/offset, wall and partition thickness choices, benches and foundation study.

## One common model
`obtp/model.py` owns base framing and presets; `obtp/envelope.py` adds lining, facade, terrace and weather roof; `obtp/export.py` converts the same stable part recipes into .3dm, browser meshes and CSV; `obtp/rhino_adapter.py` provides preview and Rhino volume audit. No separate structural generator per preset. View clipping/explosion never changes quantities. Source System section sizes remain traceable to revision 13e7d109386b270a5eab91f9461868a99d1e48bc.

## Exact measurements and limits
All lengths in mm. L = inside main length + 390; W = inside depth + 390; A = storage extension or 0; D = terrace steps × 600. Finish projection is 84 mm outside framing; ordinary roof eave projection is another 150 mm.

Roof length X = L + A + 468. Roof back Y1 = W + 234. Roof front Y0 = -234 - D for flat/single slope, or -234 for gable. Terrace front YT = -104 - D.

Conservative area bound = X × (Y1 - min(Y0,YT)) / 1e6 when a terrace exists; otherwise X × (Y1-Y0) / 1e6. This deliberately counts the entire bounding rectangle of roof/deck projection. It is not a claim that Lithuanian legal building area equals roof projection. Enclosed finished main area and terrace area are reported separately. Annex recesses do not reduce the conservative bound.

Height = highest actual generated vertex Z above the assumed ground datum at floor underside. Includes sloped roof and standing seams. Foundation components lie below that datum. Ground levels and future build-ups remain unverified.

Maximum support spacing = max(W, terrace depth, canopy-post spacing). Main transverse bearing span remains W; post spacing is rounded geometrically to fit the length and limited to 3000 mm nominal. This is a geometric limit, not member capacity verification. Gable ridge reactions and ceiling-platform load transfer need engineering.

Hard candidate limits: area ≤50 m², height ≤5000 mm, support spacing ≤6000 mm. Invalid combinations fail generation. All exports remain blocked from production release. Dimensional checks do not guarantee SLD exemption.

Wood quantities are split into structural timber, plywood, lining wood, cladding wood and deck wood. Total includes modeled wood in those categories, excludes gray furniture/door objects, waste and unmodeled fixings. Sloped prism volume uses exact geometry, not its axis-aligned bounding box. Layer names and IDs identify each piece.

## Findings and open decisions
Read `RESEARCH_R02.md` for sources and the distinction between sourced construction principles and project-specific study dimensions.

The previous slab framing has paired touching edge joists, not intersecting solids. They remain. Wall bottom plates bear on floor skins over perimeter blocking; that arrangement is geometrically coherent but bearing/fastener/anchorage capacity is not established. No promise of a solved foundation or certified opening detail is made.

The narrower shell adaptation and small source-plan offsets remain subject to owner review. Window placement and heater relocation are candidates; final heater clearances, glazing safety and sizing, vapour/air/water control, roof edge flashing/drainage, thermal continuity and connectors remain unresolved. The level ceiling cassette plus separate weather roof also needs material-efficiency review.

## Checks
`python tests/test_authoring.py` and `python tests/test_r02.py` (requires rhino3dm). Portable checks cover the six, 108 custom cases, 108 roof/terrace/window cases, actual solid extents, invalid input rejection and valid closed .3dm round trips. `CHECK_RHINO.py` repeats native Rhino geometry/export checks on six default layouts plus three roof/terrace examples. Inspect actual GH runtime messages afterward; a geometry diagnostic PASS is not a GH canvas acceptance.

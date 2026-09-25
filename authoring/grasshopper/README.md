# OBTP Grasshopper authoring prototype R01

Six saved Sauna configurations (S/M/L × exterior storage off/on), one editable Python generator. This is a review prototype, not an approved replacement for the Studio models or a construction release.

## Open now

Open `exports/OBTP_Sauna_All_Six_R01.3dm` in Rhino 8 to inspect all six, or open an individual model. Units are millimetres. Objects have stable part IDs, material and assembly metadata. Generic objects are gray; structure uses timber/plywood colours.

## Create the editable Grasshopper definition

1. Extract the entire ZIP to a writable local folder. Keep the folder structure intact.
2. Open Rhino 8 for Windows and a millimetre document. Open Grasshopper. Place a native Python 3 Script component once to load its plugin.
3. In Rhino's ScriptEditor, open `CREATE_GRASSHOPPER.py` as Python 3 and run it.
4. The builder creates and opens a timestamped `.gh` beside this README. Keep it beside `obtp/` and `components/` when moving the package.
5. Choose a saved configuration. Turn Custom on to use the extra dimensions. Inspect Panels, Cut and Explode. For a snapshot, set Export false, then true.

The native GH builder and RhinoCommon volume audit require verification in your Rhino installation; they have NOT been executed here. The supplied .3dm files were generated and reopened with rhino3dm. If the builder reports the Python3Component.Create API is missing, update Rhino 8 to a service release providing that API. A setup error is written to `setup-error.txt`; retain it for diagnosis. No plugins beyond Rhino/Grasshopper's native Python 3 are intended.

## Parameters and architecture

`obtp/model.py` owns parameters, validation, part recipes, IDs and quantities. `obtp/rhino_adapter.py` converts recipes into Rhino Breps and audits their volume. `obtp/export.py` writes Rhino, browser mesh JSON, recipe JSON and part CSV from the same data. GH has three editable script components: Model, Preview and Export. Preview clipping/explosion never changes quantities.

Saved size changes main inside length: S 3600, M 4200, L 4800 mm; inside depth stays 1800 mm. Sauna length is 2400 mm. Storage adds a nominal 1200 mm exterior-access bay on the shower side. That bay contains shower, storage and outdoor-seat zones. Outdoor shower exists with storage off as well.

Custom controls include room depth, sauna length, entrance length and storage extension in 600 mm steps; storage on/off; wall height 2100/2700; partition depth 90/120; door width, height and offset; upper/lower bench heights and bench depth; foundation visibility. These are study controls, not a guarantee every combination is functionally or structurally acceptable. Invalid model parameters stop output.

## Measurements

Exterior structural width W = inside depth + 2 × 195 mm. Main structural length L = inside length + 2 × 195 mm. A = storage extension or zero.

- Conservative building-area bound = (L + A + 24) × (W + 24) / 1,000,000 m², counting the full annex rectangle and 12 mm exterior skins. This is an explicit geometric bound, not a legal area determination. Final cladding/overhang/site classification must be reviewed before compliance release.
- Main internal clear rectangle = inside length × inside depth / 1,000,000. A second metric subtracts the partition strip; neither is the regulatory area.
- Height above assumed grade at floor underside = 220 + 18 + wall height + 220 + 18 mm. Foundation is below this datum. Terrain and future roof build-ups remain unresolved.
- Structural support-line span = W, the transverse joist span between perimeter bearing lines. Long building dimension may exceed 6 m. This check is geometric; member sizing, roof loads and foundation design are unresolved.
- Hard candidate bounds: area ≤ 50 m², height ≤ 5000 mm, bearing-line span ≤ 6000 mm. No candidate is a permit-exemption certificate.
- Structural timber and plywood volumes sum each generated solid's dimensions / 1e9. They are reported separately and together; furniture, concrete, waste and fasteners are excluded. Part CSV includes all objects, so filter material for structural quantities.

## Review holds — do not silently fix

The candidate adapts the old 4572 mm-wide cassette shell to the source plan's nominal 1800 mm interior depth. That adaptation has not been accepted for the website. The source wall thicknesses were indicative. The candidate uses System member sections but is not an exact copy of the approved six drawings: e.g. the source M partition-door offset is about 149.813 mm; candidate uses 150 mm. Entry centring and storage dividers also need overlay approval. Original monochrome SVG plans are included unchanged in `references/`.

Openings contain geometric king/jack/header studies and gray door objects. Capacities and fasteners remain null. These are Cassette 01 studies, not a released WikiHouse opening solution. Foundations are generic support strips only. Thermal layers, waterproofing, ventilation, heater clearances, sauna bench ergonomics, door operation and fire safety need design checks. Current collision tests cover structural solids and clear apertures, not complete functional clearance validation.

Every export has website_ready=false and manufacturing_release=false. The websites and pinned production System revision have not been changed by this package. Further custom variants stay in GH until individually reviewed.

## Validation and next acceptance

Portable tests check all six configurations plus 108 custom combinations for structural collisions, clear apertures, panel sheet limits, stable identity and envelope bounds. Invalid inputs are rejected. Export tests reopen all six Rhino files, verify closed valid Breps, dimensions, millimetre units and consistent browser IDs. Run `python tests/test_authoring.py` with rhino3dm installed to repeat.

In Rhino: run the builder; switch all six and return to the first; adjust custom controls; test an invalid combination; verify no output; restore valid parameters; export after false→true; inspect rhino-audit.json. Then overlay the included approved plans and agree the shell/door deviations before integrating the six files into Studio. Native host acceptance remains pending.

API references: https://developer.rhino3d.com/guides/scripting/scripting-gh-python/ and https://discourse.mcneel.com/t/programmatically-creating-new-c-python-script-components/199692/15

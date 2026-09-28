# R27 — controlled room plans and inspectable construction stages

Extract the entire package into a fresh folder. Open a Rhino millimetre document (New → Large Objects – Millimeters), open Grasshopper, then run `CREATE_GRASSHOPPER.py` with Rhino 8 Python 3. Keep the generated timestamped `.gh` beside the supporting folders. The creator retains the R24.1 Python3Component.Create compatibility fix. Existing documents are not rescaled or overwritten.

## Two definitions

- **Main:** `CREATE_GRASSHOPPER.py` — Sauna/Studio room controls and cassette construction.
- **Research:** `CREATE_RESEARCH_GRASSHOPPER.py` — construction specimens only; no building presets, room programmes or furniture. WikiHouse remains pinned source geometry; cassette offers wall, floor, roof, rough opening, corner and floor-wall interface; B retains its experimental plate-rib assemblies/interfaces. B opening framing is not implemented.

## Main canvas sequence

| Group | Responsibility / useful outputs |
|---|---|
| 01 Preset, programme and relationships | Six saved Sauna presets, Custom Sauna, six saved Studio presets, Custom Studio. Choose base S/M/L and storage; custom length changes are offsets from it. Reports show effective dimensions. |
| 02 Plan | Room bounds, layout order, relationships, opening marks and validity. No complete model generated. |
| 03 Structural arrangement | Wall runs, opening hosts, geometric contacts, levels, platform bounds and foundation rhythm; capacity remains unknown. |
| 04a / 04b / 04c | Independent floor, roof and wall/door-window branches. Each manufactures its own constituents. |
| 05 Frame | Checks that all branches originate from the same validated plan, then combines them. |
| 06–10 | Surfaces, terrace, weather roof, foundation and insulation. Each adds its physical parts. Intermediate previews show the additions. |
| 11 Complete | Final IDs, dimensions, drawing geometry and quantities. |
| 12 Assembly | Slider 0–100, current step and step list; connected walls laid flat near their erection lines, then raised. Cladding last. |
| 13 Final preview | Structure + panels / building without façade boards / complete; stable type colours and exact assembly-ID isolation. |
| Optional lower analysis group | Existing analysis-preparation controls retained, with unresolved solver/capacity status. |
| 14 Diagnostics and exports | Inspect rooms, openings, parts and checks. Exports always use the complete model. Existing PDF-disabled GH toggle preserved. |

Every construction stage has a separate preview toggle and a Details output for a Panel. These are inspection controls, not independently editable structural sizing. Authoring controls live in group 01 to keep one source of truth. Engineering member sizes and fastening are not automatically optimized or certified. The real recipes are in `obtp/model.py`, `envelope.py`, `plan_construction.py` and shared modules; `plan_pipeline.py` composes them. Short canvas Python scripts call these modules rather than hiding a prebuilt Rhino model.

## Custom controls and limits

Select Custom Sauna or Custom Studio, choose the base preset, then enable **Use custom overrides**. Length sliders show **−1 / 0 / +1 cells relative to the selected base**, where one cell is 900 mm. Turning overrides off restores effective preset room dimensions/programme; the visible sliders intentionally retain their offsets for reuse. The report states the effective result. Roof/window/height/foundation controls remain independent and are not reset.

| Input | Supported boundary | Reason |
|---|---|---|
| Plan source | Room controls only | No Rhino-drawn-plan import in this release |
| Topology | Single-level, axis-aligned contiguous rectangular strip | Implemented domain; no holes, curves, arbitrary angles or branching plan shapes |
| Sauna room length | Base ±1 cell; minimum 3 cells (2700 mm) | Existing sauna/equipment and opening recipes |
| Entrance length | Base ±1 cell; minimum 2 cells (1800 mm) | Existing entrance/opening recipes |
| Outdoor length | Base ±1 cell; minimum 1 cell (900 mm) | Existing mixed outdoor-zone detail |
| Sauna width | Base width, currently 2400 mm | User-approved architectural bound |
| Sauna room selection/order | Existing valid indoor combinations, reversed orders, terminal outdoor and disconnected indoor entries | Outdoor-only unsupported; invalid relationships/arrangements rejected |
| Studio work length | Base ±1 cell, clipped to 3–6 cells | Bounded existing architectural range |
| Studio centre / preparation | 2–3 cells | Base + at most one cell, with existing minimum |
| Studio width/order | 2400 mm; work → heated centre → preparation | Existing coordinated Studio topology |
| Wall height | 2100 / 2700 mm | Existing recipe choices, not structural approval |
| Window frame width | 580 / 880 / 1180 mm | Existing candidate products; 10 mm edge-gap assumption |
| Window position | Existing or adjacent supported bay | Invalid shifts reject explicitly; openings must retain framing space |
| Terrace | Existing front rhythm and programme-dependent return | No arbitrary terrace shape control |

Typed values obey the same rules. Negative length offsets below a minimum are rejected, never silently clamped. Room inclusion, window fitting and existing geometry guards can further limit combinations. These are architectural/manufacturing geometry limits, not permits or engineered span limits.

## What is generative, and what is not?

The resolved room plan drives dimensions and the shared construction stages. The model generates physical parts from recipes; it does not modify an imported finished building. Programme-specific wall and equipment rules still exist. This is a bounded room-control generator, not a solver for arbitrary floor plans or an automatic structural engineer. Valid shape does not establish capacity, fastening, weatherproofing, thermal performance, safe handling or supplier acceptance.

## Troubleshooting

Find the first stage with an error and read its report. Invalid input clears downstream output; stale or mixed-plan branches are rejected. To restore full display: assembly 100, Complete scope, blank assembly filter, turn off intermediate previews. To inspect one stage, turn on only its preview. Direct manual JSON editing fails hash validation; use room controls.

Intermediate mirrored geometry now follows the final model coordinate system. Floor levels come from the scene, not a fixed preview constant. Saved presets retain R26 geometry/quantities; no part reduction is claimed. Cladding remains visible in Complete, excluded only by the established primary-count rule and retained in a separate schedule. Display filters do not change source quantities or exports. Connected wall groups are not certified lifting units.

## Validation and review

`review-r27/review.html` contains canonical plans and axonometrics for Sauna M, Studio M and bounded custom variants. `before-after.csv` records all 24 saved preset/roof comparisons. `studio-m-storage.3dm` is a portable model export. `timings.json` records local Python construction timings; it is not native GH performance evidence.

Run `python -m unittest discover -s authoring/grasshopper/tests` from the repository root with rhino3dm installed. Run `python authoring/grasshopper/REVIEW_R27.py` to regenerate the local review. `tools/package-gh.py` bundles required modules and checks archive integrity.

Native Rhino/GH execution, final canvas appearance, viewport responsiveness, save/reopen and interactive exports remain unverified in the cloud environment. No prebuilt natively tested `.gh` is claimed. No websites, Drive, Studio/Architecture repositories or deployment are changed.

# SSP-R02 — local review package, not published

Owner direction: 26 September 2026. Reduce the draft to core simplified-project documents; GH must create Rhino layouts and print those same layouts as PDF. Do not update the website or GitHub in this review step.

## Included
Nine A3 landscape sheets: title; document list and basis; explanatory statement and model metrics; structural/services description; plan; two sections; four elevations over two sheets. No supplier catalogue, numerical-analysis appendix, window schedule, optional detail sheets or quantities. Site plan is REQUIRED BUT MISSING, not silently waived: no actual plot has been supplied. Regulatory classification, final STR edition review, engineering and signatures are unresolved. This is an unsigned project draft, not a completed SSP.

## Run in Rhino 8 / Grasshopper
1. Unzip the full package. Keep `obtp`, `components` and other folders beside `CREATE_GRASSHOPPER.py`.
2. In Rhino 8 Python 3, with Grasshopper open, run `CREATE_GRASSHOPPER.py`. It builds a new editable GH definition using the existing Cassette model. No paid plugin added.
3. Rhino document model units AND layout units must be millimetres. The export refuses other units instead of scaling a user's document.
4. Choose Studio or Sauna and parameters in GH. Set **Export model + SSP layouts/PDF** false, then true.
5. The current detailed model generates the 2D intersections/projections and real Rhino LinearDimension objects in model space, then nine A3 RhinoPageViews with locked scaled details. Layout text/title blocks are editable page-space objects.
6. Rhino `FilePdf` prints exactly those layouts to `<configuration>-SSP-R02.pdf` under a new `rhino-exports` snapshot folder. No alternative PDF generator is called on this path. Failure is reported, not replaced by a proof PDF.
7. **Save the active Rhino document as a .3dm to retain the layouts and model-space drawing geometry.** The separately exported geometry-only .3dm is still geometry-only; do not confuse the two files.
8. After adjusting Rhino layouts, run `PRINT_SSP_LAYOUTS.py` to reprint the latest nine pages. This reads the latest generated layout names from the Rhino document. A new GH export makes a new snapshot and retains earlier/manual layout edits.

The editable 3D model remains available through GH preview and the geometry-only export; the layouts show a frozen, hash-linked 2D derivation at the time of export. Changing a slider does not silently mutate a previously issued drawing. Export again for a new coordinated snapshot.

## Source and checks
`ssp_sheets.py` is the common sheet recipe; `native_drawings.py` creates actual Rhino layouts and prints them. `ssp_preview.py` produces an OFFLINE PROOF for review where Rhino cannot run. The supplied sample PDF is explicitly labelled as this proof, not as a Rhino-printed result.

Plan and sections use 1:10 if they fit, otherwise 1:25; unsupported larger drawings fail rather than silently using fit-to-page. Elevations use 1:50, or explicitly labelled 1:100 for taller gable variants. Detail.SetScale uses model denominator : paper 1. Per-detail layer visibility isolates drawing sets and does not globally hide user objects. Existing details hide new export layers. Export names include microseconds to preserve snapshots.

Native Rhino 8 / Grasshopper execution is NOT tested in this Linux environment. PDF capture, view centring, text metrics, display order and print line weights must be accepted in Rhino. No native .gh, Rhino-printed PDF or layout-containing .3dm is falsely claimed as executed here. The builder and shared Python sources are provided.

Elevation projection uses depth-sorted opaque part projections, not Rhino Make2D. Validate occlusion for complex future geometry. Sections are exact intersections of the current box/prism model, not engineering validation. Material hatches are conventions, not verified product build-ups. Existing broader website PDFs remain unchanged.

Primary API references checked 2026-09-26:
- https://developer.rhino3d.com/api/rhinocommon/rhino.geometry.detailview/setscale
- https://developer.rhino3d.com/api/rhinocommon/rhino.docobjects.layer/setperviewportvisible
- https://developer.rhino3d.com/api/rhinocommon/rhino.fileio.filepdf/create?version=8.x
- https://developer.rhino3d.com/api/rhinocommon/rhino.fileio.filepdf/addpage
- https://developer.rhino3d.com/api/rhinocommon/rhino.fileio.filepdf/write
- https://mcneel.github.io/rhinocommon-api-docs/api/RhinoCommon/html/T_Rhino_Display_ViewCaptureSettings.htm

Legal source: STR 1.04.04:2017 section 29 structure, as reproduced in the VTPSI 2017-12-14 explanation and official indexed consolidated text. Final current consolidated edition must be checked by the project designer before formal issue; this draft claims no full STR conformity.

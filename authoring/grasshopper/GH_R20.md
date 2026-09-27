# GH R20 — connected wall erection

GH and PDFs only. Studio remains pinned to R19; no site files or deployment are changed.

- Assembly progress is one 0–100% slider. Its status names the current step. The changing number of walls is resolved automatically for each building; 0 is empty and 100 is complete.
- Adjacent collinear wall cassettes, opening frames and their infill are one display group. Glass/door products still install later. Canonical part and assembly IDs, dimensions, quantities and manufacturing identities are unchanged.
- One wall at a time is shown flat beside its wall line, rotated 45 degrees, then upright. A fixed bottom-edge pivot is retained. Temporary supports at the floor datum are assumed for the flat work surface; supports, lifting, bracing and connections have not been engineered. Whole walls may conflict with the preference for manual small-crew erection and require equipment.
- Core-frame preview continues to colour canonical unique parts. Cladding remains the last stage.
- Default Studio M only has three supplied PDFs: Part Schedule (unchanged scope), Parts Layout (the detached cassette arrangement), and Assembly (connected wall runs and rotation stages).
- Reproduce PDFs with `python EXPORT_STUDIO_M_PDFS.py destination` (ReportLab required). No website build is involved. The GH model/drawing export toggle remains separate from this PDF utility.
- Run `CREATE_GRASSHOPPER.py` in Rhino 8 Python 3 with Grasshopper open to make a new R20 document. Existing GH documents are not overwritten. Model geometry remains R19; R20 is a display/documentation revision.

Portable validation covers fixed pivots, rigid distances, connected multi-opening wall runs, cumulative stages, stable part colours and unchanged canonical data. Native Rhino/GH execution and actual lifting feasibility remain unverified.

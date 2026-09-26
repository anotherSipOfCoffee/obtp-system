# Current OBTP System guidance — R15, 26 September 2026

Latest explicit user instructions take precedence. This revision is **review only**: continue System PR #20 and Studio PR #37, do not merge or publish. Leave Drive and Architecture unchanged.

## Authority and architecture
- `authoring/grasshopper/obtp` is the canonical Python model shared by Grasshopper, drawings, quantities and web exports. Studio owns UI and consumes a pinned System commit; never duplicate geometry in JavaScript.
- Keep the 900 mm X × 1200 mm Y planning grid (the same 1200 × 900 cell), architectural room relationships, Studio's heated sliding-glass centre and Sauna's external shower/storage/seat arrangement.
- Revised Sauna and Studio structural width is 2400 mm. Physical members may span multiple cells. Support rhythm is normally 1800 × 1200, with explicit terminal bays; it is not engineered capacity.
- Facade remains visible. Only facade finish boards (including raised roof facade) are excluded from primary part counts. Retain their separate schedule. Battens, edge trims, insulation, equipment representations and every other modelled category remain primary.
- Manufacturing identity includes material, dimensions, shape, machining, handing and connection requirements. Unknowns remain unknown. Report provisional candidate classes and geometric lower bounds, never verified manufacturing savings. Assembly grouping does not reduce constituent diversity.
- Ordinary wall bays retain two plates, two studs and one panel. Opening side plates match top/bottom; jack studs bear on bottom plates and retain 45 mm lintel bearing. Keep corner/niche terminal exceptions explicit; the local-seam trial increased diversity. See review-r15/OPENINGS.md.
- Both complete terraces use X-directed boards, max 1800 mm, supported butt joints. Interior lining remains continuous: a 900 mm cut experiment added excessive pieces/joints and was rejected.

## Reproducibility and checks
- Original baseline: `1ad71826acfcc7d6d5df9a06167c5fcfea20b516`.
- First integrated cell baseline: `a11e613ac923fd5de6a3d3f1368e6c6eebc57745`.
- `compare_manufacturing.py` reads these immutable Git snapshots into temporary folders. Do not maintain copies as parallel production pipelines.
- After geometry changes: `python authoring/grasshopper/compare_manufacturing.py authoring/grasshopper/review-r15 --full-catalogue`; run the Python suite; then `export_web.py DEST --revision COMMIT`. Export refuses stale comparisons.
- PDF generation stays disabled. Gable is absent from website and new GH controls. GH offers a complete normal preview, without object-type switches. Lithuanian flat-roof label: `Plokščias`.
- Retain geometry/solid/clash, source-hash, export-cache, native acceptance and important browser behaviour checks. Native Rhino/GH acceptance is separate from portable rhino3dm checks.
- Customer-facing brand is `studio 9120`; preserve existing UI and Lithuanian default. Main opens first; PDFs remain disabled.

## Engineering, sources and scope
- No invented capacities, fastening schedules, supplier compatibility, prices or permit exemption. All connections remain unverified; material grades, machining, wet-area detailing, glazing, heater clearances, roof uplift, soil and bracing require engineering.
- No certified manual-lift mass: wall/roof cassettes are geometry groups, not approved factory lifting units. Use loose-part/small-subassembly erection until weights and handling are verified.
- Preserve supplier/source attribution and licences; proprietary parts must not be stretched. Preserve pinned WikiHouse source geometry and CC BY-SA 4.0 obligations, Studio v1 reference and separate legacy product modes.
- No supplier outreach. Preserve ordinary Git history and existing work. GitHub remote writes use the connector. No Drive synchronization.

Historical release/research documents are evidence, not current competing instructions. Read them only for a relevant detail; this file consolidates current decisions.

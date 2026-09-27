# R18 platform, assembly and finish revision

Review revision; not merged or published. Canonical source remains System; Studio consumes its exact commit.

## Implemented

- Terrace joists retain 45 mm width and extend to the foundation rails: 210 mm depth. Removes separate deck packing blocks. Normal axes are 450 mm, coordinated with the 900 mm floor bays. End supports remain exceptions.
- Added counted terrace fascia, removable slatted bench fronts and second ends, plus cladding to niche heads, jambs and soffits. The finished niche soffit matches door height.
- Outdoor bench recess is 300 mm deep. In the 2400 mm Sauna, the storage divider moves 117 mm toward the rear, increasing storage by about 0.081 m² before finish deductions.
- Assembly slider: 0 empty, 1 foundation, 2/3 floor prepare/place, 4/5 wall prepare/erect, 6/7 roof prepare/place, 8/9 opening units flat/installed, 10 interior, 11 decking, 12 cladding. These are display poses, not quantity changes or an approved lifting plan.
- Default Studio M schedule: structural timber/concrete study parts, plywood and insulation, with individually scaled axonometric thumbnails. Facade boards remain separate. All other parts remain in the complete audit.
- GH source and creation script are tracked in GitHub. Preview caches only the current model’s Rhino solids; source hash invalidates the cache. Native speed improvement remains unmeasured.
- CI discovers all Python tests. Removed the obsolete duplicate Studio checkout from legacy cassette validation; current Studio integration is verified against its actual pin. Pages skips the legacy wait only when the API confirms workflow publishing.

## Measured effect versus previous revision

| Default M, no storage, closed Studio | Types before / after | Pieces before / after | Wood m³ before / after |
|---|---:|---:|---:|
| sauna | 121 / 130 | 1063 / 1057 | 6.395 / 6.518 |
| studio | 137 / 137 | 1354 / 1305 | 8.720 / 8.894 |

Catalogue: original 459, first cells 381, previous 319, current 329 candidate types. Current reduction from original: 28.3%; the 75% target is not met. Relative to the previous revision, diversity increases 3.1%. Newly completed details explain part of this increase; no finishes are hidden to improve the score. See manufacturing-comparison.md and its machine-readable archive for per-building, same-footprint, cladding and assembly comparisons.

## Validation and engineering holds

58 Python tests passed locally (57 core/geometry/native portable export tests plus the scoped PDF/web export test). Covers 106 accepted custom geometry cases and two intentional rejections; wood-category clash checks pass across the supported preset/roof matrix. PDF pages rendered and visually inspected. Ground-pose tests check flat opening units, identity preservation, final completeness and scene immutability.

RhinoCommon cache and native GH acceptance still require a native Rhino session; portable rhino3dm tests are not a substitute. Joist depth/spacing, stock availability, fastening, fascia end fixing, moisture drainage, niche reveal substrates, lifting masses, temporary bracing and handling need engineering. The laydown view is an explanatory sequence; large units may conflict with the no-lifting-equipment preference. Furniture remains a dimensional study. No capacities or crew lift limits are claimed.

## Next useful optimization

Resolve the manufacturing and connection details for opening/terminal members and bench covers before merging candidate identities. Terrace removal of packing reduces installation pieces, while new finishes increase diversity. Avoid widening joists or splitting finish boards further merely to regularize the drawing; both can add timber or joints without reducing genuine types.

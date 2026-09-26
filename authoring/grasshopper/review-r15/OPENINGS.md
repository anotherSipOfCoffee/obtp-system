# Opening and terminal optimization

Comparison baseline: System `20e7d87dddab93ef453f0ef2c491078ce9b376c5`. Same footprint, opening positions, heights, sheathing and counting rules; all layers remain. Primary counts exclude facade finish boards only.

| Scope | Before | After | Reduction |
|---|---:|---:|---:|
| Sauna catalogue | 251 | 249 | 0.8% |
| Studio catalogue | 228 | 226 | 0.9% |
| Shared catalogue union | 361 | 358 | 0.8% |
| Default M Sauna complete model | 118 | 117 | 0.8% |
| Default M Studio complete model | 128 | 126 | 1.6% |
| Default M Sauna wall timber/plywood only | 23 | 22 | 4.3% |
| Default M Studio wall timber/plywood only | 24 | 21 | 12.5% |

Structural-only rows are a diagnostic subset, not the primary target metric. Studio's timber saving is partly offset by an extra insulation-cut type. Physical primary pieces remain 954 Sauna and 1221 Studio. Assembly counts stay 42/63 and 65/91 (types/geometric installed groups).

## Implemented detail
Side infill now has matching full-width bottom and top plates. One ordinary-length outer stud remains on each side. Jack studs start on those bottom plates and continue to the same lintel underside. Lintel dimensions and 45 mm end bearing remain. The centre top plate uses the actual opening width, allowing 900/1200 mm cuts to reuse ordinary bay plates. Two redundant inner studs are replaced by two side top plates; this is a geometry change, not an identity rename. Ordinary bays, panel cuts, openings and building footprints are unchanged.

Default wood volume changes 6.2587 → 6.1718 m³ Sauna and 8.5901 → 8.4490 m³ Studio. Cavities are recomputed from actual framing and filled by the same insulation generator. No strength or thermal performance is claimed.

## Terminal trial rejected
A temporary trial started repeated bays at each wall-run origin and favoured complete-cell opening envelopes, leaving a single terminal remainder. For six flat-roof presets at the 1180 window setting, Sauna's catalogue increased 185 → 193 types; Studio remained 159. It shifted openings and introduced other remainder lengths. The trial was not adopted.

705 mm corner terminals (900 minus the 195 mm return wall) and Studio's 588 mm niche terminals remain explicit exceptions. A nominal 900 member carried through the corner would overlap or require a different machined connection. That would not honestly reuse the same manufactured part.

## Validation and limits
45 Python tests pass, including the complete 216-selection catalogue, structural clashes, opening clearance and direct bearing at every tested jack. Ordinary and terminal solid bays retain five pieces and three candidate types. All supported variants were recounted against the pinned prior revision. The diagram opening-detail.svg shows actual before/after framing with sheathing omitted for inspection. Native Rhino/GH, joint fastening, plate compression, header capacity and bracing remain engineering holds.

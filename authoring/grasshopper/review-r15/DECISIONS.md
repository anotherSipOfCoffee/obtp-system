# R15 review decisions and limits

## Result
The requested 75% reduction is not achieved. On the full 216-selection catalogue, provisional non-cladding manufacturing candidates are 459 original, 381 first cells, 360 revised. Sauna union: 296 → 251 → 251. Studio union: 246 → 226 → 227. The combined catalogue is a union, not a sum.

Original → revised: Sauna 15.2%, Studio 7.7%, combined 21.6%. First cells → revised: Sauna 0.0%, Studio −0.4%, combined 5.5%. At the first cell footprint, revised construction gives 379 combined candidates: only 0.5% improvement from 381. Narrowing Sauna accounts for the remaining reduction to 360 (5.0% from the same-footprint revision). These are not verified manufactured-part reductions; missing manufacturing inputs prevent such a claim.

Default M/no-storage/flat/window1180/timber/closed Studio: Sauna 130 → 118 → 118 types; Studio 144 → 125 → 127. Revised versus original is 9.2% and 11.8%, respectively. Exact pieces, assembly groups, dimensions, areas, wood volumes and cladding-exclusion effects are in the audit. Roof/window/foundation choices remain; the target was not approached by deleting options or layers.

## Selected changes
- Shared 2400 mm structural width; grid remains X900 × Y1200. Sauna has 2010 mm structural internal depth / 1938 mm after main side finishes. Sauna/hall adjacency, two bench levels and exterior shower remain. External-storage versions retain shower, storage and rear seat; the door now explicitly stays in the narrowed storage room. Heater and clearances still need review.
- Standard framing infill replaces full-width solid king blocks. Two repeated studs and a bottom plate retain the opening envelope; insulation fills the cavity. No fastening design is implied.
- 1800 × 1200 foundation support rhythm, explicit 900 mm terminal bays and beam ends on bearings. Cell nodes are no longer all piles. Floor/roof joists and support dimensions remain provisional.
- Terrace boards run X across front and returns. Max cut 1800 mm; joints are seated on joists. Extra pieces from these cuts are reported. Foundation packing follows actual deck joists rather than a duplicate coordinate formula.
- Normal full-model GH preview; remove object-type switches and one-option terrace/facade/system controls. PDF generation disabled in GH export as well as website; no gable choice in new GH definition.
- studio 9120 branding in shell, customer copy and runtime titles. Existing UI, Lithuanian default, Plokščias, Main-first navigation and WikiHouse reference preserved.
- Counts, drawings and website share one canonical scene. Website export checks the exact revised geometry hash against the frozen-baseline audit. Old wood-only comparison redirects to the same audit. Original/cell sources come from immutable Git snapshots, not duplicated production code.

## Rejected trial
Splitting all interior boards into 900 mm lengths with closer batten support reduced the twelve-base-selection catalogue union from 273 to 258 candidates, but increased default Sauna pieces 956 → 1378 and Studio 1217 → 1620. It added finish joints and supporting parts. Reverted: this was not a clean route to the target. No trial geometry is in the production model.

## Remaining diversity
Default revised Sauna: timber 34 candidate types, lining/battens 23, object representations 22, plywood 13, retained cladding battens/trim 10, insulation 10, deck 3, plus glass/roof membrane/foundation. Studio: timber 33, object representations 27, lining 21, retained cladding battens/trim 14, plywood 14, insulation 9, deck 4, glass 3, roof membrane and foundation. Opening variants, corner/terminal deductions, sloped roof bearings, lining remainders, insulation cavities and placeholder equipment dominate. The storage variants retain additional legitimate detail types. Sharing widths helps the catalogue more than each individual building.

75% would require roughly 115 candidates across the whole catalogue, versus 360 now. Even a single default building has 118–127. Reaching that level needs a coordinated engineered kit of sections, openings, joints and finishes, with verified supplier constituent BOMs; grouping current pieces as cassettes or assuming unknown machining identical would only disguise the problem.

## Assembly and small-crew scope
Assembly figures are distinct geometric group recipes and groups installed, computed from constituents and relative placement. They do not certify site work packages or factory lifting units. Repeated floor/roof strips and solid wall frames are potential jig-built subassemblies, but no mass or manual-lift limit has been verified. Use loose members/small subassemblies until weights and handling are established. Avoid claiming a complete floor/roof cassette can be lifted by a small crew without equipment.

## Engineering holds
No capacities or fastening quantities were assigned. Review foundations/soil/settlement, increased bearing intervals, beam joints, roof cantilevers/uplift, bracing, opening headers, insulation continuity, vapour/air/water layers, weathering, glazing, heater/fire clearance and ventilation. Native Rhino/GH acceptance remains pending. The conservative dimensional screen does not certify permit exemption.

## Reproduce
1. Full Git checkout of this System revision (both baseline commits must be available).
2. `python authoring/grasshopper/compare_manufacturing.py authoring/grasshopper/review-r15 --full-catalogue`
3. `python authoring/grasshopper/render_review.py authoring/grasshopper/review-r15`
4. `python -m unittest discover -s authoring/grasshopper/tests`
5. `python authoring/grasshopper/export_web.py DEST --revision EXACT_SYSTEM_COMMIT`
6. Pin that commit in Studio, prepare exports and run its non-deploying browser workflow.

No Drive/Architecture changes, merge or publication are authorized in this revision.

Finished-area comparison normalizes the original Sauna metric (which was before lining) to the same finish deductions as the cell models. This affects only the reported space comparison, not part counts or geometry.

Final support correction: the inherited cell conversion removed Studio firewood-niche joists. Restore two 2400 mm joists and six bearing packing pieces. Default Studio primary pieces become 1225; unique candidate types remain 127 and the catalogue union remains 360. A support-specific test and all 24 representative structural clash cases pass.

Identity normalization treats equal integer/decimal dimensions identically and is covered by the cross-category identity regression. Recounting all three snapshots removes one duplicate Studio candidate: final combined union 360, Studio union 227, default Studio 127. This is a counting correction applied to every baseline, not a design saving.

# R15 review decisions and limits

## Result
The 75% target is not achieved. Full-catalogue provisional types are 459 original → 381 first cells → 358 current. Sauna: 296 → 251 → 249 (15.9% from original). Studio: 246 → 226 → 226 (8.1%). Combined reduction: 22.0% from original, 6.0% from first cells.

At the first-cell footprint, current construction gives 377 combined types (1.0% below 381). Narrowing Sauna gives the further reduction to 358. The opening-only comparison against commit `20e7d87dddab93ef453f0ef2c491078ce9b376c5` holds footprints, openings and counting rules fixed: 361 → 358, or 0.8%.

Default M complete models: Sauna 130 → 118 → 117 types; Studio 144 → 125 → 126. Default current pieces: 954 and 1221. The opening-only change leaves these piece totals unchanged. See manufacturing-comparison.md and OPENINGS.md for the explicit prior-revision comparison and retained exceptions.

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
The ordinary 2100 mm wall bay already uses five pieces and three types. Across 900/1200 mm widths it uses five types. Ordinary floor and roof strips share three types. Openings, terminals, roof bearings, lining remainders, insulation cavities and product representations cause the remaining variation.

The new opening recipe reuses matching side plates and a standard 900/1200 top plate where the opening width matches. Direct lintel bearing onto jack studs remains. Terminals are retained after a local-joint trial increased Sauna's six-preset union from 185 to 193 and left Studio at 159. Do not disguise corner machining as interchangeable stock.

75% would require roughly 115 catalogue candidates versus 358 now. Reaching it needs a coordinated engineered kit and verified supplier constituent BOMs; grouping current pieces as cassettes does not achieve it.

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

Final geometry retains Studio niche joists and their six packing pieces. Terrace return joists continue through the front deck; boards meet with the same 5 mm gap at the corner. Default primary pieces are 954 Sauna and 1221 Studio. Equal integer/decimal dimensions use the same identity in every baseline. These corrections are included in all final counts.

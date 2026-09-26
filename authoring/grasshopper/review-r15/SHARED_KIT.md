# R16 shared-cut implementation and comparison

The 75% target is **not achieved**. The adopted shared family reduces the combined catalogue from 459 original candidates to 319 (30.5%). These are provisional manufacturing candidates, not certified interchangeable products: machining, connection schedules and material grades still require engineering. The same identity method and facade-board exclusion apply throughout. No other category is excluded.

## Complete 216-selection catalogue

| Version | Sauna types | Studio types | Combined types |
|---|---:|---:|---:|
| Original | 296 | 246 | 459 |
| First integrated cells | 251 | 226 | 381 |
| Previous opening revision | 249 | 226 | 358 |
| Previous revision with geometry repairs only | 251 | 233 | 370 |
| Revised at first-cell footprints | 231 | 216 | 340 |
| Revised adopted footprints | 227 | 216 | 319 |

Original-to-revised reductions: Sauna **23.3%**, Studio **12.2%**, combined **30.5%**. First cells to revised: **9.6%, 4.4%, 16.3%**. Previous opening revision to revised: **8.8%, 4.4%, 10.9%**.

The repairs-only control isolates the actual shared-cut change at unchanged footprints: **370 → 319, 13.8%**. Geometry repairs increased diversity from 358 to 370 and are not credited as optimization. At first-cell footprints, 381 → 340 is a **10.8%** construction-system reduction; Sauna resizing then contributes 340 → 319 (**6.2%**). Percentages are sequential, not additive.

## Typical complete buildings: M, no storage, flat roof, window 1180

| Version | Sauna types / pieces | Studio types / pieces |
|---|---:|---:|
| Original | 130 / 935 | 144 / 1387 |
| First cells | 118 / 1023 | 125 / 1156 |
| Previous opening revision | 117 / 954 | 126 / 1221 |
| Geometry repairs only | 118 / 954 | 133 / 1217 |
| Revised | 121 / 1063 | 137 / 1354 |

**Catalogue diversity falls, but diversity in each default building rises against the previous revision.** Shared cuts add 109 Sauna pieces and 137 Studio pieces against the repairs-only control, and add three/four types respectively. The benefit is reuse across different orders, at the cost of more joints, cuts and site handling. This is not a universal improvement in every metric.

Default assembly types / installed geometric groups are Sauna **42 / 63**, Studio **67 / 91**. Across the catalogue the unions are **140 / 140 / 258** (Sauna / Studio / combined). One of every catalogue selection would contain **85,080 / 202,472 / 287,552** primary pieces and **5,100 / 13,224 / 18,324** installed groups. These sums are not quantities for one building and groups are not certified lifting units.

Facade boards remain visible and separately scheduled: default Sauna **404**, Studio **558** pieces. Excluding facade boards removes **40 / 60 / 45** unique types from original / cells / revised Sauna, and **57 / 52 / 53** from Studio. This accounting effect contributes nothing to the design-reduction target. The six fewer Studio facade pieces versus the prior revision result from removing an overlap, not omitting a layer.

## Adopted implementation

- Keep the already-simple standard wall bay: two plates, two studs, one panel, three types. Retain matching opening-side plates and direct jack bearing from R15.
- Preserve plans, openings and 900 × 1200 planning cells. Both structural widths remain 2400 mm; Sauna is leaner than the 3600 mm first-cell proposal.
- Cut selected long interior finish runs into shared 900/1800 extensions and recurring terminal lengths, retaining already-common shorter lengths. Place actual full-width battens behind new joints. The report shows model-derived cuts.
- Share supported 1800 mm facade-batten cuts and 900 mm roof-bearing-rail cuts. Add actual studs at rail splices. Do not infer a fastening schedule from geometric support.
- Keep terrace boards in one X direction through returns, with supported joints. Foundation members are 145 mm wide in this revision to provide geometric deck seats; engineering capacity remains unverified.
- Repair inherited clashes: deck joists against edge trim, niche facade overlap, ceiling against slider heads, and Studio headers against glazing. Headers now lie in the roof depth and court joists terminate clear of them; engineered hangers/connections are still required.

Finished areas remain unchanged from the previous revision: Sauna **9.232632 m²**, Studio **12.101688 m²**. Shared cuts alone add approximately **0.45% / 0.59%** modelled wood volume. Including the wider foundation and geometry repairs, the increases are about **3.6% / 3.2%**. Interior butt joints become more visible; the overall architecture is retained.

## Measured alternatives rejected

- Door-aligned grids: the same-footprint twelve-preset reference had 271 shared types; fixed 90 mm jambs on the existing/900 pitch produced 279, 1080 pitch 311, and 1200 pitch 301. Some wider jamb choices created invalid short terminals.
- Local terminal re-panelization: Sauna six-preset union rose 185 → 193, Studio stayed 159.
- Vertical lining with cross-battens: six-preset union rose 271 → 305. A rectangular-region variant reached 268 but added thousands of pieces across those selections and introduced clearance/detail problems.
- Cutting every lining run at 900 mm reached 302 full-catalogue types, but required roughly 500 additional pieces per default building; rejected.
- A finished-room grid using 1800 mm clear width and adjusted building lengths produced 370 types in a six-preset trial versus 271 in its reference, creating new floor/roof and terminal remainders. Rejected.

These exploratory trials are not alternate production pipelines. Exact adopted geometry and immutable historical revisions are reproducible through compare_manufacturing.py.

## Remaining limits and engineering

Remaining variants come from opening/terminal framing, lining remainders, roof/foundation bearings, sheet and insulation cavities, and represented equipment/glazing. Reaching 75% would require at most about 115 combined candidates. Renaming, assembling or hiding the remaining 319 candidates cannot achieve that. More radical product simplification could change this, but tested grid changes did not.

The Thermory primary sauna-panel guide specifies battens at least 20 mm thick and 45 mm wide, recommends 400 mm spacing (600 mm maximum), and requires the orientation to suit the lining. This supports the geometric batten check only; it does not establish supplier compatibility or complete moisture detailing: https://thermory.com/wp-content/uploads/2023/01/Thermory_Installation_Guide_Sauna-wall-panels_A4_0123_ENG.pdf

Sheet formats and weights are product-specific, not universally interchangeable: https://www.wisaplywood.com/specifying-wisa/sizes-thicknesses-and-weights/

Unresolved: foundation/soil capacity, new rail and lining joints, header/hanger connections, bracing/uplift, fastening, air/vapour/weather layers, glazing, heater/fire clearances and ventilation. No capacities or supplier approval are invented. Continue loose-part or small-subassembly erection; complete cassette masses and manual handling are not certified. Native Rhino/Grasshopper acceptance remains pending.

## Reproduce

Run the full-catalogue comparison, render_review.py, and the Python unittest suite, then export_web.py with the exact source revision. Studio pins that revision and generates browser/Rhino outputs through its non-deploying review workflow. Source hashes reject stale comparisons. See manufacturing-comparison.md for all metrics and immutable revision IDs. Do not merge or publish; Drive and Architecture remain unchanged.

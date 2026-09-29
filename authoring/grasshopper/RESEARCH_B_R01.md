# B — repeated plate ribs with insulation infill

Research and implemented geometry, 27 September 2026. This B is **not** the R21 600/1200 wall-kit option that happened to use the same letter. It is an independent structural concept preview, not a proposal to change Studio's plan.

## Decision

Implement a segmented, repeated LVL plate-rib chassis as the third comparison system. Keep the pinned WikiHouse library and use Studio's current canonical cassette as the second system. Keep all three coordinate/quantity sources distinct and identified; do not stretch imported WikiHouse assets or claim equal building scopes.

A rib contains one floor member, two uprights, one roof member and four rectangular plywood cheek plates at its knees. Longitudinal plywood skins and floor/roof sheets are represented with backing at transverse sheet seams. Insulation occupies the remaining geometric cavities; it does not replace structural members. This is an inspectable assembly and quantity model, not a structural design or CNC release.

## What the primary sources establish

1. **COMPAS Wood** supplies computational workflows for plate elements, their contacts, joinery and insertion information. Its Brep workflow and insertion-direction examples are useful for representing joint relationships. They do not provide a building design code, a tested knee joint for this chassis or a global erection certificate. The current documentation has a Python interface to a separate C++ kernel; bundling an untested native dependency would make this GH package less reliable. R22 therefore implements explicit contact/insertion metadata and inspectable rectangular joint context without pretending to execute that kernel.
   - https://petrasvestartas.github.io/compas_wood/
   - https://petrasvestartas.github.io/compas_wood/examples/joinery_solver_from_breps/
   - https://petrasvestartas.github.io/compas_wood/examples/assign_insertion_direction/
2. **Metsä Kerto-Ripa** is a relevant example of ribbed timber construction, but its composite behaviour uses structural adhesive and controlled manufacture. Its published performance cannot be assigned to these dry assembled rectangles. R22 assumes no composite action. LVL beam and cross-banded panel products have different directional behaviour; “LVL” alone is not a product specification.
   - https://www.metsagroup.com/metsawood/explore-wood/kerto-lvl-applications/kerto-ripa-elements/
   - https://www.metsagroup.com/metsawood/products-and-services/design-tools/kerto-lvl-manual/
   - https://www.metsagroup.com/contentassets/f8ff384a208d4786959efa4bca9fab2c/kerto_lvl_for_load-bearing_applications.pdf
3. **WikiHouse** demonstrates a different way to assemble sheet parts into structural cassettes. Its original source objects and connection examples belong in the comparison, but no equivalence between its tested details and B is inferred. Its insulation guidance highlights installation at assembly junctions and thermal bridging; filling a CAD void alone does not make a continuous envelope. Its manufacturing guide's sheet/router constraints matter when choosing blanks, not when assigning spans.
   - https://www.wikihouse.cc/engineering/what-is-skylark
   - https://www.wikihouse.cc/design/insulation
   - https://www.wikihouse.cc/guides/manufacturing

These are design implications inferred from primary documentation. No numeric allowable loads, fastener capacities or supplier-approved assembly sizes are used.

## Alternatives considered

| Approach | Advantage | Problem controlling this implementation |
|---|---|---|
| One-piece thin plywood portal | Few nominal profiles and expressive cut-out form | Whole portal does not fit ordinary sheets; grain direction, buckling, material removed from centre, transport and splices dominate. A closed CAD outline is not evidence that 18 mm plywood carries the intended loads. Not selected. |
| Segmented plywood ribs with tab/slot knees | CNC-compatible joint exploration; repeatable profiles | Slots reduce net section, need corner relief and insertion tolerances; different load directions and sequencing affect handing and machining identity. No validated connection available. Retained as future coupon study, not represented as resolved. |
| Bonded ribbed panel | Potential composite efficiency and prefabrication | Structural glue, factory controls and product-specific design are essential. Conflicts with treating the same model as an unspecified dry site assembly. Not selected. |
| Segmented LVL plate ribs with separate cheeks | Straight blanks; visible load-path questions; replaceable adapters; members can be handled separately | Knees, longitudinal restraint and hold-downs remain engineered details. This is the implemented research baseline. |

The present ribs are plate-like solid members, not hollow timber-frame wall cassettes. Reducing thickness is not an optimization until stability and connections are checked. 27/45/63 mm in the interface are geometry candidates, not confirmed stock or suitable thicknesses.

## Same-footprint spacing screen

All cases are 3600 mm long × 3600 mm transverse structural span, with 2100 mm between finished deck top and roof-rib underside, 45 × 240 mm ribs, 18 mm skins and cheeks. No resizing is used. Terminal rib faces are flush to chassis ends; intermediate ribs are centred on their station. Ribs number bays + 1.

| Pitch | Bays / ribs | Provisional types | All modelled pieces | LVL / plywood / insulation pieces | Rib knee/base interfaces | Assembly groups |
|---|---:|---:|---:|---:|---:|---:|
| 600 | 6 / 7 | 31 | 248 | 52 / 76 / 120 | 28 | 13 |
| 900 | 4 / 5 | 31 | 168 | 36 / 52 / 80 | 20 | 9 |
| 1200 | 3 / 4 | 31 | 128 | 28 / 40 / 60 | 16 | 7 |

This is the final screen after merging adjacent insulation rectangles that share a complete face. The initial clipping output had unnecessary subdivisions (284/192/146 pieces and 33 types); those subdivisions have been removed physically from the cut schedule, without hiding insulation or changing its volume. Cuts around cheek plates and backing remain explicit. Flexible batts could use notched blanks instead, but that would require new machining/profile identities and installation assumptions. R22 does not silently call separate rectangles one piece.

The 900 mm default is an inspection starting point, not a structural optimum. At 1200 mm, pieces fall by 23.8% relative to 900 mm, but unique types remain 31. Greater sheet support spacing and rib tributary load require verification before adopting it. Retaining all three pitches makes this tradeoff visible without imposing a new Studio grid.

| Pitch | LVL blank volume m³ | Plywood m³ | Insulation cavity m³ |
|---|---:|---:|---:|
| 600 | 0.968274 | 0.885946 | 8.806676 |
| 900 | 0.724950 | 0.852768 | 9.074884 |
| 1200 | 0.603288 | 0.836179 | 9.208987 |

Volumes are rectangular model quantities, not purchased stock, thermal performance or weight. Insulation merging preserves volume. No cutting-waste percentage is reported: supplier stock formats, kerf, grain and nesting are not resolved. At the default height, wall skin blanks are 2340 mm tall; taller configurations may exceed a selected stock format and require a supported split. The model does not invent that supplier compatibility.

## Identity and quantities

Part identity uses the shared manufacturing classifier: material specification, ordered dimensions/grain context, machining, handing and connection requirements. B explicitly marks product selection, holes and fastening patterns unresolved. Equal geometric floor and roof blanks are conservatively separate where connection roles differ. Candidate types are not verified interchangeable production types. The schedule keeps insulation cuts, plywood and LVL constituents; grouping a rib does not reduce their count.

The interface count covers two knees and two bases per rib only. It is **not the total building connection count**: skin fasteners, seam attachments, tie-downs, end closures, membranes and supplier fixings are unknown. Assembly groups are model organization, not certified lifting units. There are no purchased doors/windows in this open-ended study. Existing cassette procurement and complete-model IDs remain unchanged.

No percentage reduction against WikiHouse or Studio is valid here: the imported chassis, complete architectural cassette model and open-ended B study have different envelopes and programmes. No 75% target is claimed.

## Connections, support and erection

Roof ribs bear on uprights. Paired cheeks span the butt joint and have opposite X insertion directions. They are deliberately visible rectangular blanks: hole locations, edge distances, fasteners, slip, splitting and rotational stiffness require engineering. No moment-frame behaviour is assumed. Floor bases bear through the deck and require a resolved load path/tie-down. The nominal 3120 mm clear width is between upright inside faces; knee cheeks intrude into the upper corner zones. 2100 mm is central headroom, not unobstructed headroom across every corner.

Deck/roof transverse joints at 1200 mm stations have actual 90 × 90 backing between ribs. Backing lengths differ at the ends because terminal ribs sit flush; those exceptions are counted. Longitudinal sheet seams land on ribs. A bearing surface in CAD does not establish adequate fastening edge distances, panel span, diaphragm capacity or backing attachment. Longitudinal restraint and temporary bracing are particularly important before skins are fixed.

For inspection, install/handle members separately, then cheeks, backing and skins, then fill the cavities and detail the envelope. A complete rib may be preassembled flat for a later erection study, but R22's new explode control is not that sequence. Existing Studio connected-wall animation is preserved separately. No complete B rib is labelled safe for a small crew to lift; grade/density, mass, centre of gravity, lifting points, temporary stability and risk assessment are still needed.

## Envelope and openings

Current B ends are open. No door/window frame, sill, threshold or header is smuggled into the scope. A later enclosed design needs a product-specific installation opening and an engineered host; openings may occupy several coordination increments. Insulation avoids all modelled solids but lacks membrane continuity, a verified vapour strategy, weather drainage, fire strategy, service penetrations and thermal-bridge treatment. An external continuous insulation layer could address bridging, but adding it would change quantities and connection stand-offs and is not modelled.

## Next evidence that would change the design

Select actual LVL and plywood products/stock sizes, define load and support conditions, and have an engineer establish rib, skin and connection design. Compare a dry cheek joint with an appropriate tested/proprietary connection; prototype insertion and tolerance coupons before generating CNC paths. Then add one bounded opening and end-wall module, resolve the complete envelope and rerun equal-scope counts. Those are unresolved engineering tasks, not hidden dependencies preventing the delivered GH geometry from running.

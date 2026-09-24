# Cassette 01 — initial module and interface specification

**All dimensions below are OBTP proposed nominal millimetres. They are not tested manufacturing tolerances or structurally sized members.**

## Coordinates and module family

X spans the studio width; Y is the repeating length; Z is up. Frame setting-out width is 4,572; Y length is N × 600 for integer N = 1…8. Floor top is Z = 238. Wall height H is 2,100 by default, or an explicitly optional 2,700 study. Roof frame starts at 238 + H. Exterior plywood lies outside wall framing and increases the outside envelope. Roof finishes, service zones and insulation overlays are not included in these setting-out dimensions.

| ID | Nominal assembly | Parts / logic |
|---|---|---|
| F600 | 4,572 × 600 × 238 | Two 45 × 220 boundary joists; three 45 × 510 × 220 blocking pieces; two 2,286 × 600 × 18 plywood panels |
| R600 | Same nominal box as F600 | Separate roof identity; identical provisional frame geometry, not a finished roof build-up |
| W600H… | 600 wide × 195 frame depth × H; exterior plywood 12 | Two 45 × 195 studs of H−90 length; two full-width 45-high plates; exterior plywood |
| W582H… | 582 wide, otherwise same | End-wall closure cassette; designed separately, not a stretched source model |

Every tall wall receives one mid-height backing piece and two half-height plywood panels so the sheet seam is supported. Standard-height wall plywood is 600/582 × 2,100 × 12. Taller panels are 600/582 × 1,350 × 12. Nominal panel envelopes fit the assumed 1,220 × 2,440 sheet; a nesting yield or machining allowance is **not** established.

For N modules: N floor + N roof + 2N side walls + 14 end-wall cassettes = **4N + 14 cassettes**. Each end fits six 600 cassettes plus one 582 cassette between side-wall framing: 6 × 600 + 582 = 4,182. At N = 4, setting-out is 2,400 × 4,572 and there are 30 cassettes. At N = 8: 4,800 × 4,572 and 46 cassettes. N = 1 remains a comparison geometry, not a usable room.

Default clear framing rectangle is 4,182 × (600N − 390), before internal linings/services. Wall panels are exterior sheathing, with unresolved corner wraps and weather seals; “closed frame” does not mean sealed envelope.

## Interfaces and primary source mapping

R1 is the main mechanical-fastener principle reference for each ordinary timber interface. R2 provides the European design framework. See RESEARCH.md for full citations and review limits. A source principle is not a finished connector detail.

| Interface | Geometric rule | Design / assembly requirement still open |
|---|---|---|
| Plywood → frame | Sheet boundaries supported by studs, plates, boundary joists and centre blocking | Product, fastener pattern, edge distances, gaps, racking/diaphragm design; R1 |
| Wall → wall seam | Boundary studs meet at each 600 mm line | Mechanical fastening from open cavity; design splitting, shear, slip and access; R1 |
| End wall → side wall | End-wall framing terminates at X=195 or 4,377 | Corner restraint and hold-down, exterior wrap, insulation continuity; R1 |
| Wall → floor | Bottom plate plane coincides with floor top at Z=238 | Bearing, deck compression, shear/uplift and transfer to foundations; R1/R2 |
| Roof → wall | Roof frame underside coincides with top plates | Bearing, uplift restraints, diaphragm action, roof drainage and installation access; R1/R2 |
| Slab → slab | Boundary joists meet at each Y=600i plane | Joist-to-joist fastening and supported sheathing seam; R1 |

Inter-cassette records contain identities, nominal interface points, type, source reference and **null capacity/fasteners**. Panel-to-frame is an internal interface principle; it is not counted as an inter-cassette record. There are no symbolic screws presented as verified hardware. Interface-point placement and zero positive-volume clashes are software checks only.

## Proposed manufacturing and erection route

CNC is used for repeatable plywood outlines and identification, not for a proprietary interlock. A panel saw can make these initial rectangular panels; CNC becomes more valuable with reviewed registration features and labelling. Timber is cut to length with a suitable saw. Drills/drivers, clamps, squares and a level are normal assembly tools; lifting effort and temporary stability require planning and cannot be inferred from a small web model.

Before cutting: confirm structural material grades/declarations, actual stock dimensions and moisture, sheet sizes, veneer orientation, edge protection, cutter/hold-down limits and a shop-reviewed parts list. Nominal faces touching in the model do not specify a zero physical gap. No cut files or hole locations are released. Do not replace plywood with MDF or ungraded furniture board.

Proposed sequence: prepare engineered supports and a level datum; assemble supported floor framing; check diagonals and tie the floor into its supports; erect and temporarily brace walls; connect boundary studs and corners while accessible; install roof framing and engineered restraints; inspect the load path before closing faces; then complete weather, insulation and air/vapour layers. This is a planning sequence, not a site method statement. Fastener access may require leaving selected skins off until inspection. Screws are provisionally favoured for access/disassembly, not claimed universally superior to nails.

## Habitable envelope proposal

Wall, inside to outside: fire/acoustic lining as designed → service zone → continuous taped air/vapour-control layer → 195 mm timber cavity with selected mineral wool → 12 mm plywood structural sheathing → continuous exterior insulation → compatible wind/water-control layer → drained ventilated rainscreen cavity → cladding. Product vapour resistance, outer insulation thickness and layer positions must be selected together using transient moisture analysis. Plywood on the cold side is a material concern, not assumed harmless.

Floor: finish/air-control continuity → structural deck → insulated joist zone → wind protection and designed moisture/ground separation. Foundations, underfloor ventilation, pests, splash water, capillary breaks and frost conditions need site-specific details. This is a suspended cassette floor proposal, not a concrete slab.

Roof: the displayed deck is a frame comparison datum. A reviewed warm-roof or ventilated-roof build-up, drainage fall/outlet/overflow, snow drift, waterproofing, vapour control and perimeter continuity must be added. Do not treat the current flat deck as weatherproof.

Repeated double boundary members, corners, base and roof edges are thermal bridges. Calculate whole assemblies, including timber fractions and junctions; insulation conductivity alone is not a U-value. Mineral wool does not provide airtightness or weatherproofing. Cut batts to actual cavities without gaps or uncontrolled compression. The standard cavity width is 510 mm, so off-the-shelf 565 mm batts entail trimming and waste.

Airtightness requires continuous, inspectable joins across cassette seams and service penetrations, followed by testing. Provide designed ventilation, moisture extraction and, where appropriate, heat recovery; opening a window is not the proposed ventilation specification. Habitable use also needs daylight, safe egress, fire and acoustic design. Unconditioned storage has different moisture/ventilation assumptions and must not inherit a habitable claim from this model.

## Rhino 8 / web relationship

System generates the nominal geometry in `dist/cassette/system.js`; Studio consumes that pinned System distribution. “Export geometry for Rhino 8” writes all timber/plywood parts and interface records, independent of the current visibility filter. `tools/rhino8/import_cassette.py` makes closed box Breps in a millimetre Rhino 8 document, preserves part names and stamps research status. It validates all Breps before adding objects. This is System-to-Rhino inspection, **not a newly completed bidirectional Grasshopper round trip**. Rhino edits must be deliberately reconciled back into the System specification; automatic overwriting is prohibited.


## Connection-study revision — 24 September 2026

See [CONNECTION_ALTERNATIVES.md](CONNECTION_ALTERNATIVES.md) for seven original, research-linked detail studies, review limits and the physical-validation brief. Generic plate envelopes and fastening zones are now inspectable; capacities, products and fastening schedules remain unassigned. This supersedes only the earlier description of the connection viewer, not the engineering holds.

# Cassette inspection and coordination — 24 September 2026

## Physical hierarchy

The cassette is an assembly, not a monolithic part. A nominal floor/roof cassette has two continuous 4,572 mm long joists, three cross-members and two plywood panels. The middle cross-member does not split either long joist. A standard wall has two studs, two plates and plywood; the taller study adds backing and a second panel. R90 changes selected solid member sections while preserving this hierarchy.

`inspection.js` derives the catalogue and internal contacts from the generator. Identical local geometry is grouped for browsing, while all instance IDs remain traceable. Part labels and explosion offsets are display metadata only. They never change vertices, dimensions, exports or connection measurements. Constituent parts can be isolated by name or selected in the table. Plywood visibility is separate from the complete parts list.

The rectangular frame pictured by the owner has six timber-to-timber face contacts. The inspection interface enumerates these actual contacts and each plywood-to-frame contact; it does not invent a fastening arrangement. Contact is not proof of restraint or an erection sequence. Stud–plate, blocking and sheathing fastening require product-specific coordination.

## Connector versus connection

A connector is a physical hardware item or a clearly labelled research candidate. A connection describes the relationship between particular members and the associated evidence/design holds.

- HBS580/HBS5120: simplified, dimensioned candidates from the existing source register. A screw is one physical object. Head, shank and thread envelopes are display regions, not separate manufactured parts.
- Face splice, corner angle, base tie, roof tie and internal frame angle: original concept envelopes extracted from existing research studies. An angle's two legs are presented as one object. No product, hole pattern or fabrication specification is implied.
- ABR/WHT, sheathing fasteners and foundation anchors: visible research/unselected entries without invented geometry. Actual product fit, layout, quantity and capacity remain unresolved.

Connections link to connector entries and vice versa. The default list filters to the selected object/type; All connections exposes the full register. Floor and roof seams are separate entries. Foundation and opening requirements remain explicitly undesigned.

## Three distinct inspection views

1. **Actual part contacts / assembly interface:** real members or cassette instances from the selected generated assembly. Internal contacts have no implied fasteners.
2. **Measured screw position:** the retained six representative two-bay, 2,100 mm studies, with the chosen Original/R90 revision. The UI explicitly states this fixed scope; changing the assembly height or occurrence does not extend those measurements.
3. **Research alternative:** the existing original plate/tie studies and source limitations. Their generic dimensions do not become R90 product designs by changing the revision selector.

Full cross-sections and separation are used throughout. No cut-preview control is exposed. Legacy low-level cutaway geometry tests remain available as historical API regression checks.

## Decisions and verification still open

Research, UI corrections and the System-first → Studio development sequence are authorized. No repeated owner permission is needed for routine implementation. Technical holds remain:

| Item | Required next work |
|---|---|
| Timber / plywood | Grade, declarations, stock dimensions/availability and structural sizing |
| Internal assembly | Stud/plate/blocking and panel attachment design, installation access, tolerances and sequence |
| Connectors | Product-specific assessment and fit; fastening layout, quantities, spacing and resistance |
| Supports / uplift | Support selection and a continuous foundation-to-roof load path |
| Openings / envelope | Jamb/header/sill, roof drainage, weathering, airtightness, insulation and moisture coordination |
| Verification | Engineer-defined calculations, material checks and physical prototypes |
| CAD integration | Windows Rhino validation; no automatic bidirectional workflow claimed |

The owner may choose between developed design alternatives; permission alone cannot close an engineering or evidence gap. Purchases and third-party contact require separate authorization. Existing WikiHouse opening/source restrictions continue independently.

## Software checks

`tests/inspection.cjs` checks non-mutating explosion metadata, actual contact counts, continuous joists, traceable grouping, distinct floor/roof seams and honest connector states. `tests/cassette-browser.cjs` checks real object-part explosion/isolation/reset, contact selection, integrated original/revised probes, related connector navigation, exports, mobile overflow and version switching. Existing cassette, measured-detail and WikiHouse regressions remain release gates. These are geometry and UI checks only.

> Historical research/checkpoint, retained intentionally. Not the current project rulebook. Read ../project/PROJECT_MAP.md and current variation documentation first.

# Connection source map — research checkpoint 01
Date: 2026-09-23. Status: candidate selection, not construction specification.

UPDATE: Visual LT080 audit found the published sheet insufficient to reconstruct the finished mating geometry. See [LT080_GEOMETRY_AUDIT.md](LT080_GEOMETRY_AUDIT.md). LT080 modelling is on hold pending the missing machining/profile information; no source geometry has been invented.

## Accepted direction
Independent timber frame with non-load-bearing enclosure. Timber interlocking first; screwed and bolted alternatives remain in scope. Rhino 8 / Grasshopper on Windows is available to the owner. Web geometry should be exported from the same master geometry, not redrawn independently.

The owner now explicitly requests research papers and working market solutions. This supersedes the earlier restriction against product research; it does not authorize supplier outreach or purchasing. Prefer one geometry authority per exact connection variant. Research about a related joint is supporting evidence, not validation of a product.

## Six-interface map
| Interface | Primary lead | Fit and unresolved issues |
|---|---|---|
| Post–transverse beam | Chen, Qiu & Lu (2016), Type 1 dovetail, as a separate research specimen | Documented beam-end-to-column-top connection. Current beam01 passes across/bears above posts: this is a different arrangement. Do not cut it into the current model or silently split the beam. No direct timber-joint integration selected yet. |
| Transverse–longitudinal beam | Lignatool LT080 dovetail | First commercial timber-interlocking geometry candidate. Check beam-end insertion, supporting member residual section, mortise position, uplift restraint and corner congestion. |
| Frame–enclosure | Rothoblaas WOODY | Commercial timber connector with screw attachment: hybrid, not all-timber. Candidate only; panel edge framing, movement allowances, gravity support and wind load path are undefined. |
| Floor–frame | Rothoblaas WOODY | Manufacturer lists floor applications. Current floor01 is a solid envelope without joists, rim members or supports; no valid screw anchorage substrate exists in the model yet. |
| Roof–frame | Rothoblaas WOODY | Manufacturer lists roof applications. Exact support detail, uplift resistance and weather/service conditions remain unselected. A listed application is not a complete roof connection. |
| Panel–panel | KNAPP WALCO V60 KS | Prefabricated wall connector candidate. Requires actual edge studs, insertion clearance and the specified screw/washer system. Do not substitute a generic screw. |

The existing sixth-list entry floor/wall and this floor/frame interface are not equivalent. Preserve the floor/wall threshold gap as a separate unresolved enclosure detail; do not mark it solved by adding floor support.

## Three fastening families
### Timber interlocking: Lignatool dovetail
Primary geometry authority:
https://www.lignatool.at/en/pages/dovetail-milling-jig
LT080 drawing:
https://cdn.shopify.com/s/files/1/0686/4456/9356/files/LT080_Dimensions.pdf?v=1689282969

Manufacturer lists LT080 for beam widths 60–180 mm and heights 60–320 mm, and provides a dimensioned drawing. Our provisional 160 × 320 mm beam lies within that stated tooling range; this is not a structural approval. The page distinguishes the LT080 tenon angle from the cutter flank angle: these must not be conflated.

Geometry gate: visually audit the drawing and obtain all mating-profile dimensions, reference planes, radii, clearance and cutter information. Do not infer missing manufacturing dimensions from images. Customer calculation access is described; it has not been accessed. CAD redistribution rights have not been established.

### Screwed metal alternative: KNAPP RICON S
Primary authority:
https://www.knapp-verbinder.com/en/produkt/ricon-s-connectors-for-high-capacity-standard-connections/
Document hub:
https://www.knapp-verbinder.com/en/downloads/product-downloads-2/

Manufacturer connects performance to original screws and ETA-10/0189. Its document hub offers installation documentation, assessments and CAD. Exact size, screw schedule and member compatibility remain unselected. Availability of CAD is not permission to redistribute it. Do not represent internal connector bolts as a generic bolted timber joint.

### Bolted alternative: Simpson Strong-Tie CC family
Manufacturer evidence that CC is the bolted family, distinct from CCQ:
https://seblog.strongtie.com/2023/12/ninth-day-of-trivia-strong-drive-sds-screws/

Retain as a market lead for beam-over-post geometry only. Current model-specific dimensioned data and regional assessment have not been retrieved; not ready to model. Do not scale an imperial product or invent a plate/hole schedule for 160 mm timber.

Rejected shortcut: Simpson BTC.
https://pim.strongtie.eu/api/v1/public/download/gb/en/product/497/BTC.pdf
The retrieved data sheet specifies concrete/steel supporting members. It is not the timber-to-timber bolted solution for this frame.

## Research register
1. Chen, C.; Qiu, H.; Lu, Y. (2016). Flexural behaviour of timber dovetail mortise–tenon joints. Construction and Building Materials 112, 366–377. DOI: 10.1016/j.conbuildmat.2016.02.074.
Author manuscript:
https://www.pure.ed.ac.uk/ws/files/24758306/CBM_paper_Chen_Qiu_Lu.pdf
Examines two beam–column arrangements with experiments and modelling. Type 1 inserts from above; Type 2 uses side entry, lowering and a wedge. Useful for assembly and contact behaviour. Not evidence for LT080 capacity; material, geometry, loading and restraint differ.

2. Shields, L. D. (2011). Investigation of Through-Tenon Keys on the Tensile Strength of Mortise and Tenon Joints. Virginia Tech thesis.
https://vtechworks.lib.vt.edu/items/5c390ebc-88c6-44e0-a8da-ec967d1a5974
Repository abstract confirms experimental and analytical investigation. Full thesis detail has not been audited in this checkpoint. Retain for a future keyed-through-tenon specimen, not a dimensional source for our dovetail.

3. TFEC Bulletin 2018-08A, Keyed Through Tenon Joints – Structural Design Guide.
https://www.tfguild.org/timber-frame-engineering-council/technical-bulletins/view/118/download
Previously reviewed supporting guide tied to Shields research. A separate joint family, not a recipe to combine with Lignatool geometry.

## Panel connector evidence
WOODY product:
https://www.rothoblaas.com/products/fastening/brackets-and-plates/concealed-connections/woody
Technical-sheet search result:
https://www.rothoblaas.com/attachments/291038-product-1215/woody-en-technical-data-sheet.pdf
The product page was read, but this technical-sheet URL returned 404. Indexed sheet text identifies screw attachment. Product-page and indexed sheet dimensions for the larger variant differ (165 vs 160 mm height); resolve from a current authoritative drawing before modelling. CAD/BIM headings alone do not establish downloadable files.

WALCO:
https://knappconnectors.com/prefab-wall-connectors/walco-v60-ks-screw-washer-prefab-wall-connector/
Use manufacturer installation/assessment data for the exact regional variant before detailing.

## First implementation decision
Start by auditing LT080 as an isolated beam–beam specimen. It is the strongest commercial timber-interlocking lead found for our provisional beam dimensions. Post–beam is deferred because its current topology differs from the research example. Do not alter frame topology just to fit a joint.

After geometry gate:
1. Create Rhino solids in millimetres, with separate member/joint IDs and source metadata.
2. Build the Grasshopper definition around documented parameters; freeze unknown or unverified dimensions.
3. Check closed solids, mating surfaces, residual timber and assembly path. Nominal surface contact alone is insufficient.
4. Export display meshes from these same solids with units, IDs and revision metadata.
5. Add assembled/exploded/section inspection to the existing System website.
6. Run the definition in the owner's Rhino 8 before claiming Rhino execution verified.

No Rhino model, Grasshopper definition, manufacturing file or structural approval has been produced at this checkpoint. No live application geometry changed.

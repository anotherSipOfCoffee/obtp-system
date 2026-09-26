# Supplier systems / A02

26 September 2026. Owner decisions: keep OBTP Cassette as the default; add a supplier system as a separate choice only when its assemblies are coordinated. Prioritize Lithuanian supply; prefer comprehensive Nordic packages where appropriate. Wind and snow analysis is paused, not set to zero. General location is Lithuania, not a site-specific climate assignment.

## Recommendation

**Develop Hunton as the first Nordic alternative; keep Husline and Skado medis on the Lithuanian manufacturing shortlist.** Hunton is a documented candidate, not an implemented or supplier-approved OBTP system. STEICO provides a complementary technical route with Lithuanian distribution evidence. LapWall is a strong prefabricated-element benchmark, but current detailed files and Lithuanian delivery need resolving.

| Candidate | Verified offering / documentation | OBTP decision and remaining gap |
|---|---|---|
| **Husline, Lithuania** | Gargždai manufacturer of prefabricated wall, floor and roof elements. Published scope includes insulation, openings and interior completion at different delivery levels. | Local manufacturing candidate. Four standard wall types are described, but an exact dimensioned sauna assembly and joint schedule were not recovered from the reviewed pages. Do not infer a specific build-up from marketing photographs. |
| **Skado medis, Lithuania** | Prefabricated cabins and utility buildings; wall, roof and floor systems illustrated on the manufacturer's site. | Local candidate suited to a cabin programme. Obtain identifiable assembly drawings, product declarations and wet/thermal-room details before generating its branded model. |
| **Hunton, Norway** | Construction packages cover walls, floors, roofs, beams and columns. The public wall system combines framing, Nativo insulation, wind board and vapour-control products. Project-specific precut/numbered components and connection documentation are available. | Preferred Nordic research route. General housing wall layers are not automatically sauna layers. Confirm sauna lining/vapour-control transitions, ground floor/waterproofing, small-kit supply to Lithuania and project-specific connection details. |
| **STEICO, EU / Lithuanian distributor evidence** | Structural I-joists/LVL, insulation and sealing products; separate W4 opening and W5 wall/floor details and floor/roof connection library. | Strong manufacturer-data route, but a system of products rather than evidence of a complete OBTP-sized factory kit. Sauna adaptation and fabricator remain unresolved. |
| **LapWall LEKO, Finland** | Public page offers wall/roof BIM assemblies with performance information and DWG/PDF details. Current catalogue includes low-rise element offerings. | Strong factory-element benchmark. Older indexed PDF URLs returned 404; do not use search-index excerpts as a current geometry lock. Latest manual retrieval and Lithuanian supply need resolving. |

The ranking is a project inference from breadth of documentation and delivery scope, not a cost comparison or endorsement. No suppliers were contacted, quotations obtained or purchasing availability confirmed.

## Primary evidence reviewed

1. Husline products: https://www.husline.com/products/ and timber-frame scope: https://www.husline.com/products/timber-framed-houses/ (HTML fetched successfully; search reader intermittently returned 502).
2. Skado cabins: https://www.skadomedis.lt/products-prefabricated-cabins/ ; utility buildings: https://www.skadomedis.lt/productsprefabricated-utility-buildings/ . Illustrations are not sufficient for a fabrication schedule.
3. Hunton package: https://www.hunton.no/produkter/gulv/hunton-konstruksjon/ ; wall: https://www.hunton.no/produkter/vegg/huntonveggen/ . Its procurement/design process is project-specific; a Norwegian design example is not an LT design approval.
4. Hunton **Konstruksjonsdetaljer V01-09/25**, 40 pages: https://www.hunton.no/wp-content/uploads/2023/08/hunton-konstruksjonsdetaljer-i-bjelken.pdf . The URL folder date is not the document edition. Includes bearings, hangers, reinforcement and holes. Its design factors and capacity tables are not transferred into OBTP; action cases are paused and assembly eligibility remains unresolved.
5. Hunton technical handbook, currently linked but marked **02/18**: https://www.hunton.no/wp-content/uploads/2018/09/i-bjelken-teknisk-handbok-web.pdf . Page 4 identifies STEICOjoist/STEICOwall as the ETA/CE product names. Do not combine different editions or section sizes without checking the current declaration. We have not adopted its thermal or capacity values.
6. STEICO system: https://www.steico.com/eur/solutions/new-construction/the-steico-construction-system ; details: https://www.steico.com/uk/resources/construction-details (page states updated 21 November 2023).
7. STEICO opening W4: https://www.steico.com/fileadmin/user_upload/English_Media/Construction_Details/Wall_Details/W4.pdf ; floor junction W5: https://www.steico.com/fileadmin/user_upload/English_Media/Construction_Details/Wall_Details/W5.pdf . These establish component arrangements, not a project-specific lintel/fastener specification.
8. Lithuanian STEICO distributor product listing: https://www.hesora.lt/steico/produkcija/steico-wall/ . Local stocking, lead time and system-design responsibility are unverified.
9. LapWall documentation: https://lapwall.fi/dokumentit ; low-rise elements: https://lapwall.fi/elementit-matalaan-rakentamiseen . Manufacturer-linked ProdLib lists IK1 window joints with 170 mm frames; this is not proof of compatibility with our Pihla sauna frame or OBTP wall.

## Model and configurator policy implemented

`obtp/suppliers.py` owns construction-system IDs, product status, evidence links and stable part references. The default is ID 0 OBTP Cassette. ID 1 Hunton is visible as **in development**, disabled in the buyer control and rejected by Python if requested. It cannot fall back to Cassette geometry with a different label. No extra preset is introduced.

An alternative becomes selectable only after: a distinct geometry adapter; source-locked layers/sections; all six layouts and opening fit checks; model-linked thermal domains; coordinated sauna vapour control and waterproof floor; actual junction/anchorage specifications; and transparent unresolved engineering status. Wind and snow remain paused and are not part of this research release's acceptance claim.

Reference status is explicit for each object type:
- Pihla window: dimension-based candidate, not exact proprietary extrusion or confirmed order.
- Harvia heater: researched candidate; existing model remains a generic placeholder until mounting and clearances are coordinated.
- Harvia SAS10001 foil / SAS10002 tape: sauna-specific specification candidates; all penetrations and transitions still need detailing.
- Thermory: lining/bench installation reference, not a claim that the model's generic profiles are catalogue products.
- Ruukki Classic C: pitched-roof dimension/slope reference; hidden for flat membrane roof. Complete roof system not specified.
- Structure, insulation, doors, deck, facade, foundations and fasteners: do not assign an unsupported supplier identity. These remain explicit outstanding procurement selections.

Supplier logos are original website assets used for identification, without partnership/approval claims. Source URLs and checksums are in `assets/sources.json`. Manufacturer technical drawings with reproduction restrictions are linked, not copied into the dossier.

## Window drawing correction

D1a and D1b are **vertical** head and sill cuts through the actual window centre plane. Each polygon retains its source part ID. The full window vertical section appears beside the elevation on sheet 4; sheet 5 shows enlarged head/sill cuts at 1:2. Both are generated from the same detailed 3D model. They expose missing flashings, seals and fixings instead of inventing them. Door/corner detail spaces remain reserved. The old horizontal jamb view is removed.

## Next supplier coordination package (not sent)

Provide the six layout/model sets and ask the preferred supplier for: exact proposed wall/floor/roof types and revisions; sauna-rated lining/foil/insulation assembly and drying conditions; head/sill/jamb, floor-wall, roof-wall and corner details; header/point-load provisions; connectors and installation schedules; foundation interfaces; materials/DoPs/thermal input data; BIM/DWG/IFC reuse terms; Lithuanian delivery and responsibility boundary. This is a concrete request list, not authorization to contact suppliers.

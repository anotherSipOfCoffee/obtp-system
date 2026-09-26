# Studio R07 — two enclosed blocks and a covered working court

Owner authorization, 2026-09-26: implement Studio in the same Cassette/Grasshopper pipeline as Sauna, research non-residential alternatives to the bedrooms in IMG_3141.png, validate and publish. This scoped release supersedes the earlier planning pause. No Workshop or fourth preset is introduced. Sauna remains the default.

## Program choice and evidence

Selected: personal creative/hobby workspace in the larger left block, preparation and material storage in the smaller right block, open covered work/exhibition space between. A work surface is included in each enclosed room. The covered centre remains clear for front-to-back circulation and temporary work. Storage adds shelves, not sleeping accommodation. The right block has direct external access for materials as well as access through the central space. Doors between court and rooms swing inward to keep the court route clear. No bed, kitchen, shower, sauna heater or residential program is generated.

Primary architectural precedent: Stan Allen Architect, E/S Studio (2020), https://www.stanallenarchitect.com/work/e-s-studio/ (accessed 2026-09-26). The architect describes a painting workspace paired with smaller drawing/preparation/storage space and an entry courtyard. This supports the functional pairing; its geometry and dimensions are not copied. Our two-block composition comes from the owner's screenshot, whose architect/project identity and dimensions remain unknown. It is a spatial reference, not construction evidence; the original photograph is not republished as our product render.

Alternatives considered: a second quiet workroom (useful but duplicates the main work area); equipment archive (useful as storage option); wet ceramics/darkroom (requires drainage, ventilation and material-specific design not currently solved); accommodation (excluded). Main program stays light creative/hobby work, not hazardous processing or an industrial workshop. Product label 'Studio' is not a legal use classification.

## Permit and classification limits

VTPSI: https://vtpsi.lrv.lt/lt/naujienos/statiniai-kuriems-statybos-leidimas-nereikalingas/ (published 2023-04-12; read 2026-09-26) explains that SLD requirements depend on category, parameters and territory. Its date means it is general guidance, not confirmation of current site-specific exemption.

VTPSI's 2023-05-04 auxiliary-building consultation describes the 50 m² / 5 m I-group auxiliary non-residential envelope. Existing project design constraints remain 50 m², 5 m, 6 m support spacing. Current statutory classification of a particular creative workspace, any commercial/public use, the roofed open area and land-use suitability must be verified for the actual project. Do not present renaming rooms as a permit strategy. The current STR index is https://vtpsi.lrv.lt/lt/teisine-informacija/teises-aktai-2/statybos-techniniai-reglamentai/ ; this release does not assert a fully verified current legal area interpretation or exemption.

Conservative design screen includes the entire bounding roof/deck projection, including covered court, cladding, eaves and front terrace. It is not presented as certified cadastral/regulatory area. No omission of the centre to increase permitted size. Customer information explicitly retains separate site/land-use checks. Genuine non-residential use is part of the brief, not a guarantee of SLD exemption.

## Shared implementation

`model.py` keeps one cassette floor/ceiling generator, one wall/opening routine, shared connection records and shared product window recipe. Program-specific placements and furniture are selected by `program_type` (0 Sauna, 1 Studio). `envelope.py` uses the same lining/facade surface routine and roof/terrace construction. `insulation.py` fills only enclosed Studio blocks; open centre has no thermal-room claim. Deck boards replace exposed centre floor skin. Stable IDs distinguish Studio room/entry/header/furniture instances.

Both programs use the existing 600 mm layout steps, 195 mm wall framing, 220 mm cassette members and current roof/window controls. This is reuse of the existing Cassette study, not implementation of an approved supplier alternative. Future supplier-schema refactoring remains governed by PIPELINE_ARCHITECTURE_R01.md.

Saved structural dimensions in mm:

| Size | Creative room clear structure length | Court structural opening | Prep/storage clear structure length | Overall structure L × W |
| --- | ---: | ---: | ---: | --- |
| S | 2400 | 1800 | 1800 | 6780 × 2790 |
| M | 3000 | 1800 | 1800 | 7380 × 2790 |
| L | 3600 | 1800 | 1800 | 7980 × 2790 |

Room clear structure depth is 2400; 36 mm interior finish zone each side reduces usable room dimensions. Court-facing exterior finishes reduce court clear width to 1632 mm. Cabinet option preserves preparation table clearance by shortening that table. Actual door leaves/frames reduce clear aperture below nominal 900 mm; accessibility compliance is not asserted.

Mono-pitch conservative roof/deck bounds: S32.311584, M34.986384, L37.661184 m². Maximum model bearing-line spacing is evaluated from the shared floor span, canopy supports and 1800 mm court headers. Heights use actual generated vertices/roof slopes with hard 5000 mm cap. These geometric checks are not member/connection capacity checks.

PDF: same nine A3 sheets from detailed model, Studio labels and occupied/unoccupied thermal input placeholders; no sauna heater or cycle imported. Main plan and sections retain 1:25. Conceptual web plan retains merged black wall silhouettes. Both outputs share geometry hashes. GH exposes the program selector; offline package includes six defaults for each program. Native Rhino/GH execution remains pending.

## Engineering and implementation holds

Open-centre header end connections need designed hangers/fasteners, bearing and lateral-load checks. Header sizes are existing Cassette-depth studies, not calculated spans. Foundations, roof bracing, moisture control, below-floor weather protection, window/door final products, glazing, ventilation and heating are unresolved. Wind/snow remain paused. Supplier references are candidates; Studio does not inherit sauna foil or Harvia heater records. No construction or engineering approval is claimed.

Acceptance: 54 Studio combinations plus unchanged 54 Sauna catalogue; all geometry envelope screens; open court with no enclosing thermal walls; storage variant; multiple roofs/windows; program switching roundtrip; model-derived views; nine-sheet A3 bounds; browser desktop/mobile/Lithuanian/PDF tests and live checks before publication completion.

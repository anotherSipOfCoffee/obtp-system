# R19 — continuous recesses and actual bay alignment

Review revision, not merged or published. Canonical System owns geometry; Studio consumes its pinned export. Doors and the 900 × 1200 mm grid are retained following the user's acceptance of the narrower-door recommendation.

## Implemented

- Exterior facade now extends across the Sauna annex and subtracts rectangular niche openings. Matching vertical cladding returns along the entire sides and back; the full soffit is at the 1900 mm opening datum. Added backing panels, battens and heads are physical counted components, not hidden layers.
- Outdoor seat recess remains 300 mm deep from the finished back. The thicker finish moves its storage divider 36 mm compared with R18. Clear niche width is **537 mm** for the default 900 mm annex. This is tight for shower use; usability, waterproofing, drainage, ventilation and corner fastening remain unresolved. The shower fittings were moved in front of the finish and below the soffit; their product envelope is still generic.
- Terrace bay-edge joists use the actual floor-member faces, not grid-centred members offset by 22.5 mm. Each 900 mm bay repeats edge/middle/edge terrace supports. Adjacent cassette edges remain paired; intermediate terrace supports do not imply extra floor members. Foundation rail rhythm is unchanged; no capacity is asserted.
- Existing floor bays remain intact. Adding matching middle floor joists was tested and rejected because it increased pieces and diversity without being necessary to align bay edges. Roof bays are unchanged.
- Terrace boards retain one direction including returns. GH keeps assembly/core sliders and unique-part colours. Schedule/assembly PDFs remain limited to default Studio M with open sliders. Cladding remains last in the assembly sequence.

## Doors — investigated, not substituted

Harvia D71904M is a published 690 × 1890 × 92 mm sauna-door frame. Pihla M33 offers widths from 690 mm. With a provisional 10 mm installation allowance on each side, 690 + 20 + 180 mm double-jamb framing = 890 mm, within a 900 mm bay. Frame width is not clear passage. Exact installation height, hardware and usable passage are not verified.

The preliminary default Sauna M geometry trial changed 130 to 137 provisional primary types when narrower openings were placed within individual bays. It was not a certified supplier model or an adopted design. Narrowing the entrance solely for type reduction is rejected. Existing door positions/widths remain; the remaining opening and terminal variants are honest exceptions.

Sources checked 27 September 2026:
- https://www.harvia.com/en/products/D71904M/glass-door-clear-7x19-pine-frame
- https://www.pihla.fi/product/ulko-ovi-m33/
- https://www.pihla.fi/en/product-tag/paloei30/
- https://www.pihla.fi/ulko-oven-asennus-ohje/

## Review and reproduction

`manufacturing-comparison.md` and its compressed JSON contain all baseline/current counts and same-footprint controls. `previous` is R18 at `2c21ad5d2d30915487f19e72a18f545e575befba`. The original and first integrated cell pins are unchanged. Only facade finish boards are excluded from primary counts; added backing, battens, trims and every other category remain included.

`niche-comparison.png` compares R18/R19 exact box geometry with depth-buffered orthographic views; the roof and adjacent building are cut away to expose the recesses. `terrace-frame.svg` compares the actual floor/terrace member faces at two bay seams. `index.html` is the interactive whole-model baseline comparison.

Rebuild counts with `compare_manufacturing.py review-r15 --full-catalogue`, then `render_review.py review-r15`. Rebuild detail images with `render_details.py review-r15` (NumPy and Pillow). Runtime GH does not depend on these optional review-image packages.

Engineering remains unresolved: foundations, member capacities, bracing, connections, wet-area build-up, proprietary product fit and safe manual lifting. Portable tests do not establish native Rhino/GH execution acceptance.

## Measured results

| M / flat / 1180 mm window / timber foundation | R18 types / pieces | R19 types / pieces |
|---|---:|---:|
| sauna-m-open | 130 / 1057 | 131 / 1063 |
| sauna-m-storage | 158 / 1291 | 172 / 1305 |
| studio-m-open | 137 / 1305 | 137 / 1314 |
| studio-m-storage | 138 / 1310 | 138 / 1319 |

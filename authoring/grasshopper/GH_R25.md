# R25 — Custom plans drive cassette construction

28 September 2026. GH only. No website, Studio pin, Drive or Architecture changes.

## Open
Extract the complete ZIP into a fresh writable folder. Open Grasshopper, then run `CREATE_GRASSHOPPER.py` using Rhino 8 Python 3. It creates `OBTP_Sauna_Cassette_R25_*.gh` beside its required modules. This package supplies the creator, not a pre-generated native definition. The R24.1 fix removing the redundant `SetSource` API call is retained.

## What now generates 3D
Select **Custom** (index 6 / seventh choice). Supported rectangular strip layouts include:
- Sauna alone or entrance alone.
- Either indoor room with the terminal shower/storage/seat zone.
- Both indoor rooms, in either order, with or without that terminal zone.
- The outdoor zone at either end; the complete construction is reflected consistently.
- Passage between indoor rooms, or a solid partition with a separate exterior entrance for each disconnected room.

Activation and connections stay independent. Relationship `none` does not remove a room. `adjacency` does not invent a doorway. External-access relationships remain route requirements using the terrace; they are not certified accessible circulation. Arrangement is a zero-based index into the feasible orders; the layout report lists its valid range.

Room boundaries now drive front/back wall runs, partitions, room finishes, ceiling lining, insulation, equipment and drawing labels. Existing canonical cassette, opening, roof, foundation, terrace and assembly recipes are reused. A separate plan-construction adapter holds topology rules; there is no second geometry pipeline. Six saved presets retain their exact R24.1 physical parts and drawings. Their geometry and drawing hashes are checked against frozen commit `b7508ea4048fc01d1af4bd3f380e5c6779226552`.

New topology cases place the fixed window in the back wall of the sauna (or entrance if no sauna exists), reserving the front for exterior doors. The internal door swing diagram points towards the entrance room. These are explicit custom-layout conventions, not supplier-approved handing. Original saved layouts are untouched. A standalone sauna's window behind seating needs glazing, guarding and usability review.

## Remaining limits
- Outdoor-only still reports PLAN ONLY: a detached enclosure/backing/support recipe has not been established. No fallback model is generated.
- Rectangular rooms in a single strip; no L-shapes, angled walls, arbitrary graph solver or separate roof zones.
- Dimensions, area and opening/framing fit must pass existing checks. Large window selections can fail in short rooms; choose a smaller offered frame or enlarge the room. Doors are not silently narrowed.
- Shared relationships do not certify clear passage, accessible thresholds, heater clearances, ventilation, waterproofing, foundations, roof capacity or lifting. Door products and some installation details remain candidates/placeholders.
- Existing connected-wall erection is a display sequence, not a certified lifting unit. Preview controls, quantities, loose-part recipes and export controls are retained. Sauna PDF actions remain disabled as before.
- No unique-part reduction is claimed from adding/removing rooms or changing layouts.

## Review and verification
`review-r25/review.html` contains four local examples with derived plans, structure cutaways and complete model views. The adjacent `.3dm` files contain all physical model pieces. Regenerate with `EXPORT_CUSTOM_REVIEW.py`.

Portable tests cover supported room selections/orders, disconnected access, changing dimensions/settings, stale-plan rejection, fit failure, absence of omitted-room equipment, structural/opening clashes, model/drawing identity, unchanged frozen presets and connected-wall stage integrity. Exported 3DM models are reopened and every object is checked as a valid solid. Native Rhino/GH creation, sliders, shading and exports still require host acceptance.

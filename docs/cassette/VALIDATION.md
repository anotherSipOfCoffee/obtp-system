# Cassette 01 validation — 23 September 2026

## Saved Phase 1

System: `76106edc9dae6ae711831a87d2d99919e2a84731`.
Studio: `b286ac2ae29d340e44c7115dfa2459f04dd46abd`.
Both are on `dev/obtp-independent-v1-20260923`; no live deployment.

- [System cassette check](https://github.com/anotherSipOfCoffee/obtp-system/actions/runs/35906029424): passed geometry, WikiHouse regression and browser tests.
- [System existing browser check](https://github.com/anotherSipOfCoffee/obtp-system/actions/runs/35906029341): passed.
- [Studio variations check](https://github.com/anotherSipOfCoffee/obtp-studio/actions/runs/35906113085): passed prepared pinned-System build, v1/v2/v3 switching, module counts and existing controls.

Geometry tests cover all N=1…8 at H=2,100 and 2,700: 16 full assemblies, stage counts, finite coordinates, positive-volume intersections between all box parts, continuous end-wall framing, supported nominal sheet envelopes and graph connectivity. All passed. Tests reject unsupported module counts/heights/stages. They operate on exact orthogonal box geometry; they are not physical tolerance tests.

Browser checks cover object and five inter-cassette connection views, module and height controls, skin visibility, layer selection, explode/reset, disabled openings, JSON export, WebGL error status, desktop/mobile and absence of JavaScript page errors. Screenshots were visually inspected. The default frame view is intentional so the cassette construction can be seen.

The four-module export contains 166 part boxes. Using rhino3dm, all were converted to valid closed Breps, written as Rhino 8-format `.3dm` and read back with equal object count. **Windows Rhino 8 and the Rhino ScriptEditor importer were not executed here.** This validates file geometry, not a Grasshopper solve or bidirectional workflow.

Studio v1 bytes and all Architecture runtime/deployment files are checked against pre-task Git blob hashes during consolidation. WikiHouse source meshes and source bundles remain unchanged. Post-cleanup checks and final commit mapping are recorded in project/CURRENT_STATE.md and the Drive baseline manifest.

## Limits

No structural capacity, fastener resistance, diaphragm/racking resistance, construction tolerance, fire rating, U-value, condensation resistance, ventilation performance, approval or safe erection claim follows from these results. The independent frame has no completed openings or weatherproof roof. WikiHouse's existing end-wall/opening holds and source-Brep warning remain in effect.


## Connection-study revision — 24 September 2026

See [CONNECTION_ALTERNATIVES.md](CONNECTION_ALTERNATIVES.md) for seven original, research-linked detail studies, review limits and the physical-validation brief. Generic plate envelopes and fastening zones are now inspectable; capacities, products and fastening schedules remain unassigned. This supersedes only the earlier description of the connection viewer, not the engineering holds.


## Revision R90 — geometric failure resolution

The original 45 mm receiving members and failed screw positions remain available as **Original**. The inspector defaults to **Revised** and **Full joint · no cut**. A separate Cutaway view reveals the screw; full view retains the complete cross-section but still crops long members around the joint. Neither view changes the measured source geometry.

The revised generator replaces the side-wall terminal studs with single 90 × 195 mm sections and the slab perimeter rims with single 90 × 220 mm sections. These are original proposed solid sections, not two sistered 45 mm members assumed to act as one. Member grade, availability, moisture and full technical-assessment applicability remain to be specified. Internal cassette seam members remain 45 mm. Adjacent blocking and tall-wall backing are shortened to avoid overlap. Exterior dimensions, plate depth/thickness and cassette pitch are unchanged; local insulation space is reduced.

| Position | Original nearest edge | Revised nearest edge | Screen | Receiver penetration / thread envelope |
|---|---:|---:|---:|---:|
| Corner return, HBS580 | 22.5 mm | 45 mm | ≥35 mm | 35 / 35 mm |
| Wall–floor, HBS5120 | 22.5 mm | 45 mm | ≥35 mm | 57 / 57 mm |
| Wall–roof, HBS5120 | 22.5 mm | 45 mm | ≥35 mm | 75 / 60 mm |

The screw line moves to the centre of the widened receiver. The manufacturer-based conditional end/edge limits remain 60/35 mm; they have not been weakened to turn a failure into a pass. This yields 10 mm nominal edge-distance margin, not an approved installation tolerance. The 18 mm floor deck remains excluded from timber embedment. No new screw size or unverified longer fastener is introduced.

Verification covers 32 original/revised assemblies (1–8 bays at two heights), positive-volume clash checks, and 800 revised corner/perimeter position checks including all four corners, both side walls and both end walls. These checks resolve the previously identified nominal edge-distance failures. They do not determine connection strength, screw quantity, group spacing, uplift, head pull-through, diaphragm resistance, full assembly sequence, fire, moisture, foundation hold-downs or compliance. A full ETA review, project loads and member/material specifications are needed for those decisions. **Capacity and fastening schedule remain null.**

The generator exposes `connectionRevision: 'revised'`; the System inspector has an explicit geometry selector and exports the chosen revision. API default and Studio's saved source pin remain unchanged to avoid silently changing its assembly. The seven paper-led plate concepts are separate alternatives; they are not the geometry used for these corrected screw studies.

Evidence: Rothoblaas HBS technical sheet, printed pages 32–34 / PDF pages 3–5, rechecked 24 September 2026. The revised sections and positions are OBTP design responses to that screen, not details reproduced from a research paper. Research references and their limits remain in CONNECTION_ALTERNATIVES.md. Next engineering work is load-based connection/anchorage design, followed by local and assembly testing; more green software checks cannot replace it.


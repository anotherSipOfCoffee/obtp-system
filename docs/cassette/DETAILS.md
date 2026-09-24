# Cassette connection details — 24 September 2026

## Revision R90 — geometric failure resolution

The original 45 mm receiving members and failed screw positions remain available as **Original**. The inspector defaults to **Revised** and **Full joint · no cut**. The website shows complete cross-sections only, with separation for inspection; long members remain cropped around the local joint. The owner requested removal of cut preview. Measurements continue to use complete source members.

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

## Original studies and retained comparison

System now has six inspectable local connection studies at `dist/cassette/details/index.html`. They extract real members from the two-bay, 2,100 mm cassette generator. No copied or independently redrawn cassette dimensions are used for the measurements. Studio is deliberately unchanged until connection development advances.

Each view shows one representative fastener envelope, the two receiving timber members and any intervening deck. Member separation aids inspection; the current UI retains full cross-sections. The measured distances always use the complete source members, not the cropped display. An inspection JSON export includes the source member IDs, product candidate, assumed grain directions, measured checks and explicit null resistance/schedule fields. It is not a fabrication or Rhino manufacturing export.

**One visible screw is a position probe, not the required screw quantity.** No repeated spacing, capacity or tolerance is supplied. This advances geometry/detail inspection beyond touching cassette boxes, but it is not an engineered connection release.

## Source and representation

[Rothoblaas HBS technical sheet](https://www.rothoblaas.com/attachments/288905-product-241/hbs-en-technical-data-sheet.pdf), printed pp. 32–34 / PDF pp. 3–5, visually reviewed 24 September 2026. HBS580: 5 × 80 mm, 40 mm threaded portion. HBS5120: 5 × 120 mm, 60 mm threaded portion. Both use the listed 10 mm head, 3.1 mm head thickness and 3.65 mm shank. The pre-drilled shear tables give the selected 5 mm screw a 60 mm loaded-end distance at 0° and 35 mm loaded-edge distance at 90°, under the stated density condition. The complete ETA was not reviewed.

Models are original analytical envelopes based on published dimensions, not manufacturer CAD. The head is simplified, threads are represented by their outside envelope, and the cutting tip/drive recess are omitted. Envelope overlap includes the undetailed tip and **must not be used as effective design penetration**. No product drawing, logo, proprietary manufacturing geometry or assessed capacity is reproduced. Manufacturer rights remain reserved; no licence to manufacture the screw is inferred. Source-byte SHA-256 and review scope are in `DETAIL_SOURCES.json`.

## Explicit assumptions and limited screen

The proposal assumes solid softwood, characteristic density no greater than 420 kg/m³, pre-drilling, and grain following each member's long axis. Those material and installation choices are not yet confirmed. The UI screens both members for the limiting loaded end/edge distances at the tabulated 0°/90° shear directions, treating either end/edge as potentially loaded under reversal. This is deliberately a limited screening case, not a claim about all load angles or the actual building forces.

Passing it does not establish withdrawal, lateral capacity, combined-action resistance, group behaviour, splitting resistance, minimum member-thickness applicability, fire performance, durability, installation access or a complete ETA-compliant design. The floor deck interlayer requires separate applicability assessment. No washers, holes or gaps are silently added.

## Results from actual nominal members

| Detail | Candidate | Receiver penetration / thread-envelope overlap | Result of selected distance screen |
|---|---|---|---|
| Wall seam | HBS580 across paired studs | 35 / 35 mm | Conditional pass; no strength or seam schedule established |
| Floor seam | HBS580 across paired edge joists | 35 / 35 mm | Conditional pass; deck diaphragm transfer remains unresolved |
| Roof seam | HBS580 across paired edge joists | 35 / 35 mm | Conditional pass; roof uplift remains unresolved |
| Corner | HBS580 from return stud into side-wall stud | 35 / 35 mm | Reject: 22.5 mm nearest edge is below 35 mm |
| Wall–floor | HBS5120 through bottom plate and 18 mm deck into rim | 57 / 57 mm | Reject: 22.5 mm nearest edge is below 35 mm |
| Wall–roof | HBS5120 upward through top plate into roof rim | 75 / 60 mm | Reject: 22.5 mm nearest edge is below 35 mm |

The rejection concerns these candidate positions under the stated reversible-shear screen. It does **not** prove that every screwed connection to a 45 mm member is impossible. Alternative load paths, products or assessed installation conditions may change the result; they require their own evidence.

Head locations are OBTP study choices, not positions taken from a manufacturer installation design. The floor seam is inspected at midspan and the wall seam at midheight; these probes do not establish whole-member or diaphragm performance. Cavity driver access has not been swept against a real drill/bit envelope. Drawing a centreline into timber is insufficient evidence of safe assembly.

## What must change before advancing the rejected details

1. Establish actions and load directions. If shear reverses across grain as screened, the current 45 mm narrow dimension cannot provide 35 mm to both loaded edges. Merely moving the screw cannot fix it. The mathematical 70 mm minimum face width for this screen is **not** a recommended member size or a released redesign.
2. Compare a purpose-designed local blocking/terminal member and a separately assessed bracket arrangement. Any widened member must fit insulation and adjoining cassettes and have its own force-transfer design. Two touching pieces must not be treated automatically as one wide solid member.
3. Keep uplift/overturning anchorage separate from a convenient plate screw. The support/foundation, anchor, terminal post and floor path all need definition. The previously shortlisted WHT arrangement still has an unresolved dimensional/application fit.
4. Prototype the candidate seam with actual stock and tools; verify accessible installation, damage, disassembly and moisture-conditioned fit. An engineer must establish test loads, specimen count and acceptance criteria before physical strength testing.

The [Simpson ABR technical sheet](https://pim.strongtie.eu/api/v1/public/download/gb/en/product/260/ABR.pdf) was also visually checked. Its published overall dimensions do not provide all hole coordinates, the assessment applicability or a validated placement in our cassette. No approximate hole pattern or installed ABR was invented. Detailed bracket selection remains open.

## Software verification and limits

`tests/connection-details.cjs` checks all six independent penetration expectations, excludes the deck from rim embedment, checks rejected edge positions, validates finite envelope meshes and confirms cutaway does not alter measured data. Its shortened-screw perturbation must reduce computed penetration. Browser checks exercise all six views, separation/reset, JSON export and mobile layout. The UI has no cut-preview control. Existing cassette and WikiHouse regressions remain required.

These are **geometry and UI tests only**. No connections have been physically tested by OBTP. Any Studio source-pin update must be deliberate and tested. Never publish this development work as a construction-ready kit. R90 addresses the recorded corner/bearing distance failures; product-specific resistance, fastening and anchorage design still require engineering and prototype verification.


## Paper-led alternatives follow-up

[CONNECTION_ALTERNATIVES.md](CONNECTION_ALTERNATIVES.md) adds six research sources and seven original mechanism studies. The existing product candidates, measured probes and failed distance checks remain authoritative for those tested geometric positions. Alternative plate envelopes are not assessed hardware or proof of a resolved connection.


## Unified inspection UI
See [INSPECTION.md](INSPECTION.md). Measured probes are now available inside Connections alongside actual interfaces and separately labelled research alternatives. Historical Original failures below remain comparison evidence, not unresolved R90 distance failures.

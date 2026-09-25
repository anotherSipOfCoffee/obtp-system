# R17 — openings, wall connectors and partition support

25 September 2026. Original OBTP design-development geometry, not a structural or fabrication release.

## What changed

Panels are visible by default. Wall object inspection adds four **angle concept envelopes** at the actual internal stud–plate corners. Each angle is one mesh with two legs; explosion moves it as one item. Source framing and its dimensions remain unchanged. These are the previously documented A07 mechanism, not assessed commercial hardware. No holes, fastening schedule or capacity is assigned. The plywood fastening schedule and seam/anchorage design remain outstanding.

The System review dialog now has door, window and partition-support views. These are deliberately separate from automatically generated buildings pending reconciliation of the owner's plans with the shell.

The opening object spans 1,200 mm (two 600 mm bays), uses the System 195 mm depth and 2,100 mm height, and contains full-height king studs, bearing jack studs, lintel and top plate. The rough opening is 1,020 mm wide, with head 1,900 mm and window sill 900 mm. The door review includes a generic gray frame and outward-open leaf. No structural member or panel crosses the aperture. Lintel section, clear opening after a selected door product, racking, connections, weathering and threshold are not verified. These dimensions are a review proposal, not silently applied to an owner's door.

## Partition proposal

Keep room boundaries independent of cassette seams. A lightweight non-load-bearing partition can be coordinated with additional framing beneath its sole plate. The review shows a 90 mm framing line at X=1,500 mm, running perpendicular to the long floor joists. Full-depth backing fills each cavity beneath that line and terminates at the existing long joists. Existing cross-members are reused where present: the algorithm subtracts their footprints before generating new backing, avoiding doubled timber and collisions. The continuous long joists are not cut or spliced.

This resolves geometric bearing in the displayed direction only. It does not establish floor/joist resistance to partition line loads, backing-end fastening, fire/moisture finish buildup or roof deflection allowance. Partitions parallel to long joists need a separately checked trimmer/joist arrangement; this API does not pretend to solve both directions. The 90 mm section is nominal framing only, not a finished sauna enclosure. No approved room boundary was moved.

## Primary-source review

- [WikiHouse block guide](https://www.wikihouse.cc/design/wikihouse-blocks), accessed 2026-09-25: describes half ties around openings. Its surrounding descriptions concern other series as well; it does not establish the precise pinned 150-family socket placement. The earlier full-tie jamb-clash trials remain rejected. Next WikiHouse work is a rigid half-tie placement/clearance audit against the pinned W-O-S files, not copying a Cassette lintel into WikiHouse.
- [WikiHouse structural guide](https://www.wikihouse.cc/design/how-the-structure-works), accessed 2026-09-25: openings in its external structural walls require lintels/supporting elements, and solid wall blocks contribute to stability. The general guide is not a verified assembly instruction for our pinned opening CAD.
- [APA technical note description](https://www.apawood.org/guides-tools-training/technical-document-library/technical-notes/non-load-bearing-partitions-on-apa-structural-panels-and-floor-joists/), accessed 2026-09-25: rated panels can support certain nonbearing partitions without extra blocking under defined loads. Only the public description was reviewed; its numerical conditions were not verified or transferred to OBTP's unspecified plywood. Therefore this proposal does not assume the deck alone can carry the partition.
- [Simpson PWR](https://www.strongtie.co.uk/en-UK/products/partition-wall-restraint-pwr), accessed 2026-09-25: a slotted restraint accommodates joist deflection above nonbearing partitions. This supports separating top restraint from vertical load bearing. It does not select this product or its installation dimensions for a sauna partition/roof connection.

## Tests and scope

`tests/development.cjs` checks clear apertures, no timber duplication, door joinery presence, partition bearing coverage at six axes (including partial overlap with existing blocking), unchanged source wall geometry and four angle envelopes without penetration of timber/panels. It runs through `tests/foundation.cjs` in existing workflows. Browser checks exercise all three review dialogs and exploded wall connectors. Software checks are not capacity, thermal, fire or installation tests.

The Studio source drawings remain authoritative room layouts. The previous generated shell is 4,572 mm wide, while those drawings are around 2,000 mm deep. An agreed narrow floor/roof cassette adaptation is needed before doors or partitions can be installed in the correct six Sauna models. R17 does not silently choose a new footprint.

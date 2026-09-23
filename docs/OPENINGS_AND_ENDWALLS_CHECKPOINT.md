# Openings and end-wall checkpoint — 2026-09-23

## Owner instruction
Automatic placement and structural openings only were selected. The owner then required precise WikiHouse opening instructions before finishing the configurator. Openings are therefore ON HOLD: no window/door controls, no inferred manufacturing details, no new sockets, no transplanted generic joints.

## Sources examined
Pinned official Skylark commit 6581cc1de0f4daef81a6b5c5a2eaed3c537d1d8f: README, current source tree, W-O-S-1 through W-O-S-5 CAD and corner/end-wall candidates. The examined pinned tree provides CAD/CNC and terms files but no opening assembly PDF. The current website's general assembly page discusses v0.2.2 and 200/250-series details; it does not establish the exact 150 jamb connection for these files.
- https://www.wikihouse.cc/assembly/wikihouse-assembly
- https://www.wikihouse.cc/blocks
- https://community.wikihouse.cc/t/skylark-v1-0-150-bow-tie-clearance-clash-on-floor-end-blocks/1492

No claim is made that precise instructions do not exist elsewhere. They have not been verified for this pinned opening family.

## Opening observations — not accepted placement rules
The 2240 mm W-O-S-1 envelope includes two raised internal header pieces; its main wall interfaces align at 2100 mm. Bounding height alone was insufficient to rule out placement. Sampled two-bay floor/roof intersections at eleven depths showed small tessellated overlaps (maximum about 2.30 mm²). A W-O-S-4 rigid trial similarly showed under 1.87 mm² in these sections.
However, transplanting standard full wall ties at all six side levels clashes with window jambs above the sill and door jambs at all tested side levels (about 2434 mm² section overlap). These are rejected trials, not a working opening system. No source parts have been edited.

## End walls — unresolved
Source end-floor E-S was examined with seven perpendicular W-S blocks. Existing end-floor wall sockets were sampled, with up to 3.08 mm² overlap at inner-face samples. Source E-S contains small placement offsets retained in the CAD.
Several C-S-1/C-S-2 orientations were tested at the perpendicular wall/corner interface. Standard full wall ties clashed substantially; the tested layout in EXTENDED_INTERFACE_AUDIT.json reaches 3750.47 mm². Other orientation trials were also rejected. Do not enable end-wall closure from these candidates.
The official forum discussion explains placing end-floor vertical ties before fitting removable deck tops. This is installation-sequence evidence, not validation of our corner trial. Roof verge/end termination remains unresolved.

## Completed independently
Floor/floor and roof/roof source seam sockets passed the 52 sampled tie-depth checks. They are integrated separately; see SEAM_CONNECTIONS.md. Neither openings nor end closure is marked complete.

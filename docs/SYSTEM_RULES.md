# System study 02 — frame + panels

Decision: independent frame + non-load-bearing enclosure. No suppliers in this stage. Studio and Architecture are unchanged and do not depend on this system.

## Count correction
The earlier proposed list was labelled nine but sums to eight: one post, two beams, one floor, three walls, one roof. No extra object is introduced to meet an incorrect count.

## Provisional geometric rules
- All code units metres; display dimensions millimetres.
- Setting-out coordination 600 mm. Panel/cassette repeat 1200 mm.
- Bay axes 3600 by 2400 mm. Two bays repeat along the 3600 direction.
- Grid is a design hypothesis, not a researched universal optimum or manufacturing specification.
- post01: 160 x 160 x 2400 mm, base z240, top z2640.
- beam01: 2560 x 160 x 320 mm. Transverse, extends 80 mm beyond outer post axes; lower face z2640.
- beam02: 3440 x 160 x 320 mm. Longitudinal, between transverse beam faces. Unsupported until its end connection is designed; geometric fit does not prove load transfer.
- floor01: 1200 x 2400 x 240 mm. Three per bay. Support system absent.
- wall01/02/03: outer envelope 1200 x 180 x 2400 mm, base z240. Window 900 x 1200 at sill900; door 900 x 2100. No frame/glass or thermal layers invented.
- roof01: 1200 x 2560 x 200 mm, base z2960. Flat schematic envelope, no drainage design or claimed cassette capacity.
- Global assembly axes X bay repetition, Y width, Z up. Object dimensions and rotations are explicit in kit.js. No arbitrary resizing.
- Tolerances: not specified. Zero-clearance nominal contacts are geometric placeholders, not fabrication instructions.
- Two-bay assembly shares central posts and transverse beam; no internal enclosure panel. Full assembly: 24 instances for one bay; 41 for two.

## Interfaces
Post/transverse beam; transverse/longitudinal beam; frame/enclosure; floor/wall; beam/roof; adjacent wall panels. Each is a named alignment rule with unresolved connection work. A listed pairing is conceptually intended, not structurally approved. Other pairings are unassessed, not automatically allowed.

## Assembly sequence represented in UI
Frame -> floor -> walls -> roof is a display sequence, not validated site erection guidance. Temporary bracing, access, lifting weights and safe assembly sequence remain unresolved. Exploded view is explanatory displacement only.

## Visible unresolved requirements
Foundations and floor supports; lateral bracing; beam-end support; fasteners; intermediate wall rails; corner closures; floor-to-wall/threshold 80 mm gap; roof perimeter; roof drainage; weatherproofing; 320 mm band above wall panels; material properties, structural spans, fire/thermal/acoustic performance; tolerances and disassembly access.

## Research basis and boundary
Interface rules informed by Nijs et al. (2010), https://research.utwente.nl/en/publications/interface-design-for-open-systems-building-2/
Testing reuse across assemblies informed by Brütting et al. (2021), https://doi.org/10.1016/j.autcon.2021.103614
Separating stable platform from variation informed by Veenstra et al. (2006), https://doi.org/10.1007/s00163-006-0022-6
Single component dataset/configurator direction informed by Cao et al. (2021), https://doi.org/10.1016/j.autcon.2020.103437
These sources do not validate the dimensions or performance of this kit. All current geometry is original schematic code. No WikiHouse part files copied.

## Checks
Run node tests/kit.cjs. Checks library size, instance counts, shared frame, opening voids, numeric geometry and positive-volume clashes. Does not establish supported load paths, continuous enclosure, engineering safety or browser visual correctness.

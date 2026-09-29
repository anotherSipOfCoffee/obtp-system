# R25 validation — 28 September 2026

- Complete portable suite: 102 tests passed (197.967 seconds), including the historical geometry screen (106 accepted cases, 2 rejected). Two additional tests were added afterwards; the final 7-test Custom suite passes, including frozen-baseline and structural/opening clashes.
- Frozen R24.1 comparison: all six saved presets × both roof settings retain exact geometry and drawing hashes from b7508ea4048fc01d1af4bd3f380e5c6779226552.
- Supported indoor programme selections and every enumerated default strip order generate matching room dimensions. Solid partitions remain solid without a passage edge; disconnected rooms receive exterior entrances.
- Five representative new configurations: no timber/plywood intersections or framing intrusion into openings. Window envelopes retain 10 mm modelled gaps; this is not manufacturer acceptance.
- Four complete portable 3DM exports reopened with all objects valid and solid: sauna_only 920, sauna_outdoor 1306, reversed 1862, separate_entries 1848. These are complete physical-piece counts including cladding, not manufactured-type reduction claims.
- Connected-wall erection preserves canonical parts/IDs and ends with cladding. Preview groups remain uncertified for lifting.
- Visual review: standalone plan, reversed plan and structural axon inspected. Internal door-swing diagram corrected towards entrance. The new back-wall window convention and bench/glazing usability remain explicit review issues.
- Generated review assets are included in the ZIP; regenerate locally with EXPORT_CUSTOM_REVIEW.py. Large generated binaries/images are not stored in Git.
- Native Rhino/Grasshopper component creation, interactive controls/materials and native exports remain untested. No Rhino licence/runtime is available here.

No website changes or deployment. Outdoor-only and non-strip layouts remain unsupported. Structural capacity, connections, supplier compatibility, clear passage, wet areas and lifting remain unresolved.

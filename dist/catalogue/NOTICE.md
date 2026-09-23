# Source geometry attribution
WikiHouse Skylark, by the WikiHouse team at Open Systems Lab.
Source repository: https://github.com/wikihouseproject/Skylark
Pinned commit: 6581cc1de0f4daef81a6b5c5a2eaed3c537d1d8f
Source paths and Git blob hashes are embedded in every model packet and recorded in docs/CATALOGUE_SOURCE_LOCK.json.

Source and derived geometry: Creative Commons Attribution-ShareAlike 4.0 International.
https://creativecommons.org/licenses/by-sa/4.0/
Terms: https://www.wikihouse.cc/terms
OBTP is not endorsed by WikiHouse or Open Systems Lab.

OBTP conversion, 2026-09-23:
- CAD: extracted original cached render meshes; applied nested source-instance transforms; triangulated quads, corrected reflected winding and welded coordinates rounded to six decimal places in mm. Original Brep IDs and instance paths retained. No source CAD resizing or silent repair.
- Ties: official TIES.dxf entity 4B1 (full) and 142F (half). Curved cutter profiles flattened at 0.01 mm and extruded to the source 18 mm stock with source 9 mm pockets. The DXF unit flag is unset; mm are inferred from the 2440 × 1220 × 18 sheet layer and source manufacturing notes. This is an OBTP display reconstruction, not an official 3dm tie or new manufacturing output.
- Display labels, colours, camera, exploded offsets and chassis-instance placements are OBTP additions. Exploded movement is not an assembly sequence.

The source CNC folder states that tolerance offsets and dog-bones are already applied. Do not generate CNC instructions from these display meshes or add allowances blindly. The sampled section checks are not manufacturing tolerance or structural verification.
One R-S Brep is open in the source. It is retained and flagged. E-S retains nested definition names E-M from its source file. W-O-S-1 is 2240 mm tall and is not resized to the 2100 mm W-S module.

This notice applies to imported and derived geometry, not unrelated application code.

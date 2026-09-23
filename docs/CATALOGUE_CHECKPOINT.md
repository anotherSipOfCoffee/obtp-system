# Catalogue and connection checkpoint — 2026-09-23

## Corrected interpretation
The previous interface was useful. The user requested the same Types → Objects → Connections → Assemblies structure with real WikiHouse geometry replacing generic objects. The main page now restores that structure and visual style.

## Imported objects
| Type | Object | Source parts | Use |
|---|---|---:|---|
| Walls | W-S | 7 | Chassis slice |
| Walls | C-S-1 | 7 | Corner inspection; placement pending |
| Beams | E-S | 33 instances | End-floor beam; placement pending |
| Floors | F-S | 25 | Chassis slice |
| Openings | W-O-S-1 | 13 | Opening inspection; source height differs |
| Roofs | R-S | 18 | Chassis slice; one open source Brep flagged |
| Connectors | TIE-FULL | 1 | Source-profile reconstruction and interface checks |
| Connectors | TIE-HALF | 1 | Source-profile reconstruction; not placed |

All original CAD files were collected by the GitHub-plugin-triggered Import pinned WikiHouse CAD workflow from the pinned official commit. Their Git blob hashes match CATALOGUE_SOURCE_LOCK.json. Saved render meshes were extracted locally with rhino3dm. All CAD geometry is valid; one R-S Brep is not solid. Repeated E-S definition objects are distinguished by instancePath, not mistaken for duplicate scene objects.

## Intended compatibility and placement evidence
Pinned README describes ties at the floor/wall interface and integrated corner blocks. Pinned WikiHouse_SKYLARK_assembly_axo.png depicts the overall block/tie arrangement. The older website guide still discusses 200/250, so its dimensions and connector quantities were not applied to this 150 release.
The actual 150 CAD sockets establish the displayed placement:
- F-S deck datum 380 mm above the chosen slice origin.
- W-S height 2100 mm; roof bearing datum 2480 mm.
- Source module 600 mm wide and 4572 mm end-to-end. Opposing wall footprints occupy the first and last 186 mm.
- Three vertical ties per face at X=105.1, 300 and 494.9 mm. Both floor and roof levels, both faces, both ends: 24 full ties.
- The separate wall/wall example uses a 600 mm pitch and source side-socket centres at Z=195.547, 404.453, 795.547, 1004.453, 1395.547 and 1604.453 mm, on both faces.

These are OBTP rigid placement transforms inferred and checked from source CAD, not a downloaded official chassis assembly. No source shapes were changed. Exploded offsets are viewing aids.

## Geometric checks
BLOCK_INTERFACE_FIT_CHECK.json contains 48 sampled section intersections at both tie depth levels, all three positions, both faces and both ends for floor/wall and wall/roof. Largest tie/material overlap is 0.695739 mm². Wall/wall representative section check is in WALL_TIE_FIT_CHECK.json. Small nonzero overlap is reported, not erased; these are tessellated-profile checks, not proof of clearance or fabrication tolerance.
Brep topology vertex bounds can miss curved extrema; larger bounds deltas in the audit are not treated as surface deviations. Cached render meshes are not remeshed or treated as authoritative manufacturing geometry.

## Source caveats
- R-S Brep c28a72b3-0a0a-4405-a312-5205f33668e4 is open in the supplied source.
- E-S file contains nested E-M definition names; filename, IDs and hashes are preserved.
- W-O-S-1 is 2240 mm tall versus 2100 mm for W-S, so it is not forced into this slice.
- Tie DXF units flag is unset; the source sheet layer and notes establish the mm stock interpretation. The full/half tie display reconstruction uses source 18 mm thickness and 9 mm pockets, and 0.01 mm curve tessellation.

## Validation
Run node tests/catalogue.cjs. GitHub workflow Check System catalogue passed on commit af10fefa98e34eac60682bfc2c9f513b854a8279 (run 35890259122). Six type selections, three interfaces, the 28-instance slice, exploded view, stages, mobile overflow and WebGL status passed with no page errors. Desktop assembly, connection, exploded and mobile screenshots were inspected. See BROWSER_CHECK_REPORT.json. Rhino 8 interactive checks, complete surface deviation, complete collision analysis, construction sequence and project engineering are not completed.
The current assembly is an open slice, not an enclosed or laterally stable building. End walls, corners, foundation interfaces and bracing remain next work. Studio, Architecture and Drive v74 are unchanged.

## Reproduce
Install tools/requirements-catalogue.txt. Obtain the selected official CAD through the Import pinned WikiHouse CAD workflow. Place the extracted artifact at source-cad/official; run tools/export_catalogue.py source-cad/official, tools/export_ties.py, then tools/check_interfaces.py. No official source CAD is silently rewritten.

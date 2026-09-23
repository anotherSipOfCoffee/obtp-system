# System direction — preserve interface, replace geometry
The owner's clarified instruction is to retain the useful Types → Objects → Connections → Assemblies interface. Generic members should progressively be replaced by official WikiHouse objects, not by a new single-object interface. Do not repeat that misunderstanding.

## Source and roles
Use WikiHouse Skylark150 from commit 6581cc1de0f4daef81a6b5c5a2eaed3c537d1d8f. Current import: W-S, C-S-1, E-S, F-S, W-O-S-1, R-S and full/half ties derived from the same release's TIES.dxf. See CATALOGUE_SOURCE_LOCK.json, CATALOGUE_GEOMETRY_AUDIT.json, and CATALOGUE_CHECKPOINT.md.
Preserve source IDs, shape and scale. Never transplant joints into generic geometry or mix release generations. Types reflect source roles: wall/corner blocks, end-floor beams, floor cassettes, openings, roof cassettes and ties. Do not invent a standalone post to fill the previous generic Posts category.

## Connections and assemblies
The pinned README explicitly describes floor–wall ties, removable beam tops and integrated corners. The pinned assembly axonometric depicts wall, floor and roof blocks joined by ties. The browser's connections use actual source socket geometry and source tie profiles.
Display a one-module open chassis slice: F-S + two W-S + R-S + 24 full ties. Placement uses only rigid transforms. 48 sampled floor/wall and wall/roof sections show less than 0.7 mm² profile overlap; this is not a full volume, strength, fabrication tolerance or assembly-access check.
Do not call this a complete building or assume end walls, foundation rails, lateral bracing or services are resolved. Corner, end-floor and opening objects are available but not yet placed into this slice. Do not force W-O-S-1 (2240 mm source height) into a W-S (2100 mm) slot.

## Geometry limitations
One R-S source Brep is valid but open, ID c28a72b3-0a0a-4405-a312-5205f33668e4. Retain and flag it; do not silently repair it or claim all imported CAD is closed.
Tie meshes are display reconstructions from official CNC profiles, not official 3dm solids. The source supplies 18 mm stock and 9 mm pockets, with tolerances already applied. Do not export new manufacturing files from the web derivative.
Rhino 8 Windows remains the target CAD environment; rhino3dm extraction is not Rhino execution. Existing offline asset/instance workflow is retained. New wrappers are OBTP code, not official GH definitions.

## Scope and archive
The generic-frame study remains at archive/independent-frame-v02, commit f284e74548bc68d81bc5d2b8995ba153d52ba117. Its UI structure is reused; old dimensions, joints and building arrangement are superseded.
Studio and Architecture stay unchanged. GitHub operations use the GitHub plugin only. Update Drive only when requested. Preserve CC BY-SA 4.0 geometry attribution and source notices; no WikiHouse endorsement implied.

## Repeated assembly extension
Studio is now explicitly authorized to consume the shared System implementation. See REPEATED_ASSEMBLY.md for the 1–8-module open row and reuse of the wall/wall connection. Floor and roof seam fastening remains unresolved. The original single slice remains the one-module case.

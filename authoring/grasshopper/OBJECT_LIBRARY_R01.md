# Linked object library R01

Owner authorization: 2026-09-26, research and implement an Archicad-like linked library; door first following recommendation. This is an incremental implementation in the existing Cassette pipeline, not a replacement generator or native GDL interpreter. No new paid dependency.

## Research and decision

Graphisoft defines a library part as parameters, 3D model, 2D representation and identity/revision. This is the useful pattern to adopt. Graphisoft's own documentation recommends parametric representations over static 2D elements. Rhino 8 Grasshopper provides block definitions/instances and retains object attributes. A Rhino block alone does not implement OBTP's product compatibility, shared parameter validation or drawing representation selection.

Primary sources checked 2026-09-26:
- https://gdl.graphisoft.com/gdl-basics/components-of-a-libpart/
- https://gdl.graphisoft.com/reference-guide/scripting/
- https://www.rhino3d.com/en/features/grasshopper/blocks/
- https://developer.rhino3d.com/samples/rhinocommon/create-block-definition/

Decision: portable Python object definitions supply geometry and drawing representations to the existing GH component. Keep Rhino geometry export compatible with per-part analysis/explosion. Native block baking is a possible later adapter, not claimed implemented here. No verified native GDL execution or lossless GSM import into Rhino was established; do not promise either. ProdLib/manufacturer assets can be accepted individually only with documented units, insertion axes, dimensions, source revision and redistribution permission. Do not copy Archicad's proprietary library.

## Implemented contract

`obtp/object_library.py` owns pinned definition keys/revisions and the door coordination recipe. `model.wall_run` calls that recipe using the same width, height and wall depth used by the structural opening. The host still owns the aperture, framing and lintel. Existing physical part IDs, geometry, dimensions and quantities are preserved.

After model resolution, `scene.object_library` contains:
- definitions with status, supplier selection and representation methods;
- placed instances with stable semantic IDs, part IDs, host opening ID for doors, placement and shared dimensions;
- library fingerprint and original DXF source checksum.

Door plan symbols resolve through these instances; drawing records preserve instance/part IDs and the library fingerprint. Sections continue to intersect actual detailed geometry. 3DM part attributes include object ID, definition, revision and fingerprint. Grasshopper reloads the library alongside the model and reports instance count. Existing source package creation includes the new Python module automatically.

Other object/furniture assemblies become explicit placeholders, retaining their existing generated geometry and projected plan. There is no automatic supplier substitution or invented manufacturer fidelity. Window parts form one slot. Interior sauna benches remain actual model projections: the supplied Outdoor Bench symbol is not misrepresented as an interior bench.

## Current door limitations

Door R1 preserves inherited generic joinery dimensions (30mm jamb/head, 35mm leaf) and the existing DXF Door Lining symbol. These are coordination geometry, not researched supplier dimensions. The symbol is an opening-width-based swing diagram; it does not certify clear passage or precisely depict hardware. The closed 3D leaf and open plan swing are explicitly different representation states. Existing orientations are retained, including the Studio left entry. Independent handing/open-angle controls, product substitution, detailed installation joints and scale-specific detail levels are not yet implemented.

To replace a placeholder: create a pinned definition/adapter with evidence; resolve its interfaces against the host; regenerate geometry and linked symbol from shared dimensions; validate before enabling the choice. Unknown definitions/revisions fail closed. Never stretch a supplier asset to fit. A failed product resolution must not be presented as the old valid geometry under a new product name.

## Verification

- Existing 20 portable tests passed, including 102 accepted custom candidates and 6 rejected combinations.
- Three library tests passed: all twelve base configurations' slot coverage/identity, drawing links and deterministic regeneration; changed door dimensions and unknown/stale definition/source rejection; actual 3DM roundtrip metadata.
- All twelve base geometry hashes identical before/after refactor.
- Native Rhino 8/GH execution not available here; native acceptance remains pending. This release adds no solver results or engineering claims. Wind/snow remain paused.

Files: object_library.py, model.py, drawings.py, export.py, components/model.py, tests/test_object_library.py. Website source pin and live deployment are not changed by this library development branch.

# R29 — independently usable room stages

Extract the complete ZIP into one folder. Open a millimetre Rhino document and Grasshopper, then run the desired creator in Rhino's Python 3 ScriptEditor:

| Creator | Definition produced | Inputs and result |
| --- | --- | --- |
| `CREATE_LAYOUT_GRASSHOPPER.py` | Layout only | Room functions, adjacency, boundaries and dimensions → plan |
| `CREATE_STRUCTURE_GRASSHOPPER.py` | Structure only | Imported/live plan, cassette, roof and foundation → skeleton |
| `CREATE_DETAILING_GRASSHOPPER.py` | Detailing only | Imported/live skeleton, terrace, panels and façade → complete model |
| `CREATE_ROOM_CONFIGURATOR.py` | Connected A–B–C workflow | All three stages, assembly preview and model exports |

`CREATE_GRASSHOPPER.py` and `CREATE_RESEARCH_GRASSHOPPER.py` retain their earlier main and research workflows. Unlike R28, CREATE_LAYOUT_GRASSHOPPER now creates only the layout stage. Use CREATE_ROOM_CONFIGURATOR for the previous connected workflow.

## Separate documents

1. Create Layout. Resolve a valid plan. In PLAN / FILE HANDOFF, edit the path if needed, turn **Write current plan** on once, then off.
2. Create Structure. This adds another GH document; the existing definition remains open. In PLAN / FILE HANDOFF, use that path and turn **Read saved plan** on. Change roof/foundation as needed. Export using SKELETON / FILE HANDOFF.
3. Create Detailing. Import the skeleton in the same way. Detail, inspect assembly progress and use the existing complete-model exports. SCENE / FILE HANDOFF additionally saves a validated complete scene.

No imported file is silently overwritten. Export requires live upstream data. Reading occurs on component recomputation: after overwriting a source file, toggle Read off/on to refresh. There is no background file watcher or cross-document live link.

## One canvas

Use the combined creator, or copy the required stage groups between definitions. Wire the prior stage's `data_json` to the next stage's `upstream`, or to its FILE HANDOFF component's `upstream`. Live input takes priority over file reading. Invalid live input clears output rather than falling back to an older file. Do not wire both a direct source and a handoff output into the same item input.

Creators use a shared `room_canvas.py` factory with fresh execution globals on every run. They allocate a new GH document, retain native component GUID allocation and use microsecond-stamped filenames. They do not remove or replace open documents. This is verified in source checks; multiple-open-document behaviour still needs native Rhino acceptance.

## Files you can manage

- Layout logic: `obtp/room_config.py`.
- Structure logic: `obtp/room_structure.py`.
- Detailing logic: `obtp/room_detail.py`.
- Validated import/export: `obtp/room_exchange.py` and `components/config_exchange.py`.
- Shared canvas creation: `room_canvas.py`; each creator explicitly selects its own stage.

Keep the complete extracted package together, with generated GH definitions beside the creators. A creator is not a self-contained single-file distribution; its local modules are bundled in this ZIP. Existing definitions may cache modules until Rhino restarts after manual code edits.

## Validation and limits

18 focused tests passed: 13 existing room configuration tests, four exchange/creator tests and the factory compatibility test. Roundtrips preserve layout, skeleton and complete scene; regenerated structure/detail match the direct workflow. Wrong-stage, corrupted, missing and invalid live inputs are rejected. Original geometry recipes are unchanged, so the R28 engineering and architecture limitations still apply. Hashes verify integrity, not engineering validity.

Native Rhino/Grasshopper is unavailable in this environment. Outstanding: run all creators consecutively with another definition open; inspect canvas placement, file controls, copied component connections, preview materials and assembly slider. No website, Drive or other repository changes; no merge.

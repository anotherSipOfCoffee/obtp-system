# Grasshopper part visibility R09

Adds independent visibility toggles and a Show only selector for roof beams,
roof panels, covering, fascia, facade boards/battens, window frames, glazing,
door frames/leaves, wall framing/sheathing, partitions, floor framing/panels,
insulation, interior/ceiling finishes, terrace framing/boards, foundations and furniture.
Unknown future parts remain visible through Other parts.

Download this branch's complete repository ZIP and extract it. Open a millimetre
Rhino file and Grasshopper, then run authoring/grasshopper/CREATE_GRASSHOPPER.py
in Rhino 8 ScriptEditor using Python 3. If requested, place a Python 3 component
on a blank Grasshopper canvas first. The builder creates a new timestamped
OBTP_Module_Preview_R09 definition; it does not overwrite an existing definition.
Keep the definition beside the obtp and components folders.

Use group C2 for individual visibility. Show only overrides the individual
switches; select All enabled groups to restore them. Show panels and Cut view
remain additional filters; use Show panels=True and Cut view=False for complete
isolated objects. Cut view now defaults to False. Export and analysis continue
to receive the full canonical scene, never the filtered preview.

This update adds isolation tools; it does not claim to repair the user's original
Rhino document. The user reports the same baked geometry displays correctly in
a different document. The original document's display/scene cause is unresolved.

Validation: Python compilation and real-model visibility tests for all six sizes/
storage presets in both programs. Native Rhino/Grasshopper execution remains
pending. Geometry generation, engineering holds and website are unchanged.

Source: GitHub main 65536ab47be61e069224a23d11b5037d75f7f1f6, ahead of the recorded
Drive v76 baseline. This scoped preview change preserves that newer source;
no baseline import, synchronization or website deployment is performed.

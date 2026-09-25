# Canonical Sauna authoring

Owner decision: 25 September 2026.

1. Edit `obtp/model.py` for base geometry and presets; edit `obtp/envelope.py` for finishes/roof/terrace.
2. `CREATE_GRASSHOPPER.py` wires the same core into native Rhino 8 GH. Do not put a separate generator into GH component strings.
3. Run the portable tests and native CHECK_RHINO.py where Rhino is available. Native execution is still pending; browser success cannot substitute for it.
4. `export_web.py <directory> --revision <System commit>` creates the finite website catalogue and source download. No live Rhino/server connection is required.
5. Studio pins the System commit and loads exports. Browser code may select, filter layers, render and inspect. It must not solve layouts or change geometry.
6. Update source, exports, documentation and tests together. Native GH script and web meshes must identify their authoring revision.

R03: terrace depth 600/1200 mm (default1200); window width600/900/1200 (default1200); entrance-side sauna window centred within the hot room, door-aligned top/bottom; facade0 vertical timber only. Roof flat/single/gable retained. Extra GH controls remain custom studies. All models remain engineering review candidates, not manufacturing releases.

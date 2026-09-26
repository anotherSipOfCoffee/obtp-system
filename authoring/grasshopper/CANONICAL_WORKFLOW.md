# Canonical Sauna authoring

Owner decision: 25 September 2026.

1. Edit `obtp/model.py` for base geometry and presets; edit `obtp/envelope.py` for finishes/roof/terrace.
2. `CREATE_GRASSHOPPER.py` wires the same core into native Rhino 8 GH. Do not put a separate generator into GH component strings.
3. Run the portable tests and native CHECK_RHINO.py where Rhino is available. Native execution is still pending; browser success cannot substitute for it.
4. `export_web.py <directory> --revision <System commit>` creates the finite website catalogue and source download. No live Rhino/server connection is required.
5. Studio pins the System commit and loads exports. Browser code may select, filter layers, render and inspect. It must not solve layouts or change geometry.
6. Update source, exports, documentation and tests together. Native GH script and web meshes must identify their authoring revision.

R03: terrace depth 600/1200 mm (default1200); window width600/900/1200 (default1200); entrance-side sauna window centred within the hot room, door-aligned top/bottom; facade0 vertical timber only. Roof flat/single/gable retained. Extra GH controls remain custom studies. All models remain engineering review candidates, not manufacturing releases.

R04: model-derived plan/two sections/window schedule, dimension recipes and A3 PDFs. Native GH export adds Rhino dimensions/layout; native acceptance is still required. Insulation is cavity-fit geometry with a separate envelope specification. Gable top targets 4480 mm from model datum. See RESEARCH_R04.md. Website controls and PDF select the same export key.

R05 supersedes the R03 choices: terrace1200 only; window control is frame width580/880/1180 with10mm fitting allowance each side (opening600/900/1200). Gable has no roof overhang beyond finished facade. Two drawing styles derive from one scene: conceptual merged wall regions for web, material-specific cut geometry for five A3 PDF sheets. No browser PDF embed. See RESEARCH_R05.md.

Analysis A01: `obtp/analysis.py` is the canonical preparation layer; it reads detailed model solids and material sections. `analysis/README.md` records solver research, candidates and unresolved inputs. Never feed the conceptual plan or simplified web mesh into engineering analysis. The GH builder adds six named preparation groups. Dossier sheets 6-8 are diagnostic preparation, not completed solver results. No native GH execution or website publication has occurred for A01.

A02 supplier direction: Cassette remains default (`system_type=0`). Hunton (`system_type=1`) is an unimplemented supplier candidate and must be rejected, never represented by relabelled Cassette geometry. `obtp/suppliers.py` owns product provenance and the system eligibility list. See `suppliers/RESEARCH_A02.md`. Wind/snow status is `paused_by_owner`, never a zero action. Window details are vertical `window-section`, `window-head`, `window-sill`; retired `window-plan`/`window-jamb` must not reappear in PDF. Supplier schedule precedes the three analysis pages, which remain at the end of the dossier.

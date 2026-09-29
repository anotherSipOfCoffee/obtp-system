# GH R21 — measured modularity decision

Baseline: `d02d8322bb1f456e4b005d5f6a023f236eddc220` (R20). Website updates remain paused. No Studio pin, Drive or Architecture changes.

## Result
Retain R20 geometry. Eight modes (baseline plus seven alternatives) were screened on 24 representative configurations. Adapted 900/1200 solids increased fabricated candidate diversity 280→290 while reducing total pieces 30,622→30,514. 600/1200 solids gave 295 types at the same piece total. Relocated 1500/1800 opening-host candidates produced 298–301 fabricated types and 31,170–31,188 pieces. Fixed 1500 hosts failed in 14/24 cases. No candidate improves the requested overall tradeoff. This bounded screen does not prove global optimality.

No reduction is attributed to procurement accounting. Full retained catalogue: 216 configurations, 346 primary candidate types, 281 fabricated candidate types. Geometry hashes and drawings match frozen R20 for all 216. Same footprints, room dimensions and opening positions; physical reduction 0%.

## Implemented
- `obtp.modularity`: five explicit levels (coordination, structural assemblies, manufactured parts, purchased products, interfaces).
- 300 mm candidate coordination increment, independent of 900×1200 planning and actual cut lengths. No new canvas controls.
- Canonical `scene.modularity.openings`: dimensional chains, counted supporting members, supplier evidence and explicit null unknowns. 1180 is the modelled frame outside width, not an approved Pihla product specification.
- Purchased opening units are separately reconciled with their geometric subparts; other equipment/furniture remains unresolved. Original primary counting scope is unchanged.
- Reproducible `modularity_study.py`: screen first; `--full` validates only the retained production finalist against immutable R20.
- GH model component exposes the contract summary. Updated generator creates an R21-named native definition. Existing controls, quantities, preview colours, loose-part schedule and connected wall erection sequence remain intact.

## Run and review
Extract the whole package. Open a millimetre Rhino 8 document and Grasshopper. Run `CREATE_GRASSHOPPER.py` in Rhino's Python 3 ScriptEditor. Open the generated R21 `.gh`. Never copy only one component/module from this package.

`python modularity_study.py DEST` runs the bounded screen. `python modularity_study.py DEST --full` requires the System Git history and compares against the frozen commit. The portable ZIP includes the results; it does not need Git to run the GH model. `python EXPORT_STUDIO_M_PDFS.py DEST` needs ReportLab and emits only default Studio M schedule, parts layout and assembly PDFs.

See `review-r21/OBTP_Modularity_R21.html` for measured comparisons and diagrams; `summary.json` for evidence and baseline hash manifest. Detailed screen/full JSON accompanies the downloadable package.

## Validation / limitations
- 68 Python tests passed, including new dimensional-chain, procurement reconciliation, candidate-isolation and legacy checks. Existing tests exercise solids/export consistency, custom cases, preview stages and wall pivots.
- 216/216 supported configurations match R20 geometry and drawings; no new geometry exceptions.
- Three PDFs regenerated; representative assembly and detached-layout pages visually checked.
- Native Rhino/Grasshopper is unavailable in this cloud environment. Portable rhino3dm checks do not establish native GH acceptance; no pre-generated `.gh` is supplied as if it had been solved here.
- Manufacturer documents verify Harvia's envelope and Swedoor's example size tables, not OBTP compatibility. Harvia installation tolerances, Pihla exact product, thresholds, clear passage and supplier machining remain unresolved.
- Existing 900×1900 generic door aperture does not meet Swedoor's approximate 910×1900 opening. 10×21 also fails available head height. No unverified product substitution or narrowing is adopted.
- No verified capacities, fastening quantities, assembly labour or safe full-wall lifting claim. Existing 537 mm shower niche usability remains unresolved.

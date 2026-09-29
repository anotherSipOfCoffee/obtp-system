# R26 — inspectable cassette workflow

Extract the complete ZIP into a new writable folder. Open Grasshopper, then run `CREATE_GRASSHOPPER.py` with Rhino 8 Python 3. This creates and opens a timestamped `OBTP_Cassette_Checkpoints_R26_*.gh`. Keep it beside `obtp` and `components`. The ZIP contains the creator and all supporting modules; it does not contain a natively tested prebuilt `.gh`.

## Follow the numbered groups from left to right

| Checkpoint | Manage / inspect |
|---|---|
| 01 Preset + parameters | Six Sauna presets, Custom Sauna, six Studio presets. Custom room controls apply only to Custom Sauna. Roof, window, height and foundation controls apply to both programmes. |
| 02 Layout plan | Room geometry, names, proposed openings, relationship diagram, arrangement and validity. No hidden 3D model is generated here. |
| 03 Cassette construction | Authoritative complete model and report. The lower diagnostic component exposes room rows, openings, assembly IDs, part rows and checks. Attach a Panel to the output you need. |
| 04 Assembly sequence | Slider: 0 empty, 100 complete. Current stage and complete step list are visible. Connected walls lie near their erection positions, rotate through the retained erection stages, then stand upright. Cladding is last. |
| 05 Final preview | Structure + panels; building without façade boards; complete with cladding. Optional stable colours by manufactured type. Paste an exact CP3 assembly ID into the isolation Panel; leave it blank to show all. |

The lower export group always uses the full CP3 scene, independently of assembly progress, scope or isolation. Existing model/drawing exports and separate loose-part schedules remain unchanged. The existing export toggle keeps PDF generation disabled. Existing review PDF assets are retained in the package.

## Troubleshooting

Start at the first numbered group with an error. Inspect its report before following downstream wires. Invalid input clears downstream outputs rather than showing a previous successful model. The checkpoint JSON outputs are available for inspection; editing validated JSON manually is deliberately rejected. Manage variants through the preset and parameter controls.

If only some objects appear, set assembly progress to 100, choose Complete and clear the assembly filter. Use CP3 assembly IDs to isolate a suspect assembly, and its opening/check outputs to inspect fit. Type colours are stable across assembly progress and scopes; identities remain provisional wherever manufacturing details are undefined.

Saved Studio presets preserve the existing Studio geometry and zoning. Custom graph rearrangement remains Sauna-only. Studio room labels show coordination-zone dimensions, not certified finished usable room dimensions. The assembly animation is retained display geometry, not a lifting design or a certified prefabricated unit.

## What is grasshopper-research?

`CREATE_RESEARCH_GRASSHOPPER.py` creates a separate comparison definition for the historical WikiHouse system, cassette system and experimental B plate-rib system. It is optional research material, not a dependency of the main cassette workflow. Use `CREATE_GRASSHOPPER.py` for normal work.

## Change and acceptance scope

No construction-system optimization or part reduction is claimed by this release. Changes expose workflow stages and add saved Studio presets while preserving source geometry, quantities and drawings. R24.1's Python component factory fix and R25's Custom Sauna construction remain.

Portable validation covers saved Sauna geometry, saved Studio geometry under both roof options, host input wrappers, display filtering, assembly progression, identity-colour stability, stale-input rejection and export geometry. Native Rhino/Grasshopper execution, actual canvas appearance and interactive performance require a Rhino 8 acceptance run; they cannot be verified in this cloud environment. No website changes or deployments.

# Cassette 01 validation — 23 September 2026

## Saved Phase 1

System: `76106edc9dae6ae711831a87d2d99919e2a84731`.
Studio: `b286ac2ae29d340e44c7115dfa2459f04dd46abd`.
Both are on `dev/obtp-independent-v1-20260923`; no live deployment.

- [System cassette check](https://github.com/anotherSipOfCoffee/obtp-system/actions/runs/35906029424): passed geometry, WikiHouse regression and browser tests.
- [System existing browser check](https://github.com/anotherSipOfCoffee/obtp-system/actions/runs/35906029341): passed.
- [Studio variations check](https://github.com/anotherSipOfCoffee/obtp-studio/actions/runs/35906113085): passed prepared pinned-System build, v1/v2/v3 switching, module counts and existing controls.

Geometry tests cover all N=1…8 at H=2,100 and 2,700: 16 full assemblies, stage counts, finite coordinates, positive-volume intersections between all box parts, continuous end-wall framing, supported nominal sheet envelopes and graph connectivity. All passed. Tests reject unsupported module counts/heights/stages. They operate on exact orthogonal box geometry; they are not physical tolerance tests.

Browser checks cover object and five inter-cassette connection views, module and height controls, skin visibility, layer selection, explode/reset, disabled openings, JSON export, WebGL error status, desktop/mobile and absence of JavaScript page errors. Screenshots were visually inspected. The default frame view is intentional so the cassette construction can be seen.

The four-module export contains 166 part boxes. Using rhino3dm, all were converted to valid closed Breps, written as Rhino 8-format `.3dm` and read back with equal object count. **Windows Rhino 8 and the Rhino ScriptEditor importer were not executed here.** This validates file geometry, not a Grasshopper solve or bidirectional workflow.

Studio v1 bytes and all Architecture runtime/deployment files are checked against pre-task Git blob hashes during consolidation. WikiHouse source meshes and source bundles remain unchanged. Post-cleanup checks and final commit mapping are recorded in project/CURRENT_STATE.md and the Drive baseline manifest.

## Limits

No structural capacity, fastener resistance, diaphragm/racking resistance, construction tolerance, fire rating, U-value, condensation resistance, ventilation performance, approval or safe erection claim follows from these results. The independent frame has no completed openings or weatherproof roof. WikiHouse's existing end-wall/opening holds and source-Brep warning remain in effect.


## Connection-study revision — 24 September 2026

See [CONNECTION_ALTERNATIVES.md](CONNECTION_ALTERNATIVES.md) for seven original, research-linked detail studies, review limits and the physical-validation brief. Generic plate envelopes and fastening zones are now inspectable; capacities, products and fastening schedules remain unassigned. This supersedes only the earlier description of the connection viewer, not the engineering holds.

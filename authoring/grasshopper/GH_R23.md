# R23 — constrained room graph and visible planning stages

28 September 2026. GH-only update. Websites, Studio pin, Drive and Architecture unchanged.

## Run

Extract the complete ZIP to a new folder. In Rhino 8 Python 3, with Grasshopper open, run `CREATE_GRASSHOPPER.py`. It creates a new timestamped R23 definition and keeps older definitions intact. The package contains the generator; native Rhino/GH execution and a pre-generated binary `.gh` were unavailable in the cloud environment.

The existing building and its three-system comparison remain. New groups G–J are below them. Zoom Extents in GH. The room-plan preview is at Y = −7500 mm in Rhino; the small relationship diagram is beside it. Room labels have a separate output/panel; the setup also wires native Text Tag 3D if the installed component exposes its recognised Location/Text inputs.

## Four visible stages

| Stage | Controls | Output |
|---|---|---|
| 06 / Room programme | Include sauna, entrance, outdoor; three lengths in 900 mm cells; depth in 1200 mm cells | Explicit active rooms and dimensional requirements |
| 07 / Relationships | Three pairwise selectors: none, adjacency, internal passage, external access route | Typed graph; inactive-room edges ignored with a note |
| 08 / Constrained floor plan | Arrangement index | Room zones, finished-room/provisional rectangles, passage/entrance reservations, graph preview and JSON contract |
| 09 / Plan to construction | **Use floor plan for construction** | Existing scene, or geometry driven by a compatible resolved plan |

The construction toggle defaults **off** to preserve the existing building controls. Turn it on for the original sauna–entrance order, with or without the terminal outdoor zone. The source selector feeds every original scene consumer: normal preview, assembly stages, schedules, drawings, analysis preparation and the cassette comparison. With the outdoor zone active, matching existing Sauna geometry, IDs and drawings are unchanged; only layout provenance is added. With the whole outdoor zone disabled, the three shower fixture pieces that the older no-storage model still included are omitted at generation. All remaining parts are identical to that existing model; this is a programme change, not an optimization saving.

When active, the plan owns room lengths, depth and storage inclusion. Roof, window, foundation and height come from the original building controls. This first bridge uses the existing 900 mm internal/entrance opening and 90 mm partition. Custom door/partition/bench settings outside this contract are not adopted; use the original model mode for those. The existing complete architectural drawings downstream remain authoritative for windows, wall build-ups, furniture and niche subdivisions. The new coloured room diagram is a planning view, not a replacement detailed construction plan.

## Try these cases

1. Leave all three rooms active, sauna/entrance = internal passage, entrance/outdoor = external access, arrangement 0: reproduces existing Sauna M with storage/outdoor zone. Enable the construction bridge to see its full model.
2. Turn outdoor off: exactly two rooms; the existing Sauna without storage is available for construction output with its outdoor shower fixtures removed. It is not created by hiding the old annex.
3. Turn entrance off: sauna + outdoor plan only. The inactive entrance edges are ignored, not rerouted. Add a sauna/outdoor external-access relationship if wanted. New exterior access and construction topology require a later adapter; no full building is exported.
4. Select another available arrangement: a different feasible strip order appears. These alternatives currently remain plan studies.
5. Set a connection to none: both rooms remain active. Change room activation to remove a room.

The report lists the valid arrangement range. The slider stays 0–5 because at most six permutations exist; an unavailable index produces a clear error and clears the plan instead of silently switching to a different layout.

## What the first solver does—and does not do

It enumerates bounded rectangular strip orders, keeps the mixed outdoor zone terminal, rejects incompatible adjacency graphs, and retains the 900 × 1200 planning grid. “Internal passage” requires shared adjacency; “external access” is a relationship via outside, not a doorway cut through a shared wall. It does not pretend that an edge establishes a compliant accessible route.

Outdoor shower, enclosed storage and seating remain three functions of one current zone. They are not independently resized or omitted yet. The existing narrow shower niche and wet-area/clearance concerns remain explicit. Disconnected rooms and single-room programmes can be explored, but are not declared usable finished buildings.

Construction is currently supported only for the proven sauna + entrance topology in the original order, optionally followed by the existing outdoor/storage zone. Other room sets and orderings deliberately have **PLAN ONLY** status. If selected for construction, they clear the scene output and block downstream exports; they never silently export the previous model. Unsupported room plans need actual walls/openings, envelope, circulation and connection rules before extending that adapter.

This is the first separation of room intent from construction recipes. The existing construction core has not been rewritten into an unrestricted polygon-to-building solver, and no external floor-plan add-on is required. `obtp/layout.py` provides a reusable plain JSON contract for later solvers, but manually editing a resolved contract is rejected until revalidated through this solver.

## Review and validation

`review-r23/review.html` has four labelled diagrams; their JSON is generated from the same solver as GH. `EXPORT_LAYOUT_REVIEW.py` regenerates them without a website build. `tools/package-gh.py` bundles the current source, prior R22 examples, unchanged Studio PDFs and R23 plan review.

Eight focused tests cover all seven nonempty room subsets, feasible alternative orders, explicit activation versus edges, conflicting constraints, invalid inputs, stale-plan rejection, comparison of twelve existing S/M/L × storage × roof cases (exact with outdoor active; only three shower pieces removed when inactive), custom dimensions, source immutability and deterministic output. Existing geometry and export checks remain in CI. Native GH component construction, runtime text-tag availability and slider interaction are not tested here; portable Python checks are not a substitute for that host acceptance.

R22 B remains a separate interpreted plate-rib research concept. It is not a construction system directly supplied or structurally validated by the CompassWood reference, and R23 does not connect new floor plans to that unengineered chassis.

# OBTP current state — v76, 2026-09-23

Independent Cassette 01 is implemented in System and exposed as Studio v3 through the pinned source relationship. It generates a rectangular frame from 1–8 repeating modules, including end-wall framing, with object/connection inspection, stages, exploded view, quantities and nominal Rhino box export. WikiHouse v2 and Studio v1 remain separately accessible. Architecture application files are unchanged.

This is a digital research prototype, not a finished construction kit. Timber sections, plywood, fastening schedules, racking, spans, supports, tolerances, roof drainage, envelope details and Lithuanian requirements need engineering. Openings remain disabled. Research and proposed envelope approach are in docs/cassette/; the rendered report is dist/cassette/research.html.

Phase 1 geometry and both System/Studio browser workflows passed; see docs/cassette/VALIDATION.md. The reference export round-tripped as 166 valid closed Breps in Rhino 8 file format. Windows Rhino/Grasshopper was not run. No bidirectional CAD/web workflow is claimed.

Consolidation removes the embedded v74 backup parts, obsolete old snapshot workflow/request/restoration tools, and misleading duplicate/outdated coordination instructions. Required source bundles, the W-S viewer, useful Rhino pilot, licenses, meshes and intentional data are retained. Drive historical packages are outside the active master. See CLEANUP.md and the master manifest for exact state.

Drive holds the authoritative master baseline. GitHub development branches may be ahead; main/live are intentionally still on the pre-task commits listed in PROJECT_MAP.md. Do not interpret that divergence as a synchronization error. The final Drive receipt is intentionally a later documentation commit than the packaged source if necessary to avoid self-referential commit hashes.

Next useful work: engineering concept review and one physical joint/cassette prototype; Lithuanian envelope/ventilation analysis; reviewed opening details; Windows Rhino 8 inspection. Deployment is a separate decision and was not authorized in this task.

# OBTP v76 — handoff

Completed as a **digital research prototype and consolidated project baseline**. No live website was deployed or modified.

## Inspect the result

- [Drive master](https://drive.google.com/drive/folders/1w4ZBlEJSDoW2iE9MoSV8V_f9AOT2Ja-C)
- [Download local Studio preview](https://drive.google.com/file/d/1B4ojc9qsSJ0RcH2PEIuMRGav9hB82cz5/view?usp=drivesdk). Extract it; OPEN_CASSETTE.html opens the new variation directly. For the full v1/v2/v3 selector, follow START_HERE.txt or OPEN_STUDIO.cmd and open localhost:8765/#v3. This is a local preview, not a hosted site.
- [Illustrated research, specification and Phase 1 validation](https://drive.google.com/file/d/1TWBPSlJnwd6eIdWgeioAzHTHxgyv81_A/view?usp=drivesdk). Download/open the self-contained HTML. [Readable research source](https://github.com/anotherSipOfCoffee/obtp-system/blob/dev/obtp-independent-v1-20260923/docs/cassette/RESEARCH.md).
- [Final validation](https://drive.google.com/file/d/1JPPdAtTPFLkHfVNCnnPswRF9cFrQoSuu/view?usp=drivesdk)

## What was implemented

Independent OBTP Cassette 01 uses timber framing with supported CNC plywood panels and proposed mechanical interfaces. It is not a WikiHouse derivative. System owns the geometry and placement logic; Studio v3 consumes a pinned System commit. Module count, height study, layers, exploded view, object/connection inspection, quantities and nominal Rhino export are available.

The library contains floor, roof, 600 mm wall and 582 mm end-closure cassettes. A four-module frame has 30 cassette instances and 166 solid part boxes. WikiHouse remains separately accessible as v2; Studio v1 remains inside Studio unchanged. Architecture had no existing System dependency and retains its application behaviour.

The selected approach uses established timber/fastener principles while avoiding dependence on an untested plywood friction joint. Pure plywood interlocks and glued stressed-skin cassettes remain alternatives; their limitations and evidence are documented. The report distinguishes sources, proposals and unknowns, including exactly which sources were only partially reviewed. No third-party CAD or proprietary connector profile was copied into the new system. WikiHouse attribution remains intact; publication availability is not treated as a manufacture licence.

The proposed envelope considers mineral-wool cavities, exterior insulation, timber thermal bridges, continuous air/vapour control, rainscreen drainage and ventilation. Thicknesses, vapour behaviour, roof build-up and site requirements are not yet validated. The default 2,100 mm height is a comparison reference; the optional 2,700 mm height is a study, not proof of habitation compliance.

## Saved project mapping

| Project | Drive package | Development branch |
|---|---|---|
| Studio | [v76 source ZIP](https://drive.google.com/file/d/1U4E_xVcNqIiQ3TP70vWXi-bQAimGDZLB/view?usp=drivesdk) | [obtp-studio](https://github.com/anotherSipOfCoffee/obtp-studio/tree/dev/obtp-independent-v1-20260923) |
| Architecture | [v76 source ZIP](https://drive.google.com/file/d/1CGmpFKYEOqsZPVKRZFLLjKgtt3I06Uwj/view?usp=drivesdk) | [obtp-architecture](https://github.com/anotherSipOfCoffee/obtp-architecture/tree/dev/obtp-independent-v1-20260923) |
| System | [v76 source ZIP](https://drive.google.com/file/d/1sqMJ9d5vw4znSaQ0ljiJKJQ739peLMp5/view?usp=drivesdk) | [obtp-system](https://github.com/anotherSipOfCoffee/obtp-system/tree/dev/obtp-independent-v1-20260923) |

Drive is authoritative for the master baseline. GitHub development can be ahead; no automatic two-way sync. Packages record exact included commits and file hashes. System's final receipt/handoff commit follows its packaged implementation and changes documentation only. Studio pins the packaged System implementation. Main/live branches remain at pre-task commits. Repository visibility was not changed.

## Validation and cleanup

All 16 module-count/height combinations passed geometry checks, including clashes, end-wall framing continuity and interface points touching real parts on both sides. Post-cleanup System and Studio browser workflows passed. Existing WikiHouse/W-S checks passed. Studio v1 and Architecture runtime bytes, and all three deployment workflows, remain unchanged. The Rhino reference contains 166 valid closed Breps and passed a Rhino 8 file read/write round-trip; Windows Rhino/Grasshopper was not executed.

Ten obsolete backup/tooling files (19,315,823 bytes) were removed from the active System tree: embedded v74 backup parts and their obsolete reconstruction/snapshot machinery. Older Drive packages and loose reports were moved to historical originals outside the active master. Required source CAD, licences, useful research, the direct W-S viewer and Rhino pilot were retained after checking references.

[Recovery ZIP](https://drive.google.com/file/d/15kK5WF--mBCT8tuwKmaysunFdJ-FLuuT/view?usp=drivesdk): 87,870,088 bytes; SHA-256 fcb72995420e10ba0a0fd433baadf91105f590f013a9c26896ca97a66afb794d. It stores deduplicated repository files and expanded historical package members. The original ZIP containers remain in the historical Drive folder with their IDs. Recovery and all four delivery ZIPs passed downloaded-byte checksum verification. Recovery is excluded from normal development/builds/agent context.

## Remaining work and continuation options

1. **Engineering/prototype review:** choose real materials and fastening schedules; check spans, racking, uplift, foundations, erection, fire and one physical floor/wall/roof junction.
2. **Rhino 8 inspection:** open the provided reference file and run the importer; then define a deliberate Rhino/Grasshopper-to-System update contract. A bidirectional workflow is not completed.
3. **Habitable envelope study:** Lithuanian site/use review, transient moisture analysis, thermal bridges, roof drainage, ventilation and reviewed openings.

Openings and weatherproof roof details are deliberately unfinished. No structural capacities, fabrication tolerances, energy rating or regulatory compliance are claimed. No supplier was contacted, purchase made, live deployment performed or Git history rewritten.

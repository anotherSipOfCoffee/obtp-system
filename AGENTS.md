# Current OBTP System guidance — GH R21, 27 September 2026

Latest explicit user instructions take precedence. R16 was approved and published. Schedule and assembly PDF downloads are authorized only for the default Studio M (open sliders); drawing/opening PDFs stay disabled. Leave Drive and Architecture unchanged.

## Authority and architecture
- `authoring/grasshopper/obtp` is the canonical Python model shared by Grasshopper, drawings, quantities and web exports. Studio owns UI and consumes a pinned System commit; never duplicate geometry in JavaScript.
- The user permits grid/layout redesign, with plan preservation preferred. Adopted R16 retains the 900 mm X × 1200 mm Y grid: tested alternative grids increased diversity. Preserve architectural room relationships, Studio’s heated sliding-glass centre and Sauna’s external shower/storage/seat arrangement unless a measured improvement justifies change.
- Revised Sauna and Studio structural width is 2400 mm. Physical members may span multiple cells. Support rhythm is normally 1800 × 1200, with explicit terminal bays; it is not engineered capacity.
- Facade remains visible. Only facade finish boards (including raised roof facade) are excluded from primary part counts. Retain their separate schedule. Battens, edge trims, insulation, equipment representations and every other modelled category remain primary.
- Manufacturing identity includes material, dimensions, shape, machining, handing and connection requirements. Unknowns remain unknown. Report provisional candidate classes and geometric lower bounds, never verified manufacturing savings. Assembly grouping does not reduce constituent diversity.
- Ordinary wall bays retain two plates, two studs and one panel. Opening side plates match top/bottom; jack studs bear on bottom plates and retain 45 mm lintel bearing. Keep corner/niche terminal exceptions explicit; the local-seam trial increased diversity. See review-r15/OPENINGS.md.
- Both complete terraces use X-directed boards, max 1800 mm, supported butt joints. Interior lining uses selective 900/1800 extensions with recurring terminals; every new butt joint has a full-width batten seat. Do not split every board into 900 mm pieces: that trial added excessive pieces. Facade battens use supported 1800 cuts; roof bearing rails use supported 900 cuts. See review-r15/SHARED_KIT.md.

## Reproducibility and checks
- Original baseline: `1ad71826acfcc7d6d5df9a06167c5fcfea20b516`.
- First integrated cell baseline: `a11e613ac923fd5de6a3d3f1368e6c6eebc57745`.
- `compare_manufacturing.py` reads these immutable Git snapshots into temporary folders. Do not maintain copies as parallel production pipelines.
- After geometry changes: `python authoring/grasshopper/compare_manufacturing.py authoring/grasshopper/review-r15 --full-catalogue`; run the Python suite; then `export_web.py DEST --revision COMMIT`. Export refuses stale comparisons.
- Only part-schedule and assembly PDFs are enabled. Gable is absent from website and new GH controls. GH offers assembly progress (0-100%) and core-frame (0/1) sliders. Core mode colours by canonical provisional manufacturing identity, with a legend. Preparation stages lay out subassemblies flat before placement; exterior cladding is last. These are display-only and never alter quantities or exports; no individual object-type switches. Lithuanian flat-roof label: `Plokščias`.
- Retain geometry/solid/clash, source-hash, export-cache, native acceptance and important browser behaviour checks. Native Rhino/GH acceptance is separate from portable rhino3dm checks.
- Customer-facing brand is `studio 9120`; preserve existing UI and Lithuanian default. Main opens first; Drawing/opening PDFs remain disabled.

## Engineering, sources and scope
- No invented capacities, fastening schedules, supplier compatibility, prices or permit exemption. All connections remain unverified; material grades, machining, wet-area detailing, glazing, heater clearances, roof uplift, soil and bracing require engineering.
- No certified manual-lift mass: wall/roof cassettes are geometry groups, not approved factory lifting units. Use loose-part/small-subassembly erection until weights and handling are verified.
- Preserve supplier/source attribution and licences; proprietary parts must not be stretched. Preserve pinned WikiHouse source geometry and CC BY-SA 4.0 obligations, Studio v1 reference and separate legacy product modes.
- No supplier outreach. Preserve ordinary Git history and existing work. GitHub remote writes use the connector. No Drive synchronization.

Historical release/research documents are evidence, not current competing instructions. Read them only for a relevant detail; this file consolidates current decisions.

## Current review revision (27 September 2026)
- Terrace joists keep 45 mm width and share actual edge faces with 900 mm floor bays, with intermediate deck supports, and extend to the platform rails (210 mm depth with the current floor). No terrace packing cubes. End seats remain explicit. Spans/stock/fasteners require engineering.
- Terrace perimeter fascia, removable bench front/end covers and continuous clad niche side/back returns and full soffits are real counted parts. Niche clear soffits match door height. The outdoor seat recess is 300 mm deep; its divider gives excess depth to storage.
- Default Studio M schedule contains structure, plywood panels and insulation with individually scaled part axonometrics. Its scope does not change complete-model audit counting. Facade boards retain their separate schedule; terrace/floor trims remain primary.
- Assembly ground poses and the bounded Rhino preview cache must never modify canonical part geometry, IDs or quantities. Native handling masses and safe lifting methods remain unverified.
- Python CI uses test discovery. Legacy JS cassette CI runs for its own files; current integration is tested by Studio against its exact System pin, not an obsolete duplicate consumer checkout.

## R19 review decisions
- Retain existing door widths and grid. Narrow supplier doors were investigated, but the preliminary bay-aligned trial increased types and reduced passage width; no product substitution is adopted.
- Keep existing floor cassettes. Terrace edge members use the same mathematical bay faces; intermediate supports are terrace-only. Do not add floor joists solely for visual matching.
- Outdoor recesses use the exterior cladding build-up with counted backing/supports, 1900 mm clear soffits and a 300 mm finished seat recess. Default finished niche width is only 537 mm: shower usability and wet-area details remain unresolved. This is an explicit review concern, not an approved bathroom design.
- `previous` in the current audit means R18 commit 2c21ad5d2d30915487f19e72a18f545e575befba. Earlier audit history remains reproducible in Git.

## Current scope: GH only (27 September 2026)
The user paused site updates. Do not change Studio pins, site files or publish while this scope is active. GH R20 adds a separate detached Parts Layout PDF for default Studio M and connected wall-run erection poses. The GH progress slider is 0–100%; walls raise one at a time through flat/45-degree/upright states about a fixed bottom edge. Canonical geometry and counts remain R19. Full-wall manual lifting is unverified; see GH_R20.md.

## R21 modularity decision
- R20 `d02d8322bb1f456e4b005d5f6a023f236eddc220` is the frozen current-geometry baseline. Retain its geometry after the bounded A/B screen: no candidate reduced fabricated diversity without a worse tradeoff or fit failure. Do not describe procurement reclassification as a physical reduction.
- `scene.modularity` separates the 300 mm coordination reference, existing 900×1200 planning, structural assemblies, manufactured identities, purchased products and connection details. No 300 mm physical bays or new controls are adopted.
- `window_width` is modelled frame outside width. Installation gap/profile/clear passage fields are not supplier-approved unless supported explicitly. Unknowns remain null. Do not narrow or replace entrances based only on host width; height, thresholds and structural bearing matter.
- Use `modularity_study.py` for this comparison, starting with its 24-case screen. `--full` validates only the finalist against immutable R20. Do not run the older multi-history website export pipeline for GH-only metadata changes. Existing 68-test suite and portable/native distinction remain applicable.
- See `GH_R21.md` and `review-r21/OBTP_Modularity_R21.html`; historical guidance above does not override these measured decisions or later explicit user instructions.

## Latest public Studio document scope
The later user instruction authorizes Studio publication for the two locked M-with-storage presets. Canonical PDF recipes accept `include_cladding=False` for public assembly, loose layout and schedule exports; this omits facade boards using the existing manufacturing predicate, without changing full-scene geometry, IDs, audit counts or GH default exports. Studio retains separate cladding quantities and visible 3D cladding.

## R22 current task scope
- GH only; do not change or deploy either website. Three comparison choices: pinned WikiHouse, latest Studio canonical cassette, new B plate ribs. B is independent research geometry, not a Studio replacement.
- Keep original building controls, connected-wall erection and document recipes. New inspection controls belong only to the separate comparison component.
- B is not the older R21 option-B 600/1200 bay trial. Here B means plate ribs with insulation infill. See GH_R22.md and RESEARCH_B_R01.md.
- Run portable comparison exports and source tests; no full website catalogue regeneration is needed when the canonical building geometry is unchanged. Native Rhino/GH must be reported separately.

## R23 room graph / current scope
- Additive GH-only planning pipeline: explicit activation, typed relationships, bounded strip arrangements, guarded construction adapter. No website writes or deployment.
- Retain existing Sauna S/M/L part recipes. With outdoor inactive, omit its three shower fixture pieces during generation; all other parts match the old no-storage model. Treat this as a programme change, not standardization. A plan-only alternative must clear fabrication output when selected, never fall back to stale geometry.
- Programme and connections are independent. Outdoor is currently one mixed shower/storage/seating zone; external-access edges are route requirements, not invented doors.
- Plan owns room sizes and storage when its bridge is enabled; roof/window/foundation/height remain on the original controls. Existing standard door/partition dimensions are fixed in this first adapter.
- See GH_R23.md. Run layout tests and retain the complete source test suite. Use tools/package-gh.py for the current archive. Native GH acceptance remains separate from portable checks.

## R24 active workflow — Sauna and cassette only
- Main creator must expose one sequence: seven-choice Sauna preset (six existing S/M/L × storage presets plus Custom) → authoritative layout → fixed cassette → 3D. No Studio/system selector, separate custom toggle, existing-model bypass or background legacy building generator.
- Saved presets ignore custom-only controls and reproduce existing geometry, including original exterior shower fixtures on no-storage presets. Custom outdoor-off removes those fixtures as an explicit programme change.
- All geometry consumers use the same cassette scene. Unsupported custom arrangements clear construction output. Do not silently repair or replace the resolved plan.
- Other systems/Studio remain available in the separate research creator and source history, not on the active Sauna canvas. No website edits or deployment. Read GH_R24.md.

## R25 active Custom construction
- The main Sauna/cassette sequence now supports single indoor rooms, reversed indoor order, terminal outdoor at either end, and disconnected indoor rooms with separate external entrances. Keep six saved presets exactly reproducible against R24.1 frozen hashes.
- `plan_construction.py` resolves topology using existing canonical wall/envelope/platform recipes. No hidden preset substitute. Outdoor-only and non-strip envelopes remain explicitly unsupported. Preserve stale-plan rejection and fit checks.
- New topology cases put the fixed window on the back wall; partitions, lining, insulation, furniture, opening symbols and drawing labels must follow the same room boundaries. External-route, supplier, structural and handling acceptance remain unresolved.
- Native execution remains separate from portable tests. No website/pin changes or deployment. Use GH_R25.md and tools/package-gh.py; do not repeat historical whole-site export pipelines for this GH work.

## R26 current workflow — checkpoints and Studio
- Supersedes the R24 Sauna-only canvas restriction: expose six saved Sauna presets, Custom Sauna and six saved Studio presets. Studio custom graph solving is not implemented; ignore Sauna custom controls for saved presets.
- Keep five visible checkpoints: preset, layout, cassette, assembly sequence, final preview. Expose diagnostic rows and exact assembly IDs without filling the canvas with every part.
- Preview scopes and assembly filtering never modify the canonical scene or export quantities. Connected walls are display groups, not certified lifting units.
- Retain R24.1 component factory compatibility and R25 Custom construction; use GH_R26.md. Do not change websites.

## R27 accepted scope — 28 September 2026
- Supersedes R26 canvas restriction: main has saved Sauna/Studio plus bounded Custom variants; research has specimens only, no building controls. No website/Drive changes or merge.
- Plan input is room controls only. Custom length is base ±1 existing 900 mm cell, subject to recipe minima; width fixed to selected preset (2400 mm). Preserve valid Sauna room selection/order. Studio remains work-centre-preparation. Do not restore broad R25 GUI bounds.
- Use offset sliders so preset changes stay legible. Overrides off uses base dimensions/programme; offsets remain visible but inactive. Independent roof/window/height/foundation settings persist.
- Functional construction branches share plan_pipeline and canonical model recipes; do not regenerate full buildings inside branch components. Programme-specific topology remains explicit, not an unrestricted plan solver.
- Intermediate previews must agree with final mirrored coordinates and actual levels; preview toggles do not generate construction. NewInstanceGuid overrides are unnecessary; native GUID allocation retained.
- Use GH_R27.md, REVIEW_R27.py and package-gh.py. Compare 24 saved geometry/quantity baselines; tests and portable model exports do not establish native Rhino/GH acceptance.

## R28 third creator — room configuration
- CREATE_LAYOUT_GRASSHOPPER.py is additive: do not replace either existing creator. See GH_R28.md.
- Approved domain: room controls only, 1–6 repeatable function lists, linear rectangular single row; overall 900 X / 1200 Y grid controls. No arbitrary drawn-plan or multi-row solver.
- Separate may/must/cannot adjacency from open/opening/closed boundaries. Closed access groups need exterior entries. Derive cassette geometry directly from resolved room bounds using shared member recipes, never hidden preset generation.
- U terrace = both long sides + one short side, entrance edge included. Studio passage is a central Hall/Entrance with opposing double doors. It feeds planning before framing.
- Sauna outdoor features currently occupy checked terrace reservations; an integrated storage/shower/bench niche is not implemented. Do not claim equivalence with the old niche. Windows/equipment/service design and SLD eligibility remain unresolved.
- Native test status stays explicit. User-authorized code/PR updates only; no websites, Drive or merge.

## R29 independent room stages
- Layout, structure and detailing now each have a creator; CREATE_ROOM_CONFIGURATOR retains the connected workflow. Share room_canvas.py and canonical modules rather than duplicate geometry code.
- Every creator must add a fresh document with independent setup globals and unique filenames while preserving other open definitions. Native execution acceptance remains outstanding.
- Handoffs are versioned, stage-checked JSON with integrity hashes. Live input wins; invalid live input never falls back to stale files. See GH_R29.md.

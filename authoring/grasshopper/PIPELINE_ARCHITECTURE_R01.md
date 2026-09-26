# OBTP autonomous supplier-system pipeline — proposal R01

Date: 2026-09-26. Status: architecture proposal, not an implemented supplier system.
Owner direction: autonomous regeneration, interchangeable documented parts; ProdLib web references; no VisualARQ dependency. Website development/publication paused while architecture is settled. Wind and snow remain paused. Existing Cassette is retained as a study/default, not upgraded to an engineered product by this proposal.

## Existing implementation and smallest migration

`obtp/model.py` owns layout and structural geometry but mixes them with fixed SPEC values and product dimensions. `obtp/envelope.py` creates finishes; `obtp/suppliers.py` mainly annotates generated parts and blocks unavailable systems. `obtp/drawings.py`, `plan_styles.py`, `sheets.py` and `analysis.py` already derive outputs from the shared scene. `export_web.py` compiles offline variants; Studio selects them through a pinned System revision.

Retain this canonical Python core and existing scene consumers. Introduce data records and a resolver upstream of generation, then move one category at a time behind adapters. Do not replace the application, move geometry into browser code, or rewrite all outputs. Rhino/GH is an editable front end to the same core. No paid BIM plugin is introduced; existing Rhino/GH remains required for native authoring.

## Data contracts

| Record | Mandatory information |
| --- | --- |
| SourceDocument | Original URL, supplier, title, document ID/revision/date where available, retrieval date, local checksum if downloaded, permitted reuse/redistribution, cited page/detail, unavailable fields explicitly null |
| Material | Product/grade identity, property values with units, conditions, method and evidence; unknown values null; material family for drawing classification |
| Product | Supplier/model/order code, discrete sizes or documented permitted range, geometry source and fidelity, physical size, installation opening, clearances, orientation/handing, material references |
| Assembly | Ordered layers and reference faces, framing/member recipe, thickness, use/exposure restrictions, product references, thermal/load-bearing roles, attachment interfaces |
| Interface | Named local frame, mating faces/axes, permitted counterparts, required bearing/clearance, seals/membrane continuity, connectors and evidence scope; unresolved capacity/stiffness null |
| SystemPackage | Compatible assembly/product/interface revisions, dimensional coordination rules, selection defaults, supported geometry adapter, documented application scope and unresolved requirements |
| LayoutIntent | Stable room/zone and opening-slot IDs, adjacency, orientation, size intent, clear-space requirements and dimensional anchor policy; no supplier-specific framing |
| ResolvedConfiguration | Exact record revisions, selected products, resolved dimensions, validation results and content hash; immutable input to generation |
| PartInstance | Stable semantic slot ID, selected product/assembly revision, parent, material, geometry source, local placement and source/drawing references |
| DrawingStyle | Material family, cut/projection role, drawing scale, hatch, line weight/type/tone; kept separate from physical material properties |

A product's material conductivity is not an assembly U-value. A section hatch is not proof of material specification. Source format availability is not proof of import fidelity.

## Resolution and substitution

1. Read layout intent, exact package revision and requested replacements.
2. Verify eligibility, source availability, geometry adapter support and product application scope.
3. Resolve dimensions from documented product sizes/ranges. Distinguish frame, rough opening and finished clear opening. Never scale proprietary sections to fit.
4. Resolve mating interfaces and dependent assemblies. Check structural support, weather/air/vapour continuity and installation/maintenance access where rules are documented. Missing rules remain unresolved.
5. Re-evaluate clear spaces, circulation, heater/access clearances and generated area/height/support metrics. Retain the existing envelope gates; a regulatory-area definition remains a separately reviewed rule, not internal area by assumption.
6. Generate the detailed scene. Validate finite dimensions, source IDs, topology/solids and clashes; permit documented intentional intersections only.
7. Rebuild conceptual geometry, drawings and quantities. Invalidate dependent analysis receipts whenever geometry, materials, interfaces or boundary conditions change.
8. Publish all artifacts atomically under one configuration/source hash only after required gates pass. Failed resolution must not leave mixed old/new drawings or relabel old geometry.

Compatibility outcomes: supported, conditional (explicit prerequisites), unsupported, or unknown. Unknown is never an automatic pass. Geometric validity, supplier documentation, native-runtime validation and engineering review are separate statuses, not one green flag. Existing study outputs remain possible with clear study status; technical validation must not be implied.

Example: replace a window in stable slot `opening/sauna/front/01`. Its product revision changes; the slot identity stays. Resolve frame and installation opening, then jamb/header/sill arrangement, reveals, finish returns and seals. Recheck room/window/bench conflicts and update elevations, vertical details, quantities and schedule. If no documented header or mating detail exists, report that exact gap and prevent technical acceptance; do not invent a lintel.

## Dimensional policy — proposed default

Use fixed finished external footprint for whole-system substitutions as the initial policy, with explicit minimum finished clear-space constraints. This protects the chosen product size but can make a thicker system infeasible. Show the before/after clear dimensions. Never silently enlarge the footprint, shrink a circulation clearance or snap the layout to a new grid.

Offer a deliberate designer-level alternative later: preserve finished internal room dimensions and recalculate external dimensions and envelope gates. This is a proposal, not a change to current dimensions. Supplier coordination grids belong to packages; the current 600 mm Cassette pitch is not a universal supplier rule.

## Model, drawings and analysis

Detailed geometry is the authority for assembly locations, part quantities, cuts and dimension anchors. Conceptual web plans are merged silhouettes derived from it. Technical drawings retain material layers and model-derived cuts. Supplier 2D detail overlays may supplement cuts only at matched location, orientation, scale and product revision; distinguish documented detail from schematic reconstruction.

Use manufacturer 3D where it is adequate and licensed. Otherwise build a documented parametric representation with recorded omissions. Keep display meshes, section-capable geometry and analysis abstractions separate but linked by source IDs. Do not assume a mesh contains insulation layers or an imported IFC preserves parametric behaviour. Do not derive engineering models from the web mesh.

Material properties carry conditions and evidence; drawing hatch/line styles are scale-aware presentation rules. Dimensions reference model anchors, not independent typed values. Reports only include numerical analysis results with completed, validated solver receipts matching input hashes. Supplier product data does not establish project-specific responsibility or complete-building performance; record explicit engineering scope/acceptance separately.

## ProdLib and dependency handling

ProdLib is a discovery/reference source, not a live runtime dependency. Start with public catalogue links and manufacturer documents; desktop-only items are recorded as unavailable until recovered. Do not assume native Rhino support or convert Archicad objects without checking results. A link-only record is eligible for research, not detailed implementation where dimensions or connections are missing.

Pin accepted source versions and checksums. Supplier updates enter review and never silently change existing projects. Cache permitted source files for reproducible builds; do not redistribute restricted CAD in public repositories or downloads. A library can contain many manufacturers; this does not establish that their products are mutually compatible. No supplier contact is authorized by this specification.

Public reference starting points (discovery, not verified assembly adoption):
- https://www.prodlib.com/support/downloading-content-from-the-prodlib-web-library-zy91z2xx
- https://www.prodlib.com/lapwall/seinaelementit-yksi-ja-monikerros/ikkuna-ja-oviliitokset_75bb82882ce64db9a039a13381d3d23a
- https://www.prodlib.com/lapwall/seinaelementit-yksi-ja-monikerros/ylapohjaliitokset_5a2bf50fc2e5435282caaceb95e60afe
- https://www.prodlib.com/lapwall/kkattoelementit/rakennetyypit_3fde448f58fe48e79c508322fcd0d6a1

## Execution boundary

Keep offline catalogue compilation as the first release architecture. GH supports wider designer parameters; the website exposes the successfully compiled supported subset. Arbitrary on-demand web generation is a separate future hosting decision, not implied by autonomy. No live Rhino connection is required for the finite catalogue. Every artifact records configuration hash, source lock and generator revision.

Autonomous: select, resolve, regenerate, validate software invariants and export within encoded verified rules. Human review: accept new supplier/system evidence, resolve undocumented junctions, confirm project-specific engineering scope and approve significant source updates. Automation must not invent missing engineering rules.

## Implementation increments and acceptance

1. Add record schemas, source lock and explicit status model; adapt existing Cassette constants into a package without geometry changes. Acceptance: same six base configurations and existing 54 buyer exports; stable source IDs; equivalent dimensions/quantities/drawing extents.
2. Separate layout intent from assembly dimensions; add one window-slot adapter. First test only existing documented Pihla size candidates; do not claim cross-manufacturer interchangeability yet.
3. Obtain one coordinated supplier assembly package and a genuinely documented replacement window. Implement mating details and resolve missing sauna-use evidence. Acceptance: complete wall-floor-roof-opening slice, material-aware sections and no undocumented accepted interface.
4. Demonstrate supported substitution and unsupported substitution rejection. Check frame/rough opening distinction, clear spaces, section changes, quantities, stable slot identity and invalidated analysis.
5. Check native Rhino/GH, then integrate with all six layouts and compile web outputs. Publish System first and Studio only after validation and resumed publication authorization.

Regression cases: A→B→A deterministic roundtrip; same input gives same hashes/quantities; missing document/property; unsupported opening; thicker wall loses required clear space; grid mismatch; source update; old solver receipt; failed build preserves last valid release without showing it as new.

## Outstanding decisions / evidence

- Fixed exterior vs fixed finished interior policy: fixed exterior proposed, not yet accepted.
- Complete supplier and product package: not selected. Hunton, LapWall and Lithuanian candidates remain research options, not enabled alternatives.
- Supplier responsibility requires an explicit project/service scope; product content alone is insufficient.
- Accessible source files, licensing, sauna exposure, installation interfaces and engineering properties need verification per selected package.
- Native Rhino/GH acceptance remains pending; VisualARQ is excluded. Wind/snow stay paused.

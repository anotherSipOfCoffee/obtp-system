# System working rules

## Latest scoped authorization — Studio preset R07
On 2026-09-26 the owner authorized implementing and publishing the Studio preset after research and validation, using the same Cassette/Python/GH pipeline as Sauna. Adapt the supplied two-block/open-centre reference for genuine creative workspace and preparation/storage, with no bedrooms or residential program. This supersedes the infrastructure-planning pause only for this release. Keep Sauna as default, Workshop unavailable, and all supplier/compatibility and engineering holds. System first, then pinned Studio; wind/snow remain paused. Read System authoring/grasshopper/RESEARCH_R07_STUDIO.md.

## Current owner direction — 2026-09-26: supplier-based autonomous pipeline

Read this section before historical instructions below. It supersedes older conflicting implementation direction; later explicit owner instructions take precedence. Goal: autonomous regeneration with interchangeable, documented supplier parts and compatible systems.

- Use ProdLib web catalogue and original manufacturer documentation as research sources. Desktop exports are not a prerequisite for research. Do not assume every listed file is downloadable or Rhino-compatible.
- Do not introduce VisualARQ or another paid BIM dependency as part of this pipeline. Retain existing Rhino/Grasshopper authoring; the portable Python core remains shared with offline exports.
- Separate layout intent, supplier/product/material records, assembly definitions, connection interfaces, resolved configuration and generated geometry. Supplier dimensions and documented rules must drive generation, not merely annotate generic geometry.
- Interchangeability is conditional on documented interfaces. Preserve source geometry; do not stretch proprietary parts, invent junctions, assign unverified capacities or treat unknown compatibility as a pass.
- Use supplier models where suitable. If unavailable, reconstruct only from documented dimensions/details; record source, revision, checksum where available, geometry fidelity and omissions. Respect source licences and redistribution restrictions.
- Model parts retain stable semantic IDs and product/assembly revisions. Derive conceptual previews, detailed plans/sections, quantities and analysis abstractions from the canonical detailed model. Material drawing styles are separate from physical properties. No independent browser construction geometry.
- Changing a product must resolve dependent openings, framing and junctions, regenerate affected outputs and invalidate stale analysis receipts. Failed resolution must not mix old drawings with a new configuration or relabel old geometry.
- Pin reviewed source revisions. Never silently adopt a supplier update. Missing engineering inputs remain explicit; numerical results require completed validated solver runs matching input hashes.
- A supplier BIM object or product declaration does not transfer whole-building design responsibility. Record documented supplier engineering scope separately; no automatic compliance, permit exemption or performance promises.
- Keep Cassette as the working default/study. Supplier alternatives remain unavailable until their adapters and compatibility requirements are resolved. Do not claim the current annotation catalogue already implements interchangeable systems.
- Wind and snow analysis remain paused. Preserve existing geometric envelope gates, customer choices and project-specific behaviour.
- Current phase is infrastructure planning and agent-rule preparation. Do not resume feature changes or website deployment merely from historic release authorizations. Subsequent explicit owner requests can authorize implementation/publication. Documentation-only handover changes are authorized now.
- Fixed external footprint during system substitution is a PROPOSAL, not an accepted owner decision. Do not silently change the current dimensional policy. No complete alternative supplier package has been selected.

Canonical architecture proposal: https://github.com/anotherSipOfCoffee/obtp-system/blob/main/authoring/grasshopper/PIPELINE_ARCHITECTURE_R01.md
Read its status and unresolved decisions. Proposed implementation sequence: package existing Cassette constants without geometry change, prove an opening substitution, then integrate a documented complete assembly package. This sequence is a plan, not permission to remove preservation gates.

Project boundary: System owns supplier records, assembly/interface rules, geometry adapters, validation and model-derived outputs. Read authoring/grasshopper/CANONICAL_WORKFLOW.md and PIPELINE_ARCHITECTURE_R01.md before touching the generator.

## Historical and project-specific rules
Read docs/SYSTEM_RULES.md and docs/CATALOGUE_CHECKPOINT.md. Preserve the existing Types → Objects → Connections → Assemblies interface; the owner's goal is to replace generic geometry with official WikiHouse components, not to replace the interface with a one-object viewer.
Use the pinned Skylark150 source in docs/CATALOGUE_SOURCE_LOCK.json. Current library has six CAD block objects plus full and half ties reconstructed from source CNC profiles. Do not invent joints, stretch source parts, mix generations, or fill old generic categories with false equivalents. Source IDs and nested instance paths must remain traceable.
The open chassis slice is a geometric fit study, not a complete building. Check docs/BLOCK_INTERFACE_FIT_CHECK.json and geometry audit. One R-S source Brep is open; no silent repair. E-S and W-O-S-1 source naming/height caveats are documented. Rhino 8 and full-volume/engineering checks remain distinct from browser checks.
Retain source geometry attribution under CC BY-SA 4.0. Keep Studio and Architecture integration deliberate. GitHub operations use the GitHub plugin only. No supplier outreach without authorization. Drive updates only when requested. End progress reports with continuation options, but continue routine authorized work without repeated permission requests.


## Opening instruction gate and seam checkpoint
The owner requires precise WikiHouse opening instructions before completing automatic window/door placement. Keep opening configuration on hold; CAD existence and fitted envelopes alone do not satisfy this gate. Read docs/OPENINGS_AND_ENDWALLS_CHECKPOINT.md. End-wall corner trials are rejected, not solved. Floor/roof seam ties are implemented using the separate sampled source-socket checks in docs/SEAM_CONNECTIONS.md.

## Master baseline and development branches — current owner policy
Google Drive holds the authoritative OBTP master baseline in OBTP_MASTER, organized into Studio, Architecture and System. GitHub repositories are downstream development branches and may contain valid work ahead of Drive. Never overwrite newer or unique branch work from a baseline. Compare exact commits/manifests, integrate deliberately, and record divergence; no automatic two-way synchronization.
Read the current System project/PROJECT_MAP.md and project/AGENT_GUIDE.md. Their links point to the active Drive master and historical recovery location. GitHub operations use the GitHub plugin only.
On 2026-09-24 the owner authorized publishing System first, validating both WikiHouse and Cassette 01, then publishing Studio v3 from that tested System revision. This supersedes the earlier no-deployment instruction for this release only. Preserve ordinary Git history, Studio v1 and WikiHouse. Architecture is outside this release; Drive remains the master baseline and is not automatically synchronized.
Before removal, verify a dated recovery snapshot outside active projects. Do not commit backup ZIPs, caches or nested historical packages. Source CAD bundles, licences, Studio v1, WikiHouse and useful Rhino reference evidence are intentional assets. Historical recovery content is excluded from normal builds and agent context unless recovery is requested.

## Independent variation
Cassette 01 is a separate original OBTP proposal under dist/cassette. The preceding WikiHouse source restrictions apply to WikiHouse, not a prohibition on the separately authorized new variation. Read docs/cassette/RESEARCH.md, SPECIFICATION.md and VALIDATION.md. Do not claim mechanical capacities, tolerances, habitation or compliance from the software checks. Opening controls remain disabled.


## Cassette controls and connection research — 2026-09-24
Studio v3 owns its configuration UI and follows the WikiHouse control pattern: 1–8 modules, layers, exploded view and reset at 2,100 mm wall height. Import the pinned System generator and renderer; do not embed System's inspector as the Studio configurator. System owns modules, interfaces, source references and separate object/connection inspection. Read System docs/cassette/CONNECTIONS.md. Product candidates are not engineered connection releases: preserve capacity:null and fasteners:null. The 2,700 mm study remains System-only; narrow-panel racking and terminal hold-down fit remain open. The owner subsequently authorized the System web release and its inspection fixes. Drive baseline updates remain separate.

## Connection detail studies
Read docs/cassette/DETAILS.md and DETAIL_SOURCES.json. The six local studies in dist/cassette/details use one fastener envelope each to inspect a position, never as a fastening schedule. Preserve conditional screens, rejected narrow-member positions and null capacities. Cutaway/crop/explode must never change the measurements. No repeat fastening pattern, hardware manufacturing geometry or structural release is implied. Studio source-pin changes must be deliberate, preserve its own controls and pass compatibility checks. No construction-ready claim is authorized. Run tests/connection-details.cjs and tests/connection-details-browser.cjs along with existing regressions.

## Constituent parts and coordinated inspection
Read docs/cassette/INSPECTION.md. Keep long joists continuous; the owner's sketch marks member contacts, not approved splice cuts. Use actual source assets for part explosion/isolation and internal-contact inspection. A physical screw/angle remains one connector; display regions are not manufactured subparts. Keep unselected hardware visible without guessed geometry. Run tests/inspection.cjs and tests/cassette-browser.cjs along with existing gates.

## Canonical Sauna authoring — owner decision 2026-09-25
The owner explicitly authorized the GH-R03 website update after pausing earlier publishing. System `authoring/grasshopper/obtp/model.py` and `envelope.py` are the canonical Sauna geometry source, shared by Rhino/GH and offline web exports. Make geometry changes there first; never reimplement Sauna geometry or dimensional rules in Studio JavaScript. `export_web.py` compiles the finite website catalogue. Studio owns UI only and consumes a pinned System commit through system.lock.json. Keep native Rhino/GH acceptance distinct from portable geometry and browser checks. Six base layouts remain S/M/L × external storage. Current buyer defaults: terrace 1200 (600/1200), window 1200 (600/900/1200), vertical timber only; window on entrance facade within sauna room. Read authoring/grasshopper/CANONICAL_WORKFLOW.md in System.

## R04 authoring and customer presentation
Model-derived drawings, measured dimension anchors and drawing exports belong to System authoring/grasshopper/obtp/drawings.py and sheets.py. Do not add independent browser geometry. Source DXF symbols carry a source checksum. Cake House-style controls and Koto-inspired neutral gallery/navigation are authorized; reserved photography fields remain empty. White appearance is a display override. Read RESEARCH_R04.md for insulation, 4480 mm gable reference height, legal/title-block and native Rhino acceptance limits.

## R05 customer refinement — 2026-09-26
Owner requires no embedded PDF preview; download only. Mobile controls toggle over the existing 3D view. Terrace is1200 only; Pihla sauna fixed window candidate uses frame widths580/880/1180 (default1180),170 depth and51 face with provisional10mm installation allowance. Gable roof is flush with finished walls on all sides. Only Sauna remains exposed; navigation label is Module type. Canonical model records wall regions; plan_styles.py merges these into conceptual black wall silhouettes, while drawings.py/sheets.py retain model material intersections for structural PDFs. Never add separate Studio geometry. Read System authoring/grasshopper/RESEARCH_R05.md.

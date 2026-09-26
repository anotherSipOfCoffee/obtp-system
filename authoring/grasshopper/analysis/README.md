# OBTP analysis preparation A01

This is an implemented **preflight and solver-handoff scaffold**, not a completed engineering analysis definition. No thermal, structural or wind solution has been run. It does not establish safety, compliance, a timber utilization ratio or a heating time.

## Authoring and dependencies

The source is `obtp/model.py`; `obtp/analysis.py` reads its detailed solids, connection records, assembly specifications and drawing intersections. Conceptual web geometry is not an input. Part IDs are retained; a separate content hash covers solids, connections and assembly specifications. Results must also match the input hash. Changing a material or boundary condition invalidates a receipt even if shape is unchanged.

Run `python analysis/sample.py OUTPUT_DIRECTORY` from this package to create the M/no-storage sample: JSON preflight, editable input JSON, material-section SVGs and A3 dossier. This is a real geometry preparation run, not a solver run. Native Rhino is not installed in the development runtime.

Run `CREATE_GRASSHOPPER.py` in Rhino 8 Python 3 with Grasshopper open to build the native definition. It includes six linked analysis preparation groups. This builder still needs native Rhino acceptance; no binary .gh was generated or tested here. Keep the definition next to the source package. Save local edits separately. Rhino requires a commercial/evaluation licence; exact service release is recorded by setup-receipt.json on the user's machine.

## Proposed solver handoffs (primary documentation checked 2026-09-26)

* THERM 8.1 + THERM Redistributable Libraries; Ladybug Tools 1.10 Fairyfly. `fairyfly-therm` documents `run_thmz(path, silent=False)`. `analysis/run_therm.py` invokes this public API on a separately prepared, checked THMZ. This does NOT construct a valid thermal domain from overlapping CAD sections automatically. Sections still need domain partitioning, air cavity definitions, material assignment, boundary normals and truncation checks. Exact installed package and solver builds must be recorded before accepting results. Check LBNL beta status/licence before production use. https://www.ladybug.tools/fairyfly-therm/docs/ ; https://discourse.ladybug.tools/t/introducing-fairyfly-for-therm-simulation-with-lbt-grasshopper/39878 ; https://windows.lbl.gov/window-81-therm-81-beta-releases
* Karamba3D v3 on Rhino 8: possible linear elastic forces/displacements backend, not adopted as an EC5 timber design checker. Its documented beam utilization is EC3 steel. Installation, licence tier and exact build must be recorded locally. No Karamba model or analysis has yet been executed. https://manual.karamba3d.com/appendix/a.4-background-information/a.4.6-approach-used-for-cross-section-optimization
* Elmer is an open-source candidate for a custom integration, not a copied plugin. Review its solver/library licences and validate benchmark/convergence tests before implementation. No Elmer adapter or run is claimed. https://github.com/ElmerCSC/elmerfem
* Eddy3D CFD is deferred. Code wind pressures remain a separate workflow; visual airflow is not a substitute. Current documentation identifies OpenFOAM 12 and Rhino 8.27; exact versions and licensing need pinning if adopted. https://docs.eddy3d.com/latest/

No proprietary plugin code is extracted or redistributed. The preparation code itself uses Python standard library; PDF uses ReportLab. Native GH uses RhinoCommon and Grasshopper installed with Rhino.

## Thermal method and three operating stages

Use separately validated U values with area reference conventions: Htr = sum(U A) + sum(psi L) + sum(chi), W/K. Do not sum frame area twice with complete-window Uw. Psi = L2D - sum(U b) requires a documented reference-dimension convention. Point chi requires 3D accounting and subtraction of associated planar/linear terms. Ventilation loss is separate. None is calculated in A01.

Before heating, during heating/use, and after shutdown are sequential states. The inputs explicitly distinguish rated heater power from actual duty. Warm-up/cool-down needs heat capacities, initial conditions, controls, ventilation and moisture schedules. Three steady-state THERM runs cannot establish transient warm-up or drying. Condensation screening requires surface temperature and vapour pressure; an ISO 13788-style screening is not a full intermittent-sauna hygrothermal assessment. Interstitial drying requires a suitable coupled heat/moisture model.

Heater candidate: Harvia Spirit SP90E HSPE904M, 9 kW, 385 x 334 x 687 mm, manufacturer room range 8-14 m3. Front/side clearance 80 mm, ceiling 900 mm and floor 100 mm shown on current product page, subject to installation manual. Existing model placeholder is 260 x 430 x 700 mm: **not a product model**. It has not been silently replaced. Confirm effective room volume including glazing, mounting and clearance against all six layouts before geometry substitution. https://www.harvia.com/en/products/HSPE904M/spirit-sp90e-90-kw-black

Material candidate: PAROC Ultra cavity batt, declared conductivity class 0.035 W/(m K), product page describes timber walls, partitions, pitched roofs and ventilated floors. This is not a high-temperature design conductivity or proof of available 195/220 mm layer combinations. Required: local DoP, thickness schedule, density, specific heat and temperature/moisture dependence. https://www.paroc.com/lv-lv/products/ultra-multipurpose-slab-pgm-100230

Existing connector candidates remain Rothoblaas HBS and Simpson ABR from `docs/cassette/DETAIL_SOURCES.json`. Candidate envelopes are not fastener schedules. Retain null capacities and stiffness until substrate, edge/end distances, fastener type/count, load direction and ETA checks are resolved. Timber grade, plywood grade/lay-up, foil and tapes, wind barrier, glazing Uw and installation seal data are unresolved. No generic value is substituted.

## Structural and wind method

Actual solids and structural candidate IDs are exported. Beam/shell classification and local axes require explicit assignment; longest bounding-box side does not establish timber grain. Connections cannot be inferred as rigid from touching solids. No supports are silently added to remove mechanisms. G, Q, S and W plus LT National Annex combinations remain separate inputs. Required acceptance checks include force and moment balance, reaction totals, mechanisms, member/mesh convergence and connection demand/capacity comparison with cited evidence.

Flat ground is the owner brief, not terrain roughness or an orography factor. Coordinates, altitude, orientation, surrounding obstacles/roughness per direction, openings and National Annex editions remain required. Wind workflow must retain external and internal pressure signs, loaded-area-dependent coefficients, roof/façade zones and uplift load path to anchors. No design pressures or resistance are reported in A01.

## Product dossier / STR boundary

Owner selected a technical product dossier. A3 drawing sheets are followed by analysis preparation pages; the appendix is also separately exportable. Identification, revision/source hash, sheet numbering, units, assumptions and unresolved items are retained. The existing 180 x 45 mm title block is a VIKO LST1516-based teaching example, not a claim that STR universally mandates this exact stamp.

STR 1.04.04:2017 governs building project preparation; a generic product dossier without site, responsible designers, site plan and engineering review must not be labelled an approved statutory project or fully STR-compliant. The current consolidated legal text needs clause-level review before a formal project issue. Official source: https://www.e-tar.lt/portal/lt/legalAct/ad75ac40a7dd11e69ad4c8713b612d0f/asr (automated retrieval returned 403). No legal requirements are guessed around this access failure.

## Remaining implementation

Thermal domain meshing and material assignment, numerical result parsing/diagrams, structural FE assembly and EC5 verification, wind coefficient/zoning implementation and LT NA verification, transient hygrothermal solver, and native .gh acceptance remain unfinished. The current PDF makes these missing analyses visible rather than presenting empty result tables as calculations. The website has not been published with this work.

## A02 scope update

The owner paused wind and snow; inputs now record `paused_by_owner`, with null actions. Location is Lithuania in general. Do not request site wind/snow inputs while this scope is paused. Product provenance is included in the analysis content hash. Supplier research is `../suppliers/RESEARCH_A02.md`. Window detail exports now use vertical `window-head` and `window-sill`; the prior horizontal jamb is retired. The current dossier has nine pages: five drawings, one supplier schedule, then three analysis preparation pages. The preparation pages are not numerical solver results.

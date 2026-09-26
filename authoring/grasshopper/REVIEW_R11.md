# R11 owner review - unpublished
2026-09-26. Supersedes Studio flat-only and presentation rules where explicitly changed below.

## Canonical workflow
Modify Python/GH first. Studio is a finite offline consumer. No GitHub push or website deployment is authorized for this review. Owner requests opening Main first, plain Lithuanian copy, matching gallery heights, white model only, two foundation studies, shared building/deck foundation grid, firewood access, door-height sauna niches, floor perimeter boards, visible insulation, and model-linked A3 schedules / assembly guidance. Retain flat roof with a small drainage fall alongside sloped roof choices.

## Inspection and evidence
The existing wall/floor/ceiling mineral wool existed but app.js suppressed it. This suppression is removed. The ceiling cassette is insulated; the weather roof above is a ventilated space, not a missing second insulation layer. Exposed weather-rafter ends now have fascia. Eave ventilation area, weatherproof closure, insect mesh, vapour-control products and hygrothermal performance remain unresolved. No arbitrary insulation fill in ventilated space.

Existing low-slope roof is 1:40 (1.43deg), single slope 8deg, gable solves the existing 4480mm top. Retain 1:40 as the current coordination fall; no automatic reduction to a bare finished minimum. Bauder May2026 summary of BS6229:2025 says design falls must account for deflection/tolerances, completed minimum generally1:80. UK guidance is a technical reference, not Lithuanian legal certification. Ruukki Classic LT minimum7deg supports keeping the metal option distinct from membrane.
- https://www.bauder.co.uk/technical-centre/standards-and-knowledge/bs-6229-2025-key-changes
- https://www.ruukki.com/docs/default-source/roofing-documents/lithuania/ruukki_classic_montavimo_instrukcija.pdf?sfvrsn=e790ff84_12
- https://www.paroc.com/lt/documents/uploads/ventilated-facades-design-guide
- https://lt.paroc.com/-/media/files/cad-drawings/paroc_ssn_cad_book_2023_lt.pdf

Foundation source: Zyle lists pile / reinforced grillage drawings, not publicly available engineering dimensions. `foundations.py` replaces disconnected support strips/pads with shared setting-out origin, 600mm coordination and 1800mm intermediate support pitch plus actual edge rows. Type0 timber beams on pile envelopes, type1 concrete grillage on pile envelopes. ALL sections/depths are provisional display envelopes, not adopted Zyle dimensions or a foundation design. Supplier/soil design still required. No rigid joints or capacities assumed.
- https://siltasiaure.lt/parduotuve/zyle/

## PDF sources and intended use
Owner-supplied 23-##_TDP_SA_PVZ.pdf: two parallel ruled tables with element view, index, dimensions, handing and quantity. Adopt parallel tables, dimensioned opening elevations and component axonometrics. Do not copy project metadata/stamps/signatures.
RVS_17-12-01_SA.pdf: grid bubbles, chained dimensions, levels, differentiated material cuts. Adopt model-linked setting-out axes and levels. It is an unrelated residential project, not an OBTP engineering source.
SK.pdf page2: ruled name/index contents. Adopt for core drawing index.
Mantas Minikavi ius. BD.pdf: 2017 academic residential project. Useful separation of quantities, organization and costs, not a current legal standard, timber specification or price source.

Legal scope remains project-specific: Construction Act24/27 and STR1.04.04:2017 §29. Schedules and assembly guide are coordinated technical supplements, not automatically compulsory pages for every SSP. Site plan, legal use/category, designer review/signatures remain missing. No report page count is presented as statutory. Analysis results are not inserted because there are no completed solvers; wind/snow remain paused.

## Pricing (retrieved 2026-09-26)
- Lentvario Mediena C24 45x195x6000: 544.50 EUR/m3 incl VAT =>450 exVAT. https://www.lentvariomediena.lt/straipsniai/c18-c24-mediena-lietuvoje
- Boltvita benchmark: from360 EUR/m3 +VAT for45x195x4800. https://www.boltvita.lt/mediena-statybine/
- Faneros pardavimas birch18mmBB/CP:23.63 EUR/m2 +VAT. https://www.faneros-pardavimas.lt/berzine-fanera/
- Lazertechas CNC from30EUR/h (VAT basis not stated in retrieved snippet). https://www.lazer.lt/cnc-frezavimas/
- InSky preparation50EUR/h,2000x3000mm table,Z200mm; job priced individually. https://insky.lt/cnc-frezavimas/
Price proxies do not establish material certification/compatibility. A 220mm joist and long beams are not automatically machineable on this router. CNC scenario for sheet outlines:2passes,2m/min,2min handling per part,4h preparation; all assumed, NOT CAM simulation. Timber10%/plywood15% purchasing allowances are assumptions, not nesting. Rate30/50 treated exVAT for scenario only; verify workshop tax basis. Cost scope covers timber framing/plywood, excludes all finishes, insulation, openings, concrete, connectors, installation/transport. Do not mislabel as total turnkey or procurement cost.

## Native acceptance
`documentation.py` owns openings/components/assembly A3 recipes; `native_drawings.bake` consumes those same recipes to create Rhino layouts and PDF. The offline previews are labelled non-Rhino proofs. No Rhino runtime is available here. Native execution, hatch performance, PDF output and manual editing remain to be checked on Rhino8. Assembly stages are coordination guidance; no fastener count, torque, lifting rig or temporary-bracing design is invented.

## Validation and delivery
29 existing Python tests pass (including collision, section and envelope checks). 12 added program/roof/foundation combinations passed parameter, ID, cut-filter and quantity reconciliation checks. The local catalogue contains 324 geometry variants. JavaScript syntax checks pass. Browser visual testing is blocked by this environment's browser launch restrictions; no visual web acceptance is claimed.

A3 overall views use fixed 1:25 or 1:50 as space permits (the enlarged terrace and setting-out bubbles do not always fit at 1:25). Views are not stretched. Details remain separately scaled.

The foundation concrete shape is a provisional display envelope, not a sourced constructible cross-section. Do not purchase or build from it. Wood totals sum modeled stock volumes; the collision suite covers the tested Sauna configurations, not a complete fabrication audit of every new Studio/foundation variant. Full material and fabrication totals remain unavailable without product selections, stock optimization and quotations.

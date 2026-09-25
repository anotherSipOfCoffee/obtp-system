# R02: construction research and model decisions

25 September 2026. Local Grasshopper/Rhino development only. GitHub and web publishing are paused.

## What was investigated

### Interior finish and benches
Thermory's sauna wall-panel installation guide specifies battens at least 20 × 45 mm, recommends 400 mm spacing and sets 600 mm maximum. It requires air movement behind the lining and independent bench support. Harvia also requires backing for wall-supported benches/heaters. R02 models 20 mm battens and 16 mm horizontal interior boards, with edge gaps, separate from structural sheathing. The nominal 95 mm board pitch and 16 mm thickness are project study choices; profiles, species, foil, insulation, waterproofing and fixings are not a procurement specification.

The bench-module guide distinguishes frame, removable frontboard and seat grate, and preserves wall-end/ventilation gaps. R02 retains independently supported benches, leaves a nominal 10 mm gap from finished walls and adds slatted covers only to their exposed short ends, below the seats. No full front enclosure or backrest was requested. Detailed bench supports/cleanability and heater clearances remain to be checked.

Primary references:
- https://thermory.com/wp-content/uploads/2023/01/Thermory_Installation_Guide_Sauna-wall-panels_A4_0123_ENG.pdf
- https://thermoryusa.com/wp-content/uploads/2024/10/2024-09-Sauna-Bench-Module-Installation-Guide.pdf
- https://support.harvia.com/hc/en-gb/articles/21953077934620-I-am-about-to-start-panelling-my-sauna-what-do-I-need-to-take-into-account

### Vertical facade only
TDCA describes a drained, ventilated rainscreen cavity, a breather layer and counter-battens for vertical cladding. R02 uses the existing 12 mm sheathing plus 25 mm vertical counter-battens, 25 mm horizontal battens, and nominal 22 mm vertical boards on an 80 mm pitch. Thicknesses and profile are project choices requiring supplier confirmation. The 2 mm modeled joints are visual profile reveals: they do not establish a tested open-joint weatherproof system. No horizontal facade option has been added. Corner/reveal flashings, insect mesh, membrane and ground clearances remain detail tasks.

- https://www.tdca.org.uk/timber-cladding/cladding-design-considerations/

### Slab seams and wall bearing
Exact solid checks of the prior un-exploded model found no overlapping timber slab beams. Each independent cassette has a boundary joist; at a seam the two joists abut, so two adjacent 45 mm members remain intentional. Removing one would change the cassette assembly and is not justified by a visual impression alone.

Platform framing can transfer loads from wall bottom plate through floor sheathing into rim/bearing members. That principle does not validate our particular sections, panel bending, fasteners or uplift path. R02 retains the wall bottom plate on the floor skin, with perimeter blocking below, and records the junction explicitly. Previously introduced partition trimmers are retained. No new connection is represented as engineered. Exploded views are display offsets, not assembly clearance evidence.

- https://www.woodworks.org/resources/structural-design-considerations-for-bearing-wall-top-plates-that-support-concentrated-loads/
- https://awc.org/resources/wood-products/floor/i-joist-rimboards/

### Roof and terrace
Ruukki's Lithuanian Classic C page specifies a minimum 7° roof slope, 475 mm effective sheet width and 32 mm seam height. R02 selects 8° single slope and 25° gable; these angles are study defaults, not structural optimization. Seams are simplified visual envelopes, not folded-sheet fabrication geometry. Product instructions, underlay/ventilation, clips, seams and drainage details still govern final specification.

The flat option uses a membrane at 1:40 design fall, informed by roof-manufacturer guidance on allowing for tolerances/deflection to achieve drainage. This is borrowed technical guidance, not a Lithuanian regulatory approval. The dark low-slope reference appearance is retained without assigning standing-seam steel to an unsuitable nominally flat roof.

- https://www.ruukki.com/ltu/stogai/produktai-stogams/stogo-dangos-lakstai/stogo-dangos-produktai/parnu-classic-c
- https://www.bauder.co.uk/technical-centre/standards-and-knowledge/updates-to-bs6229-2018

The terrace runs along the entrance side (including the optional annex), at depths 0/600/1200/1800/2400 mm. Flat and single-slope roof coverage follows that depth. Gable roof does not extend with the terrace. Deck framing is independently supported. The canopy has an outer beam and posts at no more than 3000 mm nominal spacing instead of relying on an unverified cantilever. Soil, frost, foundations, snow/wind, spans, member sizes, anchorage, door swing and post placement are not engineered by this geometric study.

The level structural roof cassette remains a ceiling platform, with a separate sloped weather-roof study and framed bearing upstands above it. This is conservative reuse for inspection, not a material-efficient final roof assembly. Roof edge closures, roof void ventilation, insulation continuity and rainwater goods remain incomplete.

### Window
The new sauna end-wall window uses the same rough-opening bottom and top as the entrance door. Width is 600 or 900 mm. It has actual framing and glazing geometry, and cuts through sheathing, cladding and interior lining. The heater was moved clear of the end-wall opening as a layout candidate, not as a verified heater-clearance solution. Safety glazing, low-level glass protection, condensation and heat-loss/heater sizing need product-specific checks.

## Geometry validation versus approval

R02 tests 54 size/storage/roof/terrace combinations for intersections between modeled wood solids using exact interval tests for boxes and linear sloped prisms. Separately, 108 custom configurations retain the earlier structural checks. Three roof examples are exported and reopened as valid closed Breps, with vertex extents compared to source recipes. Tests also confirm window/door vertical alignment and rejection of unsupported or oversized combinations.

The checks do not validate structural capacity, moisture behavior, thermal performance or legal permit status. All outputs remain website_ready=false and manufacturing_release=false. Native Rhino/GH execution remains pending on the owner's Rhino 8.

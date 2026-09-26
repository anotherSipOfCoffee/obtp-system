# R08 seasonal Studio and terrace coordination

Owner request 2026-09-26: continue GH library implementation; Studio flat roof only; remove exterior roof posts in both programmes; extend Sauna terrace beside shower; seasonally enclose Studio court with sliding doors; add small wood-burning heater and open firewood storage at a short end.

## Implemented
- Canonical `parameters` resolves Studio to roof type 0, explicitly locking other roof types. Direct invalid Studio `build` inputs reject. Shared GH roof selector continues to serve Sauna; resolved Studio report/model shows flat roof.
- `studio_winter_closed` boolean is wired into the GH builder and component. Both court ends use three-panel sliding coordination objects, with open/closed states, stable IDs and model-derived plan/sections. Standard nominal open width exceeds 1000mm; this is not a certified clear-opening/escape calculation.
- `seasonal.py` adds sliders, a manufacturer-dimension stove body placeholder and an open 600mm-deep rack at the left short end. Reference IMG_3142.png shows the open-end firewood-storage idea; its gable/cladding are not copied. No enclosed log-store room or log inventory model.
- Exterior canopy posts/beam removed. Existing roof projection is explicitly a **post-free cantilever study**. No inferred adequacy of existing 45×145 rafters; backspan, moment connection, deflection, uplift and anchors unresolved. Interface has null capacity/fasteners. This must not be displayed as a solved load path.
- Sauna front deck has a 1200mm side return and connecting corner beside the shower side. Independent study joists/bearers/pads retained. Deck waterproofing, drainage, foundation capacity and connection design remain open.
- Area screen now conservatively encloses roof, deck return and log rack in a common XY bound. Standard configurations remain below50m². Height and dimensional span gates remain; these gates are not structural verification.
- Export catalogue omits Studio sloped/gable entries. Studio UI source disables them and selects flat. Website pin/deployment unchanged in this development work.

## Research and limitations
Primary manufacturer sources reviewed 2026-09-26:
- https://morsoe.com/other/product/indoor/wood-burning-stove/p1442_int : Morsø1442 body H715×W388×D368mm, nominal5.9kW on this regional page. Used dimensions only; no heat-load sizing or product approval claimed. Regional product revisions/manuals must be reconciled before selection.
- https://morsoe.com/images/com_hikashop/upload/72146800_-_1400_n-en_uk_-_defra_40713311.pdf : manufacturer installation instructions initially retrieved; later request returned404. Do not treat this unstable UK manual URL as a pinned Lithuanian installation specification. Requires clearances, hearth, combustion air and approved flue; none is silently substituted. Stove body position is a space reservation, **not accepted for installation or operation**.
- https://sunflexuk.co.uk/glass-roofs/patio-terrace-roofs/ : manufacturer shows sliding enclosure of patio roofs for seasonal use.
- https://sunflexuk.co.uk/help-advice/choosing-sliding-doors-for-your-patio/ : thermally broken systems differ from simple frameless seasonal glazing; performance depends on specification.

Sliding geometry remains a generic OBTP library placeholder, not a SUNFLEX product or supplier-derived frame profile. No U-value assigned. The court retains its ventilated/deck floor and uninsulated ceiling area. Closing glazing provides a seasonal enclosure study, **not an insulated winter room and not demonstrated energy savings**. An insulated heated centre requires a separate floor/ceiling/threshold/vapour-control design and changes thermal zoning. Stove/flue fire separation and both door swing/operation zones require review before fixing its location. No invented chimney through current roof members.

## Verification scope
Portable model/drawing tests, standard states and dimensional gates; native Rhino/GH not executable here. No thermal/structural solver results. Wind/snow remain paused by owner. Production website publication is not part of this GH development checkpoint.

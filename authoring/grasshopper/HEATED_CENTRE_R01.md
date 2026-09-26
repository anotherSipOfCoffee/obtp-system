# Heated Studio centre — owner decision 2026-09-26

Supersedes R08's unheated seasonal buffer assumption. The centre is intended as a heated winter room, with large sliding glazed openings for summer.

Implemented in the canonical GH/Python source:
- Continuous existing 18mm floor cassette sheathing through the centre replaces gapped deck boards.
- Existing 220mm floor and ceiling cavities filled around actual framing using the same subtraction routine as the rest of Studio.
- Centre ceiling uses existing 16mm lining and20mm battens.
- Heated area includes the centre; conceptual/detailed plans and sections still derive from model parts.
- Thermal inputs explicitly describe winter closed / summer open; glazing U-value, airtightness, threshold psi and operating schedules remain required inputs.
- Assembly requirements record continuous air/vapour control, underside protection, insulated load-bearing sill support, drainage and head/jamb joints. These are unresolved specifications, not invented product geometry.

Primary research:
https://www.schueco.com/lt/architektams/gaminiai/slankiosios-sistemos/sliding-and-lift-sliding-systems-/ase60
https://www.schueco.com/resource/blob/4645932/bd8cc605f4c00f3939a277642de623b6/ASE%2060.pdf?domain=in
https://www.reynaers.com/products/sliding-folding/masterpatio/multirail

Schuco ASE60 provides thermally insulated sliding/lift-slide systems with triple-track arrangements. Candidate only: existing model profiles are generic OBTP placeholders. The1632mm clear central bay gives approximately577mm leaves in the current three-panel layout; minimum leaf dimensions, actual frame depth, safety glass and hardware must be confirmed before selecting this product. No manufacturer U-value is applied to an unverified assembly. Two-panel sliding is a possible fallback but reduces open width; widening the central bay is a layout decision, not applied silently.

Heater remains Morsø1442 body envelope, not a selected installation. Existing location is not certified to combustible clearances. Do not operate from this model. Heat demand, hearth, combustion air, flue clearance/penetration and egress require resolution. No energy-saving calculation or thermal approval. Post-free canopy structural holds remain.

Native Rhino/GH execution pending. Wind/snow paused. Changes are on the development branch; no production deployment.

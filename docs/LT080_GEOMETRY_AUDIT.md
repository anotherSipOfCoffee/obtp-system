> Historical research/checkpoint, retained intentionally. Not the current project rulebook. Read ../project/PROJECT_MAP.md and current variation documentation first.

# LT080 geometry audit — 2026-09-23

## Result
HOLD: the retrieved sources do not fully define a faithful three-dimensional tenon/mortise pair. No LT080 joint geometry has been generated or published. This corrects the earlier implication that the available dimensioned sheet would necessarily be sufficient.

## Inspected evidence
Manufacturer drawing, visually rendered and inspected:
https://cdn.shopify.com/s/files/1/0686/4456/9356/files/LT080_Dimensions.pdf?v=1689282969
One A3 page. PDF title: LTA1003 Zapfenschablone LT080 v14-Kopieren.
SHA-256: 999eb81270370e72e44c95c10fad2335525e27d1fa671034aa43af13bae81062

The page combines template photographs, a gridded timber/template illustration, an assembly illustration and template/profile dimensions. The 8-degree annotation spans the two inclined sides; it must not be applied independently to each side. Labels 67, 254, 330, R25 and 18.50 occur around the template/profile view. They are not an unambiguous complete finished-joint specification. BB/BH and ZB/ZH label timber/tenon dimensions without defining a complete paired 3D machining profile. Do not copy template radii directly to finished timber.

Current product page:
https://www.lignatool.at/en/pages/dovetail-milling-jig
Lists LT080 tooling range, separate flank angle and several tenon lengths. These describe tooling possibilities, not a selected complete joint. Bearing/cutter relationships and setup matter.

Older manufacturer brochure, hosted by regional distributor:
https://lignatool.sk/img/gallery/system-rybiny/downloads/Lignatool_Prospekt_2016_EN_rgb-_email.pdf
Explains the machining sequence but does not close the geometry gaps. Its LT080 range differs from the current page; do not mix generations.

## Inputs still required
| Input | Why it matters |
|---|---|
| Dimensioned finished tenon and corresponding mortise, preferably sectioned CAD | Establishes actual mating surfaces rather than template guide edges |
| Cutter profile and guide-bearing geometry, or a manufacturer-defined direct finished profile | Converts template geometry into machined geometry |
| Selected tenon depth and reference face | Controls shoulder and residual timber |
| Assembly clearance / fit specification and mortise depth allowance | Avoids silently inventing either zero-clearance or arbitrary offsets |
| Bottom termination geometry and placement relative to beam top | Determines rounded surfaces, insertion and bearing |
| Applicable product/tool revision | Prevents combining incompatible data |

Structural capacity, timber grade, moisture/service conditions, edge distances and uplift restraint are additional checks. They cannot be inferred from tooling range. A nominal source reproduction and a construction-ready connection are different milestones.

## Next actionable input
Obtain the manufacturer's finished-joint CAD/drawing for one LT080 setup, or the machining manual with the cutter and bearing dimensions plus fit specification. Link or upload is sufficient. No supplier message has been sent.

When received: model that one fixed specimen first in Rhino/Grasshopper, test solids and insertion, export its meshes to web, then expose only documented variations. Keep the independent-frame model unchanged until compatibility is checked.

The documentation gap is specific to faithful LT080 reproduction. It does not mean all timber joints are undocumented. A different fully dimensioned research specimen is a possible alternative, but has not been substituted without informing the owner.

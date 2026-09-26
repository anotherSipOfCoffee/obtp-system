# R10 — website presentation and coordinated model fixes
Owner request26September2026 authorizes implementation and publication.

Studio becomes the website default; sliders are fixed to open presentation, with winter state retained in GH. Website hides the redundant terrace-depth and sliding-state inputs. Main / Pagrindinis replaces Module type; three owner-supplied renderings fill existing gallery locations, with new original bilingual introduction inspired by Koto's spacious presentation (https://koto.co.uk/). Images are illustrative, not measured geometry.

The separate600mm log rack is replaced by600mm extensions of both long walls on the left short end. Roof weather assembly and bearing lines extend over this open niche. Heated wall/inside room dimensions stay intact. Shared wall_run creates framing; matching timber facade and niche deck use the canonical materials. No enclosed extra room. Area bounds include the projection. Connections/foundation/cantilever engineering holds remain.

cut_view.py clips every solid category to floor+1100mm for web and GH: removes above-plane solids and caps intersected axis-aligned prisms. Current generated inclined roof solids sit above plane and are removed. A future partially intersecting inclined recipe is explicitly rejected pending a suitable clipping implementation, rather than silently rendered full-height. No original scene, quantity or analysis data changes during display cuts.

Incorporates existing R09 native preview controls and explicit local-package loader from branch fix/gh-part-preview-r09 at dc26315826bf50fd34f1b7bd167605c6d768a989. Native execution remains unverified. No supplier approvals/thermal results introduced. Wind/snow paused.

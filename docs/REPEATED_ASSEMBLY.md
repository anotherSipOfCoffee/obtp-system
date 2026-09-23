# Repeated open assembly

System owns multiAssembly(bays, layer), used by Studio. Range 1–8 is a viewer scope limit, not a structural span approval. Repeat pitch 600 mm and span 4572 mm come from the pinned source geometry; shapes remain unchanged.

Each bay reuses assembly(layer) translated by 600 × bay index along X. Full view adds wallPair()'s twelve full ties at each front wall seam, translated by Z=380 mm. Opposite-wall seam ties use the same pair rotated 180° about Z with translation (1200 + 600 × seam index, 4572, 380). This maps its two W-S objects exactly onto the opposing assembly walls. Each seam has 24 ties total. IDs distinguish every instance.

Full-view quantities for N modules: F-S N, W-S 2N, R-S N, full ties 48N−24; total 52N−24. Layer views omit ties just as the original slice did.

This composes previously sampled local interfaces; no new full-volume fit or strength validation is claimed. Adjacent floor and roof modules are set out on the source pitch, but their seam fastening remains unresolved and is not invented. End closures, corners, openings, foundations and bracing are absent. One source roof Brep remains open. This is an open assembly study, not a complete or construction-ready shell.

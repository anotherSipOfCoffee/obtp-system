# OBTP state observed 28 September 2026

This is a dated inventory, not a moving latest-version declaration. Recheck branch heads before development.

| Source | Observed commit / status |
|---|---|
| System main | `f719830320fb2d6b9eaa2e55b5ddeec41dbe644b` |
| System GH R25 review | `c988f622c63d5d4601c04f754ecdd0ca263c9cdf`, PR #24, unmerged |
| Studio main | `74c36395adedbe0eaa666c56de4d28fb0d05b2f8` |
| Studio System pin | `724c70c4165bbed23f0ce0dc811466bff15c9987` — intentionally distinct from System main and R25 |
| Architecture main | `8a22fd870f571737153c8bc202376b49dbe56802` |

R25: Sauna preset → layout → cassette → 3D; six saved presets plus Custom. Bounded strip custom arrangements are implemented. Outdoor-only/nonrectangular layouts remain unsupported. Portable checks and export solids are recorded in its review; native Rhino/GH and engineering acceptance remain outstanding.

Studio's public source offers the two M-with-storage presets, fixed design options, read-only hatched alternatives, model/drawing views and three cladding-free review PDFs. Its System pin is not changed by R25.

Architecture's 24 R04 plan studies include dressing pockets. The existing 3D/cuts remain separate. Supplier-based future integration is a proposal governed by its AGENTS.md, not an implemented dependency.

The old v76/2026-09-23 Drive packages and R22 are historical. [Storage policy](STORAGE_POLICY.md) replaces the old Drive-master workflow. Cleanup changes documentation only; branch/runtime/workflow/lock bytes and deployment state are preserved.

System #8 and Studio #41 remain open review work; no potentially unique branch is deleted or force-merged. No engineering, product compatibility, permit, thermal or safe-lifting approval is implied.

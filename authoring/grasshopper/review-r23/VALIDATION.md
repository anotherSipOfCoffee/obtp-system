# R23 validation

- Full portable suite: **86 tests passed**. Includes 106 accepted custom geometry candidates and two rejected cases from inherited checks.
- Final eight layout tests passed after the inactive-outdoor fixture correction. They cover all seven nonempty room selections and all feasible strip orders, typed edges, conflicts, stale-plan rejection, dimensional propagation and source immutability.
- Twelve S/M/L × storage × roof comparisons: outdoor-active scenes match the existing geometry, IDs, config and drawings exactly. Outdoor-inactive scenes match all existing parts except three explicitly omitted shower fixtures; walls and openings match exactly. This is a programme change, not a part-standardization reduction.
- Python source compilation passed for the native-definition generator and all component scripts.
- Four generated floor-plan diagrams inspected: existing arrangement, two rooms, sauna + outdoor, alternative order. Coloured zones are coordination envelopes; they are not detailed construction plans. Existing downstream drawings remain available for supported constructions.
- Native Rhino/GH is unavailable here. Component creation, native Text Tag availability, live sliders and native preview/export execution remain unverified. Portable source checks do not claim native host acceptance.
- Baseline for this change: System commit `03ace4114cdb96361d683c86803e818372c32121`. Its GitHub authoring and independent cassette workflows both completed successfully.

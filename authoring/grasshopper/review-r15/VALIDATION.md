# Validation status

- Existing Python suite: 38 tests passed in 139.6 seconds, including all 216 configurations, structural collision checks, model/drawing identity and PDF-disabled export.
- Added manufacturing/terrace/GH checks: 6 tests passed. PDF-disabled regression rerun passed.
- 216 browser-model configurations and 12 native-format Rhino exports generated with local rhino3dm 8.17.0; this is portable validation, not native Rhino acceptance. CI uses the existing pinned rhino3dm 8.35.0.
- WikiHouse catalogue/seam, Cassette geometry/connections, Matrix and Studio preset/function/subblock regressions passed.
- Studio cache integrity: 12 tests passed. JavaScript syntax checks passed.
- Local browser launch blocked by cloud socket restrictions. Non-deploying GitHub Actions passed: System runs 36269551040 and 36269551062; Studio run 36269662595, including desktop/mobile/language/round-trip/WikiHouse/PDF controls and the six-model review. Screenshots are in that run’s studio-visual-check artifact. No local browser pass is claimed.
- No engineering or native Rhino/GH acceptance claimed.

Final niche-bearing correction adds eight fully counted physical pieces to Studio. Its support test passed; all representative structural collision cases passed (5.1 seconds). Final source-pin CI checks govern the completed review revision.

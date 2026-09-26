# Validation status

- Existing Python suite: 38 tests passed in 139.6 seconds, including all 216 configurations, structural collision checks, model/drawing identity and PDF-disabled export.
- Added manufacturing/terrace/GH checks: 5 tests passed. PDF-disabled regression rerun passed.
- 216 browser-model configurations and 12 native-format Rhino exports generated with local rhino3dm 8.17.0; this is portable validation, not native Rhino acceptance. CI uses the existing pinned rhino3dm 8.35.0.
- WikiHouse catalogue/seam, Cassette geometry/connections, Matrix and Studio preset/function/subblock regressions passed.
- Studio cache integrity: 12 tests passed. JavaScript syntax checks passed.
- Local browser launch blocked by cloud socket restrictions. Browser/UI and visual checks are delegated to the existing non-deploying GitHub Actions workflow; status recorded in PR checks. No local browser pass is claimed.
- No engineering or native Rhino/GH acceptance claimed.

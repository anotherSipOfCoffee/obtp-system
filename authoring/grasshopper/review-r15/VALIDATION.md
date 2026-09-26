# Validation status

- Final Python suite: 45 tests passed in 132.6 seconds, including 216 configurations, structural clashes, opening clearance, drawing/source identity, terrace direction and supported joints, continuous terrace corner, niche floor supports, direct opening-jack bearing and repeated side plates, identity normalization and PDF-disabled export.
- All 216 selections recounted for original, first cells, revised and same-footprint revised using the same identity rules and facade exclusion.
- Earlier complete web compilation generated 216 browser models and 12 Rhino exports with portable rhino3dm; final pinned compilation is checked by non-deploying Studio CI.
- Studio cache integrity: 12 tests passed. WikiHouse, Cassette, Matrix, preset, function and subblock regressions passed.
- Local browser launch is blocked by cloud socket restrictions. Browser verification runs in non-deploying GitHub Actions; run 36270515193 passed before the final terrace-corner change. The final pin's workflow and artifacts are linked from the PR.
- No engineering or native Rhino/GH acceptance claimed. No merge or deployment performed.

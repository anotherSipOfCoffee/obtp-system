# R16 validation

- Final Python suite: **51 tests passed in 140.231 seconds**. Includes 216-configuration coverage, source/export identity, opening bearing, terrace direction and supports, ordinary bay identity, and disabled PDFs.
- New tests check all wood categories for clashes over 24 representative configurations, full-width supports behind new lining joints, facade-batten joints, roof-rail splices, deck/trim separation and bearing, and court glazing/head clearance in open/closed states.
- All 216 selections recounted across original, first cells, opening controls, repairs-only control, current and same-footprint current using identical manufacturing rules and facade exclusion.
- Model-derived cut comparison visually inspected. Final Studio pin is validated through its non-deploying CI, which generates 216 browser models, 12 portable Rhino exports and browser screenshots. The final workflow is linked from PR #37.
- Local browser launch is blocked by cloud socket restrictions; browser QA runs in GitHub Actions.
- Portable rhino3dm validation is not native Rhino/GH acceptance. No engineering certification, merge or deployment.

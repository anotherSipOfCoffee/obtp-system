# R22 portable validation

- The full inherited suite plus initial comparison tests passed: 76 tests, including 106 accepted and 2 rejected custom geometry candidates.
- After merging adjacent insulation cut blanks and removing zero-area source display triangles, all 10 comparison tests passed. These include two added regressions for those changes.
- All five 3DM review exports were written, reopened and their object counts reconciled. The B exports were regenerated after the insulation change: default full model 168 pieces, 31 provisional types, 20 rib joint interfaces, 9 assembly groups.
- Actual-source PNG axonometrics use a depth buffer; inspected WikiHouse W-S, Studio M with storage, B frame, insulated B and knee context. No generated concept images substitute for model geometry.
- Existing three default Studio PDF recipes regenerated unchanged. The source test suite checks document scope and source identity.
- The Rhino 8 GH generator and components compile as Python source, but native RhinoCommon/GH execution is not available in this cloud environment. The package contains the native-definition generator, not a pre-generated .gh binary.
- No structural solver, COMPAS Wood kernel, lifting assessment or supplier qualification has been executed. Do not interpret a closed portable solid or a collision-free cavity as engineered capacity.

The GitHub authoring workflow repeats the whole suite and generates the R22 package without building or deploying a website.

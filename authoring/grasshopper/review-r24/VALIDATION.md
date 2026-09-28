# R24 validation

- Nine workflow tests pass: twelve exact preset/roof comparisons; native-number normalization; ignored custom fields for saved presets; active custom dimensions; unsupported-layout rejection; stale-input rejection; input validation; no geometry before construction; no obsolete main-canvas path.
- Both host-input tests pass. One executes the actual preserved research model script; the other executes the actual new preset and cassette component scripts for all seven choices with Grasshopper-style wrapped values. These are portable host-script checks, not native Rhino execution.
- Seven manufacturing tests pass, including normal-preview/removed-control checks. The existing canvas-input test was retargeted to the preserved research creator after the main canvas changed; the new main sequence has its own execution test. The preview label assertion now matches “3D model”.
- Extracted ZIP: all checksums verified and all seven selections generated nonempty geometry. A Custom scene exported and reopened with 1607 matching Rhino objects.
- Main Python scripts compile. Generated M/no-storage, M/storage and Custom planning diagrams inspected. Diagrams show planning zones; detailed drawings remain downstream from the same cassette scene.
- Full portable CI remains enabled. Native Rhino/GH canvas construction, live wiring, labels, slider behaviour and native export still require host acceptance.
- Websites were neither changed nor deployed. Other systems and Studio remain in the separate research creator and canonical modules.

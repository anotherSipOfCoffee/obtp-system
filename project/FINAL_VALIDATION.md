# OBTP v76 final validation

All three source packages were checked file-by-file against GitHub Git blob hashes at their included commits. ZIP integrity checks passed.

- System independent geometry/browser: https://github.com/anotherSipOfCoffee/obtp-system/actions/runs/35908393392 — success
- Existing System/WikiHouse browser: https://github.com/anotherSipOfCoffee/obtp-system/actions/runs/35908393270 — success
- Prepared Studio v1/v2/v3 build/browser: https://github.com/anotherSipOfCoffee/obtp-studio/actions/runs/35908494398 — success
- All 16 cassette count/height combinations: no positive-volume overlaps; continuous end-wall framing; connected graph; each interface point touches actual geometry on both sides.
- Original W-S and catalogue/seam tests pass.
- Studio v1 and Architecture runtime files: byte-identical to pre-task versions.
- Architecture: eight JS script blocks and two JSON blocks parse. No new Architecture integration was needed.
- All three Pages workflows: byte-identical; main branches unchanged. No deployment performed.
- Rhino reference: 166 valid closed Breps, Rhino 8 file read/write count agrees. Windows Rhino/Grasshopper and physical construction not tested.

Download the local preview ZIP. OPEN_CASSETTE.html is self-contained; full Studio uses a local HTTP server as described in START_HERE.txt. The Studio HTTP build and controls were browser-tested; the standalone convenience HTML is a packaging variant.

Structural capacities, tolerances, fasteners, egress, roof weathering, envelope/moisture/ventilation and Lithuanian compliance remain unvalidated. This is a geometric research prototype.

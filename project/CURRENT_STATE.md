# Current state — consolidation checkpoint
2026-09-23

## Complete before this storage migration
- Three separate repositories and GitHub Pages sites exist.
- System's original interface structure is restored with eight source-based objects: W-S, C-S-1, E-S, F-S, W-O-S-1, R-S, full tie and half tie.
- Wall/wall, floor/wall and wall/roof views, plus a four-block open slice with 24 ties.
- Source hashes checked. All imported CAD objects valid; one R-S Brep open.
- 48 floor/wall and wall/roof sampled sections: maximum reported overlap 0.695739 mm². This is not full-volume or engineering validation.
- Browser workflow run 35890259122 passed at af10fefa98e34eac60682bfc2c9f513b854a8279; desktop/mobile screenshots inspected. See docs/BROWSER_CHECK_REPORT.json.

## Storage decision
GitHub is authoritative. Drive v74 is superseded as a current handover, but preserved as historical evidence. All 196 original v74 files survive in its byte-exact archive; project/archive/v74/FILE_INVENTORY.json records their hashes. Shared Rhino pilot files are additionally extracted under project/shared/ for practical use.
Original selected CAD is stored permanently under sources/skylark150/. The prior seven-day Actions artifact is not the durable source. No Git LFS pointers are used.
The v74 ZIP is stored as three verified binary parts to satisfy the GitHub plugin request-size limit. tools/restore_v74.py reconstructs the original ZIP byte-for-byte. Drive snapshots contain the restored whole ZIP and extracted CAD, as well as the three repository exports.

## Next authorized work
Prepare the full illustrated technical PDF report from current GitHub evidence. Include the corrected user intent, actual component library, source provenance, Rhino-to-web workflow, interface checks, screenshots, assembly scope, source defects and next steps. Do not claim it is already written.

## Remaining technical work
Rhino 8 Windows comparison; resolve the source roof opening; establish corner/end-floor and opening placements; extend the open slice only with supported source connections. No closed building or engineering approval is claimed.

## Project boundaries
Studio and Architecture visual behaviour remain unchanged by this consolidation. System has not been integrated into their model generation. Their app-specific rules remain in their own AGENTS.md files.

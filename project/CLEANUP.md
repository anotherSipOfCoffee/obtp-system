# Consolidation and cleanup record

## Inspection

All three current repository trees were fetched via the GitHub plugin and compared to the local v75 export using Git blob hashes. Every baseline file matched after fetching newer Studio/System files. Architecture already matched v75. Dynamic catalogue loading, System copying in Studio, direct W-S routes, Rhino tools, source locks and workflows were checked before classifying files.

The Drive inspection covered the active project folder, 36 entries in the old release archive and 11 entries in its earlier G2 folder. Historical ZIP member contents were inspected and hashed. Older versions contain both duplicates and unique documents; filenames alone were not used to discard them. The old standalone web export had all 13 members already represented in inspected historical packages. The Cloudflare bundle contains obsolete nested deployment exports, not the current GitHub runtime.

## Removed from active development after verified recovery

- System project/archive/v74: three embedded backup chunks plus their reconstruction manifest, inventory and README. They are historical backups, not application dependencies.
- System tools/restore_v74.py, tools/build_project_snapshot.py, project/SNAPSHOT_REQUEST.json and .github/workflows/project-snapshot.yml: obsolete machinery whose only purpose was rebuilding the old nested v75 backup. The source manifest is updated to retain only current CAD source bundles.
- Superseded full duplicate coordination instructions: project/00_START_HERE.md is now a short pointer. Root start guides, READMEs, agent guides, current state and latest-baseline pointer now describe the actual Drive-master relationship and separate development branch.
- Old loose Drive packages, PDFs and starter/link documents move out of the active parent into historical originals. The former archive folder moves under the separate recovery folder. Original Drive IDs/history are retained; no permanent deletion is necessary.

## Intentionally retained

Studio v1; every WikiHouse mesh and CAD bundle; CC BY-SA attribution and source terms; source locks and fit audits; direct dist/ws viewer, its tests/exporter and model (intentional independent inspection route); the Rhino offline pilot and user export evidence; useful historical connection research (labelled historical); Architecture catalogue, privacy/configuration files and all runtime code. The Architecture _headers file is retained as existing hosting configuration rather than guessed obsolete.

No unused third-party dependency manifests were found. Static dist files are the actual application source, so deleting dist as “build output” would break these projects. The generated Studio dist/system-source copy, screenshots, test output and Python caches are ignored; delivered previews/test evidence remain explicit artifacts, not extra editable sources.

## Recovery and limits

A dated compressed recovery was generated before removals and verified by reconstructing and hashing every stored file. The initial byte-exact-container version exceeded the connector's 100 MB limit; the uploaded version expands historical ZIPs and deduplicates their member contents. Original ZIP containers remain in historical Drive originals, preserving their exact bytes and IDs. Repository files, including removed backup chunks, are preserved exactly in recovery. See RECOVERY_RECEIPT.json for checksum/size and the Drive master manifest for the uploaded location.

No live site, main branch, repository visibility or Git history was changed. Existing Pages deployment workflows are retained byte-for-byte. Removing the obsolete backup workflow changes only historical packaging, not application builds/deployment. A future agent must compare new GitHub heads against the recorded baseline before further integration.

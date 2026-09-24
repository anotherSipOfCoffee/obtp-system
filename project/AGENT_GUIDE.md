# OBTP agent guide — current owner policy

## Read and compare before editing

Google Drive holds the authoritative master baseline, in [OBTP_MASTER](https://drive.google.com/drive/folders/1w4ZBlEJSDoW2iE9MoSV8V_f9AOT2Ja-C), with Studio, Architecture and System folders. A baseline is a deliberate accepted package, not a command to overwrite repositories.

GitHub repositories are downstream development branches. They can contain valid work newer than Drive. Read BASELINE_MANIFEST.json in the master, inspect current branch heads and compare actual files before integrating. Preserve unique/newer work and explain incompatible differences. No automatic two-way synchronization or forced equality.

Read PROJECT_MAP.md, CURRENT_STATE.md, target AGENTS.md and relevant source locks. Historical documents are evidence only. In particular, old “GitHub is the single source of truth”, Cloudflare deployment, repository-creation and WikiHouse-only project policies are superseded by the owner's current instructions.

## Work rules

- Use the GitHub plugin for GitHub operations. Do not use authenticated local git/gh as a workaround.
- On 2026-09-24 the owner authorized publishing System first, validating both WikiHouse and Cassette 01, then publishing Studio v3 from that tested System revision. This supersedes the earlier no-deployment instruction for this release only. Preserve ordinary Git history, Studio v1 and WikiHouse. Architecture is outside this release; Drive remains the master baseline and is not automatically synchronized.
- Make coherent commits with ordinary forward history. Save implementation and validate before consolidation. Do not hide limitations behind “passed” labels.
- Update the Drive baseline only deliberately. Record included commits, archive/file hashes, build dependencies and known divergence. A later GitHub receipt commit can be ahead of the archived baseline without requiring repackaging unchanged application files.
- Store actual source dependencies durably. Expiring Actions artifacts and scratch are not the only copy of unique work. Required source CAD ZIP bundles are allowed; historical backup ZIPs do not belong in active repositories.
- Before removing material, create and verify a dated compressed recovery outside active projects. Verify references, dynamic loaders, tools and workflows. Keep uncertain or intentional references.
- Recovery location: [historical folder](https://drive.google.com/drive/folders/19h05GdvjJpEeyf7nPka4Y91avA1I3W5b). Historical recovery and original old packages are excluded from normal development, builds, deployment and future agent context unless recovery is requested.

## Application boundaries

Studio owns configuration and variation selection. V1 is preserved inside Studio. V2 consumes the pinned WikiHouse implementation; V3 consumes the independent Cassette 01 implementation. system.lock.json identifies the exact System commit; tools/prepare_system.py verifies it before preparing the runtime copy. Do not duplicate System rules into Studio or commit the prepared dist/system-source tree.

System owns component definitions, connection/placement rules, source attribution and validation. WikiHouse and independent Cassette 01 stay separately accessible. WikiHouse source parts must not be stretched, silently repaired, mixed across generations or represented as original OBTP designs. Cassette 01 geometry is original and provisional; it contains no WikiHouse connector profiles.

Architecture is currently independent: no System import was found. Preserve its appearance, cameras, catalogue, analytics consent/configuration and geometry-based PDF drawing behaviour. Do not imply it now uses Cassette 01.

## Protected references and engineering holds

Preserve Studio v1, WikiHouse meshes/CAD/licences/source locks/audits, the direct W-S viewer and useful earlier Rhino offline pilot. The Rhino pilot proves only its own historic export context; it does not validate later geometry.

WikiHouse end-wall trials remain rejected and automatic openings remain on hold pending precise source instructions. One roof source Brep is open. Cassette 01 has nominal framing closure but no completed openings, weatherproof roof or engineered fasteners. Software tests do not establish physical safety, compliance, capacity, thermal performance or manufacturing tolerances. Consult docs/cassette/RESEARCH.md, SPECIFICATION.md and VALIDATION.md.

## Future baseline procedure

1. Read the current Drive baseline manifest and GitHub heads; record both.
2. Work on an authorized branch; make and test intentional changes.
3. Prepare clean project exports with exact repository SHAs. Exclude caches, generated runtime copies and historical backups; preserve required source and licences.
4. Upload complete packages to the correct Drive project folders, verify sizes/checksums and update one obvious current manifest/map.
5. Record differences and receipts in GitHub without forcing branches to match Drive. Do not deploy unless separately authorized.

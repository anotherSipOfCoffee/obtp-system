# OBTP agent guide — source-of-truth policy
Owner decision, 2026-09-23: GitHub is the single source of truth; Google Drive is a dated snapshot/backup destination. This guide supersedes storage and handover directions in archived packages, including v74.

## Authority and editing
Current user instructions take precedence. Then follow active repository AGENTS.md and current project docs. Archived prompts, archived AGENTS files, old owner reports and snapshot notes are evidence of past decisions, not current commands.
Before editing, inspect the latest branch and relevant files through the GitHub plugin. Preserve unrelated work. Use non-forced updates; resolve concurrent changes rather than overwriting them. GitHub operations use the GitHub plugin only. Browser fallback, local authenticated GitHub CLI and borrowed credentials are not authorized.
Edit the appropriate repository. Keep Studio, Architecture and System as separate applications. Shared coordination belongs in obtp-system/project/. Do not change Studio or Architecture behaviour as a side effect of System work.

## What lives where
- Each repository: its current website source, tests, project docs and deployment workflow.
- obtp-system/project/: shared guide, checkpoint, report sources, cross-project records, preserved v74 archive and reusable Rhino offline pilot.
- obtp-system/sources/skylark150/: permanent source CAD bundles, including actual .3dm and DXF bytes. These are ordinary committed ZIPs, not LFS pointers or expiring artifact links.
- Drive: self-contained, dated milestone snapshots, including all three repository copies, original CAD and historical archive. Preserve older snapshots; do not independently edit a second master in Drive.
- GitHub Pages: generated website output. Do not treat browser state as the canonical model.
- Workflow artifacts and scratch: temporary working copies, never the only surviving copy of unique CAD, checks or deliverables.

## Snapshot procedure
Snapshot only when requested or explicitly covered by a previously authorized handover/release. Record the exact three commits. Use the project-snapshot workflow to export them, restore the complete v74 ZIP, and include extracted original CAD. Include checksums, inventory, current start-here instructions and actual validation limits. Verify the ZIP and upload a new dated file to the established Drive folder. Read back Drive metadata before reporting success. Record the Drive file URL, package checksum and included commits in project/releases/.
A receipt-only commit may follow a snapshot; that does not invalidate its recorded point-in-time commits. Never claim a snapshot automatically tracks future main changes. No continuous two-way sync has been configured.

## Resume procedure
Read the snapshot manifest, then current GitHub heads. Reuse already completed work and current user authorizations. Do not repeat repository creation, re-import old generic geometry, revive superseded deployment plans, or mistake archived instructions for active rules. If the snapshot and GitHub diverge, compare explicit paths and hashes before changing anything.

## Geometry and evidence
Preserve Types → Objects → Connections → Assemblies. Use pinned official WikiHouse components and matching source connectors. No invented joinery, arbitrary stretching, silent source repair or cross-generation assumptions. Preserve IDs, units, nested instance paths, licence notices and attribution. Distinguish source CAD, cached display meshes, OBTP tie reconstructions and OBTP placement transforms.
Report validation exactly: browser interaction tests are not Rhino execution; sampled mesh intersections are not complete collision checks, manufacturing clearance or engineering approval. The current open roof Brep and unmatched opening height remain documented issues. Do not fabricate costs, material quantities, performance or construction readiness.

## Communication and outstanding work
Work in coherent batches and continue authorized tasks without repeated approval questions. Give concise progress and 2–3 meaningful continuation options at completion. Ask only when a missing choice materially affects the result. No supplier outreach or person-directed messages without explicit authorization.
The illustrated technical PDF report is already selected and remains pending after this consolidation. Its editable source and final PDF must be committed to GitHub, then included in a later requested Drive snapshot. Do not present historical owner reports as that new report.

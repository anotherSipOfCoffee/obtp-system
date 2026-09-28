# OBTP storage and authority

Owner direction confirmed 28 September 2026. Covers System, its Grasshopper code, Studio and Architecture.

| Location | Authority and purpose |
|---|---|
| GitHub System | Canonical construction geometry, GH creators/components, part identities, drawings, quantities, source dependencies, tests and technical decisions. |
| GitHub Studio | Customer website/configurator, presentation and integration with its exact System pin. |
| GitHub Architecture | Independent architecture application, layout catalogue, drawing sources and its project-specific rules. |
| Google Drive | Launch planning, supplier/engineering documents, commercial work, reference studies and deliberate historical records. |
| Published websites | Generated/published output. Never recover authoritative source by editing deployed files. |

## GitHub workflow
- Inspect the actual branch/commit and relevant PRs. `main`, an unmerged review branch and a public deployment are different states.
- System GH R25 is review work in PR #24 on `feat/aligned-platform-assembly`, not `main`. Its source is `authoring/grasshopper/`; `CREATE_GRASSHOPPER.py` creates the native definition in Rhino. Keep all bundled modules beside it. Native acceptance remains outstanding.
- Studio consumes its exact `system.lock.json` revision. Updating System does not update Studio automatically. Never duplicate canonical geometry formulas in Studio or repin during housekeeping.
- Architecture remains independent; cleanup does not integrate its generator with System.
- Keep permanent source CAD, licences, pinned product/source records and unique research sources. Generated exports must identify their source commit and configuration; they are not another editable model.
- Prefer review branches/PRs for changes. Remote writes use the GitHub connector. No history rewriting, branch deletion, supplier outreach, merger or deployment is implied by cleanup.
- Ordinary package creation does not require copying all three repositories to Drive. GH release packages should be built from a recorded commit using the repository packaging tool. Do not promote a review package to a release merely because a ZIP exists.

## Drive workflow
Keep Drive: it supports the launch plan and document collaboration; it is not needed to execute GH or maintain source code.

The former OBTP_MASTER folder is now **OBTP_PROJECT_DOCUMENTS** (same folder ID). Its project folders hold documents/references; Project Management holds the launch plan. Code pointers lead to GitHub rather than duplicated working code folders.

Historical v76 source/preview ZIPs and GH R22 are archived outside the active document folders. Preserve original file IDs, revision history and recovery records. Old validation applies only to its stated revision. Research proposals are not proof of implemented or approved construction.

Do not repeatedly export whole repositories just to keep Drive looking current. Optional milestone backups require a deliberate purpose, exact commits and verified checksums, and remain read-only history. No automatic two-way synchronization.

## Continuing work
Read the target repository's AGENTS.md and relevant current source first. Use project/PROJECT_MAP.md for routing and project/CURRENT_STATE.md as a dated observation. Read historical handoffs only for a specific recovery question. Software validation, native Rhino execution and engineering acceptance remain separate.

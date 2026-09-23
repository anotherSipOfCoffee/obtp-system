# OBTP System
The original Types → Objects → Connections → Assemblies interface, now populated with official WikiHouse Skylark150 source geometry.

[Open System](https://anothersipofcoffee.github.io/obtp-system/)

Six CAD block objects and two source-derived tie objects are available. Three connection examples and a four-block open chassis slice use source sockets and ties. Read [the checkpoint](docs/CATALOGUE_CHECKPOINT.md) and [working rules](docs/SYSTEM_RULES.md) for the evidence and remaining limits. This is not a complete or engineering-validated building.

Run `node tests/catalogue.cjs` for geometry/placement checks. `Check System catalogue` runs browser interactions and captures screenshots. `Import pinned WikiHouse CAD` collects exact official source files without changing them. Rhino 8 verification remains a separate step.

GitHub Pages publishes `dist/`. Root routing fallbacks also support the existing branch-based Pages setting. The previous generic-frame study is preserved at `archive/independent-frame-v02`; its UI structure is retained, but its generic members and assumed bay dimensions are superseded.

WikiHouse team / Open Systems Lab. Source and derived geometry: CC BY-SA 4.0; see [attribution](dist/catalogue/NOTICE.md). OBTP is not endorsed by WikiHouse. Studio and Architecture application behaviour is unchanged. The original Drive v74 package is preserved as historical evidence.

## Authoritative project storage
GitHub is the editable source of truth. Read [Start here](00_START_HERE.md), [agent guide](project/AGENT_GUIDE.md) and [current state](project/CURRENT_STATE.md). All three applications remain separate repositories; shared coordination and the historical v74 material live under project/ here. [Permanent source CAD](sources/skylark150/README.md) is committed as actual file bundles, not expiring artifact links.

Google Drive receives dated, verified, self-contained snapshots built from three pinned commits. See project/SNAPSHOT_REQUEST.json and the Build complete project snapshot workflow. No two-way sync is configured. Snapshot receipts are recorded under project/releases/ after successful upload. The full illustrated technical report remains the next authorized deliverable.

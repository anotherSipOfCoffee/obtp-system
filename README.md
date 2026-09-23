# OBTP System

Independent repository for the System project. Website files are in `dist/`.
Static HTML/CSS/JavaScript; no build or server required.

## GitHub Pages
The deployment workflow in `.github/workflows/pages.yml` publishes `dist/` on pushes to `main` or a manual workflow run. No build step is required.

One-time setup: in repository Settings → Pages → Build and deployment, select **GitHub Actions** as the source. Then run **Deploy GitHub Pages** from Actions, or re-run the initial failed run. The connected plugin cannot change the Pages source setting.

## Active direction
The owner selected the WikiHouse structural system. See [current rules](docs/SYSTEM_RULES.md) and [pinned source files](docs/WIKIHOUSE_SOURCE_LOCK.json). The previous independent-frame study is preserved on branch `archive/independent-frame-v02`. The active application now lists official W-S under Wall blocks, with seven selectable source parts. No provisional frame objects or bay assemblies remain in the active catalogue. This is the first imported block, not the entire WikiHouse library. See [geometry checkpoint](docs/WS_CHECKPOINT.md) for validation limits.

## Historical application status
Imported from OBTP Project System v74 into this public GitHub repository with owner approval. Website files are in dist/. GitHub Pages deployment workflow is committed. Successful GitHub Pages deployment was verified through workflow results in this session. GitHub Pages is the selected hosting target.

The archived v02 study contains eight definitions, two bay configurations and six conceptual interfaces. Its code and tests are retained on the archive branch. For the current catalogue run `node tests/ws.cjs`. Rhino 8 comparison and browser visual verification remain pending; no engineering validation is claimed.

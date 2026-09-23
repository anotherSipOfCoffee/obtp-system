# OBTP System

Independent repository for the System project. Website files are in `dist/`.
Static HTML/CSS/JavaScript; no build or server required.

## GitHub Pages
The deployment workflow in `.github/workflows/pages.yml` publishes `dist/` on pushes to `main` or a manual workflow run. No build step is required.

One-time setup: in repository Settings → Pages → Build and deployment, select **GitHub Actions** as the source. Then run **Deploy GitHub Pages** from Actions, or re-run the initial failed run. The connected plugin cannot change the Pages source setting.

## Status
Imported from OBTP Project System v74 into this public GitHub repository with owner approval. Website files are in dist/. GitHub Pages deployment workflow is committed. A successful deployment has not yet been verified. GitHub Pages is the selected hosting target.

System v02: eight definitions, two bay configurations, six conceptual interfaces. Run `node tests/kit.cjs` and `node tests/interface.cjs`. Read docs/SYSTEM_RULES.md before editing. No engineering validation claimed.

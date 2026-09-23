# OBTP project map

Current master: [OBTP_MASTER](https://drive.google.com/drive/folders/1w4ZBlEJSDoW2iE9MoSV8V_f9AOT2Ja-C), baseline v76 / 2026-09-23. Exact packaged commits and checksums are recorded in its BASELINE_MANIFEST.json and project/releases/v76-2026-09-23.json when the upload receipt is saved.

| Project | Drive master project | GitHub development repository |
|---|---|---|
| Studio | [Studio](https://drive.google.com/drive/folders/1jOwBFn24rVDDqjlFh5nI6upSvWtp0VR5) | [obtp-studio](https://github.com/anotherSipOfCoffee/obtp-studio/tree/dev/obtp-independent-v1-20260923) |
| Architecture | [Architecture](https://drive.google.com/drive/folders/1auSySo9qLSr2stBvnzzxneKAHrNO-L2U) | [obtp-architecture](https://github.com/anotherSipOfCoffee/obtp-architecture/tree/dev/obtp-independent-v1-20260923) |
| System | [System](https://drive.google.com/drive/folders/1-aNqmBKp6WXOoiTNLwM7WRdOaQ9WpDIw) | [obtp-system](https://github.com/anotherSipOfCoffee/obtp-system/tree/dev/obtp-independent-v1-20260923) |

All use branch `dev/obtp-independent-v1-20260923` for this work. Repositories were already public at inspection; visibility was not changed in this task. Drive remains the authoritative baseline, and GitHub may advance independently. Main and live sites are intentionally unchanged.

| Project | Pre-task main / live source | Phase 1 development checkpoint |
|---|---|---|
| Studio | 5bbb1caa6e017b4b702b41747c7b952c4ba1c393 | b286ac2ae29d340e44c7115dfa2459f04dd46abd |
| Architecture | 5db2450cd2e94d193a77cec3ca5bacf04c5d2b0e | unchanged application |
| System | 31fd86e46d11514f19a4e1de07ec622d06238714 | 76106edc9dae6ae711831a87d2d99919e2a84731 |

The previous Drive v75 used Studio c70452343bcda8d24fc454f47f868fd8b4fd960b and System d4f52b62b9957c14d053701ec20b0278ec03edfb; its Architecture commit matches pre-task main. Current GitHub Studio/System already contained later module/seam work. Those newer files were fetched through the plugin and matched against every Git blob before this task's changes; no old package was copied over them blindly.

## Runtime relationship

Studio v2/v3 → system.lock.json → exact System commit → tools/prepare_system.py → prepared dist/system-source. The runtime copy is build output, not a fourth editable project. Studio v1 stays local to Studio. Architecture has no System import and remains separate.

## Recovery

[Historical recovery folder](https://drive.google.com/drive/folders/19h05GdvjJpEeyf7nPka4Y91avA1I3W5b). One consolidated dated recovery ZIP stores deduplicated pre-cleanup files and historical package contents. Old Drive originals are retained in a clearly historical folder to preserve their IDs and revision identity; they are not current masters. Recovery instructions are inside the ZIP. Do not load its obsolete rulebooks for normal agent context.

See CLEANUP.md for removals/retentions and CURRENT_STATE.md for validation and remaining work.

# Contributing to BOSS Cube

Contributions to the generators, model geometry, documentation, and validation records are welcome. Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) when participating.

## Report an issue or propose a change

Use the repository's [Issues](https://github.com/yydrowz3/boss-cube/issues) for reproducible bugs, documentation corrections, and feature proposals. For substantial changes, describe the intended behavior in an issue before implementing them.

Include the affected file or model size, commit identifier, expected and actual behavior, reproduction steps, and relevant Python, dependency, or Bambu Studio versions. Attach small examples, screenshots, or sanitized logs when useful. Distinguish software checks, slicer estimates, and results from an actual physical print.

Report vulnerabilities privately using [SECURITY.md](SECURITY.md), rather than a public issue or pull request.

## Set up a working copy

Fork the repository, clone your fork, and create a branch from the latest `main`. Install Python 3.11 or later and uv. Run the following commands from the repository root:

```sh
# Generate the 35 mm model
uv run scripts/build_model_35mm.py

# Generate the 50 mm model
uv run scripts/build_model.py
```

The generators declare their dependencies in their script headers. uv supplies the runtime environment. Both scripts read `assets/reference/images.jpg`; they write the corresponding models, previews, outlines, and geometry reports under `models/`.

These commands overwrite existing generated files. Use a disposable working copy when experimenting, and inspect the resulting diff before including generated changes in a contribution.

## Make changes that fit the project

- Keep changes focused and preserve both supported model sizes unless the change explicitly requires otherwise.
- Use repository-relative paths in documentation, examples, and output. Locate script resources from the script location; do not embed local usernames, drive paths, or machine-specific directories.
- Keep the English and Chinese versions of documentation consistent, including commands, dimensions, screenshots, and validation limitations.
- Treat `scripts/` as the main source and review delivery copies under `models/*/source/` when changing generators. Updating a main script does not automatically update every delivery copy.
- Preserve the original source, licensing notices, and attribution for third-party material. Do not submit assets or code that you cannot license for inclusion.
- Keep credentials, device identifiers, private network details, and unrelated cache or troubleshooting files out of contributions.

Changes to `SIDE`, `LOGO_WIDTH`, or `RELIEF` may also require updates to assertions, preview dimensions, and export metadata. The 50 mm generator contains fixed dimension values in several places.

## Validate your contribution

For documentation changes, check relative links, filenames, command targets, and consistency between language versions. For script changes, check Python syntax and run the affected workflow in a disposable working copy.

For geometry changes, run the affected generator and review its assertions, `geometry_validation.json`, and `preview.png`. Confirm:

- The body and lettering have the intended dimensions, orientation, and relative positions.
- Meshes are watertight, have consistent winding, and have positive volume.
- Lettering contacts the body's top face and remains within the body's footprint.
- Strokes and internal holes are preserved. The current reference models have 8 lettering components and 14 outline holes.

If a change affects Bambu projects or slicing behavior, inspect the affected project in Bambu Studio, slice it again, and review part assignments, lettering paths, contact layers, filament changes, and material estimates. Record the software version and settings used. Label a physical print test as completed only if it was actually performed.

There is currently no automated CI workflow or dedicated test suite in this repository. Describe the checks you actually ran, including any checks you could not perform, in the pull request.

## Handle project and delivery artifacts

The generic generators do not update configured `_P2S_04` projects, slicing records, or ZIP packages. Keep derived artifacts consistent with the change, and identify any records that no longer describe the updated geometry.

`scripts/prepare_projects.py` derives configured projects from `archive/qa/original50_session.3mf`. It does not consume newly generated generic models or invoke a slicer. It overwrites the corresponding project files.

`scripts/finalize_delivery.py` requires NumPy, trimesh, mesh connectivity analysis dependencies, the configured 35 mm project, and the existing sliced inputs in `archive/qa/`. It reads saved slicing results rather than slicing again. Running it rewrites delivery reports and the 35 mm source copy; manually added inspection fields in reports are not automatically preserved.

Do not run either helper merely to check a documentation change. If modifying their workflow, use matching inputs and explain what was regenerated. ZIP packages under `archive/packages/` are historical snapshots and are not updated automatically.

## Submit a pull request

1. Make a focused change on your branch.
2. Run the checks appropriate to the change and inspect the full diff for unintended generated files or private data.
3. Write commits using the project's [commit conventions](docs/commit-conventions.en.md): an emoji, a Conventional Commits type, an optional scope, and an English imperative description. Explain compatibility changes when applicable.
4. Open a pull request against `main`. Describe the problem, resulting behavior, affected model sizes or artifacts, and validation performed. Link the related issue when one exists.
5. Include previews or screenshots when appearance or slicer behavior changes, and respond to review feedback.

## Licensing

Submit original contributions under the terms applicable to the files you change, as described in [LICENSE](LICENSE). Original project code, documentation, and model geometry are covered by MIT to the extent contributors own those rights. Third-party source, reference artwork, trademarks, and attributed templates retain their respective rights and terms. Do not assume that a model geometry license grants rights to a depicted brand or logo.

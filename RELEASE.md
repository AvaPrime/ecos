# Release Process

E-COS follows Semantic Versioning and Conventional Commits for automated release management.

## Versioning Strategy

- `MAJOR`: Breaking changes (rare in early phases)
- `MINOR`: New features, non-breaking
- `PATCH`: Bug fixes, docs, internal improvements

We use `commitizen` (configured in pyproject.toml) to bump versions and update CHANGELOG.

## Release Workflow

1. Ensure `main` is green (all CI passing).
2. Update `CHANGELOG.md` if not auto-managed (or let commitizen handle).
3. Create and push a version tag:
   ```bash
   git tag -a v0.2.0 -m "chore(release): v0.2.0"
   git push origin v0.2.0
   ```
4. GitHub Actions (future `release.yml`) will:
   - Build distribution (wheel + sdist)
   - Create GitHub Release with changelog excerpt
   - Publish to PyPI (when configured with trusted publishing)

## Current Status (v0.1.x)

Releases are manual until a dedicated release workflow is added. For now:
- Tag and create GitHub Release manually.
- Update PyPI via `python -m build && twine upload` (maintainers only).

See also [ROADMAP.md](ROADMAP.md) and [CONTRIBUTING.md](CONTRIBUTING.md#releases--versioning).

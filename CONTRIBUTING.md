# Contributing to E-COS

Thank you for your interest in contributing to the Event-Sourced Cognitive Operating System!

We follow strict architectural principles: **determinism**, **event-sourcing purity**, **separation of concerns**, and **replayability**. Contributions that violate these will be thoughtfully declined with explanation.

## Development Process

1. Fork the repository and create a feature branch from `main`:
   ```bash
   git checkout -b feat/my-awesome-skill-compiler
   ```
2. Make focused, small commits using [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat: add X`
   - `fix: handle Y edge case`
   - `docs: improve Z`
   - `test: add coverage for W`
3. Ensure all checks pass locally:
   ```bash
   ruff format src tests && ruff check src tests --fix
   mypy src
   pytest -q
   ```
4. Push and open a Pull Request against `main`.
5. PRs require:
   - Passing CI
   - Conventional commit title
   - Updated docs/tests where relevant
   - Approval from at least one maintainer

## Code Style

- Python 3.11+
- Type hints everywhere (mypy strict)
- Ruff for formatting + linting (configured in pyproject.toml)
- Docstrings on all public APIs (Google or NumPy style)
- Keep core runtime minimal; push complexity into skills or projections

## Architectural Guidelines

- Never mutate state directly — go through events.
- Projections must be idempotent and rebuildable from any point in history.
- New core primitives require an ADR in `docs/adr/`.
- Skills should be versioned and schema-declared.
- Avoid shared mutable state between components.

## Reporting Issues

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md) or [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md).

For security issues, follow [SECURITY.md](SECURITY.md).

## Questions & Discussions

Use GitHub Discussions (once enabled) or open a draft PR with "RFC:" prefix for major proposals.

We value thoughtful, principle-aligned contributions over volume.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial production bootstrap of E-COS repository
- Core event sourcing primitives (Event, EventStore, InMemoryEventStore)
- Skill abstraction, registry, and naive compiler
- RuntimeKernel with scheduling, replay, and branching support
- Projection system and StateRehydrator with example AuditLog
- Comprehensive test suite and examples
- Full documentation suite (README, ARCHITECTURE, CONTRIBUTING, etc.)
- GitHub Actions CI (lint, test, typecheck, security)
- Pre-commit hooks and developer tooling (ruff, mypy, commitizen)

### Changed
- N/A (initial release)

## [0.1.0] - 2026-07-15

### Added
- Foundational package structure and public API exports
- MIT license and open-source governance files
- This changelog

[Unreleased]: https://github.com/AvaPrime/ecos/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AvaPrime/ecos/releases/tag/v0.1.0

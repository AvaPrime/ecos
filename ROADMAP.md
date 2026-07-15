# E-COS Roadmap

## v0.1.x — Foundations (Current)

**Status: In Progress / Bootstrap Complete**

- [x] Core data models (Event, Skill, ExecutionPlan, Projection)
- [x] In-memory EventStore + RuntimeKernel
- [x] Naive SkillCompiler + basic scheduling
- [x] Branching and replay primitives
- [x] Example projections and StateRehydrator
- [x] Production repository bootstrap (docs, CI, tooling, tests)
- [ ] Persistent EventStore adapter (PostgreSQL)
- [ ] Improved compiler with basic validation
- [ ] 85%+ test coverage + property-based tests

## v0.2 — Agentic Runtime

- MCP integration for dynamic capability providers
- Agent loop / scheduler with priority and deadlines
- Memory vault implementation using projections + snapshots
- Skill versioning and compatibility checks
- Basic observability (structured logging, tracing hooks)

## v0.3 — Deterministic Compiler Pipeline

- SkillIR (intermediate representation) + AST
- Multi-pass compiler (validation, optimization, cost estimation)
- WASM execution sandbox for untrusted skills
- Replayable execution traces

## v0.4+ — Distributed & Self-Improving

- Sharded event log + CRDT for branches
- Projection snapshotting and incremental rehydration
- Self-observation and meta-skills for runtime self-improvement
- Integration with broader Codessa intelligence layer (MUSE, memory, etc.)

## Long-term Vision

E-COS becomes the reference runtime for trustworthy, auditable, time-travel capable agentic systems — powering the cognitive layer of Codessa.

See also [ARCHITECTURE.md](docs/ARCHITECTURE.md) and GitHub Projects for detailed task tracking.

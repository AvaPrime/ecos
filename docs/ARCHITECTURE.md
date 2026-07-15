# E-COS Architecture

This document describes the high-level architecture and key design decisions of the Event-Sourced Cognitive Operating System.

## Guiding Principles

1. **Event Graph as OS** — The immutable, causally-linked event log is the single source of truth. All state is derived.
2. **Determinism & Replayability** — Any past state can be exactly reconstructed by replaying events from any point.
3. **Branching for Simulation** — Safe what-if analysis via lightweight branch events without mutating history.
4. **Skills as First-Class** — Versioned, schema-declared capabilities scheduled by the kernel.
5. **Projections, not Mutations** — Read models are rebuilt on demand; no shared mutable state in core.
6. **Minimal Core, Pluggable Extensions** — Core has very few deps. Persistence, execution backends, compilers are swappable.

## Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Projections Layer                       │
│  (AuditLog, AgentMemory, BeliefGraph, UI Views, Snapshots)    │
├─────────────────────────────────────────────────────────────┤
│                      Runtime Kernel                           │
│  (record_event, schedule_skill, replay, create_branch)        │
├─────────────────────────────────────────────────────────────┤
│  Event Store (InMemory | PostgreSQL | S3 + outbox | ...)     │
├─────────────────────────────────────────────────────────────┤
│  Skill Compiler (Naive | SkillIR + AST | LLM-assisted)       │
│  Skill Registry + Execution Sandbox (WASM / MCP / local)     │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### Event Model (`src/ecos/events.py`)
- Immutable Pydantic model with strong EventID typing.
- Supports causation_id and correlation_id for full causality tracing.
- Metadata for schema versioning and future evolution.

### EventStore Protocol
- `append`, `get_stream`, `get_event`.
- InMemory for dev/test; production adapters expected (e.g. relational with event sourcing patterns).

### RuntimeKernel
- Central orchestrator.
- Maintains projections registry.
- Handles branching as first-class event type.
- Future: integrates with MCP for capability discovery.

### Skill System
- `Skill` dataclass with version, schemas, handler_ref.
- `SimpleSkillCompiler` (v0.1) — naive string match; future phases replace with deterministic IR compiler + LLM planner.
- ExecutionPlan is frozen and replayable.

### Projections
- Abstract base with `apply(event)` (idempotent) and `rehydrate`.
- `StateRehydrator` coordinates multiple projections for agent/memory restoration.
- Example: `SimpleAuditLog`.

## Data Flow

1. External actor or agent expresses **intent**.
2. `RuntimeKernel.schedule_skill(intent)` → `SkillCompiler.compile(...)` → `ExecutionPlan`.
3. Plan execution (or scheduling event) produces new **Events**.
4. Events appended → projections updated automatically.
5. For queries: replay relevant events into target projection(s).
6. For simulation: `create_branch(from_event_id)` creates a new timeline fork.

## Future Extensions (not in v0.1)
- Persistent durable store with exactly-once semantics.
- SkillIR intermediate representation + multi-pass compiler (optimization, validation).
- WASM execution sandbox for untrusted skills.
- MCP (Multi-Capability Provider) integration for dynamic skill discovery.
- Snapshotting of projections for fast rehydration.
- Distributed kernel (event log sharded, CRDT or consensus for branches).

See also:
- [ROADMAP.md](../ROADMAP.md)
- [docs/adr/](../docs/adr/) (future ADRs)
- [README.md](../README.md#architecture-summary)

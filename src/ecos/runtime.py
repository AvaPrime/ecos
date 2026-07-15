"""Runtime kernel for E-COS — the heart of deterministic execution and replay.

The kernel consumes events, schedules skills via the compiler, maintains
projections, and supports branching/replay for what-if analysis and debugging.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ecos.events import Event, EventID, EventStore, InMemoryEventStore
from ecos.skills import SkillCompiler, ExecutionPlan, SimpleSkillCompiler, SkillRegistry


@dataclass
class RuntimeKernel:
    """Core runtime that drives the event-sourced cognitive system.

    Responsibilities:
    - Append events to store
    - Compile intents to plans via SkillCompiler
    - Execute plans (synchronously for v0.1)
    - Maintain live projections
    - Support time-travel replay and branching
    """

    event_store: EventStore = field(default_factory=InMemoryEventStore)
    skill_registry: SkillRegistry = field(default_factory=SkillRegistry)
    compiler: SkillCompiler = field(init=False)
    projections: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.compiler = SimpleSkillCompiler(self.skill_registry)

    def record_event(self, event: Event) -> Event:
        """Append event and trigger any side effects (projections, scheduling)."""
        self.event_store.append(event)
        self._apply_to_projections(event)
        return event

    def schedule_skill(self, intent: str, context: dict[str, Any] | None = None) -> ExecutionPlan:
        """Compile intent and record a scheduling event."""
        plan = self.compiler.compile(intent, context)
        sched_event = Event(
            type="SkillScheduled",
            payload={"intent": intent, "plan": plan.model_dump()},
            metadata={"source": "RuntimeKernel"},
        )
        self.record_event(sched_event)
        return plan

    def replay(self, since: EventID | None = None) -> list[Event]:
        """Replay events from store (or from a point) to rebuild state."""
        return self.event_store.get_stream(since=since)

    def create_branch(self, from_event_id: EventID, new_branch_name: str) -> Event:
        """Create a branching point for hypothetical simulation (foundational for what-if)."""
        branch_event = Event(
            type="BranchCreated",
            payload={
                "from_event_id": str(from_event_id),
                "branch_name": new_branch_name,
            },
            metadata={"source": "RuntimeKernel", "branching": True},
        )
        return self.record_event(branch_event)

    def _apply_to_projections(self, event: Event) -> None:
        """Update all registered projections with new event."""
        for name, proj in self.projections.items():
            if hasattr(proj, "apply"):
                proj.apply(event)

    def register_projection(self, name: str, projection: Any) -> None:
        self.projections[name] = projection

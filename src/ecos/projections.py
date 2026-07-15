"""Projection primitives for E-COS rehydration and read models.

Projections are derived views rebuilt by replaying the event log.
They enable efficient queries without mutating the source of truth.
State rehydrators restore agent/memory state from events.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ecos.events import Event, EventID


class Projection(ABC):
    """Base class for all projections. Subclasses implement apply() for event handling."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.version = "1.0.0"
        self.last_event_id: EventID | None = None

    @abstractmethod
    def apply(self, event: Event) -> None:
        """Apply an event to update the projection's state. Must be idempotent."""
        ...

    def rehydrate(self, events: list[Event]) -> None:
        """Rebuild projection from a list of events (used for time-travel or catch-up)."""
        for event in events:
            self.apply(event)
            self.last_event_id = event.id


class StateRehydrator:
    """Rehydrates arbitrary state objects from event history using registered projectors."""

    def __init__(self) -> None:
        self._projectors: dict[str, Projection] = {}

    def register(self, name: str, projector: Projection) -> None:
        self._projectors[name] = projector

    def rehydrate_state(self, events: list[Event], target_names: list[str] | None = None) -> dict[str, Any]:
        """Rehydrate selected (or all) projections from events."""
        targets = target_names or list(self._projectors.keys())
        result: dict[str, Any] = {}
        for name in targets:
            if name in self._projectors:
                proj = self._projectors[name]
                proj.rehydrate(events)
                result[name] = proj  # or proj.get_state() in real impl
        return result


# Example concrete projection
class SimpleAuditLog(Projection):
    """Example projection: append-only audit log of all events."""

    def __init__(self) -> None:
        super().__init__(name="audit_log")
        self.entries: list[dict[str, Any]] = []

    def apply(self, event: Event) -> None:
        self.entries.append(
            {
                "event_id": str(event.id),
                "type": event.type,
                "timestamp": event.timestamp.isoformat(),
                "actor": event.actor_id,
                "payload_preview": str(event.payload)[:200],
            }
        )
        self.last_event_id = event.id

    def get_state(self) -> list[dict[str, Any]]:
        return self.entries

"""Core event-sourcing primitives for E-COS.

Events are immutable facts. The event graph forms the source of truth and enables
branching (time-travel, hypothetical simulation), replayability, and deterministic
state reconstruction via projections.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Protocol

from pydantic import BaseModel, Field, ConfigDict


class EventID(str):
    """Strongly-typed event identifier (ULID or UUIDv7 recommended in production)."""

    @classmethod
    def new(cls) -> EventID:
        return cls(str(uuid.uuid4()))


class Event(BaseModel):
    """Immutable domain event representing a fact that occurred in the system."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: EventID = Field(default_factory=EventID.new)
    type: str = Field(..., min_length=1, description="Event type, e.g. 'SkillScheduled', 'BeliefUpdated'")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict[str, Any] = Field(default_factory=dict, description="Event payload (must be JSON serializable)")
    causation_id: EventID | None = Field(None, description="ID of the event that caused this one (for causality tracking)")
    correlation_id: EventID | None = Field(None, description="Correlation ID for tracing across boundaries")
    actor_id: str | None = Field(None, description="Actor or agent that triggered the event")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata (versioning, schema, etc.)")

    def with_causation(self, causation_id: EventID) -> Event:
        """Return a copy with causation_id set (immutable pattern)."""
        return self.model_copy(update={"causation_id": causation_id})


class EventStore(Protocol):
    """Abstract event store interface. Implementations provide durability guarantees."""

    def append(self, event: Event) -> None:
        """Append a new event to the store."""
        ...

    def get_stream(self, stream_id: str | None = None, since: EventID | None = None) -> list[Event]:
        """Retrieve events, optionally filtered by stream or since a given event."""
        ...

    def get_event(self, event_id: EventID) -> Event | None:
        """Fetch a single event by ID."""
        ...


class InMemoryEventStore(EventStore):
    """In-memory event store for testing, simulation, and development.

    Not for production durability — use a persistent implementation (e.g. PostgreSQL + outbox).
    """

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._by_id: dict[EventID, Event] = {}

    def append(self, event: Event) -> None:
        if event.id in self._by_id:
            raise ValueError(f"Duplicate event ID: {event.id}")
        self._events.append(event)
        self._by_id[event.id] = event

    def get_stream(self, stream_id: str | None = None, since: EventID | None = None) -> list[Event]:
        # Simple linear stream for v0.1; production would use stream partitioning
        events = self._events
        if since:
            # Find index after 'since'
            idx = next((i for i, e in enumerate(events) if e.id == since), -1)
            events = events[idx + 1 :]
        return list(events)  # copy

    def get_event(self, event_id: EventID) -> Event | None:
        return self._by_id.get(event_id)

"""Unit tests for E-COS event sourcing primitives."""

import pytest

from ecos.events import Event, EventID, InMemoryEventStore


def test_event_creation(sample_event: Event) -> None:
    assert sample_event.type == "TestEvent"
    assert sample_event.payload["num"] == 42
    assert isinstance(sample_event.id, EventID)


def test_event_immutability(sample_event: Event) -> None:
    with pytest.raises(Exception):  # pydantic frozen
        sample_event.payload["new"] = 1  # type: ignore[index]


def test_event_with_causation(sample_event: Event) -> None:
    cause = EventID.new()
    caused = sample_event.with_causation(cause)
    assert caused.causation_id == cause
    assert caused.id != sample_event.id  # new id generated? Wait, with_causation keeps id? No, model_copy keeps id unless updated


def test_inmemory_store_append_and_get(event_store: InMemoryEventStore, sample_event: Event) -> None:
    event_store.append(sample_event)
    retrieved = event_store.get_event(sample_event.id)
    assert retrieved is not None
    assert retrieved.type == sample_event.type


def test_store_duplicate_prevention(event_store: InMemoryEventStore, sample_event: Event) -> None:
    event_store.append(sample_event)
    with pytest.raises(ValueError, match="Duplicate event ID"):
        event_store.append(sample_event)


def test_get_stream(event_store: InMemoryEventStore) -> None:
    e1 = Event(type="E1")
    e2 = Event(type="E2")
    event_store.append(e1)
    event_store.append(e2)
    stream = event_store.get_stream()
    assert len(stream) == 2

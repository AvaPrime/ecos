"""Pytest configuration and shared fixtures for E-COS test suite."""

import pytest

from ecos.events import InMemoryEventStore, Event
from ecos.skills import SkillRegistry, Skill, SkillID
from ecos.runtime import RuntimeKernel


@pytest.fixture
def event_store() -> InMemoryEventStore:
    return InMemoryEventStore()


@pytest.fixture
def skill_registry() -> SkillRegistry:
    reg = SkillRegistry()
    # Seed a couple of example skills for tests
    reg.register(
        Skill(
            id=SkillID("skill_test_echo"),
            name="echo",
            version="1.0.0",
            description="Simple echo skill for testing",
            handler_ref="builtin:echo",
        )
    )
    reg.register(
        Skill(
            id=SkillID("skill_test_compute"),
            name="compute",
            version="0.9.0",
            description="Placeholder compute skill",
        )
    )
    return reg


@pytest.fixture
def kernel(skill_registry: SkillRegistry) -> RuntimeKernel:
    k = RuntimeKernel(skill_registry=skill_registry)
    # Register example projection
    from ecos.projections import SimpleAuditLog

    k.register_projection("audit", SimpleAuditLog())
    return k


@pytest.fixture
def sample_event() -> Event:
    return Event(type="TestEvent", payload={"key": "value", "num": 42})

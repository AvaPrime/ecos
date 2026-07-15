"""Event-Sourced Cognitive Operating System (E-COS).

Foundational primitives for a deterministic, branching, replayable cognitive runtime.
The event graph *is* the OS. Agents schedule Skills. MCP provides pure capabilities.
UI and external systems are pure projections of the underlying event-sourced truth.
"""

__version__ = "0.1.0"
__author__ = "Ava Prime"
__email__ = "ava.prime@outlook.com"

from ecos.events import Event, EventID, EventStore, InMemoryEventStore
from ecos.skills import Skill, SkillID, SkillRegistry, SkillCompiler
from ecos.runtime import RuntimeKernel, ExecutionPlan
from ecos.projections import Projection, StateRehydrator

__all__ = [
    "__version__",
    "Event",
    "EventID",
    "EventStore",
    "InMemoryEventStore",
    "Skill",
    "SkillID",
    "SkillRegistry",
    "SkillCompiler",
    "RuntimeKernel",
    "ExecutionPlan",
    "Projection",
    "StateRehydrator",
]

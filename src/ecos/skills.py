"""Skill abstraction, registry, and compiler for E-COS.

Skills are first-class, versioned, deterministic units of capability.
The SkillCompiler transforms high-level intent into executable ExecutionPlans.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Protocol

from pydantic import BaseModel, Field

from ecos.events import Event, EventID


class SkillID(str):
    """Strongly typed skill identifier."""

    @classmethod
    def new(cls) -> SkillID:
        import uuid

        return cls(f"skill_{uuid.uuid4().hex[:12]}")


@dataclass(frozen=True)
class Skill:
    """A versioned, deterministic capability unit that can be scheduled and executed."""

    id: SkillID
    name: str
    version: str = "1.0.0"
    description: str = ""
    # In real impl, handler could be WASM module, Python fn ref, or remote MCP endpoint
    handler_ref: str = ""
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Skill name cannot be empty")


class SkillRegistry:
    """In-memory registry of available skills. Production would sync from skill catalog service."""

    def __init__(self) -> None:
        self._skills: dict[SkillID, Skill] = {}

    def register(self, skill: Skill) -> None:
        self._skills[skill.id] = skill

    def get(self, skill_id: SkillID) -> Skill | None:
        return self._skills.get(skill_id)

    def list_all(self) -> list[Skill]:
        return list(self._skills.values())


class SkillCompiler(Protocol):
    """Compiles high-level goal or intent into a deterministic ExecutionPlan."""

    def compile(self, intent: str, context: dict[str, Any]) -> ExecutionPlan:
        """Produce an ExecutionPlan from natural language or structured intent."""
        ...


# Placeholder compiler implementation (to be replaced by LLM-backed or symbolic compiler in later phase)
class SimpleSkillCompiler:
    """Naive compiler for bootstrapping. Real version will use SkillIR + AST + optimization passes."""

    def __init__(self, registry: SkillRegistry) -> None:
        self.registry = registry

    def compile(self, intent: str, context: dict[str, Any] | None = None) -> ExecutionPlan:
        context = context or {}
        # Very naive: assume intent contains skill name
        for skill in self.registry.list_all():
            if skill.name.lower() in intent.lower():
                return ExecutionPlan(
                    plan_id=EventID.new(),
                    steps=[{"skill_id": str(skill.id), "action": "execute", "intent": intent}],
                    metadata={"compiler": "SimpleSkillCompiler", "intent": intent},
                )
        # Fallback empty plan
        return ExecutionPlan(
            plan_id=EventID.new(),
            steps=[],
            metadata={"compiler": "SimpleSkillCompiler", "intent": intent, "note": "no matching skill"},
        )


class ExecutionPlan(BaseModel):
    """Deterministic, replayable plan produced by SkillCompiler."""

    model_config = {"frozen": True}

    plan_id: EventID
    steps: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

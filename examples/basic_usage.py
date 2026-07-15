"""Basic usage example for E-COS runtime.

Demonstrates event recording, skill scheduling, replay, and projections.
Run with: python -m examples.basic_usage
"""

from ecos import RuntimeKernel, Event
from ecos.projections import SimpleAuditLog


def main() -> None:
    print("=== E-COS Basic Usage Demo ===\n")

    kernel = RuntimeKernel()

    # Register example projection
    audit = SimpleAuditLog()
    kernel.register_projection("audit", audit)

    # Record some events
    kernel.record_event(Event(type="SystemInitialized", payload={"version": "0.1.0"}))
    kernel.record_event(Event(type="AgentSpawned", payload={"agent_id": "agent_alpha"}))

    # Schedule a skill (uses naive compiler)
    plan = kernel.schedule_skill("please echo hello world", context={"user": "demo"})
    print(f"Compiled plan: {plan.plan_id}")
    print(f"Steps: {plan.steps}")

    # Create a branch for simulation
    branch_event = kernel.create_branch(plan.plan_id, "what-if-v1")
    print(f"Branch created from: {branch_event.payload['from_event_id']}")

    # Replay
    history = kernel.replay()
    print(f"\nReplayed {len(history)} events")

    # Show audit projection
    print("\nAudit log entries:")
    for entry in audit.get_state()[:5]:
        print(f"  - {entry['type']} @ {entry['timestamp']}")

    print("\n=== Demo complete. Event graph is the source of truth. ===")


if __name__ == "__main__":
    main()

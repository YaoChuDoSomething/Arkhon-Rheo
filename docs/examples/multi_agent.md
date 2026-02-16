# Multi-Agent Orchestration Example

This example demonstrates how to orchestrate multiple Arkhon-Rheo agents using the new **Graph** and **RuntimeScheduler** engine.

## Scenario

We have a two-agent team:

1. **Researcher**: Analyzes the initial query and provides raw facts.
2. **Writer**: Takes those facts and produces a final draft.

## The Graph

The workflow is defined as a directed graph: `START -> research -> write -> END`.

## Code Walkthrough

```python
# See examples/multi_agent_orchestration/main.py for full code
graph = create_orchestration_graph()
scheduler = RuntimeScheduler(graph, checkpoint_manager=None)
await scheduler.run(initial_state, entry_point="research")
```

## Running the Example

```bash
uv run examples/multi_agent_orchestration/main.py
```

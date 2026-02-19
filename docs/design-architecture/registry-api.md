# Registry API Reference

Arkhon-Rheo uses a registry-based system for decentralized discovery of both **Agents** and **Tools**.

## 1. Tool Registry

The `ToolRegistry` manages the lifecycle and discovery of tools available to agents.

### `ToolRegistry` (Class)

Centralized container for tool instances.

#### Methods

| Method | Signature | Description |
| :--- | :--- | :--- |
| `register` | `(tool: BaseTool) -> None` | Adds a tool to the registry. Overwrites existing tools with same name. |
| `get_tool` | `(name: str) -> BaseTool \| None` | Retrieves a tool by its unique name string. |
| `list_tools` | `() -> list[BaseTool]` | Returns all registered tool instances. |
| `clear` | `() -> None` | Wipes the registry (useful for test isolation). |

### Global Access

Access the registry via the singleton helper:

```python
from arkhon_rheo.tools.registry import get_registry

registry = get_registry()
```

---

## 2. Agent Registry

The `AgentRegistry` is a thread-safe singleton that enables agents to locate and communicate with each other.

### `AgentRegistry` (Class)

#### Static/Class Methods

| Method | Signature | Description |
| :--- | :--- | :--- |
| `register` | `(agent: Agent) -> None` | Static method to register an agent globally. |
| `get` | `(name: str) -> Agent \| None` | Static method to look up an agent by name. |
| `list_agents`| `() -> dict[str, Agent]` | Returns a copy of the registry mapping. |
| `clear` | `() -> None` | Resets the singleton state. |

### Implementation Details

- **Singleton Pattern**: Managed via `__new__` to ensure a single shared instance across the process.
- **Async Safety**: Registry lookups are synchronous, but agent interactions are typically `async`.

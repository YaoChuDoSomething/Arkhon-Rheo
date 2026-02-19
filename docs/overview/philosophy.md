# Core Philosophy

**Arkhon-Rheo** is not just a library; it's a design philosophy for building autonomous systems with **rigorous governance**.

## The Name

- **Arkhon** (*ἄρχων*): Ruler / Governor. Represents the governance layer that ensures agents follow rules.
- **Rheo** (*ῥέω*): To Flow. Represents the streaming orchestration and data flow between agents.

## Design Pillars

### 1. Governance First

Every "step" an agent takes is validated by a **Governance Node** before it is allowed to interact with the world. This prevents hallucinated actions and enforces safety constraints (e.g., spending limits, depth limits).

### 2. Isomorphic Architecture

Arkhon-Rheo is built on top of **Graph** (based on LangGraph principles) but extends it with:

- **Event Sourcing**: Every state change is a permanent event record.
- **Static Schema**: Uses Pydantic to ensure data integrity across agent boundaries.

### 3. Separation of Concerns

- **Orchestration**: Managed by `Graph` and `Executor`.
- **Logic**: Contained within modular `Node` implementations.
- **State**: Centralized in the `AgentState` object.
- **Capabilities**: Isolated in `Tools`.

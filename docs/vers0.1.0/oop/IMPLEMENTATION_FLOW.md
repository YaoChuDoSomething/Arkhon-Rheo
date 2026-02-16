# Arkhon-Rheo Phase 1 Implementation Flow

**Status**: Active  
**Phase**: 1 (Foundation)  
**Goal**: Build the immutable state machine engine.

This document bridges the high-level [ROADMAP.md](../../ROADMAP.md) with the detailed [Class Inventory](class_inventory.md). It provides the **daily execution guide** for developers.

---

## 📅 Sprint 1.1: Core State Machine (Week 1)

**Focus**: Immutable State & Graph Execution Engine

### 🎯 Objective

Implement the core `ReActState` container and the `StateGraph` capability to define and execute workflows.

### 🧩 Classes to Implement

| Class | Module | Priority | Role |
| :--- | :--- | :--- | :--- |
| **`ReasoningStep`** | `core/state.py` | P0 | Immutable event log unit. |
| **`ReActState`** | `core/state.py` | P0 | Main state container (frozen dataclass). |
| **`ContextManager`** | `core/context.py` | P1 | Thread-local storage for Trace IDs. |
| **`StateGraph`** | `core/graph.py` | P1 | Graph topology and execution loop. |

### 🧠 Relevant Skills

- **`context-fundamentals`**: For implementing `ContextManager`.
- **`python-pro`**: For `dataclasses` and type safety.
- **`tdd-workflow`**: Apply Red-Green-Refactor cycle.

### ✅ Success Criteria (TDD)

- [ ] `test_state_immutability`: Verify state cannot be mutated directly.
- [ ] `test_step_creation`: Verify step generation and serialization.
- [ ] `test_context_isolation`: Verify context is isolated per thread/task.
- [ ] `test_graph_topology`: Verify nodes and edges can be added.

---

## 📅 Sprint 1.2: Node Implementations (Week 2)

**Focus**: The ReAct Components

### 🎯 Objective

Implement the diverse node types that form the ReAct loop.

### 🧩 Classes to Implement

| Class | Module | Priority | Role |
| :--- | :--- | :--- | :--- |
| **`BaseNode`** | `nodes/base.py` | P0 | Abstract base class with template method. |
| **`ThoughtNode`** | `nodes/thought_node.py` | P0 | LLM interaction handler. |
| **`ActionNode`** | `nodes/action_node.py` | P0 | Tool dispatcher. |
| **`ObservationNode`** | `nodes/observation_node.py` | P1 | Output formatter. |
| **`ValidateNode`** | `nodes/validate_node.py` | P2 | Rule checker. |
| **`CommitNode`** | `nodes/commit_node.py` | P2 | State persistence. |

### 🧠 Relevant Skills

- **`context-window-management`**: For `ThoughtNode` token tracking.
- **`software-architecture`**: For Template Method pattern in `BaseNode`.

### ✅ Success Criteria (TDD)

- [ ] `test_node_inheritance`: All nodes must inherit from BaseNode.
- [ ] `test_thought_generation`: Mock LLM returns expected thought.
- [ ] `test_action_dispatch`: Mock tool execution.

---

## 📅 Sprint 1.3: Tool Integration (Week 3)

**Focus**: Capability Expansion

### 🎯 Objective

Build the plugin system for tools and implement standard capabilities.

### 🧩 Classes to Implement

| Class | Module | Priority | Role |
| :--- | :--- | :--- | :--- |
| **`Tool`** | `tools/base.py` | P0 | Abstract tool interface. |
| **`ToolRegistry`** | `tools/registry.py` | P0 | Plugin discovery/registration. |
| **`SearchTool`** | `tools/builtin/search.py` | P1 | Web search implementation. |
| **`FileOpsTool`** | `tools/builtin/file_ops.py` | P1 | Filesystem operations. |
| **`CalculatorTool`** | `tools/builtin/calculator.py` | P2 | Math operations. |

### 🧠 Relevant Skills

- **`agent-tool-builder`**: Best practices for tool interfaces.
- **`context-manager`**: Passing context to tools.

### ✅ Success Criteria (TDD)

- [ ] `test_tool_registry`: Operations (register, get, list).
- [ ] `test_schema_generation`: Pydantic to JSON Schema conversion.
- [ ] `test_safe_calculator`: Prevent code injection in math tool.

---

## 📅 Sprint 1.4: Configuration & Rules (Week 4)

**Focus**: Governance & Control

### 🎯 Objective

Externalize configuration and enforce execution boundaries.

### 🧩 Classes to Implement

| Class | Module | Priority | Role |
| :--- | :--- | :--- | :--- |
| **`EngineConfig`** | `config/schema.py` | P0 | Main config model. |
| **`ConfigLoader`** | `config/loader.py` | P1 | YAML loader with env override. |
| **`RuleEngine`** | `rules/rule_engine.py` | P0 | Chain of responsibility runner. |
| **`MaxDepthRule`** | `rules/builtin.py` | P1 | Loop prevention. |

### 🧠 Relevant Skills

- **`context-management-context-restore`**: Resuming from config.
- **`security-auditor`**: Reviewing rule implementations.

### ✅ Success Criteria (TDD)

- [ ] `test_config_loading`: Load valid YAML, fail invalid.
- [ ] `test_rule_enforcement`: Max depth triggers stop.

---

## 🔗 Reference

- [Class Inventory](class_inventory.md)
- [Methods & Properties](methods_properties.md)
- [Project Roadmap](../../ROADMAP.md)

---

## ✅ Definition of Done (Phase Completion)

Upon completing all sprints in a Phase:

1. **Verify Tests**: All tests must pass (`uv run pytest`).
2. **Linting**: Code must be linted (`ruff check`, `ty`).
3. **Commit**: Commit all changes to the working branch.
4. **Merge**: Merge the working branch into `main`.
5. **Push**: Push `main` to the remote repository.

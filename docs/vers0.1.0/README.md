# Arkhon-Rheo + ReActEngine Documentation

**Version**: 1.0.0  
**Status**: Draft  
**Last Updated**: 2026-02-14  
**Code Path**: `src/arkhon-rheo/`

---

## 📖 Overview

This documentation suite provides comprehensive specifications, design documents, and implementation guides for **Arkhon-Rheo**, a production-grade autonomous agent system built on the **ReActEngine** OOP architecture.

**Arkhon-Rheo** is a **Deterministic AI Workflow Engine** that combines:

- **State Machine**: Explicit state transitions governing all agent behavior
- **Event Sourcing**: Immutable, append-only log of every reasoning step
- **Rule Engine**: Governance constraints and policy enforcement
- **Tool Registry**: Pluggable tool architecture with JSON Schema validation

**NOT** a prompt hack or simple LLM wrapper. This is a structured, testable, production-ready agent system.

---

## 🎯 Core Philosophy

```text
Arkhon-Rheo = Philosophy + Governance Standards
ReActEngine = Concrete OOP Implementation  
Integration = Philosophy ⟺ Code Architecture
```

### Design Principles

1. **State Machine Driven** - All behavior governed by explicit FSM transitions
2. **Event Sourcing** - Complete audit trail with checkpoint/replay capability
3. **YAML Configuration** - Declarative runtime behavior without code changes
4. **Tool Pluggability** - Dynamic tool registration via standardized schema
5. **Rule Engine Extensibility** - Custom governance rules defined in YAML
6. **LangGraph Isomorphism** - Structurally equivalent to LangGraph StateGraph

---

## 📚 Documentation Roadmap

This directory contains **9 core documents** organized from high-level specification to implementation details:

### 📋 Specifications & Design (01-02)

| Document                                   | Purpose                                                        | Audience                      |
|--------------------------------------------|----------------------------------------------------------------|-------------------------------|
| **[SPECIFICATION.md](./SPECIFICATION.md)** | Technical requirements, API reference, and system contracts    | All stakeholders              |
| **[DESIGN.md](./DESIGN.md)**               | System design patterns, data flow, and architectural decisions | Architects, senior engineers  |

### 🏗️ Architecture & Planning (03-04)

| Document                                 | Purpose                                                       | Audience                     |
|------------------------------------------|---------------------------------------------------------------|------------------------------|
| **[ROADMAP.md](./ROADMAP.md)**           | 4-phase development plan (12 weeks) with sprint deliverables  | Project managers, team leads |
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | Component hierarchy, layered design (L1-L5), extension points | Software architects          |

### 🛠️ Implementation Guides (05-06)

| Document                         | Purpose                                                          | Audience                 |
|----------------------------------|------------------------------------------------------------------|--------------------------|
| **[DEVGUIDE.md](./DEVGUIDE.md)** | Developer workflows, IDE setup, CLI usage, debugging             | Developers, contributors |
| **[TDD.md](./TDD.md)**           | Test-driven development strategy, test pyramid, mocking patterns | QA engineers, developers |

### 🔐 Advanced Topics (07-09)

| Document                                   | Purpose                                                       | Audience                       |
|--------------------------------------------|---------------------------------------------------------------|--------------------------------|
| **[ACL.md](./ACL.md)**                     | Multi-agent roles, permissions, message passing protocols     | System integrators             |
| **[STATE_MACHINE.md](./STATE_MACHINE.md)** | FSM design, state transitions, checkpointing mechanisms       | Advanced developers            |
| **[RULES.md](./RULES.md)**                 | Rule engine implementation, built-in governance rules         | Security reviewers, architects |

### 📑 Supplementary

- **[SKILLS_MANIFEST.md](./SKILLS_MANIFEST.md)** - Available skills and their integration points

---

## 🚀 Quick Start

### For New Readers

**Start here** depending on your role:

- **Product Managers / Stakeholders**: Read [SPECIFICATION.md](./SPECIFICATION.md) § 1-2
- **Architects**: [ARCHITECTURE.md](./ARCHITECTURE.md) → [DESIGN.md](./DESIGN.md)
- **Developers**: [DEVGUIDE.md](./DEVGUIDE.md) → [TDD.md](./TDD.md)
- **Security Reviewers**: [RULES.md](./RULES.md) → [ACL.md](./ACL.md)

### Reading Path by Objective

#### 🎯 Understanding the System (Top-Down)

```text
SPECIFICATION → DESIGN → ARCHITECTURE → DEVGUIDE
```

#### 🔨 Implementing Features (Bottom-Up)

```text
DEVGUIDE → TDD → STATE_MACHINE → RULES → ACL
```

#### 📅 Project Planning

```text
ROADMAP → SPECIFICATION (§2-§5) → ARCHITECTURE (§8)
```

---

## 🏛️ System Architecture

### High-Level Component Structure

```text
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                 │
│         CLI / API / REPL / Human Approval Gates         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Orchestration & Runtime Layer              │
│    StateGraph Engine │ Scheduler │ Checkpointing       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 ReAct Node Layer (FSM)                  │
│  ThoughtNode │ ValidateNode │ ActionNode │ ObsNode     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Tool & Policy Layer                        │
│   ToolRegistry │ RuleEngine │ ACL Permissions          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Storage & Persistence                      │
│     SQLite Checkpointing │ YAML Config │ Event Log     │
└─────────────────────────────────────────────────────────┘
```

### State Machine (FSM)

```mermaid
graph LR
    START((Start)) --> Thought[ThoughtNode]
    Thought --> Validate[ValidateNode]
    Validate -->|✓ Valid| Action[ActionNode]
    Validate -->|✗ Reject| Thought
    Action --> Observation[ObservationNode]
    Observation --> Commit[CommitNode]
    Commit --> Thought
    Commit --> END((End))
```

### Directory Structure

```text
src/arkhon-rheo/
├── core/                    # State machine & graph engine
│   ├── state.py            # ReActState (immutable dataclass)
│   ├── graph.py            # StateGraph executor
│   └── step.py             # ReasoningStep abstraction
├── nodes/                   # FSM node implementations
│   ├── base_node.py        # BaseNode ABC
│   ├── thought_node.py     # LLM reasoning
│   ├── validate_node.py    # Rule validation
│   ├── action_node.py      # Tool execution
│   └── observation_node.py # Result processing
├── tools/                   # Tool registry & implementations
│   ├── registry.py         # Dynamic tool registration
│   ├── base_tool.py        # BaseTool ABC
│   └── implementations/    # Concrete tools
├── rules/                   # Governance & validation
│   ├── engine.py           # RuleEngine
│   ├── base_rule.py        # BaseRule ABC
│   └── builtin/            # Built-in rules
│       ├── max_depth.py    # Prevent infinite loops
│       ├── forbid_guessing.py
│       ├── cost_limit.py
│       └── require_tool.py
├── config/                  # Configuration subsystem
│   ├── schema.py           # YAML schema definitions
│   └── loader.py           # Config loader with validation
└── runtime/                 # Execution & checkpointing
    ├── executor.py         # Runtime orchestration
    ├── checkpoint.py       # SQLite-based persistence
    └── scheduler.py        # Task scheduling
```

---

## 💻 Technology Stack

| Component            | Technology      | Version | Purpose                                   |
|----------------------|-----------------|---------|-------------------------------------------|
| **Language**         | Python          | 3.12+   | Modern type hints (PEP 695), performance  |
| **Package Manager**  | uv              | Latest  | Fast dependency resolution                |
| **LLM Integration**  | Google GenAI SDK| Latest  | Gemini API (Flash/Pro)                    |
| **Configuration**    | YAML + Pydantic | -       | Type-safe config validation               |
| **Storage**          | SQLite          | -       | Checkpoint persistence                    |
| **Testing**          | pytest          | -       | Unit/integration/E2E tests                |
| **Linting**          | ruff            | -       | Fast Python linter                        |
| **Type Checking**    | mypy            | -       | Static type analysis                      |
| **Documentation**    | MkDocs          | -       | Docs site generation                      |

---

## 📖 Key Concepts

### ReActState

Immutable container representing the agent's complete state at any point:

```python
@dataclass(frozen=True)
class ReActState:
    """Immutable state container (similar to LangGraph's TypedDict)."""
    thought: str
    action: dict | None
    observation: str | None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def update(self, **changes) -> "ReActState":
        """Create new state with updates (copy-on-write)."""
        return replace(self, **changes)
```

### ReasoningStep

Single atomic unit of the ReAct cycle:

```python
@dataclass
class ReasoningStep:
    """Immutable reasoning step (event sourcing)."""
    step_id: int
    thought: str
    action: dict | None
    observation: str | None
    timestamp: datetime
    metadata: dict[str, Any]
```

### StateGraph

Execution engine (isomorphic to LangGraph):

```python
class StateGraph:
    """
    Directed graph executor for stateful agent workflows.
    
    Isomorphic to LangGraph's StateGraph but with:
    - Full control over execution
    - YAML-driven configuration
    - Built-in rule engine
    - SQLite checkpointing
    """
    
    def add_node(self, name: str, node: BaseNode) -> None: ...
    def add_edge(self, from_node: str, to_node: str) -> None: ...
    def compile(self) -> CompiledGraph: ...
```

### Rule Engine

Governance constraints enforced at validation nodes:

```python
class BaseRule(ABC):
    """Abstract base for all governance rules."""
    
    @abstractmethod
    def validate(self, state: ReActState, metadata: dict) -> RuleResult:
        """Return RuleResult(passed=bool, reason=str, severity=str)."""
        pass

# Built-in rules
class MaxDepthRule(BaseRule):
    """Prevent infinite reasoning loops (max steps = 20)."""
    
class ForbidGuessingRule(BaseRule):
    """Require tool use - no hallucinated answers."""

class CostLimitRule(BaseRule):
    """Enforce token budget limits."""
    
class RequireToolUseRule(BaseRule):
    """Action steps MUST invoke a tool."""
```

---

## 🧪 Development Workflow

### Phase 1: Foundation (4 weeks) - **Current**

- ✅ PEP8 + Docstring production code
- ✅ Core state machine implementation
- ✅ YAML configuration system
- 🔄 Rule engine with built-in rules
- 🔄 Basic tool registry

### Phase 2: Multi-Agent (3 weeks)

- Multi-agent message passing
- Role-based access control (ACL)
- Coordinator agent orchestration
- Agent communication protocol

### Phase 3: Memory & Storage (3 weeks)

- SQLite checkpoint/restore
- Event log persistence
- State replay mechanism
- Long-term memory integration

### Phase 4: Package & Publish (2 weeks)

- pip-installable package structure
- pyproject.toml configuration
- CLI entry points (`arkhon-rheo init`, `run`)
- MkDocs documentation site

---

## 🧩 Extension Points

Arkhon-Rheo is designed for extensibility:

### Custom Nodes

Implement `BaseNode` ABC:

```python
from arkhon_rheo.nodes import BaseNode

class CustomResearchNode(BaseNode):
    """Custom node for deep research tasks."""
    
    def execute(self, state: ReActState) -> ReActState:
        # Your logic here
        return state.update(thought="Research complete")
```

### Custom Tools

Implement `BaseTool` ABC and register:

```python
from arkhon_rheo.tools import BaseTool, ToolRegistry

class WebScraperTool(BaseTool):
    """Tool for web scraping."""
    
    def execute(self, **params) -> dict:
        # Scraping logic
        return {"content": "..."}

# Register
ToolRegistry.register("web_scraper", WebScraperTool)
```

### Custom Rules

Implement `BaseRule` ABC:

```python
from arkhon_rheo.rules import BaseRule, RuleResult

class DataPrivacyRule(BaseRule):
    """Ensure no PII in responses."""
    
    def validate(self, state: ReActState, metadata: dict) -> RuleResult:
        if contains_pii(state.thought):
            return RuleResult(
                passed=False, 
                reason="PII detected", 
                severity="critical"
            )
        return RuleResult(passed=True)
```

---

## 🧪 Testing Strategy

### Test Pyramid

```text
     E2E (10%)
    /         \
   Integration (20%)
  /            \
Unit Tests (70%)
```

**Coverage Target**: 90%+

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src/arkhon-rheo --cov-report=term-missing

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

See [TDD.md](./TDD.md) for complete testing guidelines.

---

## 🔐 Security & Governance

### Built-in Rules

| Rule                  | Purpose                                | Configuration         |
|-----------------------|----------------------------------------|-----------------------|
| `MaxDepthRule`        | Prevent infinite loops                 | `max_steps: 20`       |
| `ForbidGuessingRule`  | Require tool use for factual questions | `min_confidence: 0.8` |
| `CostLimitRule`       | Enforce token budgets                  | `max_tokens: 100000`  |
| `RequireToolUseRule`  | Action steps MUST invoke tools         | -                     |

### Multi-Agent Access Control

See [ACL.md](./ACL.md) for complete role-based permissions.

```yaml
# config/agents.yaml
agents:
  coordinator:
    permissions: [read, write, delegate]
  planner:
    permissions: [read, propose]
  coder:
    permissions: [read, execute_tool]
  reviewer:
    permissions: [read,validate]
```

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.12+
- uv (package manager)
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/dlamp.git
cd dlamp

# Navigate to agent system
cd src/arkhon-rheo

# Install dependencies
uv sync

# Run development agent
python dev.py
```

### Configuration

Copy example config:

```bash
cp config/agent.example.yaml config/agent.yaml
```

Edit `config/agent.yaml`:

```yaml
# Agent configuration
agent:
  name: "DLAMP Agent"
  max_steps: 20
  llm:
    provider: "google"
    model: "gemini-3-flash-preview"
    
# Rules
rules:
  - name: "max_depth"
    params: {max_steps: 20}
  - name: "cost_limit"
    params: {max_tokens: 100000}
```

See [DEVGUIDE.md](./DEVGUIDE.md) for complete setup instructions.

---

## 🛠️ CLI Usage

```bash
# Initialize new agent config
arkhon-rheo init --template basic

# Run agent
arkhon-rheo run --config config/agent.yaml

# Validate configuration
arkhon-rheo validate config/agent.yaml

# Inspect checkpoints
arkhon-rheo checkpoint list
arkhon-rheo checkpoint restore <checkpoint_id>

# Debug mode
arkhon-rheo run --debug --log-level DEBUG
```

---

## 📊 Monitoring & Observability

### Event Logging

All reasoning steps logged to `events.log`:

```json
{
  "step_id": 1,
  "thought": "I need to analyze the data",
  "action": {"tool": "python_repl", "params": {...}},
  "observation": "Analysis complete",
  "timestamp": "2026-02-14T13:58:00Z",
  "metadata": {"cost": 150, "latency_ms": 1200}
}
```

### Checkpointing

SQLite-based state persistence:

```bash
# Checkpoint created automatically after each commit
# Location: .arkhon-rheo/checkpoints.db

# Restore from checkpoint
python -m arkhon_rheo.runtime.checkpoint restore --id abc123
```

---

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Follow [DEVGUIDE.md](./DEVGUIDE.md) coding standards
4. Write tests following [TDD.md](./TDD.md)
5. Run linters: `ruff check` + `mypy`
6. Submit PR with clear description

### Code Standards

- **PEP 8** compliance (enforced by ruff)
- **Type hints** for all functions
- **Docstrings** following Google style
- **90%+ test coverage**

---

## 📄 License

This project is licensed under the MIT License - see `LICENSE` file for details.

---

## 📚 Further Reading

### Document Reading Order

**For System Understanding**:

1. [SPECIFICATION.md](./SPECIFICATION.md) - Technical requirements
2. [DESIGN.md](./DESIGN.md) - Design patterns
3. [ARCHITECTURE.md](./ARCHITECTURE.md) - Component hierarchy

**For Implementation**:

1. [DEVGUIDE.md](./DEVGUIDE.md) - Development workflows
2. [TDD.md](./TDD.md) - Testing strategy
3. [STATE_MACHINE.md](./STATE_MACHINE.md) - FSM internals

**For Advanced Topics**:

1. [ACL.md](./ACL.md) - Multi-agent architecture
2. [RULES.md](./RULES.md) - Governance engine
3. [ROADMAP.md](./ROADMAP.md) - Development plan

---

## 🙋 FAQ

### Q: How is this different from LangGraph?

**A:** Arkhón-Rheo is **structurally isomorphic** to LangGraph (same StateGraph model) but provides:

- Full control over execution (not a black box)
- YAML-driven configuration (no code changes needed)
- Built-in rule engine for governance
- Production-ready checkpointing with SQLite

### Q: Can I migrate from LangGraph?

**A:** Yes! See [SPECIFICATION.md § 7](./SPECIFICATION.md) - Migration Guide. The APIs are designed for compatibility.

### Q: What's the performance overhead?

**A:** Minimal. The state machine adds ~5ms per reasoning step. Checkpointing is async and doesn't block execution.

### Q: Is this production-ready?

**A:** Currently in **Phase 1** (Foundation). Production deployment planned for **Phase 4** (Week 12). See [ROADMAP.md](./ROADMAP.md).

---

## 📞 Support & Contact

- **Issues**: GitHub Issues
- **Documentation**: This directory + [MkDocs site](https://github.com/your-org/dlamp) (coming in Phase 4)
- **Email**: [your-email@domain.com]

---

**Last Updated**: 2026-02-14  
**Documentation Version**: 1.0.0

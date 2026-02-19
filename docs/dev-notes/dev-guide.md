# Arkhon-Rheo + Arkhon-Rheo Development Guide

**Version**: 1.0.0  
**Status**: Draft  
**Last Updated**: 2026-02-14  
**Code Path**: `src/arkhon-rheo/`

---

## 1. Getting Started

### 1.1 Prerequisites

**Required**:

- Python 3.12+
- uv (package manager)
- Git

**Optional**:

- Docker (for local vector DB testing)
- Make (for convenience commands)

### 1.2 Repository Setup

> **注意**: 本文件中的路徑使用標準相對路徑 `src/arkhon-rheo/`。
> 您的實際專案可能位於不同的絕對路徑（如 `/wk2/yaochu/github/dlamp/src/arkhon-rheo`）。
> 請根據您的環境調整路徑。

```bash
# 導航到專案目錄（使用相對路徑）
cd src/arkhon-rheo

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate

# Verify installation
python -c "import arkhon_rheo; print(arkhon_rheo.__version__)"
```

### 1.3 Project Structure

```text
src/arkhon-rheo/
├── arkhon_rheo/          # Main package
│   ├── __init__.py
│   ├── core/             # State machine & graph
│   ├── nodes/            # ReAct nodes
│   ├── tools/            # Tool registry & implementations
│   ├── rules/            # Governance rules
│   ├── memory/           # Memory systems
│   ├── runtime/          # Execution runtime
│   ├── config/           # Configuration loading
│   └── cli/              # Command-line interface
├── tests/                # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── examples/             # Example projects
├── docs/                 # Documentation
├── pyproject.toml        # Package metadata
└── README.md
```

---

## 2. Development Workflow

### 2.1 Branch Strategy

**Main Branches**:

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - Feature branches
- `hotfix/*` - Emergency fixes

**Workflow**:

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "feat: add feature X"

# Push and create PR
git push origin feature/my-feature
# Create PR: feature/my-feature → develop
```

### 2.2 Commit Convention

**Format**: `<type>(<scope>): <subject>`

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring
- `test`: Add/update tests
- `chore`: Build process, dependencies

**Examples**:

```bash
git commit -m "feat(tools): add web search tool"
git commit -m "fix(graph): prevent infinite loops"
git commit -m "docs(readme): update installation instructions"
```

### 2.3 Code Quality Checks

**Before Commit**:

```bash
# Format code
ruff format src/arkhon-rheo

# Lint
ruff check src/arkhon-rheo --fix

# Type check
mypy --strict src/arkhon-rheo

# Run tests
pytest tests/ -v

# Check coverage
pytest --cov=arhon_rheo --cov-report=html
```

**Pre-commit Hook** (`.git/hooks/pre-commit`):

```bash
#!/bin/bash
ruff check src/arkhon-rheo || exit 1
mypy src/arkhon-rheo || exit 1
pytest tests/unit || exit 1
```

---

## 3. Development Environment

### 3.1 IDE Configuration

**VSCode** (`.vscode/settings.json`):

```json
{
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "none",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "python.testing.pytestEnabled": true
}
```

**PyCharm**:

- Enable mypy plugin
- Configure Ruff as external tool
- Set pytest as test runner

### 3.2 Environment Variables

**Create `.env` file**:

```bash
# LLM Provider
OPENAI_API_KEY=sk-your-key-here

# Vector Store (optional)
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=your-environment

# Logging
LOG_LEVEL=DEBUG
STRUCTURED_LOGS=true

# Development
ARKHON_RHEO_ENV=development
```

**Load in code**:

```python
from dotenv import load_dotenv

load_dotenv()  # Reads .env file
```

---

## 4. Running the Agent

### 4.1 Quick Start

```bash
# Run example agent
python src/arkhon-rheo/dev.py
```

**Script content** (`dev.py`):

```python
from arkhon_rheo import Graph, AgentState
from arkhon_rheo.nodes import ThoughtNode, ActionNode
from arkhon_rheo.config import Config

# Load config
config = Config.from_yaml("config/default.yaml")

# Build graph
graph = Graph()
graph.add_node("thought", ThoughtNode(config.llm))
graph.add_node("action", ActionNode(config.tools))
graph.add_edge("thought", "action")
graph.add_edge("action", "__end__")

# Run
initial_state = AgentState(
    trace_id="dev-001",
    steps=[],
    current_node="thought",
    metadata={"goal": "Find information about X"}
)

result = graph.run(initial_state)
print(f"Completed in {len(result.steps)} steps")
```

### 4.2 CLI Usage

```bash
# Initialize new project
arkhon-rheo init my-agent --template basic

# Validate config
arkhon-rheo config validate config/my-config.yaml

# Run agent
arkhon-rheo run --config config/my-config.yaml

# Interactive REPL
arkhon-rheo repl
```

---

## 5. Writing Tests

### 5.1 Unit Test Example

```python
# tests/unit/core/test_state.py
import pytest
from arkhon_rheo.core.state import AgentState, ReasoningStep

def test_state_immutability():
    state = AgentState(trace_id="test", steps=[], current_node="thought")
    
    # Should raise error (frozen dataclass)
    with pytest.raises(AttributeError):
        state.trace_id = "modified"
        
def test_step_creation():
    step = ReasoningStep(
        id=0,
        thought="Test thought",
        action=None,
        observation=None,
        status="draft"
    )
    
    assert step.thought == "Test thought"
    assert step.status == "draft"
```

### 5.2 Integration Test Example

```python
# tests/integration/test_react_cycle.py
def test_full_react_cycle(mock_llm, mock_tools):
    graph = Graph()
    graph.add_node("thought", ThoughtNode(mock_llm))
    graph.add_node("action", ActionNode(mock_tools))
    graph.add_edge("thought", "action")
    
    initial_state = AgentState(...)
    result = graph.run(initial_state, max_steps=3)
    
    assert len(result.steps) >= 1
    assert result.steps[0].thought is not None
    assert result.steps[0].observation is not None
```

### 5.3 Test Fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def mock_llm():
    class MockLLM:
        def generate(self, prompt: str) -> str:
            return "I should search for information"
    return MockLLM()

@pytest.fixture
def sample_state():
    return AgentState(
        trace_id="test-123",
        steps=[],
        current_node="thought"
    )
```

---

## 6. Debugging

### 6.1 Enable Debug Logging

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ]
)

logger = structlog.get_logger()
logger.setLevel("DEBUG")
```

### 6.2 Inspect State

```python
from pprint import pprint

# Print current state
pprint(state.to_dict())

# Print last N steps
for step in state.steps[-5:]:
    print(f"Step {step.id}: {step.thought}")
```

### 6.3 Checkpoint Inspection

```python
from arkhon_rheo.runtime.checkpoint import CheckpointManager

mgr = CheckpointManager(".checkpoints.db")

# List all checkpoints
checkpoints = mgr.list_all()
for cp in checkpoints:
    print(f"{cp.trace_id} - {cp.timestamp}")
    
# Load specific checkpoint
state = mgr.load("trace-abc123")
```

---

## 7. Adding New Components

### 7.1 Add a Custom Node

```python
# arkhon_rheo/nodes/custom_node.py
from arkhon_rheo.nodes.base import BaseNode
from arkhon_rheo.core.state import AgentState

class MyCustomNode(BaseNode):
    def run(self, state: AgentState) -> AgentState:
        # Custom logic here
        result = perform_custom_logic(state)
        
        # Update state
        return replace(state, metadata={
            **state.metadata,
            "custom_result": result
        })
```

**Register in graph**:

```python
graph.add_node("custom", MyCustomNode())
graph.add_edge("thought", "custom")
graph.add_edge("custom", "action")
```

### 7.2 Add a Custom Tool

```python
# arkhon_rheo/tools/custom/my_tool.py
from arkhon_rheo.tools.base import Tool, ToolResult

class MyTool(Tool):
    name = "my_custom_tool"
    description = "Performs custom action on input"
    
    def execute(self, query: str, param: int = 10) -> ToolResult:
        result = my_custom_function(query, param)
        return ToolResult(
            success=True,
            output=result,
            metadata={"param_used": param}
        )
```

**Register**:

```python
from arkhon_rheo.tools.registry import ToolRegistry

registry = ToolRegistry()
registry.register(MyTool())
```

### 7.3 Add a Custom Rule

```python
# arkhon_rheo/rules/custom/my_rule.py
from arkhon_rheo.rules.base import Rule
from arkhon_rheo.core.state import ReasoningStep

class MyCustomRule(Rule):
    name = "my_rule"
    
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        
    def check(self, step: ReasoningStep) -> bool:
        # Custom validation logic
        return confidence_score(step.thought) >= self.threshold
        
    @property
    def violation_message(self) -> str:
        return f"Confidence below {self.threshold}"
```

---

## 8. Configuration Management

### 8.1 YAML Structure

```yaml
engine:
  max_steps: 20
  checkpoint_interval: 5
  interruptible: false

llm:
  provider: openai
  model: gpt-4o-mini
  temperature: 0.0
  max_tokens: 500

tools:
  - name: search
    enabled: true
    config:
      api_key: ${SEARCH_API_KEY}
  - name: calculator
    enabled: true

rules:
  - type: max_depth
    value: 10
  - type: cost_limit
    value: 0.50

memory:
  short_term:
    max_tokens: 8000
  long_term:
    type: pinecone
    index: agent-memory
```

### 8.2 Load Config

```python
from arkhon_rheo.config import Config

# From file
config = Config.from_yaml("config/my-config.yaml")

# From dict
config = Config.from_dict({
    "engine": {"max_steps": 30},
    "llm": {"provider": "openai", "model": "gpt-4"}
})

# With env var expansion
config = Config.from_yaml("config.yaml", expand_env=True)
```

---

## 9. Performance Profiling

### 9.1 Profiling Execution

```python
import cProfile
import pstats

# Profile graph execution
profiler = cProfile.Profile()
profiler.enable()

result = graph.run(initial_state)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats(20)  # Top 20 functions
```

### 9.2 Memory Profiling

```python
from memory_profiler import profile

@profile
def run_agent():
    graph = Graph()
    # ... setup
    result = graph.run(initial_state)
    return result

if __name__ == "__main__":
    run_agent()
```

**Run**:

```bash
python -m memory_profiler script.py
```

---

## 10. Deployment

### 10.1 Local Development Server

```python
# server.py
from fastapi import FastAPI
from arkhon_rheo import Graph, AgentState

app = FastAPI()

@app.post("/execute")
async def execute_agent(request: dict):
    initial_state = AgentState(**request)
    result = graph.run(initial_state)
    return result.to_dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 10.2 Production Checklist

- [ ] Environment variables configured
- [ ] Secrets managed via external vault
- [ ] Logging set to INFO level
- [ ] Metrics endpoint exposed
- [ ] Health check endpoint
- [ ] Rate limiting enabled
- [ ] Checkpointing configured
- [ ] Error monitoring (Sentry) enabled

---

## 11. Troubleshooting

### 11.1 Common Issues

**Issue**: `ImportError: No module named 'arkhon_rheo'`

**Solution**:

```bash
# Ensure you're in virtual environment
source .venv/bin/activate

# Reinstall package
uv sync
```

---

**Issue**: Tests fail with "Checkpoint DB locked"

**Solution**:

```python
# Use separate test DB
import pytest

@pytest.fixture
def checkpoint_mgr(tmp_path):
    db_path = tmp_path / "test.db"
    return CheckpointManager(str(db_path))
```

---

**Issue**: LLM API timeout

**Solution**:

```python
# Increase timeout in config
llm:
  provider: openai
  timeout: 30  # seconds
```

---

### End of Development Guide

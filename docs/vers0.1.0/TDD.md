# Arkhon-Rheo + ReActEngine Test-Driven Development Strategy

**Version**: 1.0.0  
**Status**: Draft  
**Last Updated**: 2026-02-14  
**Code Path**: `src/arkhon-rheo/`

---

## 1. TDD Principles for Agent Systems

### 1.1 Why TDD for Agents?

**Challenges**:

- Non-deterministic LLM outputs
- Complex state transitions
- External API dependencies
- Long execution loops

**Benefits**:

- Catch edge cases early
- Document expected behavior
- Enable safe refactoring
- Build confidence in system reliability

### 1.2 Core Philosophy

```text
RED → GREEN → REFACTOR

1. Write failing test (RED)
2. Write minimal code to pass (GREEN)
3. Improve code quality (REFACTOR)
```

**Modified for Agents**:

```text
RED → MOCK → GREEN → VERIFY

1. Write failing test with expected behavior
2. Mock non-deterministic components (LLM, tools)
3. Implement until test passes
4. Verify with integration tests
```

---

## 2. Test Pyramid

```text
     /\\
    /E2E\\       5 tests  (Full agent workflows)
   /------\\
  /Integ  \\    30 tests (Multi-component integration)
 /----------\\
/   Unit    \\  150 tests (Individual components)
--------------
```

**Distribution**:

- **70%** Unit tests (fast, isolated)
- **20%** Integration tests (multi-component)
- **10%** E2E tests (full workflows)

---

## 3. Unit Testing Strategy

### 3.1 Testing State Management

**Test**: State immutability

```python
# tests/unit/core/test_state.py
import pytest
from dataclasses import FrozenInstanceError
from arkhon_rheo.core.state import ReActState

def test_state_is_frozen():
    \"\"\"States must be immutable to ensure event sourcing integrity.\"\"\"
    state = ReActState(trace_id=\"test\", steps=[], current_node=\"thought\")
    
    with pytest.raises(FrozenInstanceError):
        state.trace_id = \"modified\"
        
def test_state_equality():
    \"\"\"States with same data should be equal.\"\"\"
    state1 = ReActState(trace_id=\"test\", steps=[], current_node=\"thought\")
    state2 = ReActState(trace_id=\"test\", steps=[], current_node=\"thought\")
    
    assert state1 == state2
```

### 3.2 Testing Nodes

**Test**: ThoughtNode with mocked LLM

```python
# tests/unit/nodes/test_thought_node.py
import pytest
from arkhon_rheo.nodes.thought_node import ThoughtNode

class MockLLM:
    def generate(self, prompt: str, **kwargs) -> str:
        return \"I should search for information about X\"
        
def test_thought_node_creates_reasoning_step():
    \"\"\"ThoughtNode should append new reasoning step with LLM output.\"\"\"
    # Arrange
    node = ThoughtNode(llm=MockLLM())
    state = ReActState(trace_id=\"test\", steps=[], current_node=\"thought\")
    
    # Act
    new_state = node.run(state)
    
    # Assert
    assert len(new_state.steps) == 1
    assert new_state.steps[0].thought == \"I should search for information about X\"
    assert new_state.steps[0].status == \"draft\"
    assert new_state.current_node == \"validate\"  # Transitions to next node
```

### 3.3 Testing Rules

**Test**: MaxDepthRule

```python
# tests/unit/rules/test_max_depth_rule.py
from arkhon_rheo.rules.builtin import MaxDepthRule
from arkhon_rheo.core.state import ReActState, ReasoningStep

def test_max_depth_rule_passes_when_under_limit():
    \"\"\"Rule should pass when step count is below threshold.\"\"\"
    rule = MaxDepthRule(max_depth=10)
    
    state = ReActState(
        trace_id=\"test\",
        steps=[ReasoningStep(...) for _ in range(5)],  # 5 steps
        current_node=\"thought\"
    )
    
    # Should not raise
    rule.validate(state)
    
def test_max_depth_rule_fails_when_over_limit():
    \"\"\"Rule should raise RuleViolationError when limit exceeded.\"\"\"
    rule = MaxDepthRule(max_depth=10)
    
    state = ReActState(
        trace_id=\"test\",
        steps=[ReasoningStep(...) for _ in range(15)],  # 15 steps (over limit)
        current_node=\"thought\"
    )
    
    with pytest.raises(RuleViolationError) as exc_info:
        rule.validate(state)
        
    assert \"max_depth\" in str(exc_info.value)
```

### 3.4 Testing Tools

**Test**: Calculator tool

```python
# tests/unit/tools/test_calculator.py
from arkhon_rheo.tools.builtin.calculator import CalculatorTool

def test_calculator_basic_arithmetic():
    \"\"\"Calculator should evaluate simple expressions.\"\"\"
    tool = CalculatorTool()
    
    result = tool.execute(expression=\"2 + 2\")
    
    assert result.success is True
    assert result.output == \"4\"
    
def test_calculator_rejects_dangerous_input():
    \"\"\"Calculator should reject eval/exec attempts.\"\"\"
    tool = CalculatorTool()
    
    with pytest.raises(SecurityError):
        tool.execute(expression=\"__import__('os').system('ls')\")
```

---

## 4. Integration Testing Strategy

### 4.1 Testing Graph Execution

**Test**: Complete ReAct cycle

```python
# tests/integration/test_react_cycle.py
def test_full_react_cycle():
    \"\"\"Test complete thought→validate→action→observe→commit cycle.\"\"\"
    # Arrange
    mock_llm = MockLLM()
    mock_tools = MockToolRegistry()
    
    graph = StateGraph()
    graph.add_node(\"thought\", ThoughtNode(mock_llm))
    graph.add_node(\"validate\", ValidateNode(RuleEngine()))
    graph.add_node(\"action\", ActionNode(mock_tools))
    graph.add_node(\"observe\", ObservationNode())
    graph.add_node(\"commit\", CommitNode())
    
    graph.add_edge(\"thought\", \"validate\")
    graph.add_edge(\"validate\", \"action\")
    graph.add_edge(\"action\", \"observe\")
    graph.add_edge(\"observe\", \"commit\")
    graph.add_edge(\"commit\", \"__end__\")
    
    initial_state = ReActState(
        trace_id=\"test\",
        steps=[],
        current_node=\"thought\"
    )
    
    # Act
    result = graph.run(initial_state, max_steps=5)
    
    # Assert
    assert len(result.steps) >= 1
    assert result.steps[0].thought is not None
    assert result.steps[0].action is not None
    assert result.steps[0].observation is not None
    assert result.steps[0].status == \"committed\"
    assert result.terminated is True
```

### 4.2 Testing Multi-Agent Coordination

**Test**: Coordinator delegating to specialists

```python
# tests/integration/test_multi_agent.py
def test_coordinator_delegates_to_specialists():
    \"\"\"Coordinator should route tasks to appropriate specialist agents.\"\"\"
    # Arrange
    coordinator = CoordinatorAgent()
    planner = PlanningAgent()
    coder = CodingAgent()
    
    task = \"Implement login validation\"
    
    # Act
    coordinator.assign_task(task)
    plan = coordinator.await_response_from(planner)
    code = coordinator.await_response_from(coder)
    
    # Assert
    assert plan is not None
    assert \"steps\" in plan
    assert code is not None
    assert \"diff\" in code
```

### 4.3 Testing Checkpoint/Restore

**Test**: Rollback to previous step

```python
# tests/integration/test_checkpointing.py
def test_rollback_restores_previous_state(tmp_path):
    \"\"\"Checkpointing should allow rollback to any previous step.\"\"\"
    # Arrange
    checkpoint_mgr = CheckpointManager(tmp_path / \"test.db\")
    graph = create_test_graph()
    
    initial_state = ReActState(...)
    
    # Act - Execute 5 steps
    state_after_step_3 = None
    for i in range(5):
        state = graph.step(state)
        checkpoint_mgr.save(state)
        if i == 2:
            state_after_step_3 = state
            
    # Rollback to step 3
    restored_state = checkpoint_mgr.load(state_after_step_3.trace_id)
    
    # Assert
    assert restored_state == state_after_step_3
    assert len(restored_state.steps) == 3
```

---

## 5. End-to-End Testing Strategy

### 5.1 Real-World Scenarios

**Test**: Research and summarize topic

```python
# tests/e2e/test_research_workflow.py
@pytest.mark.e2e
@pytest.mark.slow
def test_agent_researches_and_summarizes_topic():
    \"\"\"Agent should search, gather info, and produce summary.\"\"\"
    # This uses REAL LLM and tools (marked as slow test)
    
    config = Config.from_yaml(\"config/test.yaml\")
    graph = build_production_graph(config)
    
    initial_state = ReActState(
        trace_id=str(uuid.uuid4()),
        steps=[],
        current_node=\"thought\",
        metadata={\"goal\": \"Research quantum computing basics\"}
    )
    
    # Run with 30s timeout
    with timeout(30):
        result = graph.run(initial_state, max_steps=20)
        
    # Verify
    assert result.terminated
    assert len(result.steps) >= 3  # At least search, read, summarize
    
    # Check that search tool was used
    actions = [s.action for s in result.steps if s.action]
    assert \"search\" in actions
    
    # Check summary quality (basic heuristic)
    final_thought = result.steps[-1].thought
    assert len(final_thought) > 100  # Non-trivial summary
    assert \"quantum\" in final_thought.lower()
```

### 5.2 Failure Recovery

**Test**: Agent recovers from tool failure

```python
@pytest.mark.e2e
def test_agent_recovers_from_tool_failure():
    \"\"\"Agent should retry or use alternative when tool fails.\"\"\"
    graph = build_test_graph_with_flaky_tool()
    
    initial_state = ReActState(...)
    
    result = graph.run(initial_state, max_steps=10)
    
    # Verify retry or alternative action taken
    failed_steps = [s for s in result.steps if s.status == \"failed\"]
    assert len(failed_steps) >= 1  # Tool failed at least once
    
    successful_steps = [s for s in result.steps if s.status == \"committed\"]
    assert len(successful_steps) >= 1  # Eventually succeeded
```

---

## 6. TDD Workflow Example

### 6.1 Implementing a New Node (RED → GREEN → REFACTOR)

#### Step 1: RED - Write failing test

```python
# tests/unit/nodes/test_summarize_node.py
def test_summarize_node_condenses_previous_steps():
    \"\"\"SummarizeNode should create concise summary of previous steps.\"\"\"
    # Arrange
    node = SummarizeNode(llm=MockLLM())
    state = ReActState(
        steps=[
            ReasoningStep(thought=\"Step 1\", ...),
            ReasoningStep(thought=\"Step 2\", ...),
            ReasoningStep(thought=\"Step 3\", ...)
        ]
    )
    
    # Act
    new_state = node.run(state)
    
    # Assert
    assert \"summary\" in new_state.metadata
    assert len(new_state.metadata[\"summary\"]) < sum(len(s.thought) for s in state.steps)
```

**Run**: `pytest tests/unit/nodes/test_summarize_node.py`

**Result**: ❌ FAIL (SummarizeNode doesn't exist)

---

#### Step 2: GREEN - Implement minimal code

```python
# arkhon_rheo/nodes/summarize_node.py
from arkhon_rheo.nodes.base import BaseNode

class SummarizeNode(BaseNode):
    def __init__(self, llm):
        self.llm = llm
        
    def run(self, state: ReActState) -> ReActState:
        # Minimal implementation
        all_thoughts = \" \".join(s.thought for s in state.steps)
        summary = self.llm.generate(f\"Summarize: {all_thoughts}\")
        
        return replace(state, metadata={
            **state.metadata,
            \"summary\": summary
        })
```

**Run**: `pytest tests/unit/nodes/test_summarize_node.py`

**Result**: ✅ PASS

---

#### Step 3: REFACTOR - Improve code quality

```python
class SummarizeNode(BaseNode):
    \"\"\"Node that condenses previous reasoning steps into a concise summary.\"\"\"
    
    MAX_CONTEXT_LENGTH = 2000  # Characters
    
    def __init__(self, llm: LLMClient):
        self.llm = llm
        
    def run(self, state: ReActState) -> ReActState:
        context = self._build_context(state.steps)
        summary = self._generate_summary(context)
        
        logger.info(
            \"summary_generated\",
            original_length=len(context),
            summary_length=len(summary)
        )
        
        return replace(state, metadata={
            **state.metadata,
            \"summary\": summary
        })
        
    def _build_context(self, steps: list[ReasoningStep]) -> str:
        \"\"\"Build context from reasoning steps, truncating if needed.\"\"\"
        context = \"\\n\".join(
            f\"Step {s.id}: {s.thought}\" for s in steps
        )
        
        if len(context) > self.MAX_CONTEXT_LENGTH:
            context = context[:self.MAX_CONTEXT_LENGTH] + \"...\"
            
        return context
        
    def _generate_summary(self, context: str) -> str:
        \"\"\"Generate LLM summary with retry logic.\"\"\"
        prompt = f\"Provide a concise summary of the following reasoning:\\n{context}\"
        
        for attempt in range(3):
            try:
                return self.llm.generate(prompt, max_tokens=200)
            except Exception as e:
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
```

**Run**: `pytest tests/unit/nodes/test_summarize_node.py`

**Result**: ✅ PASS (with improved code quality)

---

## 7. Test Fixtures

### 7.1 Common Fixtures

```python
# tests/conftest.py
import pytest
from arkhon_rheo.core.state import ReActState, ReasoningStep

@pytest.fixture
def mock_llm():
    class MockLLM:
        def generate(self, prompt: str, **kwargs) -> str:
            if \"search\" in prompt.lower():
                return \"I should search for information\"
            elif \"summarize\" in prompt.lower():
                return \"Summary: ...\"
            return \"Default response\"
    return MockLLM()

@pytest.fixture
def sample_state():
    return ReActState(
        trace_id=\"test-123\",
        steps=[],
        current_node=\"thought\",
        metadata={},
        terminated=False
    )

@pytest.fixture
def sample_state_with_steps():
    return ReActState(
        trace_id=\"test-456\",
        steps=[
            ReasoningStep(id=0, thought=\"Thought 1\", status=\"committed\"),
            ReasoningStep(id=1, thought=\"Thought 2\", status=\"committed\"),
        ],
        current_node=\"action\"
    )

@pytest.fixture
def tool_registry():
    from arkhon_rheo.tools.registry import ToolRegistry
    registry = ToolRegistry()
    # Register mock tools
    return registry

@pytest.fixture
def checkpoint_db(tmp_path):
    return CheckpointManager(tmp_path / \"test.db\")
```

---

## 8. Mocking Strategies

### 8.1 Mocking LLM Responses

```python
class PredictableLLM:
    \"\"\"LLM that returns deterministic responses based on prompt keywords.\"\"\"
    
    def __init__(self, response_map: dict[str, str]):
        self.response_map = response_map
        
    def generate(self, prompt: str, **kwargs) -> str:
        for keyword, response in self.response_map.items():
            if keyword in prompt.lower():
                return response
        return \"Default response\"

# Usage in test
llm = PredictableLLM({
    \"search for\": \"I should use the search tool\",
    \"calculate\": \"I should use the calculator tool\"
})
```

### 8.2 Mocking Tools

```python
class MockTool(Tool):
    name = \"mock_tool\"
    description = \"Mock tool for testing\"
    
    def __init__(self, return_value: str = \"Mock result\"):
        self._return_value = return_value
        
    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(
            success=True,
            output=self._return_value,
            metadata={\"mock\": True}
        )
```

---

## 9. Code Coverage

### 9.1 Coverage Goals

| Component | Target Coverage | Current |
| :--- | :--- | :--- |
| core/ | 95% | TBD |
| nodes/ | 90% | TBD |
| tools/ | 85% | TBD |
| rules/ | 95% | TBD |
| Overall | 90% | TBD |

### 9.2 Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=arkhon_rheo --cov-report=html

# View report
open htmlcov/index.html
```

### 9.3 Coverage in CI

```yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: |
    pytest --cov=arkhon_rheo --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
```

---

## 10. Test Organization

```text
tests/
├── unit/
│   ├── core/
│   │   ├── test_state.py
│   │   ├── test_graph.py
│   │   └── test_step.py
│   ├── nodes/
│   │   ├── test_thought_node.py
│   │   ├── test_action_node.py
│   │   └── test_validate_node.py
│   ├── tools/
│   │   ├── test_registry.py
│   │   └── builtin/
│   │       ├── test_search.py
│   │       └── test_calculator.py
│   └── rules/
│       ├── test_rule_engine.py
│       └── test_builtin_rules.py
├── integration/
│   ├── test_react_cycle.py
│   ├── test_multi_agent.py
│   └── test_checkpointing.py
├── e2e/
│   ├── test_research_workflow.py
│   └── test_coding_workflow.py
└── conftest.py
```

---

### End of TDD Strategy Document

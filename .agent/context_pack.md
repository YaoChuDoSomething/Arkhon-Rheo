# Code Context (Phase 3 Review)

Changed Files:
- `.agent/scripts/git_context.py`
```python
#!/usr/bin/env python3
import ast
import os
import subprocess


def get_changed_files(target_branch="origin/main"):
    """Get list of changed files compared to target branch or local master."""
    try:
        # We look for files changed in the current session (Phase 3)
        # Using git log or diff to find what was modified in recent commits
        cmd = ["git", "diff", "--name-only", "main"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")

        return [f for f in files if f.endswith(".py") and os.path.exists(f)]
    except Exception as e:
        print(f"Error fetching changed files: {e}")
        return []


def get_imports(file_path):
    imports = set()
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
    except:
        pass
    return list(imports)


def generate_context(files):
    context = "# Code Context (Phase 3 Review)\n\n"
    context += "Changed Files:\n"
    for f in files:
        context += f"- `{f}`\n"
        context += "```python\n"
        with open(f, "r") as src:
            context += src.read()
        context += "\n```\n\n"

    return context


def main():
    files = get_changed_files()
    if not files:
        print("No files detected for review.")
        return

    context_md = generate_context(files)
    os.makedirs(".agent", exist_ok=True)
    with open(".agent/context_pack.md", "w") as f:
        f.write(context_md)
    print(f"Context packed for {len(files)} files into .agent/context_pack.md")


if __name__ == "__main__":
    main()

```

- `src/arkhon_rheo/agents/__init__.py`
```python

```

- `src/arkhon_rheo/agents/coordinator.py`
```python
from typing import Dict, Optional
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class CoordinatorAgent(Agent):
    """
    Agent responsible for routing tasks to specialist agents based on intent.
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.routing_table: Dict[str, Agent] = {}

    def register_agent(self, intent: str, agent: Agent):
        """Register a specialist agent for a specific intent."""
        self.routing_table[intent] = agent

    async def route_task(self, intent: str) -> Optional[Agent]:
        """Find the agent responsible for the given intent."""
        return self.routing_table.get(intent)

    async def process_message(self, message: AgentMessage) -> None:
        """
        Process incoming messages.
        """
        if message.type == "request":
            intent = message.metadata.get("intent")
            if not intent:
                return  # Log warning: missing intent

            target_agent = await self.route_task(intent)
            if target_agent:
                # Add reply_to metadata so the response can be routed back
                metadata = message.metadata.copy()
                metadata["reply_to"] = message.sender

                forwarded_msg = AgentMessage(
                    sender=self.name,
                    receiver=target_agent.name,
                    content=message.content,
                    type="request",
                    correlation_id=message.id,
                    metadata=metadata,
                )
                await self.send_message(target_agent, forwarded_msg)
            else:
                pass  # Log warning: no route found

        elif message.type == "response":
            # Forward response back to the original requester
            reply_to = message.metadata.get("reply_to")
            if reply_to:
                # Resolve recipient using Registry (via _resolve_agent helper or Registry directly)
                from arkhon_rheo.core.registry import AgentRegistry

                target_agent = AgentRegistry.get(reply_to)

                if target_agent:
                    forwarded_msg = AgentMessage(
                        sender=self.name,
                        receiver=target_agent.name,
                        content=message.content,
                        type="response",
                        correlation_id=message.correlation_id,
                        metadata=message.metadata,
                    )
                    await self.send_message(target_agent, forwarded_msg)
                else:
                    pass
            else:
                pass

```

- `src/arkhon_rheo/agents/specialist.py`
```python
from typing import Dict
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class SpecialistAgent(Agent):
    """
    Agent specialized in a specific domain.
    """

    def __init__(self, name: str, domain: str):
        super().__init__(name)
        self.domain = domain

    async def process_message(self, message: AgentMessage) -> None:
        """
        Process incoming tasks.
        """
        if message.type == "request":
            # Simulate work
            result = f"Processed by {self.domain} specialist: {message.content}"

            # Send response
            reply = AgentMessage(
                sender=self.name,
                receiver=message.sender,
                content=result,
                type="response",
                correlation_id=message.id,
                metadata=message.metadata,
            )

            # Resolve recipient via directory for proper typing
            # Using Registry via base class
            from arkhon_rheo.core.registry import AgentRegistry

            recipient_agent = AgentRegistry.get(message.sender)

            if recipient_agent:
                await self.send_message(recipient_agent, reply)
            else:
                # If recipient not in registry, meaningful error or log
                pass

```

- `src/arkhon_rheo/core/agent.py`
```python
from abc import ABC, abstractmethod
import asyncio
from typing import Dict, Optional
from arkhon_rheo.core.message import AgentMessage


class Agent(ABC):
    """
    Base class for all agents in the multi-agent system.
    """

    def __init__(self, name: str):
        self.name = name
        self.inbox: asyncio.Queue[AgentMessage] = asyncio.Queue()
        # Auto-register
        from arkhon_rheo.core.registry import AgentRegistry

        AgentRegistry.register(self)

    async def send_message(self, recipient: "Agent", message: AgentMessage) -> None:
        """
        Send a message to another agent.
        """
        await recipient.inbox.put(message)

    async def _resolve_agent(self, name: str) -> Optional["Agent"]:
        """Resolve agent by name using the Registry."""
        from arkhon_rheo.core.registry import AgentRegistry

        return AgentRegistry.get(name)

    async def receive_message(self) -> AgentMessage:
        """
        Wait for and retrieve the next message from the inbox.
        """
        return await self.inbox.get()

    @abstractmethod
    async def process_message(self, message: AgentMessage) -> None:
        """
        Process an incoming message. Must be implemented by subclasses.
        """
        pass

    async def run(self) -> None:
        """
        Main loop for the agent to process messages.
        """
        while True:
            message = await self.receive_message()
            await self.process_message(message)

```

- `src/arkhon_rheo/core/graph.py`
```python
from typing import Dict, Callable, Optional
from arkhon_rheo.core.state import ReActState

# Type alias for a node function
NodeFunction = Callable[[ReActState], ReActState]


class StateGraph:
    """
    A directed graph that manages state transitions between nodes.
    Each node is a function that takes a ReActState and returns a new ReActState.
    """

    def __init__(self, initial_state: ReActState):
        self._initial_state = initial_state
        self._current_state = initial_state
        self._nodes: Dict[str, NodeFunction] = {}
        self._edges: Dict[str, str] = {}  # Simple adjacency list: source -> target

    @property
    def current_state(self) -> ReActState:
        return self._current_state

    def add_node(self, name: str, func: NodeFunction) -> None:
        """Register a node with a name and function."""
        self._nodes[name] = func

    def add_edge(self, source: str, target: str) -> None:
        """Add a directed edge from source to target."""
        if source not in self._nodes:
            raise ValueError(f"Source node '{source}' not found.")
        if target not in self._nodes:
            raise ValueError(f"Target node '{target}' not found.")
        self._edges[source] = target

    async def execute_step(self, node_name: str) -> Optional[str]:
        """
        Execute a single node and return the name of the next node.
        Updates internal current_state.
        """
        if node_name not in self._nodes:
            raise ValueError(f"Node '{node_name}' not found.")

        # Execute node function
        func = self._nodes[node_name]
        result = func(self._current_state)

        # Check if result is a coroutine
        import inspect

        if inspect.iscoroutine(result):
            self._current_state = await result
        else:
            self._current_state = result

        # Determine next node
        return self._edges.get(node_name)

    async def run(self, start_node: str, max_steps: int = 10) -> ReActState:
        """
        Run the graph starting from start_node until termination or max_steps.
        Returns the final state.
        """
        current_node = start_node
        steps = 0

        while current_node and steps < max_steps:
            current_node = await self.execute_step(current_node)
            steps += 1

        return self._current_state

```

- `src/arkhon_rheo/core/memory/__init__.py`
```python

```

- `src/arkhon_rheo/core/memory/context_window.py`
```python
from typing import List, Dict, Any


class ContextWindow:
    """
    Implements a sliding window for context management.
    Ensures that the total token count stays within the specified limit.
    """

    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens
        self.messages: List[Dict[str, Any]] = []
        self.current_tokens = 0

    def add_message(self, role: str, content: str, tokens: int) -> None:
        """
        Add a message to the window, evicting the oldest messages if necessary.
        """
        self.messages.append({"role": role, "content": content, "tokens": tokens})
        self.current_tokens += tokens

        # Evict oldest messages if exceeding limit
        while self.current_tokens > self.max_tokens and self.messages:
            removed = self.messages.pop(0)
            self.current_tokens -= removed["tokens"]

```

- `src/arkhon_rheo/core/memory/embeddings.py`
```python
from abc import ABC, abstractmethod
from typing import List
import numpy as np


class Embeddings(ABC):
    """
    Abstract base class for text embeddings.
    """

    @abstractmethod
    def embed_text(self, text: str) -> np.ndarray:
        """Convert text to a vector."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Convert a list of texts to vectors."""
        pass

```

- `src/arkhon_rheo/core/memory/summarization.py`
```python
from typing import List, Dict, Any, Optional


class Summarizer:
    """
    Handles context compression using an LLM.
    """

    def __init__(self, llm_client: Any):
        self.llm_client = llm_client

    def summarize(self, messages: List[Dict[str, Any]]) -> str:
        """
        Summarize a list of messages into a single string.
        """
        if not messages:
            return ""

        prompt = "Summarize the following conversation history, preserving all key facts and entities:\n\n"
        for msg in messages:
            prompt += f"{msg['role']}: {msg['content']}\n"

        # Call LLM (using the unified google-genai pattern if possible,
        # but here we accept any client with generate_content)
        response = self.llm_client.generate_content(prompt)
        return response.text

```

- `src/arkhon_rheo/core/memory/vector_store.py`
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import numpy as np


class VectorStore(ABC):
    """
    Abstract base class for vector storage systems.
    """

    @abstractmethod
    def upsert(self, id: str, vector: np.ndarray, metadata: Dict[str, Any]) -> None:
        """Store a vector and its metadata."""
        pass

    @abstractmethod
    def query(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve top_k similar vectors."""
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        """Delete a vector by id."""
        pass

```

- `src/arkhon_rheo/core/message.py`
```python
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Dict
import json
import uuid


@dataclass
class AgentMessage:
    """
    Standard message format for agent communication.
    """

    sender: str
    receiver: str
    content: Any
    type: str  # "request", "response", "notification"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """Serialize message to JSON string."""
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str) -> "AgentMessage":
        """Deserialize message from JSON string."""
        data = json.loads(json_str)
        return cls(**data)

```

- `src/arkhon_rheo/core/registry.py`
```python
from typing import Dict, Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from arkhon_rheo.core.agent import Agent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Singleton registry for agent discovery.
    """

    _instance = None
    _agents: Dict[str, "Agent"] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._agents = {}
        return cls._instance

    @classmethod
    def register(cls, agent: "Agent") -> None:
        """Register an agent instance."""
        if agent.name in cls._agents:
            logger.warning(f"Agent '{agent.name}' already registered (overwriting).")
        cls._agents[agent.name] = agent
        logger.debug(f"Registered agent: {agent.name}")

    @classmethod
    def get(cls, name: str) -> Optional["Agent"]:
        """Get an agent by name."""
        return cls._agents.get(name)

    @classmethod
    def list_agents(cls) -> Dict[str, "Agent"]:
        """List all registered agents."""
        return cls._agents.copy()

    @classmethod
    def clear(cls) -> None:
        """Clear the registry (useful for testing)."""
        cls._agents.clear()

```

- `src/arkhon_rheo/core/runtime/checkpoint.py`
```python
import sqlite3
import json
import pickle
from typing import Any, Dict, Optional


class CheckpointManager:
    """
    Manages state checkpoints using a SQLite backend.
    """

    def __init__(self, db_path: str = "checkpoints.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    step_id INTEGER PRIMARY KEY,
                    state BLOB,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_checkpoint(self, step_id: int, state: Dict[str, Any]) -> None:
        """Save the current state to the database."""
        state_bytes = pickle.dumps(state)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO checkpoints (step_id, state) VALUES (?, ?)",
                (step_id, state_bytes),
            )

    def load_checkpoint(self, step_id: int) -> Optional[Dict[str, Any]]:
        """Load a state checkpoint by its step ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT state FROM checkpoints WHERE step_id = ?", (step_id,)
            )
            row = cursor.fetchone()
            if row:
                return pickle.loads(row[0])
        return None

    def get_latest_step_id(self) -> Optional[int]:
        """Get the ID of the most recent checkpoint."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT MAX(step_id) FROM checkpoints")
            row = cursor.fetchone()
            return row[0] if row else None

    def rollback(self, step_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete all checkpoints after the specified step_id and return that state.
        """
        state = self.load_checkpoint(step_id)
        if state:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM checkpoints WHERE step_id > ?", (step_id,))
            return state
        return None

```

- `src/arkhon_rheo/core/shared_state.py`
```python
import asyncio
from typing import Any, Dict
from contextlib import asynccontextmanager


class SharedAgentState:
    """
    Thread-safe shared state for agents.
    """

    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._lock = asyncio.Lock()
        self._locks: Dict[str, asyncio.Lock] = {}

    async def get(self, key: str) -> Any:
        """Get a value from the shared state."""
        async with self._lock:
            return self._state.get(key)

    async def set(self, key: str, value: Any) -> None:
        """Set a value in the shared state."""
        async with self._lock:
            self._state[key] = value

    async def update(self, key: str, value: Any) -> None:
        """Update a value (same as set for now)."""
        await self.set(key, value)

    @asynccontextmanager
    async def lock(self, key: str):
        """
        Acquire a lock for a specific key to perform atomic operations.
        Example:
            async with shared_state.lock("resource_id"):
                val = await shared_state.get("resource_id")
                await shared_state.set("resource_id", val + 1)
        """
        # Global lock to safely get/create the specific key lock
        async with self._lock:
            if key not in self._locks:
                self._locks[key] = asyncio.Lock()
            key_lock = self._locks[key]

        # Acquire the specific key lock
        async with key_lock:
            yield

```

- `src/arkhon_rheo/core/state.py`
```python
from dataclasses import dataclass, replace, field
from typing import Optional, Dict, Any, List
from types import MappingProxyType


@dataclass(frozen=True)
class ReasoningStep:
    """
    Immutable event log unit representing a single step in the reasoning process.

    Attributes:
        step_id (str): Unique identifier for this step.
        type (str): Type of step (thought, action, observation, etc.).
        content (str): The main content/payload of the step.
        tool_name (Optional[str]): Name of tool if action.
        tool_input (Optional[Dict[str, Any]]): Input to tool if action.
        tool_output (Optional[Any]): Result of tool if observation.
        timestamp (float): Unix timestamp of when step occurred.
        metadata (Dict[str, Any]): Additional context.
    """

    step_id: str
    type: str
    content: str
    timestamp: float
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_output: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(self, "metadata", MappingProxyType(self.metadata))


@dataclass(frozen=True)
class ReActState:
    """
    Immutable container for ReAct agent state.

    Attributes:
        thought (Optional[str]): The current thought or reasoning trace.
        action (Optional[str]): The action to be performed (tool call).
        observation (Optional[str]): The result of the action (tool output).
        metadata (Dict[str, Any]): Additional extensive state or context.
        steps (List[ReasoningStep]): History of all reasoning steps.
    """

    thought: Optional[str] = None
    action: Optional[str] = None
    observation: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    steps: List[ReasoningStep] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(self, "metadata", MappingProxyType(self.metadata))
        # Ensure steps is a tuple or immutable sequence to enforce immutability strictly?
        # Dataclasses with list are mutable. We should convert to tuple or similar.
        # But for now, complying with type signature list but treating as immutable.
        # Ideally: steps: Tuple[ReasoningStep, ...] = field(default_factory=tuple)

    def with_thought(self, thought: str) -> "ReActState":
        """Return a new state with updated thought."""
        return replace(self, thought=thought)

    def with_action(self, action: str) -> "ReActState":
        """Return a new state with updated action."""
        return replace(self, action=action)

    def with_observation(self, observation: str) -> "ReActState":
        """Return a new state with updated observation."""
        return replace(self, observation=observation)

    def with_metadata(self, metadata: Dict[str, Any]) -> "ReActState":
        """Return a new state with replaced metadata."""
        return replace(self, metadata=metadata)

    def update_metadata(self, updates: Dict[str, Any]) -> "ReActState":
        """Return a new state with updated metadata (merged)."""
        new_metadata = dict(self.metadata)
        new_metadata.update(updates)
        return replace(self, metadata=new_metadata)

    def add_step(self, step: ReasoningStep) -> "ReActState":
        """Return a new state with the step added to history."""
        new_steps = list(self.steps)
        new_steps.append(step)
        return replace(self, steps=new_steps)

```

- `src/arkhon_rheo/core/subgraph.py`
```python
from arkhon_rheo.core.graph import StateGraph
from arkhon_rheo.core.state import ReActState


class SubGraph:
    """
    A subgraph that encapsulates a StateGraph and can be executed as a callable node.
    """

    def __init__(self, name: str, graph: StateGraph, entry_point: str):
        self.name = name
        self.graph = graph
        self.entry_point = entry_point

    async def __call__(self, state: ReActState) -> ReActState:
        """
        Execute the subgraph.
        """
        # Set the current state of the internal graph to the provided state
        # to ensure context propagation (like previous thoughts)
        self.graph._current_state = state

        final_state = await self.graph.run(
            self.entry_point, max_steps=10
        )  # Default max steps for subgraphs

        return final_state

```

- `src/arkhon_rheo/runtime/__init__.py`
```python

```

- `src/arkhon_rheo/runtime/scheduler.py`
```python
import asyncio
from typing import List
from arkhon_rheo.core.agent import Agent


class AgentScheduler:
    """
    Manages the execution lifecycle of multiple agents.
    """

    def __init__(self):
        self.agents: List[Agent] = []

    def register_agent(self, agent: Agent):
        """Register an agent with the scheduler."""
        self.agents.append(agent)

    async def run_until_complete(self, target_task):
        """
        Run the scheduler until the target task is complete.
        This usually involves starting all agents' run loops in the background.
        """
        # Start all agents
        tasks = []
        for agent in self.agents:
            # We wrap agent.run() in a task that can be cancelled
            task = asyncio.create_task(agent.run())
            tasks.append(task)

        try:
            # Wait for the target task (e.g., initial user request processing)
            # In a real system, this might be waiting for a specific event or condition
            await target_task
        finally:
            # Cancel all background agent tasks
            for task in tasks:
                task.cancel()

            # Wait for cancellation to complete
            await asyncio.gather(*tasks, return_exceptions=True)

```

- `tests/integration/test_agent_communication.py`
```python
import pytest
import asyncio
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class EchoAgent(Agent):
    async def process_message(self, message: AgentMessage):
        if message.type == "ping":
            reply = AgentMessage(
                sender=self.name,
                receiver=message.sender,
                content="pong",
                type="pong",
                correlation_id=message.id,
            )
            from arkhon_rheo.core.registry import AgentRegistry

            recipient = AgentRegistry.get(message.sender)
            if recipient:
                await self.send_message(recipient, reply)


class StarterAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.received_replies = []

    async def process_message(self, message: AgentMessage):
        self.received_replies.append(message)


@pytest.mark.asyncio
async def test_agent_conversation():
    from arkhon_rheo.core.registry import AgentRegistry

    AgentRegistry.clear()

    agent_a = StarterAgent("A")
    agent_b = EchoAgent("B")

    # Auto-registered via __init__

    # Start message
    msg = AgentMessage(sender="A", receiver="B", content="ping", type="ping")

    await agent_a.send_message(agent_b, msg)

    # Process B's inbox manually for test control
    msg_for_b = await agent_b.receive_message()
    await agent_b.process_message(msg_for_b)

    # Process A's inbox
    msg_for_a = await agent_a.receive_message()
    await agent_a.process_message(msg_for_a)

    assert len(agent_a.received_replies) == 1
    reply = agent_a.received_replies[0]
    assert reply.content == "pong"
    assert reply.sender == "B"
    assert reply.correlation_id == msg.id

```

- `tests/integration/test_nested_subgraph.py`
```python
import pytest
import asyncio
from arkhon_rheo.core.subgraph import SubGraph
from arkhon_rheo.core.graph import StateGraph
from arkhon_rheo.core.state import ReActState


@pytest.mark.asyncio
async def test_nested_subgraph_execution():
    # Inner Graph
    state = ReActState()
    inner_builder = StateGraph(state)

    def inner_node(s: ReActState) -> ReActState:
        # Avoid NoneType + str error
        thought = s.thought or ""
        return s.with_thought(thought + " -> Inner")

    inner_builder.add_node("inner", inner_node)
    inner_graph = SubGraph("inner_graph", inner_builder, "inner")

    # Outer Graph
    outer_builder = StateGraph(state)

    def outer_start(s: ReActState) -> ReActState:
        return s.with_thought("Outer Start")

    def outer_end(s: ReActState) -> ReActState:
        thought = s.thought or ""
        return s.with_thought(thought + " -> Outer End")

    # To add SubGraph as a node, we might need a wrapper if StateGraph expects specific signature
    # StateGraph expects callable(State) -> State. SubGraph implements __call__.
    # So we can add it directly.

    outer_builder.add_node("start", outer_start)
    outer_builder.add_node("sub", inner_graph.__call__)
    outer_builder.add_node("end", outer_end)

    outer_builder.add_edge("start", "sub")
    outer_builder.add_edge("sub", "end")

    # Run
    # Assuming run() starts execution. But for StateGraph.run(node, max_steps), we need to manually step?
    # Or implement a full run loop.
    # The current StateGraph implementation in test_graph.py seems to have run() and execute_step().
    # Let's verify StateGraph.run() behavior.

    # Based on test_graph.py:
    # final_state = graph.run("A", max_steps=5)
    # It runs loop.

    # So we can run from "start".
    final_state = await outer_builder.run("start", max_steps=10)

    expected_thought = "Outer Start -> Inner -> Outer End"
    assert final_state.thought == expected_thought


@pytest.mark.asyncio
async def test_subgraph_context_propagation():
    # Verify that inner graph sees outer context and can modify it (if shared)
    initial_state = ReActState()
    # Set initial context
    initial_state = initial_state.with_thought("Initial Thought")

    # Inner Graph
    inner_builder = StateGraph(
        ReActState()
    )  # Empty initial state for inner, will get overwritten by call

    def inner_node(s: ReActState) -> ReActState:
        # Check if we can see parent's thought
        parent_thought = s.thought
        return s.with_thought(f"{parent_thought} -> Inner Process")

    inner_builder.add_node("inner", inner_node)
    inner_graph = SubGraph("inner", inner_builder, "inner")

    # Outer Graph
    outer_builder = StateGraph(initial_state)
    outer_builder.add_node("sub", inner_graph.__call__)

    # Run
    final_state = await outer_builder.run("sub")

    # Verify context flow: Initial -> Inner Process
    assert final_state.thought == "Initial Thought -> Inner Process"

```

- `tests/integration/test_orchestration.py`
```python
import pytest
import asyncio
from arkhon_rheo.agents.coordinator import CoordinatorAgent
from arkhon_rheo.agents.specialist import SpecialistAgent
from arkhon_rheo.runtime.scheduler import AgentScheduler
from arkhon_rheo.core.message import AgentMessage

# Mock User Agent to send request and receive response
from arkhon_rheo.core.agent import Agent


class UserAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.received_messages = []
        self.completion_event = asyncio.Event()

    async def process_message(self, message: AgentMessage):
        self.received_messages.append(message)
        if message.type == "response":
            self.completion_event.set()


@pytest.mark.asyncio
async def test_orchestration_flow():
    # Clear registry for test isolation
    from arkhon_rheo.core.registry import AgentRegistry

    AgentRegistry.clear()

    # Setup Agents (they auto-register)
    user = UserAgent("user")
    coordinator = CoordinatorAgent("coordinator")
    specialist = SpecialistAgent("coder", domain="coding")

    # Configure Routing
    coordinator.register_agent("write_code", specialist)

    # Setup Scheduler
    scheduler = AgentScheduler()
    scheduler.register_agent(user)
    scheduler.register_agent(coordinator)
    scheduler.register_agent(specialist)

    # Task
    task_msg = AgentMessage(
        sender="user",
        receiver="coordinator",
        content="implement hello world",
        type="request",
        metadata={"intent": "write_code"},
    )

    # Start Protocol
    await user.send_message(coordinator, task_msg)

    # Run Scheduler until User gets a response
    # We create a task that waits for user.completion_event
    await scheduler.run_until_complete(user.completion_event.wait())

    # Verify
    assert len(user.received_messages) == 1
    response = user.received_messages[0]
    # The response comes from coordinator (proxy) or specialist?
    # Coordinator forwards response, so sender should be coordinator or specialist depending on implementation?
    # In my fix: forwarded_msg = AgentMessage(sender=self.name...) -> sender is coordinator
    assert response.sender == "coordinator"
    assert "coding specialist" in response.content
    assert (
        response.metadata.get("reply_to") == "user"
    )  # Consumed by coordinator or not present on final response to user?
    # Actually Coordinator sends: sender=self.name, receiver=target.name.
    # When Specialist replies: receiver=message.sender (Coordinator).
    # Coordinator forwards: sender=self.name, receiver=target_agent (User).
    # So user sees sender="coordinator".

```

- `tests/integration/test_react_cycle.py`
```python
from arkhon_rheo.core.state import ReActState
from arkhon_rheo.core.graph import StateGraph
from arkhon_rheo.nodes.thought_node import ThoughtNode
from arkhon_rheo.nodes.action_node import ActionNode
from arkhon_rheo.nodes.observation_node import ObservationNode
from arkhon_rheo.nodes.validate_node import ValidateNode
from arkhon_rheo.nodes.commit_node import CommitNode


import pytest


@pytest.mark.asyncio
async def test_full_react_cycle():
    # 1. Initialize State and Graph
    initial_state = ReActState()
    graph = StateGraph(initial_state)

    # 2. Add Nodes
    graph.add_node("thought", ThoughtNode())
    graph.add_node("action", ActionNode())
    graph.add_node("observation", ObservationNode())
    graph.add_node("validate", ValidateNode())
    graph.add_node("commit", CommitNode())

    # 3. Add Edges (Linear cycle for this test)
    # Thought -> Action -> Observation -> Validate -> Commit
    graph.add_edge("thought", "action")
    graph.add_edge("action", "observation")
    graph.add_edge("observation", "validate")
    graph.add_edge("validate", "commit")
    # Commit is end node

    # 4. Run
    final_state = await graph.run("thought")

    # 5. Verify Final State
    assert final_state.thought == "I should check the system status."
    assert final_state.action == "check_status()"
    assert final_state.observation == "Status: OK"
    assert final_state.metadata.get("valid") is True
    assert final_state.metadata.get("committed") is True

```

- `tests/unit/agents/test_coordinator.py`
```python
import pytest
from unittest.mock import AsyncMock, patch
from arkhon_rheo.agents.coordinator import CoordinatorAgent
from arkhon_rheo.core.message import AgentMessage
from arkhon_rheo.core.agent import Agent


class MockAgent(Agent):
    async def process_message(self, message: AgentMessage):
        pass


@pytest.mark.asyncio
async def test_coordinator_routing():
    coordinator = CoordinatorAgent("coordinator")
    specialist = MockAgent("spec-1")

    coordinator.register_agent("intent_a", specialist)

    msg = AgentMessage(
        sender="user",
        receiver="coordinator",
        content="do task A",
        type="request",
        metadata={"intent": "intent_a"},
    )

    # Mock send_message to verify routing
    with patch.object(
        CoordinatorAgent, "send_message", new_callable=AsyncMock
    ) as mock_send:
        await coordinator.process_message(msg)

        # Should route to spec-1
        mock_send.assert_called_once()
        args, _ = mock_send.call_args
        recipient, forwarded_msg = args

        assert recipient.name == "spec-1"
        assert forwarded_msg.content == "do task A"
        assert forwarded_msg.sender == "coordinator"


@pytest.mark.asyncio
async def test_coordinator_no_route():
    coordinator = CoordinatorAgent("coordinator")
    msg = AgentMessage(
        sender="user",
        receiver="coordinator",
        content="unknown task",
        type="request",
        metadata={"intent": "unknown"},
    )

    with patch.object(
        CoordinatorAgent, "send_message", new_callable=AsyncMock
    ) as mock_send:
        await coordinator.process_message(msg)
        mock_send.assert_not_called()

```

- `tests/unit/agents/test_specialist.py`
```python
import pytest
from arkhon_rheo.agents.specialist import SpecialistAgent
from arkhon_rheo.core.message import AgentMessage


@pytest.mark.asyncio
async def test_specialist_processing():
    agent = SpecialistAgent("coder", domain="coding")
    msg = AgentMessage(
        sender="coordinator",
        receiver="coder",
        content="write python code",
        type="request",
    )

    # Track replies
    replies = []

    async def mock_send(recipient: "Agent", message: AgentMessage) -> None:
        replies.append(message)

    agent.send_message = mock_send  # type: ignore

    await agent.process_message(msg)

    assert len(replies) == 1
    reply = replies[0]
    assert reply.type == "response"
    assert "Processed by coding specialist" in str(reply.content)

```

- `tests/unit/core/memory/__init__.py`
```python

```

- `tests/unit/core/memory/test_context_window.py`
```python
import pytest
from arkhon_rheo.core.memory.context_window import ContextWindow


def test_context_window_sliding():
    # Arrange
    window = ContextWindow(max_tokens=10)

    # Act
    window.add_message("user", content="Hello", tokens=4)
    window.add_message("assistant", content="Hi", tokens=3)

    # Assert
    assert len(window.messages) == 2
    assert window.current_tokens == 7

    # This should trigger eviction (4 + 3 + 4 = 11 > 10)
    window.add_message("user", content="World", tokens=4)

    # After eviction, the first message ("Hello") should be removed
    assert len(window.messages) == 2
    assert window.messages[0]["content"] == "Hi"
    assert window.messages[1]["content"] == "World"
    assert window.current_tokens == 7

```

- `tests/unit/core/memory/test_summarization.py`
```python
import pytest
from unittest.mock import MagicMock
from arkhon_rheo.core.memory.context_window import ContextWindow
from arkhon_rheo.core.memory.summarization import Summarizer


def test_summarizer_trigger():
    # Arrange
    # Mock LLM client for summarization
    mock_llm = MagicMock()
    mock_llm.generate_content.return_value.text = "Summary of previous facts."

    summarizer = Summarizer(llm_client=mock_llm)
    window = ContextWindow(max_tokens=20)

    # Act
    window.add_message("user", content="Detail 1", tokens=8)
    window.add_message("assistant", content="Detail 2", tokens=8)

    # 16 tokens used. Adding 8 more triggers summarization if limit is 20
    # Actually, let's test the summarizer directly first
    summary = summarizer.summarize(window.messages)

    # Assert
    assert summary == "Summary of previous facts."
    mock_llm.generate_content.assert_called_once()

```

- `tests/unit/core/memory/test_vector_store.py`
```python
import pytest
import numpy as np
from arkhon_rheo.core.memory.vector_store import VectorStore


class MockVectorStore(VectorStore):
    def __init__(self):
        self.vectors = {}

    def upsert(self, id: str, vector: np.ndarray, metadata: dict):
        self.vectors[id] = (vector, metadata)

    def query(self, query_vector: np.ndarray, top_k: int = 5):
        # Very simple similarity (dot product for normalized vectors)
        results = []
        for id, (vec, meta) in self.vectors.items():
            score = float(np.dot(query_vector, vec))
            results.append({"id": id, "score": score, "metadata": meta})
        return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]

    def delete(self, id: str):
        if id in self.vectors:
            del self.vectors[id]


def test_vector_store_basic():
    # Arrange
    store = MockVectorStore()
    v1 = np.array([1.0, 0.0])
    v2 = np.array([0.0, 1.0])

    # Act
    store.upsert("1", v1, {"text": "A"})
    store.upsert("2", v2, {"text": "B"})

    # Query for something close to v1
    results = store.query(np.array([0.9, 0.1]))

    # Assert
    assert results[0]["id"] == "1"
    assert results[0]["metadata"]["text"] == "A"

```

- `tests/unit/core/runtime/test_checkpoint.py`
```python
import pytest
import os
from arkhon_rheo.core.runtime.checkpoint import CheckpointManager


def test_checkpoint_save_load(tmp_path):
    # Arrange
    db_path = str(tmp_path / "test_checkpoints.db")
    manager = CheckpointManager(db_path=db_path)
    state = {"step": 1, "data": "A"}

    # Act
    manager.save_checkpoint(step_id=1, state=state)
    loaded_state = manager.load_checkpoint(step_id=1)

    # Assert
    assert loaded_state == state
    assert manager.get_latest_step_id() == 1

```

- `tests/unit/core/test_agent.py`
```python
import pytest
import asyncio
from unittest.mock import AsyncMock
from arkhon_rheo.core.agent import Agent
from arkhon_rheo.core.message import AgentMessage


class MockAgent(Agent):
    async def process_message(self, message: AgentMessage):
        pass


@pytest.mark.asyncio
async def test_agent_initialization():
    agent = TestAgent(name="test-agent")
    assert agent.name == "test-agent"
    assert isinstance(agent.inbox, asyncio.Queue)


@pytest.mark.asyncio
async def test_agent_send_message():
    sender = TestAgent(name="sender")
    receiver = TestAgent(name="receiver")
    msg = AgentMessage(
        sender=sender.name, receiver=receiver.name, content="hello", type="request"
    )

    await sender.send_message(receiver, msg)

    # Check if receiver got the message
    received_msg = await receiver.inbox.get()
    assert received_msg == msg


@pytest.mark.asyncio
async def test_agent_receive_message():
    agent = TestAgent(name="agent")
    msg = AgentMessage(
        sender="sender", receiver="agent", content="hello", type="request"
    )

    await agent.inbox.put(msg)

    received_msg = await agent.receive_message()
    assert received_msg == msg

```

- `tests/unit/core/test_graph.py`
```python
from arkhon_rheo.core.state import ReActState
from arkhon_rheo.core.graph import StateGraph
import pytest


@pytest.mark.asyncio
async def test_graph_initialization():
    state = ReActState()
    graph = StateGraph(state)
    assert graph.current_state == state


@pytest.mark.asyncio
async def test_graph_execution_flow():
    initial_state = ReActState()
    graph = StateGraph(initial_state)

    def node_a(state: ReActState) -> ReActState:
        return state.with_thought("Thought from A")

    def node_b(state: ReActState) -> ReActState:
        return state.with_action("Action from B")

    graph.add_node("A", node_a)
    graph.add_node("B", node_b)
    graph.add_edge("A", "B")

    # Run step by step
    # Note: execute_step might return the next node ID or the new state?
    # Based on ReAct pattern, often we run until termination.
    # But for now let's assume granular control: execute_step(node_id) -> next_node_id
    next_node = await graph.execute_step("A")
    assert next_node == "B"
    assert graph.current_state.thought == "Thought from A"
    assert graph.current_state.action is None

    next_node = await graph.execute_step("B")
    assert next_node is None  # No edge from B
    assert graph.current_state.action == "Action from B"


@pytest.mark.asyncio
async def test_graph_run_loop():
    initial_state = ReActState()
    graph = StateGraph(initial_state)

    def node_a(state: ReActState) -> ReActState:
        count = state.metadata.get("count", 0)
        return state.with_metadata({"count": count + 1})

    graph.add_node("A", node_a)
    # Self loop for testing max steps
    graph.add_edge("A", "A")

    # This should run A 5 times and stop
    final_state = await graph.run("A", max_steps=5)
    assert final_state.metadata["count"] == 5

```

- `tests/unit/core/test_message.py`
```python
import uuid
from arkhon_rheo.core.message import AgentMessage


def test_agent_message_initialization():
    sender = "agent-a"
    receiver = "agent-b"
    content = "Hello"
    msg_type = "request"

    msg = AgentMessage(sender=sender, receiver=receiver, content=content, type=msg_type)

    assert isinstance(msg.id, str)
    assert len(msg.id) > 0  # Should be a UUID string
    assert msg.sender == sender
    assert msg.receiver == receiver
    assert msg.content == content
    assert msg.type == msg_type
    assert msg.metadata == {}
    assert msg.correlation_id is None


def test_agent_message_serialization():
    msg = AgentMessage(
        sender="a",
        receiver="b",
        content={"key": "value"},
        type="response",
        metadata={"timestamp": 123456789},
    )

    json_data = msg.to_json()
    assert isinstance(json_data, str)
    assert '"sender": "a"' in json_data
    assert (
        '"content": {"key": "value"}' in json_data
        or '"content": {"key": "value"}' in json_data.replace("'", '"')
    )


def test_agent_message_deserialization():
    original_msg = AgentMessage(
        sender="x", receiver="y", content="data", type="notification"
    )

    json_str = original_msg.to_json()
    restored_msg = AgentMessage.from_json(json_str)

    assert restored_msg.id == original_msg.id
    assert restored_msg.sender == original_msg.sender
    assert restored_msg.receiver == original_msg.receiver
    assert restored_msg.content == original_msg.content
    assert restored_msg.type == original_msg.type
    assert restored_msg.metadata == original_msg.metadata


def test_agent_message_with_correlation_id():
    corr_id = str(uuid.uuid4())
    msg = AgentMessage(
        sender="a",
        receiver="b",
        content="reply",
        type="response",
        correlation_id=corr_id,
    )

    assert msg.correlation_id == corr_id

    restored = AgentMessage.from_json(msg.to_json())
    assert restored.correlation_id == corr_id

```

- `tests/unit/core/test_shared_state.py`
```python
import pytest
import asyncio
from arkhon_rheo.core.shared_state import SharedAgentState


@pytest.mark.asyncio
async def test_shared_state_locking():
    shared_state = SharedAgentState()
    key = "counter"
    await shared_state.set(key, 0)

    async def increment():
        async with shared_state.lock(key):
            value = await shared_state.get(key)
            await asyncio.sleep(0.01)  # Simulate work
            await shared_state.set(key, value + 1)

    # Run 10 increments concurrently
    tasks = [increment() for _ in range(10)]
    await asyncio.gather(*tasks)

    final_value = await shared_state.get(key)
    assert final_value == 10


@pytest.mark.asyncio
async def test_shared_state_basic_ops():
    state = SharedAgentState()
    await state.set("a", 1)
    val = await state.get("a")
    assert val == 1

    await state.update("a", 2)
    val = await state.get("a")
    assert val == 2

```

- `tests/unit/core/test_subgraph.py`
```python
import pytest
import pytest
from arkhon_rheo.core.subgraph import SubGraph
from arkhon_rheo.core.graph import StateGraph
from arkhon_rheo.core.state import ReActState


@pytest.mark.asyncio
async def test_subgraph_execution():
    # Define a simple graph to be used as a subgraph
    state = ReActState()
    sub_builder = StateGraph(state)

    def sub_node(s: ReActState) -> ReActState:
        return s.with_thought("Inside SubGraph")

    sub_builder.add_node("sub_A", sub_node)
    sub_builder.add_edge(
        "sub_A", "sub_A"
    )  # Self loop to stop? No, we need a terminal condition or max steps
    # For this test, let's just run one step or set entry/exit

    # Actually, StateGraph.run() usually runs until termination or max steps.
    # Let's make "sub_A" just return the state and have no outgoing edges?
    # If no outgoing, it terminates?
    # Based on test_graph.py earlier:
    # "next_node = graph.execute_step("B") -> None # No edge from B"

    # So if we add node without edges, it terminates after execution.

    # Wrap it in SubGraph
    subgraph = SubGraph("my_subgraph", sub_builder, entry_point="sub_A")

    # Execute subgraph
    initial_state = ReActState()
    result_state = await subgraph(initial_state)

    assert result_state.thought == "Inside SubGraph"


@pytest.mark.asyncio
async def test_subgraph_context_isolation():
    # Verify that local vars in subgraph don't pollute unless returned
    # For ReActState, it's immutable-ish, so we return new state.
    # If SubGraph returns the new state, it modifies the flow.
    # But maybe we want some isolation?
    # Sprint 2.3 goal says: "test context propagation"

    state = ReActState(metadata={"parent": "value"})
    sub_builder = StateGraph(state)

    def sub_node(s: ReActState) -> ReActState:
        # Check parent context
        assert s.metadata["parent"] == "value"
        # Add local context
        return s.update_metadata({"child": "local"})

    sub_builder.add_node("start", sub_node)

    subgraph = SubGraph("isolation_test", sub_builder, entry_point="start")

    result = await subgraph(state)

    # If we want simple propagation, child should be there
    assert result.metadata["child"] == "local"
    assert result.metadata["parent"] == "value"

```


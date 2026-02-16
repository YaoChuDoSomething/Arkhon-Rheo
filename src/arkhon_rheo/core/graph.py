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

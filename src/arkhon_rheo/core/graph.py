from typing import Callable, Dict, Optional
from arkhon_rheo.core.state import ReActState


class StateGraph:
    """
    Manages the state transitions for the ReAct agent.
    """

    def __init__(self, initial_state: ReActState):
        self._state = initial_state
        self._nodes: Dict[str, Callable[[ReActState], ReActState]] = {}
        self._edges: Dict[str, str] = {}  # simple next step mapping

    @property
    def current_state(self) -> ReActState:
        return self._state

    def add_node(self, name: str, func: Callable[[ReActState], ReActState]) -> None:
        """Register a node function."""
        self._nodes[name] = func

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Register a transition."""
        self._edges[from_node] = to_node

    def execute_step(self, node_name: str) -> Optional[str]:
        """
        Execute a single step (node) and return the name of the next node.
        """
        if node_name not in self._nodes:
            raise ValueError(f"Node '{node_name}' not found in graph.")

        node_func = self._nodes[node_name]
        self._state = node_func(self._state)

        return self._edges.get(node_name)

    def run(self, start_node: str, max_steps: int = 10) -> ReActState:
        """Run the graph until end or max steps."""
        current_node: Optional[str] = start_node
        steps = 0
        while current_node and steps < max_steps:
            current_node = self.execute_step(current_node)
            steps += 1
        return self._state

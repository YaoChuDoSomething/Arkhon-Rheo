import time
import uuid
from typing import Any, Dict, Callable
from arkhon_rheo.core.state import ReActState, ReasoningStep
from arkhon_rheo.core.nodes.base import BaseNode


class ActionNode(BaseNode):
    """
    Node responsible for executing actions (tools) requested by the ThoughtNode.
    """

    def __init__(self, tools: Dict[str, Any]):
        """
        Initialize with a dictionary of tools.
        Tools can be callables or objects with a 'run' method.
        """
        self.tools = tools

    def execute(self, state: ReActState) -> ReActState:
        """
        Execute the action specified in state.action.
        """
        action_str = state.action
        if not action_str:
            # No action to perform
            return state

        # Parse action: "tool_name:input"
        # Very naive parsing for MVP
        if ":" in action_str:
            tool_name, tool_input = action_str.split(":", 1)
            tool_input = tool_input.strip()
        else:
            # Fallback or error
            tool_name = action_str
            tool_input = ""

        # Find tool
        tool = self.tools.get(tool_name)

        step_id = str(uuid.uuid4())

        if not tool:
            observation = f"Error: Tool '{tool_name}' not found"
        else:
            try:
                # Support both callable and .run() interface
                if hasattr(tool, "run"):
                    observation = tool.run(tool_input)
                elif callable(tool):
                    observation = tool(tool_input)
                else:
                    observation = f"Error: Tool '{tool_name}' is not executable"
            except Exception as e:
                observation = f"Error executing '{tool_name}': {str(e)}"

        # Create ReasoningStep for the action execution
        step = ReasoningStep(
            step_id=step_id,
            type="action",
            content=action_str,
            tool_name=tool_name,
            tool_input={"input": tool_input},
            tool_output=observation,
            timestamp=time.time(),
            metadata={"node": "ActionNode"},
        )

        # Update state: set observation, clear action?
        # ReAct usually clears action after execution to avoid loops if not updated by next thought.
        return state.with_observation(str(observation)).with_action(None).add_step(step)

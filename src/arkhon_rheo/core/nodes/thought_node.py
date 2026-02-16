from typing import Any, Optional
import time
import uuid
from arkhon_rheo.core.state import ReActState, ReasoningStep
from arkhon_rheo.core.nodes.base import BaseNode


class ThoughtNode(BaseNode):
    """
    Node responsible for generating thoughts using an LLM.
    """

    def __init__(self, llm: Any, system_prompt: Optional[str] = None):
        """
        Initialize with a LangChain-compatible runnable (LLM or Chain).
        """
        self.llm = llm
        self.system_prompt = system_prompt

    def execute(self, state: ReActState) -> ReActState:
        """
        Generate a thought based on the current state.
        """
        # Prepare input for LLM.
        # Ideally this would involve a prompt template that formats the state.
        # For this MVP step, we assume the LLM/Chain can handle the state dict
        # or we serialize it simply.

        # Simple string representation for now if LLM expects string
        input_str = f"Observation: {state.observation}\nGoal: {state.metadata.get('goal', 'Unknown')}"
        if self.system_prompt:
            input_str = f"System: {self.system_prompt}\n{input_str}"

        # Invoke LLM
        # We assume llm.invoke returns a string or a message with content
        response = self.llm.invoke(input_str)

        # Handle response types (Str or AIMessage)
        thought_content = response
        if hasattr(response, "content"):
            thought_content = response.content

        # Create ReasoningStep
        step = ReasoningStep(
            step_id=str(uuid.uuid4()),
            type="thought",
            content=str(thought_content),
            timestamp=time.time(),
            metadata={"node": "ThoughtNode"},
        )

        # Update state
        return state.with_thought(str(thought_content)).add_step(step)

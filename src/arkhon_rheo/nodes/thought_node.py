from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.base import BaseNode


class ThoughtNode(BaseNode):
    """
    Node responsible for generating thoughts using an LLM.
    """

    def execute(self, state: AgentState) -> AgentState:
        # 1. Construct Prompt (Stub)
        prompt = self._construct_prompt(state)

        # 2. Manage Context Window (Stub)

        # 3. Call LLM (Stub)
        thought_content = self._call_llm(prompt)

        # 4. Update State
        state["messages"].append({"role": "assistant", "content": thought_content})
        return state

    def _construct_prompt(self, state: AgentState) -> str:
        return f"State: {state}"

    def _call_llm(self, prompt: str) -> str:
        return "I should check the system status."

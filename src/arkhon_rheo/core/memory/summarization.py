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

from typing import Any, Dict, List


class Summarizer:
    """
    Handles context compression using an LLM.
    """

    def __init__(self, llm_client: Any):
        self.llm_client = llm_client

    async def summarize(self, messages: List[Dict[str, Any]]) -> str:
        """
        Summarize a list of messages into a single string (async).
        """
        if not messages:
            return ""

        lines = [
            "Summarize the following conversation history, preserving all key facts and entities:\n"
        ]
        for msg in messages:
            lines.append(f"{msg['role']}: {msg['content']}")

        prompt = "\n".join(lines)

        # Call LLM (using the unified google-genai pattern if possible)
        # Assuming the client supports async or we run it in a thread
        if hasattr(self.llm_client, "generate_content_async"):
            response = await self.llm_client.generate_content_async(prompt)
        else:
            # Fallback for sync clients
            response = self.llm_client.generate_content(prompt)
        return response.text

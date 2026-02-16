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

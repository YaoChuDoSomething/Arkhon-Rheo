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

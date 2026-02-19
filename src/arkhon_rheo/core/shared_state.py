"""Shared State Module.

This module provides a SharedAgentState class that enables thread-safe
and asynchronous sharing of state data between agents, including
support for atomic operations via key-level locking.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any


class SharedAgentState:
    """Thread-safe shared state for multiple agents.

    Provides mechanisms for concurrently accessing and modifying shared
    data, with support for specific key-based locking to ensure atomicity.

    Attributes:
        _state: Internal storage for shared state data.
        _lock: Global lock used to manage access to the registry of key locks.
        _locks: Mapping of specific keys to their respective asyncio Locks.
    """

    def __init__(self) -> None:
        """Initialize a SharedAgentState instance."""
        self._state: dict[str, Any] = {}
        self._lock = asyncio.Lock()
        self._locks: dict[str, asyncio.Lock] = {}

    async def get(self, key: str) -> Any:
        """Retrieve a value from the shared state.

        Args:
            key: The key of the value to retrieve.

        Returns:
            The value associated with the key, or None if it does not exist.
        """
        async with self._lock:
            return self._state.get(key)

    async def set(self, key: str, value: Any) -> None:
        """Set a value in the shared state.

        Args:
            key: The key under which to store the value.
            value: The data to be stored.
        """
        async with self._lock:
            self._state[key] = value

    async def update(self, key: str, value: Any) -> None:
        """Update a value in the shared state (identical to set).

        Args:
            key: The key to update.
            value: The new value to store.
        """
        await self.set(key, value)

    @asynccontextmanager
    async def lock(self, key: str):
        """Acquire an asynchronous lock for a specific key.

        This enables atomic operations on a specific piece of shared data.

        Args:
            key: The key for which to acquire the lock.

        Example:
            async with shared_state.lock("resource_id"):
                val = await shared_state.get("resource_id")
                await shared_state.set("resource_id", (val or 0) + 1)
        """
        # Global lock to safely get/create the specific key lock
        async with self._lock:
            if key not in self._locks:
                self._locks[key] = asyncio.Lock()
            key_lock = self._locks[key]

        # Acquire the specific key lock
        async with key_lock:
            yield

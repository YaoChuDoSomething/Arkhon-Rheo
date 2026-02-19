"""Checkpoint Manager Module.

This module provides the CheckpointManager class, which handles state
persistence for agentic graphs using a secure SQLite backend and JSON
serialization to prevent arbitrary code execution vulnerabilities.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any


class CheckpointManager:
    """High-security checkpoint manager using SQLite and JSON.

    Serializes agent state to JSON before storing it in a database, ensuring
    that state can be safely persisted and restored without the risks
    associated with pickle.

    Attributes:
        db_path: The filesystem path to the SQLite database file.
    """

    def __init__(self, db_path: str = "checkpoints.db") -> None:
        """Initialize a CheckpointManager instance.

        Args:
            db_path: The path to the SQLite database.
        """
        self.db_path = db_path
        self._setup_db()

    def _setup_db(self) -> None:
        """Initialize the SQLite database with the checkpoints table."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    thread_id TEXT PRIMARY KEY,
                    data TEXT,
                    timestamp TEXT
                )
            """)

    def save_checkpoint(self, state: dict[str, Any]) -> None:
        """Save the current agent state to the database.

        Uses JSON serialization to prevent arbitrary code execution risks.
        The state must contain a 'thread_id' to identify the conversation.

        Args:
            state: The AgentState dictionary to persist.
        """
        thread_id = state.get("thread_id", "default")
        # Use default=str to handle datetime or other non-serializable objects
        serialized = json.dumps(state, default=str)
        timestamp = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO checkpoints (thread_id, data, timestamp) VALUES (?, ?, ?)",
                (thread_id, serialized, timestamp),
            )

    def load_checkpoint(self, thread_id: str) -> dict[str, Any] | None:
        """Load the persisted state for a specific thread.

        Args:
            thread_id: The unique identifier for the conversation thread.

        Returns:
            The restored AgentState as a dictionary, or None if not found.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT data FROM checkpoints WHERE thread_id = ?", (thread_id,)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
        return None

    def list_threads(self) -> list[str]:
        """List all available conversation thread identifiers.

        Returns:
            A list of thread_id strings.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT thread_id FROM checkpoints")
            return [row[0] for row in cursor.fetchall()]

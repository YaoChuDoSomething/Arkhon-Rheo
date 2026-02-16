import sqlite3
import json
from typing import Any, Dict, Optional
from datetime import datetime


class CheckpointManager:
    """
    High-security checkpoint manager using JSON serialization and SQLite.
    Prevents arbitrary code execution by avoiding pickle.
    """

    def __init__(self, db_path: str = "checkpoints.db"):
        self.db_path = db_path
        self._setup_db()

    def _setup_db(self):
        """Initialize the SQLite database with a thread-safe checkpoints table."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    thread_id TEXT PRIMARY KEY,
                    data TEXT,
                    timestamp TEXT
                )
            """)

    def save_checkpoint(self, state: Dict[str, Any]):
        """
        Save state using JSON to prevent arbitrary code execution.
        Uses thread_id from state as the primary key.
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

    def load_checkpoint(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Load state for a specific thread_id."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT data FROM checkpoints WHERE thread_id = ?", (thread_id,)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
        return None

    def list_threads(self) -> list[str]:
        """List all available conversation threads."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT thread_id FROM checkpoints")
            return [row[0] for row in cursor.fetchall()]

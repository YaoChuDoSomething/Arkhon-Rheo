import sqlite3
import json
import pickle
from typing import Any, Dict, Optional


class CheckpointManager:
    """
    Manages state checkpoints using a SQLite backend.
    """

    def __init__(self, db_path: str = "checkpoints.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    step_id INTEGER PRIMARY KEY,
                    state BLOB,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_checkpoint(self, step_id: int, state: Dict[str, Any]) -> None:
        """Save the current state to the database."""
        state_bytes = pickle.dumps(state)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO checkpoints (step_id, state) VALUES (?, ?)",
                (step_id, state_bytes),
            )

    def load_checkpoint(self, step_id: int) -> Optional[Dict[str, Any]]:
        """Load a state checkpoint by its step ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT state FROM checkpoints WHERE step_id = ?", (step_id,)
            )
            row = cursor.fetchone()
            if row:
                return pickle.loads(row[0])
        return None

    def get_latest_step_id(self) -> Optional[int]:
        """Get the ID of the most recent checkpoint."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT MAX(step_id) FROM checkpoints")
            row = cursor.fetchone()
            return row[0] if row else None

    def rollback(self, step_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete all checkpoints after the specified step_id and return that state.
        """
        state = self.load_checkpoint(step_id)
        if state:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM checkpoints WHERE step_id > ?", (step_id,))
            return state
        return None

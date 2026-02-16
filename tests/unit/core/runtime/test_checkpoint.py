import pytest
import os
from arkhon_rheo.core.runtime.checkpoint import CheckpointManager


def test_checkpoint_save_load(tmp_path):
    # Arrange
    db_path = str(tmp_path / "test_checkpoints.db")
    manager = CheckpointManager(db_path=db_path)
    state = {"step": 1, "data": "A"}

    # Act
    manager.save_checkpoint(step_id=1, state=state)
    loaded_state = manager.load_checkpoint(step_id=1)

    # Assert
    assert loaded_state == state
    assert manager.get_latest_step_id() == 1

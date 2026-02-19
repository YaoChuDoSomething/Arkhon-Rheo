from arkhon_rheo.core.runtime.checkpoint import CheckpointManager


def test_checkpoint_save_load_json(tmp_path):
    db_path = str(tmp_path / "test_checkpoints.db")
    manager = CheckpointManager(db_path=db_path)

    state = {
        "thread_id": "thread_123",
        "messages": [{"role": "user", "content": "hello"}],
        "shared_context": {"key": "value"},
    }

    manager.save_checkpoint(state)
    loaded_state = manager.load_checkpoint("thread_123")

    assert loaded_state == state
    assert loaded_state["shared_context"]["key"] == "value"
    assert "thread_123" in manager.list_threads()


def test_checkpoint_overwrite(tmp_path):
    db_path = str(tmp_path / "test_checkpoints.db")
    manager = CheckpointManager(db_path=db_path)

    state_v1 = {"thread_id": "t1", "val": 1}
    state_v2 = {"thread_id": "t1", "val": 2}

    manager.save_checkpoint(state_v1)
    manager.save_checkpoint(state_v2)

    loaded = manager.load_checkpoint("t1")
    assert loaded["val"] == 2

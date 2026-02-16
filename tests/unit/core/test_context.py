import pytest
from arkhon_rheo.core.context import ContextManager
import threading


def test_context_set_get():
    """Verify basic set and get functionality."""
    ctx = ContextManager()
    ctx.set("trace_id", "12345")
    assert ctx.get("trace_id") == "12345"
    assert ctx.get("non_existent") is None


def test_context_thread_isolation():
    """Verify that context is isolated between threads."""
    ctx = ContextManager()
    ctx.set("user", "main_thread")

    def worker():
        # Should be empty in new thread
        assert ctx.get("user") is None
        ctx.set("user", "worker_thread")
        assert ctx.get("user") == "worker_thread"

    t = threading.Thread(target=worker)
    t.start()
    t.join()

    # Main thread should be unchanged
    assert ctx.get("user") == "main_thread"


def test_context_clear():
    """Verify clear functionality."""
    ctx = ContextManager()
    ctx.set("key", "value")
    ctx.clear()
    assert ctx.get("key") is None

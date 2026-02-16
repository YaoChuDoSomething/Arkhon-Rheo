from uuid import UUID
from arkhon_rheo.core.context import ContextManager


def test_context_initialization():
    ctx = ContextManager()
    assert ctx.trace_id is not None
    assert ctx.session_id is not None
    assert ctx.created_at is not None
    # Validate UUID format
    assert UUID(ctx.trace_id)
    assert UUID(ctx.session_id)


def test_metadata_operations():
    ctx = ContextManager()
    ctx.add_metadata("user", "test_user")
    ctx.add_metadata("role", "admin")

    assert ctx.get_metadata("user") == "test_user"
    assert ctx.get_metadata("role") == "admin"
    assert ctx.get_metadata("missing") is None
    assert ctx.get_metadata("missing", "default") == "default"


def test_get_all_metadata():
    ctx = ContextManager()
    ctx.add_metadata("key", "value")

    all_meta = ctx.get_all_metadata()
    assert all_meta["trace_id"] == ctx.trace_id
    assert all_meta["session_id"] == ctx.session_id
    assert "created_at" in all_meta
    assert all_meta["key"] == "value"


def test_new_trace():
    ctx = ContextManager()
    old_trace = ctx.trace_id
    new_trace = ctx.new_trace()

    assert old_trace != new_trace
    assert ctx.trace_id == new_trace
    assert UUID(new_trace)

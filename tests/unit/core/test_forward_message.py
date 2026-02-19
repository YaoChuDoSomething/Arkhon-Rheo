"""Unit tests for ForwardedMessage — Phase 3 architectural improvement."""

from __future__ import annotations

from arkhon_rheo.core.forward_message import ForwardedMessage


class TestForwardedMessage:
    def test_basic_construction(self):
        msg = ForwardedMessage(content="hello", source_agent="coder")
        assert msg.content == "hello"
        assert msg.source_agent == "coder"
        assert msg.direct_to_user is True
        assert msg.metadata == {}

    def test_str_returns_content(self):
        msg = ForwardedMessage(content="answer", source_agent="qa")
        assert str(msg) == "answer"

    def test_direct_to_user_can_be_disabled(self):
        msg = ForwardedMessage(content="log", source_agent="arch", direct_to_user=False)
        assert msg.direct_to_user is False

    def test_metadata_is_preserved(self):
        msg = ForwardedMessage(
            content="result",
            source_agent="pm",
            metadata={"model": "gemini-3-flash-preview", "tokens": "120"},
        )
        assert msg.metadata["model"] == "gemini-3-flash-preview"

    def test_independent_metadata_dicts(self):
        """Each instance must have its own metadata dict (no shared default)."""
        a = ForwardedMessage(content="a", source_agent="x")
        b = ForwardedMessage(content="b", source_agent="y")
        a.metadata["key"] = "val"
        assert "key" not in b.metadata

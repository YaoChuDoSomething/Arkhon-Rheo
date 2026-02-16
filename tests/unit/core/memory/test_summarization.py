import pytest
from unittest.mock import MagicMock
from arkhon_rheo.core.memory.context_window import ContextWindow
from arkhon_rheo.core.memory.summarization import Summarizer


def test_summarizer_trigger():
    # Arrange
    # Mock LLM client for summarization
    mock_llm = MagicMock()
    mock_llm.generate_content.return_value.text = "Summary of previous facts."

    summarizer = Summarizer(llm_client=mock_llm)
    window = ContextWindow(max_tokens=20)

    # Act
    window.add_message("user", content="Detail 1", tokens=8)
    window.add_message("assistant", content="Detail 2", tokens=8)

    # 16 tokens used. Adding 8 more triggers summarization if limit is 20
    # Actually, let's test the summarizer directly first
    summary = summarizer.summarize(window.messages)

    # Assert
    assert summary == "Summary of previous facts."
    mock_llm.generate_content.assert_called_once()

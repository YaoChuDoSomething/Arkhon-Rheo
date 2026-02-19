from unittest.mock import MagicMock

import pytest

from arkhon_rheo.core.state import AgentState
from arkhon_rheo.nodes.thought_node import ThoughtNode


@pytest.mark.asyncio
async def test_thought_node_execution():
    """Verify ThoughtNode calls LLM and updates messages in AgentState."""

    # Mock LLM chain/runnable
    mock_llm = MagicMock()
    # If ThoughtNode uses a Runnable sequence, we mock the invoke or astream
    mock_llm.invoke = MagicMock(
        return_value=MagicMock(content="I need to check the file size.")
    )

    node = ThoughtNode(llm=mock_llm)
    initial_state: AgentState = {
        "messages": [{"role": "user", "content": "Calculate 2+2"}],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test_thread",
    }

    new_state = await node(initial_state)

    # Verify LLM was called
    assert mock_llm.invoke.called

    # Verify state update (new message appended)
    assert len(new_state["messages"]) == 2
    assert "file size" in new_state["messages"][-1]["content"]


@pytest.mark.asyncio
async def test_thought_node_context_awareness():
    """Verify ThoughtNode utilizes previous messages context."""
    mock_llm = MagicMock()
    mock_llm.invoke = MagicMock(return_value=MagicMock(content="Thinking..."))

    node = ThoughtNode(llm=mock_llm)
    state: AgentState = {
        "messages": [{"role": "assistant", "content": "Previously I thought X"}],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test",
    }

    await node(state)
    assert mock_llm.invoke.called

from arkhon_rheo.core.state import AgentState


def test_agent_state_initialization():
    """Test standard initialization of AgentState."""
    state: AgentState = {
        "messages": [{"role": "user", "content": "Hello"}],
        "next_step": "thought",
        "shared_context": {"user_id": "123"},
        "is_completed": False,
        "errors": [],
        "thread_id": "thread_abc",
    }

    assert state["messages"][0]["content"] == "Hello"
    assert state["next_step"] == "thought"
    assert state["shared_context"] == {"user_id": "123"}
    assert not state["is_completed"]
    assert state["errors"] == []
    assert state["thread_id"] == "thread_abc"


def test_agent_state_message_accumulation():
    """Test how messages would accumulate in a list (as intended by operator.add in Graph)."""
    messages = [{"role": "user", "content": "Hello"}]
    new_messages = [{"role": "assistant", "content": "Hi there!"}]

    # In practice, RuntimeScheduler/Graph uses operator.add which concatenates lists
    accumulated = messages + new_messages

    assert len(accumulated) == 2
    assert accumulated[0]["role"] == "user"
    assert accumulated[1]["role"] == "assistant"


def test_agent_state_typed_dict_behavior():
    """Test that AgentState is a TypedDict (dictionary at runtime)."""
    state: AgentState = {
        "messages": [],
        "next_step": "end",
        "shared_context": {},
        "is_completed": True,
        "errors": [],
        "thread_id": "test_thread",
    }

    assert isinstance(state, dict)
    assert "messages" in state
    assert state["is_completed"] is True

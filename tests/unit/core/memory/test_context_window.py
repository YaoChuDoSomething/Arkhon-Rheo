from arkhon_rheo.core.memory.context_window import ContextWindow


def test_context_window_sliding():
    # Arrange
    window = ContextWindow(max_tokens=10)

    # Act
    window.add_message("user", content="Hello", tokens=4)
    window.add_message("assistant", content="Hi", tokens=3)

    # Assert
    assert len(window.messages) == 2
    assert window.current_tokens == 7

    # This should trigger eviction (4 + 3 + 4 = 11 > 10)
    window.add_message("user", content="World", tokens=4)

    # After eviction, the first message ("Hello") should be removed
    assert len(window.messages) == 2
    assert window.messages[0]["content"] == "Hi"
    assert window.messages[1]["content"] == "World"
    assert window.current_tokens == 7

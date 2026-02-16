import uuid
from arkhon_rheo.core.message import AgentMessage


def test_agent_message_initialization():
    sender = "agent-a"
    receiver = "agent-b"
    content = "Hello"
    msg_type = "request"

    msg = AgentMessage(sender=sender, receiver=receiver, content=content, type=msg_type)

    assert isinstance(msg.id, str)
    assert len(msg.id) > 0  # Should be a UUID string
    assert msg.sender == sender
    assert msg.receiver == receiver
    assert msg.content == content
    assert msg.type == msg_type
    assert msg.metadata == {}
    assert msg.correlation_id is None


def test_agent_message_serialization():
    msg = AgentMessage(
        sender="a",
        receiver="b",
        content={"key": "value"},
        type="response",
        metadata={"timestamp": 123456789},
    )

    json_data = msg.to_json()
    assert isinstance(json_data, str)
    assert '"sender": "a"' in json_data
    assert (
        '"content": {"key": "value"}' in json_data
        or '"content": {"key": "value"}' in json_data.replace("'", '"')
    )


def test_agent_message_deserialization():
    original_msg = AgentMessage(
        sender="x", receiver="y", content="data", type="notification"
    )

    json_str = original_msg.to_json()
    restored_msg = AgentMessage.from_json(json_str)

    assert restored_msg.id == original_msg.id
    assert restored_msg.sender == original_msg.sender
    assert restored_msg.receiver == original_msg.receiver
    assert restored_msg.content == original_msg.content
    assert restored_msg.type == original_msg.type
    assert restored_msg.metadata == original_msg.metadata


def test_agent_message_with_correlation_id():
    corr_id = str(uuid.uuid4())
    msg = AgentMessage(
        sender="a",
        receiver="b",
        content="reply",
        type="response",
        correlation_id=corr_id,
    )

    assert msg.correlation_id == corr_id

    restored = AgentMessage.from_json(msg.to_json())
    assert restored.correlation_id == corr_id

import pytest
from arkhon_rheo.core.state import AgentState
from arkhon_rheo.core.rules.engine import RuleEngine


def test_rule_engine_validation():
    """Verify RuleEngine correctly validates state using custom rules."""
    engine = RuleEngine()

    # Custom rule for testing
    def mock_rule(state: AgentState) -> bool:
        return "valid" in state["shared_context"]

    engine.add_rule(mock_rule)

    state_valid: AgentState = {
        "messages": [],
        "next_step": "",
        "shared_context": {"valid": True},
        "is_completed": False,
        "errors": [],
        "thread_id": "test",
    }
    assert engine.validate(state_valid)

    state_invalid: AgentState = {
        "messages": [],
        "next_step": "",
        "shared_context": {},
        "is_completed": False,
        "errors": [],
        "thread_id": "test",
    }
    assert not engine.validate(state_invalid)

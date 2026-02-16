from arkhon_rheo.core.state import ReActState
from arkhon_rheo.core.rules.rule_engine import RuleEngine
from arkhon_rheo.core.rules.builtin import (
    MaxDepthRule,
    ForbidGuessingRule,
    CostLimitRule,
)


def test_rule_engine():
    engine = RuleEngine()
    engine.add_rule(MaxDepthRule(max_steps=5))

    # Valid state
    state_valid = ReActState().with_metadata({"step_count": 3})
    assert len(engine.evaluate(state_valid)) == 0

    # Invalid state
    state_invalid = ReActState().with_metadata({"step_count": 6})
    violations = engine.evaluate(state_invalid)
    assert len(violations) == 1
    assert "MaxDepth" in violations[0]


def test_forbid_guessing():
    rule = ForbidGuessingRule()

    state_valid = ReActState(thought="The answer is 42.")
    assert rule.check(state_valid) is None

    state_invalid = ReActState(thought="I guess the answer is 42.")
    result = rule.check(state_invalid)
    assert result is not None
    assert "forbidden guess" in result


def test_cost_limit():
    rule = CostLimitRule(max_cost=0.5)

    state_valid = ReActState().with_metadata({"total_cost": 0.1})
    assert rule.check(state_valid) is None

    state_invalid = ReActState().with_metadata({"total_cost": 0.6})
    result = rule.check(state_invalid)
    assert result is not None
    assert "Total cost 0.6" in result

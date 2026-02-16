from typing import List, Optional
from arkhon_rheo.core.rules.base import BaseRule
from arkhon_rheo.core.state import ReActState


class RuleEngine:
    """
    Engine to evaluate a set of rules against a state.
    """

    def __init__(self, rules: Optional[List[BaseRule]] = None):
        self.rules = rules or []

    def add_rule(self, rule: BaseRule) -> None:
        """Register a rule."""
        self.rules.append(rule)

    def evaluate(self, state: ReActState) -> List[str]:
        """
        Evaluate all rules.
        Returns a list of violation messages.
        """
        violations = []
        for rule in self.rules:
            error = rule.check(state)
            if error:
                violations.append(f"Rule '{rule.name}' violated: {error}")
        return violations

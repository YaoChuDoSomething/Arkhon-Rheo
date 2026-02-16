from typing import List, Callable, Dict, Any, Optional
from arkhon_rheo.core.state import AgentState


class RuleEngine:
    """
    Engine to evaluate rules against an AgentState.
    Rules are simple callables returning a boolean (True = Pass, False = Fail).
    """

    def __init__(self, rules: Optional[List[Callable[[AgentState], bool]]] = None):
        self.rules = rules or []

    def add_rule(self, rule: Callable[[AgentState], bool]) -> None:
        """Register a new rule."""
        self.rules.append(rule)

    def validate(self, state: AgentState) -> bool:
        """
        Check if the state satisfies all registered rules.
        """
        for rule in self.rules:
            if not rule(state):
                return False
        return True

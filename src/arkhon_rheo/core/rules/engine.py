"""Rule Engine Module.

This module provides the RuleEngine class, which evaluates a set of rules
(callables) against an AgentState to determine if the state meets specific
criteria or governance requirements.
"""

from __future__ import annotations

from collections.abc import Callable

from arkhon_rheo.core.state import AgentState


class RuleEngine:
    """Engine to evaluate rules against an AgentState.

    Rules are simple callables that take an AgentState and return a
    boolean (True if the state passes, False otherwise).
    """

    def __init__(self, rules: list[Callable[[AgentState], bool]] | None = None) -> None:
        """Initialize a RuleEngine instance.

        Args:
            rules: An optional initial list of rule callables.
        """
        self.rules = rules or []

    def add_rule(self, rule: Callable[[AgentState], bool]) -> None:
        """Register a new rule in the engine.

        Args:
            rule: A callable that returns True/False based on the state.
        """
        self.rules.append(rule)

    def validate(self, state: AgentState) -> bool:
        """Check if the provided state satisfies all registered rules.

        Args:
            state: The AgentState instance to validate.

        Returns:
            True if all rules return True, otherwise False.
        """
        return all(rule(state) for rule in self.rules)

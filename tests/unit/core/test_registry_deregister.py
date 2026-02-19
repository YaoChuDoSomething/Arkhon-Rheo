"""Unit tests for AgentRegistry.deregister — Phase 3 architectural improvement."""

from __future__ import annotations

from unittest.mock import MagicMock

from arkhon_rheo.core.registry import AgentRegistry


def _make_mock_agent(name: str):
    """Return a simple mock that satisfies registry's type expectations."""
    agent = MagicMock()
    agent.name = name
    return agent


class TestAgentRegistryDeregister:
    def setup_method(self):
        AgentRegistry().clear()

    def test_deregister_removes_known_agent(self):
        registry = AgentRegistry()
        agent = _make_mock_agent("alpha")
        registry._agents["alpha"] = agent  # type: ignore[assignment]

        registry.deregister("alpha")
        assert registry.get("alpha") is None

    def test_deregister_unknown_agent_is_noop(self):
        """Deregistering a non-existent name must not raise."""
        AgentRegistry().deregister("does_not_exist")

    def test_deregister_does_not_affect_other_agents(self):
        registry = AgentRegistry()
        a = _make_mock_agent("a")
        b = _make_mock_agent("b")
        registry._agents["a"] = a  # type: ignore[assignment]
        registry._agents["b"] = b  # type: ignore[assignment]

        registry.deregister("a")
        assert registry.get("a") is None
        assert registry.get("b") is b

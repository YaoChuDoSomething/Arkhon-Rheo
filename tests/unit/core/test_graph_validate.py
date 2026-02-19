"""Unit tests for Graph.validate — Phase 3 architectural improvement."""

from __future__ import annotations

import pytest

from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.state import AgentState


def _noop(_state: AgentState) -> dict:
    return {}


class TestGraphValidate:
    def test_valid_graph_passes(self):
        g = Graph()
        g.add_node("a", _noop)
        g.add_node("b", _noop)
        g.add_edge("a", "b")
        g.validate()  # should not raise

    def test_end_sentinel_is_valid(self):
        g = Graph()
        g.add_node("a", _noop)
        g.add_edge("a", "END")
        g.validate()  # END is always valid

    def test_missing_edge_start_raises(self):
        g = Graph()
        g.add_node("b", _noop)
        g.add_edge("ghost", "b")  # 'ghost' not added
        with pytest.raises(ValueError, match="ghost"):
            g.validate()

    def test_missing_edge_end_raises(self):
        g = Graph()
        g.add_node("a", _noop)
        g.add_edge("a", "ghost")  # 'ghost' not added
        with pytest.raises(ValueError, match="ghost"):
            g.validate()

    def test_missing_conditional_source_raises(self):
        g = Graph()
        g.add_node("b", _noop)
        g.conditional_edges["ghost"] = {"map": {"yes": "b"}, "fn": lambda _s: "yes"}
        with pytest.raises(ValueError, match="ghost"):
            g.validate()

    def test_missing_conditional_target_raises(self):
        g = Graph()
        g.add_node("a", _noop)
        g.add_conditional_edge("a", {"yes": "ghost"}, lambda _s: "yes")
        with pytest.raises(ValueError, match="ghost"):
            g.validate()

    def test_empty_graph_passes(self):
        g = Graph()
        g.validate()  # no nodes, no edges → valid by definition

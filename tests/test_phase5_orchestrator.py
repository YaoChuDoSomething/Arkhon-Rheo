"""Phase 5 Unit Tests — Meta-Orchestrator."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from langgraph.graph.state import CompiledStateGraph

from arkhon_rheo.config.schema import WorkflowScheme
from arkhon_rheo.orchestrator.decision_nodes import evaluate_task_complexity
from arkhon_rheo.orchestrator.meta_graph import meta_orchestrator_graph
from arkhon_rheo.workflows.base import build_state


def _node_names(graph) -> set[str]:
    return set(graph.nodes.keys())


class TestMetaOrchestratorTopology:
    def test_meta_graph_has_expected_nodes(self) -> None:
        nodes = _node_names(meta_orchestrator_graph)
        assert "evaluate_complexity" in nodes
        assert "waterfall" in nodes
        assert "agile" in nodes
        assert "critic" in nodes

    def test_meta_graph_is_compiled(self) -> None:
        assert isinstance(meta_orchestrator_graph, CompiledStateGraph)


@pytest.mark.asyncio
async def test_evaluate_complexity_node() -> None:
    state = build_state("Add a simple logging statement")
    with patch("arkhon_rheo.orchestrator.decision_nodes._pm.invoke") as mock_invoke:
        mock_invoke.return_value = "SCHEME: waterfall\nReasoning: Simple task."
        result = await evaluate_task_complexity(state)

    assert result["shared_context"]["selected_scheme"] == WorkflowScheme.WATERFALL
    assert "evaluation_reasoning" in result["shared_context"]

    assert "selected_scheme" in result["shared_context"]
    assert result["shared_context"]["selected_scheme"] in [
        WorkflowScheme.WATERFALL,
        WorkflowScheme.AGILE,
        WorkflowScheme.CRITIC,
    ]

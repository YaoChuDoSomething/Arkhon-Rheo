"""Phase 2 Unit Tests — RACI Workflow Graph Topology.

These tests verify that all 9 compiled LangGraph graphs:
1. Import without errors
2. Have the expected set of nodes
3. The ``build_state()`` helper produces a validly structured initial state

No LLM calls are made — only graph structure is inspected.
"""

from __future__ import annotations

from arkhon_rheo.workflows import (
    build_state,
    flow_1_1,
    flow_1_2,
    flow_1_3,
    flow_2_1,
    flow_2_2,
    flow_2_3,
    flow_3_1,
    flow_3_2,
    flow_3_3,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _node_names(graph) -> set[str]:
    """Extract node names from a compiled LangGraph graph."""
    # CompiledStateGraph exposes `.nodes` directly as a dict keyed by node name
    return set(graph.nodes.keys())


# ---------------------------------------------------------------------------
# build_state
# ---------------------------------------------------------------------------


class TestBuildState:
    def test_basic_structure(self) -> None:
        state = build_state("add login feature")
        assert state["messages"][0]["role"] == "human"
        assert "add login feature" in state["messages"][0]["content"]
        assert state["is_completed"] is False
        assert state["errors"] == []
        assert "user_request" in state["shared_context"]

    def test_thread_id(self) -> None:
        state = build_state("foo", thread_id="my-session")
        assert state["thread_id"] == "my-session"

    def test_extra_context(self) -> None:
        state = build_state("foo", extra_context={"prd_result": "my PRD"})
        assert state["shared_context"]["prd_result"] == "my PRD"


# ---------------------------------------------------------------------------
# Scheme 1 Waterfall — topology
# ---------------------------------------------------------------------------


class TestScheme1Waterfall:
    def test_flow_1_1_has_expected_nodes(self) -> None:
        nodes = _node_names(flow_1_1)
        assert "pm_write_prd" in nodes
        assert "arch_receive_prd" in nodes
        assert "coder_receive_prd" in nodes
        assert "qa_receive_prd" in nodes

    def test_flow_1_2_has_expected_nodes(self) -> None:
        nodes = _node_names(flow_1_2)
        assert "arch_write_spec" in nodes
        assert "coder_receive_spec" in nodes

    def test_flow_1_3_has_expected_nodes(self) -> None:
        nodes = _node_names(flow_1_3)
        assert "coder_implement" in nodes
        assert "qa_acceptance" in nodes

    def test_flow_1_1_is_compiled(self) -> None:
        from langgraph.graph.state import CompiledStateGraph

        assert isinstance(flow_1_1, CompiledStateGraph)

    def test_flow_1_2_is_compiled(self) -> None:
        from langgraph.graph.state import CompiledStateGraph

        assert isinstance(flow_1_2, CompiledStateGraph)

    def test_flow_1_3_is_compiled(self) -> None:
        from langgraph.graph.state import CompiledStateGraph

        assert isinstance(flow_1_3, CompiledStateGraph)


# ---------------------------------------------------------------------------
# Scheme 2 Agile — topology
# ---------------------------------------------------------------------------


class TestScheme2Agile:
    def test_flow_2_1_has_expected_nodes(self) -> None:
        nodes = _node_names(flow_2_1)
        assert "pm_draft_requirements" in nodes
        assert "arch_consult_feasibility" in nodes
        assert "qa_consult_testability" in nodes
        assert "pm_finalise_requirements" in nodes

    def test_flow_2_2_has_tdd_loop_nodes(self) -> None:
        nodes = _node_names(flow_2_2)
        assert "qa_write_tests" in nodes
        assert "coder_implement" in nodes
        assert "qa_evaluate" in nodes
        assert "increment_retry" in nodes  # safety ceiling node

    def test_flow_2_3_has_sign_off_nodes(self) -> None:
        nodes = _node_names(flow_2_3)
        assert "qa_demo_summary" in nodes
        assert "pm_sign_off" in nodes
        assert "coder_revise" in nodes

    def test_flow_2_1_is_compiled(self) -> None:
        from langgraph.graph.state import CompiledStateGraph

        assert isinstance(flow_2_1, CompiledStateGraph)

    def test_flow_2_2_is_compiled(self) -> None:
        from langgraph.graph.state import CompiledStateGraph

        assert isinstance(flow_2_2, CompiledStateGraph)

    def test_flow_2_3_is_compiled(self) -> None:
        from langgraph.graph.state import CompiledStateGraph

        assert isinstance(flow_2_3, CompiledStateGraph)


# ---------------------------------------------------------------------------
# Scheme 3 Critic — topology
# ---------------------------------------------------------------------------


class TestScheme3Critic:
    def test_flow_3_1_has_lockdown_nodes(self) -> None:
        nodes = _node_names(flow_3_1)
        assert "pm_propose_requirements" in nodes
        assert "arch_define_constraints" in nodes
        assert "pm_counter_sign" in nodes

    def test_flow_3_2_has_tribunal_nodes(self) -> None:
        nodes = _node_names(flow_3_2)
        assert "coder_submit_pr" in nodes
        assert "qa_prosecution" in nodes
        assert "coder_defense" in nodes
        assert "arch_verdict" in nodes

    def test_flow_3_3_has_refactor_loop_nodes(self) -> None:
        nodes = _node_names(flow_3_3)
        assert "arch_refactor_order" in nodes
        assert "coder_refactor" in nodes
        assert "arch_re_review" in nodes
        assert "qa_informed" in nodes
        assert "increment_retry" in nodes

    def test_flow_3_1_is_compiled(self) -> None:
        from langgraph.graph.state import CompiledStateGraph

        assert isinstance(flow_3_1, CompiledStateGraph)

    def test_flow_3_2_is_compiled(self) -> None:
        from langgraph.graph.state import CompiledStateGraph

        assert isinstance(flow_3_2, CompiledStateGraph)

    def test_flow_3_3_is_compiled(self) -> None:
        from langgraph.graph.state import CompiledStateGraph

        assert isinstance(flow_3_3, CompiledStateGraph)


# ---------------------------------------------------------------------------
# verdict_router
# ---------------------------------------------------------------------------


class TestVerdictRouter:
    def test_approved_verdict_routes_approved(self) -> None:
        from arkhon_rheo.workflows.base import build_state, verdict_router

        router = verdict_router(approved_key="ok", rejected_key="retry")
        state = build_state("x")
        state["shared_context"]["verdict"] = "approved"
        assert router(state) == "ok"

    def test_rejected_verdict_routes_retry(self) -> None:
        from arkhon_rheo.workflows.base import build_state, verdict_router

        router = verdict_router(approved_key="ok", rejected_key="retry")
        state = build_state("x")
        state["shared_context"]["verdict"] = "bad"
        assert router(state) == "retry"

    def test_merge_counts_as_approved(self) -> None:
        from arkhon_rheo.workflows.base import build_state, verdict_router

        router = verdict_router(approved_key="merge", rejected_key="reject")
        state = build_state("x")
        state["shared_context"]["verdict"] = "merge"
        assert router(state) == "merge"

"""Meta-Orchestrator Graph Definition."""

from __future__ import annotations

from typing import Any, cast

from langgraph.graph import END, START, StateGraph

from arkhon_rheo.config.schema import WorkflowScheme
from arkhon_rheo.core.state import RACIState
from arkhon_rheo.orchestrator.decision_nodes import evaluate_task_complexity, scheme_router
from arkhon_rheo.workflows import (
    flow_1_1,
    flow_2_1,
    flow_3_1,
)


def _build_meta_graph() -> StateGraph:
    sg = StateGraph(cast(Any, RACIState))

    # Task evaluation node
    sg.add_node("evaluate_complexity", evaluate_task_complexity)

    # Scheme entry points (subgraphs)
    # Note: In a full implementation, we might chain multiple flows 1-1 -> 1-2 -> 1-3.
    # For the Meta-Orchestrator, we start with the first flow of each scheme.
    sg.add_node("waterfall", flow_1_1)
    sg.add_node("agile", flow_2_1)
    sg.add_node("critic", flow_3_1)

    sg.add_edge(START, "evaluate_complexity")

    sg.add_conditional_edges(
        "evaluate_complexity",
        scheme_router,
        {
            str(WorkflowScheme.WATERFALL): "waterfall",
            str(WorkflowScheme.AGILE): "agile",
            str(WorkflowScheme.CRITIC): "critic",
        },
    )

    sg.add_edge("waterfall", END)
    sg.add_edge("agile", END)
    sg.add_edge("critic", END)

    return sg


meta_orchestrator_graph = _build_meta_graph().compile()

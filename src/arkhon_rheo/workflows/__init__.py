"""Arkhon-Rheo RACI Workflow Schemes.

Exports all 9 compiled LangGraph workflow graphs, grouped by scheme.

Scheme 1 — Hierarchical Waterfall:
    :data:`flow_1_1` Requirement Handover
    :data:`flow_1_2` Design-to-Code Handover
    :data:`flow_1_3` Code Delivery

Scheme 2 — Collaborative Agile:
    :data:`flow_2_1` Joint Requirement Analysis
    :data:`flow_2_2` Dev-Test Loop (TDD)
    :data:`flow_2_3` Agile Sign-off

Scheme 3 — Critic / Supervisor:
    :data:`flow_3_1` Spec Lockdown
    :data:`flow_3_2` Review Tribunal
    :data:`flow_3_3` Refactoring Loop
"""

from arkhon_rheo.workflows.base import build_state, make_role_node, verdict_router
from arkhon_rheo.workflows.scheme1_waterfall import flow_1_1, flow_1_2, flow_1_3
from arkhon_rheo.workflows.scheme2_agile import flow_2_1, flow_2_2, flow_2_3
from arkhon_rheo.workflows.scheme3_critic import flow_3_1, flow_3_2, flow_3_3

__all__ = [
    "build_state",
    "flow_1_1",
    "flow_1_2",
    "flow_1_3",
    "flow_2_1",
    "flow_2_2",
    "flow_2_3",
    "flow_3_1",
    "flow_3_2",
    "flow_3_3",
    "make_role_node",
    "verdict_router",
]

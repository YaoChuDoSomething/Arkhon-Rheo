"""Scheme 1 — Hierarchical Waterfall Workflows.

Implements three sub-flows representing the classic waterfall RACI scheme:

- **1-1 Requirement Handover** (`flow_1_1`):
  PM broadcasts PRD → Arch, Coder, QA all receive (Informed).

- **1-2 Design-to-Code Handover** (`flow_1_2`):
  Architect translates PRD → Tech Spec → Coder receives (Handover).

- **1-3 Code Delivery** (`flow_1_3`):
  Coder implements → hands off deliverable → QA validates acceptance.

All three are standalone :class:`CompiledGraph` objects that can be invoked
individually or chained by the Meta-Orchestrator.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from arkhon_rheo.core.state import RACIState
from arkhon_rheo.roles.concrete import (
    ProductManager,
    QualityAssurance,
    SoftwareEngineer,
    SystemArchitect,
)
from arkhon_rheo.workflows.base import build_state, make_role_node

# ---------------------------------------------------------------------------
# Shared role instances (stateless — invoke() calls are independent)
# ---------------------------------------------------------------------------
_pm = ProductManager()
_arch = SystemArchitect()
_coder = SoftwareEngineer()
_qa = QualityAssurance()


# ---------------------------------------------------------------------------
# 1-1: Requirement Handover (Broadcast mode)
# ---------------------------------------------------------------------------
# RACI: PM (R/A) → Arch (I), Coder (I), QA (I)
# Flow: PM writes PRD → broadcast nodes notify each stakeholder
# ---------------------------------------------------------------------------


def _build_flow_1_1() -> StateGraph:
    sg = StateGraph(RACIState)

    # PM creates PRD — the single Responsible + Accountable agent
    sg.add_node("pm_write_prd", make_role_node(_pm, task_key="prd"))

    # "Broadcast" nodes: each stakeholder receives and logs the PRD
    # In a real system this would dispatch async notifications; here each
    # role does a lightweight "acknowledge receipt" inference.
    sg.add_node(
        "arch_receive_prd",
        make_role_node(
            _arch,
            task_key="prd_ack_arch",
            extract_prompt=(
                "Acknowledge receipt of the following PRD and confirm you have no blocking questions at this stage."
            ),
        ),
    )
    sg.add_node(
        "coder_receive_prd",
        make_role_node(
            _coder,
            task_key="prd_ack_coder",
            extract_prompt="Acknowledge receipt of the following PRD. Note any immediate concerns.",
        ),
    )
    sg.add_node(
        "qa_receive_prd",
        make_role_node(
            _qa,
            task_key="prd_ack_qa",
            extract_prompt=(
                "Acknowledge receipt of the following PRD. List measurable acceptance criteria you will use."
            ),
        ),
    )

    sg.add_edge(START, "pm_write_prd")
    sg.add_edge("pm_write_prd", "arch_receive_prd")
    sg.add_edge("pm_write_prd", "coder_receive_prd")
    sg.add_edge("pm_write_prd", "qa_receive_prd")
    sg.add_edge("arch_receive_prd", END)
    sg.add_edge("coder_receive_prd", END)
    sg.add_edge("qa_receive_prd", END)

    return sg


# ---------------------------------------------------------------------------
# 1-2: Design-to-Code Handover
# ---------------------------------------------------------------------------
# RACI: Arch (R/A) receives PRD → produces Tech Spec → Coder (I)
# ---------------------------------------------------------------------------


def _build_flow_1_2() -> StateGraph:
    sg = StateGraph(RACIState)

    sg.add_node(
        "arch_write_spec",
        make_role_node(
            _arch,
            task_key="tech_spec",
            extract_prompt=(
                "Using the PRD in shared_context['prd_result'], produce a detailed "
                "Tech Spec covering: system design, module breakdown, API contracts, "
                "data models, and architectural constraints the Coder MUST follow."
            ),
        ),
    )
    sg.add_node(
        "coder_receive_spec",
        make_role_node(
            _coder,
            task_key="spec_ack",
            extract_prompt=(
                "Review the Tech Spec in shared_context['tech_spec_result']. "
                "Confirm you understand the constraints. Flag any ambiguities before starting."
            ),
        ),
    )

    sg.add_edge(START, "arch_write_spec")
    sg.add_edge("arch_write_spec", "coder_receive_spec")
    sg.add_edge("coder_receive_spec", END)

    return sg


# ---------------------------------------------------------------------------
# 1-3: Code Delivery
# ---------------------------------------------------------------------------
# RACI: Coder (R) implements → Handover to QA (R/A for acceptance)
# ---------------------------------------------------------------------------


def _build_flow_1_3() -> StateGraph:
    sg = StateGraph(RACIState)

    sg.add_node(
        "coder_implement",
        make_role_node(
            _coder,
            task_key="implementation",
            extract_prompt=(
                "Implement the feature described in the Tech Spec "
                "(shared_context['tech_spec_result']). Write clean, tested code. "
                "Output the files to create/modify and their content."
            ),
        ),
    )
    sg.add_node(
        "qa_acceptance",
        make_role_node(
            _qa,
            task_key="acceptance_report",
            extract_prompt=(
                "Review the implementation (shared_context['implementation_result']). "
                "Write an acceptance report: list each acceptance criterion and whether "
                "it PASSES or FAILS. Set shared_context['verdict'] = 'approved' if all "
                "pass, else 'rejected'."
            ),
        ),
    )

    sg.add_edge(START, "coder_implement")
    sg.add_edge("coder_implement", "qa_acceptance")
    sg.add_edge("qa_acceptance", END)

    return sg


# ---------------------------------------------------------------------------
# Public compiled graphs
# ---------------------------------------------------------------------------

flow_1_1 = _build_flow_1_1().compile()
flow_1_2 = _build_flow_1_2().compile()
flow_1_3 = _build_flow_1_3().compile()

__all__ = ["flow_1_1", "flow_1_2", "flow_1_3", "build_state"]

"""Scheme 2 — Collaborative Agile Workflows.

Implements three sub-flows for the iterative, feedback-rich Agile scheme:

- **2-1 Joint Requirement Analysis** (`flow_2_1`):
  PM drafts requirements → Arch + QA consult and validate → PM finalises.

- **2-2 Dev-Test Loop (TDD)** (`flow_2_2`):
  QA writes test cases → Coder implements → automated check →
  retry loop until tests pass (max ``MAX_TDD_RETRIES`` iterations).

- **2-3 Agile Sign-off** (`flow_2_3`):
  QA demos to PM → PM decides accept / request revision → loop back to Coder.
"""

from __future__ import annotations

from typing import Any, cast

from langgraph.graph import END, START, StateGraph

from arkhon_rheo.core.state import RACIState
from arkhon_rheo.roles.concrete import (
    ProductManager,
    QualityAssurance,
    SoftwareEngineer,
    SystemArchitect,
)
from arkhon_rheo.workflows.base import make_role_node, verdict_router

MAX_TDD_RETRIES: int = 3
"""Maximum Coder-rework iterations in the TDD loop (safety ceiling)."""

# ---------------------------------------------------------------------------
# Shared role instances
# ---------------------------------------------------------------------------
_pm = ProductManager()
_arch = SystemArchitect()
_coder = SoftwareEngineer()
_qa = QualityAssurance()


# ---------------------------------------------------------------------------
# 2-1: Joint Requirement Analysis
# ---------------------------------------------------------------------------
# RACI:
#   PM (A/R) — drafts requirement
#   Arch (C) — validates technical feasibility
#   QA  (C)  — validates testability
#   PM  (R)  — finalises based on feedback
# ---------------------------------------------------------------------------


def _build_flow_2_1() -> StateGraph:
    sg = StateGraph(cast(Any, RACIState))

    sg.add_node(
        "pm_draft_requirements",
        make_role_node(
            _pm,
            task_key="req_draft",
            extract_prompt=(
                "Draft initial requirements for the user's request. "
                "Produce a PRD draft: goals, scope, acceptance criteria. "
                "Explicitly note areas where technical feasibility is uncertain."
            ),
        ),
    )
    sg.add_node(
        "arch_consult_feasibility",
        make_role_node(
            _arch,
            task_key="feasibility_review",
            extract_prompt=(
                "Review the PRD draft (shared_context['req_draft_result']). "
                "Assess technical feasibility. Flag any infeasible items and "
                "propose alternatives. Mark feasible items as APPROVED."
            ),
        ),
    )
    sg.add_node(
        "qa_consult_testability",
        make_role_node(
            _qa,
            task_key="testability_review",
            extract_prompt=(
                "Review the PRD draft (shared_context['req_draft_result']). "
                "Assess testability: are acceptance criteria measurable? "
                "List missing test hooks or definition-of-done gaps."
            ),
        ),
    )
    sg.add_node(
        "pm_finalise_requirements",
        make_role_node(
            _pm,
            task_key="req_final",
            extract_prompt=(
                "Incorporate the feasibility review (shared_context['feasibility_review_result']) "
                "and testability review (shared_context['testability_review_result']) into a "
                "FINAL requirements document. Resolve all flagged issues. "
                "This document is now the locked specification."
            ),
        ),
    )

    sg.add_edge(START, "pm_draft_requirements")
    # Parallel consultation
    sg.add_edge("pm_draft_requirements", "arch_consult_feasibility")
    sg.add_edge("pm_draft_requirements", "qa_consult_testability")
    # Both consultants lead into finalisation
    sg.add_edge("arch_consult_feasibility", "pm_finalise_requirements")
    sg.add_edge("qa_consult_testability", "pm_finalise_requirements")
    sg.add_edge("pm_finalise_requirements", END)

    return sg


# ---------------------------------------------------------------------------
# 2-2: Dev-Test Loop (TDD)
# ---------------------------------------------------------------------------
# RACI:
#   QA  (R) — writes test cases first
#   Coder(R) — implements against tests
#   QA  (R) — evaluates pass/fail → verdict
#   Coder(R) — reworks if verdict = rejected (max MAX_TDD_RETRIES)
# ---------------------------------------------------------------------------


def _increment_retry(state: RACIState) -> dict[str, Any]:
    """Increment the TDD retry counter in shared_context."""
    ctx = dict(state.get("shared_context", {}))
    ctx["tdd_retries"] = ctx.get("tdd_retries", 0) + 1
    return {"shared_context": ctx}


def _retry_limit_router(state: RACIState) -> str:
    """Route to END if max retries exceeded, otherwise back to coder."""
    retries = state.get("shared_context", {}).get("tdd_retries", 0)
    return "end_exceeded" if retries >= MAX_TDD_RETRIES else "coder_implement"


def _build_flow_2_2() -> StateGraph:
    sg = StateGraph(cast(Any, RACIState))

    sg.add_node(
        "qa_write_tests",
        make_role_node(
            _qa,
            task_key="test_cases",
            extract_prompt=(
                "Based on the finalised requirements (shared_context['req_final_result']), "
                "write concrete test cases. Format as pytest functions. "
                "Each test MUST target a single acceptance criterion."
            ),
        ),
    )
    sg.add_node(
        "coder_implement",
        make_role_node(
            _coder,
            task_key="implementation",
            extract_prompt=(
                "Implement the feature to pass the test cases in "
                "shared_context['test_cases_result']. "
                "Write production-quality Python code."
            ),
        ),
    )
    sg.add_node(
        "qa_evaluate",
        make_role_node(
            _qa,
            task_key="tdd_evaluation",
            extract_prompt=(
                "Evaluate the implementation (shared_context['implementation_result']) "
                "against the test cases (shared_context['test_cases_result']). "
                "For each test, state PASS or FAIL with reason. "
                "Set shared_context['verdict'] = 'approved' if ALL pass, else 'rejected'."
            ),
        ),
    )
    sg.add_node("increment_retry", _increment_retry)

    _verdict = verdict_router(approved_key="end_approved", rejected_key="check_retries")
    _retries = _retry_limit_router

    sg.add_edge(START, "qa_write_tests")
    sg.add_edge("qa_write_tests", "coder_implement")
    sg.add_edge("coder_implement", "qa_evaluate")
    sg.add_conditional_edges(
        "qa_evaluate",
        _verdict,
        {
            "end_approved": END,
            "check_retries": "increment_retry",
        },
    )
    sg.add_conditional_edges(
        "increment_retry",
        _retries,
        {
            "coder_implement": "coder_implement",
            "end_exceeded": END,
        },
    )

    return sg


# ---------------------------------------------------------------------------
# 2-3: Agile Sign-off
# ---------------------------------------------------------------------------
# RACI:
#   QA  (R)  — prepares demo summary
#   PM  (A)  — evaluates and gives thumbs up/down
#   Coder(R) — reworks if PM rejects
# ---------------------------------------------------------------------------


def _build_flow_2_3() -> StateGraph:
    sg = StateGraph(cast(Any, RACIState))

    sg.add_node(
        "qa_demo_summary",
        make_role_node(
            _qa,
            task_key="demo_summary",
            extract_prompt=(
                "Prepare a demo summary for the PM. "
                "List implemented features, any edge cases / known limitations, "
                "and the test run results from shared_context['tdd_evaluation_result']."
            ),
        ),
    )
    sg.add_node(
        "pm_sign_off",
        make_role_node(
            _pm,
            task_key="sign_off",
            extract_prompt=(
                "Review the demo summary (shared_context['demo_summary_result']). "
                "Does it satisfy the business requirements? "
                "Set shared_context['verdict'] = 'approved' if yes, 'rejected' if revision needed. "
                "Provide specific feedback if rejecting."
            ),
        ),
    )
    sg.add_node(
        "coder_revise",
        make_role_node(
            _coder,
            task_key="revision",
            extract_prompt=(
                "The PM has requested revisions. "
                "Review PM feedback (shared_context['sign_off_result']) "
                "and update the implementation accordingly."
            ),
        ),
    )

    _verdict = verdict_router(approved_key="approved", rejected_key="rejected")

    sg.add_edge(START, "qa_demo_summary")
    sg.add_edge("qa_demo_summary", "pm_sign_off")
    sg.add_conditional_edges(
        "pm_sign_off",
        _verdict,
        {
            "approved": END,
            "rejected": "coder_revise",
        },
    )
    sg.add_edge("coder_revise", "qa_demo_summary")  # loop back for re-demo

    return sg


# ---------------------------------------------------------------------------
# Public compiled graphs
# ---------------------------------------------------------------------------

flow_2_1 = _build_flow_2_1().compile()
flow_2_2 = _build_flow_2_2().compile()
flow_2_3 = _build_flow_2_3().compile()

__all__ = ["flow_2_1", "flow_2_2", "flow_2_3"]

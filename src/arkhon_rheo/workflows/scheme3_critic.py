"""Scheme 3 — Critic / Supervisor Workflows.

Implements three sub-flows for the rigorous Critic/Supervisor scheme:

- **3-1 Spec Lockdown** (`flow_3_1`):
  PM proposes requirements → Architect defines hard constraints (red lines) →
  PM counter-signs the locked specification.

- **3-2 Review Tribunal** (`flow_3_2`):
  Coder submits PR → QA (prosecutor) finds violations →
  Architect (judge) issues Merge / Reject verdict.

- **3-3 Refactoring Loop** (`flow_3_3`):
  Architect (A) forces refactoring when a Reject is issued. Coder must
  comply and resubmit. Loop continues until Architect approves
  (max ``MAX_REFACTOR_RETRIES`` iterations).
"""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from arkhon_rheo.core.state import RACIState
from arkhon_rheo.roles.concrete import (
    ProductManager,
    QualityAssurance,
    SoftwareEngineer,
    SystemArchitect,
)
from arkhon_rheo.workflows.base import make_role_node, verdict_router

MAX_REFACTOR_RETRIES: int = 3
"""Maximum forced-refactor iterations the Coder must undergo before escalation."""

# ---------------------------------------------------------------------------
# Shared role instances
# ---------------------------------------------------------------------------
_pm = ProductManager()
_arch = SystemArchitect()
_coder = SoftwareEngineer()
_qa = QualityAssurance()


# ---------------------------------------------------------------------------
# 3-1: Spec Lockdown
# ---------------------------------------------------------------------------
# RACI:
#   PM   (R)   — proposes requirements
#   Arch (A/R) — defines non-negotiable technical constraints
#   PM   (A)   — signs off on locked spec (counter-sign)
# ---------------------------------------------------------------------------


def _build_flow_3_1() -> StateGraph:
    sg = StateGraph(RACIState)

    sg.add_node(
        "pm_propose_requirements",
        make_role_node(
            _pm,
            task_key="proposal",
            extract_prompt=(
                "Propose the high-level requirements for the feature. "
                "Include business goals, desired behaviours, and any known constraints. "
                "This is a draft — the Architect will define the hard technical boundaries."
            ),
        ),
    )
    sg.add_node(
        "arch_define_constraints",
        make_role_node(
            _arch,
            task_key="constraints",
            extract_prompt=(
                "Based on the PM's proposal (shared_context['proposal_result']), "
                "define the non-negotiable Technical Constraints (red lines). "
                "Format as a numbered list. Each constraint MUST include: "
                "1) What is forbidden, 2) The architectural reason, "
                "3) How a violation will be detected during review. "
                "These constraints ARE the locked spec."
            ),
        ),
    )
    sg.add_node(
        "pm_counter_sign",
        make_role_node(
            _pm,
            task_key="spec_signed",
            extract_prompt=(
                "Review the Architect's constraints (shared_context['constraints_result']). "
                "If you accept them as the project's law, respond with SIGNED. "
                "If any constraint conflicts with business requirements, raise the issue now — "
                "this is the last chance before the spec is locked."
            ),
        ),
    )

    sg.add_edge(START, "pm_propose_requirements")
    sg.add_edge("pm_propose_requirements", "arch_define_constraints")
    sg.add_edge("arch_define_constraints", "pm_counter_sign")
    sg.add_edge("pm_counter_sign", END)

    return sg


# ---------------------------------------------------------------------------
# 3-2: Review Tribunal
# ---------------------------------------------------------------------------
# RACI:
#   Coder (R)   — submits PR/implementation for review
#   QA    (R)   — prosecutor: finds ALL violations vs locked spec
#   Coder (C)   — consulted: defends implementation decisions
#   Arch  (A)   — judge: issues final Merge or Reject verdict
# ---------------------------------------------------------------------------


def _build_flow_3_2() -> StateGraph:
    sg = StateGraph(RACIState)

    sg.add_node(
        "coder_submit_pr",
        make_role_node(
            _coder,
            task_key="pr_submission",
            extract_prompt=(
                "Prepare your Pull Request submission. "
                "Summarise: what was implemented, how it satisfies the spec "
                "(shared_context['constraints_result']), "
                "and any trade-offs or deviations you made and why."
            ),
        ),
    )
    sg.add_node(
        "qa_prosecution",
        make_role_node(
            _qa,
            task_key="prosecution_report",
            extract_prompt=(
                "You are the prosecutor. Examine the PR submission "
                "(shared_context['pr_submission_result']) against each constraint "
                "in the locked spec (shared_context['constraints_result']). "
                "For each constraint, judge: COMPLIANT or VIOLATION (with severity: CRITICAL/MAJOR/MINOR). "
                "Be rigorous — your job is to find problems, not approve."
            ),
        ),
    )
    sg.add_node(
        "coder_defense",
        make_role_node(
            _coder,
            task_key="defense",
            extract_prompt=(
                "The QA prosecution report is in shared_context['prosecution_report_result']. "
                "For each VIOLATION, provide your technical justification: "
                "why did you make this decision and is there an alternative? "
                "Be precise and factual."
            ),
        ),
    )
    sg.add_node(
        "arch_verdict",
        make_role_node(
            _arch,
            task_key="tribunal_verdict",
            extract_prompt=(
                "You are the judge. Review the prosecution report "
                "(shared_context['prosecution_report_result']) and the Coder's defence "
                "(shared_context['defense_result']). "
                "Issue your verdict: MERGE or REJECT. "
                "If REJECT, list the specific issues that MUST be fixed before resubmission. "
                "Set shared_context['verdict'] = 'merge' or 'reject' accordingly."
            ),
        ),
    )

    _verdict = verdict_router(
        approved_key="merge",
        rejected_key="reject",
        verdict_ctx_key="verdict",
    )

    sg.add_edge(START, "coder_submit_pr")
    sg.add_edge("coder_submit_pr", "qa_prosecution")
    sg.add_edge("qa_prosecution", "coder_defense")
    sg.add_edge("coder_defense", "arch_verdict")
    sg.add_conditional_edges(
        "arch_verdict",
        _verdict,
        {
            "merge": END,
            "reject": END,  # rejection hands off to flow_3_3
        },
    )

    return sg


# ---------------------------------------------------------------------------
# 3-3: Refactoring Loop
# ---------------------------------------------------------------------------
# RACI:
#   Arch  (A) — commands Coder to refactor, re-reviews result
#   Coder (R) — must comply with refactor order, no shortcuts
#   QA    (I) — informed of outcomes
# ---------------------------------------------------------------------------


def _increment_refactor_retry(state: RACIState) -> dict[str, Any]:
    """Increment the Refactor retry counter in shared_context."""
    ctx = dict(state.get("shared_context", {}))
    ctx["refactor_retries"] = ctx.get("refactor_retries", 0) + 1
    return {"shared_context": ctx}


def _refactor_limit_router(state: RACIState) -> str:
    retries = state.get("shared_context", {}).get("refactor_retries", 0)
    return "end_max_retries" if retries >= MAX_REFACTOR_RETRIES else "coder_refactor"


def _build_flow_3_3() -> StateGraph:
    sg = StateGraph(RACIState)

    sg.add_node(
        "arch_refactor_order",
        make_role_node(
            _arch,
            task_key="refactor_order",
            extract_prompt=(
                "The previous tribunal issued a REJECT verdict. "
                "As Architect, issue a mandatory refactor order based on the verdict "
                "(shared_context['tribunal_verdict_result']). "
                "Provide a prioritised list of changes the Coder MUST make. "
                "Be specific: file names, function names, exact changes required."
            ),
        ),
    )
    sg.add_node(
        "coder_refactor",
        make_role_node(
            _coder,
            task_key="refactored_code",
            extract_prompt=(
                "You have received a mandatory refactor order from the Architect "
                "(shared_context['refactor_order_result']). "
                "Comply with every point. Output the refactored code. "
                "Do not skip or modify the requirements."
            ),
        ),
    )
    sg.add_node(
        "arch_re_review",
        make_role_node(
            _arch,
            task_key="re_review",
            extract_prompt=(
                "Review the refactored code (shared_context['refactored_code_result']) "
                "against the original refactor order (shared_context['refactor_order_result']). "
                "Has the Coder complied with ALL points? "
                "Set shared_context['verdict'] = 'approved' if yes, 'rejected' if further work needed."
            ),
        ),
    )
    sg.add_node(
        "qa_informed",
        make_role_node(
            _qa,
            task_key="refactor_notification",
            extract_prompt=(
                "You are being informed of the refactoring outcome. "
                "Review shared_context['re_review_result'] and log the result for the audit trail. "
                "No action required — this is an informational step."
            ),
        ),
    )
    sg.add_node("increment_retry", _increment_refactor_retry)

    _verdict = verdict_router(approved_key="approved", rejected_key="check_retries")
    _retries = _refactor_limit_router

    sg.add_edge(START, "arch_refactor_order")
    sg.add_edge("arch_refactor_order", "coder_refactor")
    sg.add_edge("coder_refactor", "arch_re_review")
    sg.add_conditional_edges(
        "arch_re_review",
        _verdict,
        {
            "approved": "qa_informed",
            "check_retries": "increment_retry",
        },
    )
    sg.add_edge("qa_informed", END)
    sg.add_conditional_edges(
        "increment_retry",
        _retries,
        {
            "coder_refactor": "coder_refactor",
            "end_max_retries": END,
        },
    )

    return sg


# ---------------------------------------------------------------------------
# Public compiled graphs
# ---------------------------------------------------------------------------

flow_3_1 = _build_flow_3_1().compile()
flow_3_2 = _build_flow_3_2().compile()
flow_3_3 = _build_flow_3_3().compile()

__all__ = ["flow_3_1", "flow_3_2", "flow_3_3"]

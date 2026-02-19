"""Decision nodes for the Meta-Orchestrator."""

from __future__ import annotations

from typing import Any

import structlog

from arkhon_rheo.config.schema import WorkflowScheme
from arkhon_rheo.core.state import RACIState
from arkhon_rheo.roles.concrete import ProductManager

logger = structlog.get_logger(__name__)

_pm = ProductManager()


async def evaluate_task_complexity(state: RACIState) -> dict[str, Any]:
    """Evaluates the task complexity and suggests a RACI scheme.

    Uses PM agent to reason about the user request.
    """
    user_request = state.get("shared_context", {}).get("user_request", "")

    prompt = (
        "Evaluate the following user request and decide which RACI scheme is most appropriate.\n\n"
        f"User Request: {user_request}\n\n"
        "Schemes:\n"
        "- waterfall: Best for simple, clear, and well-defined tasks. Minimal feedback loops.\n"
        "- agile: Best for complex, iterative tasks requiring tight Dev-QA collaboration.\n"
        "- critic: Best for security-critical, high-quality, or architectural baseline tasks. Strict gatekeeping.\n\n"
        "Use 'sequential-thinking' if the task seems complex or ambiguous.\n\n"
        "Output your decision in the format: SCHEME: [waterfall|agile|critic]\n"
        "Reasoning: [Your brief explanation]\n"
    )

    logger.info("evaluating_task_complexity", user_request=user_request)

    # In a real implementation, this would involve a specific LLM call
    # that can trigger sequential-thinking. For now, we simulate the selection.
    # We use the PM's invoke method which should ideally handle this.
    response = _pm.invoke(prompt)

    selected_scheme = WorkflowScheme.WATERFALL
    if "critic" in response.lower():
        selected_scheme = WorkflowScheme.CRITIC
    elif "agile" in response.lower():
        selected_scheme = WorkflowScheme.AGILE

    logger.info("task_complexity_evaluated", selected=selected_scheme)

    ctx = dict(state.get("shared_context", {}))
    ctx["selected_scheme"] = selected_scheme
    ctx["evaluation_reasoning"] = response

    return {"shared_context": ctx}


def scheme_router(state: RACIState) -> str:
    """Routes to the appropriate scheme subgraph."""
    scheme = state.get("shared_context", {}).get("selected_scheme", WorkflowScheme.WATERFALL)
    return str(scheme)

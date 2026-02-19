"""Shared utilities for RACI Workflow Graph construction.

Provides the :func:`make_role_node` factory that wraps a :class:`BaseRole`
into a LangGraph-compatible ``async`` node function, and :func:`build_state`
to bootstrap a :class:`RACIState` from a plain task description.
"""

from __future__ import annotations

from typing import Any

import structlog

from arkhon_rheo.core.state import RACIState
from arkhon_rheo.roles.base import BaseRole

logger = structlog.get_logger(__name__)


def make_role_node(
    role: BaseRole,
    *,
    task_key: str,
    extract_prompt: str | None = None,
) -> Any:
    """Factory that wraps a BaseRole into an async LangGraph node function.

    The node:
    1. Extracts the latest ``user_content`` from ``state["shared_context"]``
       (key = ``task_key``) or falls back to ``extract_prompt``.
    2. Calls ``role.invoke()`` with the current message history.
    3. Appends the response as ``{"role": "ai", "content": ..., "agent": role_name}``
       to ``state["messages"]``.
    4. Writes the response into ``shared_context[task_key + "_result"]``.

    Args:
        role: The :class:`BaseRole` agent to invoke.
        task_key: Logical name of the task this node performs (used for context keys).
        extract_prompt: Static fallback prompt if nothing found in shared_context.

    Returns:
        An async callable suitable for LangGraph ``add_node()``.
    """
    role_name = role.config.role
    result_key = f"{task_key}_result"

    async def node_fn(state: RACIState) -> dict[str, Any]:
        ctx = state.get("shared_context", {})
        user_content: str = ctx.get(task_key) or extract_prompt or f"Execute task: {task_key}"

        history: list[dict[str, Any]] = state.get("messages", [])
        log = logger.bind(role=role_name, task_key=task_key)
        log.info("node_start")

        response = role.invoke(user_content, history=history)
        log.info("node_done", chars=len(response))

        new_message = {"role": "ai", "content": response, "agent": role_name}
        new_ctx = {**ctx, result_key: response}

        return {
            "messages": [new_message],
            "shared_context": new_ctx,
            "current_task": task_key,
        }

    node_fn.__name__ = f"{role_name}_{task_key}"
    return node_fn


def build_state(
    task_description: str,
    *,
    thread_id: str = "default",
    extra_context: dict[str, Any] | None = None,
) -> RACIState:
    """Bootstrap an initial :class:`RACIState` for a workflow run.

    Args:
        task_description: Human language task prompt from the orchestrator.
        thread_id: Session identifier for checkpointing.
        extra_context: Optional additional entries for ``shared_context``.

    Returns:
        A :class:`RACIState` ready to be fed into :meth:`StateGraph.invoke`.
    """
    return RACIState(
        messages=[{"role": "human", "content": task_description}],
        next_step="",
        shared_context={"user_request": task_description, **(extra_context or {})},
        is_completed=False,
        errors=[],
        thread_id=thread_id,
        raci_config={},
        current_task="",
    )


def verdict_router(
    approved_key: str = "approved",
    rejected_key: str = "rejected",
    verdict_ctx_key: str = "verdict",
) -> Any:
    """Build a routing function that reads a verdict from ``shared_context``.

    Args:
        approved_key: Return value when verdict == 'approved'.
        rejected_key: Return value when verdict == 'rejected'.
        verdict_ctx_key: Key in ``shared_context`` to read verdict from.

    Returns:
        A synchronous router function for LangGraph conditional edges.
    """

    def router(state: RACIState) -> str:
        v = state.get("shared_context", {}).get(verdict_ctx_key, "rejected")
        result = approved_key if str(v).lower() in {"approved", "pass", "ok", "merge"} else rejected_key
        logger.info("verdict_router", verdict=v, route=result)
        return result

    return router

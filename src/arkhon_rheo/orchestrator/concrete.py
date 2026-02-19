"""Meta-Orchestrator Implementation."""

from __future__ import annotations

import asyncio
from typing import cast

from arkhon_rheo.core.state import RACIState
from arkhon_rheo.orchestrator.base import BaseOrchestrator
from arkhon_rheo.orchestrator.meta_graph import meta_orchestrator_graph
from arkhon_rheo.workflows.base import build_state

_DEFAULT_TIMEOUT_SECONDS = 300.0


class MetaOrchestrator(BaseOrchestrator):
    """The central brain for Arkhon-Rheo RACI workflows."""

    async def run(
        self,
        task_description: str,
        *,
        timeout: float = _DEFAULT_TIMEOUT_SECONDS,
    ) -> RACIState:
        """Runs the meta-orchestration graph for the given task.

        Args:
            task_description: Natural language description of the task.
            timeout: Maximum seconds to wait for the graph to complete.
                     Defaults to 300 seconds (5 minutes). Pass ``0`` to
                     disable the timeout.

        Returns:
            The final RACIState after graph execution, or an error state
            on timeout.
        """
        state = build_state(task_description)

        try:
            coro = meta_orchestrator_graph.ainvoke(state)
            if timeout > 0:
                result = await asyncio.wait_for(coro, timeout=timeout)
            else:
                result = await coro
        except TimeoutError:
            state["errors"].append(f"MetaOrchestrator timed out after {timeout}s for task: {task_description!r}")
            state["is_completed"] = True
            return state

        return cast(RACIState, result)

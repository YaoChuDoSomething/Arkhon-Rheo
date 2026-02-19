"""Unit tests for MetaOrchestrator timeout — Phase 3 architectural improvement."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from arkhon_rheo.config.schema import RACIWorkflowConfig
from arkhon_rheo.orchestrator.concrete import MetaOrchestrator


def _orchestrator() -> MetaOrchestrator:
    return MetaOrchestrator(config=RACIWorkflowConfig())


class TestMetaOrchestratorTimeout:
    @pytest.mark.asyncio
    async def test_timeout_returns_error_state(self):
        """When the graph exceeds the timeout, errors are populated."""
        orchestrator = _orchestrator()

        async def slow_coro(*_args, **_kwargs):
            await asyncio.sleep(10)  # will never finish in test

        with patch(
            "arkhon_rheo.orchestrator.concrete.meta_orchestrator_graph.ainvoke",
            side_effect=slow_coro,
        ):
            state = await orchestrator.run("slow task", timeout=0.01)

        assert state["is_completed"] is True
        assert len(state["errors"]) == 1
        assert "timed out" in state["errors"][0]
        assert "slow task" in state["errors"][0]

    @pytest.mark.asyncio
    async def test_no_timeout_when_zero(self):
        """Passing timeout=0 disables the timeout guard."""
        orchestrator = _orchestrator()
        expected = {
            "is_completed": True,
            "errors": [],
            "messages": [],
            "shared_context": {},
            "next_step": "END",
            "thread_id": "test",
        }

        mock_invoke = AsyncMock(return_value=expected)
        with patch(
            "arkhon_rheo.orchestrator.concrete.meta_orchestrator_graph.ainvoke",
            mock_invoke,
        ):
            state = await orchestrator.run("quick task", timeout=0)

        assert state["is_completed"] is True
        assert state["errors"] == []

    @pytest.mark.asyncio
    async def test_successful_run_passes_through(self):
        """Normal execution returns the graph result unchanged."""
        orchestrator = _orchestrator()
        expected = {
            "is_completed": True,
            "errors": [],
            "messages": [],
            "shared_context": {},
            "next_step": "END",
            "thread_id": "test",
        }

        mock_invoke = AsyncMock(return_value=expected)
        with patch(
            "arkhon_rheo.orchestrator.concrete.meta_orchestrator_graph.ainvoke",
            mock_invoke,
        ):
            state = await orchestrator.run("fast task")

        assert state["is_completed"] is True

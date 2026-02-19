"""Meta-Orchestrator Base Interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from arkhon_rheo.config.schema import RACIWorkflowConfig
from arkhon_rheo.core.state import RACIState


class BaseOrchestrator(ABC):
    """Abstract base class for all orchestrators."""

    def __init__(self, config: RACIWorkflowConfig):
        self.config = config

    @abstractmethod
    async def run(self, task_description: str) -> RACIState:
        """Execute a full workflow based on the task description."""
        pass

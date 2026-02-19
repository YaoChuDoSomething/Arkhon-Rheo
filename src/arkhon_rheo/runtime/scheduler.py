import asyncio

from arkhon_rheo.core.agent import Agent


class AgentScheduler:
    """
    Manages the execution lifecycle of multiple agents.
    """

    def __init__(self):
        self.agents: list[Agent] = []

    def register_agent(self, agent: Agent):
        """Register an agent with the scheduler."""
        self.agents.append(agent)

    async def run_until_complete(self, target_task):
        """
        Run the scheduler until the target task is complete.
        This usually involves starting all agents' run loops in the background.
        """
        # Start all agents
        tasks = []
        for agent in self.agents:
            # We wrap agent.run() in a task that can be cancelled
            task = asyncio.create_task(agent.run())
            tasks.append(task)

        try:
            # Wait for the target task (e.g., initial user request processing)
            # In a real system, this might be waiting for a specific event or condition
            await target_task
        finally:
            # Cancel all background agent tasks
            for task in tasks:
                task.cancel()

            # Wait for cancellation to complete
            await asyncio.gather(*tasks, return_exceptions=True)

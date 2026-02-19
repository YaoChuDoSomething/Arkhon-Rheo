"""Agent State Module.

This module defines the state structures used within the Arkhon-Rheo
agentic graphs and governance workflows. It utilizes TypedDict for
structured state definitions.
"""

import operator
from typing import Annotated, Any, TypedDict


class RACIAssignment(TypedDict, total=False):
    """Assignment of roles in a RACI matrix for a specific task.

    Attributes:
        responsible: List of agent names responsible for executing the task.
        accountable: Name of the agent accountable for the task outcome.
        consulted: List of agent names to be consulted during the task.
        informed: List of agent names to be informed of the task progress.
    """

    responsible: list[str]
    accountable: str
    consulted: list[str]
    informed: list[str]


class AgentState(TypedDict):
    """Standard state definition for Arkhon-Rheo agentic graphs.

    Attributes:
        messages: A sequence of messages, accumulated using operator.add.
        next_step: The name of the next node to execute (fallback for static routing).
        shared_context: Arbitrary key-value store for cross-node data.
        is_completed: Flag to terminate the execution loop.
        errors: List of error messages captured during execution.
        thread_id: Unique identifier for the conversation session (used for checkpointing).
    """

    messages: Annotated[list[dict[str, Any]], operator.add]
    next_step: str
    shared_context: dict[str, Any]
    is_completed: bool
    errors: list[str]
    thread_id: str


class RACIState(AgentState):
    """State definition for RACI-based governance workflows.

    Attributes:
        raci_config: Mapping of tasks/nodes to RACIAssignment.
        current_task: Name of the current task being evaluated.
    """

    raci_config: dict[str, RACIAssignment]
    current_task: str

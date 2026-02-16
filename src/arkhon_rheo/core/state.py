from typing import Annotated, TypedDict, List, Any, Dict
import operator


class AgentState(TypedDict):
    """
    Standard state definition for Arkhon-Rheo agentic graphs.

    Attributes:
        messages: A sequence of messages, accumulated using operator.add.
        next_step: The name of the next node to execute (fallback for static routing).
        shared_context: Arbitrary key-value store for cross-node data.
        is_completed: Flag to terminate the execution loop.
        errors: List of error messages captured during execution.
        thread_id: Unique identifier for the conversation session (used for checkpointing).
    """

    messages: Annotated[List[Dict[str, Any]], operator.add]
    next_step: str
    shared_context: Dict[str, Any]
    is_completed: bool
    errors: List[str]
    thread_id: str

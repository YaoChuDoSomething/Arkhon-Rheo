"""RACI Rules Module.

This module defines specific validation rules for RACI (Responsible,
Accountable, Consulted, Informed) governance configurations.
"""

from arkhon_rheo.core.state import RACIState


def validate_raci_config(state: RACIState) -> bool:
    """Validate that the RACI configuration meets mandatory requirements.

    Rule: Every task in raci_config MUST have exactly one Accountable agent
    and at least one Responsible agent.

    Args:
        state: The RACIState instance to validate.

    Returns:
        True if the configuration is valid, otherwise False.
    """
    config = state.get("raci_config", {})
    for task_name, assignment in config.items():
        if not assignment.get("accountable"):
            return False
        # Responsible is also usually required
        if not assignment.get("responsible"):
            return False
    return True


def validate_responsible_overlap(state: RACIState) -> bool:
    """Check for recommended separation of Responsible and Accountable roles.

    Rule: While an Accountable agent can also be Responsible, it's
    recommended to separate them for clearer governance.

    Args:
        state: The RACIState instance to evaluate.

    Returns:
        True (currently always returns True as this is a recommendation).
    """
    # Simple pass for now, can be used for warnings in the future
    return True

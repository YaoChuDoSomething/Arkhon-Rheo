"""Arkhon-Rheo RACI Agent Roles.

Provides four concrete role classes built on top of :class:`BaseRole`:
- :class:`ProductManager`
- :class:`SystemArchitect`
- :class:`SoftwareEngineer`
- :class:`QualityAssurance`
"""

from arkhon_rheo.roles.base import BaseRole
from arkhon_rheo.roles.concrete import (
    ProductManager,
    QualityAssurance,
    SoftwareEngineer,
    SystemArchitect,
)

__all__ = [
    "BaseRole",
    "ProductManager",
    "QualityAssurance",
    "SoftwareEngineer",
    "SystemArchitect",
]

"""Vector Store Module.

This module defines the abstract base class for vector storage systems used
within the Arkhon-Rheo framework for efficient similarity searches and
memory persistence.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class VectorStore(ABC):
    """Abstract base class for vector storage systems.

    Subclasses must implement methods for upserting, querying, and deleting
    vectors and their associated metadata.
    """

    @abstractmethod
    async def upsert(
        self, id: str, vector: np.ndarray, metadata: dict[str, Any]
    ) -> None:
        """Store or update a vector and its metadata.

        Args:
            id: Unique identifier for the vector.
            vector: The numpy array representing the vector.
            metadata: Associated key-value pairs for the vector.
        """
        pass

    @abstractmethod
    async def query(
        self, query_vector: np.ndarray, top_k: int = 5
    ) -> list[dict[str, Any]]:
        """Retrieve similar vectors based on a query vector.

        Args:
            query_vector: The vector to search with.
            top_k: The number of top similar results to return.

        Returns:
            A list of matches, each represented as a dictionary.
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        """Delete a vector and its metadata by its identifier.

        Args:
            id: The unique identifier of the vector to delete.
        """
        pass

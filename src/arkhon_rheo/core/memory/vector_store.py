from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class VectorStore(ABC):
    """Abstract base class for vector storage and retrieval.

    Defines the interface for storing, searching, and managing embeddings
    and their associated metadata.
    """

    @abstractmethod
    async def upsert(self, item_id: str, vector: np.ndarray, metadata: dict[str, Any]) -> None:
        """Store or update a vector and its metadata.

        Args:
            item_id: Unique identifier for the vector.
            vector: The embedding vector as a numpy array.
            metadata: Associated metadata dictionary.
        """
        pass

    @abstractmethod
    async def search(self, query_vector: np.ndarray, top_k: int = 5) -> list[dict[str, Any]]:
        """Search for the most similar vectors.

        Args:
            query_vector: The search query embedding.
            top_k: Number of results to return.

        Returns:
            A list of result dictionaries containing metadata and similarity scores.
        """
        pass

    @abstractmethod
    async def delete(self, item_id: str) -> None:
        """Delete a vector and its metadata by its identifier.

        Args:
            item_id: Unique identifier of the vector to delete.
        """
        pass

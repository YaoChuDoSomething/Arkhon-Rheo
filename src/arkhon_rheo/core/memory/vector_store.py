from abc import ABC, abstractmethod
from typing import Any, Dict, List

import numpy as np


class VectorStore(ABC):
    """
    Abstract base class for vector storage systems.
    """

    @abstractmethod
    async def upsert(
        self, id: str, vector: np.ndarray, metadata: Dict[str, Any]
    ) -> None:
        """Store a vector and its metadata (async)."""
        pass

    @abstractmethod
    async def query(
        self, query_vector: np.ndarray, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve top_k similar vectors (async)."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        """Delete a vector by id (async)."""
        pass

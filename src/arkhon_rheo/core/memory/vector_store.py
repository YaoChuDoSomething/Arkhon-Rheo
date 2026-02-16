from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import numpy as np


class VectorStore(ABC):
    """
    Abstract base class for vector storage systems.
    """

    @abstractmethod
    def upsert(self, id: str, vector: np.ndarray, metadata: Dict[str, Any]) -> None:
        """Store a vector and its metadata."""
        pass

    @abstractmethod
    def query(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve top_k similar vectors."""
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        """Delete a vector by id."""
        pass

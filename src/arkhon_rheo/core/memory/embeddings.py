from abc import ABC, abstractmethod
from typing import List

import numpy as np


class Embeddings(ABC):
    """
    Abstract base class for text embeddings.
    """

    @abstractmethod
    async def embed_text(self, text: str) -> np.ndarray:
        """Convert text to a vector (async)."""
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Convert a list of texts to vectors (async)."""
        pass

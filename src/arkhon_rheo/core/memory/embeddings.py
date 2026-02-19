"""Embeddings Module.

This module defines the abstract base class for text embedding systems used
within the Arkhon-Rheo framework to convert text into vector representations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class Embeddings(ABC):
    """Abstract base class for text embeddings.

    Subclasses must implement methods for converting single strings or
    batches of text into numerical vectors (numpy arrays).
    """

    @abstractmethod
    async def embed_text(self, text: str) -> np.ndarray:
        """Convert a single string into a vector.

        Args:
            text: The input text to be embedded.

        Returns:
            A numpy array representing the text embedding.
        """
        pass

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[np.ndarray]:
        """Convert a list of strings into a list of vectors.

        Args:
            texts: A list of input strings to be embedded.

        Returns:
            A list of numpy arrays representing the text embeddings.
        """
        pass

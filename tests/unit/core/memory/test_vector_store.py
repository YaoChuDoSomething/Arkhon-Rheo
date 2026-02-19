from typing import Any

import numpy as np
import pytest

from arkhon_rheo.core.memory.vector_store import VectorStore


class MockVectorStore(VectorStore):
    def __init__(self):
        self.vectors = {}

    async def upsert(self, item_id: str, vector: np.ndarray, metadata: dict[str, Any]) -> None:
        self.vectors[item_id] = (vector, metadata)

    async def search(self, query_vector: np.ndarray, top_k: int = 5) -> list[dict[str, Any]]:
        # Very simple similarity (dot product for normalized vectors)
        results = []
        for item_id, (vec, meta) in self.vectors.items():
            score = float(np.dot(query_vector, vec))
            results.append({"item_id": item_id, "score": score, "metadata": meta})
        return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]

    async def delete(self, item_id: str) -> None:
        if item_id in self.vectors:
            del self.vectors[item_id]


@pytest.mark.asyncio
async def test_vector_store_basic():
    # Arrange
    store = MockVectorStore()
    v1 = np.array([1.0, 0.0])
    v2 = np.array([0.0, 1.0])

    # Act
    await store.upsert("1", v1, {"text": "A"})
    await store.upsert("2", v2, {"text": "B"})

    # Query for something close to v1
    results = await store.search(np.array([0.9, 0.1]))

    # Assert
    assert results[0]["item_id"] == "1"
    assert results[0]["metadata"]["text"] == "A"

import numpy as np
import pytest

from arkhon_rheo.core.memory.vector_store import VectorStore


class MockVectorStore(VectorStore):
    def __init__(self):
        self.vectors = {}

    async def upsert(self, id: str, vector: np.ndarray, metadata: dict):
        self.vectors[id] = (vector, metadata)

    async def query(self, query_vector: np.ndarray, top_k: int = 5):
        # Very simple similarity (dot product for normalized vectors)
        results = []
        for id, (vec, meta) in self.vectors.items():
            score = float(np.dot(query_vector, vec))
            results.append({"id": id, "score": score, "metadata": meta})
        return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]

    async def delete(self, id: str):
        if id in self.vectors:
            del self.vectors[id]


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
    results = await store.query(np.array([0.9, 0.1]))

    # Assert
    assert results[0]["id"] == "1"
    assert results[0]["metadata"]["text"] == "A"

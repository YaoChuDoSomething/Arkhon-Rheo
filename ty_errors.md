error[invalid-return-type]: Return type does not match returned value
  --> src/arkhon_rheo/core/runtime/scheduler.py:70:16
   |
68 |         if asyncio.iscoroutine(result):
69 |             result = await result
70 |         return result if isinstance(result, dict) else None
   |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `dict[str, Any] | None`, found `Top[dict[Unknown, Unknown]] | None`
71 |
72 |     def _apply_delta(self, state: AgentState, result: dict[str, Any]) -> None:
   |
  ::: src/arkhon_rheo/core/runtime/scheduler.py:64:10
   |
62 |     async def _execute_node(
63 |         self, node_name: str, state: AgentState
64 |     ) -> dict[str, Any] | None:
   |          --------------------- Expected `dict[str, Any] | None` because of return type
65 |         """Execute a specific node's action."""
66 |         action = self.graph.nodes[node_name]
   |
info: rule `invalid-return-type` is enabled by default

error[invalid-key]: TypedDict `AgentState` can only be subscripted with a string literal key, got key of type `str`.
  --> src/arkhon_rheo/core/runtime/scheduler.py:76:23
   |
74 |         for k, v in result.items():
75 |             if k == "messages" and k in state:
76 |                 state[k] = state[k] + v
   |                       ^
77 |             else:
78 |                 state[k] = v
   |
info: rule `invalid-key` is enabled by default

error[invalid-key]: TypedDict `AgentState` can only be subscripted with a string literal key, got key of type `str`
  --> src/arkhon_rheo/core/runtime/scheduler.py:76:34
   |
74 |         for k, v in result.items():
75 |             if k == "messages" and k in state:
76 |                 state[k] = state[k] + v
   |                                  ^
77 |             else:
78 |                 state[k] = v
   |
info: rule `invalid-key` is enabled by default

error[invalid-key]: TypedDict `AgentState` can only be subscripted with a string literal key, got key of type `str`.
  --> src/arkhon_rheo/core/runtime/scheduler.py:78:23
   |
76 |                 state[k] = state[k] + v
77 |             else:
78 |                 state[k] = v
   |                       ^
79 |
80 |     def _handle_error(self, state: AgentState, error: Exception) -> str:
   |
info: rule `invalid-key` is enabled by default

error[invalid-method-override]: Invalid override of method `run`
  --> src/arkhon_rheo/tools/builtin/calculator.py:25:9
   |
23 |     description = "Evaluate mathematical expressions safely."
24 |
25 |     def run(self, tool_input: str, **_kwargs: Any) -> str:
   |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Definition is incompatible with `BaseTool.run`
26 |         """Evaluate a mathematical expression string.
   |
  ::: src/arkhon_rheo/tools/base.py:54:9
   |
53 |     @abstractmethod
54 |     def run(self, **kwargs: Any) -> Any:
   |         ------------------------------- `BaseTool.run` defined here
55 |         """Execute the core tool logic.
   |
info: This violates the Liskov Substitution Principle
info: rule `invalid-method-override` is enabled by default

error[unresolved-reference]: Name `Agent` used when not defined
  --> tests/unit/agents/test_specialist.py:22:37
   |
20 |     replies = []
21 |
22 |     async def mock_send(recipient: "Agent", message: AgentMessage) -> None:
   |                                     ^^^^^
23 |         replies.append(message)
   |
info: rule `unresolved-reference` is enabled by default

error[invalid-method-override]: Invalid override of method `upsert`
  --> tests/unit/core/memory/test_vector_store.py:11:15
   |
 9 |         self.vectors = {}
10 |
11 |     async def upsert(self, id: str, vector: np.ndarray, metadata: dict):
   |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Definition is incompatible with `VectorStore.upsert`
12 |         self.vectors[id] = (vector, metadata)
   |
  ::: src/arkhon_rheo/core/memory/vector_store.py:15:15
   |
14 |     @abstractmethod
15 |     async def upsert(self, item_id: str, vector: np.ndarray, metadata: dict[str, Any]) -> None:
   |               -------------------------------------------------------------------------------- `VectorStore.upsert` defined here
16 |         """Store or update a vector and its metadata.
   |
info: This violates the Liskov Substitution Principle
info: rule `invalid-method-override` is enabled by default

error[invalid-method-override]: Invalid override of method `delete`
  --> tests/unit/core/memory/test_vector_store.py:22:15
   |
20 |         return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
21 |
22 |     async def delete(self, id: str):
   |               ^^^^^^^^^^^^^^^^^^^^^ Definition is incompatible with `VectorStore.delete`
23 |         if id in self.vectors:
24 |             del self.vectors[id]
   |
  ::: src/arkhon_rheo/core/memory/vector_store.py:39:15
   |
38 |     @abstractmethod
39 |     async def delete(self, item_id: str) -> None:
   |               ---------------------------------- `VectorStore.delete` defined here
40 |         """Delete a vector and its metadata by its identifier.
   |
info: This violates the Liskov Substitution Principle
info: rule `invalid-method-override` is enabled by default

error[not-subscriptable]: Cannot subscript object of type `None` with no `__getitem__` method
  --> tests/unit/core/runtime/test_checkpoint.py:18:12
   |
17 |     assert loaded_state == state
18 |     assert loaded_state["shared_context"]["key"] == "value"
   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
19 |     assert "thread_123" in manager.list_threads()
   |
info: rule `not-subscriptable` is enabled by default

error[not-subscriptable]: Cannot subscript object of type `None` with no `__getitem__` method
  --> tests/unit/core/runtime/test_checkpoint.py:33:12
   |
32 |     loaded = manager.load_checkpoint("t1")
33 |     assert loaded["val"] == 2
   |            ^^^^^^^^^^^^^
   |
info: rule `not-subscriptable` is enabled by default

error[invalid-method-override]: Invalid override of method `run`
  --> tests/unit/tools/test_registry.py:17:13
   |
15 |         description = "A mock tool"
16 |
17 |         def run(self, input: str, **kwargs: Any) -> str:
   |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Definition is incompatible with `BaseTool.run`
18 |             return f"Mock: {input}"
   |
  ::: src/arkhon_rheo/tools/base.py:54:9
   |
53 |     @abstractmethod
54 |     def run(self, **kwargs: Any) -> Any:
   |         ------------------------------- `BaseTool.run` defined here
55 |         """Execute the core tool logic.
   |
info: This violates the Liskov Substitution Principle
info: rule `invalid-method-override` is enabled by default

error[invalid-method-override]: Invalid override of method `run`
  --> tests/unit/tools/test_registry.py:38:13
   |
36 |         description = "A mock tool"
37 |
38 |         def run(self, input: str, **kwargs: Any) -> str:
   |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Definition is incompatible with `BaseTool.run`
39 |             return ""
   |
  ::: src/arkhon_rheo/tools/base.py:54:9
   |
53 |     @abstractmethod
54 |     def run(self, **kwargs: Any) -> Any:
   |         ------------------------------- `BaseTool.run` defined here
55 |         """Execute the core tool logic.
   |
info: This violates the Liskov Substitution Principle
info: rule `invalid-method-override` is enabled by default

Found 12 diagnostics

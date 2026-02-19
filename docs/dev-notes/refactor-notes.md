# REVIEW REPORT

這份分析與重構建議針對 `Arkhon-Rheo` 專案現狀（Phase 3：Memory & Storage）進行深度解構，並對標 LangGraph 的工業級架構進行模組化設計。

## 1. 架構深度分析 (Architectural Analysis)

`Arkhon-Rheo` 目前展現出高度解耦的層級設計，其核心邏輯圍繞著 **Graph-based Execution** 與 **Hierarchical Memory** 展開。

* **核心引擎 (Core Engine)**：透過 `graph.py` 與 `runtime/` 驅動，支持節點化執行。
* **節點類型 (Node Specialization)**：區分了 `Thought`, `Action`, `Observation`, `Commit`, `Validate`。這表明系統不只是簡單的 Chain，而是具備推理與驗證能力的複雜圖形。
* **記憶體架構 (Memory Architecture)**：具備 `context_window` (短期)、`vector_store` (長期) 與 `summarization` (壓縮)，這屬於典型的 **Memory-Augmented Agent**。
* **持久化機制 (State Persistence)**：`checkpoint.py` 指向了狀態恢復與中斷重啟的能力，這是處理長耗時 Agent 任務的關鍵。

---

## 2. Agentic System 判定與控制循環

該系統確屬於 **Agentic System**，且採用了類 **ReAct (Reasoning and Acting)** 的變體。

### 控制循環 (Control Loop)

系統預期的控制流如下：

1. **Thought Node**: 接收 `SharedState`，生成推理邏輯。
2. **Action Node**: 決定執行的工具或子任務。
3. **Observation Node**: 捕獲工具執行結果。
4. **Validate/Commit Node**: 檢查結果是否符合預期，若否則回溯至 Thought Node（形成 **Cyclic Graph**）。

### 狀態機 (State Machine)

透過 `graph.py` 定義節點間的跳轉邏輯。目前結構暗示了一個 **Persistent State Machine**，狀態儲存於 `SharedState` 中，並透過 `CheckpointManager` 寫入 SQLite 或磁碟。

---

## 3. 工程級重構方案：對齊 LangGraph 架構

為了達到 LangGraph 等級的健壯性，我們將強化以下三點：

1. **定義強型別 State**：確保節點間數據傳遞的穩定。
2. **異步調度器 (Async Scheduler)**：提高並發處理能力。
3. **條件邊緣 (Conditional Edges)**：顯式化控制流決策邏輯。

### 專案文件結構路徑

`Arkhon-Rheo/src/arkhon_rheo/core/`

```python
# arkhon_rheo/core/state.py
from typing import Annotated, TypedDict, Union, List, Any
import operator

class AgentState(TypedDict):
    """
    State definition for the agentic graph.
    Uses operator.add to handle sequence accumulation for messages.
    """
    messages: Annotated[List[dict], operator.add]
    next_step: str
    shared_context: dict
    is_completed: bool
    errors: List[str]

# arkhon_rheo/core/graph.py
from typing import Callable, Dict, Optional
from arkhon_rheo.core.state import AgentState

class Graph:
    """
    An advanced execution graph inspired by LangGraph.
    Supports nodes, edges, and conditional routing.
    """
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}
        self.edges: List[tuple] = []
        self.conditional_edges: Dict[str, Dict[str, Callable]] = {}

    def add_node(self, name: str, action: Callable):
        self.nodes[name] = action

    def add_edge(self, start_node: str, end_node: str):
        self.edges.append((start_node, end_node))

    def add_conditional_edge(self, source: str, path_map: Dict[str, str], condition: Callable):
        """
        Routes the flow based on the result of the condition function.
        """
        self.conditional_edges[source] = {"map": path_map, "fn": condition}

# arkhon_rheo/core/runtime/scheduler.py
import asyncio
from datetime import datetime
import numpy as np
from arkhon_rheo.core.graph import Graph
from arkhon_rheo.core.state import AgentState

class RuntimeScheduler:
    """
    Asynchronous executor for the agentic graph with checkpointing support.
    """
    def __init__(self, graph: Graph, checkpoint_manager: Any):
        self.graph = graph
        self.checkpoint_manager = checkpoint_manager

    async def step(self, current_node: str, state: AgentState) -> str:
        """
        Execute a single node and determine the next transition.
        """
        # Node execution
        new_state_delta = await self.graph.nodes[current_node](state)
        state.update(new_state_delta)
        
        # Checkpoint persistence
        timestamp = np.datetime64(datetime.now())
        self.checkpoint_manager.save(state, timestamp)

        # Routing logic
        if current_node in self.graph.conditional_edges:
            cond_cfg = self.graph.conditional_edges[current_node]
            decision = cond_cfg["fn"](state)
            return cond_cfg["map"][decision]
        
        # Static routing
        for start, end in self.graph.edges:
            if start == current_node:
                return end
        
        return "END"

    async def run(self, initial_state: AgentState, entry_point: str):
        """
        Main control loop (The Engine).
        """
        curr = entry_point
        while curr != "END" and not initial_state.get("is_completed"):
            curr = await self.step(curr, initial_state)

```

---

## 4. 針對 `CheckpointManager` 的安全性與效能修正

根據 `meta_prompts.yaml`  的要求，我們需要移除潛在的 `pickle` 漏洞並優化併發。

### 修改模組：`arkhon_rheo/core/runtime/checkpoint.py`

```diff
--- old/checkpoint.py
+++ new/checkpoint.py
@@ -1,15 +1,28 @@
-import pickle
+import json
+import sqlite3
+from typing import Any, Dict

 class CheckpointManager:
     def __init__(self, db_path: str):
-        self.db_path = db_path
+        self.conn = sqlite3.connect(db_path, check_same_thread=False)
+        self._setup_db()
+
+    def _setup_db(self):
+        with self.conn:
+            self.conn.execute("""
+                CREATE TABLE IF NOT EXISTS checkpoints (
+                    thread_id TEXT PRIMARY KEY,
+                    data TEXT,
+                    timestamp TEXT
+                )
+            """)
 
     def save(self, state: Dict[str, Any], timestamp: Any):
-        [cite_start]# REFACTOR: Avoid pickle for security [cite: 14]
-        data = pickle.dumps(state)
-        # ... storage logic
+        """Save state using JSON to prevent arbitrary code execution."""
+        serialized = json.dumps(state, default=str)
+        with self.conn:
+            self.conn.execute(
+                "INSERT OR REPLACE INTO checkpoints (thread_id, data, timestamp) VALUES (?, ?, ?)",
+                (state.get("thread_id", "default"), serialized, str(timestamp))
+            )

```

---


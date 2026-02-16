# Phase 3 (Memory Systems) 技能指南

**版本**: 1.0.0  
**適用階段**: Phase 3 - Memory & Storage Systems (Week 8-10)

---

## 🚀 Phase 3 核心技能矩陣

在 Phase 3 中，重點轉向 **長期記憶** 與 **狀態持久化**。

### 核心實作技能

- `vector-db-expert` - 用於 `VectorStore` 與 RAG 整合。
- `sqlite-persistence` - 用於 `CheckpointManager` 實作。
- `token-optimization` - 用於 `ContextWindow` 與 `Summarization`。
- `performance-profiler` - 確保查詢延遲 <500ms。

### 上下文管理技能 (Memory Ops)

- `context-window-management` (Week 8): 深入處理 Sliding Window 邏輯。
- `context-persistence` (Week 9/10): 處理向量化存儲與檢索。
- `context-management-context-restore` (Week 10): 實現 Checkpoint 回滾與復原。

---

## 📅 Sprint 建議路徑

### Sprint 3.1: Short-term Memory (Week 8)

- **重點**: 管理 Agent 的注意力與 Token 限制。
- **建議作業**:
    1. 使用 `context-window-management` 實作 `ContextWindow` 類別。
    2. 整合 `tiktoken` 進行精確的 Token 計數。
    3. 實作 LLM 觸發的摘要 (Summarization) 機制。

### Sprint 3.2: Vector Store Integration (Week 9)

- **重點**: 為 Agent 提供廣大的背景知識（長期記憶）。
- **建議作業**:
    1. 定義 `VectorStore` 抽象介面。
    2. 實作 RAG 檢索策略（語義、混合、時間加權）。
    3. 使用 `vector-db-expert` 技能優化檢索性能。

### Sprint 3.3: Checkpointing & Rollback (Week 10)

- **重點**: 系統可靠性與人類干預機制。
- **建議作業**:
    1. 實作 `CheckpointManager` 使用 SQLite 持久化狀態。
    2. 實作 `rollback(step_n)` 函數，確保狀態回溯的冪等性。
    3. 整合人類審核節點 (Human Approval Gates)，實現「中斷-審核-恢復」流程。

---

## 🔑 Phase 3 Context 策略總結

| Sprint | 策略維度 | 實作目標 |
| :--- | :--- | :--- |
| **Week 8** | **寬度控制** | Sliding Window 確保即時 Context 不超出窗口且成本可控。 |
| **Week 9** | **深度檢索** | 利用向量數據庫進行高效檢索，補充當前 Context。 |
| **Week 10** | **持久化/恢復** | 將 Context 歷史完整保存，支援跨 Session 的斷點續行。 |

# Phase 2 (Multi-Agent) 文件索引

**版本**: 1.0.0  
**最後更新**: 2026-02-16  
**狀態**: ✅ 已完成 (Completed)
**適用階段**: Phase 2 - Multi-Agent Architecture (Week 5-7)

---

## 📚 核心開發流程文件

Phase 2 的開發流程導向文件，按重要性排序：

| # | 文件 | 用途 | 何時使用 |
| :--- | :--- | :--- | :--- |
| 1 | [**PHASE2_SKILLS.md**](PHASE2_SKILLS.md) | **Sprint 技能指南** | **每個 Sprint 開始時必讀** (Phase 2 專屬) |
| 2 | [ROADMAP.md](./ROADMAP.md#milestone-2-multi-agent-architecture-phase-2---weeks-5-7) | Phase 2 詳細計劃和里程碑 | 了解 Sprint 目標和交付物 |
| 3 | [ARCHITECTURE.md](./ARCHITECTURE.md#multi-agent-orchestration-phase-2) | 多代理架構設計 | 理解系統設計細節 |
| 4 | [PHASE1_INDEX.md](PHASE1_INDEX.md) | Phase 1 基礎參考 | 查閱基礎組件 (Nodes, State) 用法 |
| 5 | [DOC_INDEX.md](DOC_INDEX.md) | 全專案文件導航 | 查找其他文件 |

---

## 🎯 Sprint 對應表

Phase 2 包含 3 個 Sprint，每週一個：

| Sprint | 週數 | 主要目標 | 主要交付物 | 推薦技能 | 狀態 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sprint 2.1** | Week 5 | Agent Communication | `Agent`, `Message`, `SharedState` | [PHASE2_SKILLS.md §Sprint 2.1](./PHASE2_SKILLS.md#sprint-21-agent-communication-week-5) | ✅ |
| **Sprint 2.2** | Week 6 | Agent Orchestration | `Coordinator`, `Specialist` | [PHASE2_SKILLS.md §Sprint 2.2](./PHASE2_SKILLS.md#sprint-22-agent-orchestration-week-6) | ✅ |
| **Sprint 2.3** | Week 7 | Subgraph Support | `SubGraph`, 巢狀執行 | [PHASE2_SKILLS.md §Sprint 2.3](./PHASE2_SKILLS.md#sprint-23-subgraph-support-week-7) | ✅ |

詳細 Sprint 計劃請參考 [ROADMAP.md §Milestone 2](./ROADMAP.md#milestone-2-multi-agent-architecture-phase-2---weeks-5-7)。

---

## ✅ Phase 2 測試標準

Phase 2 測試標準包含並繼承所有 Phase 1 標準：

### 繼承標準

- ✅ **Phase 1 所有測試必須通過** (Single Agent Loop)
- ✅ 覆蓋率維持 **≥90%**
- ✅ mypy/ty 零錯誤

### Phase 2 新增標準

- **Multi-Agent**:
  - 2+ 代理可交換訊息
  - 資源鎖防止並發衝突
- **Orchestration**:
  - Coordinator 正確分發任務
  - 獨立任務並行執行
  - 端對端：User → Coordinator → Specialists → Result
- **Subgraph**:
  - 巢狀子圖深度達 3 層
  - 錯誤正確傳播

### 驗證命令

```bash
# 執行所有測試（核心 + 代理）
uv run pytest tests/core/ tests/agents/ --cov=arkhon_rheo --cov-report=html

# 僅執行 Phase 2 相關測試
uv run pytest tests/agents/

# 僅執行 Phase all 相關測試
uv run pytest

# 類型檢查、品質檢查
uv run ruff check src/arkhon_rheo --fix
uv run ty
```

詳細測試策略請參考 [TDD.md](TDD.md)。

---

## 🔑 Context 管理技能路徑 (Phase 2)

Phase 2 重點在於 **Context 的傳遞與共享**：

| 週次 | Context 重點 | 技能與策略 |
| :--- | :--- | :--- |
| **Week 5** | **訊息 Context** | 使用 `context-fundamentals` 確保 `AgentMessage` 攜帶 Trace ID 與 Metadata。 |
| **Week 6** | **共享 Context** | 使用 `context-manager` 實作 `SharedAgentState`，確保線程安全與資料一致性。 |
| **Week 7** | **層級 Context** | 使用 `context-window-management` 與 Scoping 機制，實作子圖對父圖 Context 的繼承與隔離。 |

詳細說明請參考 [PHASE2_SKILLS.md §Phase 2 Context 策略總結](./PHASE2_SKILLS.md#phase-2-context-策略總結)。

---

## 🚀 快速開始指南 (Phase 2)

### 新手入門

1. 確保 Phase 1 基礎穩固（所有測試通過）。
2. 閱讀 **[ROADMAP.md §Phase 2](./ROADMAP.md#milestone-2-multi-agent-architecture-phase-2---weeks-5-7)** 理解架構目標。
3. 閱讀 **[PHASE2_SKILLS.md](PHASE2_SKILLS.md)** 準備技能。

### 開始 Sprint 2.1 (Week 5)

1. **目標**: 讓兩個 Agent 可以說話。
2. **核心類別**: `Agent` (擴展自 Phase 1 `BaseNode` 或包裝它), `AgentMessage`.
3. **第一步**:
    - 定義 `AgentMessage` dataclass (src/arkhon_rheo/core/message.py)。
    - 實作 `Agent.send_message()` 與 `Agent.receive_message()`。
4. **測試**: 撰寫一個測試，模擬 Agent A 發送訊息給 Agent B，Agent B 接收並確認。

---

## 📂 專案目錄結構 (Phase 2 新增)

```text
src/                          # updated
├── arkhon_rheo/
│   ├── core/
│   │   ├── agent.py          # Sprint 2.1: Agent 基礎
│   │   ├── message.py        # Sprint 2.1: 訊息定義
│   │   ├── shared_state.py   # Sprint 2.1: 共享狀態
│   │   └── subgraph.py       # Sprint 2.3: 子圖
│   ├── agents/               # Sprint 2.2: 具體代理實作
│   │   ├── coordinator.py
│   │   └── specialist.py
│   └── runtime/
│       └── scheduler.py      # Sprint 2.2: 調度器
└── docs/                     # 本目錄
    └── vers0.1.0/
        ├── PHASE2_INDEX.md   # 本文件
        └── PHASE2_SKILLS.md
```

---

## ❓ 常見問題 (Phase 2)

### Q1: Agent 和 Node 有什麼不同？

**A**: `Node` 是執行單元（函數或類別），`Agent` 是擁有自己狀態、信箱和目標的高級實體。Agent 內部可能由一個 `Graph` (包含多個 Nodes) 用於推理，也可能只是一個簡單的 Node。在 Phase 2，我們將 Agent 視為圖中的一個高級節點。

### Q2: 為什麼需要 SharedState？ContextManager 不夠嗎？

**A**: `ContextManager` 通常處理 Thread-local 或 Request-scoped 的上下文。但在 Multi-Agent 並行執行時，我們需要一個明確的共享記憶體空間 (`SharedState`) 來處理資源鎖和跨代理的資料交換，這比隱式的 Context 更安全且易於除錯。

---

## 🛠️ Phase 2 優化與修復 (Hotfixes)

在 Phase 2 的實作過程中，我們針對以下問題進行了優化與修復：

### 1. 解決 Orchestration Hang (協作卡死)

- **問題**: 在複雜的代理編排場景下，由於代理無法正確識別彼此的狀態，導致 `test_orchestration.py` 出現無限等待。
- **解決方案**: 引入了中央代理註冊表 (`AgentRegistry`)，支持代理間的動態查找與狀態監控。
- **相關文件**: `src/arkhon_rheo/core/registry.py`

### 2. 引入 Agent Registry (中央註冊表)

- **功能**: 單例模式 (Singleton) 的註冊表，用於集中管理所有活躍的代理實例。
- **自動註冊**: `Agent` 基類現在會在初始化時自動向 `AgentRegistry` 註冊，簡化了動態拓撲的建構。

### 3. 子圖測試與穩定性增強

- **改進**: 強化了子圖 (Subgraph) 的隔離性測試，確保巢狀執行時的錯誤傳播與資源釋放邏輯正確執行。

---

**維護者**: Arkhon-Rheo Team  
**最後更新**: 2026-02-16  
**文件版本**: 1.0.0

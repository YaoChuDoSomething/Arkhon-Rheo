# Phase 2 Skills 推薦清單

**版本**: 1.0.0  
**最後更新**: 2026-02-16  
**整合**: ROADMAP.md + workflows_ai-agentic-system-builder.md + Multi-Agent Patterns

---

## 概述

本文件為 **Phase 2 (Multi-Agent Architecture)** 的每個 Sprint 推薦相關的開發技能，整合了：

- [ROADMAP.md](./ROADMAP.md#milestone-2-multi-agent-architecture-phase-2---weeks-5-7) 的 Phase 2 詳細計劃
- [workflows_ai-agentic-system-builder.md](./workflows_ai-agentic-system-builder.md) 的技能組合建議
- 多智能體協作與編排模式

---

## Sprint 2.1: Agent Communication (Week 5)

### Sprint 2.1 目標

建立多代理通訊基礎設施與共享狀態機制。

### Sprint 2.1 核心架構 Skills

- **`ai-agents-architect`** ⭐ - 代理架構設計的核心
- **`multi-agent-patterns`** ⭐ - 多代理設計模式（通訊、協作）
- **`distributed-systems`** - 分散式系統概念（雖然是本地運行，但在邏輯上是分散的）
- **`event-sourcing-architect`** - 訊息作為事件的設計

### Sprint 2.1 Context 管理 Skills

- **`context-fundamentals`** - 訊息格式中的 Context Metadata 設計
- **`context-management-context-save`** - 共享狀態的持久化

### Sprint 2.1 實作 Skills

- **`python-pro`** - 進階 Python 實作（Dataclasses, Async IO 準備）
- **`memory-safety-patterns`** - 資源鎖定與並發安全

### Sprint 2.1 主要交付物

- `src/arkhon_rheo/core/agent.py` - Agent 基礎類別
- `src/arkhon_rheo/core/message.py` - 結構化訊息定義
- `src/arkhon_rheo/core/shared_state.py` - 線程安全的共享狀態

### Sprint 2.1 退出標準

- ✅ 兩個代理可以交換訊息
- ✅ 請求-響應關聯 (Correlation ID) 正常工作
- ✅ 資源鎖防止並發修改衝突

---

## Sprint 2.2: Agent Orchestration (Week 6)

### Sprint 2.2 目標

實作代理編排器與專責代理 (Specialists)。

### Sprint 2.2 編排 Skills

- **`agent-orchestration-multi-agent-optimize`** ⭐ - 代理編排與優化
- **`saga-orchestration`** - 長時間運行事務的編排模式
- **`dispatching-parallel-agents`** - 並行任務分發

### Sprint 2.2 角色設計 Skills

- **`architect-review`** - 定義 Coordinator 與 Specialist 的職責邊界
- **`role-based-design`** (General) - 專責代理的設計

### Sprint 2.2 Context 管理 Skills

- **`context-manager`** - 在 Coordinator 與 Specialist 間傳遞 Context
- **`context-optimization`** - 減少傳遞給子代理的上下文大小（只傳相關資訊）

### Sprint 2.2 測試 Skills

- **`distributed-debugging-debug-trace`** - 多代理交互的除錯與追蹤
- **`systematic-debugging`** - 複雜交互的除錯

### Sprint 2.2 主要交付物

- `src/arkhon_rheo/agents/coordinator.py` - 任務協調者
- `src/arkhon_rheo/agents/specialist.py` - 專責代理實作
- `src/arkhon_rheo/runtime/scheduler.py` - 任務調度器

### Sprint 2.2 退出標準

- ✅ Coordinator 能將任務路由給正確的 Specialist
- ✅ 獨立任務可並行執行
- ✅ 端對端測試：使用者請求 → 3 個專責代理 → 最終結果

---

## Sprint 2.3: Subgraph Support (Week 7)

### Sprint 2.3 目標

支援巢狀圖 (Subgraphs) 以處理複雜任務分解。

### Sprint 2.3 核心架構 Skills

- **`hierarchical-agents`** (General) - 層級化代理結構
- **`graph-theory`** (General) - 圖論基礎（處理巢狀結構）
- **`software-architecture`** - 遞迴結構設計

### Sprint 2.3 Context 管理 Skills

- **`context-window-management`** - 子圖的 Context 隔離與繼承
- **`context-propagation`** (General) - 父子圖之間的上下文傳播

### Sprint 2.3 視覺化與工具 Skills

- **`mermaid-expert`** - 生成巢狀圖的視覺化表示
- **`debugger`** - 深入子圖的除錯

### Sprint 2.3 主要交付物

- `src/arkhon_rheo/core/subgraph.py` - 子圖容器
- 巢狀執行邏輯（父圖暫停 → 子圖執行 → 返回）
- 範例：認證子圖、數據處理子圖

### Sprint 2.3 退出標準

- ✅ 子圖可巢狀達 3 層深
- ✅ 父圖 Context 可被子圖存取（依配置）
- ✅ 子圖錯誤正確傳播回父圖
- ✅ 視覺化工具能顯示巢狀結構

---

## Phase 2 Context 策略總結

| Sprint | 重點 | 策略 |
| :--- | :--- | :--- |
| **2.1** | **訊息 Context** | 確保每一條 `AgentMessage` 都攜帶必要的 Context Metadata (Trace ID, Source, Intent)。 |
| **2.2** | **共享 Context** | 實作 `SharedAgentState`，讓多個 Agent 能安全地讀寫共享資訊，同時避免 Context 污染。 |
| **2.3** | **層級 Context** | 實作 Context 的 Scope 機制。子圖應繼承父圖的 Context 快照，但其執行過程中的臨時狀態不應無條件汙染父圖。 |

---

## 相關文件

- [PHASE1_SKILLS.md](./PHASE1_SKILLS.md) - Foundation Skills
- [ROADMAP.md](./ROADMAP.md) - 專案路線圖

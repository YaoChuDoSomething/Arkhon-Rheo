# Phase 1 (Foundation) 文件索引

**版本**: 1.0.0  
**最後更新**: 2026-02-16  
**適用階段**: Phase 1 - Foundation (Week 1-4)

---

## 📚 核心開發流程文件

Phase 1 的開發流程導向文件，按重要性排序：

| # | 文件 | 用途 | 何時使用 |
| :--- | :--- | :--- | :--- |
| 1 | [ROADMAP.md](./ROADMAP.md#milestone-1-foundation-phase-1---weeks-1-4) | Phase 1 詳細計劃和里程碑 | 了解 Sprint 目標和交付物 |
| 2 | [PHASE1_SKILLS.md](./PHASE1_SKILLS.md) | 每個 Sprint 的技能推薦 | 選擇和學習相關技能 |
| 3 | [DEVGUIDE.md](./DEVGUIDE.md) | 開發環境設定和工作流程 | 設定開發環境、日常開發 |
| 4 | [TDD.md](./TDD.md) | 測試驅動開發策略 | 撰寫測試、TDD 工作流程 |
| 5 | [workflows_ai-agentic-system-builder.md](./workflows_ai-agentic-system-builder.md) | AI 代理系統技能組合 | 理解整體技能架構 |
| 6 | [DOC_INDEX.md](./DOC_INDEX.md) | 全專案文件導航 | 查找其他文件 |

---

## 🎯 Sprint 對應表

Phase 1 包含 4 個 Sprint，每週一個：

| Sprint | 週數 | 主要目標 | 主要交付物 | 推薦技能 |
| :--- | :--- | :--- | :--- | :--- |
| **Sprint 1.1** | Week 1 | 核心狀態機 | `ReActState`, `StateGraph`, `ContextManager` | [PHASE1_SKILLS.md §Sprint 1.1](./PHASE1_SKILLS.md#sprint-11-核心狀態機-week-1) |
| **Sprint 1.2** | Week 2 | 節點實作 | 6 個 ReAct 節點類別 | [PHASE1_SKILLS.md §Sprint 1.2](./PHASE1_SKILLS.md#sprint-12-節點實作-week-2) |
| **Sprint 1.3** | Week 3 | 工具整合 | Tool Registry + 3 內建工具 | [PHASE1_SKILLS.md §Sprint 1.3](./PHASE1_SKILLS.md#sprint-13-工具整合-week-3) |
| **Sprint 1.4** | Week 4 | YAML 配置與驗證 | Config系統 + Rule Engine | [PHASE1_SKILLS.md §Sprint 1.4](./PHASE1_SKILLS.md#sprint-14-yaml-配置與驗證-week-4) |

詳細 Sprint 計劃請參考 [ROADMAP.md §Milestone 1](./ROADMAP.md#milestone-1-foundation-phase-1---weeks-1-4)。

---

## ✅ Phase 1 測試標準

### 覆蓋率目標

**統一標準**: ≥**90%** （所有組件）

### 類型檢查

- **ty**: 零錯誤

### 驗證命令

```bash
# 執行測試並生成覆蓋率報告
pytest --cov=arkhon_rheo --cov-report=html

# 類型檢查
uv run ty

# 查看覆蓋率報告
open htmlcov/index.html
```

詳細測試策略請參考 [TDD.md](./TDD.md)。

---

## 🔑 Context 管理技能路徑

Phase 1 的 Context 技能整合路徑（按週次）：

| 週次 | Context 技能 | 用途 |
| :--- | :--- | :--- |
| **Week 1** | `context-fundamentals` | 建立 ContextManager 基礎 |
| **Week 2** | `context-window-management` | LLM 上下文視窗管理 |
| **Week 3** | `context-manager` | 工具上下文傳遞 |
| **Week 4** | `context-management-context-restore` | 配置恢復機制 |

詳細說明請參考 [PHASE1_SKILLS.md §Context Skills 整體策略](./PHASE1_SKILLS.md#context-skills-整體策略)。

---

## 🚀 快速開始指南

### 新手入門路徑

如果您剛開始 Phase 1 開發，建議按以下順序閱讀：

1. **[本文件 PHASE1_INDEX.md](./PHASE1_INDEX.md)** - 您在這裡 ✓
2. **[ROADMAP.md §Phase 1](./ROADMAP.md#milestone-1-foundation-phase-1---weeks-1-4)** - 理解整體計劃
3. **[DEVGUIDE.md §1-2](./DEVGUIDE.md)** - 設定開發環境
4. **[PHASE1_SKILLS.md](./PHASE1_SKILLS.md)** - 學習當前 Sprint 的技能
5. **[TDD.md](./TDD.md)** - 開始 TDD 工作流程

### 按 Sprint 開始

**Sprint 1.1** (本週是 Week 1):

1. 閱讀 [ROADMAP.md §Sprint 1.1](./ROADMAP.md#sprint-11-core-state-machine-week-1)
2. 學習 [PHASE1_SKILLS.md §Sprint 1.1](./PHASE1_SKILLS.md#sprint-11-核心狀態機-week-1) 推薦的技能
3. 特別重點：**`context-fundamentals`** 技能（必讀）
4. 開始 TDD 循環：寫測試 → 實作 → 重構

---

## 📂 專案目錄結構

```text
src/arkhon-rheo/
├── arkhon_rheo/          # 主套件
│   ├── core/             # Sprint 1.1: 狀態機和圖
│   ├── nodes/            # Sprint 1.2: ReAct 節點
│   ├── tools/            # Sprint 1.3: 工具註冊表
│   ├── rules/            # Sprint 1.4: 規則引擎
│   ├── config/           # Sprint 1.4: 配置
│   ├── memory/           # Phase 2-3
│   └── runtime/          # Phase 2-3
├── tests/                # 測試套件
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── docs/                 # 本目錄
    └── vers0.1.0/        # Phase 1 文件
```

---

## 🛠️ 開發工作流程

### 日常開發循環

```bash
# 1. 切換分支（如果需要）
git checkout feature/my-feature

# 2. 執行 TDD 循環
# RED: 寫失敗的測試
pytest tests/unit/core/test_state.py -v

# GREEN: 最小實作使測試通過
# 編輯 src/arkhon_rheo/core/state.py
pytest tests/unit/core/test_state.py -v

# REFACTOR: 重構代碼
# 重新執行測試確保仍然通過

# 3. 代碼品質檢查
uv run ruff check src/arkhon_rheo --fix
uv run ty

# 4. 提交
git add .
git commit -m "feat(core): add ReActState immutable container"
```

詳細工作流程請參考 [DEVGUIDE.md §2](./DEVGUIDE.md#2-development-workflow)。

---

## 🔗 相關系統文件

Phase 1 不直接需要，但可能參考的系統文件：

- [SPECIFICATION.md](./SPECIFICATION.md) - 技術需求規格
- [ARCHITECTURE.md](./ARCHITECTURE.md) - 組件架構
- [DESIGN.md](./DESIGN.md) - 系統設計細節
- [STATE_MACHINE.md](./STATE_MACHINE.md) - 狀態機設計
- [WORKFLOW_AUTOMATION.md](../system/WORKFLOW_AUTOMATION.md) - SDLC 工作流程自動化

---

## ❓ 常見問題

### Q1: Sprint 1.1 應該從哪裡開始？

**A**:

1. 閱讀 [ROADMAP.md §Sprint 1.1](./ROADMAP.md#sprint-11-core-state-machine-week-1) 的交付物清單
2. 學習 `context-fundamentals` 技能（位於 `.agent/skills/context-fundamentals/`）
3. 從 `tests/unit/core/test_state.py` 開始寫第一個測試（TDD RED 階段）

### Q2: 如何找到推薦的技能？

**A**:
所有技能位於 `.agent/skills/` 目錄：

```bash
# 查看 context-fundamentals 技能
cat .agent/skills/context-fundamentals/SKILL.md
```

### Q3: 測試覆蓋率達不到 90% 怎麼辦？

**A**:

1. 執行 `pytest --cov=arkhon_rheo --cov-report=term-missing` 查看未覆蓋的行
2. 為未覆蓋的分支添加測試
3. 參考 [TDD.md §9](./TDD.md#9-code-coverage) 的覆蓋率策略

### Q4: SDLC 狀態和 Sprint 是什麼關係？

**A**:

- **Sprint** 是時程里程碑（每週一個）
- **SDLC 狀態** 是工作流程狀態（Planning → Design → Implementation → Testing → Review → Deployment → Monitoring）
- **Agile 概念**: 每個 Sprint 會經歷多次完整的 SDLC 循環
- 詳見 [WORKFLOW_AUTOMATION.md](../system/WORKFLOW_AUTOMATION.md)

---

## 📬 需要幫助？

- **技能問題**: 查看 [workflows_ai-agentic-system-builder.md](./workflows_ai-agentic-system-builder.md)
- **環境問題**: 查看 [DEVGUIDE.md §11 Troubleshooting](./DEVGUIDE.md#11-troubleshooting)
- **測試問題**: 查看 [TDD.md](./TDD.md)
- **架構問題**: 查看 [ARCHITECTURE.md](./ARCHITECTURE.md)

---

**維護者**: Arkhon-Rheo Team  
**最後更新**: 2026-02-16  
**文件版本**: 1.0.0

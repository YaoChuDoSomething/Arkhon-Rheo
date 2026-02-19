# Phase 1 Skills 推薦清單

**版本**: 1.0.0  
**最後更新**: 2026-02-16  
**整合**: ROADMAP.md + workflows_ai-agentic-system-builder.md + Context Skills

---

## 概述

本文件為 **Phase 1 (Foundation)** 的每個 Sprint 推薦相關的開發技能，整合了：

- [ROADMAP.md](ROADMAP.md) 的 Phase 1 詳細計劃
- [workflows_ai-agentic-system-builder.md](workflows_ai-agentic-system-builder.md) 的技能組合建議
- Context 管理技能（貫穿整個 Phase 1）

---

## Sprint 1.1: 核心狀態機 (Week 1)

### Sprint 1.1 目標

建立事件驅動的狀態管理系統。

### Sprint 1.1 核心架構 Skills

- **`architect-review`** - 架構審核
- **`architecture-patterns`** - 選擇狀態機設計模式
- **`clean-code`** - 代碼品質標準
- **`python-pro`** - Python 最佳實踐

### Sprint 1.1 Context 管理 Skills

- **`context-fundamentals`** ⭐ - 理解上下文基礎（**必讀**）
- **`context-management-context-save`** - 實作狀態保存機制

### Sprint 1.1 測試 Skills

- **`tdd-workflow`** - 測試驅動開發流程
- **`python-testing-patterns`** - Python 測試模式
- **`systematic-debugging`** - 系統化除錯

### Sprint 1.1 主要交付物

- `src/arkhon_rheo/core/state.py` - 不可變狀態容器
- `src/arkhon_rheo/core/step.py` - 推理步驟定義
- `src/arkhon_rheo/core/graph.py` - 狀態圖執行引擎
- `src/arkhon_rheo/core/context.py` - 上下文管理器

### Sprint 1.1 退出標準

- ✅ 所有測試通過 (`pytest tests/core/`)
- ✅ 90%+ 代碼覆蓋率
- ✅ ty 通過
- ✅ 可執行簡單的 thought → action → observation 循環

---

## Sprint 1.2: 節點實作 (Week 2)

### Sprint 1.2 目標

實作 6 個 ReAct 節點類型。

### Sprint 1.2 核心實作 Skills

- **`software-architecture`** - 軟體架構實作
- **`python-pro`** - Python OOP 實作
- **`clean-code`** - 代碼品質控制

### Sprint 1.2 Context 管理 Skills

- **`context-window-management`** ⭐ - 管理 LLM 上下文視窗
- **`context-optimization`** - 壓縮和快取策略

### Sprint 1.2 AI 整合 Skills

- **`ai-engineer`** - LLM 整合最佳實踐
- **`llm-app-patterns`** - LLM 應用模式

### Sprint 1.2 測試 Skills

- **`tdd-workflow`** - TDD 持續循環
- **`python-testing-patterns`** - 節點單元測試

### Sprint 1.2 主要交付物

- `src/arkhon_rheo/nodes/base.py` - 節點基礎類別
- `src/arkhon_rheo/nodes/thought_node.py` - 思考節點（LLM 整合）
- `src/arkhon_rheo/nodes/action_node.py` - 動作節點（工具執行）
- `src/arkhon_rheo/nodes/observation_node.py` - 觀察節點
- `src/arkhon_rheo/nodes/validate_node.py` - 驗證節點
- `src/arkhon_rheo/nodes/commit_node.py` - 提交節點

### Sprint 1.2 退出標準

- ✅ 所有 6 個節點實作 `BaseNode`
- ✅ 整合測試：Thought → Validate → Action → Observation → Commit 循環
- ✅ 錯誤情境處理完善
- ✅ 結構化日誌記錄

---

## Sprint 1.3: 工具整合 (Week 3)

### Sprint 1.3 目標

建立可插拔的工具系統和工具註冊表。

### Sprint 1.3 工具設計 Skills

- **`agent-tool-builder`** ⭐⭐ - **工具描述比實作更重要**
- **`tool-design`** - 架構縮減模式
- **`mcp-builder`** - 符合 MCP 標準的工具伺服器

### Sprint 1.3 Context 管理 Skills

- **`context-manager`** ⭐ - 動態上下文管理（整合多個工具的上下文）

### Sprint 1.3 API 整合 Skills

- **`api-patterns`** - API 設計模式
- **`api-design-principles`** - API 設計原則
- **`context7-auto-research`** - 自動獲取最新文件（用於工具開發者文件）

### Sprint 1.3 測試 Skills

- **`tdd-workflow`** - TDD 持續循環
- **`python-testing-patterns`** - 工具測試模式

### Sprint 1.3 主要交付物

- `src/arkhon_rheo/tools/base.py` - Tool 基礎類別
- `src/arkhon_rheo/tools/registry.py` - 工具註冊表（單例模式）
- `src/arkhon_rheo/tools/builtin/search.py` - 網頁搜尋工具
- `src/arkhon_rheo/tools/builtin/calculator.py` - 計算器工具
- `src/arkhon_rheo/tools/builtin/file_ops.py` - 檔案操作工具

### Sprint 1.3 退出標準

- ✅ ToolRegistry 可以發現所有內建工具
- ✅ 每個工具都有有效的 JSON Schema
- ✅ 整合測試：代理依序使用 search → calculator → file_ops
- ✅ 工具文件自動生成

---

## Sprint 1.4: YAML 配置與驗證 (Week 4)

### Sprint 1.4 目標

實作 YAML 配置系統和規則引擎。

### Sprint 1.4 配置管理 Skills

- **`deployment-validation-config-validate`** - 配置驗證
- **`python-patterns`** - Pydantic 模型設計

### Sprint 1.4 Context 管理 Skills

- **`context-management-context-restore`** ⭐ - 從配置恢復上下文狀態
- **`context-compression`** - 配置壓縮策略

### Sprint 1.4 規則引擎 Skills

- **`architecture-patterns`** - 規則引擎設計模式

### Sprint 1.4 安全性 Skills

- **`backend-security-coder`** - 後端安全實踐（secrets 管理）

### Sprint 1.4 測試 Skills

- **`tdd-workflow`** - TDD 持續循環
- **`python-testing-patterns`** - 配置和規則測試

### Sprint 1.4 主要交付物

- `src/arkhon_rheo/config/schema.py` - Pydantic 配置模型
- `src/arkhon_rheo/config/loader.py` - YAML 載入器
- `config/templates/default.yaml` - 預設配置範本
- `src/arkhon_rheo/rules/base.py` - Rule 抽象類別
- `src/arkhon_rheo/rules/rule_engine.py` - 規則引擎
- 內建規則：`MaxDepthRule`, `ForbidGuessingRule`, `CostLimitRule`

### Sprint 1.4 退出標準

- ✅ 從 YAML 載入的配置通過 Pydantic 驗證
- ✅ 無效配置會產生清晰的錯誤訊息
- ✅ Secrets 永不被記錄或提交
- ✅ 所有內建規則都經過測試

---

## Context Skills 整體策略

在 Phase 1，Context 技能的整合策略：

### Week 1: 基礎建立

- 使用 **`context-fundamentals`** 建立 `ContextManager` 基礎類別
- 實作 trace ID 生成和 metadata 管理

### Week 2: LLM 整合

- 使用 **`context-window-management`** 整合 LLM 上下文管理
- 實作 token 計數和上下文視窗滑動機制

### Week 3: 工具上下文

- 使用 **`context-manager`** 處理工具調用的上下文傳遞
- 確保工具之間的狀態共享

### Week 4: 配置恢復

- 使用 **`context-management-context-restore`** 實作配置驅動的上下文恢復
- 支援從 checkpoint 恢復執行狀態

---

## 最小可行技能組合 (MVP Skills)

根據 [workflows_ai-agentic-system-builder.md](workflows_ai-agentic-system-builder.md)，Phase 1 MVP 必需技能：

| 技能 | 用途 | 優先級 |
| :--- | :--- | :--- |
| **`ai-agents-architect`** | 總體代理設計 | ⭐⭐⭐ |
| **`python-pro`** | Python 實作 | ⭐⭐⭐ |
| **`agent-tool-builder`** | 工具設計 | ⭐⭐⭐ |
| **`context-manager`** | 記憶體管理 | ⭐⭐⭐ |
| **`tdd-workflow`** | 測試策略 | ⭐⭐⭐ |

---

## Skills 查找指南

### 如何找到技能

所有技能位於 `.agent/skills/` 目錄：

```bash
# 查看所有可用技能
ls .agent/skills/

# 查看特定技能的說明
cat .agent/skills/context-manager/SKILL.md

# 搜尋與關鍵字相關的技能
grep -r "context" .agent/skills/*/SKILL.md
```

### 技能命名規則

- `context-*`: Context 管理相關技能
- `*-pro`: 語言專家技能（如 `python-pro`, `typescript-pro`）
- `*-architect`: 架構設計技能
- `*-patterns`: 設計模式技能
- `tdd-*`: 測試驅動開發技能

---

## 測試覆蓋率目標

Phase 1 統一測試標準：**90%+** （所有組件）

```bash
# 檢查覆蓋率
pytest --cov=arkhon_rheo --cov-report=html

# 查看詳細報告
open htmlcov/index.html
```

詳細測試策略請參考 [TDD.md](TDD.md)。

---

## 參考資料

### 相關文件

- [ROADMAP.md - Phase 1 詳細計劃](file:///wk2/yaochu/github/arkhon-rheo/docs/vers0.1.0/ROADMAP.md#milestone-1-foundation-phase-1---weeks-1-4)
- [workflows_ai-agentic-system-builder.md](file:///wk2/yaochu/github/arkhon-rheo/docs/vers0.1.0/workflows_ai-agentic-system-builder.md)
- [TDD.md](file:///wk2/yaochu/github/arkhon-rheo/docs/vers0.1.0/TDD.md)
- [DEVGUIDE.md](file:///wk2/yaochu/github/arkhon-rheo/docs/vers0.1.0/DEVGUIDE.md)

### Skills 目錄

- [.agent/skills/](file:///wk2/yaochu/github/arkhon-rheo/.agent/skills/) - 可用技能目錄
- [context-manager](file:///wk2/yaochu/github/arkhon-rheo/.agent/skills/context-manager/SKILL.md)
- [context-fundamentals](file:///wk2/yaochu/github/arkhon-rheo/.agent/skills/context-fundamentals/SKILL.md)
- [agent-tool-builder](file:///wk2/yaochu/github/arkhon-rheo/.agent/skills/agent-tool-builder/SKILL.md)
- [python-pro](file:///wk2/yaochu/github/arkhon-rheo/.agent/skills/python-pro/SKILL.md)

---

**維護者**: Arkhon-Rheo Team  
**最後更新**: 2026-02-16  
**文件版本**: 1.0.0

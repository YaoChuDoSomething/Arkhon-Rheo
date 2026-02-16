---
description: SDLC State Machine Workflow for Complex Features
---

# SDLC State Machine Workflow

完整的軟體開發生命週期（SDLC）工作流程，基於狀態機模式，整合 Arkhon-Rheo Skills 系統。

**適用場景**: 中大型功能開發、架構重構、跨模組整合

---

## 🎯 工作流程配置 (Workflow Configuration)

### 關鍵字注入機制

本工作流程支援**關鍵字注入**，允許根據專案特性動態調整 Skills 推薦、工具鏈選擇和驗證標準。

### 配置範本 (`.agent/workflow-context.yaml`)

```yaml
# 工作流程執行上下文配置
workflow_config:
  # 專案基本資訊
  project:
    name: "${PROJECT_NAME}"           # 例: "user-authentication-system"
    type: "${PROJECT_TYPE}"           # 例: "backend" | "frontend" | "fullstack" | "mobile"
    priority: "${PRIORITY}"           # 例: "High" | "Medium" | "Low"
    
  # 技術堆疊配置
  tech_stack:
    primary_language: "${LANGUAGE}"   # 例: "python" | "typescript" | "go" | "rust"
    framework: "${FRAMEWORK}"         # 例: "django" | "fastapi" | "nextjs" | "react"
    database: "${DATABASE}"           # 例: "postgresql" | "mongodb" | "redis"
    deployment: "${DEPLOYMENT}"       # 例: "kubernetes" | "docker" | "serverless"
    
  # Skills 過濾與推薦
  skill_preferences:
    # 根據語言自動選擇專家 Skills
    language_expert: "${LANGUAGE}-pro" # 自動解析為 "python-pro" 等
    
    # 可選的額外 Skills（會自動附加到推薦清單）
    additional_skills:
      - "${CUSTOM_SKILL_1}"
      - "${CUSTOM_SKILL_2}"
    
    # 排除特定 Skills（若不適用）
    excluded_skills:
      - "${EXCLUDED_SKILL_1}"
      
  # 品質閾值配置
  quality_thresholds:
    test_coverage: ${TEST_COVERAGE:-90}      # 預設 90%
    cyclomatic_complexity: ${MAX_CC:-10}     # 預設 10
    maintainability_index: ${MIN_MI:-65}    # 預設 65
    max_function_lines: ${MAX_LINES:-400}   # 預設 400 行
    
  # 人工審核閘門
  human_gates:
    design_approval: ${REQUIRE_DESIGN_APPROVAL:-true}
    security_review: ${REQUIRE_SECURITY_REVIEW:-true}
    deployment_approval: ${REQUIRE_DEPLOY_APPROVAL:-true}
```

### 使用範例：注入關鍵字

#### 方法 1: 環境變數注入

```bash
# 設定環境變數
export PROJECT_NAME="payment-gateway"
export LANGUAGE="python"
export FRAMEWORK="fastapi"
export TEST_COVERAGE=95

# 執行工作流程（自動讀取環境變數）
arkhon-rheo workflow run \
  --template .agent/workflows/sdlc-state-machine.md \
  --config .agent/workflow-context.yaml \
  --trace-id feature-payment-001
```

#### 方法 2: CLI 參數注入

```bash
arkhon-rheo workflow run \
  --template .agent/workflows/sdlc-state-machine.md \
  --var PROJECT_NAME="user-dashboard" \
  --var LANGUAGE="typescript" \
  --var FRAMEWORK="nextjs" \
  --var DATABASE="postgresql" \
  --trace-id feature-dashboard-001
```

#### 方法 3: Python API 注入

```python
from arkhon_rheo.workflow import WorkflowEngine

# 定義配置注入
workflow_vars = {
    "PROJECT_NAME": "api-gateway",
    "PROJECT_TYPE": "backend",
    "LANGUAGE": "go",
    "FRAMEWORK": "gin",
    "DATABASE": "postgresql",
    "DEPLOYMENT": "kubernetes",
    "TEST_COVERAGE": 95,
    "REQUIRE_DESIGN_APPROVAL": True,
}

# 載入並注入
engine = WorkflowEngine.from_markdown(
    ".agent/workflows/sdlc-state-machine.md",
    context_vars=workflow_vars
)

# 執行（Skills 會自動根據 LANGUAGE 調整）
result = engine.run(initial_state)
```

### 關鍵字解析規則

| 關鍵字 | 解析行為 | 範例 |
| :--- | :--- | :--- |
| `${LANGUAGE}-pro` | 自動匹配語言專家 Skill | `python` → `python-pro` |
| `${FRAMEWORK}` | 框架特定 Skills | `django` → 推薦 `django-pro` |
| `${DATABASE}` | 資料庫 Skills | `postgresql` → 推薦 `database-architect` |
| `${PROJECT_TYPE}` | 前後端分類 | `backend` → 排除前端 Skills |
| `${TEST_COVERAGE:-90}` | 帶預設值 | 未設定時使用 90 |

### 智能 Skills 推薦

工作流程引擎會根據注入的關鍵字，在各 SDLC 狀態**自動調整** Skills 清單：

```yaml
# 範例：當 LANGUAGE="python" 且 FRAMEWORK="django" 時
Implementation 狀態自動推薦:
  - python-pro        # 因為 LANGUAGE=python
  - django-pro        # 因為 FRAMEWORK=django
  - tdd-workflow      # 預設保留
  - clean-code        # 預設保留
  - database-architect # 因為 DATABASE 有設定
```

---

## 概述

本工作流程實作 7 個主要狀態，涵蓋從規劃到監控的完整 SDLC：

```text
Planning → Design → Implementation → Testing → Review → Deployment → Monitoring
```

每個狀態對應特定的 **Skills 組合** 和 **完成標準**，確保開發品質和效率。

---

## 狀態定義

### 1. Planning (研究與規劃)

**目標**: 從需求到可執行規劃

**Entry Conditions**:

- [ ] User Story / Feature Request 已建立
- [ ] Initial context 已提供

**推薦 Skills**:

- `brainstorming` - 創意發想和需求探索
- `concise-planning` - 簡潔計劃生成
- `plan-writing` - 正式計劃文件撰寫
- `architecture` - 架構決策框架
- `product-manager-toolkit` (可選) - 產品需求管理

**工作成果**:

1. **需求規格文件** (`spec.md`)
2. **技術可行性評估**
3. **資源估算** (時間/人力)
4. **風險清單**

**Exit Criteria**:

- [x] Specification 文件完成
- [x] 利害關係人已批准
- [x] 技術風險已識別

**預估時間**: 2-4 天

---

### 2. Design (系統設計)

**目標**: 從規劃到可實作的設計

**Entry Conditions**:

- [ ] Specification 已批准
- [ ] 架構需求已明確

**推薦 Skills**:

- `architect-review` - 架構審核
- `architecture-patterns` - 架構模式選擇
- `architecture-decision-records` - ADR 撰寫
- `design-orchestration` - 設計協調

**條件性 Skills** (根據 `${DATABASE}` 和 `${PROJECT_TYPE}` 自動推薦):

- `database-architect` - 資料庫設計 (當 `${DATABASE}` 有設定時)
- `api-design-principles` - API 設計 (當 `${PROJECT_TYPE}` 為 `backend` 或 `fullstack` 時)

**工作成果**:

1. **設計文件** (`design.md`)
2. **Architecture Decision Records** (ADRs)
3. **資料庫 Schema** (如適用)
4. **API 規格** (如適用)
5. **元件介面定義**

**Exit Criteria**:

- [x] Design Doc 完成且審核通過
- [x] ADRs 已記錄重要決策
- [x] 所有介面已定義
- [x] 無阻塞性設計缺陷

**預估時間**: 1-3 天

---

### 3. Implementation (實作)

**目標**: 高品質代碼實作

**Entry Conditions**:

- [ ] Design 已批准
- [ ] 開發環境已準備

**推薦 Skills**:

- `tdd-workflow` - 測試驅動開發
- `clean-code` - 代碼品質標準
- `software-architecture` - 軟體架構實作

**語言專家 Skills** (自動根據 `${LANGUAGE}` 選擇):

- `${LANGUAGE}-pro` - 語言專家 Skill (例: `python-pro`, `typescript-pro`)
- 備選手動選擇:
  - `python-pro` - Python 專案
  - `typescript-pro` - TypeScript 專案
  - `golang-pro` - Go 專案
  - `rust-pro` - Rust 專案

**框架專家 Skills** (自動根據 `${FRAMEWORK}` 推薦):

- `${FRAMEWORK}-pro` - 框架專家 Skill (例: `django-pro`, `fastapi-pro`, `nextjs-expert`)

**品質保證 Skills**:

- `code-reviewer` - 代碼自我審核
- `production-code-audit` - 生產級稽核
- `systematic-debugging` - 系統化除錯

**工作成果**:

1. **Working Code** (可執行程式碼)
2. **Unit Tests** (單元測試，覆蓋率 >90%)
3. **Integration Tests** (整合測試)
4. **Code Documentation** (程式碼文件)

**Exit Criteria**:

- [x] 所有功能實作完成
- [x] 單元測試通過
- [x] 測試覆蓋率 ≥ 90%
- [x] Linter 檢查通過 (`ruff check .`)
- [x] 類型檢查通過 (`ty check src/`)
- [x] 函數長度 ≤ 400 行（使用 `radon cc src/` 驗證）

**預估時間**: 3-10 天

---

### 4. Testing (測試驗證)

**目標**: 全面測試覆蓋

**Entry Conditions**:

- [ ] 單元測試通過
- [ ] Code 符合品質標準

**推薦 Skills**:

- `test-automator` - 測試自動化
- `e2e-testing-patterns` - E2E 測試模式
- `javascript-testing-patterns` - JS 測試 (如適用)
- `python-testing-patterns` - Python 測試 (如適用)
- `systematic-debugging` - 除錯專家
- `verification-before-completion` - 完成前驗證

**工作成果**:

1. **E2E 測試套件**
2. **效能測試報告**
3. **測試報告** (Coverage Report)
4. **Bug 修復記錄**

**Exit Criteria**:

- [x] E2E 測試通過
- [x] 所有測試場景已覆蓋
- [x] 無阻塞性 Bug
- [x] 效能符合預期

**預估時間**: 1-2 天

---

### 5. Review (代碼審核)

**目標**: 多維度審核確保品質

**Entry Conditions**:

- [ ] 所有測試通過
- [ ] PR 已建立

**推薦 Skills**:

- `code-reviewer` - 綜合代碼審核
- `architect-review` - 架構審核
- `security-auditor` - 安全審核
- `performance-engineer` - 性能審核
- `backend-security-coder` (可選) - 後端安全
- `frontend-security-coder` (可選) - 前端安全

**工作成果**:

1. **Code Review 報告**
2. **Security Scan 報告**
3. **Performance Analysis**
4. **Change Requests** (如有)

**Exit Criteria**:

- [x] PR 已批准
- [x] 無阻塞性問題
- [x] 安全掃描通過
- [x] 效能指標符合標準

**預估時間**: 0.5-1 天

---

### 6. Deployment (部署上線)

**目標**: 安全部署到生產環境

**Entry Conditions**:

- [ ] PR 已合併
- [ ] CI/CD Pipeline 通過

**推薦 Skills**:

- `deployment-engineer` - 部署工程師
- `deployment-procedures` - 部署流程
- `gitops-workflow` - GitOps 工作流程

**基礎設施 Skills** (自動根據 `${DEPLOYMENT}` 選擇):

- `cloud-architect` - 雲端架構 (當 `${DEPLOYMENT}` 為 `serverless` 或通用雲端部署時)
- `kubernetes-architect` - K8s 部署 (當 `${DEPLOYMENT}` 為 `kubernetes` 時)
- `terraform-specialist` - IaC 自動化 (當需要基礎設施管理時)
- `docker-expert` - 容器化 (當 `${DEPLOYMENT}` 為 `docker` 時)

**工作成果**:

1. **Deployment Plan**
2. **Rollback Plan**
3. **Deployment Logs**
4. **Health Check 報告**

**Exit Criteria**:

- [x] 部署到生產環境成功
- [x] Health Checks 通過
- [x] Rollback Plan 已準備
- [x] 監控已啟用

**預估時間**: 0.5-1 天

---

### 7. Monitoring (監控觀察)

**目標**: 持續監控和改進

**Entry Conditions**:

- [ ] 功能已部署
- [ ] 監控已設置

**推薦 Skills**:

- `observability-engineer` - 可觀測性工程
- `incident-responder` - 事件響應
- `performance-engineer` - 性能監控
- `analytics-tracking` (可選) - 分析追蹤

**工作成果**:

1. **監控儀表板**
2. **Alert 配置**
3. **SLI/SLO 定義**
4. **Incident Response Playbook**

**Exit Criteria**:

- [x] 功能穩定運行 7 天
- [x] 無 Critical 級別問題
- [x] SLI 符合 SLO 目標
- [x] 用戶反饋正面

**預估時間**: 持續進行

---

## 狀態轉換規則

### 正常流程

```text
Planning → Design → Implementation → Testing → Review → Deployment → Monitoring → ✓
```

### 異常處理 (Backtracking)

| 當前狀態 | 觸發條件 | 回退目標 | 原因 |
| :--- | :--- | :--- | :--- |
| Design | 設計發現需求不明確 | Planning | 需求缺陷 |
| Implementation | 實作發現設計缺陷 | Design | 設計缺陷 |
| Testing | 測試失敗 | Implementation | 代碼缺陷 |
| Review | 發現重大問題 | Implementation | 品質問題 |
| Deployment | 部署失敗 | Review | 部署風險 |
| Monitoring | 發現生產問題 | Implementation | 生產缺陷 |

---

## 使用範例

### 啟動工作流程 (Python API)

```python
from arkhon_rheo.workflow import WorkflowEngine
from arkhon_rheo.core import ReActState

# 載入工作流程定義
engine = WorkflowEngine.from_markdown(
    ".agent/workflows/sdlc-state-machine.md"
)

# 初始狀態 (Planning)
initial_state = ReActState(
    trace_id="feature-xyz-001",
    current_node="planning",
    metadata={
        "feature_name": "用戶認證系統",
        "user_story": "As a user, I want to login securely...",
        "priority": "High",
    }
)

# 執行工作流程
result = engine.run(initial_state)

# 查看結果
print(f"Final state: {result.current_node}")
print(f"Steps taken: {len(result.steps)}")
```

### 啟動工作流程 (CLI)

```bash
# 使用 arkhon-rheo CLI
arkhon-rheo workflow run \
  --template .agent/workflows/sdlc-state-machine.md \
  --input feature-request.md \
  --trace-id feature-xyz-001

# 查看狀態
arkhon-rheo workflow status --trace-id feature-xyz-001

# 查看歷史
arkhon-rheo workflow history --trace-id feature-xyz-001
```

---

## Skills 自動選擇邏輯

### 基於分類自動推薦

工作流程引擎會根據當前狀態，從 `skill_tags.yaml` 自動推薦 skills：

```yaml
# .agent/workflow-context.yaml
skill_selection:
  planning:
    primary_categories: ["Planning", "Strategy"]
    fallback: ["brainstorming", "concise-planning"]
    
  design:
    primary_categories: ["Architecture", "Design"]
    fallback: ["architect-review", "architecture-patterns"]
    
  implementation:
    primary_categories: ["Coding", "Development"]
    language_aware: true  # 根據語言選擇 Skills
    fallback: ["clean-code", "tdd-workflow"]
```

### 手動覆蓋

你可以在執行時覆蓋推薦的 skills：

```python
result = engine.run(
    initial_state,
    skill_overrides={
        "implementation": ["python-pro", "django-pro", "clean-code"]
    }
)
```

---

## 檢查點和恢復

### 自動檢查點

工作流程在每個狀態轉換後自動儲存檢查點：

```python
# 配置檢查點
engine = WorkflowEngine.from_markdown(
    ".agent/workflows/sdlc-state-machine.md",
    checkpoint_config={
        "enabled": True,
        "storage": "sqlite",  # 或 "postgres"
        "interval": 1,  # 每個狀態轉換後儲存
        "retention_days": 30,
    }
)
```

### 恢復執行

```python
# 從檢查點恢復
state = engine.restore_checkpoint(trace_id="feature-xyz-001")
result = engine.run(state)
```

---

## 人工審核閘門 (HITL)

### 啟用人工審核

在關鍵狀態設置人工審核閘門：

```python
def approval_gate(state: ReActState) -> dict:
    """在 Design → Implementation 轉換前需要人工批准."""
    if state.current_node == "design":
        print(f"請審核設計文件: {state.metadata['design_doc']}")
        decision = input("批准? (yes/no/rollback): ")
        
        if decision == "rollback":
            return {"action": "rollback", "target_step": 0}
        elif decision == "no":
            return {"action": "abort"}
        else:
            return {"action": "resume"}
    
    return {"action": "resume"}

# 執行時提供 interrupt function
result = engine.run(initial_state, interrupt_fn=approval_gate)
```

---

## 與現有系統整合

### 整合 ROADMAP.md

本工作流程對應 `docs/ROADMAP.md` 的：

- **Phase 1**: Foundation ⟺ Implementation 狀態
- **Phase 2**: Multi-Agent ⟺ Planning + Design 狀態
- **Phase 3**: Memory ⟺ Implementation 狀態
- **Phase 4**: Package ⟺ Deployment 狀態

### 整合 STATE_MACHINE.md

每個 SDLC 狀態內部可以包含 `docs/STATE_MACHINE.md` 定義的 ReAct 循環：

```text
SDLC State: Implementation
│
└─> ReAct Loop: Thought → Validate → Action → Observation → Commit
    (每個功能子任務執行一次 ReAct 循環)
```

---

## OOP 規範檢查

在 **Implementation** 和 **Review** 狀態自動執行：

```bash
# 在 Implementation Exit Criteria 檢查
radon cc src/ -a -nc  # Cyclomatic Complexity
radon mi src/ -s      # Maintainability Index

# 在 Review 階段自動化檢查
# 工作流程會拒絕 CC > 10 或 MI < 65 的代碼
```

---

## 參考文件

- [WORKFLOW_AUTOMATION.md](../../WORKFLOW_AUTOMATION.md) - 工作流程系統概述
- [DEPENDENCIES.md](../../DEPENDENCIES.md) - 環境依賴
- [docs/ROADMAP.md](../../docs/ROADMAP.md) - 開發路線圖
- [docs/STATE_MACHINE.md](../../docs/STATE_MACHINE.md) - 狀態機設計
- [skill_tags.yaml](../skill_tags.yaml) - Skills 分類

---

**維護者**: Arkhon-Rheo Team  
**最後更新**: 2026-02-15  
**版本**: 1.0.0

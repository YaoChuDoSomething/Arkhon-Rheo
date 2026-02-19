# Skills Manifest for Arkhon-Rheo + Arkhon-Rheo

## 概念整合

**Arkhon-Rheo** (哲學核心規範) ⟺ **Arkhon-Rheo** (OOP 程式碼架構)

- **專案名稱**: Arkhon-Rheo
- **核心類別**: Arkhon-Rheo
- **定位**: 獨立臨時外掛/插件 (不整合 DLAMP/Hydra)
- **技術規格**: Python 3.12, 無 GPU 加速需求
- **代理人系統路徑**: src/arkhon-rheo/
- **執行代理人系統進行 [目標專案=DLAMP] 開發指令**: `python src/arkhon-rheo/dev.py`

---

## 技能堆疊配置

根據 Arkhon-Rheo SDLC 六階段,為 Arkhon-Rheo 文檔開發配置以下技能:

### 📋 Phase 1: 規劃與研究 (PLANNING)

**目標**: 定義文檔結構、確立規範一致性

| Skill ID | Skill Name | 用途 |
| :--- | :--- | :--- |
| `doc-coauthoring` | Doc Coauthoring | 結構化文檔撰寫工作流 |
| `concise-planning` | Concise Planning | 生成清晰可執行的檢查清單 |
| `writing-plans` | Writing Plans | 撰寫 implementation_plan.md |
| `brainstorming` | Brainstorming | 設計想法驗證與風險識別 |

**應用**:

- 使用 `doc-coauthoring` 建立文檔協作框架
- 使用 `concise-planning` 生成 task.md 檢查清單
- 使用 `writing-plans` 完成實施計劃

---

### 🏗️ Phase 2: 設計與建模 (DESIGN)

**目標**: 創建架構圖、設計文檔、狀態機規範

| Skill ID | Skill Name | 用途 |
| :--- | :--- | :--- |
| `docs-architect` | Docs Architect | 長篇技術文檔架構 |
| `design-md` | Design MD | 設計文檔最佳實踐 |
| `architecture-patterns` | Architecture Patterns | Clean Architecture / Hexagonal |
| `mermaid-expert` | Mermaid Expert | 架構圖 / 狀態機圖 |
| `software-architecture` | Software Architecture | 質量導向軟體架構 |

**應用**:

- `docs-architect`: 撰寫 SPECIFICATION.md (800-1200 行)
- `design-md`: 撰寫 DESIGN.md, ARCHITECTURE.md
- `mermaid-expert`: 生成狀態轉移圖 (STATE_MACHINE.md)
- `architecture-patterns`: 確保符合 Clean Architecture 原則

---

### 💻 Phase 3: 實作 (IMPLEMENTATION)

**目標**: 生成符合 PEP8 的 Production-ready 代碼範例

| Skill ID | Skill Name | 用途 |
| :--- | :--- | :--- |
| `python-pro` | Python Pro | Python 3.12+ 現代化實踐 |
| `clean-code` | Clean Code | Robert C. Martin 原則 |
| `autonomous-agent-patterns` | Autonomous Agent Patterns | Agent 工具整合模式 |
| `agent-tool-builder` | Agent Tool Builder | Tool Schema / MCP 標準 |

**應用**:

- `python-pro`: 確保所有代碼範例符合 Python 3.12 type hints
- `clean-code`: Code reviews, 變數命名, 函數設計
- `autonomous-agent-patterns`: 權限系統、瀏覽器自動化設計
- `agent-tool-builder`: Tool Registry, JSON Schema 最佳實踐

---

### 🧪 Phase 4: 驗證與測試 (VALIDATION)

**目標**: 驗證文檔完整性、代碼範例正確性

| Skill ID | Skill Name | 用途 |
| :--- | :--- | :--- |
| `test-driven-development` | TDD | TDD 策略文檔 (TDD.md) |
| `python-testing-patterns` | Python Testing Patterns | pytest fixture / mock 模式 |
| `code-reviewer` | Code Reviewer | 代碼品質審查 |

**應用**:

- `test-driven-development`: 撰寫 TDD.md (350-450 行)
- `python-testing-patterns`: 測試模式範例
- `code-reviewer`: 驗證所有代碼範例可執行

---

### 🚀 Phase 5: 部署 (DEPLOYMENT)

**目標**: 完成打包規範、發布文檔

| Skill ID | Skill Name | 用途 |
| :--- | :--- | :--- |
| `uv-package-manager` | UV Package Manager | Python 項目打包 |
| `readme` | README | 更新項目文檔 |
| `development-md` | Development MD | 開發指南 |

**應用**:

- `uv-package-manager`: ROADMAP Phase 4 打包規範
- `readme`: 更新 README.md
- 撰寫 DEVELOPMENT.md (300-400 行)

---

### 📊 Phase 6: 監控與迭代 (MONITORING)

**目標**: 文檔維護、版本更新

| Skill ID | Skill Name | 用途 |
| :--- | :--- | :--- |
| `architect-review` | Architect Review | 架構一致性審查 |
| `design-orchestration` | Design Orchestration | 多文檔一致性協調 |

**應用**:

- `architect-review`: 最終架構審查
- `design-orchestration`: 確保 9 份文檔間的一致性

---

## 跨階段技能 (Cross-Cutting)

| Skill ID | 用途 | 何時使用 |
| :--- | :--- | :--- |
| `multi-agent-brainstorming` | 高風險設計決策的多代理審查 | Phase 2 重大架構決策 |
| `langgraph` | LangGraph 等價性分析 | SPECIFICATION.md LangGraph 對照章節 |
| `agent-memory-systems` | Memory/VectorStore 架構設計 | ROADMAP Phase 3 |
| `agent-orchestration-multi-agent-optimize` | Multi-Agent 優化 | ROADMAP Phase 2 |

---

## 技能使用原則

### 1. **分階段激活**

- PLANNING 階段: 激活 PM/Governance 技能
- DESIGN 階段: 激活架構設計技能
- IMPLEMENTATION 階段: 激活代碼實踐技能

### 2. **遵循 SDLC Complex 規範**

- 每個階段完成後使用 `architect-review` 進行 Gate Check
- 使用 `doc-coauthoring` 建立 HITL (人機協作) 檢查點

### 3. **避免技能衝突**

- 不同時激活 `autonomous-agent-patterns` 和 `autonomous-agents`
  (前者是工程實作,後者是哲學指導)

---

## 預期產出對照

| 文檔 | 主要技能 | 預估行數 |
| :--- | :--- | :--- |
| SPECIFICATION.md | `docs-architect`, `python-pro` | 800-1200 |
| ROADMAP.md | `concise-planning`, `writing-plans` | 400-600 |
| DESIGN.md | `design-md`, `mermaid-expert` | 600-800 |
| ARCHITECTURE.md | `architecture-patterns`, `software-architecture` | 400-500 |
| DEVELOPMENT.md | `clean-code`, `uv-package-manager` | 300-400 |
| TDD.md | `test-driven-development` | 350-450 |
| STATE_MACHINE.md | `mermaid-expert`, `autonomous-agent-patterns` | 300-400 |
| AGENT_ROLES_ACL.md | `agent-orchestration-multi-agent-optimize` | 250-350 |
| RULES.md | `agent-tool-builder` | 250-350 |

**總計**: 3650-4650 行

# ROADMAP V1.0.0

這是一份基於 Arkhon-Rheo 現有架構文件（S0-S6 狀態機、憲法、TDD 工程化）所規劃的 **開發藍圖（Roadmap）**。

根據您的架構深度與自動化野心，**預計足夠釋出 Release (v1.0) 的產品將落在【PHASE 4】完成之後。**
雖然【PHASE 3】已具備完整功能（MVP），但缺乏 ArkhonFlow 核心承諾的「絕對治理（Governance）」與「不可逆狀態鎖」，因此不建議作為正式 Release。

---

## 📅 Arkhon-Rheo Project Roadmap

## 🚀 Release Target: Post-Phase 4
>
> 只有在 ACL (存取控制) 與 State Cryptography (狀態簽章) 完成後，系統才具備「不需人類看管也能安全運作」的能力。

---

## [PHASE 1] The Bedrock: Infrastructure & Connectivity

**階段目標**：建立專案地基，打通 LLM (Gemma 3) 與 LangGraph 的連接，確保工具鏈 (UV, MCP) 運作正常。

- **[FEAT-01] Project Initialization & Dependency Management**
  - [TASK] 使用 `uv init` 初始化專案，建立標準 `src/arkhonflow` 結構。
  - [TASK] 設定 `pyproject.toml`，鎖定 python >= 3.12。
  - [TASK] 設定 `uv` 虛擬環境與 `pytest` 基礎配置。
  - [TASK] 實作 `logging` 模組，確保所有 stdout 都有結構化輸出。

- **[FEAT-02] LLM Integration (Gemma 3 / Ollama)**
  - [TASK] 實作 `LLMProvider` 介面，支援 `ollama-python` 連接本地 Gemma 3。
  - [TASK] 實作 `ToolBinder`，將 Python function 轉換為 Gemma 可用的 tool schema。
  - [TASK] 整合 `context7` MCP Server，測試自動化依賴查詢功能。

- **[FEAT-03] LangGraph Skeleton**
  - [TASK] 建立最簡單的 `StateGraph` (Hello World)，測試節點間的 state 傳遞。
  - [TASK] 設定 LangSmith 追蹤，確保可觀測性 (Observability)。

---

## [PHASE 2] The Engine: S0-S6 State Machine Implementation

**階段目標**：將 `AGENT_WORKFLOWS.md` 中的核心邏輯程式碼化，**這是本專案與一般 Agent 系統最大的分水嶺**。

- **[FEAT-04] State Definition & Persistence**
  - [TASK] 定義 `ArkhonState` Pydantic models (包含 `current_state`, `artifacts`, `history`)。
  - [TASK] 實作 S0-S6 七大狀態的 Enum 與各狀態的資料結構 (Schema)。
  - [TASK] 實作 `StateStore` (基於 JSON/File)，支援 append-only 寫入。

- **[FEAT-05] The Core Loop (Graph Construction)**
  - [TASK] 在 `graph.py` 中硬編碼 S0→S6 的標準轉移路徑。
  - [TASK] 實作「條件邊 (Conditional Edge)」，處理 `S5(Validation)` 失敗時的回退邏輯。
  - [TASK] 定義 `StatePacket` 交換格式，作為 Agent 間唯一的溝通協議。

- **[FEAT-06] Basic Agents (Role Implementation)**
  - [TASK] 實作 `Designer` (S0→S1)：負責將自然語言轉為 spec。
  - [TASK] 實作 `CodeWritter` (S3)：負責生成 code 與 test。
  - [TASK] 實作 `StateValidater` (S5)：負責執行測試並回傳 Boolean 結果。

---

## [PHASE 3] The Brain: APE & TDD Engineering (Alpha Release / MVP)

**階段目標**：導入 `TESTS_PLANNING.md` 與 `APE_ART.md`，讓 AI 寫出「能通過測試」的程式碼。**此階段完成後，系統具備內部使用的價值。**

- **[FEAT-07] Automated Prompt Engineering (APE)**
  - [TASK] 實作 `ReviewDesigner` (S2)，負責讀取設計並生成 `checklist.yaml`。
  - [TASK] 實作 Context Packing 機制，將 Git diff 與相關檔案打包進 Prompt。
  - [TASK] 建立 Meta-Prompt 模板庫，針對不同任務動態組裝 Prompt。

- **[FEAT-08] TDD Enforcement System**
  - [TASK] 實作「測試矩陣生成器」 (依照 `TESTS_PLANNING.md` 流程)。
  - [TASK] 強制實作順序：`CodeWritter` 必須先產出 `test_*.py` 才能產出 `*.py`。
  - [TASK] 整合 `pytest` 執行器，將測試結果 (STDOUT/STDERR) 解析為結構化證據 (Evidence)。

- **[FEAT-09] Sandbox Execution**
  - [TASK] 建立安全的程式碼執行環境 (Docker 或受限 subprocess)。
  - [TASK] 實作自動修復迴圈 (Self-Healing Loop)：當測試失敗時，將錯誤訊息餵回給 `CodeWritter`。

---

## [PHASE 4] The Law: Constitution & Governance (v1.0 Release Ready)

**階段目標**：實作 `CONSTITUTIONS.md` 與 ACL，防止 Agent 幻覺導致的破壞，確保系統「安全、可信」。

- **[FEAT-10] Access Control Layer (ACL)**
  - [TASK] 實作 `acl_engine.py`，攔截所有檔案寫入請求。
  - [TASK] 定義 `constitution.yaml`，設定哪些 Agent 可以寫入哪些路徑 (e.g., `Designer` 不可寫 `src/*`)。
  - [TASK] 實作 `RepoLock`，只有在 S5 驗證通過後，才解鎖 Git Commit 權限。

- **[FEAT-11] Cryptographic Integrity**
  - [TASK] 實作 Artifact Hashing (對 code/tests 計算 SHA256)。
  - [TASK] 實作 `StateSignature`，由 `StateValidater` 對通過的狀態進行數位簽章。
  - [TASK] 建立 `project_state.yaml` (State Canon)，作為專案唯一真理來源。

- **[FEAT-12] Non-Standard Flows**
  - [TASK] 實作 `Hotfix` 流程 (跳過 S1 設計，但保留 S5 驗證)。
  - [TASK] 實作 `Refactor` 流程 (保留 Acceptance 測試，重寫 Implementation)。
  - [TASK] 實作 `GovernorAgent`，負責判斷並授權切換至非標準流程。

---

## [PHASE 5] Optimization: Self-Evolution (Future / v1.1+)

- **[FEAT-13] Knowledge Distillation** (將成功的 history 存入 Vector DB 供未來參考)。
- **[FEAT-14] Parallel Execution** (同時跑多個 Implementation 提案並擇優)。

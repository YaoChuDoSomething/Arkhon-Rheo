# RULES for Arkhon-Rheo Project 實現自動化SOP式的AI代理開發流程

## Core Development Philosophy | 核心開發理念

* **Primary Skills**: Utilize `@tdd-workflow` and `@workflow-automation` as the core skills for the development process.
  * **主要技能**：以 `@tdd-workflow` 與 `@workflow-automation` 作為主要開發流程技能。
* **Sequential Reasoning**: Automatically apply `sequential-thinking` when reasoning or complex logic is required.
  * **循序推理**：需要進行推理時，自動套用 `sequential-thinking` 技能。

## Toolchain & Environment | 工具鏈與環境規範

* **Package Management**: This is a `UV` managed Python project (`python=3.12`).
  * **套件管理**：本專案為 `UV` 管理的 Python 專案 (`python=3.12`)。使用@uv-package-manager。
  * **Commands**: Use `uv add [DEPENDENCIES]` to manage dependencies and `uv pip install --editable .` for local development. `pyproject.toml` should be managed via `uv` commands to verify dependencies and minimize manual edits. No extra `PYTHONPATH` is needed.
  * **指令規範**：使用 `uv add [DEPENDENCIES]` 管理依賴，並使用 `uv pip install --editable .` 進行本地開發安裝。`pyproject.toml` 應透過 `uv` 指令維護以確保依賴正確性並減少手動編輯，因此無需額外設定 `PYTHONPATH`。
* **Strict Tool Enforcement**: `micromamba` and `mypy` are **prohibited**. You MUST use `uv`, `uvx`, `pytest`, `pytest-cov`, `ruff`, `ty`, and `radon`.
  * **強制工具**：嚴禁使用 `micromamba` 與 `mypy`。必須使用 `uv`、`uvx`、`pytest`、`pytest-cov`、`ruff`、`ty` 與 `radon`。
* **IDE Integration**: The IDE should automatically recognize the default `uv` virtual environment.
  * **IDE 整合**：IDE 應自動識別 `uv` 建立的預設虛擬環境。
* **Automatic Testing**：已經整合成腳本，除了測試`pytest`之外，還包含`ruff check`, `ty check`, `radon cc`。

## Code Quality & Workflow | 程式碼品質與工作流

* **Linting Policy**:
  * **Markdown**: Linting must be performed **immediately** after writing any Markdown document.
  * **Markdown 檢查**：Markdown 文件撰寫完成後，必須「立即」執行 Linting 檢查。
  * **Python**: Python source files must undergo linting before the completion of any sprint task.
  * **Python 檢查**：Python 程式碼必須在 Sprint 任務結束前完成 Linting 檢查。
  * Using skills @lint-and-validate 技能。
* **Version Control**: Commit appropriately and frequently. **Push** to the remote repository upon the completion of each **Phase**.
  * **版本控制**：適時進行 Commit。每一個階段 (Phase) 完成時務必執行 Push。
  * 本專案根目錄的狀態直接等於 main 分支的檔案結構。
* **Project Structure**: Follow the standard Python project directory structure, with `main.py` serving as the entry script.
  * **專案結構**：遵循標準 Python 專案目錄結構，並以 `main.py` 作為入口腳本。

## Architecture & Agent Design | 架構與代理人設計

* **Framework Stack**: Adopt the `langchain` ecosystem integrating `google-genai`. This includes `langchain`, `langgraph`, and `langsmith` for the information flow.
  * **技術堆疊**：採用 `langchain` 生態系整合 `google-genai`。資訊流傳遞使用 `langchain`、`langgraph` 與 `langsmith`。
* **Context Awareness**: When starting a coding task, automatically use the `@context7-auto-research` skill to query dependency versions based on `pyproject.toml` or `uv.lock`.
  * **上下文感知**：啟動開發任務時，自動使用 `@context7-auto-research` 技能依據 `pyproject.toml` 或 `uv.lock` 查詢依賴版本，並查找函式庫中的程式碼，或是查找文件中的使用範例。
* **Project Definition**: Clearly distinguish between the **Development Tool Project** (Arkhon-Rheo) and the **Target Project** (DEV-TARGET).
  * **專案定義**：明確區分「開發工具專案」（本專案 Arkhon-Rheo）與「被開發專案」（DEV-TARGET）。
* **Agent Governance**: Implement `Agent-Decision` or `Agent-Governance` mechanisms.
  * **代理人治理**：實作 `Agent-Decision`（決策）或 `Agent-Governance`（治理）機制。
* **MCP Integration**: Support Agents using MCP tools. Alternatively, use `repomix` with the `--mcp` option to translate rules into `xml` or `markdown` format for MCP mounting.
  * **MCP 整合**：支援代理人使用 MCP 工具；或利用 `repomix` 搭配 `--mcp` 選項，將規則轉譯為 `xml` 或 `markdown` 格式後以 MCP 掛載。

## 開發流程與順序

將下列與軟體開發相關的工項，依照執行順序編號，亦可以加入不在下列的工項，。

### Waterfall (傳統瀑布式開發)

**核心邏輯：** 線性流程，強調前期詳盡的規劃與設計，編碼在後段，文件與測試往往在最後才補齊。

01. **b. 計畫撰寫** (專案啟動，定義範圍)
02. **h. 製作開發路線圖** (依據計畫排定長期的甘特圖或里程碑)
03. **c. 文件規劃** (決定要產出哪些規格書)
04. **l. 文件設計** (設計規格書的格式與大綱)
05. **d. 架構設計** (系統分析與細部設計，產出 SD 文件)
06. **f. 測試方法** (依據設計撰寫測試計畫書)
07. **g. 測試樣態** (撰寫詳細測試案例 Test Cases)
08. **j. 版本控制** (架設 Server，準備開發環境)
09. **e. 程式撰寫** (按圖施工)
10. **i. 執行腳本撰寫** (撰寫編譯或部署腳本)
11. **m. 文件開發** (補齊操作手冊與系統說明)
12. **n. 專案程式碼與專案文件對齊** (檢查程式是否符合當初的規格)
13. **a. 撰寫 README** (最後打包，說明專案如何安裝)
14. **k. 專案審查** (驗收交付)

---

### Agile (敏捷式開發)

**核心邏輯：** 迭代循環 (Sprints)。README 與版本控制前置（為了協作），文件與測試隨程式碼同步產出，強調「可用的軟體」勝過「詳盡的文件」。

01. **b. 計畫撰寫** (確立願景與 Product Backlog)
02. **h. 製作開發路線圖** (規劃 Release Plan，但保持彈性)
03. **j. 版本控制** (建立 Repository 與 Branch 策略)
04. **a. 撰寫 README** (願景先行，讓團隊知道如何開始)
05. **c. 文件規劃** (定義 DoD - Definition of Done 需要哪些文件)
06. **d. 架構設計** (足夠的設計即可，不必完美)
07. **f. 測試方法** (定義測試策略與自動化框架)
08. **g. 測試樣態** (針對該次 Sprint 的 Story 設計案例)
09. **e. 程式撰寫** (實作功能)
10. **i. 執行腳本撰寫** (同步建立 CI/CD 自動化腳本)
11. **m. 文件開發** (隨功能釋出同步更新文件)
12. **n. 專案程式碼與專案文件對齊** (在 Sprint 結束前確認一致)
13. **k. 專案審查** (Sprint Review / Demo)
14. **l. 文件設計** (若有需要，於回顧後優化文件結構)

---

### Critic-Supervisor (架構師/監工視角)

**核心邏輯：** 這是**「修正後的最佳實務」**。強調 **RDD (README Driven Development)**，並將測試與腳本視為基礎建設優先處理，解決「文件過期」與「測試不足」的常見痛點。

01. **[新增] 需求分析** (先確認做對的事情，再開始計畫)
02. **b. 計畫撰寫** (資源與時程確認)
03. **h. 製作開發路線圖** (確認階段性目標)
04. **j. 版本控制** (一切的基礎)
05. **a. 撰寫 README** (最重要的步驟！先寫好「如何使用」，作為開發的指引)
06. **f. 測試方法** (先決定怎麼測，才能決定怎麼寫)
07. **d. 架構設計** (模組化設計)
08. **i. 執行腳本撰寫** (先寫好 Build/Deploy 流程，確保開發環境一致)
09. **g. 測試樣態** (列出 Edge Cases)
10. **e. 程式撰寫** (實作邏輯)
11. **m. 文件開發** (推薦使用 Code-as-Docs 工具自動生成)
12. **n. 專案程式碼與專案文件對齊** (利用 Linter 或 CI 工具自動檢查)
13. **c. 文件規劃** & **l. 文件設計** (這兩項應融入日常，而非獨立階段，故排後段作為整理)
14. **k. 專案審查** (Code Review + QA 驗收)

#### 監工的關鍵筆記：

* **README 的位置**：在 Waterfall 裡 README 是最後寫的廢紙；在高品質專案裡，README 是第 1 個被寫下的程式碼 (Documentation First)。
* **測試的順序**：先有 **f (方法)** 與 **g (樣態)**，才有 **e (程式)**。這能避免「為了讓測試通過而寫測試」的無效工時。
* **缺漏補充**：此清單缺少了 **「CI/CD Pipeline 建置」** 與 **「安全性掃描」**，建議將 `i. 執行腳本撰寫` 擴大解釋為包含自動化維運工程。


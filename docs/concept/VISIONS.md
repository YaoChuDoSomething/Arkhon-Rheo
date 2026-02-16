# VISION

這是一個非常清晰的視覺化請求。根據您提供的 `IMPLEMENTATION_GUIDE.md`（以下簡稱 SPEC），我們可以將專案結構分為「Phase 0 初始化完成」與「Phase 8 全面完工」兩個階段。
這裡使用標準的 ASCII Tree 格式來繪製，並標註了 SPEC 中提到的關鍵檔案。

---

## 1. 尚未開發前的目錄架構 (Phase 0 完成後)

這是執行完 SPEC 中 **Phase 0: Project Initialization** 所有指令（`uv init`, `mkdir`, `touch`）後的狀態。此時只有骨架，沒有核心邏輯。

```text
arkhon-rheo/                  # [專案根目錄]
├── .git/                     # Git 版控資料夾
├── .venv/                    # Python 虛擬環境 (由 uv sync 產生)
├── arkhon_rheo/              # [主要 Python 套件目錄]
│   ├── __init__.py           # 套件入口 (目前為空)
│   ├── cli/                  # (空資料夾) 用於存放 CLI 工具
│   ├── config/               # (空資料夾) 用於存放設定載入器
│   ├── core/                 # (空資料夾) 用於核心狀態機
│   ├── memory/               # (空資料夾) 用於記憶體管理
│   ├── nodes/                # (空資料夾) 用於執行節點
│   ├── rules/                # (空資料夾) 用於規則引擎
│   ├── runtime/              # (空資料夾) 用於執行時與 Checkpoint
│   └── tools/                # (空資料夾) 用於工具註冊
├── tests/                    # [測試目錄]
│   ├── e2e/                  # 端對端測試
│   ├── integration/          # 整合測試
│   └── unit/                 # 單元測試
├── .gitignore                # Git 忽略清單
├── .python-version           # 指定 Python 版本 (如 3.12)
├── pyproject.toml            # [核心設定檔] (uv, ruff, mypy, pytest 設定)
├── uv.lock                   # 鎖定依賴版本
└── README.md                 # 專案說明文件
```

---

## 2. 完成開發的目錄架構 (Phase 8 完成後)

這是執行完 **Phase 1 到 Phase 8** 所有開發步驟後的最終狀態。包含了 SPEC 中提到的所有類別實作、設定檔與打包產物。

```text
arkhon-rheo/
├── .git/
├── .venv/
├── arkhon_rheo/                # [核心原始碼]
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py             # (Phase 8) CLI Scaffolding Tool
│   ├── config/
│   │   ├── __init__.py
│   │   └── loader.py           # (Phase 4/Config) Configuration Loader
│   ├── core/
│   │   ├── __init__.py
│   │   ├── state.py            # (Phase 1) ReActState, ReasoningStep
│   │   └── graph.py            # (Phase 1) StateGraph Engine
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── context_window.py   # (Phase 5) Short-term memory
│   │   └── vector_store.py     # (Phase 5) VectorStore Abstraction
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── base.py             # (Phase 2) BaseNode (Template Method)
│   │   ├── thought_node.py     # (Phase 2) LLM Reasoning
│   │   ├── action_node.py      # (Phase 2) Tool Execution
│   │   ├── validate_node.py    # (Phase 2) Rule Checking
│   │   └── ...                 # (ObserveNode, CommitNode)
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── base.py             # (Phase 4) Rule Abstract Class
│   │   └── engine.py           # (Phase 4) RuleEngine & Built-in Rules
│   ├── runtime/
│   │   ├── __init__.py
│   │   └── checkpoint.py       # (Phase 5) CheckpointManager (SQLite)
│   └── tools/
│       ├── __init__.py
│       ├── base.py             # (Phase 3) Tool Base Class & Schema Gen
│       ├── registry.py         # (Phase 3) ToolRegistry
│       └── builtin/            # (Phase 3) 內建工具集
│           ├── __init__.py
│           ├── search.py
│           ├── calculator.py
│           └── file_ops.py
├── config/                     # [外部設定]
│   └── default.yaml            # (Config Guide) 預設 YAML 設定檔
├── dist/                       # (Phase 8) 打包後的 Wheel/Sdist 檔案
├── docs/                       # (Phase 8) API 文件 (Sphinx/MkDocs)
├── examples/                   # (Phase 8) 範例程式碼
│   └── research_agent.py
├── tests/                      # [完整測試套件]
│   ├── unit/                   # (涵蓋 Core, Nodes, Tools, Rules)
│   │   ├── core/
│   │   ├── nodes/
│   │   └── ...
│   ├── integration/            # (Phase 6) 完整 ReAct 循環測試
│   └── e2e/                    # (Phase 7) 真實 LLM 場景測試
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md                   # (Phase 8) 更新後的使用說明
```

## 關鍵差異摘要

1.  **檔案填充**：原本空的 `arkhon_rheo/` 子目錄現在填滿了具體的 `.py` 實作檔（如 `state.py`, `thought_node.py`）。
2.  **設定檔**：新增了 `config/default.yaml` 用於控制 Agent 行為。
3.  **發布產物**：新增了 `dist/`（用於 PyPI 發布）、`docs/`（文件）和 `examples/`（範例）。
4.  **測試完整性**：`tests/` 目錄結構會隨著每個 Phase 的 TDD 流程而擴充，對應到原始碼的每個模組。


# Arkhon-Rheo Class Inventory

完整的類別清單，涵蓋 PHASE 1-4 所有模組

---

## PHASE 1: Foundation Classes (25 個類別)

### Core Module (`arkhon_rheo/core/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `ReActState` | `@dataclass(frozen=True)` | 保存不可變的 ReAct 執行狀態 | Immutable Object | ReasoningStep, StateGraph |
| `ReasoningStep` | `@dataclass(frozen=True)` | 表示單個推理步驟的事件日誌 | Event Sourcing | ReActState |
| `StateGraph` | - | 管理圖結構和執行流程 | State Pattern, Graph | BaseNode, ReActState |
| `ContextManager` | Context Manager Protocol | 管理線程本地狀態和追蹤 ID | Context Manager | ReActState |

### Nodes Module (`arkhon_rheo/nodes/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `BaseNode` | `ABC` | 定義節點執行框架 | Template Method | StateGraph |
| `ThoughtNode` | `BaseNode` | 使用 LLM 生成思維步驟 | Strategy | LLMClient, PromptTemplate |
| `ActionNode` | `BaseNode` | 選擇和執行工具 | Strategy | ToolRegistry, Tool |
| `ObservationNode` | `BaseNode` | 格式化和截斷觀察結果 | Strategy | ReasoningStep |
| `ValidateNode` | `BaseNode` | 執行規則驗證邏輯 | Strategy, Chain of Resp. | RuleEngine |
| `CommitNode` | `BaseNode` | 持久化狀態並轉換循環 | Strategy | ReActState |

### Tools Module (`arkhon_rheo/tools/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `Tool` | `ABC` | 定義工具接口 | Strategy | ToolRegistry |
| `ToolResult` | `@dataclass` | 封裝工具執行結果 | Value Object | Tool |
| `ToolRegistry` | Singleton | 管理工具註冊和發現 | Registry, Singleton | Tool |
| `SearchTool` | `Tool` | Web 搜索功能 | Strategy | External API |
| `CalculatorTool` | `Tool` | 安全數學計算 | Strategy | - |
| `FileOpsTool` | `Tool` | 文件讀寫操作 | Strategy | Filesystem |

### Config Module (`arkhon_rheo/config/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `EngineConfig` | `BaseModel` (Pydantic) | 引擎配置驗證 | Builder | ConfigLoader |
| `LLMConfig` | `BaseModel` | LLM 提供商配置 | Builder | ThoughtNode |
| `ToolConfig` | `BaseModel` | 工具配置驗證 | Builder | ToolRegistry |
| `RuleConfig` | `BaseModel` | 規則引擎配置 | Builder | RuleEngine |
| `ConfigLoader` | - | 載入和合併 YAML 配置 | Builder, Template Method | All Config Classes |

### Rules Module (`arkhon_rheo/rules/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `Rule` | `ABC` | 定義規則接口 | Strategy | RuleEngine |
| `RuleEngine` | - | 順序執行規則集合 | Chain of Responsibility | Rule, ValidateNode |
| `MaxDepthRule` | `Rule` | 防止無限循環 | Strategy | ReActState |
| `ForbidGuessingRule` | `Rule` | 要求置信度閾值 | Strategy | ReasoningStep |
| `CostLimitRule` | `Rule` | 限制 LLM token 花費 | Strategy | LLMClient |

---

## PHASE 2: Multi-Agent Classes (12 個類別)

### Core Module Extensions (`arkhon_rheo/core/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `Agent` | - | 表示單個代理實體 | Agent Pattern | AgentMessage, StateGraph |
| `AgentMessage` | `@dataclass` | 代理間訊息傳遞 | Message | Agent |
| `SharedAgentState` | - | 線程安全的共享狀態 | Shared State, Monitor | Agent, Lock |
| `SubGraph` | - | 支持圖嵌套 | Composite | StateGraph, BaseNode |

### Agents Module (`arkhon_rheo/agents/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `Coordinator` | `Agent` | 任務分解和結果聚合 | Mediator | Specialist, Scheduler |
| `PlanningSpecialist` | `Agent` | 規劃專家代理 | Strategy | Coordinator |
| `CodingSpecialist` | `Agent` | 編碼專家代理 | Strategy | Coordinator |
| `ReviewSpecialist` | `Agent` | 審查專家代理 | Strategy | Coordinator |

### Runtime Module (`arkhon_rheo/runtime/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `Scheduler` | - | 代理任務調度 | Scheduler | Agent, Task |
| `Task` | `@dataclass` | 任務定義和依賴 | Value Object | Scheduler |
| `ExecutionPlan` | - | 並行執行計劃 | Strategy | Scheduler |

---

## PHASE 3: Memory System Classes (11 個類別)

### Memory Module (`arkhon_rheo/memory/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `ContextWindow` | - | 滑動窗口記憶管理 | Sliding Window | ReasoningStep, TokenCounter |
| `Summarization` | - | LLM 驅動的上下文壓縮 | Strategy | LLMClient, ContextWindow |
| `VectorStore` | `ABC` | 向量存儲抽象接口 | Abstract Factory | EmbeddingsClient |
| `PineconeStore` | `VectorStore` | Pinecone 實作 | Strategy | External API |
| `WeaviateStore` | `VectorStore` | Weaviate 實作 | Strategy | External API |
| `EmbeddingsClient` | - | 生成文本嵌入 | Strategy | VectorStore |
| `RetrievalStrategy` | `ABC` | 檢索策略接口 | Strategy | VectorStore |
| `SemanticSearch` | `RetrievalStrategy` | 語義搜索 | Strategy | VectorStore |
| `HybridSearch` | `RetrievalStrategy` | 混合搜索 | Strategy | VectorStore, KeywordSearch |

### Runtime Module Extensions (`arkhon_rheo/runtime/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `CheckpointManager` | - | 管理狀態檢查點 | Memento | ReActState, SQLite |
| `RollbackManager` | - | 狀態回滾機制 | Memento, Command | CheckpointManager, ReActState |

---

## PHASE 4: Framework Release Classes (7 個類別)

### CLI Module (`arkhon_rheo/cli/`)

| 類別名稱 | 基類/協議 | 主要責任 | 設計模式 | 協作者 |
|:---|:---|:---|:---|:---|
| `CLI` | - | 命令行接口主類 | Command | All Commands |
| `InitCommand` | `Command` | 初始化項目 | Command | ProjectScaffolder |
| `RunCommand` | `Command` | 執行 ReAct 循環 | Command | StateGraph, ConfigLoader |
| `MigrateCommand` | `Command` | 遷移 LangGraph 項目 | Command | MigrationTool |
| `ProjectScaffolder` | - | 生成項目模板 | Template Method | TemplateRenderer |
| `ConfigValidator` | - | 驗證配置文件 | Strategy | EngineConfig |
| `MigrationTool` | - | AST 轉換工具 | Visitor | ASTTransformer |

---

## 統計摘要

| Phase | 模組數 | 類別數 | 主要設計模式 |
|:---|:---:|:---:|:---|
| **PHASE 1** | 5 | 25 | Template Method, Strategy, Registry, Chain of Resp. |
| **PHASE 2** | 3 | 12 | Mediator, Composite, Agent, Observer |
| **PHASE 3** | 2 | 11 | Abstract Factory, Memento, Sliding Window |
| **PHASE 4** | 1 | 7 | Command, Template Method, Visitor |
| **總計** | **11** | **55** | **15+ 種設計模式** |

---

## 類別依賴關係層級

```
Layer 5 (CLI)
    ├── CLI
    └── Commands

Layer 4 (Memory)
    ├── VectorStores
    ├── Checkpointing
    └── Context Management

Layer 3 (Agents)
    ├── Multi-Agent System
    └── Scheduler

Layer 2 (Execution)
    ├── Nodes
    ├── Tools
    └── Rules

Layer 1 (Core)
    ├── State
    ├── Graph
    └── Context

Layer 0 (Config)
    └── Configuration Models
```

---

**下一步**: 查看 `methods_properties.md` 了解每個類別的方法和屬性詳情

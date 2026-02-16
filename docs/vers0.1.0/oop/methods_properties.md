# Arkhon-Rheo Methods & Properties Reference

完整的方法、屬性和函數清單，含類型簽名

---

## PHASE 1: Foundation

### Core Module

#### `ReActState` (Dataclass)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 | 預設值 |
|:---|:---|:---|:---|
| `steps` | `list[ReasoningStep]` | 推理步驟歷史 | `field(default_factory=list)` |
| `metadata` | `dict[str, Any]` | 元數據字典 | `field(default_factory=dict)` |
| `trace_id` | `str` | 追蹤 ID | 自動生成 UUID |
| `status` | `Literal["running", "completed", "failed"]` | 執行狀態 | `"running"` |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `add_step` | `(self, step: ReasoningStep)` | `Self` | 添加步驟並返回新狀態 |
| `validate` | `(self)` | `bool` | 驗證狀態一致性 |
| `get_latest_step` | `(self)` | `ReasoningStep \| None` | 獲取最新步驟 |
| `to_dict` | `(self)` | `dict[str, Any]` | 序列化為字典 |

---

#### `ReasoningStep` (Dataclass)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `step_id` | `str` | 步驟唯一 ID |
| `type` | `Literal["thought", "action", "observation"]` | 步驟類型 |
| `content` | `str` | 步驟內容 |
| `tool_name` | `str \| None` | 使用的工具名稱 |
| `tool_input` | `dict[str, Any] \| None` | 工具輸入 |
| `tool_output` | `Any \| None` | 工具輸出 |
| `timestamp` | `datetime` | 時間戳 |
| `metadata` | `dict[str, Any]` | 額外元數據 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `to_event` | `(self)` | `dict[str, Any]` | 轉換為事件日誌格式 |
| `is_action` | `(self)` | `bool` | 是否為 action 步驟 |
| `is_thought` | `(self)` | `bool` | 是否為 thought 步驟 |

---

#### `StateGraph` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `nodes` | `dict[str, BaseNode]` | 節點映射 |
| `edges` | `dict[str, list[str]]` | 邊關係 |
| `entry_point` | `str \| None` | 入口節點名稱 |
| `state` | `ReActState` | 當前狀態 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---| `add_node` | `(self, name: str, node: BaseNode)` | `Self` | 添加節點 |
| `add_edge` | `(self, from_node: str, to_node: str)` | `Self` | 添加邊 |
| `set_entry_point` | `(self, name: str)` | `Self` | 設置入口點 |
| `compile` | `(self)` | `CompiledGraph` | 編譯圖為可執行對象 |
| `invoke` | `(self, input: dict[str, Any])` | `ReActState` | 同步執行圖 |
| `stream` | `(self, input: dict[str, Any])` | `Iterator[ReActState]` | 流式執行圖 |
| `validate_graph` | `(self)` | `bool` | 驗證圖結構合法性 |

---

#### `ContextManager` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `_context` | `ContextVar[dict[str, Any]]` | 線程本地上下文 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `get` | `(self, key: str, default: T = None)` | `T \| None` | 獲取上下文值 |
| `set` | `(self, key: str, value: Any)` | `None` | 設置上下文值 |
| `generate_trace_id` | `()` | `str` | 生成追蹤 ID (靜態方法) |
| `__enter__` | `(self)` | `Self` | 進入上下文管理器 |
| `__exit__` | `(self, ...)` | `None` | 退出上下文管理器 |

---

### Nodes Module

#### `BaseNode` (ABC)

**抽象屬性 (Abstract Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `name` | `str` | 節點名稱 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `run` | `(self, state: ReActState)` | `ReActState` | 執行節點邏輯 (抽象) |
| `before_run` | `(self, state: ReActState)` | `None` | 執行前鉤子 |
| `after_run` | `(self, state: ReActState)` | `None` | 執行後鉤子 |
| `__call__` | `(self, state: ReActState)` | `ReActState` | 可調用接口 |

---

#### `ThoughtNode` (BaseNode)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `llm_client` | `LLMClient` | LLM 客戶端 |
| `prompt_template` | `PromptTemplate` | 提示模板 |
| `token_tracker` | `TokenTracker` | Token 計數器 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `run` | `(self, state: ReActState)` | `ReActState` | 生成思維步驟 |
| `format_prompt` | `(self, state: ReActState)` | `str` | 格式化提示 |
| `parse_response` | `(self, response: str)` | `str` | 解析 LLM 響應 |

---

#### `ActionNode` (BaseNode)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `tool_registry` | `ToolRegistry` | 工具註冊表 |
| `max_retries` | `int` | 最大重試次數 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `run` | `(self, state: ReActState)` | `ReActState` | 執行工具調用 |
| `select_tool` | `(self, thought: str)` | `Tool \| None` | 選擇工具 |
| `execute_tool` | `(self, tool: Tool, input: dict)` | `ToolResult` | 執行工具 |
| `handle_error` | `(self, error: Exception)` | `ToolResult` | 錯誤處理 |

---

#### `ObservationNode` (BaseNode)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `max_length` | `int` | 最大觀察長度 |
| `formatter` | `Callable[[Any], str]` | 格式化函數 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `run` | `(self, state: ReActState)` | `ReActState` | 格式化觀察 |
| `truncate` | `(self, text: str)` | `str` | 截斷文本 |
| `format_result` | `(self, result: ToolResult)` | `str` | 格式化結果 |

---

#### `ValidateNode` (BaseNode)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `rule_engine` | `RuleEngine` | 規則引擎 |
| `auto_retry` | `bool` | 自動重試 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `run` | `(self, state: ReActState)` | `ReActState` | 執行驗證 |
| `collect_violations` | `(self, state: ReActState)` | `list[RuleViolation]` | 收集違規 |
| `format_error_report` | `(self, violations: list)` | `str` | 格式化錯誤報告 |

---

#### `CommitNode` (BaseNode)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `checkpoint_manager` | `CheckpointManager \| None` | 檢查點管理器 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `run` | `(self, state: ReActState)` | `ReActState` | 提交狀態 |
| `persist_state` | `(self, state: ReActState)` | `None` | 持久化狀態 |
| `transition` | `(self, state: ReActState)` | `ReActState` | 狀態轉換 |

---

### Tools Module

#### `Tool` (ABC)

**抽象屬性 (Abstract Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `name` | `str` | 工具名稱 |
| `description` | `str` | 工具描述 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `run` | `(self, **kwargs: Any)` | `ToolResult` | 執行工具 (抽象) |
| `get_schema` | `(self)` | `dict[str, Any]` | 獲取 JSON Schema |
| `validate_input` | `(self, input: dict)` | `bool` | 驗證輸入 |

---

#### `ToolResult` (Dataclass)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `success` | `bool` | 是否成功 |
| `output` | `Any` | 輸出內容 |
| `error` | `str \| None` | 錯誤信息 |
| `metadata` | `dict[str, Any]` | 元數據 |

---

#### `ToolRegistry` (Class, Singleton)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `_tools` | `dict[str, Tool]` | 工具映射 |
| `_instance` | `ToolRegistry \| None` | 單例實例 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `register` | `(self, tool: Tool)` | `None` | 註冊工具 |
| `get` | `(self, name: str)` | `Tool \| None` | 獲取工具 |
| `list_tools` | `(self)` | `list[str]` | 列出所有工具 |
| `discover` | `(cls, package: str)` | `None` | 動態發現工具 (類方法) |

---

### Config Module

#### `EngineConfig` (Pydantic BaseModel)

**屬性 (Fields)**

| 屬性名稱 | 類型 | 說明 | 驗證器 |
|:---|:---|:---|:---|
| `max_iterations` | `int` | 最大迭代次數 | `Field(gt=0, le=100)` |
| `llm` | `LLMConfig` | LLM 配置 | - |
| `tools` | `list[ToolConfig]` | 工具配置列表 | - |
| `rules` | `list[RuleConfig]` | 規則配置列表 | - |
| `debug` | `bool` | 調試模式 | `Field(default=False)` |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `validate_llm_config` | `(cls, v: LLMConfig)` | `LLMConfig` | 驗證器 (validator) |
| `to_yaml` | `(self)` | `str` | 序列化為 YAML |

---

#### `LLMConfig` (Pydantic BaseModel)

**屬性 (Fields)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `provider` | `Literal["openai", "anthropic", "google"]` | LLM 提供商 |
| `model` | `str` | 模型名稱 |
| `api_key` | `SecretStr` | API 密鑰 |
| `temperature` | `float` | 溫度參數 |
| `max_tokens` | `int` | 最大 token 數 |

---

#### `ConfigLoader` (Class)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `load_yaml` | `(cls, path: Path)` | `dict[str, Any]` | 載入 YAML (類方法) |
| `merge_configs` | `(cls, *configs: dict)` | `dict[str, Any]` | 合併配置 (類方法) |
| `expand_env_vars` | `(cls, config: dict)` | `dict[str, Any]` | 擴展環境變量 (類方法) |
| `load` | `(cls, path: Path)` | `EngineConfig` | 載入並驗證配置 (類方法) |

---

### Rules Module

#### `Rule` (ABC)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `evaluate` | `(self, state: ReActState)` | `RuleViolation \| None` | 評估規則 (抽象) |
| `name` | `(self)` | `str` | 規則名稱 (屬性) |

---

#### `RuleEngine` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `rules` | `list[Rule]` | 規則列表 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `add_rule` | `(self, rule: Rule)` | `Self` | 添加規則 |
| `execute` | `(self, state: ReActState)` | `list[RuleViolation]` | 執行所有規則 |
| `execute_until_violation` | `(self, state: ReActState)` | `RuleViolation \| None` | 執行直到違規 |

---

#### `RuleViolation` (Dataclass)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `rule_name` | `str` | 規則名稱 |
| `message` | `str` | 違規信息 |
| `severity` | `Literal["error", "warning"]` | 嚴重程度 |
| `step_id` | `str \| None` | 相關步驟 ID |

---

## PHASE 2: Multi-Agent System

### Core Module Extensions

#### `Agent` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `agent_id` | `str` | 代理 ID |
| `role` | `str` | 代理角色 |
| `graph` | `StateGraph` | 代理執行圖 |
| `message_queue` | `Queue[AgentMessage]` | 訊息隊列 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `send_message` | `(self, to: str, msg: AgentMessage)` | `None` | 發送訊息 |
| `receive_message` | `(self, timeout: float = None)` | `AgentMessage \| None` | 接收訊息 |
| `process_message` | `(self, msg: AgentMessage)` | `AgentMessage` | 處理訊息 |
| `run` | `(self, input: dict)` | `ReActState` | 執行代理 |

---

#### `AgentMessage` (Dataclass)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `message_id` | `str` | 訊息 ID |
| `from_agent` | `str` | 發送者 ID |
| `to_agent` | `str` | 接收者 ID |
| `type` | `Literal["request", "response", "notification"]` | 訊息類型 |
| `payload` | `dict[str, Any]` | 訊息內容 |
| `correlation_id` | `str \| None` | 關聯 ID (用於請求-響應) |
| `timestamp` | `datetime` | 時間戳 |

---

#### `SharedAgentState` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `_state` | `dict[str, Any]` | 共享狀態字典 |
| `_locks` | `dict[str, Lock]` | 資源鎖 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `get` | `(self, key: str)` | `Any \| None` | 獲取狀態 (線程安全) |
| `set` | `(self, key: str, value: Any)` | `None` | 設置狀態 (線程安全) |
| `acquire_lock` | `(self, resource: str)` | `Lock` | 獲取資源鎖 |
| `release_lock` | `(self, resource: str)` | `None` | 釋放資源鎖 |

---

#### `SubGraph` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `graph` | `StateGraph` | 子圖實例 |
| `name` | `str` | 子圖名稱 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `as_node` | `(self)` | `BaseNode` | 轉換為節點 |
| `invoke` | `(self, state: ReActState)` | `ReActState` | 執行子圖 |
| `propagate_context` | `(self, parent_state: ReActState)` | `ReActState` | 傳播上下文 |

---

### Agents Module

#### `Coordinator` (Agent)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `decompose_task` | `(self, task: str)` | `list[Task]` | 分解任務 |
| `select_agent` | `(self, task: Task)` | `str` | 選擇代理 |
| `aggregate_results` | `(self, results: list[Any])` | `Any` | 聚合結果 |
| `coordinate` | `(self, task: str)` | `dict[str, Any]` | 協調多代理執行 |

---

#### `PlanningSpecialist` / `CodingSpecialist` / `ReviewSpecialist` (Agent)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `execute_specialty` | `(self, input: dict)` | `dict[str, Any]` | 執行專業任務 |

---

### Runtime Module

#### `Scheduler` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `task_queue` | `PriorityQueue[Task]` | 任務隊列 |
| `agents` | `dict[str, Agent]` | 代理映射 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `schedule` | `(self, task: Task)` | `None` | 調度任務 |
| `resolve_dependencies` | `(self, tasks: list[Task])` | `ExecutionPlan` | 解析依賴 |
| `execute_parallel` | `(self, plan: ExecutionPlan)` | `list[Any]` | 並行執行 |

---

#### `Task` (Dataclass)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `task_id` | `str` | 任務 ID |
| `description` | `str` | 任務描述 |
| `agent_role` | `str` | 代理角色 |
| `dependencies` | `list[str]` | 依賴任務 ID |
| `priority` | `int` | 優先級 |

---

## PHASE 3: Memory Systems

### Memory Module

#### `ContextWindow` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `max_tokens` | `int` | 最大 token 限制 |
| `messages` | `deque[ReasoningStep]` | 滑動窗口消息 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `add_message` | `(self, step: ReasoningStep)` | `None` | 添加消息 |
| `evict_oldest` | `(self)` | `ReasoningStep \| None` | 驅逐最舊消息 |
| `count_tokens` | `(self)` | `int` | 計算當前 token 數 |
| `get_messages` | `(self)` | `list[ReasoningStep]` | 獲取所有消息 |

---

#### `Summarization` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `llm_client` | `LLMClient` | LLM 客戶端 |
| `compression_ratio` | `float` | 壓縮比率 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `summarize` | `(self, steps: list[ReasoningStep])` | `str` | 摘要生成 |
| `preserve_critical_info` | `(self, steps: list)` | `list[ReasoningStep]` | 保留關鍵信息 |

---

#### `VectorStore` (ABC)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `upsert` | `(self, id: str, vector: list[float], metadata: dict)` | `None` | 插入/更新向量 (抽象) |
| `query` | `(self, vector: list[float], top_k: int)` | `list[tuple[str, float]]` | 查詢最近鄰 (抽象) |
| `delete` | `(self, id: str)` | `None` | 刪除向量 (抽象) |

---

#### `PineconeStore` / `WeaviateStore` (VectorStore)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `client` | `Pinecone \| WeaviateClient` | 客戶端實例 |
| `index_name` | `str` | 索引名稱 |

**方法 (Methods)**

實作 `VectorStore` 的所有抽象方法

---

#### `EmbeddingsClient` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `provider` | `Literal["openai", "cohere"]` | 嵌入提供商 |
| `batch_size` | `int` | 批處理大小 |
| `cache` | `dict[str, list[float]]` | 嵌入緩存 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `embed` | `(self, text: str)` | `list[float]` | 生成嵌入 |
| `embed_batch` | `(self, texts: list[str])` | `list[list[float]]` | 批量生成嵌入 |

---

### Runtime Module Extensions

#### `CheckpointManager` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `db_path` | `Path` | SQLite 數據庫路徑 |
| `checkpoint_interval` | `int` | 檢查點間隔 (步數) |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `save` | `(self, state: ReActState)` | `str` | 保存檢查點，返回 checkpoint_id |
| `load` | `(self, checkpoint_id: str)` | `ReActState` | 載入檢查點 |
| `list_checkpoints` | `(self)` | `list[str]` | 列出所有檢查點 |
| `cleanup_old` | `(self, keep_n: int = 10)` | `None` | 清理舊檢查點 |

---

#### `RollbackManager` (Class)

**屬性 (Properties)**

| 屬性名稱 | 類型 | 說明 |
|:---|:---|:---|
| `checkpoint_manager` | `CheckpointManager` | 檢查點管理器 |

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `rollback_to_step` | `(self, step_id: str)` | `ReActState` | 回滾到指定步驟 |
| `rollback_to_checkpoint` | `(self, checkpoint_id: str)` | `ReActState` | 回滾到檢查點 |
| `validate_rollback` | `(self, state: ReActState)` | `bool` | 驗證回滾狀態 |

---

## PHASE 4: Framework Release

### CLI Module

#### `CLI` (Class)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `main` | `(cls, args: list[str])` | `int` | CLI 入口 (類方法) |
| `parse_args` | `(cls, args: list[str])` | `Namespace` | 解析參數 (類方法) |
| `dispatch_command` | `(cls, command: str)` | `Command` | 分發命令 (類方法) |

---

#### `InitCommand` (Command)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `execute` | `(self, args: Namespace)` | `int` | 執行初始化命令 |
| `scaffold_project` | `(self, path: Path, template: str)` | `None` | 生成項目結構 |

---

#### `RunCommand` (Command)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `execute` | `(self, args: Namespace)` | `int` | 執行 ReAct 循環 |
| `load_graph` | `(self, config: Path)` | `StateGraph` | 載入執行圖 |

---

#### `MigrateCommand` (Command)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `execute` | `(self, args: Namespace)` | `int` | 執行遷移 |
| `analyze_langgraph` | `(self, path: Path)` | `MigrationPlan` | 分析 LangGraph 代碼 |
| `generate_diff` | `(self, plan: MigrationPlan)` | `str` | 生成差異預覽 |
| `apply_migration` | `(self, plan: MigrationPlan)` | `None` | 應用遷移 |

---

#### `ProjectScaffolder` (Class)

**方法 (Methods)**

| 方法名稱 | 簽名 | 返回類型 | 說明 |
|:---|:---|:---|:---|
| `create_structure` | `(self, path: Path, template: str)` | `None` | 創建項目結構 |
| `render_template` | `(self, template: str, context: dict)` | `str` | 渲染模板 |

---

## 統計摘要

| 類別 | 方法總數 | 屬性總數 |
|:---|:---:|:---:|
| Core (PHASE 1) | 42 | 28 |
| Nodes (PHASE 1) | 24 | 18 |
| Tools (PHASE 1) | 15 | 8 |
| Config (PHASE 1) | 8 | 12 |
| Rules (PHASE 1) | 7 | 5 |
| Agents (PHASE 2) | 18 | 12 |
| Memory (PHASE 3) | 16 | 10 |
| CLI (PHASE 4) | 12 | 6 |
| **總計** | **142** | **99** |

---

**下一步**: 查看 `class_diagram.md` 了解完整的 UML 類圖

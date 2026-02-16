# Arkhon-Rheo CRC Cards

Class-Responsibility-Collaborator 卡片設計

---

## 什麼是 CRC 卡片?

CRC (Class-Responsibility-Collaborator) 卡片是一種面向對象設計工具，用於：

- Class: 類別名稱
- Responsibilities: 該類別的職責（它知道什麼，它做什麼）
- Collaborators: 與該類別協作的其他類別

---

## PHASE 1: Foundation Classes

### 1. `ReActState`

```yaml
┌─────────────────────────────────────────────────────────┐
│ Class: ReActState                                       │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 保存不可變的推理執行狀態                                  │
│ • 維護推理步驟的完整歷史                                   │
│ • 追蹤執行元數據和狀態轉換                                  │
│ • 提供狀態驗證和序列化功能                                  │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • ReasoningStep  - 組成狀態的事件                         │
│ • StateGraph     - 管理和轉換狀態                         │
│ • ContextManager - 提供追蹤 ID                           │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 創建初始狀態
state = ReActState(trace_id=ContextManager.generate_trace_id())

# 添加思維步驟 (不可變)
new_state = state.add_step(
    ReasoningStep(
        step_id="step-1",
        type="thought",
        content="I need to search for information"
    )
)

# 驗證狀態
assert new_state.validate() == True
```

---

### 2. `StateGraph`

```
┌─────────────────────────────────────────────────────────┐
│ Class: StateGraph                                       │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 管理執行圖的節點和邊                                     │
│ • 協調節點間的執行流程                                     │
│ • 驗證圖結構的合法性                                       │
│ • 提供同步和流式執行接口                                   │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • BaseNode      - 執行的節點                             │
│ • ReActState    - 傳遞的狀態                             │
│ • ContextManager - 上下文管理                            │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 構建執行圖
graph = (
    StateGraph()
    .add_node("thought", ThoughtNode(llm_client))
    .add_node("validate", ValidateNode(rule_engine))
    .add_node("action", ActionNode(tool_registry))
    .add_edge("thought", "validate")
    .add_edge("validate", "action")
    .set_entry_point("thought")
)

# 編譯並執行
compiled = graph.compile()
result = compiled.invoke({"query": "What is 2+2?"})
```

---

### 3. `BaseNode`

```
┌─────────────────────────────────────────────────────────┐
│ Class: BaseNode (ABC)          │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 定義節點執行的通用框架 (模版方法)                         │
│ • 提供前置和後置執行鉤子                                   │
│ • 強制子類實現 run() 方法                                 │
│ • 標準化節點可調用接口                                     │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • ReActState  - 輸入和輸出                               │
│ • StateGraph  - 被添加到圖中                             │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
class CustomNode(BaseNode):
    name = "custom"
    
    def run(self, state: ReActState) -> ReActState:
        # 實現自定義邏輯
        return state.add_step(...)
    
    def before_run(self, state: ReActState) -> None:
        logger.info(f"Starting {self.name}")
    
    def after_run(self, state: ReActState) -> None:
        logger.info(f"Completed {self.name}")
```

---

### 4. `ToolRegistry`

```
┌─────────────────────────────────────────────────────────┐
│ Class: ToolRegistry (Singleton)                         │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 註冊和管理所有可用工具                                   │
│ • 提供工具發現和查詢功能                                   │
│ • 動態載入工具包                                          │
│ • 確保工具名稱唯一性                                       │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • Tool        - 被註冊的工具                             │
│ • ActionNode  - 查詢和使用工具                           │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 註冊工具
registry = ToolRegistry()
registry.register(SearchTool())
registry.register(CalculatorTool())

# 動態發現工具
ToolRegistry.discover("arkhon_rheo.tools.builtin")

# 獲取工具
tool = registry.get("search")
result = tool.run(query="Python async")
```

---

### 5. `RuleEngine`

```
┌─────────────────────────────────────────────────────────┐
│ Class: RuleEngine                                       │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 順序執行規則集合 (責任鏈)                                │
│ • 收集所有規則違規                                         │
│ • 提供提前終止選項                                         │
│ • 管理規則註冊                                            │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • Rule           - 被執行的規則                          │
│ • RuleViolation  - 違規報告                             │
│ • ValidateNode   - 使用引擎驗證狀態                       │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 配置規則引擎
engine = (
    RuleEngine()
    .add_rule(MaxDepthRule(max_depth=10))
    .add_rule(ForbidGuessingRule(min_confidence=0.8))
    .add_rule(CostLimitRule(max_cost_usd=1.0))
)

# 執行驗證
violations = engine.execute(state)
if violations:
    for v in violations:
        logger.warning(f"{v.rule_name}: {v.message}")
```

---

## PHASE 2: Multi-Agent Classes

### 6. `Agent`

```
┌─────────────────────────────────────────────────────────┐
│ Class: Agent                                            │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 表示獨立的 AI 代理實體                                  │
│ • 管理代理間訊息傳遞                                       │
│ • 執行自己的 ReAct 推理循環                               │
│ • 處理同步和異步通訊                                       │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • StateGraph       - 代理的執行邏輯                      │
│ • AgentMessage     - 訊息傳遞                            │
│ • SharedAgentState - 共享狀態訪問                        │
│ • Scheduler        - 被調度執行                          │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 創建專家代理
agent = Agent(
    agent_id="planner-01",
    role="planning",
    graph=planning_graph
)

# 發送任務請求
agent.send_message(
    to="coder-01",
    msg=AgentMessage(
        type="request",
        payload={"task": "Implement feature X"}
    )
)

# 處理響應
response = agent.receive_message(timeout=10.0)
```

---

### 7. `Coordinator`

```
┌─────────────────────────────────────────────────────────┐
│ Class: Coordinator (extends Agent)                      │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 分解複雜任務為子任務                                     │
│ • 選擇合適的專家代理                                       │
│ • 聚合專家結果                                            │
│ • 協調多代理工作流程                                       │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • PlanningSpecialist - 規劃專家                          │
│ • CodingSpecialist   - 編碼專家                          │
│ • ReviewSpecialist   - 審查專家                          │
│ • Scheduler          - 任務調度                          │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 協調多代理
coordinator = Coordinator(agent_id="coordinator")

result = coordinator.coordinate(
"Build a REST API with auth"
)
# 内部流程:
# 1. decompose_task() -> [plan, code, review]
# 2. select_agent() for each task
# 3. Wait for specialists
# 4. aggregate_results()
```

---

### 8. `Scheduler`

```
┌─────────────────────────────────────────────────────────┐
│ Class: Scheduler                                        │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 管理代理任務隊列                                         │
│ • 解析任務依賴關係                                         │
│ • 並行執行獨立任務                                         │
│ • 優先級調度                                              │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • Agent - 被調度的代理                                   │
│ • Task  - 任務定義                                       │
│ • ExecutionPlan - 執行計劃                               │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 創建任務
tasks = [
    Task(id="t1", agent_role="planning", dependencies=[]),
    Task(id="t2", agent_role="coding", dependencies=["t1"]),
    Task(id="t3", agent_role="testing", dependencies=["t2"]),
]

# 調度執行
scheduler = Scheduler(agents={...})
plan = scheduler.resolve_dependencies(tasks)
results = scheduler.execute_parallel(plan)  # t1 → (t2 || t3)
```

---

## PHASE 3: Memory System Classes

### 9. `ContextWindow`

```
┌─────────────────────────────────────────────────────────┐
│ Class: ContextWindow                                    │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 實現滑動窗口記憶管理                                     │
│ • 自動驅逐最舊消息                                         │
│ • Token 計數和限制                                        │
│ • FIFO 消息隊列                                          │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • ReasoningStep  - 被存儲的消息                          │
│ • TokenTracker   - Token 計數                           │
│ • Summarization  - 觸發壓縮                              │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 配置 context window
window = ContextWindow(max_tokens=4000)

# 添加步驟
for step in reasoning_steps:
    window.add_message(step)
    # 自動驅逐超出限制的消息

# 獲取當前上下文
current_context = window.get_messages()
assert window.count_tokens() <= 4000
```

---

### 10. `VectorStore`

```
┌─────────────────────────────────────────────────────────┐
│ Class: VectorStore (ABC)                                │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 定義向量存儲接口                                         │
│ • 抽象不同向量數據庫的差異                                  │
│ • 提供 upsert/query/delete 操作                          │
│ • 支持語義搜索                                            │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • EmbeddingsClient    - 生成嵌入                         │
│ • RetrievalStrategy   - 檢索策略                         │
│ • PineconeStore/...   - 具體實現                         │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 抽象工廠模式
def create_vector_store(provider: str) -> VectorStore:
    if provider == "pinecone":
        return PineconeStore(index_name="memory")
    elif provider == "weaviate":
        return WeaviateStore(index_name="memory")

# 使用
store = create_vector_store("pinecone")
store.upsert(id="doc1", vector=embedding, metadata={...})

# 語義搜索
results = store.query(query_vector, top_k=5)
```

---

### 11. `CheckpointManager`

```
┌─────────────────────────────────────────────────────────┐
│ Class: CheckpointManager                                │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 保存執行狀態快照 (Memento)                             │
│ • 管理 SQLite 持久化存儲                                  │
│ • 自動增量檢查點                                          │
│ • 清理舊檢查點                                            │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • ReActState       - 被保存的狀態                        │
│ • RollbackManager  - 回滾操作                            │
│ • CommitNode       - 觸發保存                            │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```python
# 配置檢查點
manager = CheckpointManager(
    db_path=Path(".arkhon/checkpoints.db"),
    checkpoint_interval=5  # 每5步一次
)

# 保存檢查點
checkpoint_id = manager.save(current_state)

# 列出檢查點
checkpoints = manager.list_checkpoints()

# 清理
manager.cleanup_old(keep_n=10)
```

---

## PHASE 4: CLI Classes

### 12. `CLI`

```
┌─────────────────────────────────────────────────────────┐
│ Class: CLI                                              │
├─────────────────────────────────────────────────────────┤
│ Responsibilities:                                       │
│ • 提供命令行接口入口                                       │
│ • 解析命令行參數                                          │
│ • 分發到具體命令                                          │
│ • 錯誤處理和幫助信息                                       │
├─────────────────────────────────────────────────────────┤
│ Collaborators:                                          │
│ • InitCommand    - init 命令                            │
│ • RunCommand     - run 命令                             │
│ • MigrateCommand - migrate 命令                         │
└─────────────────────────────────────────────────────────┘
```

**使用場景**:

```bash
# 初始化項目
arkhon-rheo init my-agent --template=basic

# 運行代理
arkhon-rheo run --config=config.yaml --debug

# 遷移 LangGraph 項目
arkhon-rheo migrate ./langgraph-project --output=./arkhon-project
```

---

## CRC 設計原則

### 1. **單一職責原則 (SRP)**

每個類別只有一個明確的職責，例如：

- `ReActState` 只管理狀態
- `ToolRegistry` 只管理工具註冊
- `RuleEngine` 只執行規則

### 2. **協作者最小化**

限制每個類別的協作者數量，降低耦合：

- `ReasoningStep` 只協作 `ReActState`
- `BaseNode` 主要協作 `ReActState` 和 `StateGraph`

### 3. **抽象穩定**

抽象類(ABC) 的協作者應該是穩定的：

- `BaseNode` → `ReActState` (穩定)
- `Tool` → `ToolResult` (穩定)
- `VectorStore` → `EmbeddingsClient` (穩定)

### 4. **依賴倒置**

高層模組不依賴低層模組，都依賴抽象：

- `ActionNode` → `Tool` (抽象)
- `ThoughtNode` → `LLMClient` (抽象)
- `ValidateNode` → `Rule` (抽象)

---

**下一步**: 查看 `typing_guide.md` 了解完整的 Typing Hints 和 Docstrings 規範

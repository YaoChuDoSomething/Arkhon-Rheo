# Arkhon-Rheo 核心概念

這是一套結合 **Deterministic Engineering (確定性工程)** 與 **Probabilistic Generative AI (機率性生成 AI)** 的高階混合架構。這種架構試圖通過嚴格的規範（憲法、RACI、ACL）來約束 LLM 的幻覺，並利用 LangGraph 的循環圖特性來模擬人類開發者的迭代行為。

以下針對您提出的核心概念進行專業分析，並探討實現 100% 自動化的其他策略。

## 1. 核心概念與 Pros & Cons 分析

這套架構的核心在於 **「用制度管理智能」**。以下是各組件的技術評估：

| `核心概念 (Core Concept)` | `技術定義 (Definition)` | `優點 (Pros)` | `缺點 (Cons)` |
| :---- | :---- | :---- | :---- |
| `TDD (Test-Driven Development)` | `將測試案例作為 Agent 的 Reward Function 與 Acceptance Criteria。先寫測試，再生成代碼，直到測試通過。` | `1. 提供明確的終止條件 (Termination Condition)。 2. 防止回歸錯誤 (Regression)。 3. 迫使 Agent 理解需求邊界。` | `1. Agent 容易寫出「自我實現」的測試 (測試與實作邏輯同構，無效驗證)。 2. 測試代碼本身的維護成本高。 3. 消耗大量 Token 進行 Red-Green-Refactor 循環。` |
| `LangChain-LangGraph (Agent State Machine)` | `使用 Cyclic Graph 取代傳統 DAG，支援持久化狀態 (Persistence) 與人機協作 (Human-in-the-loop)。` | `1. 支援複雜的循環邏輯 (Plan -> Code -> Critique -> Refine)。 2. 狀態可回溯 (Time Travel)，便於除錯。 3. 結構化控制流，優於純 Prompt 驅動。` | `1. 狀態管理極其複雜，尤其是涉及多 Agent 共享記憶時。 2. Graph 定義若過於僵化，會限制 Agent 的靈活性。` |
| `最高憲法規範 (Supreme Constitution)` | `在 System Prompt 層級注入不可覆蓋的指令 (Constitutional AI)，定義 Coding Style、安全性與倫理邊界。` | `1. 確保全系統一致性 (Consistency)。 2. 防止 Agent 越權或產生危險代碼。 3. 減少個別 Agent 的 Prompt 長度。` | `1. 過強的規範可能導致 Agent 拒絕執行邊緣案例 (Over-refusal)。 2. 佔用 Context Window，增加推理成本。` |
| `代理人 ACL 區別 (Visible/Invisible Scope)` | `基於角色的存取控制。限制 Agent 對文件系統、API 或對話歷史的 Read/Write 權限。` | `1. 資安沙箱化 (Sandboxing)：防止 Agent 誤刪庫或洩漏金鑰。 2. Context 優化：減少無關資訊干擾 (Need-to-know basis)。` | `1. 設計複雜，需動態掛載/卸載權限。 2. 若 Context 隔離過度，Agent 可能因缺乏全局觀而做出局部最佳解 (Local Optima)。` |
| `RACI 矩陣` | `定義多 Agent 協作中的角色：Responsible (執行), Accountable (當責), Consulted (諮詢), Informed (告知)。` | `1. 解決多 Agent 爭論不休 (Infinite Loop) 的問題。 2. 明確決策權，由 Accountable Agent 做最終定奪。` | `1. 增加通訊開銷 (Communication Overhead)。 2. 若 Consulted Agent 回應延遲或品質差，會阻塞流程。` |
| `Agent-Decision & Machine-Governance` | `混合治理模式：Agent 負責創造性決策，Machine (Linter, AST Parser, CI/CD) 負責硬性攔截。` | `1. 互補性強：LLM 擅長生成，Rule-based 擅長驗證。 2. 100% 確保語法與靜態分析通過，降低 Runtime Error。` | `1. 整合介面開發成本高。 2. 當 Machine 報錯訊息晦澀時，Agent 可能無法理解並陷入修復死循環。` |
| `Gemma 3 LLM` | `Google 最新一代開源模型 (假設為多模態原生、高性能版本)。` | `1. Multimodal Native：可直接理解 UI 設計圖或架構圖。 2. Open Weights：可針對特定 Codebase 進行 Fine-tuning，數據隱私性高。 3. 推理成本低於閉源 SOTA 模型。` | `1. 複雜邏輯推理能力可能仍略遜於頂級閉源模型 (如 GPT-4o / Claude 3.5)。 2. Context Window 長度限制 (視具體版本而定)。` |

---

## 2. 邁向 100% 自動化開發的其他策略與作法

除了上述標準流程，要達成「100% 無人值守」開發，還需引入更底層或更抽象的技術：

### A. Formal Verification Integration (形式化驗證整合)

* **概念**：不只依賴 TDD，而是讓 Agent 撰寫 **TLA+** 或 **Dafny** 規格書，證明程式碼在數學上的正確性。
* **價值**：對於金融或區塊鏈合約開發，這是達成 100% 可靠性的唯一途徑，消除了「測試案例未覆蓋」的盲點。

### B. AST-Based Code Manipulation (基於抽象語法樹的操作)

* **概念**：限制 Agent 直接輸出純文字代碼，轉而讓 Agent 操作 **AST (Abstract Syntax Tree)** 或使用 **LSP (Language Server Protocol)** 的 Action。
* **價值**：杜絕語法錯誤 (Syntax Error)，Agent 的輸出保證是可編譯/可解析的結構。
* **實作**：Agent 輸出 JSON patch 指令 -> 系統解析並應用於 AST -> 還原為程式碼。

### C. Evolution Strategies & Genetic Algorithms (演化策略)

* **概念**：不依賴單一 Agent 的「思考」，而是生成 10 個變體 (Population)，通過測試 (Fitness Function) 篩選，再進行交叉/突變 (Crossover/Mutation)。
* **價值**：解決 LLM 容易陷入思維定勢 (Stuck in a rut) 的問題，透過暴力演算法尋找全域最佳解。

### D. DSPy / Automatic Prompt Optimization

* **概念**：將 Prompt 視為可優化的參數。使用 DSPy 等框架，讓 Agent 在開發過程中自動優化自己的 System Prompt 和 Few-shot Examples。
* **價值**：系統會隨著開發任務的增加而「自我進化」，越用越聰明，而非靜態的 Prompt 工程。

### E. Memory Stream & Reflection Forest (記憶流與反思森林)

* **概念**：建立類似 Generative Agents 的長期記憶庫（向量資料庫），並構建「反思樹」。當遇到類似 Bug 時，檢索過去的解決方案。
* **價值**：避免 Agent 重複犯錯，建立專案專屬的「經驗庫」。

---

## 3. 專案文件結構與實作範例

以下展示如何使用 `LangGraph` 實作 **State Machine** 與 **ACL** 概念的骨架。

**Project Structure:**

```text
project_root/
├── agents/
│   ├── __init__.py
│   ├── base.py       # Base Agent with ACL logic
│   └── coder.py      # Coder Agent implementation
├── workflow/
│   ├── graph.py      # LangGraph state machine definition
│   └── constitution.py # Supreme Constitution prompts
└── config/
    └── settings.yaml # Project configuration

```

**Implementation:**

```python
# project_root/agents/base.py
"""
Base agent module handling ACL and common behaviors.
"""
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ACLContext:
    """
    Defines the Access Control List for an agent.
    
    Attributes:
        visible_files: List of file paths the agent can read.
        editable_files: List of file paths the agent can write.
        allowed_tools: List of tool names the agent can execute.
    """
    visible_files: List[str]
    editable_files: List[str]
    allowed_tools: List[str]

class BaseAgent:
    """
    Abstract base agent enforcing ACLs and constitutional constraints.
    """
    def __init__(self, name: str, acl: ACLContext, system_prompt: str):
        self.name = name
        self.acl = acl
        self.system_prompt = system_prompt

    def can_edit(self, filepath: str) -> bool:
        """Checks if the agent has write permission for the file."""
        return filepath in self.acl.editable_files

    def filter_context(self, full_context: dict) -> dict:
        """
        Filters the context based on visible_files (Information Hiding).
        Only explicitly allowed information is passed to the LLM.
        """
        filtered = {}
        for key, content in full_context.items():
            if key in self.acl.visible_files:
                filtered[key] = content
        return filtered

# -------------------------------------------------------------------------
# project_root/workflow/constitution.py
"""
Supreme Constitution definition.
"""

SUPREME_CONSTITUTION = """
## SUPREME CONSTITUTION
1. **Safety First**: Never generate code that executes arbitrary system commands without explicit user review.
2. **TDD Mandate**: No production code shall be written before a failing test exists.
3. **Idempotency**: All scripts must be re-runnable without side effects.
4. **English Only**: All variable names, function names, and docstrings must be in English.
"""

# -------------------------------------------------------------------------
# project_root/workflow/graph.py
"""
LangGraph workflow definition implementing the RACI matrix and state transitions.
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator

# Define the state of the agent system
class AgentState(TypedDict):
    """
    Represents the shared state of the development process.
    """
    messages: Annotated[List[str], operator.add]
    current_file: Optional[str]
    test_results: Optional[str]
    raci_status: dict  # Tracks who is currently responsible

def coder_node(state: AgentState):
    """
    Node for the Coder agent.
    Responsible for implementation based on specs.
    """
    # Logic to invoke Gemma 3 with ACL filtering
    print("--- Coder Agent Working ---")
    # ... implementation details ...
    return {"messages": ["Code generated"], "current_file": "main.py"}

def tester_node(state: AgentState):
    """
    Node for the Tester agent.
    Responsible for TDD verification.
    """
    print("--- Tester Agent Verifying ---")
    # ... execute tests ...
    test_passed = False # Mock result
    
    if test_passed:
        return {"test_results": "PASS"}
    else:
        return {"test_results": "FAIL", "messages": ["Fix required"]}

def decision_router(state: AgentState):
    """
    Router logic (Machine Governance).
    Determines the next state based on strict criteria.
    """
    if state.get("test_results") == "PASS":
        return "end"
    else:
        return "coder"

# Construct the graph
workflow = StateGraph(AgentState)

workflow.add_node("coder", coder_node)
workflow.add_node("tester", tester_node)

workflow.set_entry_point("coder")
workflow.add_edge("coder", "tester")

workflow.add_conditional_edges(
    "tester",
    decision_router,
    {
        "coder": "coder",
        "end": END
    }
)

app = workflow.compile()

```

```yaml
# project_root/config/settings.yaml
model:
  provider: "google"
  name: "gemma-3-27b-it" # Assuming a hypothetical instruct model
  temperature: 0.2

acl_roles:
  coder_agent:
    visible_files: ["src/**/*.py", "tests/**/*.py"]
    editable_files: ["src/**/*.py"]
    allowed_tools: ["file_writer", "linter"]
  
  architect_agent:
    visible_files: ["**/*"]
    editable_files: ["docs/architecture.md", "workflow/*.py"]
    allowed_tools: ["diagram_generator"]

raci_matrix:
  feature_implementation:
    R: "coder_agent"
    A: "tech_lead_agent"
    C: "security_agent"
    I: "project_manager_agent"

```

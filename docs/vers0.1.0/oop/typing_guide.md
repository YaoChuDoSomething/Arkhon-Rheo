# Arkhon-Rheo Typing & Docstring Guide

Python 3.12+ 類型提示和文檔字符串最佳實踐

---

## 目錄

1. [Typing Hints 規範](#typing-hints-規範)
2. [Docstring 格式 (Google Style)](#docstring-格式)
3. [完整範例](#完整範例)
4. [特殊模式](#特殊模式)
5. [mypy 配置](#mypy-配置)

---

## Typing Hints 規範

### 1. 基本類型標註

```python
from typing import Any, Optional, Union, Literal
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from datetime import datetime

# 簡單類型
name: str = "example"
count: int = 0
ratio: float = 0.5
is_valid: bool = True

# 集合類型 (Python 3.9+)
numbers: list[int] = [1, 2, 3]
mapping: dict[str, Any] = {"key": "value"}
unique_ids: set[str] = {"id1", "id2"}
coordinates: tuple[float, float] = (1.0, 2.0)

# 可選類型 (Python 3.10+)
optional_text: str | None = None  # 推薦
# 或
from typing import Optional
optional_text: Optional[str] = None  # 舊風格
```

### 2. 泛型和類型變量

```python
from typing import TypeVar, Generic, Protocol

# 類型變量
T = TypeVar("T")
TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")

# 泛型類
class Container(Generic[T]):
    """通用容器類型."""
    
    def __init__(self, value: T) -> None:
        self._value = value
    
    def get(self) -> T:
        return self._value
    
    def set(self, value: T) -> None:
        self._value = value

# 使用
int_container: Container[int] = Container(42)
str_container: Container[str] = Container("hello")
```

### 3. Protocol 和 Duck Typing

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Executable(Protocol):
    """可執行協議."""
    
    def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        """執行操作."""
        ...

# 任何實現 execute 方法的類都滿足此協議
class Worker:
    def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        return {"result": "done"}

def run_task(executor: Executable) -> dict[str, Any]:
    """接受任何實現 Executable 協議的對象."""
    return executor.execute({})

assert isinstance(Worker(), Executable)  # True
```

### 4. Self 類型 (Python 3.11+)

```python
from typing import Self

class Builder:
    """建造者模式，支持鏈式調用."""
    
    def __init__(self) -> None:
        self._config: dict[str, Any] = {}
    
    def set_option(self, key: str, value: Any) -> Self:
        """設置選項並返回 self."""
        self._config[key] = value
        return self  # 返回類型自動推斷為 Builder
    
    def build(self) -> dict[str, Any]:
        """構建最終對象."""
        return self._config.copy()

# 使用
config = (
    Builder()
    .set_option("debug", True)
    .set_option("timeout", 30)
    .build()
)
```

### 5. Literal 類型

```python
from typing import Literal

StatusType = Literal["running", "completed", "failed"]

def set_status(status: StatusType) -> None:
    """設置狀態，只接受特定值."""
    print(f"Status: {status}")

set_status("running")  # OK
set_status("unknown")  # mypy error!
```

### 6. TypedDict

```python
from typing import TypedDict, NotRequired

class ConfigDict(TypedDict):
    """配置字典類型."""
    name: str
    version: str
    debug: NotRequired[bool]  # Python 3.11+ 可選字段
    timeout: NotRequired[int]

# 使用
config: ConfigDict = {
    "name": "my-app",
    "version": "1.0.0"
}
```

### 7. Callable 類型

```python
from collections.abc import Callable

# 函數類型
ProcessorFunc = Callable[[str], int]  # (str) -> int

def apply_processor(text: str, processor: ProcessorFunc) -> int:
    """應用處理函數."""
    return processor(text)

def len_processor(s: str) -> int:
    return len(s)

result = apply_processor("hello", len_processor)
```

---

## Docstring 格式

使用 **Google Style** docstrings

### 1. 模組級別 Docstring

```python
"""Arkhon-Rheo 核心狀態管理模組.

此模組提供不可變的狀態管理和事件溯源功能，是 ReAct 引擎的基礎。

典型用法範例:

    from arkhon_rheo.core.state import ReActState, ReasoningStep
    
    state = ReActState()
    state = state.add_step(
        ReasoningStep(type="thought", content="I need to think")
    )

作者:
    Arkhon-Rheo Team

版本:
    1.0.0
"""

from __future__ import annotations
```

### 2. 類級別 Docstring

```python
from dataclasses import dataclass, field
from typing import Literal, Any

@dataclass(frozen=True)
class ReActState:
    """不可變的 ReAct 執行狀態.
    
    使用 frozen dataclass 確保狀態不可變性，支持事件溯源模式。
    每次狀態變更都創建新實例而非修改現有實例。
    
    屬性:
        steps: 推理步驟的完整歷史記錄
        metadata: 執行相關的元數據字典
        trace_id: 分布式追蹤的唯一標識符
        status: 當前執行狀態 ("running"/"completed"/"failed")
    
    範例:
        >>> state = ReActState(trace_id="abc-123")
        >>> new_state = state.add_step(ReasoningStep(...))
        >>> assert state != new_state  # 不可變
        >>> assert new_state.validate()
    
    注意:
        由於使用 frozen=True，所有屬性在創建後無法修改。
        使用 add_step() 等方法返回新實例。
    """
    
    steps: list[ReasoningStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: Literal["running", "completed", "failed"] = "running"
```

### 3. 方法級別 Docstring

```python
def add_step(self, step: ReasoningStep) -> Self:
    """添加新的推理步驟並返回新狀態實例.
    
    由於狀態是不可變的，此方法創建並返回包含新步驟的全新
    ReActState 實例，原實例保持不變。
    
    Args:
        step: 要添加的推理步驟對象
    
    Returns:
        包含新步驟的 ReActState 實例
    
    Raises:
        ValueError: 如果 step 的 type 無效
    
    範例:
        >>> state = ReActState()
        >>> step = ReasoningStep(type="thought", content="thinking...")
        >>> new_state = state.add_step(step)
        >>> len(new_state.steps)
        1
        >>> len(state.steps)  # 原狀態不變
        0
    """
    if step.type not in ("thought", "action", "observation"):
        raise ValueError(f"Invalid step type: {step.type}")
    
    return ReActState(
        steps=self.steps + [step],
        metadata=self.metadata.copy(),
        trace_id=self.trace_id,
        status=self.status
    )
```

### 4. 函數 Docstring

```python
def create_state_from_events(
    events: Sequence[dict[str, Any]],
    trace_id: str | None = None
) -> ReActState:
    """從事件列表重建 ReActState.
    
    此函數實現事件溯源的狀態重建邏輯，從事件日誌恢復
    完整的執行狀態。
    
    Args:
        events: 事件字典序列，每個事件必須包含 'type' 和 'content' 鍵
        trace_id: 可選的追蹤 ID。如果為 None，將生成新 ID
    
    Returns:
        從事件重建的 ReActState 實例
    
    Raises:
        KeyError: 如果事件缺少必需的鍵
        ValueError: 如果事件格式無效
    
    範例:
        >>> events = [
        ...     {"type": "thought", "content": "I need to search"},
        ...     {"type": "action", "content": "search(query='Python')"}
        ... ]
        >>> state = create_state_from_events(events)
        >>> len(state.steps)
        2
    """
    state = ReActState(trace_id=trace_id or str(uuid.uuid4()))
    
    for event in events:
        step = ReasoningStep(
            step_id=str(uuid.uuid4()),
            type=event["type"],
            content=event["content"],
            timestamp=datetime.now()
        )
        state = state.add_step(step)
    
    return state
```

### 5. 屬性 Docstring

```python
class StateGraph:
    """狀態圖執行引擎."""
    
    @property
    def entry_point(self) -> str | None:
        """圖的入口節點名稱.
        
        Returns:
            入口節點名稱，如果未設置則為 None
        
        Raises:
            ValueError: 如果引用的節點不存在
        """
        return self._entry_point
    
    @entry_point.setter
    def entry_point(self, value: str) -> None:
        """設置入口節點.
        
        Args:
            value: 節點名稱，必須已存在於圖中
        
        Raises:
            ValueError: 如果節點不存在
        """
        if value not in self.nodes:
            raise ValueError(f"Node '{value}' not found")
        self._entry_point = value
```

---

## 完整範例

### 核心類別範例: `ReActState`

```python
"""arkhon_rheo.core.state - 核心狀態管理."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal, Self

__all__ = ["ReActState", "ReasoningStep"]


@dataclass(frozen=True)
class ReasoningStep:
    """單個推理步驟的事件日誌.
    
    表示 ReAct 循環中的一個原子步驟（思維、行動或觀察）。
    使用 frozen dataclass 確保事件不可變性。
    
    屬性:
        step_id: 步驟的唯一標識符
        type: 步驟類型 (thought/action/observation)
        content: 步驟的文本內容
        tool_name: 使用的工具名稱（僅 action 類型）
        tool_input: 工具輸入參數（僅 action 類型）
        tool_output: 工具執行結果（僅 action 類型）
        timestamp: 步驟創建時間
        metadata: 額外的元數據字典
    """
    
    step_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: Literal["thought", "action", "observation"] = "thought"
    content: str = ""
    tool_name: str | None = None
    tool_input: dict[str, Any] | None = None
    tool_output: Any | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_event(self) -> dict[str, Any]:
        """轉換為事件日誌格式.
        
        Returns:
            事件字典，包含所有非 None 字段
        
        範例:
            >>> step = ReasoningStep(type="thought", content="I need to think")
            >>> event = step.to_event()
            >>> event["type"]
            'thought'
        """
        event = {
            "step_id": self.step_id,
            "type": self.type,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }
        
        if self.tool_name:
            event["tool_name"] = self.tool_name
        if self.tool_input:
            event["tool_input"] = self.tool_input
        if self.tool_output:
            event["tool_output"] = self.tool_output
        if self.metadata:
            event["metadata"] = self.metadata
        
        return event
    
    def is_action(self) -> bool:
        """檢查是否為 action 步驟.
        
        Returns:
            如果類型為 "action" 則返回 True
        """
        return self.type == "action"
    
    def is_thought(self) -> bool:
        """檢查是否為 thought 步驟.
        
        Returns:
            如果類型為 "thought" 則返回 True
        """
        return self.type == "thought"


@dataclass(frozen=True)
class ReActState:
    """不可變的 ReAct 執行狀態.
    
    核心狀態容器，使用事件溯源模式管理推理執行的完整歷史。
    所有狀態變更都通過創建新實例實現，確保歷史記錄不可篡改。
    
    屬性:
        steps: 推理步驟的時間序列
        metadata: 執行元數據
        trace_id: 分布式追蹤標識符
        status: 執行狀態
    
    範例:
        >>> state = ReActState()
        >>> step = ReasoningStep(type="thought", content="I need data")
        >>> state = state.add_step(step)
        >>> assert state.validate()
    """
    
    steps: list[ReasoningStep] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: Literal["running", "completed", "failed"] = "running"
    
    def add_step(self, step: ReasoningStep) -> Self:
        """添加推理步驟.
        
        創建包含新步驟的新狀態實例。原狀態保持不變。
        
        Args:
            step: 要添加的推理步驟
        
        Returns:
            新的 ReActState 實例
        
        範例:
            >>> state = ReActState()
            >>> new_state = state.add_step(ReasoningStep(type="thought", content="..."))
            >>> len(new_state.steps)
            1
            >>> len(state.steps)
            0
        """
        return ReActState(
            steps=self.steps + [step],
            metadata=self.metadata.copy(),
            trace_id=self.trace_id,
            status=self.status
        )
    
    def validate(self) -> bool:
        """驗證狀態一致性.
        
        檢查狀態是否滿足以下不變量:
        - 所有步驟的 step_id 唯一
        - action 步驟必須有 tool_name
        - 步驟時間戳單調遞增
        
        Returns:
            驗證通過返回 True，否則 False
        """
        # 檢查 step_id 唯一性
        step_ids = [s.step_id for s in self.steps]
        if len(step_ids) != len(set(step_ids)):
            return False
        
        # 檢查 action 步驟
        for step in self.steps:
            if step.is_action() and not step.tool_name:
                return False
        
        # 檢查時間戳順序
        for i in range(1, len(self.steps)):
            if self.steps[i].timestamp < self.steps[i-1].timestamp:
                return False
        
        return True
    
    def get_latest_step(self) -> ReasoningStep | None:
        """獲取最新的推理步驟.
        
        Returns:
            最新步驟，如果沒有步驟則返回 None
        """
        return self.steps[-1] if self.steps else None
    
    def to_dict(self) -> dict[str, Any]:
        """序列化為字典.
        
        Returns:
            包含所有狀態信息的字典
        """
        return {
            "steps": [s.to_event() for s in self.steps],
            "metadata": self.metadata,
            "trace_id": self.trace_id,
            "status": self.status
        }
```

---

## 特殊模式

### 1. 抽象基類 (ABC)

```python
from abc import ABC, abstractmethod
from typing import Any

class BaseNode(ABC):
    """節點抽象基類.
    
    定義所有節點必須實現的接口。子類必須實現 run() 方法。
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """節點名稱.
        
        Returns:
            節點的唯一標識符
        """
        ...
    
    @abstractmethod
    def run(self, state: ReActState) -> ReActState:
        """執行節點邏輯.
        
        Args:
            state: 輸入狀態
        
        Returns:
            轉換後的狀態
        """
        ...
    
    def before_run(self, state: ReActState) -> None:
        """執行前鉤子（可選）.
        
        Args:
            state: 即將執行的狀態
        """
        pass
    
    def after_run(self, state: ReActState) -> None:
        """執行後鉤子（可選）.
        
        Args:
            state: 執行後的狀態
        """
        pass
    
    def __call__(self, state: ReActState) -> ReActState:
        """使節點可調用.
        
        實現模板方法模式，協調 before_run、run、after_run 的執行順序。
        
        Args:
            state: 輸入狀態
        
        Returns:
            執行後的狀態
        """
        self.before_run(state)
        result = self.run(state)
        self.after_run(result)
        return result
```

### 2. 工廠方法

```python
from typing import TypeVar, Type

T = TypeVar("T", bound="VectorStore")

class VectorStore(ABC):
    """向量存儲抽象基類."""
    
    @classmethod
    def create(cls: Type[T], provider: str, **kwargs: Any) -> T:
        """工廠方法創建向量存儲實例.
        
        Args:
            provider: 提供商名稱 ("pinecone" | "weaviate")
            **kwargs: 提供商特定的配置參數
        
        Returns:
            向量存儲實例
        
        Raises:
            ValueError: 如果 provider 不支持
        
        範例:
            >>> store = VectorStore.create("pinecone", index_name="test")
            >>> isinstance(store, PineconeStore)
            True
        """
        from .pinecone_store import PineconeStore
        from .weaviate_store import WeaviateStore
        
        providers = {
            "pinecone": PineconeStore,
            "weaviate": WeaviateStore,
        }
        
        if provider not in providers:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return providers[provider](**kwargs)
```

### 3. 上下文管理器

```python
from typing import Self
from contextvars import ContextVar

class ContextManager:
    """線程本地上下文管理器.
    
    使用 ContextVar 實現線程安全的上下文存儲。
    支持 with 語句自動管理上下文生命週期。
    """
    
    _context: ContextVar[dict[str, Any]] = ContextVar(
        "arkhon_context",
        default={}
    )
    
    def get(self, key: str, default: Any = None) -> Any:
        """獲取上下文值.
        
        Args:
            key: 鍵名
            default: 默認值
        
        Returns:
            上下文值或默認值
        """
        return self._context.get().get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """設置上下文值.
        
        Args:
            key: 鍵名
            value: 值
        """
        ctx = self._context.get().copy()
        ctx[key] = value
        self._context.set(ctx)
    
    def __enter__(self) -> Self:
        """進入上下文."""
        return self
    
    def __exit__(self, *args: Any) -> None:
        """退出上下文，清理資源."""
        self._context.set({})
```

---

## mypy 配置

在 `pyproject.toml` 中配置:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_unimported = false
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true

# 外部庫存根
[[tool.mypy.overrides]]
module = [
    "pinecone.*",
    "weaviate.*",
]
ignore_missing_imports = true
```

---

## 驗證命令

```bash
# 類型檢查
mypy src/arkhon_rheo --strict

# 文檔檢查
pydocstyle src/arkhon_rheo --convention=google

# 生成文檔
pdoc arkhon_rheo --html --output-dir docs/api
```

---

**總結**: 本指南遵循 Python 3.12+ 的最佳實踐，結合 Google Style docstrings 和嚴格的 mypy 類型檢查，確保代碼的類型安全性和文檔完整性。

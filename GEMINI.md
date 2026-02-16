# RULES for Arkhon-Rheo Project 實現自動化SOP式的AI代理開發流程

* 主要開發流程技能@tdd-development @workflow-automation
* 禁止使用 micromamba、mypy 指令，必須使用 uv, uvx, pytest, pytest-cov, ruff, ty, radon
* markdown文件需要在撰寫完成後立刻使用linting
* python程式文件在sprint之前要執行linting
* 適時的進行commit，每一個Phase完成時要push
* `langchain`, `langgraph`, `langsmith`, `langchain-google-genai` 採用`langchain`整合`google-genai`的架構
* 標準Python專案目錄架構，`main.py` is the entry script
* 當開發任務(coding)啟動之時，自動使用@context7技能依照`pyproject.toml`|`uv.lock`內容中的依賴版本查詢，`python=3.12`
* 需要推理時自動套用`sequential-thinking`
* 資訊流的傳遞使用`langchain`-`langgraph`-`langsmith`開發框架，並使用`langchain-google-genai`整合`google-genai`開發框架
* 定義開發工具專案(本專案Arkhon-Rheo)與被開發專案(DEV-TARGET)
* `Agent-Dicision` or `Agent-Governence`
* 支援代理人使用MCP工具，或是利用`repomix`搭配`--mcp`選項，將規則轉譯成`xml`或`markdown`格式文件再以`mcp`掛載
* `UV` managed python project. IDE自動識別uv預設虛擬環境。使用`uv add [DEPENDENCIES]`新增依賴。專案本身使用`uv pip install --editable .`。`pyproject.toml`應透過uv指令調整文件內容減少人工手動調整機會(因此不需要另外加PYTHONPATH環境變數)。

---


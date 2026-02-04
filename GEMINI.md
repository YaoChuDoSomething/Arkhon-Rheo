# Rules - GEMINI.md

## Project Builder Wishlists Inputs.

01. 標準Python專案目錄架構，`main.py` is the entry script
02. 當開發任務(coding)啟動之時，自動使用`context7` mcp server依照`pyproject.toml`|`uv.lock`內容中的依賴版本查詢，`python=3.12`
03. 需要推理時自動套用`sequential-thinking`
04. 本專案初期版本使用使用`gemma3`系列LLM，支援調用工具使用`google-deepmind`|`ollama`|`huggingface`
05. 資訊流的傳遞使用`langchain`-`langgraph`-`langsmith`開發框架，未來可能支援獨立`google-genai`開發框架
06. `ollama`與`ollama-python`專案支援工具
07. 專案憲法文件尚未定案，模板檔案: ./.concepts
08. 開發流程圖之7項作業程序
09. 定義開發工具專案(本專案Arkhon-Rheo)與被開發專案(DEV-TARGET)
10. `Agent-Dicision` or `Agent-Governence` 
11. 支援代理人使用MCP工具，或是利用`repomix`搭配`--mcp`選項，將規則轉譯成`xml`或`markdown`格式文件再以`mcp`掛載
12. 測試系統工程化步驟流程文件路徑 `./.research/initial/tests.md`
13. `UV` managed python project. IDE自動識別uv預設虛擬環境。使用`uv add [DEPENDENCIES]`新增依賴。專案本身使用`uv pip install --editable .`。`pyproject.toml`應透過uv指令調整文件內容減少人工手動調整機會(因此不需要另外加PYTHONPATH環境變數)。


## 

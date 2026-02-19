# SECURITY REPORT 2026-02-20

## 🛡️ Arkhon-Rheo 安全與隱私審計報告 (2026-02-20)

本次審計針對當前 PR 的核心組件、代理人邏輯與沙盒工具進行了靜態代碼分析（SAST）。

## 🚨 關鍵風險摘要

  ┌──────────┬───────────────────────────────┬──────────────────────────────────────────────────────────────┐
  │ 嚴重程度 │ 漏洞類型                      │ 描述                                                         │
  ├──────────┼───────────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ Critical │ 沙盒繞過 (`Sandbox Bypass`)     │ `TargetProject` 的白名單檢查可輕易透過路徑遍歷與命令拼接繞過。 │
  │ High     │ 提示詞注入 (`Prompt Injection`) │ 使用者輸入直接流入 `LLM` 提示詞，可能導致非預期工具調用。      │
  │ High     │ 參數注入 (`Argument Injection`) │ `ActionNode` 完全信任並執行來自 `LLM` 的工具參數。               │
  │ Medium   │ 路徑遍歷 (`Path Traversal`)     │ `CLI` 的 `init` 命令過濾邏輯不足，存在目錄穿越風險。             │
  │ Medium   │ 不安全代碼執行                │ `CalculatorTool` 使用 `eval` 且防禦層級不足以應對進階沙箱逃逸。  │
  └──────────┴───────────────────────────────┴──────────────────────────────────────────────────────────────┘

---

## 🔍 詳細漏洞分析

1. TargetProject 白名單機制失效
  
    * 漏洞： 沙盒邊界繞過 (`Sandbox Bypass`)
    * 嚴重程度： Critical
    * 位置： `src/arkhon_rheo/tools/target_project.py` (Line 183-193)
    * 描述： `_check_write_allowed` 與 `_check_command_allowed` 僅使用 `startswith` 檢查相對路徑或命令字串。攻擊者可提供 `src/../.ssh/id_rsa` 來修改敏感檔案，或利用 `uv run pytest && rm -rf` / 執行惡意指令。
    * 建議： 應先使用 `Path(relative_path).resolve()` 正規化路徑，並對命令進行精確匹配或參數化處理。

2. 間接提示詞注入與工具濫用

    * 漏洞： 提示詞注入 (`Prompt Injection`) / 參數注入 (`Argument Injection`)
    * 嚴重程度： High
    * 位置： `src/arkhon_rheo/roles/base.py` (Line 76) & `src/arkhon_rheo/nodes/action_node.py` (Line 56-59)
    * 描述： 系統將使用者訊息（`AgentMessage.content`）未經脫殼直接傳遞給 `Gemini`。惡意使用者可透過提示詞注入誘導 LLM 產生惡意的 `tool_calls`。由於 `ActionNode` 完全信任並執行這些生成的參數，攻擊者可藉此操作檔案或執行系統指令。
    * 建議： 實施輸入淨化、輸出驗證（`Output Validation`），並在 `ActionNode` 執行前對工具參數進行強類型校驗。

3. CLI 初始化路徑遍歷

    * 漏洞： 路徑遍歷 (`Path Traversal`)
    * 嚴重程度： Medium
    * 位置： `src/arkhon_rheo/cli/main.py` (Line 42-44)
    * 描述： `init` 命令僅過濾 `..` 與 `/`。這種基於黑名單的檢查無法防禦所有環境下的路徑操縱（如絕對路徑或 OS 特有的敏感名稱）。
    * 建議： 使用白名單驗證專案名稱，僅允許字母、數字與底線。

4. CalculatorTool 沙盒逃逸風險

    * 漏洞： 不安全代碼執行 (`Unsafe Eval`)
    * 嚴重程度： Medium
    * 位置： `src/arkhon_rheo/tools/builtin/calculator.py` (Line 44-46)
    * 描述： 雖然限制了 `__builtins__`，但 `eval` 本質上不安全。進階攻擊者可能利用繼承鏈（如屬性訪問）來恢復受限環境並執行惡意代碼。
    * 建議： 改用安全數學表達式解析器（如 `numexpr` 或 `ast.literal_eval` 配合自定義限制）。

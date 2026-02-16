# Build Phase [N] Documentation Prompt

## 角色 (Role)

你是由 @skills:docs-architect 驅動的 Arkhon-Rheo 專案文件架構師。你的任務是為特定開發階段 (`[PHASE_NUMBER]`) 建構、整理並驗證開發導向的文件集。

## 上下文 (Context)

- **核心控制文件**:
  - `@Files:docs/vers0.1.0/ROADMAP.md`: 定義了各階段的里程碑、交付物與測試標準。
  - `@Files:docs/system/WORKFLOW_AUTOMATION.md`: 定義了 SDLC 流程與狀態機。
- **目標階段**: `[PHASE_NUMBER]` (使用者需替換此變數，例如 "PHASE 1")

## 任務目標 (Objectives)

1. **分析階段需求**: 閱讀 `ROADMAP.md` 中針對目標階段的 "Goal", "Deliverables", "Exit Criteria"。
2. **盤點現有文件**: 掃描 `@Directories:docs/vers0.1.0/` 和 `@Directories:docs/vers0.1.0/oop/` 中的文件。
3. **文件重組與對齊**:
   - 識別哪些文件與當前階段最相關。
   - 檢查文件內容是否與 `ROADMAP.md` 中的階段目標一致。
   - 修正任何發現的矛盾或過時資訊。
   - 產出或更新該階段的索引文件 (如 `PHASE[N]_INDEX.md`) 或實作指南。
4. **記憶體管理**: 在處理過程中，必須使用以 `context-` 開頭的技能 (如 `context-manager`, `context-window-management`) 來管理資訊流，確保不遺漏關鍵上下文。

## 執行步驟 (Execution with Sequential Thinking)

@mcp:sequential-thinking

1. **Analyze**: 深入分析 `ROADMAP.md` 中 `[PHASE_NUMBER]` 的具體要求。
2. **Audit**: 審查 `docs/vers0.1.0/` 下的所有文件，標記出與此階段相關的文件。
3. **Verify**: 驗證這些文件中的架構設計、類別定義是否符合此階段的測試標準。
   - *Check*: 是否有文件描述的功能超出了此階段的範圍？
   - *Check*: 是否有此階段必要的實作細節在文件中缺失？
4. **Organize**: 建議文件結構調整或內容更新。
5. **Commit/Push Strategy**:
   - 若為 **Sprint 完成**: 建議 git commit message。
   - 若為 **Phase 完成**: 建議 git push 至 main 分支的策略。

## 輸出要求 (Output)

- 一份針對 `[PHASE_NUMBER]` 的文件整理報告。
- 建議的 `PHASE[N]_INDEX.md` 內容 (如果還沒有)。
- 需要修正的矛盾點清單 (如果有)。

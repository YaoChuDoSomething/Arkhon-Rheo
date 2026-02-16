# Phase 4 Skills: Release & Packaging

Phase 4 的重點在於工程化與產品化，建議在 Sprints 中使用以下 Skills 以確保產出品質。

## 推薦技能 (Skills)

### 1. Packaging & CLI

- `python-pro`: 用於實作穩健的 CLI 工具與 `pyproject.toml` 配置。
- `uv-package-manager`: 用於管理依賴與構建 Wheel/Sdist。
- `ty`: 用於 CLI 參數的強型別驗證。

### 2. Documentation & Examples

- `docs-architect`: 用於設計文檔結構與撰寫清晰的 API 手冊。
- `markdown-lint`: 確保所有文檔符合 GFM 標準。
- `writing-skills`: 用於編寫高品質的教學手冊與 Notebooks。

## Context 管理策略

在 Phase 4 中，Context 的重點應在於**跨模組整合**：

- **Review**: 確保 CLI 呼叫的邏輯與 `core` / `runtime` 保持一致。
- **Examples**: 範例應真實反映 Phase 1-3 的最佳實踐。
- **Consistency**: 維護 `ROADMAP.md`、`README.md` 與程式碼註解的一致性。

## 進階考量 (Post-0.1.0)

- **GitHub Actions**: 建立自動化 CI/CD pipeline。
- **PyPI Deployment**: 規劃自動化發布至 PyPI。

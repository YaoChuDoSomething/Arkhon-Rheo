# Phase 4 Index: Framework Release

本文件為 Arkhon-Rheo Phase 4 (Framework Release) 的核心索引，涵蓋了打包分發、CLI 開發以及完整文檔/範例的建立。

## 階段目標

1. **打包與分發**: 將框架打包為可透過 `pip install` 安裝的套件。
2. **CLI 工具**: 建立 `arkhon-rheo` 命令列工具，支援專案初始化與運行。
3. **文檔與範例**: 提供 5 個以上的範例專案與完整的 API 參考手冊。

## Sprint Breakdown

### Sprint 4.1: Packaging & Distribution (Week 11)

- **目標**: 建立 `pyproject.toml`，實作 CLI 基礎架構。
- **交付物**:
  - `pyproject.toml` (Metadata, Dependencies, Entry Points)
  - `src/arkhon_rheo/cli/main.py` (`init`, `run`)
  - `src/arkhon_rheo/cli/migrate.py` (LangGraph 遷移工具)
- **驗證**: `pip install .` 成功，CLI 命令可執行。

### Sprint 4.2: Documentation & Examples (Week 12)

- **目標**: 建立完整的文檔系統與教學範例。
- **交付物**:
  - `docs/` (Getting Started, API Reference, Architecture)
  - `examples/` (Simple, Multi-agent, Memory, Migration)
  - Tutorial Notebooks
- **驗證**: 文檔建置成功，所有範例皆可無誤運行。

## 測試標準 (Cumulative P1-P4)

✅ **P4 測試標準**:

- `pip install arkhon-rheo` 在乾淨環境下成功。
- `arkhon-rheo --version` 返回正確版本。
- 5+ 範例專案執行成功率 100%。
- Sphinx/MkDocs 文檔建置無錯誤。

## 目錄結構 (Phase 4 相關)

```bash
arkhon-rheo/
├── pyproject.toml
├── src/
├── arkhon_rheo/
│   └── cli/
│       ├── main.py
│       └── migrate.py
├── docs/
│   ├── tutorials/
│   └── reference/
└── examples/
    ├── simple_agent/
    └── multi_agent/
```

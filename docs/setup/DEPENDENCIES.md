# Arkhon-Rheo 環境依賴清單

**版本**: 1.0.0  
**更新日期**: 2026-02-15  
**專案結構**: 扁平架構

---

## 📋 概述

本文件記錄 Arkhon-Rheo 專案的完整環境依賴，包含核心依賴、開發工具鏈、基礎設施組件及其配置建議。

**套件管理**: 使用 [uv](https://github.com/astral-sh/uv) - Astral 的極速 Python 套件管理器

---

## 🐍 Python 環境需求

| 項目 | 版本 | 說明 |
| :--- | :--- | :--- |
| **Python** | `>=3.12` | 需要 PEP 695 類型提示支援 |
| **uv** | latest | 套件管理器和虛擬環境工具 |

### 安裝 Python 3.12+

```bash
# macOS (使用 Homebrew)
brew install python@3.12

# Ubuntu/Debian
sudo apt install python3.12 python3.12-venv

# 或使用 pyenv
pyenv install 3.12.0
pyenv local 3.12.0
```

### 安裝 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv

# 驗證安裝
uv --version
```

---

## 📦 核心依賴 (Runtime Dependencies)

### 1. AI/LLM 整合

| 套件 | 用途 | 版本建議 |
| :--- | :--- | :--- |
| `google-genai` | Google Gemini API SDK | `>=0.3.0` |

```bash
uv add google-genai
```

**配置**: 需要設置 `GEMINI_API_KEY` 環境變數

### 2. 配置與驗證

| 套件 | 用途 | 版本建議 |
| :--- | :--- | :--- |
| `pydantic` | 資料驗證和設定管理 | `>=2.0` |
| `pyyaml` | YAML 配置解析 | `>=6.0` |

```bash
uv add "pydantic>=2.0" "pyyaml>=6.0"
```

### 3. 資料持久化

| 套件 | 用途 | 版本建議 |
| :--- | :--- | :--- |
| Python 內建 `sqlite3` | Checkpoint 儲存 | 隨 Python 提供 |

**說明**: SQLite 是 Python 標準庫的一部分，無需額外安裝

### 4. 日誌與可觀測性

| 套件 | 用途 | 版本建議 |
| :--- | :--- | :--- |
| `structlog` | 結構化日誌記錄 | `>=24.0` |

```bash
uv add "structlog>=24.0"
```

### 5. Metrics (可選)

| 套件 | 用途 | 版本建議 |
| :--- | :--- | :--- |
| `prometheus-client` | Prometheus metrics 匯出 | latest |

```bash
uv add prometheus-client  # 可選
```

---

## 🛠️ 開發工具鏈 (Development Dependencies)

### 1. 測試框架

| 套件 | 用途 | 版本建議 |
| :--- | :--- | :--- |
| `pytest` | 測試框架 | `>=8.0` |
| `pytest-cov` | 測試覆蓋率 | latest |
| `pytest-asyncio` | 非同步測試支援 | latest |

```bash
uv add --dev pytest pytest-cov pytest-asyncio
```

### 2. 程式碼品質

| 套件 | 用途 | 版本建議 |
| :--- | :--- | :--- |
| `ruff` | 極速 Linter + Formatter | `>=0.8.0` |
| `ty` | 類型檢查器 | latest |
| `radon` | 程式碼複雜度分析 | latest |

```bash
uv add --dev ruff ty radon
```

**使用方式**:

```bash
# Ruff - Linting 和格式化
ruff check .
ruff format .

# ty - 類型檢查
ty check src/

# Radon - 複雜度分析
radon cc src/ -a  # Cyclomatic Complexity
radon mi src/     # Maintainability Index
```

### 3. 文件生成

| 套件 | 用途 | 版本建議 |
| :--- | :--- | :--- |
| `mkdocs` | 文件網站生成 | latest |
| `mkdocs-material` | Material 主題 | latest |

```bash
uv add --dev mkdocs mkdocs-material
```

---

## ⚙️ pyproject.toml 配置建議

### 完整配置範例

```toml
[project]
name = "arkhon-rheo"
version = "0.1.0"
description = "Deterministic AI Workflow Engine with State Machine Architecture"
readme = "README.md"
requires-python = ">=3.12"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]

dependencies = [
    "google-genai>=0.3.0",
    "pydantic>=2.0",
    "pyyaml>=6.0",
    "structlog>=24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov",
    "pytest-asyncio",
    "ruff>=0.8.0",
    "ty",
    "radon",
    "mkdocs",
    "mkdocs-material",
]
metrics = [
    "prometheus-client",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# ===== Ruff 配置 =====
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
]
ignore = [
    "E501",  # line-too-long (handled by formatter)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

# ===== Pytest 配置 =====
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]

# ===== Coverage 配置 =====
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

---

## 🚀 快速開始

### 1. 建立虛擬環境並安裝依賴

```bash
# 進入專案目錄
cd /wk2/yaochu/github/arkhon-rheo

# 使用 uv 建立虛擬環境並安裝依賴
uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 安裝專案（包含開發依賴）
uv pip install -e ".[dev]"
```

### 2. 驗證安裝

```bash
# 檢查 Python 版本
python --version  # 應該 >= 3.12

# 檢查工具
ruff --version
ty --version
pytest --version
radon --version

# 執行測試（如果有）
pytest

# 執行 Linter
ruff check .

# 類型檢查
ty check src/
```

---

## 📁 專案結構說明（扁平架構）

```text
arkhon-rheo/
├── .venv/                  # uv 虛擬環境
├── .agent/                 # Agent 配置和 skills
│   ├── skills/
│   ├── workflows/
│   └── skill*.{json,yaml}
├── docs/                   # 文件目錄
├── repos/                  # 待評估專案
├── research/               # 研究文件
├── src/                    # 未來可能的源碼目錄（目前未使用）
├── tests/                  # 測試目錄（未來）
├── pyproject.toml          # 專案配置
├── README.md
└── IMPLEMENTATION_GUIDE.md
```

**注意**: 目前專案採用**扁平架構**，主要文件位於根目錄和 `docs/`, `.agent/` 等頂層目錄下。

---

## 🔧 額外工具建議

### Git Hooks (pre-commit)

建議使用 `pre-commit` 確保程式碼品質：

```bash
uv add --dev pre-commit

# 建立 .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
EOF

# 安裝 hooks
pre-commit install
```

### 環境變數管理

建議使用 `.env` 文件管理敏感資訊：

```bash
# .env.example
GEMINI_API_KEY=your_api_key_here
ARKHON_RHEO_ENV=development
ARKHON_RHEO_LOG_LEVEL=DEBUG
```

使用 `python-dotenv` 載入：

```bash
uv add python-dotenv
```

---

## 📊 程式碼品質標準

### OOP 函數規範

根據專案要求，單一函數/方法的程式碼行數（不計空行、不計 Docstring）應：

- **最大長度**: ≤ 400 行純代碼
- **建議長度**: ≤ 100 行
- **複雜度**: Cyclomatic Complexity ≤ 10（使用 radon 檢查）

**檢查方式**:

```bash
# 使用 radon 檢查複雜度
radon cc src/ -a -nc  # -a: 平均值, -nc: 不顯示 C 級
radon mi src/         # Maintainability Index

# 函數行數檢查 (自定義)
# 可以寫一個簡單腳本檢查每個函數的 LOC
```

---

## 🔄 依賴更新

### 使用 uv 管理依賴

```bash
# 查看過時的套件
uv pip list --outdated

# 更新單一套件
uv add package-name --upgrade

# 更新所有套件（謹慎使用）
uv pip install --upgrade -e ".[dev]"

# 鎖定依賴版本（生成 uv.lock）
uv pip freeze > requirements.txt
```

---

## 📚 參考文件

- [uv 官方文件](https://github.com/astral-sh/uv)
- [Ruff 文件](https://docs.astral.sh/ruff/)
- [Pydantic 文件](https://docs.pydantic.dev/)
- [Google GenAI SDK](https://ai.google.dev/gemini-api/docs)
- [Pytest 文件](https://docs.pytest.org/)

---

**維護者**: [Your Team]  
**最後更新**: 2026-02-15

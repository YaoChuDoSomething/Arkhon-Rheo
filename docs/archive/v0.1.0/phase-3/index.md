# Phase 3 (Memory & Storage Systems) 文件索引

**版本**: 1.0.0  
**最後更新**: 2026-02-16  
**狀態**: 🚧 進行中 (In Progress)
**適用階段**: Phase 3 - Memory & Storage Systems (Week 8-10)

---

## 📚 核心開發流程文件

Phase 3 的開發流程導向文件：

| # | 文件 | 用途 | 何時使用 |
| :--- | :--- | :--- | :--- |
| 1 | [**PHASE3_SKILLS.md**](PHASE3_SKILLS.md) | **Sprint 技能指南** | **每個 Sprint 開始時必讀** (Phase 3 專屬) |
| 2 | [ROADMAP.md](./ROADMAP.md#milestone-3-memory-systems-phase-3---weeks-8-10) | Phase 3 詳細計劃和里程碑 | 了解 Sprint 目標和交付物 |
| 3 | [ARCHITECTURE.md](./ARCHITECTURE.md#memory--storage-systems-phase-3) | 記憶與存儲系統設計 | 理解系統設計細節 |
| 4 | [PHASE2_INDEX.md](PHASE2_INDEX.md) | Phase 2 多代理參考 | 查閱代理編排與通訊機制 |
| 5 | [DOC_INDEX.md](DOC_INDEX.md) | 全專案文件導航 | 查找其他文件 |

---

## 🎯 Sprint 對應表

Phase 3 包含 3 個 Sprint，每週一個：

| Sprint | 週數 | 主要目標 | 主要交付物 | 推薦技能 | 狀態 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sprint 3.1** | Week 8 | Short-term Memory | `ContextWindow`, `Summarizer` | [PHASE3_SKILLS.md §Sprint 3.1](./PHASE3_SKILLS.md#sprint-31-short-term-memory-week-8) | ⏳ |
| **Sprint 3.2** | Week 9 | Vector Store Integration | `VectorStore`, `Embeddings` | [PHASE3_SKILLS.md §Sprint 3.2](./PHASE3_SKILLS.md#sprint-32-vector-store-integration-week-9) | ⏳ |
| **Sprint 3.3** | Week 10 | Checkpointing & Rollback | `CheckpointManager`, `Rollback` | [PHASE3_SKILLS.md §Sprint 3.3](./PHASE3_SKILLS.md#sprint-33-checkpointing--rollback-week-10) | ⏳ |

詳細 Sprint 計劃請參考 [ROADMAP.md §Milestone 3](./ROADMAP.md#milestone-3-memory-systems-phase-3---weeks-8-10)。

---

## ✅ Phase 3 測試標準

Phase 3 測試標準繼承所有 P1 與 P2 標準：

### 繼承標準

- ✅ **Phase 1 & 2 所有測試必須通過**
- ✅ 覆蓋率維持 **≥90%**
- ✅ mypy/ty 零錯誤

### Phase 3 新增標準

- **Memory**:
  - Context 維持在 Token 限制內 (Sliding Window)
  - 摘要 (Summarization) 保留關鍵事實
  - 向量存儲處理 10k+ 向量
  - 查詢延遲 <500ms (p95)
- **Checkpoint**:
  - 可回滾至任一歷史步驟
  - 回滾後狀態保持一致性
  - Checkpoint 開銷 <5% 執行時間
  - E2E: 執行 → 中斷 → 回滾 → 恢復

### 驗證命令

```bash
# 執行所有測試
uv run pytest tests/core/ tests/agents/ tests/memory/ --cov=arkhon_rheo --cov-report=html

# 僅執行 Phase 3 相關測試
uv run pytest tests/memory/ tests/runtime/checkpoint.py
```

---

## 📂 專案目錄結構 (Phase 3 預期)

```text
src/                          # updated
├── arkhon_rheo/
│   ├── memory/               # Phase 3: 記憶系統
│   │   ├── context_window.py # Sprint 3.1
│   │   ├── summarization.py  # Sprint 3.1
│   │   ├── vector_store.py   # Sprint 3.2
│   │   └── embeddings.py     # Sprint 3.2
│   └── runtime/
│       ├── checkpoint.py     # Sprint 3.3
│       └── rollback.py       # Sprint 3.3
└── docs/
    └── vers0.1.0/
        ├── PHASE3_INDEX.md   # 本文件
        └── PHASE3_SKILLS.md
```

---

**維護者**: Arkhon-Rheo Team  
**最後更新**: 2026-02-16  
**文件版本**: 1.0.0

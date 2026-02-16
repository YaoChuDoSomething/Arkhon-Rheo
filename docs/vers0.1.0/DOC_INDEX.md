# ReActEngine Documentation Index

**Version**: 1.0.0  
**Last Updated**: 2026-02-16

---

## Quick Navigation

### 🚀 Start Here

**Quickstart**: [DEVGUIDE.md](./DEVGUIDE.md) → [ROADMAP.md](./ROADMAP.md)

### 📌 Phase 1 (Foundation) 快速入口

**正在進行 Phase 1 開發？**閱讀順序：

1. **[PHASE1_INDEX.md](PHASE1_INDEX.md)** - Phase 1 專屬索引（⭐ 新增）
2. **[ROADMAP.md - Phase 1 詳細計劃](ROADMAP.md#milestone-1-foundation-phase-1---weeks-1-4)**
3. **[PHASE1_SKILLS.md](PHASE1_SKILLS.md)** - 每個 Sprint 的技能推薦（⭐ 新增）
4. **[DEVGUIDE.md](DEVGUIDE.md)** - 開發環境設定
5. **[TDD.md](TDD.md)** - 測試策略

### 📌 Phase 2 (Multi-Agent) 快速入口

**正在進行 Phase 2 開發？**閱讀順序：

1. **[PHASE2_INDEX.md](PHASE2_INDEX.md)** - Phase 2 專屬索引（⭐ 新增）
2. **[ROADMAP.md - Phase 2 詳細計劃](ROADMAP.md#milestone-2-multi-agent-architecture-phase-2---weeks-5-7)**
3. **[PHASE2_SKILLS.md](PHASE2_SKILLS.md)** - 每個 Sprint 的技能推薦（⭐ 新增）

### 📌 Phase 3 (Memory Systems) 快速入口

**正在進行 Phase 3 開發？**閱讀順序：

1. **[PHASE3_INDEX.md](PHASE3_INDEX.md)** - Phase 3 專屬索引（⭐ 新增）
2. **[ROADMAP.md - Phase 3 詳細計劃](ROADMAP.md#milestone-3-memory-systems-phase-3---weeks-8-10)**
3. **[PHASE3_SKILLS.md](PHASE3_SKILLS.md)** - 每個 Sprint 的技能推薦（⭐ 新增）

---

## Documentation by Category

### 📋 Implementation Guides

| Document                                                                             | Purpose                            | When to Use                      |
|--------------------------------------------------------------------------------------|------------------------------------|----------------------------------|
| **[workflows_ai-agentic-system-builder.md](workflows_ai-agentic-system-builder.md)** | Complete implementation workflow   | Building the system from scratch |
| **[DEVGUIDE.md](DEVGUIDE.md)**                                                       | Developer guide                    | Day-to-day development           |
| **[TDD.md](TDD.md)**                                                                 | Test-driven development strategy   | Writing tests                    |

### 🏗️ Architecture & Design

| Document                                       | Purpose                | When to Use                          |
|------------------------------------------------|------------------------|--------------------------------------|
| **[SPECIFICATION.md](SPECIFICATION.md)**       | Technical requirements | Understanding what to build          |
| **[ARCHITECTURE.md](ARCHITECTURE.md)**         | Component architecture | Understanding system structure       |
| **[DESIGN.md](DESIGN.md)**                     | System design details  | Understanding data flow, performance |
| **[STATE_MACHINE.md](STATE_MACHINE.md)**       | State machine design   | Understanding execution flow         |

### 📐 Domain-Specific

| Document                                       | Purpose                | When to Use                |
|------------------------------------------------|------------------------|----------------------------|
| **[RULES.md](RULES.md)**                       | Rule engine governance | Implementing rules         |
| **[ACL.md](ACL.md)**                           | Access control         | Implementing permissions   |
| **[SKILLS_MANIFEST.md](SKILLS_MANIFEST.md)**   | Skills catalog         | Understanding capabilities |

### 📅 Planning

| Document                     | Purpose             | When to Use          |
|------------------------------|---------------------|----------------------|
| **[ROADMAP.md](ROADMAP.md)** | Development roadmap | Planning future work |

---

## Recommended Reading Path

### For Developers Starting Implementation

```text
1. SPECIFICATION.md       (Understand requirements)
   ↓
2. ARCHITECTURE.md         (Understand structure)
   ↓
3. workflows_*.md          (Follow implementation steps)
   ↓
4. DEVGUIDE.md + TDD.md    (Start coding with TDD)
   ↓
5. DESIGN.md + RULES.md    (Reference as needed)
```

### For Architecture Review

```text
1. SPECIFICATION.md        (Requirements)
   ↓
2. ARCHITECTURE.md          (Component design)
   ↓
3. STATE_MACHINE.md         (Execution model)
   ↓
4. DESIGN.md                (Design patterns)
```

### For Testing

```text
1. TDD.md                  (Testing strategy)
   ↓
2. workflows_*.md          (Phase 6-7: Testing)
   ↓
3. DEVGUIDE.md §7          (Writing tests)
```

---

## Phase-to-Documentation Mapping

| Phase | Primary Reference | Supporting Docs |
| :--- | :--- | :--- |
| **Phase 0: Initialization** | [DEVGUIDE.md §1](./DEVGUIDE.md) | [SPECIFICATION.md §5](./SPECIFICATION.md) |
| **Phase 1: Foundation** | **[PHASE1_INDEX.md](./PHASE1_INDEX.md)** | [ROADMAP.md](./ROADMAP.md), **[PHASE1_SKILLS.md](./PHASE1_SKILLS.md)** |
| **Phase 2: Multi-Agent** | **[PHASE2_INDEX.md](./PHASE2_INDEX.md)** (⭐ 新增) | [ROADMAP.md](./ROADMAP.md), **[PHASE2_SKILLS.md](./PHASE2_SKILLS.md)** (⭐ 新增), ARCHITECTURE.md §Multi-agent |
| **Phase 3: Memory Systems** | **[PHASE3_INDEX.md](./PHASE3_INDEX.md)** (⭐ 新增) | [ROADMAP.md](./ROADMAP.md), **[PHASE3_SKILLS.md](./PHASE3_SKILLS.md)** (⭐ 新增), ARCHITECTURE.md §Memory |
| Phase 4: Release Preparation | [ROADMAP.md §Phase 4](./ROADMAP.md) | DEVGUIDE.md §Deployment/Publishing |
| Phase 5: Memory | SPECIFICATION.md §4.3-4.4 | ARCHITECTURE.md §4.5 |
| :--- | :--- | :--- |
| Phase 6-7: Testing | TDD.md | DEVGUIDE.md §7 |
| Phase 8: Packaging | SPECIFICATION.md §5 | DEVGUIDE.md §10 |

---

## Document Status

| Document           | Status   | Completeness | Last Updated |
|--------------------|----------|--------------|--------------|
| SPECIFICATION.md   | ✅ Final | 100%         | 2026-02-14   |
| ARCHITECTURE.md    | ✅ Final | 100%         | 2026-02-14   |
| DESIGN.md          | ✅ Final | 100%         | 2026-02-14   |
| DEVGUIDE.md        | ✅ Final | 100%         | 2026-02-14   |
| TDD.md             | ✅ Final | 100%         | 2026-02-14   |
| RULES.md           | ✅ Final | 100%         | 2026-02-14   |
| STATE_MACHINE.md   | ✅ Final | 100%         | 2026-02-14   |
| workflows_*.md     | ✅ Final | 100%         | 2026-02-14   |
| ACL.md             | ✅ Final | 100%         | 2026-02-14   |
| SKILLS_MANIFEST.md | ✅ Final | 100%         | 2026-02-14   |
| ROADMAP.md         | ✅ Final | 100%         | 2026-02-14   |

---

## Quick Reference

### Key Concepts

- **Arkhon-Rheo**: The philosophical framework and governance standards
- **ReActEngine**: The concrete OOP implementation
- **Event Sourcing**: Immutable append-only state log
- **State Machine**: Deterministic execution flow
- **Rule Engine**: Governance constraints
- **Tool Registry**: Pluggable external APIs

### Core Classes

- `ReActState` - Immutable state container
- `ReasoningStep` - Single thought-action-observation cycle
- `BaseNode` - Abstract base for all execution nodes
- `StateGraph` - Directed graph of nodes
- `Tool` - External API wrapper
- `Rule` - Governance constraint

### File Locations

```text
src/arkhon-rheo/
├── arkhon_rheo/          # Main package
│   ├── core/             # State machine & graph
│   ├── nodes/            # ReAct nodes
│   ├── tools/            # Tool registry
│   ├── rules/            # Governance rules
│   ├── memory/           # Memory systems
│   ├── runtime/          # Execution runtime
│   └── config/           # Configuration
├── tests/                # Test suite
└── docs/                 # This directory
```

---

## External References

- **Python 3.12+ Documentation**: <https://docs.python.org/3.12/>
- **Pydantic V2**: <https://docs.pydantic.dev/>
- **Pytest**: <https://docs.pytest.org/>
- **Ruff**: <https://docs.astral.sh/ruff/>
- **mypy**: <https://mypy.readthedocs.io/>

---

**Questions?** Refer to [DEVGUIDE.md §11 (Troubleshooting)](DEVGUIDE.md#11-troubleshooting).

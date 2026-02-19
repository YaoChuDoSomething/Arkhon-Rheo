# RACI Workflows – Implementation Roadmap

## 1. Vision

Implement 9 RACI workflows in `arkhon-rheo`, each targeting a `DEV-TARGET` (`../dlamp`).
A **Meta-Orchestrator** with `sequential-thinking` selects the scheme; each agent carries a specific skill persona.

## 2. Agent Roles (from `config/workflow_context.yaml`)

| Role | Class | Model | Key Skills |
| --- | --- | --- | --- |
| PM | `ProductManager` | gemini-3-pro-preview | research-engineer, writing-plans, tdd-workflow |
| Architect | `SystemArchitect` | gemini-3-pro-preview | ai-agents-architect, architecture-patterns, langchain-architecture |
| Coder | `SoftwareEngineer` | gemini-3-flash-preview | clean-code, python-pro, langgraph, mcp-builder |
| QA | `QualityAssurance` | gemini-3-flash-preview | research-engineer, uv-package-manager, langgraph |

## 3. Memory Architecture

- **Workflow Context (Short-term)**: `AgentState.messages` — wiped on workflow end.
- **Project Memory (Long-term)**: RAG over `../dlamp` — persists across workflows.
- **Episode Log**: `.agent/episodes.json` — structured history of decisions.

## 4. Nine Workflow Diagrams

---

### Scheme 1 — Hierarchical / Waterfall

#### 1-1: Requirement Handover

```mermaid
sequenceDiagram
    participant PM as ProductManager
    participant AR as SystemArchitect
    participant CD as SoftwareEngineer
    participant QA as QualityAssurance

    PM->>PM: Draft PRD
    PM-->>AR: Inform (PRD locked)
    PM-->>CD: Inform (PRD locked)
    PM-->>QA: Inform (PRD locked)
    Note over PM: A/R — result broadcast, no feedback loop
```

#### 1-2: Design-to-Code Handover

```mermaid
sequenceDiagram
    participant PM as ProductManager
    participant AR as SystemArchitect
    participant CD as SoftwareEngineer

    AR->>AR: Translate PRD → Tech Spec
    PM-->>AR: Monitor (no intervention)
    AR-->>CD: Inform (Tech Spec delivered)
    Note over AR: R — PM is A (monitors outcome)
```

#### 1-3: Code Delivery

```mermaid
sequenceDiagram
    participant AR as SystemArchitect
    participant CD as SoftwareEngineer
    participant QA as QualityAssurance

    CD->>CD: Implement to Tech Spec
    CD->>QA: Submit code (handover)
    Note over QA: A/R — accountability shifts to QA
    QA->>QA: Execute test suite
```

---

### Scheme 2 — Collaborative / Agile

#### 2-1: Joint Requirement Analysis

```mermaid
sequenceDiagram
    participant PM as ProductManager
    participant AR as SystemArchitect
    participant CD as SoftwareEngineer
    participant QA as QualityAssurance

    PM->>AR: Request feasibility review
    PM->>CD: Request effort estimate
    PM->>QA: Request risk assessment
    AR-->>PM: Feasibility + constraints
    CD-->>PM: Story points / blockers
    QA-->>PM: Test scope / risks
    PM->>PM: Consolidate → finalize PRD
    Note over PM: A/R — synthesizes all inputs
```

#### 2-2: Dev-Test Loop (TDD)

```mermaid
sequenceDiagram
    participant CD as SoftwareEngineer
    participant QA as QualityAssurance

    loop Until all tests pass
        CD->>QA: Request test cases for feature
        QA-->>CD: Return test cases
        CD->>CD: Implement to pass tests
        CD->>QA: Run tests
        QA-->>CD: Pass / Fail report
    end
    Note over CD: R — QA is C (tight feedback)
```

#### 2-3: Agile Sign-off

```mermaid
sequenceDiagram
    participant PM as ProductManager
    participant QA as QualityAssurance

    QA->>QA: Final integration tests
    QA->>PM: Demo + acceptance criteria
    alt Accepted
        PM-->>QA: ✅ Sign-off
    else Rejected
        PM-->>QA: ❌ Revise (back to 2-2)
    end
    Note over QA: R → PM is A (fast acceptance)
```

---

### Scheme 3 — Critic / Supervisor

#### 3-1: Spec Lockdown

```mermaid
sequenceDiagram
    participant PM as ProductManager
    participant AR as SystemArchitect

    PM->>AR: Initial concept / idea
    AR->>AR: Formalize → Architecture Constraints Doc
    AR->>PM: Present locked constraints
    alt PM approves
        PM-->>AR: ✅ Sign-off → constraints frozen
    else PM rejects
        PM-->>AR: ❌ Revise constraints
    end
    Note over AR: R — PM is A (signs off freeze)
```

#### 3-2: Review Tribunal

```mermaid
sequenceDiagram
    participant CD as SoftwareEngineer
    participant QA as QualityAssurance
    participant AR as SystemArchitect

    CD->>QA: Submit Pull Request
    QA->>QA: Static analysis + test run (Prosecutor)
    QA->>CD: Challenge: "Explain [issue X]"
    CD-->>QA: Defense / justification
    QA->>AR: Review report + verdict recommendation
    alt AR: Merge
        AR-->>CD: ✅ LGTM — merge
    else AR: Reject
        AR-->>CD: ❌ Reject — trigger 3-3
    end
    Note over AR: A (Judge) | QA: R (Prosecutor) | CD: C (Defendant)
```

#### 3-3: Refactoring Loop

```mermaid
sequenceDiagram
    participant AR as SystemArchitect
    participant CD as SoftwareEngineer
    participant QA as QualityAssurance

    AR->>CD: Rejection rationale + violation points
    loop Until re-approved
        CD->>CD: Refactor (not just bug-fix)
        CD->>QA: Re-submit PR
        QA->>AR: Updated review report
        AR-->>CD: Merge OR Reject again
    end
    Note over AR: A (commands) | CD: R (executes)
```

---

## 5. Meta-Orchestration Flow

```mermaid
flowchart TD
    START([User Intent]) --> ORCH[Meta-Orchestrator\n sequential-thinking]
    ORCH -->|simple/clear scope| W1[Scheme 1: Waterfall\n1-1 → 1-2 → 1-3]
    ORCH -->|complex/iterative| W2[Scheme 2: Agile\n2-1 → 2-2 → 2-3]
    ORCH -->|critical/security| W3[Scheme 3: Critic\n3-1 → 3-2 → 3-3]
    ORCH -->|agent-evaluated next workflow| WE[agent-evaluation\nNo write to target]
    W1 --> END([Episode Log])
    W2 --> END
    W3 --> END
    WE --> END
```

## 6. Implementation Phases

| Phase | Deliverable |
| --- | --- |
| 1 | `src/arkhon_rheo/roles/` — BaseRole + 4 role classes |
| 2 | `src/arkhon_rheo/workflows/hierarchical/` — 1-1, 1-2, 1-3 |
| 3 | `src/arkhon_rheo/workflows/collaborative/` — 2-1, 2-2, 2-3 |
| 4 | `src/arkhon_rheo/workflows/critic/` — 3-1, 3-2, 3-3 |
| 5 | `src/arkhon_rheo/orchestrator/` — Meta-Orchestrator + Memory |

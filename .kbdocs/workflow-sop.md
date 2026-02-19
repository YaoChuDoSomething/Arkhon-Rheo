# Workflow SOP

為了將上述的文字邏輯轉化為視覺化的 SOP，我使用 **Mermaid 流程圖** 來呈現這三種方案的運作機制。這些圖表可以直接嵌入到您的技術文件（如 Notion, GitHub Markdown）中。

以下是針對三種方案的 **SOP 流程示意圖** 與 **關鍵節點說明**：

---

## 第一類：層級式瀑布流 (Scheme 1: Hierarchical)

**特徵：** 單向流動，無回頭路，強調文件交付 (Document-Driven)。

```mermaid
graph TD
    %% Optimized Hierarchical Workflow (Waterfall)
    
    %% Node Definitions with Icons
    PM[<center><b>PM</b><br/>📝 PRD 廣播</center>]
    Arch[<center><b>Architect</b><br/>🏗️ Tech Spec 交付</center>]
    Coder[<center><b>Coder</b><br/>💻 核心實作</center>]
    QA[<center><b>QA</b><br/>🔍 驗收測試</center>]
    
    Start((<b>Project Start</b>))
    End((<b>Release</b>))

    %% Flow Structure
    Start --> PM
    PM -- "Inform (R-I)" --> Arch
    PM -. "Broadcast" .-> Coder
    PM -. "Broadcast" .-> QA
    
    Arch -- "Handover (Spec)" --> Coder
    Coder -- "Handoff (Code)" --> QA
    QA --> End

    %% Professional Styling
    classDef roles fill:#f9f9f9,stroke:#333,stroke-width:2px,color:#333;
    classDef highlight fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef startnode fill:#c8e6c9,stroke:#2e7d32;
    classDef endnode fill:#ffcdd2,stroke:#c62828;

    class PM,Arch,Coder,QA roles;
    class Arch highlight;
    class Start startnode;
    class End endnode;
```

**SOP 執行重點：**

1. **觸發點：** 文件的產生（PRD, Tech Spec）。
2. **檢核點：** 無中間檢核，直到最後 QA 階段。
3. **異常處理：** 若 QA 發現嚴重錯誤，通常需重開一張 Ticket 回到起點，而非在流程內直接折返。

---

## 第二類：協作迭代式 (Scheme 2: Collaborative)

**特徵：** 雙向溝通，測試驅動，強調共識 (Consensus-Driven)。

```mermaid
graph LR
    %% Optimized Collaborative Workflow Overview (Scheme 2)
    
    subgraph S1 [Phase 1: Alignment]
        direction TB
        PM[<center><b>PM</b><br/>💡 草案提出</center>]
        Team[<center><b>技術團隊</b><br/>🛠️ 可行性評估</center>]
        PM <==> |"諮詢與回饋 (C)"| Team
    end

    subgraph S2 [Phase 2: TDD Cycle]
        direction TB
        QA[<center><b>QA</b><br/>📜 測試案例</center>]
        Coder[<center><b>Coder</b><br/>🏗️ 實作與重構</center>]
        QA --> |"定義驗收基準"| Coder
        Coder --> |"自動化驗對"| QA
        Coder -- "Loop" --> Coder
    end

    subgraph S3 [Phase 3: Demo]
        direction TB
        Demo[<center><b>Demo</b><br/>🤝 敏捷驗收</center>]
        Sign((<b>Release</b>))
        Demo --> |"Approve"| Sign
    end

    S1 --> S2 --> S3
    S3 -- "Iterate" --> S1

    %% Styling
    classDef agilePhase fill:#fffde7,stroke:#fbc02d,stroke-width:1px,stroke-dasharray: 5 5;
    classDef agileActor fill:#fff,stroke:#fdd835,stroke-width:2px;
    class S1,S2,S3 agilePhase;
    class PM,Team,QA,Coder,Demo agileActor;
```

```mermaid
graph TD
    %% Detailed Agile Dev-Test Loop (Scheme 2 Detail)
    
    Start((需求定稿)) --> QAC[<center><b>QA</b><br/>📜 測試案例撰寫</center>]
    
    subgraph TDD [核心 TDD 循環 / Sprint]
        direction TB
        QAC --> Code[<center><b>Coder</b><br/>🏗️ 實作代碼</center>]
        Code --> Test{通過測試?}
        Test -- "No (Fail)" --> Fix[<center>🔧 修正代碼</center>]
        Fix --> Code
        Test -- "Yes (Pass)" --> Demo[<center><b>Demo</b><br/>🤝 敏捷驗收</center>]
    end
    
    Demo --> Decision{PM 滿意?}
    Decision -- "No (調整需求)" --> QAC
    Decision -- "Yes" --> Release((🚀 完成發布))

    %% Styling
    classDef loop fill:#f1f8e9,stroke:#558b2f,stroke-width:2px;
    classDef actor fill:#fff,stroke:#fbc02d,stroke-width:2px;
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    class TDD loop;
    class QAC,Code,Demo,Fix actor;
    class Test,Decision decision;
```

**SOP 執行重點：**

1. **觸發點：** 對話與諮詢請求。
2. **迴圈機制：** `Flow 2-2` 是最核心的自動化迴圈，Coder 必須跑通 QA 的測試腳本才能進入下一步。
3. **異常處理：** 錯誤在開發中即時修正，不累積到最後。

---

## 第三類：雙重驗證/審查者模式 (Scheme 3: Critic/Supervisor)

**特徵：** 嚴格關卡，權責分立，強調合規 (Compliance-Driven)。

```mermaid
graph TD
    %% Optimized Supervisor Workflow (Scheme 3 Detail)

    subgraph Lockdown [1. 規格鎖定 Lockdown]
        PM[<b>PM</b><br/>提出需求] --> ArchL[<b>Arch</b><br/>定義強規範]
        ArchL --> Lock{合規鎖定}
    end

    subgraph Tribunal [2. 審查審判 Tribunal]
        Coder[<b>Coder</b><br/>提交 PR] --> QA[<b>QA</b><br/>掃描異常]
        QA -- "提交報告" --> ArchJ[<b>Arch</b><br/>判決與裁定]
        
        ArchJ --> Verdict{判決結果}
    end

    subgraph Recovery [3. 強制重構 Recovery]
        Verdict -- "Reject (退回)" --> Fix[<b>Coder</b><br/>強制重構]
        Fix -- "重新提交" --> QA
    end

    Verdict -- "Merge (通過)" --> Deploy((合併代碼))

    %% Expert Styling
    classDef gatekeeper fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
    classDef worker fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef gold fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    
    class ArchL,ArchJ,QA gatekeeper;
    class Coder,Fix worker;
    class PM gold;
    style Verdict fill:#ffecb3,stroke:#ffa000,stroke-width:4px;
    style Lock fill:#ffecb3,stroke:#ffa000,stroke-width:2px;
```

**SOP 執行重點：**

1. **觸發點：** Pull Request (PR) 提交。
2. **角色權力：** Architect 擁有絕對否決權（Veto Power）。
3. **異常處理：** `Flow 3-3` 是強制性的懲罰迴圈，必須直到 Architect 滿意為止，否則無法進入部署階段。

---

### 總結：如何將圖表轉化為 Agent 指令

在實作自動化 Agent 時，您可以根據上述流程圖設定 **State Machine (狀態機)** 的轉移條件：

* **Scheme 1 (Waterfall):** 線性狀態機。
* `State: Idle` -> `Event: Receive_Doc` -> `State: Working` -> `Event: Complete` -> `State: Handover`.

* **Scheme 2 (Collaborative):** 帶有通訊的狀態機。
* `State: Coding` 必須包含 `Action: Request_Test_Case`。
* 轉移條件是 `Pass_Rate == 100%`。

* **Scheme 3 (Supervisor):** 條件判斷狀態機。
* 核心在於 `Verdict` 節點。
* `If (QA_Score < Threshold) OR (Arch_Review == Reject)` THEN `Goto: Refactor_State`.

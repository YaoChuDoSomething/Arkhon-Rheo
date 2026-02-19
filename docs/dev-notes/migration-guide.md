---
description: AI-Agentic System Builder depend on Agentic-Skills
---

# 建構AI代理人系統 [AI-Agentic System]

根據提供的資源，建構一個穩健且生產級的代理人系統（Agent System）並非單一技能可以完成，而是需要結合架構設計、核心組件構建、工作流程編排以及評估測試等多個維度的技能。

以下是根據「Antigravity Agentic Skills Directory」整理出最適合建構代理人系統的技能組合建議：

## **1. 核心架構與設計 (The Brain & Blueprint)**

這部分決定了代理人如何思考、規劃以及系統的整體藍圖。

* **`ai-agents-architect`**：這是最核心的技能。負責自主代理的總體設計，精通工具使用、記憶體系統、規劃策略以及多代理編排。
* **`autonomous-agents`**：專注於代理的內部循環（如 ReAct、Plan-Execute 循環）和目標分解。此技能強調「可靠性」，解決錯誤累積會導致代理失敗的問題。
* **`multi-agent-patterns`**：如果您的系統涉及多個代理協作，此技能涵蓋主編排器 (Master Orchestrator)、點對點 (P2P) 和分層架構的設計模式。

## **2. 開發框架與實作 (The Skeleton)**

選擇正確的框架來落實設計。

* **`langgraph`**：目前被推薦為建構「有狀態」（Stateful）、多參與者 AI 應用的生產級框架。它支援循環（Loops）、分支和持久化，是將代理從簡單腳本轉化為複雜應用的關鍵。
* **`langchain-architecture`**：用於設計代理架構的通用模式，整合代理、記憶體和工具。
* **`ai-engineer`**：負責將這些設計轉化為生產級代碼，整合向量搜尋和多模態能力。

## **3. 記憶與上下文管理 (The Memory)**

沒有記憶的代理每次互動都會歸零，無法處理複雜任務。

* **`agent-memory-systems`**：這是智慧體的基石。涵蓋短期記憶（上下文視窗）與長期記憶（向量儲存）的架構，以及決定代理「記住或遺忘」的檢索策略。
* **`context-manager`**：負責動態管理上下文，確保在多代理工作流程和長期專案中，資訊流不會中斷或「腐爛」。
* **`context-window-management`**：專門處理 LLM 上下文視窗的限制，透過摘要和修剪策略來優化 Token 使用效率。

## **4. 工具與互動能力 (The Hands)**

代理需要工具才能與外部世界互動。

* **`agent-tool-builder`**：極為關鍵的技能。重點在於設計高品質的工具描述（如 JSON Schema），因為「工具描述比工具實作更重要」，設計不良的工具會導致代理產生幻覺或失敗。
* **`mcp-builder`**：建立符合模型上下文協定（MCP）的伺服器，這是讓 LLM 連接外部服務和資料的新興標準介面。
* **`context7-auto-research`**：透過 Context7 API 自動取得要調查的最新庫/框架文檔 (id/lib/doc)

## **5. 穩定性與工作流程 (The Nervous System)**

確保代理在遇到錯誤或網路問題時能恢復，而不是崩潰。

* **`workflow-automation`**：代理可靠性的基礎設施。使用如 Temporal 或 n8n 等工具，確保長流程（如 10 步驟的任務）具有持久執行能力，發生故障時可從斷點恢復。
* **`agent-orchestration-multi-agent-optimize`**：透過成本感知編排和工作負載分配，優化多代理系統的吞吐量與穩定性。

## **6. 評估與監控 (The Quality Control)**

代理系統往往不可預測，需要嚴格的測試。

* **`agent-evaluation`**：對代理進行行為測試、能力評估和基準測試。資源指出，即使是頂尖代理在真實世界基準測試中也常達不到 50% 的成功率，因此此技能不可或缺。
* **`langfuse`**：提供 LLM 的可觀測性（Observability），包括追蹤（Tracing）、提示管理和評估，幫助開發者看見代理內部的思考過程。
* **`agent-orchestration-improve-agent`**：透過性能分析和持續迭代，系統化地改進現有代理的表現。

**總結建議：**
若要組建一個最小可行性（MVP）的代理人開發團隊，建議至少需要掌握

1. **`ai-agents-architect`**（架構）
2. **`langgraph`**（實作）
3. **`agent-tool-builder`**（工具）
4. **`agent-memory-systems`**（記憶）
5. **`agent-evaluation`**（測試）

以上這五項核心技能。

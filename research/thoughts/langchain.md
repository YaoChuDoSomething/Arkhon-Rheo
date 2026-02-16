# LangGraph

```mermaid
graph TD
    %% Define Styles
    classDef control fill: #f9f, stroke: #333, stroke-width: 2px, color: black;
    classDef input fill: #ccf, stroke: #333, stroke-width: 1px, color: black;
    classDef logic fill: #ff9, stroke: #333, stroke-width: 2px, color: black;
    classDef storage fill: #afa, stroke: #333, stroke-width: 1px, color: black;
    classDef monitor fill: #faa, stroke: #333, stroke-width: 1px, color: black;

    %% External User Layer
    User(("使用者/學生")):::input

    %% Deployment Layer (LangServe)
    subgraph "Deployment (The Classroom)"
        LangServe[LangServe API]:::input
    end

    %% Monitoring Layer (LangSmith)
    subgraph "Evaluation & Optimization (The Teacher's Review)"
        LangSmith[LangSmith]:::monitor
        Datasets[("黃金數據集")]:::storage
    end

    %% Core Orchestration Layer (LangGraph)
    subgraph "Orchestration (The Logic of Guidance)"
        direction TB
        LangGraph(("LangGraph 狀態機")):::control
        
        %% Internal Nodes
        Node_Reasoning["LLM 推理節點"]:::logic
        Node_Tool["工具調用節點"]:::logic
        Node_Reflection["反思/修正節點"]:::logic
        
        %% Memory
        Memory["Checkpointers (短期記憶/黑板)"]:::storage
    end

    %% Infrastructure Layer (LangChain Core)
    subgraph "Resources (The Textbook & Tools)"
        Prompt["Prompt Templates (提問框架)"]:::input
        RAG["Retriever / Vector Store (外部知識庫)"]:::storage
        ExternalTools["Google Search / Calc (計算機與工具)"]:::logic
    end
    
    %% Connections
    User -->|提問| LangServe
    LangServe -->|輸入| LangGraph

    %% LangGraph Internal Logic
    LangGraph -->|1. 規劃路徑| Node_Reasoning
    Node_Reasoning -->|需要資料?| Node_Tool
    Node_Tool -->|2. 查閱| RAG
    Node_Tool -->|2. 操作| ExternalTools
    RAG & ExternalTools -->|返回結果| Node_Reasoning
    
    Node_Reasoning -->|3. 產生答案| Node_Reflection
    Node_Reflection -->|品質不佳?| LangGraph
    LangGraph -->|重新引導| Node_Reasoning
    
    Node_Reflection -->|品質合格| LangServe
    LangServe -->|最終回答| User

    %% Monitoring Connections
    LangGraph -.->|Trace Log| LangSmith
    Node_Reasoning -.->|Token Usage| LangSmith
    LangSmith -.->|優化 Prompt| Prompt

    %% Apply Link Styles
    linkStyle default stroke-width: 2px, fill: none, stroke: #333;
```

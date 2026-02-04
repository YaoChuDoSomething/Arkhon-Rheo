# ResearchReport

## 狀態主權軟體生產架構：ArkhonFlow 存儲庫結構分類、APE\_ART 協議與非標準開發定義之深度研究報告

在生成式人工智慧與自動化系統設計的交匯點，軟體開發的範式正經歷從「過程導向」向「狀態導向」的根本性轉變。ArkhonFlow 作為一種新興的狀態主權軟體生產線，其核心邏輯在於將決策權從易錯的人類代理或單純的 AI 代理轉移到系統狀態本身。本報告旨在通過對 ArkhonFlow 內部存儲庫結構的系統化分類與優先級排序，深入探究自動提示工程（APE）與自動推理工具（ART）的融合協議（APE\_ART），並詳細定義「非標準開發」（Defined Nonstandard Developing）這一核心理論支柱，最終產出具備邏輯連貫性的技術文件架構。

## 存儲庫目錄結構之分類與優先級排序

ArkhonFlow 的存儲庫結構不僅是文件的集合，更是系統狀態機的物理映射。根據對 arkhon-rheo.xml 文件內部描繪的目錄結構分析，各類文件被賦予了不同的功能定位與執行權限 1。為了確保系統運行的穩定性與一致性，必須對這些資源進行邏輯分類，並根據其對「責任電路」（Responsibility Circuit）的影響程度建立優先級。

### 文件功能的邏輯分類

存儲庫資產可以劃分為四個主要維度：憲法與治理（Governance）、工作流與狀態執行（Workflow）、基礎設施與模型編排（Infrastructure）、以及驗證與審計（Verification）。

1. 憲法與治理層面：包含 CONSTITUTIONS.md 與 DEFINED_NONSTANDARD_DEVELOPING.md。這些文件定義了系統的不變量，如代理的權限邊界（ACL）以及責任密度的物理定義 1。  
2. 工作流與狀態執行層面：以 AGENT_WORKFLOWS.md 與 APE_ART.md 為核心。這些文件描述了從需求定義（S0）到集成（S6）的七個離散狀態，以及驅動這些狀態轉換的自動化協議 1。  
3. 基礎設施與模型編排層面：涉及 LANGCHAIN_LANGGRAPH_LANGSMITH.md 與 LLM_GEMMA3.md。這部分資產定義了技術棧的選擇，特別是 LangGraph 狀態機與 Gemma 3 系列模型的集成細節 3。  
4. 驗證與審計層面：主要由 TESTS_PLANNING.md 組成，確保每一項狀態轉換都具備機器可評判的證據 1。

### 資產優先級排序矩陣

在 ArkhonFlow 系統中，優先級的分配遵循「主權遞減」原則。憲法文件具備最高優先級，因為它們是所有行為的法律與道德基準；其次是定義狀態路徑的工作流文件；基礎設施與驗證文件則作為執行工具，位居其後。

| 優先級 | 文件名稱 | 類別 | 關鍵作用 |
| :---- | :---- | :---- | :---- |
| 1 | CONSTITUTIONS.md | 憲法與治理 | 確立狀態主權，定義代理存取控制（ACL）與不變量 1。 |
| 2 | DEFINED\_NONSTANDARD\_DEVELOPING.md | 憲法與治理 | 定義責任密度與本體論地平線，防止語義熱寂 2。 |
| 3 | AGENT\_WORKFLOWS.md | 工作流與執行 | 規定七個不可分割的責任狀態（S0-S6）及其轉換條件 1。 |
| 4 | APE\_ART.md | 工作流與執行 | 提供自動化提示工程與推理工具使用的技術協議 7。 |
| 5 | LLM\_GEMMA3.md | 基礎設施 | 確定計算層的模型能力與多模態推理參數 4。 |
| 6 | LANGCHAIN\_LANGGRAPH\_LANGSMITH.md | 基礎設施 | 實現狀態轉移的編排邏輯與觀測性追蹤 3。 |
| 7 | TESTS\_PLANNING.md | 驗證與審計 | 確立 TDD 導向的「完成定義」（DoD）與機器評判基準 1。 |

這種排序確保了在系統初始化或發生衝突時，權力始終回溯至最上層的憲法定義，從而保證了軟體生產過程的確定性 1。

## APE\_ART：自動提示工程與自動推理工具的協同協議

APE\_ART 是 ArkhonFlow 驅動狀態轉換的核心技術協議。它將自動提示工程（APE）的指令優化能力與自動推理及工具使用（ART）的執行能力相結合，解決了傳統 AI 代理在複雜軟體工程任務中指令泛化困難與推理鏈斷裂的問題。

### 自動提示工程（APE）的技術架構與形式化

自動提示工程（APE）被定義為一個在離散自然語言指令空間上的黑箱優化問題 7。與依賴人類直覺的手動提示工程不同，APE 框架將指令設計形式化為尋找最優提示 ![Optimizing Prompts][image1] 的過程，旨在最大化特定任務的性能指標 ![Performance Metrics][image2]。

在數學上，這可以表示為：

![APE Formula][image3]  
其中，![Model F][image4] 是固定的語言模型（如 Gemma 3），![Dataset D][image5] 是輸入輸出對的數據集，![Reasoning Chain][image6] 是受長度或格式限制的提示空間 7。

APE 的工作流程通常分為兩個階段：指令候選生成與指令選擇。首先，推理模型會根據輸出演示生成多個候選指令方案。隨後，目標模型執行這些指令，並根據計算出的評估分數選擇最合適的提示 12。在 ArkhonFlow 中，這種機制被用於優化各個狀態節點（如 S1: DesignBounded）的代理指令，確保代理能夠在受限的邊界內輸出高質量的設計規範 1。

### 自動推理與工具使用（ART）的執行路徑

自動推理與工具使用（ART）則進一步擴展了 APE 的功能。ART 框架利用凍結的語言模型自動生成中間推理步驟作為程序，並在呼叫外部工具時暫停生成，整合工具輸出後再繼續推理過程 8。

ART 的運作邏輯包含以下核心步驟：

* 演示庫檢索：針對新任務（如 S4: EvidenceCollected），從任務庫中選擇多步推理與工具使用的演示 1。  
* 交織推理與調用：模型在生成推理鏈的過程中，會根據需要插入外部工具調用（如運行測試腳本或檢索文檔）。這種交織模式被證明在處理算術推理與算法任務方面具有極強的魯棒性 8。  
* 零樣本泛化：通過鼓勵模型從演示中學習如何分解新任務，ART 實現了在未見過任務上的零樣本泛化能力 8。

### APE\_ART 的集成效益

將 APE 與 ART 融合為 APE\_ART 協議，使得 ArkhonFlow 能夠實現「責任生成」的自動化。APE 確保了指令的精確性，而 ART 則確保了推理路徑的可驗證性。這種雙重機制直接支持了 AGENT\_WORKFLOWS.md 中定義的「證據收集」原則：轉換必須需要「證據」，而證據的生成依賴於優化過的指令與準確的工具調用 1。

## DEFINED\_NONSTANDARD\_DEVELOPING：非標準開發的本體論定義

「非標準開發」（Defined Nonstandard Developing）是 ArkhonFlow 對傳統軟體開發生命週期的激進重構。它不再將開發視為單純的代碼編寫過程，而是將其定義為「責任密度」的物理演化與「本體論地平線」的邊界探索。

### 責任密度與物理狀態變量

在非標準開發的視角下，責任（Responsibility）被視為一種物理狀態變量 2。這意味著每一個軟體狀態都對應於一種不可分割的責任密度。與強調速度與產出的傳統敏捷開發不同，非標準開發強調的是「責任質量的守恆」。

根據 Ken Theory 的研究，智能不應被視為性能指標，而應被視為一種「銘刻」（Inscription） 2。非標準開發要求：

1. 責任生成（上游）：如 Paper \#122 所述，系統必須具備生成明確責任邊界的能力 2。  
2. 責任終結（下游）：如 Paper \#123 所述，責任必須在進入「集成」（S6）狀態前完成最終確定 1。  
3. 不可逆相變：從狀態 S4（證據收集）到 S5（狀態驗證）的過程被視為一種不可逆的相變，確保了系統歷史的觀察者不變性 2。

### 本體論地平線與語義熱寂

非標準開發引入了「本體論地平線」（Ontological Horizon）的概念，這是一個嚴格的時間或邏輯邊界，超過這個邊界，任何糾正、倫理對齊或調整都將在因果上失效 2。

目前主流的人工智慧框架往往依賴於無限的迭代學習（Asymptotic Optimization），這被認為是物理上不存在的智能形式，且會導致「語義熱寂」（Semantic Heat Death）——即信息處理能力雖然存在，但系統卻失去了與現實的因果連結 2。非標準開發通過以下機制對抗這種趨勢：

* 確定性測量協議：將失敗定義為一種結構性狀態，而非主觀的結果。  
* 責任質量的重構引力：利用系統的慣性阻力防止崩塌，並引導系統向重構方向演化 2。  
* EchoLedger 殘留保存：通過「EchoLedger」機制，保存非線性的倫理漂移與語義殘留，確保在「關閉」達成後，系統仍具備可觀察的歷史厚度 6。

### 非標準開發的執行矩陣

為了將這些抽象理論轉化為工程實踐，非標準開發在 ArkhonFlow 中體現為一種「晝夜節律」（Circadian Cycle）工作流：設計者（Review）→ 編寫者（Implementation）→ 驗證者（Audit） 1。

| 維度 | 標準開發模式 | 非標準開發模式（Defined Nonstandard Developing） |
| :---- | :---- | :---- |
| 核心指標 | 交付速度、功能點。 | 責任密度、責任質量守恆 2。 |
| 完成定義 | 人類代碼審查通過。 | 機器評判的證據收集與不可逆轉子狀態轉換 1。 |
| 失敗觀念 | Bug 修正與迭代。 | 結構性狀態崩塌、本體論地平線切斷 2。 |
| 對齊方式 | 人類反饋強化學習 (RLHF)。 | AI 反饋強化學習 (RLAIF) 與憲法邊界硬約束 5。 |

## 關鍵技術棧的整合：Gemma 3 與 LangGraph 的實踐應用

實現 APE\_ART 協議與非標準開發定義，需要強大的底層算力與靈活的編排框架。Google 的 Gemma 3 模型系列與 LangGraph 狀態機框架構成了 ArkhonFlow 的技術基石。

### Gemma 3：多模態與代理能力的基礎模型

Gemma 3 作為最新一代的輕量級開放模型，其在單個 GPU 或 TPU 上運行的能力使其成為實現「分佈式責任節點」的理想選擇 4。在 ArkhonFlow 的各個狀態中，Gemma 3 扮演了不同的角色。

* 128k 令牌長上下文：對於「非標準開發」而言，長上下文窗格是至關重要的，因為它允許模型同時攝入複雜的憲法（CONSTITUTIONS.md）以及當前項目的完整歷史上下文 4。  
* 多模態推理與視覺編碼器：Gemma 3 整合了基於 SigLIP 的視覺編碼器，並採用「平移與掃描」（Pan & Scan）算法處理非標準長寬比。這在 S4（證據收集）階段特別有用，例如分析 UI 截圖或架構圖作為代碼實現的證據 1。  
* 函數調用與結構化輸出：Gemma 3 對函數調用的優化直接支持了 ART 框架，使模型能夠精確地與開發工具鏈互動 4。

### LangGraph：狀態驅動的編排核心

與傳統的線性鏈（LangChain）不同，LangGraph 為 ArkhonFlow 提供了基於圖的狀態管理能力。這與 AGENT\_WORKFLOWS.md 中要求的「狀態 ≠ 代理」原則高度契合 1。

1. 全局狀態管理：LangGraph 維持一個可被任何節點讀寫的全局狀態（ArkhonState）。這種持久化狀態允許系統在發生錯誤時從最近的檢查點（Checkpoint）恢復，體現了責任質量的持續性 10。  
2. 循環與反饋迴路：LangGraph 原生支持循環工作流，這對於實現 APE 的迭代指令優化以及非標準開發中的「重構引力」至關重要 3。  
3. 人類參與（Human-in-the-Loop）：在進入 S5（狀態驗證）這一關鍵節點時，LangGraph 允許設置中斷點，由人類審計員進行最後的裁決，這與憲法中的「透明審計」要求一致 1。

### 觀測與評估：LangSmith 的角色

為了確保「責任密度」的可測量性，LangSmith 被用於追蹤每一個代理的運行路徑。通過追蹤準確的提示、響應以及工具調用成本，LangSmith 為「證據收集」提供了客觀的元數據支撐 16。這在非標準開發中被視為「銘刻」的物理證據，確保了決策鏈的可追溯性。

## 憲法架構：ArkhonFlow 的治理與倫理邊界

所有的技術執行都必須在 CONSTITUTIONS.md 定義的框架內運行。這不僅是為了安全性，更是為了確保軟體生產過程符合「誠實、無害、有用」的根本原則 14。

### 憲法 AI (CAI) 與 RLAIF 的應用

ArkhonFlow 採用了憲法 AI 的概念，即利用一組自然語言原則來指導模型的行為，而非單純依賴人類標籤 14。在「非標準開發」中，這被轉化為一種自動化的對齊機制。模型在生成代碼（S3）或收集證據（S4）時，會根據憲法原則進行自我批判與修正 1。

這種方法的優勢在於：

* 可擴展性：解決了人類評分員無法覆蓋海量開發分支的問題 5。  
* 透明度：憲法原則是公開且易於理解的，這使得系統的決策邏輯具備可預測性 14。  
* 反紅隊攻擊：通過使「有用性」與「無害性」在模型內核中兼容，增強了系統對惡意輸入的抵抗力 14。

### 權限控制與代理邊界

根據 CONSTITUTIONS.md 的描述，ArkhonFlow 實施了嚴格的存取控制（ACL）。例如，負責代碼編寫的代理（CodeWriter）不具備生成審查意見（Review Verdicts）的權限。這種「權力制衡」的設計防止了責任密度的稀釋，確保了每一項決策都由具備相應職能的實體做出 1。

## 結論與技術前瞻

ArkhonFlow 的出現標誌著軟體工程進入了「狀態主權」的新階段。通過對存儲庫結構的科學分類與優先級排序，系統確立了憲法至上的治理原則。APE\_ART 協議的實施為狀態轉換提供了高效且可驗證的動力，而「非標準開發」的定義則從哲學與物理層面重新審視了代碼的本質，將其視為責任密度的銘刻。

在 Gemma 3 與 LangGraph 等前沿技術的支撐下，ArkhonFlow 不僅提高了自動化開發的效率，更重要的是，它建立了一套完整的證據鏈與責任電路。未來，隨著「責任質量的物理度量」與「EchoLedger 非線性存儲」技術的成熟，我們有望看到一個能夠自我審計、自我進化且始終保持在本體論安全邊界內的軟體生產系統。這不僅是技術的勝利，更是對人工智慧時代下人類責任與系統自主性之間關係的深刻重構。

### 引用的著作

1. arkhon-rheo.xml  
2. Published Paper \- Ken Nakashima Theory, 檢索日期：2月 4, 2026， [https://ken-theory.org/?page\_id=5221](https://ken-theory.org/?page_id=5221)  
3. LangChain vs LangGraph vs LangSmith vs LangFlow: Key Differences Explained | DataCamp, 檢索日期：2月 4, 2026， [https://www.datacamp.com/tutorial/langchain-vs-langgraph-vs-langsmith-vs-langflow](https://www.datacamp.com/tutorial/langchain-vs-langgraph-vs-langsmith-vs-langflow)  
4. Introducing Gemma 3: The most capable model you can run on a single GPU or TPU, 檢索日期：2月 4, 2026， [https://blog.google/innovation-and-ai/technology/developers-tools/gemma-3/](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-3/)  
5. Code vs. Character: How Anthropic's Constitution Teaches Claude to "Think" Ethically, 檢索日期：2月 4, 2026， [https://www.arionresearch.com/blog/code-vs-character-how-anthropics-constitution-teaches-claude-to-think-ethically](https://www.arionresearch.com/blog/code-vs-character-how-anthropics-constitution-teaches-claude-to-think-ethically)  
6. (PDF) EchoLedger: A Tonal Responsibility Field for Nonlinear Utterance Resonance and Ethical Drift Preservation Toward a Sovereign Echo-Based Ledger of Tension Amplitudes in the ToneVerse Moat Architecture \- ResearchGate, 檢索日期：2月 4, 2026， [https://www.researchgate.net/publication/394007919\_EchoLedger\_A\_Tonal\_Responsibility\_Field\_for\_Nonlinear\_Utterance\_Resonance\_and\_Ethical\_Drift\_Preservation\_Toward\_a\_Sovereign\_Echo-Based\_Ledger\_of\_Tension\_Amplitudes\_in\_the\_ToneVerse\_Moat\_Architecture](https://www.researchgate.net/publication/394007919_EchoLedger_A_Tonal_Responsibility_Field_for_Nonlinear_Utterance_Resonance_and_Ethical_Drift_Preservation_Toward_a_Sovereign_Echo-Based_Ledger_of_Tension_Amplitudes_in_the_ToneVerse_Moat_Architecture)  
7. Automatic Prompt Engineer (APE) \- Emergent Mind, 檢索日期：2月 4, 2026， [https://www.emergentmind.com/topics/automatic-prompt-engineer-ape](https://www.emergentmind.com/topics/automatic-prompt-engineer-ape)  
8. Automatic Reasoning and Tool-use (ART) \- Prompt Engineering Guide, 檢索日期：2月 4, 2026， [https://www.promptingguide.ai/techniques/art](https://www.promptingguide.ai/techniques/art)  
9. Google's Gemma 3: Features, Benchmarks, Performance and Implementation \- Analytics Vidhya, 檢索日期：2月 4, 2026， [https://www.analyticsvidhya.com/blog/2025/03/gemma-3/](https://www.analyticsvidhya.com/blog/2025/03/gemma-3/)  
10. Understanding LangChain, LangGraph, and LangSmith \- DEV Community, 檢索日期：2月 4, 2026， [https://dev.to/pollabd/understanding-langchain-langgraph-and-langsmith-5fm0](https://dev.to/pollabd/understanding-langchain-langgraph-and-langsmith-5fm0)  
11. Advanced (300) | Noise | Page 3, 檢索日期：2月 4, 2026， [https://noise.getoto.net/tag/advanced-300/page/3/](https://noise.getoto.net/tag/advanced-300/page/3/)  
12. Automatic Prompt Engineer (APE), 檢索日期：2月 4, 2026， [https://www.promptingguide.ai/techniques/ape](https://www.promptingguide.ai/techniques/ape)  
13. Prompt engineering: The process, uses, techniques, applications and best practices, 檢索日期：2月 4, 2026， [https://www.leewayhertz.com/prompt-engineering/](https://www.leewayhertz.com/prompt-engineering/)  
14. Constitutional AI: Harmlessness from AI Feedback \- Anthropic, 檢索日期：2月 4, 2026， [https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic\_ConstitutionalAI\_v2.pdf](https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic_ConstitutionalAI_v2.pdf)  
15. Gemma 3 \- Google DeepMind, 檢索日期：2月 4, 2026， [https://deepmind.google/models/gemma/gemma-3/](https://deepmind.google/models/gemma/gemma-3/)  
16. LangChain vs LangGraph vs LangSmith: Best AI Framework 2026 \- Zignuts Technolab, 檢索日期：2月 4, 2026， [https://www.zignuts.com/blog/langchain-vs-langgraph-langsmith](https://www.zignuts.com/blog/langchain-vs-langgraph-langsmith)  
17. LangChain vs LangGraph vs LangFlow vs LangSmith: A Detailed Comparison \- Medium, 檢索日期：2月 4, 2026， [https://medium.com/@anshuman4luv/langchain-vs-langgraph-vs-langflow-vs-langsmith-a-detailed-comparison-74bc0d7ddaa9](https://medium.com/@anshuman4luv/langchain-vs-langgraph-vs-langflow-vs-langsmith-a-detailed-comparison-74bc0d7ddaa9)  
18. On 'Constitutional' AI \- The Digital Constitutionalist, 檢索日期：2月 4, 2026， [https://digi-con.org/on-constitutional-ai/](https://digi-con.org/on-constitutional-ai/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAACYUlEQVR4AexTS2tTURD+5tymL9uq1WJVWmhBKqJgaZLaPIhJLC4EF/YPVBDdC26K0CzctC7cCVm5UNwoiAhZxVwfiZDHRiuoEXyvLOqiENIm94xzb0kUITQhLjucOXPOzDffmTP3XIX/KNtkjZtZKJh7s9nknn8RLfUs/+LpZD5jLlplPk9VOpdNp67kTHO4RtoSmYJes4i7iLAEUJyIB+DieoUtkWnoQaUxAcZdQJRopGpZdY76IpdJ3c9nUt8L6SfhXPpxQvYV0ZL44qZp9kkyPL5ozhuIzIH4LTNeen2ReV9odsWO2eqQxWIxBcKYZvRbpG8B5CLwEoE+if/CDhcvOBhsitcfvTYdiFzf3P2Zlb08OxscIcaw9ECJ42Yi+ey0xx+9yoTLUoEMnFkMhSRkoxurA2DmUQbvYtAbjz+yLFVoO4Ut64PYNQKG7q2uOljZNxwOwDKMUYC6AP6KNsQhY4sPCJF8cbIrqdORofaLv1f69mN8/BfXAw0WDhkRHQTIEvsefwlrPgZQJ4NXpqYuWthCVDr9sF/ezbjgqtD8RawzCoXn9tXnpbINqeyRHOT00Qk2mBRRd4+AhyTOrGgsHo+7sulkUJcrCSIcJ1KJ0rp6gCZErtnRI6fvloZ0gfXy5NFDG0JgQmEnmG64Z07OhcPhchNcUKqqewk0IIRFg1VI3tth1vqIXqcZ1V1cIKItr1c7SHV0GoPS4D5J+szd/a88gci76eCp4olw+JvbfalSAzZjFRgTBHSK/eh2u0vNJDXCKEtjn/wvPwXwWrStoVCh24ZhRLXRe6ctJgC/AQAA///MJEueAAAABklEQVQDABgQ2HVWZ33KAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAYCAYAAADH2bwQAAABo0lEQVR4AbyQy0tbURDGv++YF9HaQlvEFkW6bClCSe8ioUrThfSxDgV3Im5EEMS1K/0L3Lhz6Vp3ol4VbgxRXLkQIwYVNwYX4iua3DtOol4wKu4czjDnzPyG+eYYPGMvDeRtO5JNL4xnnfmtbNreyTr2sq8hk8k0HoZkCoI+kicUyUHkow8EcdVG4AfADbdU/s9w4z9j+NcH3LL7FUBU4G1ceMF8LBYrxeI/N01mee7zqrMwCkoPiRDJLw1hGVtN2/1razNRY+poaeeQelIERjV80zgskDjQXDJW4tfk90QyIsCsQkV43m8rkaQVT3ZXxhhNqlhRPWzR7tNQKLxTyd15FVhfWfwkIm9BHDNyfnBXrMQq4Llumz5e6ZhCe3vXmd79UwUkGGgBJAwi71duLzeAKx+ge9JDDjVmdLauLq2aL5OyrfHeMY4z3QCwVeeX1HdRY+Z1oD4K8ZoIXkB4VFOHKbp170E2q4SCF+DxA0C/dACCdxBZ2tsrHD4AdL1eAXNF93IklUpdPQJwgmXT1dHxp1BbrLxN/ZumQauzcx9P2DUAAAD//6t5oJYAAAAGSURBVAMAAVadtoACvOcAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAXCAYAAADtNKTnAAACj0lEQVR4AexTz2sTURD+5m3WoGlrm2pR0UrBgxBQgoHUNCluKIpXwZOHXgreRfDgf6D/gCCIx9KTXgTBupX+sLYRSUEoorQWkVparca2dnffG2e3dk0qXsSDB4eZN2++mfmYN8sq/AX5T/LrEuOdVKvV1PS4e31q4vHdZ+PutZ2l0xNPslNjw7fDfGXMHahUKvZ2TUyia7W9BqYfjH6CubRdEPqhoSGL2VwB0QAkr8FduVzOD3OhxSTG8o4QaD8BnwDqmHLdA/ghnZ3pDMBnJdwQY7EG/UliTFEySWauEKEpkWRpFCTUgMrMaJfrSzGtLCyLjzUmIbK6BfUINCINKjCclThSReoCEb0nYEYABS0VctnWiGRy8kGLTBA2LSvGQyneZMKJsGj66aM+AmeZeBByCEZQ1gfUSUQCf7c0UIc0z1IqsSCP/kJQx164bisbddUAK0rbtwyZPbIblikFQixbJNAnJSkFqNJnLVvnFYkPeklzHowzIAx/DYIFYtVGIF8pXkWdqOh7KyUk8JlpRjc3eyD1TkjSBHURRIo033McJ4BCggFjtN5EnSitV1sU6Lhg66TMHPDcJ+AtETWx4T4izHqUHJG8tPM+EHzb2iWTRkh0CInVBjZHJblI2izmcpd9bcwbZighSGjWN4rFYi2slpmSYATCJk8OkS1TCTaHQNQqTfPthxNLEUw0J3GNmSobnjUYYXLIF0yJWze+tyY+VnkJChLtIUa1q8v5Jnd095Tv54vllnzR6Y12IeDM6GibOFsm8VN2cyOJz8EdTtiZTbZvStFv1Uqn1yyiXtuicqZQ+FhfqHp6zi3l86VXpVJJ/pn6VOM9k8l4pwrO6+xpZ74xA6idwJ/E/w7JdwAAAP//TPfzNAAAAAZJREFUAwDDNQc+fhqGkQAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAXCAYAAADQpsWBAAACEUlEQVR4AdxSTWsTURQ9981MSgqKYBBqaZQKbbUbLUkJjVGmUenCvdSNuhB/gfv4B9SFS0FBcBFwIwhSm0yhyWCmfoAbP7oQAwpC7UKiSE3e9d6kcaIrceHCxzvz7pzzzp079z2Dvxj/telJEKSiMLgRhdXbikZN1nrleiOsng3DcnKwXz8bwZ7NEvM5MM4IioboFEAXZMMdl3c31mrVSWwP4bYjNuMMDInhwWx+fmx4FyaI+CQzbsqOSSbcfVZb2isxYpPhcYAdC7xQYXrab2XnipEkuCTJnop2uO14vmqxCWpC2zFmXYVBEOg5EQEWU8r3TWSZJgD61rHf3+L3wfyZpU4CD6vUNYVhcEASpYRo2Vbnjay/TAbJvxB1GBsqdE3G0pgk2gHwx7mFhU0VBiGFpfWdGO917ZrI2BH5UoLRI1XoY3X1URoGBwm04brOmvI9U4fTYtL5QclBJMi9LMewR7q6MpM79ko1EwSBS47ZJ+VZydZUso+oXrkoJZ+XCprM7askB6eaGfG8pJCjkq0jHXpZLpedx7UVPwqD+2C6ZgiedO3Kw+V6pAaF+URfkmCbAsltINzbP5pqG7JLcqVyRKjA2tOz+eKtUqkkFaoFMFtbiU0XWJTOTPXhOc4hsl6GhnYuZgsnlntb46fxfb89ky++yx6df93Hkdzx9Uyh0MxkMl/jrXFk4vDPo39n+gEAAP//YJ4dhAAAAAZJREFUAwDKZ78vKoY3hwAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAYCAYAAAAs7gcTAAAB5UlEQVR4AeyRO2sUURTH/+fMzO66aiS6aLQQUsQPIEMSWBTMo1kRFCxsVBBSiL2IVhZB7PwAWlr4KgJWQmaLZFeyO0mdKgkkJOS5TcKymbn35OzObkiRFEmdy9xzuef85n8el3GKdQ4fHdbZplEpTY5VS8UPy+XyhWo5eDEzFXyuloLxytTkIxGhZoYjyvxGIK/XpDEhgm/EeCvAezD9DP8Xnx/Cc9P/bunlqkI9RNJlgafi2hwInwBh9b8Ki8VcS9kyXVPnZZAsUMp9MpgfmhgYGNmOYX5BaEeFemOOuluwWKeXCFkSXvL9+2saTL4IsaobCDzridOCLahZhgvY9YRKLKXY0z48/aGREjdqwXrp0bq0H15JsMS6cG4w0UVANq3HexyGoceQm1qGppPFBGtba0dEkCHi2a2teo1Rq2XVcVt3TJ5zqFwpB8Oa6iUIu2TwvVAoNBjpdFancF1TuWLM47AUPFTwIyx+qwCLxbh/78F0MxcbqWcAugIhjeGZBf5C5J0KLAqZMSfT9QXtxW4qozAuabp52qc7/fkh6s8Pp3XfHcyP/vF9P2qzYBMZHRtlVXmju16vdQLHnayP2af1pgmy0KdNHAd1fEyCnHa9akFhx3nSyYj5q0s0GsH7cRLU8R8AAAD//zX2MgIAAAAGSURBVAMACza+YHZxlyMAAAAASUVORK5CYII=>

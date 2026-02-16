# TODOLIST


```yaml

```

---

## SDLC in 6 Stages 

### 瀑布式

1. 規劃 (Planning)
這是最關鍵的基礎階段，開發團隊與利害關係人溝通，蒐集並定義軟體必須具備的功能、預算、時間表以及資源分配。 

2. 系統設計 (Design)
在此階段，架構師會根據需求規格，設計軟體的整體架構。這包括定義技術堆疊、資料庫結構、使用者介面 (UI) 和系統流程，並產出軟體設計說明書 (SDD)。 

3. 程式開發與實作 (Development / Implementation)
程式設計師開始編寫程式碼，將設計圖轉化為實際可運作的軟體模組。這是整個週期中工作量最密集的階段。 

4. 測試 (Testing)
品質保證 (QA) 團隊對軟體進行嚴格檢查，包含單元測試、整合測試及驗收測試。目標是找出並修正錯誤 (Bugs)，確保軟體穩定且符合需求。 

5. 部署 (Deployment)
當軟體經過測試並排除重大問題後，會正式發佈到生產環境（如雲端伺服器或應用程式商店），供最終使用者使用。 

6. 維運與優化 (Maintenance)
軟體上線後的長期階段。團隊會根據使用者回饋進行錯誤修復、效能優化，並隨著環境變化進行系統更新，以確保軟體的長期價值。


### Waterfall

階段    Waterfall 實踐方式
1. 規劃 [LLM]
2. 設計 [LLM]
3. 開發 [LLM]
4. 測試 [LLM]
5. 部署 [LLM]
6. 維運 [LLM]

### Agile

階段	Agile 實踐方式
1. 規劃	Sprint Planning：每兩週決定一次要做的功能，而非一次規劃整年的需求。
2. 設計	持續設計：只針對當前要做的功能進行足夠的設計（Just-Enough Design）。
3. 開發	每日站會 (Daily Stand-up)：每天同步進度，確保開發方向正確。
4. 測試	自動化測試 & CI/CD：程式碼一寫完就自動跑測試，確保隨時可交付。
5. 部署	持續交付：每個 Sprint 結束後，都有一個「可運作的軟體增量」可以展示或上線。
6. 維運	回顧會議 (Retrospective)：每個循環結束後檢討流程並即時優化。

### 螺旋模型 (Spiral Model)

階段    [TITLE] 實踐方式
1. 規劃 [LLM]
2. 設計 [LLM]
3. 開發 [LLM]
4. 測試 [LLM]
5. 部署 [LLM]
6. 維運 [LLM]


### V 模型 (V-Model)

階段    V-Model 實踐方式
1. 規劃 [LLM]
2. 設計 [LLM]
3. 開發 [LLM]
4. 測試 [LLM]
5. 部署 [LLM]
6. 維運 [LLM]

### 增量模型 (Incremental Model)

階段    Incremental Model 實踐方式
1. 規劃 [LLM]
2. 設計 [LLM]
3. 開發 [LLM]
4. 測試 [LLM]
5. 部署 [LLM]
6. 維運 [LLM]

---

1. 時間軸與里程碑總覽表格
展示四個階段的完整資訊：

PHASE 1 (Foundation): 4 個里程碑（M1.1-M1.4）
PHASE 2 (Multi-Agent): 3 個里程碑（M2.1-M2.3）
PHASE 3 (Memory Systems): 3 個里程碑（M3.1-M3.3）
PHASE 4 (Framework Release): 2 個里程碑（M4.1-M4.2）
2. 累積測試標準
每個 PHASE 的測試標準都採用累積制：

P1: 基礎測試（90%+ 覆蓋率、mypy --strict、單代理循環）
P2: 繼承 P1 + 多代理協作測試
P3: 繼承 P1+P2 + 記憶系統測試
P4: 繼承 P1+P2+P3 + 打包與文件測試
3. 各階段詳細測試標準
使用 YAML 格式清楚說明：

繼承的測試項目（inherited_from_*）
新增的測試需求（additional_requirements）
退出標準（exit_criteria）
這樣的結構確保： ✅ 每個階段都有明確的里程碑 ✅ 測試標準越來越嚴格（累積制） ✅ 最後階段必須通過前三個階段的所有測試


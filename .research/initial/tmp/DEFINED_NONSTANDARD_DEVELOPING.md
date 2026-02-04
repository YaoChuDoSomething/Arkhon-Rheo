# DEFINED NONSTANDARD FLOW

是的，你的直覺**完全正確**：

> **任務切得越細，本質越單一，狀態機就越容易理解與驗證。**

而你問的這一題，其實是在問 **Arkhon-Rheo 是否只支援「一種」開發敘事**。
答案是：**不只，而且必須明確定義「非標準流程」**，否則才是真正的風險來源。

下面我會用**狀態機語言**來回答，不回到 Agent，不談實作細節。

---

## 一、先給總論（重要）

> **標準流程 ≠ 唯一合法流程**
> **標準流程 = 頻率最高、風險最低的「主幹路徑」**

**非標準流程不是例外處理，而是「受憲法約束的替代敘事」**。

---

## 二、為什麼一定要設計「非標準流程」

如果你不設計，系統還是會「發生」：

* 緊急修補（Hotfix）
* 試驗性探索（Spike）
* 純重構（Refactor）
* 失敗回收（Rollback）
* 架構遷移（Migration）

> 差別只在於：
> **你是讓它們「非法發生」，還是「被命名、被約束地發生」**

---

## 三、Arkhon-Rheo 中的「非標準流程」分類（狀態機觀點）

我會把它們分成 **4 種合法偏移路徑**。

---

## 1️⃣ 快速修補流程（Hotfix Loop）

### 使用時機

* 生產問題
* 明確 bug
* 已知修法、低設計不確定性

### 狀態特徵

* 跳過大部分設計推導
* **但不能跳過驗證**

```text
IntentDefined
→ AcceptanceSpecified
→ ImplementationProposed
→ EvidenceCollected
→ StateValidated
→ Integrated
```

### 憲法限制

* 必須標記 `mode: hotfix`
* 回到主幹後強制補齊設計文件

---

## 2️⃣ 探索性實驗流程（Spike / Research）

### 使用時機

* 技術可行性不明
* API 行為不確定
* 模型或演算法試驗

### 狀態特徵

* **允許無法完成**
* 結果是「知識」，不是功能

```text
IntentDefined
→ ExperimentExecuted
→ FindingsRecorded
→ Archived
```

### 關鍵規則

* 絕不進入 `Integrated`
* 不污染主狀態機

---

## 3️⃣ 純重構流程（Refactor-only）

### 使用時機

* 技術債處理
* 結構調整
* 不變更外部行為

### 狀態特徵

* Acceptance 固定
* Evidence 重心在 regression

```text
DesignBounded
→ ImplementationProposed
→ EvidenceCollected
→ StateValidated
→ Integrated
```

### 憲法硬約束

* 行為測試不得減少
* Coverage 不得下降

---

## 4️⃣ 回退與修復流程（Recovery / Rollback）

### 使用時機

* 驗證失敗
* State 污染
* 不可預期副作用

### 狀態特徵

* 不產生新功能
* 修復狀態一致性

```text
StateValidated (fail)
→ RecoveryProposed
→ EvidenceCollected
→ StateValidated
→ Integrated
```

---

## 四、關鍵設計原則（這裡是精髓）

### ❗ 非標準流程 ≠ 少流程

而是：

> **「改變的是『哪些狀態存在』，不是『規則是否存在』」**

三條鐵律：

1. **永遠有 Acceptance 或其等價物**
2. **永遠有 Evidence**
3. **永遠由 StateValidated 裁決**

---

## 五、在憲法中的正確寫法（示意）

```yaml
allowed_workflows:
  standard:
    states: [IntentDefined, DesignBounded, AcceptanceSpecified, ImplementationProposed, EvidenceCollected, StateValidated, Integrated]

  hotfix:
    states: [IntentDefined, AcceptanceSpecified, ImplementationProposed, EvidenceCollected, StateValidated, Integrated]
    constraints:
      require_tag: hotfix

  spike:
    states: [IntentDefined, ExperimentExecuted, FindingsRecorded, Archived]
    constraints:
      forbid_integration: true
```

---

## 六、一句話總結（請記住這句）

> **標準流程是為了效率設計的，
> 非標準流程是為了「不讓例外毀掉系統」而設計的。**

你現在的 Arkhon-Rheo 架構，**已經足以承載多敘事狀態機**，只差你要不要把它們正式寫進憲法。

如果你下一步想繼續，我建議的順序是：

1. 把「非標準流程」**列為一級憲法條款**
2. 明確哪些 state **在某些模式下不存在**
3. 為每種流程定義 **最小證據集合**

這一步做完，你的系統就不是「嚴格」，而是**成熟**了。


# TESTS_PLANNING

你現在問到的這一層，其實已經從「寫測試技巧」正式升級到：

👉 **測試系統工程化（Test System Engineering）**

先直接回答你：

✅ 是的，需要表格
✅ 而且不是一張，而是一組彼此銜接的表
✅ 但「不是 QA 規格書格式」，而是 **設計推導工具**

下面我給你一套 **可落地、可重複、可教給團隊的流程**。

---

## 🧭 整體流程鳥瞰

```text
需求
  ↓
使用情境 (Use Case)
  ↓
失敗模式 (Failure Modes)
  ↓
行為規格 (Behavior Spec)
  ↓
測試矩陣 (Test Matrix)
  ↓
測試類型映射
  ↓
Pipeline Gate 設計
```

你要的「步驟化流程」其實長這樣：

---

## 🧩 Step 1 — 需求 → 使用情境表

先不要想測試。

先想：

👉 這個系統「被怎麼用」。

### Use Case Table

| UC-ID | Actor  | Action               | Input    | Expected Outcome |
| ----- | ------ | -------------------- | -------- | ---------------- |
| UC-01 | User   | Create Order         | sku, qty | order created    |
| UC-02 | User   | Pay Order            | order_id | status=PAID      |
| UC-03 | System | Cancel Timeout Order | order_id | status=CANCEL    |

這張表的目的：

👉 切掉抽象需求文字
👉 轉成可操作行為

---

## 🧩 Step 2 — 使用情境 → Failure Mode 表

對每個 Use Case 問：

> 這個動作「會怎麼失敗」？

### Failure Mode Table

| UC-ID | FM-ID | Failure Description     |
| ----- | ----- | ----------------------- |
| UC-01 | FM-01 | SKU not found           |
| UC-01 | FM-02 | Qty <= 0                |
| UC-01 | FM-03 | DB write fail           |
| UC-02 | FM-04 | Order not exist         |
| UC-02 | FM-05 | Already paid            |
| UC-02 | FM-06 | Payment gateway timeout |

這一層是整個體系的核心。

👉 未來所有測試都能追溯到這張表

---

## 🧩 Step 3 — Failure Mode → 行為規格表（你提到的關鍵）

這裡正式回答你：

👉 是的，**要同時定義通過、失敗、非定義行為**

### Behavior Spec Table

| FM-ID | Input Condition | Expected Result (PASS) | Rejected Result (FAIL) | Undefined / Out-of-Scope |
| ----- | --------------- | ---------------------- | ---------------------- | ------------------------ |
| FM-02 | qty = -1        | HTTP 400 + msg         | order created          | qty=0?                   |
| FM-04 | order_id=999    | HTTP 404               | status=PAID            |                          |

意義：

* PASS → 自動測試斷言
* FAIL → 反向測試斷言
* Undefined → 設計缺口清單

Undefined 欄非常重要：

👉 逼設計者補規格

---

## 🧩 Step 4 — 行為規格 → 測試矩陣

開始進入測試工程。

### Test Matrix

| FM-ID | Test Type        | Level       | Tool           | Automated | Priority |
| ----- | ---------------- | ----------- | -------------- | --------- | -------- |
| FM-02 | Input validation | Unit        | pytest         | Yes       | High     |
| FM-03 | DB failure       | Integration | pytest+db      | Yes       | High     |
| FM-06 | Timeout          | Integration | docker-compose | Yes       | High     |
| FM-05 | Business rule    | Unit        | pytest         | Yes       | Medium   |

你會得到：

👉 一份「為什麼要有這個測試」的清單

不是憑感覺寫。

---

## 🧩 Step 5 — 測試類型映射規則

建立團隊準則：

```text
Pure logic → Unit
跨模組 → Integration
跨服務 → Contract
使用者流程 → E2E
```

可整理成：

| Condition    | Test Level  |
| ------------ | ----------- |
| No I/O       | Unit        |
| DB or FS     | Integration |
| External API | Contract    |
| Full path    | E2E         |

---

## 🧩 Step 6 — Pipeline Gate 設計

將測試矩陣轉成門禁。

### Pipeline

```text
PR Stage:
  Unit + Integration(High)

Main Stage:
  All Unit
  All Integration
  Contract

Release Stage:
  Smoke E2E
```

而且：

👉 每個 Gate 可追溯 FM-ID

---

## 🧩 Step 7 — Traceability（關聯性）

理想結構：

```text
Test Case
  → FM-ID
      → UC-ID
          → Requirement
```

這代表：

刪一個測試時，你知道風險。

---

## 🧠 關於你提到的三分類

你說：

> 定義通過的答案，也要定義出不通過的答案，還有不在這兩者範圍內的解

工程化對應是：

| 類型 | 意義 |
| --- | --- |
| PASS | Spec 定義 |
| FAIL | 明確拒絕 |
| Undefined | 需要產品/架構決策 |

Undefined 是高價值輸出，不是垃圾桶。

---

## 🔁 進階：事件驅動補洞

每次 Production Incident：

```text
Incident
  → 新 FM
     → 新 Behavior Spec
         → 新 Test
```

測試庫會隨時間「貼近真實風險」。

---

## ✅ 你真正需要的不是

「寫很多測試技巧」

而是：

👉 一條 **從需求可推導到測試的工業化流水線**

---

## 🧩 一句話總結流程

```text
先列行為
再列失敗
再定規格
最後才寫測試
```

---

如果你願意，我可以下一步帶你走一次完整範例：

👉 以「訂單服務」或你自己的系統
👉 直接一起填完整 7 張表

你只要告訴我：
你比較想用「什麼類型的系統」當示範？（API 服務 / 資料處理 pipeline / ML 推論服務 / 其他）

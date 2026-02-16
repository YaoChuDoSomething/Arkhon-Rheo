# Review Task: Phase 3 Memory & Storage Integrity Audit

## Checklist

- [ ] **[Security]** `CheckpointManager` 內使用了 `pickle.dumps/loads`。針對不信任資料的反序列化風險，應評估是否需增加 HMAC 簽章或改用較安全的序列化格式（如 `json` + `msgpack`）。
- [ ] **[Concurrency]** `sqlite3` 的 `connect` 在非同步環境下使用。需確認是否需設置 `check_same_thread=False` 或使用 `aiosqlite` 以避免阻塞 Event Loop。
- [ ] **[Performance]** `Summarizer` 在建立提示詞時使用簡單的字串拼接。應檢查大批次對話時的記憶體分配效率。
- [ ] **[Architecture]** `VectorStore` 的 `query` 目前為同步方法。考量未來整合向量資料庫（如 Milvus, Qdrant），建請評估改為 `async` 介面。
- [ ] **[Consistency]** `CheckpointManager.rollback` 會刪除後的資料。需確認在分散式或多代理環境下，是否有防範誤刪的機制。

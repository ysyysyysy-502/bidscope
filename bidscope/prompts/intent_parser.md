# Intent AI Prompt 设计草案

MVP 当前使用规则解析，后续可接入 LLM，但必须输出以下 JSON Schema：

```json
{
  "topic": "服务器与算力",
  "synonyms": ["AI服务器", "GPU服务器", "算力集群"],
  "regions": ["上海"],
  "start_at": "2026-04-18T00:00:00+08:00",
  "end_at": "2026-07-18T23:59:59+08:00",
  "stages": ["PROCUREMENT", "CHANGE", "AWARD"],
  "schedule_cron": "0 9 * * *",
  "timezone": "Asia/Shanghai",
  "confidence": 0.96,
  "clarification_questions": []
}
```

约束：

- 模型不能调用任意 URL；
- 相对日期由程序计算，不由模型自由猜测；
- 事实字段不得由模型补空；
- 低置信度必须追问或进入人工复核。

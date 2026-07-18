# API 接口说明

## GET /api/v1/health

健康检查。

## GET /api/v1/sources

返回三类数据源健康状态：政府公开源、API 源、商业聚合源。

## POST /api/v1/intents/parse

请求：

```json
{"query":"最近3个月上海服务器与算力招标，请每天9:00汇总发送给我"}
```

返回结构化意图：主题、同义词、地区、时间范围、频率、公告阶段、置信度。

## POST /api/v1/runs

创建一次检索任务。Demo 版本同步返回结果；生产版应返回 202 + run_id，然后通过轮询或 SSE 查看进度。

## GET /api/v1/runs/{run_id}

读取任务结果。

## GET /api/v1/reports/{run_id}/download

下载 Word 报告。

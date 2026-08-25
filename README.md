# BidScope / 标讯罗盘

> 将多源招投标信息整理为可追溯、可去重、可订阅并可导出 Word 的销售线索。

## 项目简介

BidScope 是 2026 AI 先锋未来人才大赛超聚变企业命题的工程 Demo。用户输入一句自然语言需求，系统解析主题、地区、时间与频率，规划数据源，完成标准化、证据分层、相关性判断、去重和增量记录，最后返回结构化结果与 Word 报告。

> 当前仓库使用脱敏样例数据和模拟连接器，用于验证端到端流程；不代表已经接入所有真实外部平台。

## 核心能力

- Vue 3 单页检索工作台与 FastAPI API
- 政府公开源、API 型数据源、商业聚合源三类连接器骨架
- 自然语言意图解析与来源规划
- T0/T1/T2/T3 证据分层和带证据的相关性理由
- URL、正文哈希、项目编号/组合字段三级确定性去重
- 查询级增量推送账本，避免重复交付
- 正式公告与待核验线索分区的 Word 报告
- 对验证码、付费墙和受限字段的明确合规边界

## 技术栈

- 后端：Python、FastAPI、Pydantic、HTTPX、python-docx
- 前端：Vue 3、TypeScript、Vite、Axios
- 测试：pytest
- 可选基础设施：Docker Compose、PostgreSQL 16、Redis 7

## 项目结构

```text
bidscope/
├── backend/       FastAPI、领域模型、连接器与服务
├── frontend/      Vue 3 工作台
├── docs/          API、演示和接入说明
├── prompts/       意图解析约束
├── templates/     报告与卡片模板说明
├── scripts/       冒烟测试
└── tests/fixtures 脱敏测试数据
```

## 快速开始

### 后端

```bash
cd bidscope/backend
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API 文档：`http://127.0.0.1:8000/docs`

### 前端

另开终端：

```bash
cd bidscope/frontend
npm install
npm run dev
```

访问 `http://127.0.0.1:5173`。前端如需自定义后端地址，请设置 `VITE_API_BASE`。

### Docker Compose

```bash
cd bidscope
docker compose up --build
```

该方式会同时启动前端、API、PostgreSQL 和 Redis。当前 Demo 的核心流程仍以本地状态和样例数据为主。

## 使用示例

```bash
curl -X POST http://127.0.0.1:8000/api/v1/runs \
  -H 'Content-Type: application/json' \
  -d '{"query":"最近3个月上海服务器与算力招标，请每天9:00汇总发送给我"}'
```

使用响应中的 `run_id` 下载报告：

```bash
curl -OJ http://127.0.0.1:8000/api/v1/reports/<run_id>/download
```

## 测试与构建

```bash
cd bidscope/backend
pytest -q
cd ../frontend
npm run build
```

可按需运行 `python bidscope/scripts/smoke_test.py`；运行前请先启动后端。

## 合规边界

真实接入外部网站前，必须逐源确认服务条款、robots、API 协议、账号授权、限速和导出限制。遇到验证码、付费墙、权限不足或禁止自动化时，系统应停止并标记限制原因，不得绕过访问控制。

## 常见问题

### 返回的结果是否为真实线上数据？

默认不是。仓库中的连接器和 JSON 数据用于演示流程，真实数据源需要在合规评估和授权后接入。

### Word 报告在哪里？

运行查询后通过报告下载 API 获取；具体接口见 `bidscope/docs/API接口说明.md`。

## 贡献

请从独立分支提交 Pull Request，并为后端逻辑补充 pytest。新增连接器必须说明授权方式、访问限制、退避策略及脱敏方案。

## 许可证

仓库当前未提供独立开源许可证文件。在许可证明确前，默认保留全部权利。

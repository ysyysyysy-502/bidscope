# BidScope / 标讯罗盘

> 2026 AI 先锋未来人才大赛 · 超聚变企业命题最小工程雏形。  
> 一句话完成多源标讯的检索、订阅、审计与 Word 交付。

## 项目定位

标讯罗盘不是“再做一个爬虫”，而是把分散、不稳定、权限边界复杂的招投标网页，整理成可追溯、可去重、可订阅、可交付的信息产品。

本仓库提供一个可运行 Demo：

- Vue 3 单页问答工作台；
- FastAPI 后端；
- 三类样例数据源连接器：政府公开源、API 型数据源、商业聚合源；
- 自然语言意图解析：主题、地区、时间范围、频率；
- 标讯标准化字段：标题、发布时间、来源链接、核心内容、附件链接；
- T0/T1/T2/T3 证据分层；
- 相关性评分与证据片段；
- 三级确定性去重；
- 增量推送账本；
- Word 报告生成，文件名遵循 `{用户的问题}_{yyyyMMddHHmm}.docx`；
- 合规边界：不绕验证码、不绕付费墙、不硬编码真实结果。

## 当前 Demo 做到什么程度

本版本是“可提交 GitHub 的工程雏形”，重点证明整体链路和工程结构，不声称已真实接入所有外部平台。

已完成：

1. **前后端可运行**：前端输入一句自然语言，后端返回结构化意图、来源计划、标讯结果与 Word 下载地址。
2. **三类数据源骨架**：
   - `government_mock`：代表中国政府采购网 / 全国公共资源交易平台等 T0 官方源；
   - `api_bid_mock`：代表招投标 API 数据服务；
   - `commercial_mock`：代表剑鱼、千里马、采招网等商业聚合站合法可见字段。
3. **合规模拟**：商业源中对联系人、深度画像等字段标记 `access_restricted`，不恢复遮罩字段。
4. **确定性去重**：URL、正文哈希、项目编号 / 标题 + 采购人 + 地区 + 时间窗三级去重。
5. **增量账本**：同一个 query 再次运行不会重复推送相同 notice。
6. **Word 输出**：报告分为“正式公告”和“待核验线索”，列出证据等级、命中理由、附件、受限字段和去重统计。

未完成但已预留接口：

- 真实中国政府采购网 / 全国公共资源交易平台连接器；
- 真实 API Key 接入；
- 真实剑鱼 / 标标达登录会话；
- 飞书机器人、多维表格 AI 字段与自动化路由；
- Celery/Redis/PostgreSQL 生产化异步任务，本地 Demo 默认使用内存状态和本地文件，便于一键运行。

## 快速启动

### 1. 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

访问：<http://127.0.0.1:8000/docs>

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问：<http://127.0.0.1:5173>

### 3. 推荐演示输入

```text
最近3个月上海服务器与算力招标，请每天9:00汇总发送给我
```

或：

```text
最近一个月安徽充电站和AI基础设施招标
```

## API 示例

```bash
curl -X POST http://127.0.0.1:8000/api/v1/runs \
  -H 'Content-Type: application/json' \
  -d '{"query":"最近3个月上海服务器与算力招标，请每天9:00汇总发送给我"}'
```

下载 Word：

```bash
curl -OJ http://127.0.0.1:8000/api/v1/reports/<run_id>/download
```

## 目录结构

```text
bidscope/
  backend/                # FastAPI 后端
  frontend/               # Vue 3 前端
  connectors/             # 预留给独立连接器包，本 Demo 连接器在 backend/app/connectors
  prompts/                # 提示词和 Schema 约束说明
  templates/              # Word / 飞书卡片模板说明
  docs/                   # 操作文档、演示脚本、人工事项清单
  tests/fixtures/         # 脱敏样例数据
  output/sample_outputs/  # 示例输出
```

## 合规声明

本 Demo 默认使用脱敏样例数据和模拟连接器。真实接入外部网站前，需要逐源确认：

- robots / 服务条款 / API 使用协议；
- 是否允许自动化访问；
- 是否需要用户授权登录；
- 是否存在验证码、付费墙、CA、供应商资格或导出限制；
- 账号可见字段与会话有效期；
- 限速、缓存、退避和人工续登流程。

系统遇到验证码、付费墙、权限不足或明确禁止自动化时，应停止采集并标记 `access_restricted` 或 `automation_prohibited`，不得尝试绕过。

## 适合向组长汇报的话

我已经先做了一个工程雏形，不直接承诺真实跑通所有外部站点，而是把政府源、API 源、商业源三类连接器、统一 Notice 结构、证据分层、去重、增量账本和 Word 交付都打通了。下一步只需要人工注册 API、确认政府源页面规则、准备商业站授权账号和飞书权限，就能把 mock 连接器逐步替换为真实连接器。

---
name: Apify Automation
description: "使用 Apify 自动化网页抓取和数据提取 -- 运行 Actor、管理数据集、创建可重用任务，并通过 Composio Apify 集成检索抓取结果。"
requires:
  mcp:
    - rube
---

# Apify 自动化

直接从 Claude Code 运行 **Apify** 网页抓取 Actor 并管理数据集。同步或异步执行爬虫，检索结构化数据，创建可重用任务，并检查运行日志，无需离开终端。

**工具包文档:** [composio.dev/toolkits/apify](https://composio.dev/toolkits/apify)

---

## 设置

1. 将 Composio MCP 服务器添加到您的配置：
   ```
   https://rube.app/mcp
   ```
2. 在提示时连接您的 Apify 账户。代理将提供身份验证链接。
3. 在 [apify.com/store](https://apify.com/store) 浏览可用的 Actor。每个 Actor 都有自己独特的输入架构 — 在运行之前始终检查 Actor 的文档。

---

## 核心工作流

### 1. 同步运行 Actor 并获取结果

执行 Actor 并在单个调用中立即检索其数据集项。最适合快速抓取任务。

**工具：** `APIFY_RUN_ACTOR_SYNC_GET_DATASET_ITEMS`

**关键参数：**
- `actorId`（必需）-- `username/actor-name` 格式的 Actor ID（例如 `compass/crawler-google-places`）
- `input` -- 与 Actor 架构匹配的 JSON 输入对象。每个 Actor 都有唯一的字段名称 — 请在 [apify.com/store](https://apify.com/store) 检查确切架构。
- `limit` -- 要返回的最大项数
- `offset` -- 跳过项目以进行分页
- `format` -- `json`（默认）、`csv`、`jsonl`、`html`、`xlsx`、`xml`
- `timeout` -- 运行超时（秒）
- `waitForFinish` -- 最大等待时间（0-300 秒）
- `fields` -- 要包含的字段的逗号分隔列表
- `omit` -- 要排除的字段的逗号分隔列表

**示例提示：** *"运行 Google Places 抓取器，搜索'纽约的餐厅'并返回前 50 个结果"*

---

### 2. 异步运行 Actor

触发 Actor 运行而无需等待完成。用于长时间运行的抓取任务。

**工具：** `APIFY_RUN_ACTOR`

**关键参数：**
- `actorId`（必需）-- Actor 标识符或 ID
- `body` -- Actor 的 JSON 输入对象
- `memory` -- 内存限制（MB，必须是 2 的幂，最小 128）
- `timeout` -- 运行超时（秒）
- `maxItems` -- 返回项的上限
- `build` -- 特定构建标签（例如 `latest`、`beta`）

使用运行的 `datasetId` 跟进 `APIFY_GET_DATASET_ITEMS` 以检索结果。

**示例提示：** *"异步启动 example.com 的网页抓取器 Actor，使用 1024MB 内存"*

---

### 3. 检索数据集项

从特定数据集获取数据，支持分页、字段选择和过滤。

**工具：** `APIFY_GET_DATASET_ITEMS`

**关键参数：**
- `datasetId`（必需）-- 数据集标识符
- `limit`（默认/最大 1000）-- 每页项数
- `offset`（默认 0）-- 分页偏移
- `format` -- `json`（推荐）、`csv`、`xlsx`
- `fields` -- 仅包含特定字段
- `omit` -- 排除特定字段
- `clean` -- 移除 Apify 特定的元数据
- `desc` -- 反向顺序（最新的在前）

**示例提示：** *"以 JSON 格式从数据集 myDatasetId 获取前 500 项"*

---

### 4. 检查 Actor 详情

在运行之前查看 Actor 元数据、输入架构和配置。

**工具：** `APIFY_GET_ACTOR`

**关键参数：**
- `actorId`（必需）-- `username/actor-name` 格式或十六进制 ID 的 Actor ID

**示例提示：** *"显示 apify/web-scraper Actor 的详细信息和输入架构"*

---

### 5. 创建可重用任务

为重复的抓取任务配置可重用的 Actor 任务，使用预设输入。

**工具：** `APIFY_CREATE_TASK`

配置一次任务，然后使用一致的输入参数重复触发它。适用于计划或重复的数据收集工作流。

**示例提示：** *"为 Google Search 抓取器创建 Apify 任务，使用默认查询'AI 初创公司'和美国位置"*

---

### 6. 管理运行和数据集

列出 Actor 运行、浏览数据集，并检查运行详情以进行监控和调试。

**工具：** `APIFY_GET_LIST_OF_RUNS`、`APIFY_DATASETS_GET`、`APIFY_DATASET_GET`、`APIFY_GET_LOG`

**列出运行：**
- 按 Actor 过滤，可选按状态
- 从运行详情获取 `datasetId` 以进行数据检索

**数据集管理：**
- `APIFY_DATASETS_GET` -- 列出所有数据集，支持分页
- `APIFY_DATASET_GET` -- 获取特定数据集的元数据

**调试：**
- `APIFY_GET_LOG` -- 检索运行或构建的执行日志

**示例提示：** *"列出网页抓取器 Actor 的最后 10 次运行，并显示最近一次的日志"*

---

## 已知陷阱

- **Actor 输入架构差异很大：** 每个 Actor 都有自己独特的输入字段。像 `queries` 或 `search_terms` 这样的通用字段名称将被拒绝。始终在 [apify.com/store](https://apify.com/store) 上检查 Actor 的页面以获取确切的字段名称（例如，Google Maps 使用 `searchStringsArray`，网页抓取器使用 `startUrls`）。
- **URL 格式要求：** 始终在 URL 中包含完整的协议（`https://` 或 `http://`）。许多 Actor 要求 URL 作为带有 `url` 属性的对象：`{"startUrls": [{"url": "https://example.com"}]}`。
- **数据集分页上限：** `APIFY_GET_DATASET_ITEMS` 每次调用的最大 `limit` 为 1000。对于大型数据集，使用 `offset` 循环以收集所有项。
- **枚举值为小写：** 大多数 Actor 期望小写枚举值（例如，`relevance` 而不是 `RELEVANCE`，`all` 而不是 `ALL`）。
- **同步超时为 5 分钟：** `APIFY_RUN_ACTOR_SYNC_GET_DATASET_ITEMS` 的最大 `waitForFinish` 为 300 秒。对于更长的运行，请使用 `APIFY_RUN_ACTOR`（异步）并使用 `APIFY_GET_DATASET_ITEMS` 轮询。
- **数据量成本：** 大型数据集的获取可能很昂贵。请首选适度的限制和增量处理，以避免超时或内存压力。
- **推荐 JSON 格式：** 虽然 CSV/XLSX 格式可用，但 JSON 对于自动化处理最可靠。避免在下游自动化中使用 CSV/XLSX。

---

## 快速参考

| 工具标识符 | 描述 |
|---|---|
| `APIFY_RUN_ACTOR_SYNC_GET_DATASET_ITEMS` | 同步运行 Actor 并立即获取结果 |
| `APIFY_RUN_ACTOR` | 异步运行 Actor（触发并返回） |
| `APIFY_RUN_ACTOR_SYNC` | 同步运行 Actor，返回输出记录 |
| `APIFY_GET_ACTOR` | 获取 Actor 元数据和输入架构 |
| `APIFY_GET_DATASET_ITEMS` | 从数据集检索项（分页） |
| `APIFY_DATASET_GET` | 获取数据集元数据（项数等） |
| `APIFY_DATASETS_GET` | 列出所有用户数据集 |
| `APIFY_CREATE_TASK` | 创建可重用的 Actor 任务 |
| `APIFY_GET_TASK_INPUT` | 检查任务的存储输入 |
| `APIFY_GET_LIST_OF_RUNS` | 列出 Actor 的运行 |
| `APIFY_GET_LOG` | 获取运行的执行日志 |

---

*由 [Composio](https://composio.dev) 提供支持*

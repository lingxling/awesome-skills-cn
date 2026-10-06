---
name: SurveyMonkey Automation
description: "通过自然语言命令自动化 SurveyMonkey 问卷创建、回复收集、收集器管理和问卷发现"
requires:
  mcp:
    - rube
---

# SurveyMonkey Automation

自动化 SurveyMonkey 问卷工作流 -- 创建问卷、列出和搜索现有问卷、管理收集器和分发链接、获取回复、查看问卷详情 -- 全部通过自然语言完成。

**工具包文档：** [composio.dev/toolkits/survey_monkey](https://composio.dev/toolkits/survey_monkey)

---

## 设置

1. 将 Rube MCP 服务器添加到你的环境中：`https://rube.app/mcp`
2. 按提示连接你的 SurveyMonkey 账户（通过 Composio 的 OAuth 流程）
3. 开始使用自然语言命令进行 SurveyMonkey 自动化操作

---

## 核心工作流

### 1. 创建新问卷

创建一个空的新问卷，之后可以进一步配置问题和页面。

**工具：** `SURVEY_MONKEY_CREATE_SURVEY`

关键参数：
- `title` -- 显示给受访者的问卷标题（必填）
- `nickname` -- 用于组织问卷的内部名称（可选，不会展示给受访者）
- `language` -- ISO 639-1 语言代码（默认 `en`）；示例：`es`、`fr`、`de`
- `footer` -- 是否显示 SurveyMonkey 品牌页脚（默认 `true`）

> 新创建的问卷以一个空页面开始，不含任何问题。请使用返回的 `survey_id` 配合其他操作添加内容并配置收集器。

示例提示词：
> "创建一个标题为 'Customer Satisfaction Q1 2026' 的新问卷"

---

### 2. 列出和搜索问卷

枚举账户中的所有问卷，支持筛选、排序和分页。

**工具：** `SURVEY_MONKEY_GET_SURVEYS`

关键参数：
- `title` -- 按问卷标题搜索（支持部分匹配）
- `sort_by` -- 按 `title`、`date_modified` 或 `num_responses` 排序
- `sort_order` -- `ASC` 或 `DESC`
- `page` / `per_page` -- 分页控制（默认每页 50 条，最大 100）
- `include` -- 附加字段：`response_count`、`date_modified`、`date_created`、`question_count`、`page_count`、`category`、`language`、`folder_id`
- `folder_id` -- 筛选指定文件夹中的问卷
- `start_modified_at` / `end_modified_at` -- 日期范围筛选（格式：`YYYY-MM-DDTHH:MM:SS`）

示例提示词：
> "列出我所有的问卷，按最近修改时间排序，并包含回复数"

---

### 3. 获取问卷详情

获取特定问卷的完整元数据，包括配置、问题/页面数量、回复数以及所有相关网址。

**工具：** `SURVEY_MONKEY_GET_SURVEY_DETAILS`

关键参数：
- `survey_id` -- 唯一问卷标识符（必填）

返回内容：标题、语言、问题数量、页面数量、回复数量、预览/编辑/分析/收集的网址、按钮文本和时间戳。

示例提示词：
> "给我看问卷 123456789 的完整详情和回复数"

---

### 4. 管理收集器和分发链接

获取问卷的收集器（分发渠道）以获取可分享链接并监控回复进度。

**工具：** `SURVEY_MONKEY_GET_COLLECTORS`

关键参数：
- `survey_id` -- 要获取收集器的问卷（必填）
- `include` -- 附加字段：`type`、`status`、`response_count`、`date_created`、`date_modified`、`url`
- `name` -- 按收集器名称部分匹配筛选
- `sort_by` -- 按 `id`、`date_modified`、`type`、`status` 或 `name` 排序
- `sort_order` -- `ASC` 或 `DESC`
- `page` / `per_page` -- 分页（默认 50，最大 1000）
- `start_date` / `end_date` -- 按创建日期筛选（格式：`YYYY-MM-DDTHH:MM:SS`）

示例提示词：
> "获取问卷 123456789 的所有收集器，包含网址和回复数"

---

### 5. 获取问卷回复

获取特定问卷的回复数据，并提供全面的筛选选项。

**工具：** `SURVEY_MONKEY_GET_RESPONSES`

关键参数：
- `survey_id` -- 要获取回复的问卷（必填）
- `status` -- 按状态筛选：`completed`、`partial`、`overquota` 或 `disqualified`
- `page` / `per_page` -- 分页（默认 50，最大 1000）
- `sort_order` -- `ASC` 或 `DESC`（按 `date_modified` 排序）
- `start_created_at` / `end_created_at` -- 按创建日期范围筛选（ISO 8601）
- `start_modified_at` / `end_modified_at` -- 按修改日期范围筛选
- `email` -- 按受访者邮箱筛选
- `first_name` / `last_name` -- 按受访者姓名筛选
- `ip` -- 按 IP 地址筛选
- `total_time_min` / `total_time_max` / `total_time_units` -- 按完成时间筛选

示例提示词：
> "获取问卷 123456789 过去 30 天内所有已完成的回复"

---

### 6. 完整问卷生命周期工作流

组合多个工具实现端到端的问卷管理：

1. **创建**：`SURVEY_MONKEY_CREATE_SURVEY` -- 创建问卷，保存 `survey_id`
2. **分发**：`SURVEY_MONKEY_GET_COLLECTORS` -- 获取可分享给受访者的收集器链接
3. **监控**：`SURVEY_MONKEY_GET_SURVEY_DETAILS` -- 检查回复数和问卷状态
4. **收集**：`SURVEY_MONKEY_GET_RESPONSES` -- 获取已完成的回复，按 `status=completed` 筛选
5. **查找**：`SURVEY_MONKEY_GET_SURVEYS` -- 如果 `survey_id` 丢失，浏览并查找问卷

示例提示词：
> "创建一个名为 'Event Feedback' 的问卷，然后告诉我如何分发它"

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|---------|
| 需要分页 | `SURVEY_MONKEY_GET_COLLECTORS` 和 `SURVEY_MONKEY_GET_RESPONSES` 在处理大型问卷时需要管理 `page`/`per_page`，以免遗漏数据 |
| 状态筛选至关重要 | `SURVEY_MONKEY_GET_RESPONSES` 如果不筛选会返回部分、超配额和不合格的条目 -- 使用 `status=completed` 获取可靠数据 |
| 创建时不生成可分享链接 | `SURVEY_MONKEY_CREATE_SURVEY` 不会创建分发链接 -- 使用 `SURVEY_MONKEY_GET_COLLECTORS` 获取可分享网址 |
| survey_id 的保存 | 丢失 `survey_id` 会被迫依赖较慢的 `SURVEY_MONKEY_GET_SURVEYS` -- 创建后应立即保存 ID |
| 问题 ID 映射 | 回复中的问题 ID 和答案格式需要仔细映射；使用 `SURVEY_MONKEY_GET_SURVEY_DETAILS` 了解结构 |
| 日期格式 | 日期筛选使用 `YYYY-MM-DDTHH:MM:SS` 格式，而不是带时区的 ISO 8601 |
| 创建时为空问卷 | 新问卷以一个空页面开始，不含任何问题 -- 需要进一步配置 |

---

## 快速参考

| 操作 | 工具标识 | 关键参数 |
|--------|-----------|------------|
| 创建问卷 | `SURVEY_MONKEY_CREATE_SURVEY` | `title`、`language`、`nickname` |
| 列出问卷 | `SURVEY_MONKEY_GET_SURVEYS` | `title`、`sort_by`、`include`、`page` |
| 获取问卷详情 | `SURVEY_MONKEY_GET_SURVEY_DETAILS` | `survey_id` |
| 列出收集器 | `SURVEY_MONKEY_GET_COLLECTORS` | `survey_id`、`include`、`sort_by` |
| 获取回复 | `SURVEY_MONKEY_GET_RESPONSES` | `survey_id`、`status`、`start_created_at` |

---

*由 [Composio](https://composio.dev) 提供支持*

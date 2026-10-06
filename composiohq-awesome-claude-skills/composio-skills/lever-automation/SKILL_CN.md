---
name: Lever Automation
description: "自动化 Lever ATS 中的招聘工作流 —— 通过 Composio 的 Lever 集成管理职位机会、职位发布、招聘需求、流程阶段和候选人标签。"
requires:
  mcp:
    - rube
---

# Lever Automation

直接从 Claude Code 自动化你在 **Lever ATS** 中的招聘运营。管理职位发布、跟踪候选人管道、更新招聘需求，以及查询职位机会 —— 全程无需离开终端。

**工具包文档：** [composio.dev/toolkits/lever](https://composio.dev/toolkits/lever)

---

## 设置

1. 将 Composio MCP 服务器添加到你的配置中：
   ```
   https://rube.app/mcp
   ```
2. 运行任意 Lever 命令时，按提示连接你的 Lever 账户。智能体会提供一个 OAuth 链接以完成身份验证。
3. 确保你的 Lever API 密钥具有足够的权限范围（对职位发布、职位机会、招聘需求的读/写访问权限），以执行你所需的操作。

---

## 核心工作流

### 1. 列出并筛选职位发布

检索所有职位发布，可按状态、团队、部门、地点或雇佣类型进行可选筛选。

**工具：** `LEVER_LIST_POSTINGS`

关键参数：
- `state` —— 按 `published`、`internal`、`closed`、`draft`、`pending`、`rejected` 筛选
- `team`、`department`、`location`、`commitment` —— 按组织属性缩小结果范围
- `limit`（1-100）和 `offset` —— 对大量职位发布结果进行分页
- `tag` —— 按职位发布标签筛选

示例提示：*"列出 Lever 中所有已发布的工程类职位"*

---

### 2. 浏览候选人职位机会

列出招聘管道中的所有职位机会，具有丰富的筛选功能，适用于管道分析和候选人跟踪。

**工具：** `LEVER_LIST_OPPORTUNITIES`

关键参数：
- `posting_id`、`stage_id`、`tag` —— 按职位发布、流程阶段或标签筛选
- `email`、`contact_id` —— 查找特定候选人的职位机会
- `archived` —— 按归档状态筛选（`true`/`false`）
- `created_at_start`、`created_at_end` —— 日期范围筛选（ISO 8601）
- `expand` —— 将 `applications`、`contact`、`owner`、`stage`、`stageChanges`、`sources`、`sourcedBy` 展开为完整对象

示例提示：*"显示 Senior Engineer 职位发布的所有活跃职位机会，并展开联系人详情"*

---

### 3. 获取职位机会详情

获取单个候选人职位机会的全面详情，包括联系信息、阶段进展、来源和申请记录。

**工具：** `LEVER_GET_OPPORTUNITY`

关键参数：
- `opportunity`（必需）—— 唯一的职位机会 UID
- `expand` —— 以逗号分隔的要展开字段：`contact`、`stage`、`owner`

示例提示：*"获取职位机会 31c9716c-d4e3-47e8-a6a1-54078a1151d6 的完整详情，并展开 contact 和 stage"*

---

### 4. 管理招聘需求

创建、列出、更新和删除招聘需求，以跟踪编制人数和招聘需求。

**工具：** `LEVER_LIST_REQUISITIONS`、`LEVER_GET_REQUISITION`、`LEVER_UPDATE_REQUISITION`、`LEVER_DELETE_REQUISITION`

更新操作需要以下字段：
- `requisition`（必需）—— 招聘需求的 UUID
- `requisitionCode`（必需）—— 唯一编码，如 `REQ-001`
- `name`（必需）—— 招聘需求标题
- `headcountTotal`（必需）—— 职位数量（最少 1）
- `status` —— `open` 或 `closed`
- 可选项：`hiringManager`、`owner`、`department`、`team`、`location`、`compensationBand`

示例提示：*"将招聘需求 REQ-001 的编制人数增加到 3 并将状态改为 open"*

---

### 5. 查看流程阶段

检索你 Lever 账户中配置的所有招聘管道阶段。

**工具：** `LEVER_LIST_STAGES`

关键参数：
- `limit`（1-100）—— 每页最大条目数
- `offset` —— 上一个响应中的分页令牌

示例提示：*"列出我们 Lever 账户中的所有流程阶段"*

---

### 6. 管理标签

列出用于对候选人、职位机会和职位发布进行分类的所有标签。

**工具：** `LEVER_LIST_TAGS`

关键参数：
- `limit` —— 每页最大条目数
- `offset` —— 分页令牌

示例提示：*"显示 Lever 中的所有候选人标签"*

---

## 已知问题

- **大数据集需要分页：** `LEVER_LIST_OPPORTUNITIES` 和 `LEVER_LIST_POSTINGS` 每页默认最多返回 100 条结果。务必检查响应中是否存在 `offset` 令牌，并进行迭代以获取完整结果。
- **expand 参数格式：** `LEVER_LIST_OPPORTUNITIES` 上的 `expand` 字段接受字符串数组，而 `LEVER_GET_OPPORTUNITY` 和 `LEVER_GET_REQUISITION` 上的该字段接受逗号分隔的字符串。请严格遵循各工具的确切模式。
- **招聘需求更新是全量替换：** `LEVER_UPDATE_REQUISITION` 要求提供所有必填字段（`requisitionCode`、`name`、`headcountTotal`），即使你只想更改其中一个字段。务必先用 `LEVER_GET_REQUISITION` 获取当前的招聘需求。
- **时间戳：** 职位机会的日期筛选使用 ISO 8601 格式，而 `LEVER_LIST_POSTINGS` 的 `updated_at_start` 使用毫秒级 Unix 时间戳。
- **连接权限范围：** 如果你的 API 令牌缺少必要的权限，写操作（更新/删除招聘需求）将会失败，即使读操作能够成功。

---

## 快速参考

| 工具标识 | 描述 |
|---|---|
| `LEVER_LIST_POSTINGS` | 列出所有职位发布，可按状态、团队、部门筛选 |
| `LEVER_LIST_OPPORTUNITIES` | 列出候选人职位机会，支持管道筛选 |
| `LEVER_GET_OPPORTUNITY` | 获取单个职位机会的详细信息 |
| `LEVER_GET_REQUISITION` | 按 ID 检索单个招聘需求 |
| `LEVER_LIST_REQUISITIONS` | 列出所有招聘需求，支持按状态/编码筛选 |
| `LEVER_UPDATE_REQUISITION` | 更新现有招聘需求（全量替换） |
| `LEVER_DELETE_REQUISITION` | 删除/归档招聘需求 |
| `LEVER_LIST_STAGES` | 列出所有流程阶段 |
| `LEVER_LIST_TAGS` | 列出所有用于分类的标签 |

---

*Powered by [Composio](https://composio.dev)*

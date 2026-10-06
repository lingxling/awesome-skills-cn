---
name: Workday Automation
description: "自动化 Workday 中的人力资源操作 —— 通过自然语言指令管理员工、请假申请、休假余额和员工数据。"
requires:
  mcp:
    - rube
---

# Workday Automation

直接从 Claude Code 自动化你的 Workday 人力资源操作。查找员工、创建请假申请、检查休假余额，以及验证请假资格 —— 全程无需离开终端。

**工具包文档：** [composio.dev/toolkits/workday](https://composio.dev/toolkits/workday)

---

## 设置

1. 将 Rube MCP 服务器添加到你的 Claude Code 配置中，URL 为：`https://rube.app/mcp`
2. 收到提示时，通过提供的连接链接对你的 Workday 账户进行身份验证
3. 开始用自然语言自动化你的 HR 工作流

---

## 核心工作流

### 1. 搜索并列出员工

检索员工信息，支持搜索和分页。

**工具：** `WORKDAY_LIST_WORKERS`

```
Search for workers named "Sarah" and include terminated employees
```

关键参数：
- `search` —— 按姓名或员工 ID 搜索（不区分大小写，用空格分隔表示“或”搜索）
- `includeTerminatedWorkers` —— 结果中是否包含已离职员工
- `limit`（默认 20，最大 100）/ `offset` —— 分页控制

### 2. 创建请假申请

为员工提交请假申请，完整支持业务流程。

**工具：** `WORKDAY_CREATE_TIME_OFF_REQUEST`

```
Create a vacation request for worker abc123 for March 15-17, 2026 (8 hours each day)
```

关键参数：
- `ID`（必需）—— Workday 员工 ID
- `businessProcessParameters`（必需）—— 必须包含带 `id` 字段的 `action`（提交操作使用 `"d9e4223e446c11de98360015c5e6daf6"`）
- `days`（必需）—— 请假条目数组，每项包含：
  - `date`（必需）—— `yyyy-mm-dd` 格式的日期
  - `timeOffType`（必需）—— 包含符合条件的休假类型 `id` 的对象
  - `dailyQuantity` —— 小时数或天数
  - `comment`、`start`、`end`、`position`、`reason` —— 可选字段
- `businessProcessParameters.comment` —— 可选的业务流程备注

### 3. 检查请假资格

在提交申请之前，验证员工可以请假的日期。

**工具：** `WORKDAY_GET_WORKER_VALID_TIME_OFF_DATES`

```
Check if worker abc123 is eligible to take time off on March 15, 2026
```

关键参数：
- `ID`（必需）—— Workday 员工 ID
- `date` —— 要验证的特定日期（`yyyy-mm-dd`）
- `position` —— 按特定职位 ID 筛选
- `timeOff` —— 按特定休假方案/类型 ID 筛选
- `limit`（最大 100）/ `offset` —— 分页

### 4. 查看休假余额

查看组织内员工在各休假方案下的剩余休假余额。

**工具：** `WORKDAY_LIST_ABSENCE_BALANCES`

```
Show me absence balances for all workers in the organization
```

- 检索休假方案和请假类型的余额
- 可按员工 ID、类别和生效日期进行筛选

### 5. 获取当前用户的个人资料

检索已通过身份验证员工的个人资料信息。

**工具：** `WORKDAY_GET_CURRENT_USER`

```
Show me my Workday profile information
```

- 不需要任何参数
- 返回经过身份验证员工的个人资料
- 使用此工具首先获取员工 ID，以供后续操作使用

### 6. 查看请假历史

检索特定员工的请假详情和历史记录。

**工具：** `WORKDAY_GET_WORKER_TIME_OFF_DETAILS`

```
Show me the time off history for worker abc123
```

- 检索指定员工的一组请假详情
- 便于审计请假使用情况和剩余余额

---

## 已知问题

- **员工 ID 解析：** 务必先调用 `WORKDAY_GET_CURRENT_USER` 或 `WORKDAY_LIST_WORKERS` 来解析 Workday 员工 ID。员工 ID 是 Workday 专用的 UUID，并非员工工号。
- **请假类型 ID 必须有效：** `WORKDAY_CREATE_TIME_OFF_REQUEST` 中的 `timeOffType.id` 必须引用该员工有效的符合条件的休假类型。使用“获取员工符合条件的休假类型”流程来发现有效的类型 ID。
- **提交操作 ID：** `businessProcessParameters.action.id` 对于提交操作应为 `"d9e4223e446c11de98360015c5e6daf6"`。使用错误的 ID 会导致业务流程失败。
- **日期格式：** 所有日期字段均使用 `yyyy-mm-dd` 格式。带时间戳的 ISO 8601 格式对纯日期字段不被接受。
- **分页限制：** 所有 Workday 端点的最大 `limit` 为 100，默认值为 20。务必进行分页以获取完整数据集。
- **业务流程审批：** 创建请假申请会启动业务流程，但不保证获得批准。该申请将进入正常的审批工作流。

---

## 快速参考

| 工具标识 | 描述 |
|---|---|
| `WORKDAY_LIST_WORKERS` | 搜索并列出员工及其在职信息 |
| `WORKDAY_GET_CURRENT_USER` | 获取已通过身份验证员工的个人资料 |
| `WORKDAY_CREATE_TIME_OFF_REQUEST` | 提交请假申请（需要 `ID`、`businessProcessParameters`、`days`） |
| `WORKDAY_GET_WORKER_VALID_TIME_OFF_DATES` | 检查请假日期资格（需要 `ID`） |
| `WORKDAY_LIST_ABSENCE_BALANCES` | 检索各休假方案下的休假余额 |
| `WORKDAY_GET_WORKER_TIME_OFF_DETAILS` | 获取员工的请假历史 |

---

*Powered by [Composio](https://composio.dev)*

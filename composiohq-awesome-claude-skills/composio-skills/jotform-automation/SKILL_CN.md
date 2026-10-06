---
name: Jotform Automation
description: "通过自然语言命令自动化 Jotform 表单列表、用户管理、活动历史、文件夹整理和套餐查询"
requires:
  mcp:
    - rube
---

# Jotform Automation

自动化 Jotform 工作流 -- 列出和搜索表单、查看用户详情、浏览活动历史、管理文件夹和标签、检查套餐限制 -- 全部通过自然语言完成。

**工具包文档：** [composio.dev/toolkits/jotform](https://composio.dev/toolkits/jotform)

---

## 设置

1. 将 Rube MCP 服务器添加到你的环境中：`https://rube.app/mcp`
2. 按提示连接你的 Jotform 账户（通过 Composio 进行 API 密钥认证）
3. 开始使用自然语言命令进行 Jotform 自动化操作

---

## 核心工作流

### 1. 列出和搜索表单

获取已认证用户创建的所有表单，支持搜索、筛选、排序和分页。

**工具：** `JOTFORM_GET_USER_FORMS`

关键参数：
- `search` -- 按名称或内容筛选表单的搜索查询
- `limit` -- 要返回的表单数量
- `offset` -- 分页偏移量
- `orderby` -- 排序所依据的字段
- `sorting` -- 排序方向：`ASC` 或 `DESC`
- `folder` -- 按文件夹 ID 筛选

示例提示词：
> "列出我所有名称中包含 'feedback' 的 Jotform 表单，按最新排序"

---

### 2. 获取用户账户详情

获取已认证用户的详情，包括账户类型、使用统计和限制。

**工具：** `JOTFORM_GET_USER_DETAILS`

无需参数。返回用户名、邮箱、账户类型、表单数量、提交数量和使用限制等账户信息。

示例提示词：
> "给我看我的 Jotform 账户详情和当前用量"

---

### 3. 浏览活动历史

获取用户活动记录用于审计，支持按操作类型和日期范围筛选。

**工具：** `JOTFORM_GET_USER_HISTORY`

关键参数：
- `action` -- 按操作类型筛选（例如 `formCreation`、`userLogin`、`formUpdate`、`apiKeyCreated`、`userLogout`）
- `date` -- 预定义日期范围：`lastWeek`、`lastMonth`、`last3Months`、`last6Months`、`lastYear`、`all`
- `startDate` -- 自定义开始日期，格式为 `MM/DD/YYYY`
- `endDate` -- 自定义结束日期，格式为 `MM/DD/YYYY`
- `sortBy` -- 排序方式：`ASC` 或 `DESC`

示例提示词：
> "给我看过去一个月内所有的表单创建活动，按最新排序"

---

### 4. 管理文件夹和标签

浏览用于整理表单的文件夹/标签结构。

**工具：** `JOTFORM_GET_USER_FOLDERS`

关键参数：
- `add_resources` -- 设置为 `true` 以在响应中包含标签资源（表单）
- `owner` -- 所有者用户名或工作区/团队 ID（某些账户下为条件必填）

> Jotform 已从文件夹迁移到标签系统。此工具使用的是 `GET /user/labels` 接口。

示例提示词：
> "列出我所有的 Jotform 文件夹及其包含的表单"

---

### 5. 检查套餐限制和定价

获取特定 Jotform 系统套餐的详情，以了解其限制和功能。

**工具：** `JOTFORM_GET_SYSTEM_PLAN`

关键参数：
- `planName` -- 要查看的套餐（必填）：`FREE`、`BRONZE`、`SILVER`、`GOLD` 或 `PLATINUM`

示例提示词：
> "Jotform GOLD 套餐的限制是什么？"

---

### 6. 完整表单管理工作流

组合多个工具实现全面的表单管理：

1. **了解**：`JOTFORM_GET_USER_DETAILS` -- 检查账户类型和使用限制
2. **浏览**：`JOTFORM_GET_USER_FORMS` -- 带筛选条件列出和搜索表单
3. **整理**：`JOTFORM_GET_USER_FOLDERS` -- 使用 `add_resources=true` 查看文件夹结构
4. **审计**：`JOTFORM_GET_USER_HISTORY` -- 跟踪表单创建和修改活动
5. **规划**：`JOTFORM_GET_SYSTEM_PLAN` -- 升级前比较套餐功能

示例提示词：
> "给我看我的账户用量，列出我最近的表单，并告诉我是否接近套餐限制"

---

## 常见陷阱

| 陷阱 | 详情 |
|---------|---------|
| API 密钥认证 | Jotform 使用 API 密钥认证，而不是 OAuth -- 请确保连接中配置了有效的 API 密钥 |
| 文件夹已迁移到标签 | 文件夹接口现在映射到 Jotform 的标签系统；API 行为可能与旧版文件夹文档有所不同 |
| 历史记录的日期格式 | 自定义日期筛选使用 `MM/DD/YYYY` 格式（例如 `01/15/2026`），而不是 ISO 8601 |
| 套餐名称必须精确 | `planName` 的取值是大小写敏感的枚举：`FREE`、`BRONZE`、`SILVER`、`GOLD`、`PLATINUM` |
| 分页基于偏移量 | 表单使用 `limit`/`offset` 分页，而不是游标或页码分页 |
| owner 字段为条件必填 | 对于工作区/团队账户，`JOTFORM_GET_USER_FOLDERS` 可能需要提供 `owner` 参数 |

---

## 快速参考

| 操作 | 工具标识 | 关键参数 |
|--------|-----------|------------|
| 列出表单 | `JOTFORM_GET_USER_FORMS` | `search`、`limit`、`offset`、`orderby` |
| 获取用户详情 | `JOTFORM_GET_USER_DETAILS` | （无） |
| 活动历史 | `JOTFORM_GET_USER_HISTORY` | `action`、`date`、`startDate`、`endDate` |
| 列出文件夹/标签 | `JOTFORM_GET_USER_FOLDERS` | `add_resources`、`owner` |
| 检查套餐 | `JOTFORM_GET_SYSTEM_PLAN` | `planName` |

---

*由 [Composio](https://composio.dev) 提供支持*

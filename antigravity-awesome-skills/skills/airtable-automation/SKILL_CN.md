---
name: airtable-automation
description: "通过 Rube MCP (Composio) 自动化 Airtable 任务：记录、库、表、字段、视图。始终首先搜索工具以获取当前模式。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Airtable 自动化

通过 Rube MCP 的 Composio Airtable 工具包自动化 Airtable 操作。

## 前置条件

- 必须连接 Rube MCP（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 与工具包 `airtable` 的活动 Airtable 连接
- 始终首先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具模式

## 设置

**获取 Rube MCP**：在您的客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——只需添加端点即可工作。

1. 通过确认 `RUBE_SEARCH_TOOLS` 响应来验证 Rube MCP 可用
2. 用工具包 `airtable` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是 ACTIVE，请按照返回的授权链接完成 Airtable 授权
4. 在运行任何工作流之前，确认连接状态显示 ACTIVE

## 核心工作流

### 1. 创建和管理记录

**何时使用**：用户想创建、读取、更新或删除记录

**工具序列**：
1. `AIRTABLE_LIST_BASES` - 发现可用库 [前置条件]
2. `AIRTABLE_GET_BASE_SCHEMA` - 检查表结构 [前置条件]
3. `AIRTABLE_LIST_RECORDS` - 列出/过滤记录 [可选]
4. `AIRTABLE_CREATE_RECORD` / `AIRTABLE_CREATE_RECORDS` - 创建记录 [可选]
5. `AIRTABLE_UPDATE_RECORD` / `AIRTABLE_UPDATE_MULTIPLE_RECORDS` - 更新记录 [可选]
6. `AIRTABLE_DELETE_RECORD` / `AIRTABLE_DELETE_MULTIPLE_RECORDS` - 删除记录 [可选]

**关键参数**：
- `baseId`：库 ID（以 'app' 开头，例如 'appXXXXXXXXXXXXXX'）
- `tableIdOrName`：表 ID（以 'tbl' 开头）或表名称
- `fields`：将字段名称映射到值的对象
- `recordId`：记录 ID（以 'rec' 开头）用于更新/删除
- `filterByFormula`：用于过滤的 Airtable 公式
- `typecast`：设置为 true 以进行自动类型转换

**缺陷**：
- pageSize 上限为 100；使用偏移分页；在页面间更改过滤器可能会跳过/重复行
- CREATE_RECORDS 硬限制为每个请求 10 条记录；分块更大的导入
- 字段名称区分大小写且必须与模式完全匹配
- 字段名称错误时出现 422 UNKNOWN_FIELD_NAME；权限问题时出现 403
- INVALID_MULTIPLE_CHOICE_OPTIONS 可能需要 typecast=true

### 2. 搜索和过滤记录

**何时使用**：用户想使用公式查找特定记录

**工具序列**：
1. `AIRTABLE_GET_BASE_SCHEMA` - 验证字段名称和类型 [前置条件]
2. `AIRTABLE_LIST_RECORDS` - 使用 filterByFormula 查询 [必需]
3. `AIRTABLE_GET_RECORD` - 获取完整记录详情 [可选]

**关键参数**：
- `filterByFormula`：Airtable 公式（例如 `{Status}='Done'`）
- `sort`：排序对象数组
- `fields`：要返回的字段名称数组
- `maxRecords`：所有页面中的最大记录数
- `offset`：来自前一个响应的分页游标

**缺陷**：
- 公式中的字段名称必须用 `{}` 包装且与模式完全匹配
- 字符串值必须引用：`{Status}='Active'` 而不是 `{Status}=Active`
- 422 INVALID_FILTER_BY_FORMULA 表示语法不当或字段不存在
- Airtable 速率限制：~5 请求/秒每个库；用 Retry-After 处理 429

### 3. 管理字段和模式

**何时使用**：用户想创建或修改表字段

**工具序列**：
1. `AIRTABLE_GET_BASE_SCHEMA` - 检查当前模式 [前置条件]
2. `AIRTABLE_CREATE_FIELD` - 创建新字段 [可选]
3. `AIRTABLE_UPDATE_FIELD` - 重命名/描述字段 [可选]
4. `AIRTABLE_UPDATE_TABLE` - 更新表元数据 [可选]

**关键参数**：
- `name`：字段名称
- `type`：字段类型（singleLineText、number、singleSelect 等）
- `options`：特定于类型的选项（选择的选项、数字的精度）
- `description`：字段描述

**缺陷**：
- UPDATE_FIELD 仅更改名称/描述，NOT 类型/选项；创建替代字段并迁移
- 计算字段（公式、汇总、查找）不能通过 API 创建
- 422 当类型选项缺失或格式错误时

### 4. 管理注释

**何时使用**：用户想查看或添加记录上的注释

**工具序列**：
1. `AIRTABLE_LIST_COMMENTS` - 列出记录上的注释 [必需]

**关键参数**：
- `baseId`：库 ID
- `tableIdOrName`：表标识符
- `recordId`：记录 ID（17 个字符，以 'rec' 开头）
- `pageSize`：每页注释数（最多 100）

**缺陷**：
- 记录 ID 必须恰好是 17 个字符，以 'rec' 开头

## 常见模式

### Airtable 公式语法

**比较**：
- `{Status}='Done'` - 等于
- `{Priority}>1` - 大于
- `{Name}!=''` - 非空

**函数**：
- `AND({A}='x', {B}='y')` - 两个条件
- `OR({A}='x', {A}='y')` - 任一条件
- `FIND('test', {Name})>0` - 包含文本
- `IS_BEFORE({Due Date}, TODAY())` - 日期比较

**转义规则**：
- 值中的单引号：加倍（`{Name}='John''s Company'`）

### 分页

- 设置 `pageSize`（最多 100）
- 检查响应中的 `offset` 字符串
- 将 `offset` 原样传递给下一个请求
- 在页面间保持过滤器/排序/视图稳定

## 已知缺陷

**ID 格式**：
- 库 ID：`appXXXXXXXXXXXXXX`（17 个字符）
- 表 ID：`tblXXXXXXXXXXXXXX`（17 个字符）
- 记录 ID：`recXXXXXXXXXXXXXX`（17 个字符）
- 字段 ID：`fldXXXXXXXXXXXXXX`（17 个字符）

**批处理限制**：
- CREATE_RECORDS：每个请求最多 10 个
- UPDATE_MULTIPLE_RECORDS：每个请求最多 10 个
- DELETE_MULTIPLE_RECORDS：每个请求最多 10 个

## 快速参考

| 任务 | 工具 Slug | 关键参数 |
|------|-----------|---------|
| 列出库 | AIRTABLE_LIST_BASES | (无) |
| 获取模式 | AIRTABLE_GET_BASE_SCHEMA | baseId |
| 列出记录 | AIRTABLE_LIST_RECORDS | baseId, tableIdOrName |
| 获取记录 | AIRTABLE_GET_RECORD | baseId, tableIdOrName, recordId |
| 创建记录 | AIRTABLE_CREATE_RECORD | baseId, tableIdOrName, fields |
| 创建记录 | AIRTABLE_CREATE_RECORDS | baseId, tableIdOrName, records |
| 更新记录 | AIRTABLE_UPDATE_RECORD | baseId, tableIdOrName, recordId, fields |
| 更新记录 | AIRTABLE_UPDATE_MULTIPLE_RECORDS | baseId, tableIdOrName, records |
| 删除记录 | AIRTABLE_DELETE_RECORD | baseId, tableIdOrName, recordId |
| 创建字段 | AIRTABLE_CREATE_FIELD | baseId, tableIdOrName, name, type |
| 更新字段 | AIRTABLE_UPDATE_FIELD | baseId, tableIdOrName, fieldId |
| 更新表 | AIRTABLE_UPDATE_TABLE | baseId, tableIdOrName, name |
| 列出注释 | AIRTABLE_LIST_COMMENTS | baseId, tableIdOrName, recordId |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 示例

**用户请求：**

> 通过 Rube MCP (Composio) 自动化 Airtable 任务：记录、库、表、字段、视图。

## 限制
- 仅在任务与上述描述范围明确匹配时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并寻求澄清。

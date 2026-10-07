---
name: circleci-automation
description: "通过Rube MCP (Composio)自动化CircleCI任务：触发管道、监控工作流/作业、检索工件和测试元数据。始终首先搜索工具以获取当前的schemas。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过Rube MCP进行CircleCI自动化

通过Composio的CircleCI工具包通过Rube MCP自动化CircleCI CI/CD操作。

## 先决条件

- Rube MCP必须连接（RUBE_SEARCH_TOOLS可用）
- 通过`RUBE_MANAGE_CONNECTIONS`的活跃CircleCI连接，使用工具包`circleci`
- 始终首先调用`RUBE_SEARCH_TOOLS`以获取当前的工具schemas

## 设置

**获取Rube MCP**：在客户端配置中添加`https://rube.app/mcp`作为MCP服务器。不需要API密钥 — 只需添加端点即可使用。


1. 通过确认`RUBE_SEARCH_TOOLS`响应来验证Rube MCP可用
2. 使用工具包`circleci`调用`RUBE_MANAGE_CONNECTIONS`
3. 如果连接不是ACTIVE，请按照返回的身份验证链接完成CircleCI身份验证
4. 在运行任何工作流之前，确认连接状态显示为ACTIVE

## 核心工作流

### 1. 触发管道

**何时使用**：用户想要启动新的CI/CD管道运行

**工具序列**：
1. `CIRCLECI_TRIGGER_PIPELINE` - 在项目上触发新管道 [必需]
2. `CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID` - 监控生成的工作流 [可选]

**关键参数**：
- `project_slug`：项目标识符，格式为`gh/org/repo`或`bb/org/repo`
- `branch`：运行管道的Git分支
- `tag`：运行管道的Git标签（与分支互斥）
- `parameters`：管道参数键值对

**陷阱**：
- `project_slug`格式为`{vcs}/{org}/{repo}`（例如，`gh/myorg/myrepo`）
- `branch`和`tag`互斥；同时提供两者会导致错误
- 管道参数必须与`.circleci/config.yml`中定义的参数匹配
- 触发返回管道ID；工作流异步启动

### 2. 监控管道和工作流

**何时使用**：用户想要检查管道或工作流的状态

**工具序列**：
1. `CIRCLECI_LIST_PIPELINES_FOR_PROJECT` - 列出项目的最近管道 [必需]
2. `CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID` - 列出管道中的工作流 [必需]
3. `CIRCLECI_GET_PIPELINE_CONFIG` - 查看使用的管道配置 [可选]

**关键参数**：
- `project_slug`：项目标识符，格式为`{vcs}/{org}/{repo}`
- `pipeline_id`：特定管道的UUID
- `branch`：按分支名称过滤管道
- `page_token`：下一页结果的分页游标

**陷阱**：
- 管道ID是UUID，不是数字ID
- 工作流继承管道ID；单个管道可以有多个工作流
- 工作流状态包括：success、running、not_run、failed、error、failing、on_hold、canceled、unauthorized
- `page_token`在响应中返回以进行分页；继续直到缺少

### 3. 检查作业详情

**何时使用**：用户想要钻入特定作业的执行详情

**工具序列**：
1. `CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID` - 查找包含作业的工作流 [前提条件]
2. `CIRCLECI_GET_JOB_DETAILS` - 获取详细的作业信息 [必需]

**关键参数**：
- `project_slug`：项目标识符
- `job_number`：数字作业编号（不是UUID）

**陷阱**：
- 作业编号是整数，不是UUID（与管道和工作流ID不同）
- 作业详情包括执行器类型、并行性、开始/停止时间和状态
- 作业状态：success、running、not_run、failed、retried、timedout、infrastructure_fail、canceled

### 4. 检索构建工件

**何时使用**：用户想要下载或列出作业产生的工件

**工具序列**：
1. `CIRCLECI_GET_JOB_DETAILS` - 确认作业成功完成 [前提条件]
2. `CIRCLECI_GET_JOB_ARTIFACTS` - 列出作业中的所有工件 [必需]

**关键参数**：
- `project_slug`：项目标识符
- `job_number`：数字作业编号

**陷阱**：
- 工件仅在作业完成后可用
- 每个工件都有一个`path`和`url`用于下载
- 工件URL可能需要身份验证标头才能下载
- 大工件可能具有下载大小限制

### 5. 查看测试结果

**何时使用**：用户想要检查特定作业的测试结果

**工具序列**：
1. `CIRCLECI_GET_JOB_DETAILS` - 验证作业运行了测试 [前提条件]
2. `CIRCLECI_GET_TEST_METADATA` - 检索测试结果和元数据 [必需]

**关键参数**：
- `project_slug`：项目标识符
- `job_number`：数字作业编号

**陷阱**：
- 测试元数据要求作业已上载测试结果（JUnit XML格式）
- 如果没有上载测试结果，响应将为空
- 测试元数据包括classname、name、result、message和run_time字段
- 失败的测试在`message`字段中包括失败消息

## 常见模式

### 项目Slug格式

```
格式：{vcs_type}/{org_name}/{repo_name}
- GitHub:    gh/myorg/myrepo
- Bitbucket: bb/myorg/myrepo
```

### 管道 -> 工作流 -> 作业层次结构

```
1. 调用CIRCLECI_LIST_PIPELINES_FOR_PROJECT以获取管道ID
2. 使用pipeline_id调用CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID
3. 从工作流详情中提取作业编号
4. 使用job_number调用CIRCLECI_GET_JOB_DETAILS
```

### 分页

- 检查响应中的`next_page_token`字段
- 在下一个请求中将令牌作为`page_token`传递
- 继续直到`next_page_token`缺少或为null

## 已知陷阱

**ID格式**：
- 管道ID：UUID（例如，`5034460f-c7c4-4c43-9457-de07e2029e7b`）
- 工作流ID：UUID
- 作业编号：整数（例如，`123`）
- 不要在不同端点之间混淆UUID和整数

**项目Slugs**：
- 必须包括VCS前缀：GitHub为`gh/`，Bitbucket为`bb/`
- 组织和repo名称区分大小写
- 不正确的slug格式导致404错误

**速率限制**：
- CircleCI API具有每个端点的速率限制
- 在429响应上实施指数退避
- 避免快速轮询；使用合理的间隔（5-10秒）

## 快速参考

| 任务 | 工具Slug | 关键参数 |
|------|-----------|------------|
| 触发管道 | CIRCLECI_TRIGGER_PIPELINE | project_slug、branch、parameters |
| 列出管道 | CIRCLECI_LIST_PIPELINES_FOR_PROJECT | project_slug、branch |
| 列出工作流 | CIRCLECI_LIST_WORKFLOWS_BY_PIPELINE_ID | pipeline_id |
| 获取管道配置 | CIRCLECI_GET_PIPELINE_CONFIG | pipeline_id |
| 获取作业详情 | CIRCLECI_GET_JOB_DETAILS | project_slug、job_number |
| 获取作业工件 | CIRCLECI_GET_JOB_ARTIFACTS | project_slug、job_number |
| 获取测试元数据 | CIRCLECI_GET_TEST_METADATA | project_slug、job_number |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述描述的范围时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。

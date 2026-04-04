---
name: Ashby Automation
description: "自动化 Ashby 招聘和招聘工作流 -- 管理候选人、职位、申请和备注，通过自然语言命令。"
requires:
  mcp:
    - rube
---

# Ashby 自动化

直接从 Claude Code 自动化您的 Ashby ATS 招聘操作。创建候选人、发布职位、管理申请、查看面试计划，并搜索您的人才管道 — 全部无需离开终端。

**工具包文档:** [composio.dev/toolkits/ashby](https://composio.dev/toolkits/ashby)

---

## 设置

1. 将 Rube MCP 服务器添加到您的 Claude Code 配置，URL：`https://rube.app/mcp`
2. 在提示时通过提供的连接链接认证您的 Ashby 账户
3. 开始使用自然语言自动化您的招聘工作流

---

## 核心工作流

### 1. 管理候选人

创建、列出、搜索、更新和检索详细的候选人信息。

**工具：** `ASHBY_CREATE_CANDIDATE`、`ASHBY_LIST_CANDIDATES`、`ASHBY_SEARCH_CANDIDATES`、`ASHBY_GET_CANDIDATE_INFO`、`ASHBY_UPDATE_CANDIDATE`

```
创建一个名为 "Jane Smith" 的候选人，电子邮件为 jane@example.com，LinkedIn 个人资料为 https://linkedin.com/in/janesmith
```

**`ASHBY_CREATE_CANDIDATE` 的关键参数：**
- `name`（必需）-- 候选人的全名
- `email` -- 主要电子邮件地址
- `phoneNumber`、`linkedInUrl`、`githubUrl`、`websiteUrl` -- 联系人/社交个人资料

**`ASHBY_SEARCH_CANDIDATES` 的关键参数：**
- `email` -- 精确的电子邮件匹配
- `name` -- 部分名称匹配

**`ASHBY_LIST_CANDIDATES` 的关键参数：**
- `perPage`（最多 100） / `cursor` -- 分页
- `syncToken` -- 用于自上次同步以来的增量更新

### 2. 创建和列出职位

发布新的职位空缺并浏览现有职位。

**工具：** `ASHBY_CREATE_JOB`、`ASHBY_LIST_JOBS`、`ASHBY_GET_JOB_INFO`

```
在部门 dept-123、位置 loc-456、品牌 brand-789 创建一个新的 "高级软件工程师" 职位
```

**`ASHBY_CREATE_JOB` 的关键参数：**
- `title`（必需）-- 职位名称
- `teamId`（必需）-- 部门/团队 ID（来自列出部门）
- `locationId`（必需）-- 办公位置 ID（来自列出位置）
- `brandId`（必需）-- 雇主品牌 ID（来自列出品牌）
- `defaultInterviewPlanId` -- 必需，用于开放职位以接受申请
- `jobTemplateId` -- 从模板预填充

**`ASHBY_LIST_JOBS` 的关键参数：**
- `perPage`（最多 100） / `cursor` / `syncToken` -- 分页和增量同步

**注意：** 通过 `ASHBY_CREATE_JOB` 新创建的职位默认处于"草稿"状态。您必须设置 `defaultInterviewPlanId` 才能开放/发布职位。

### 3. 管理申请

创建申请以将候选人连接到职位并跟踪其进度。

**工具：** `ASHBY_CREATE_APPLICATION`、`ASHBY_LIST_APPLICATIONS`

```
将候选人 cand-abc123 应用于职位 job-xyz789，来源为 src-referral
```

**`ASHBY_CREATE_APPLICATION` 的关键参数：**
- `candidateId`（必需）-- 现有候选人的 UUID
- `jobId`（必需）-- 现有职位的 UUID
- `sourceId` -- 申请来源的 UUID（LinkedIn、Referral 等）
- `creditedToUserId` -- 要记功的招聘人员/推荐人的 UUID
- `interviewStageId` -- 直接放入特定阶段（默认为第一阶段）

**`ASHBY_LIST_APPLICATIONS` 的关键参数：**
- `perPage`（最多 100） / `cursor` / `syncToken` -- 分页和增量同步

### 4. 查看面试计划

列出包含时间、面试官和候选人详情的预定面试。

**工具：** `ASHBY_LIST_INTERVIEW_SCHEDULES`

```
显示我所有即将到来的面试计划
```

**关键参数：**
- `perPage`（最多 100） / `cursor` -- 分页
- `syncToken` -- 用于更改计划的增量同步

### 5. 候选人备注

查看招聘团队成员和招聘经理添加的内部备注、观察和评论。

**工具：** `ASHBY_LIST_CANDIDATE_NOTES`

```
显示候选人 cand-abc123 的所有备注
```

- 检索招聘人员和团队成员添加的所有备注
- 适用于查看面试反馈和内部评估

### 6. 管道报告

组合列出工具以构建招聘管理道报告。

**工具：** `ASHBY_LIST_CANDIDATES`、`ASHBY_LIST_APPLICATIONS`、`ASHBY_LIST_JOBS`

```
列出所有申请以查看我们招聘管道的当前状态
```

- 使用 `syncToken` 仅获取更改的记录（对于重复报告效率很高）
- 组合候选人、申请和职位数据以获得完整的管道可见性
- 使用 `cursor` 分页所有结果以获取完整数据集

---

## 已知陷阱

- **职位默认为草稿：** 通过 `ASHBY_CREATE_JOB` 新创建的职位默认处于"草稿"状态，无法接受申请，直到设置了 `defaultInterviewPlanId` 且职位被开放。
- **职位需要四个必填字段：** `ASHBY_CREATE_JOB` 需要 `title`、`teamId`、`locationId` 和 `brandId`。使用列出部门、位置和品牌端点发现有效的 ID。
- **申请前必须有候选人：** 必须先创建或查找候选人，然后创建申请。始终先创建/查找候选人，然后创建申请。
- **基于游标的分页：** 所有列表端点使用基于游标的分页，包含 `perPage`（最多 100）和 `cursor`。您无法跳转到任意页面 — 必须按顺序迭代。
- **`syncToken` 提高效率：** 使用先前响应中的 `syncToken` 仅获取更改的记录。这显著减少了重复工作流的 API 调用。
- **所有地方都是 UUID：** 所有 ID（候选人、职位、申请、阶段）都是 UUID。传递格式错误的 ID 会返回 400 错误。
- **搜索限制：** `ASHBY_SEARCH_CANDIDATES` 支持精确的电子邮件匹配或部分名称匹配，但不支持组合查询或其他字段。对于更广泛的搜索，请使用 `ASHBY_LIST_CANDIDATES` 进行分页。

---

## 快速参考

| 工具标识符 | 描述 |
|---|---|
| `ASHBY_CREATE_CANDIDATE` | 创建新候选人（需要 `name`） |
| `ASHBY_LIST_CANDIDATES` | 列出所有候选人，支持分页和同步 |
| `ASHBY_SEARCH_CANDIDATES` | 按电子邮件或姓名搜索候选人 |
| `ASHBY_GET_CANDIDATE_INFO` | 获取完整候选人详情（需要 `candidateId`） |
| `ASHBY_UPDATE_CANDIDATE` | 更新候选人个人资料信息 |
| `ASHBY_LIST_CANDIDATE_NOTES` | 列出候选人的内部备注 |
| `ASHBY_CREATE_JOB` | 创建职位空缺（需要 `title`、`teamId`、`locationId`、`brandId`） |
| `ASHBY_LIST_JOBS` | 列出所有职位，支持分页和同步 |
| `ASHBY_GET_JOB_INFO` | 按 ID 获取完整职位详情 |
| `ASHBY_CREATE_APPLICATION` | 将候选人应用于职位（需要 `candidateId`、`jobId`） |
| `ASHBY_LIST_APPLICATIONS` | 列出所有申请，支持分页和同步 |
| `ASHBY_LIST_INTERVIEW_SCHEDULES` | 列出预定面试，支持分页 |

---

*由 [Composio](https://composio.dev) 提供支持*

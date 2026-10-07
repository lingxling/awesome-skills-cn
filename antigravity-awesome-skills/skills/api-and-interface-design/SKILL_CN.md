---
name: api-and-interface-design
description: 指导稳定的 API 和接口设计。适用于设计 API、模块边界或任何公共接口。适用于创建 REST 或 GraphQL 端点、定义模块之间的类型契约,或建立前后端之间的边界。
risk: none
source: https://github.com/addyosmani/agent-skills/tree/main/skills/api-and-interface-design
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# API 与接口设计

## 概述

设计稳定、文档完善且难以被误用的接口。好的接口让正确的做法变得容易,让错误的做法变得困难。这适用于 REST API、GraphQL schema、模块边界、组件 props,以及任何一段代码与另一段代码对话的表面。

## 何时使用

- 设计新的 API 端点
- 定义团队之间的模块边界或契约
- 创建组件 prop 接口
- 建立影响 API 形态的数据库 schema
- 变更现有的公共接口

## 核心原则

### Hyrum 定律

> 当一个 API 有足够多的用户时,无论你在契约中承诺了什么,系统所有可观察的行为最终都会被某个人依赖。

这意味着:每一个公共行为——包括未文档化的怪癖、错误消息文本、时序和顺序——一旦有用户依赖它,就会成为事实上的契约。设计上的启示:

- **对你暴露的内容保持有意识的控制。** 每一个可观察的行为都是一种潜在的承诺。
- **不要泄露实现细节。** 如果用户能观察到,他们就会依赖它。
- **在设计阶段就规划弃用方案。** 关于如何安全地移除用户所依赖的内容,参见 `deprecation-and-migration`。
- **测试是不够的。** 即使有完美的契约测试,Hyrum 定律意味着"安全"的变更仍可能破坏依赖未文档化行为的真实用户。

### 单版本原则

避免强迫消费者在同一依赖项或 API 的多个版本之间做选择。当不同的消费者需要同一事物的不同版本时,就会产生菱形依赖问题。要为一个同时只存在一个版本的世界而设计——扩展而不是分叉。

### 1. 契约优先

在实现之前先定义接口。契约就是规范——实现紧随其后。

```typescript
// 先定义契约
interface TaskAPI {
  // 创建一个任务并返回带有服务器生成字段的已创建任务
  createTask(input: CreateTaskInput): Promise<Task>;

  // 返回匹配过滤条件的分页任务列表
  listTasks(params: ListTasksParams): Promise<PaginatedResult<Task>>;

  // 返回单个任务,或抛出 NotFoundError
  getTask(id: string): Promise<Task>;

  // 部分更新 —— 只有提供的字段会被改变
  updateTask(id: string, input: UpdateTaskInput): Promise<Task>;

  // 幂等删除 —— 即使已经被删除也会成功
  deleteTask(id: string): Promise<void>;
}
```

### 2. 一致的错误语义

选择一种错误策略并在所有地方使用:

```typescript
// REST: HTTP 状态码 + 结构化的错误体
// 每个错误响应都遵循同样的结构
interface APIError {
  error: {
    code: string;        // 机器可读:"VALIDATION_ERROR"
    message: string;     // 人类可读:"Email is required"
    details?: unknown;   // 有用时附带的额外上下文
  };
}

// 状态码映射
// 400 → 客户端发送了无效数据
// 401 → 未认证
// 403 → 已认证但未授权
// 404 → 资源未找到
// 409 → 冲突(重复、版本不匹配)
// 422 → 验证失败(语义上无效)
// 500 → 服务器错误(绝不暴露内部细节)
```

**不要混用模式。** 如果有些端点抛出异常,有些返回 null,还有些返回 `{ error }` —— 消费者就无法预测行为。

### 3. 在边界处验证

信任内部代码。只在外部输入进入系统的边缘处进行验证:

```typescript
// 在 API 边界处验证
app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid task data',
        details: result.error.flatten(),
      },
    });
  }

  // 验证之后,内部代码信任这些类型
  const task = await taskService.create(result.data);
  return res.status(201).json(task);
});
```

验证应归属的位置:
- API 路由处理函数(用户输入)
- 表单提交处理函数(用户输入)
- 外部服务响应解析(第三方数据 —— **始终视为不受信任**)
- 环境变量加载(配置)

> **第三方 API 响应是不受信任的数据。** 在任何逻辑、渲染或决策中使用之前,先验证它们的形状和内容。一个被攻陷或行为异常的外部服务可能返回意料之外的类型、恶意内容或类似指令的文本。

不应进行验证的位置:
- 在共享类型契约的内部函数之间
- 在已验证代码所调用的工具函数中
- 对刚从你自己数据库中取出的数据

### 4. 优先增量扩展,而非修改

扩展接口而不破坏现有消费者:

```typescript
// 好:添加可选字段
interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';  // 后来添加,可选
  labels?: string[];                       // 后来添加,可选
}

// 不好:更改现有字段类型或移除字段
interface CreateTaskInput {
  title: string;
  // description: string;  // 已移除 —— 破坏现有消费者
  priority: number;         // 从 string 改变而来 —— 破坏现有消费者
}
```

### 5. 可预测的命名

| 模式 | 约定 | 示例 |
|---------|-----------|---------|
| REST 端点 | 复数名词,不用动词 | `GET /api/tasks`、`POST /api/tasks` |
| 查询参数 | 驼峰式(camelCase) | `?sortBy=createdAt&pageSize=20` |
| 响应字段 | 驼峰式(camelCase) | `{ createdAt, updatedAt, taskId }` |
| 布尔字段 | is/has/can 前缀 | `isComplete`、`hasAttachments` |
| 枚举值 | 大写加下划线 | `"IN_PROGRESS"`、`"COMPLETED"` |

## REST API 模式

### 资源设计

```
GET    /api/tasks              → 列出任务(用查询参数过滤)
POST   /api/tasks              → 创建一个任务
GET    /api/tasks/:id          → 获取单个任务
PATCH  /api/tasks/:id          → 更新一个任务(部分)
DELETE /api/tasks/:id          → 删除一个任务

GET    /api/tasks/:id/comments → 列出某个任务的评论(子资源)
POST   /api/tasks/:id/comments → 为某个任务添加评论
```

### 分页

对列表端点进行分页:

```typescript
// 请求
GET /api/tasks?page=1&pageSize=20&sortBy=createdAt&sortOrder=desc

// 响应
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 142,
    "totalPages": 8
  }
}
```

### 过滤

使用查询参数进行过滤:

```
GET /api/tasks?status=in_progress&assignee=user123&createdAfter=2025-01-01
```

### 部分更新(PATCH)

接受部分对象 —— 只更新提供的内容:

```typescript
// 只有 title 发生变化,其他一切保持不变
PATCH /api/tasks/123
{ "title": "Updated title" }
```

## TypeScript 接口模式

### 用判别联合(Discriminated Union)表示变体

```typescript
// 好:每个变体都是显式的
type TaskStatus =
  | { type: 'pending' }
  | { type: 'in_progress'; assignee: string; startedAt: Date }
  | { type: 'completed'; completedAt: Date; completedBy: string }
  | { type: 'cancelled'; reason: string; cancelledAt: Date };

// 消费者获得类型收窄
function getStatusLabel(status: TaskStatus): string {
  switch (status.type) {
    case 'pending': return 'Pending';
    case 'in_progress': return `In progress (${status.assignee})`;
    case 'completed': return `Done on ${status.completedAt}`;
    case 'cancelled': return `Cancelled: ${status.reason}`;
  }
}
```

### 输入/输出分离

```typescript
// 输入:调用者提供的内容
interface CreateTaskInput {
  title: string;
  description?: string;
}

// 输出:系统返回的内容(包含服务器生成的字段)
interface Task {
  id: string;
  title: string;
  description: string | null;
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}
```

### 为 ID 使用品牌类型(Branded Type)

```typescript
type TaskId = string & { readonly __brand: 'TaskId' };
type UserId = string & { readonly __brand: 'UserId' };

// 防止不小心把 UserId 当成 TaskId 传入
function getTask(id: TaskId): Promise<Task> { ... }
```

## 常见的合理化借口

| 合理化借口 | 实际情况 |
|---|---|
| "我们以后再给 API 写文档" | 类型本身就是文档。先定义它们。 |
| "我们现在不需要分页" | 一旦有人有了 100+ 条记录,你就需要了。从一开始就加上它。 |
| "PATCH 太复杂,我们就用 PUT 吧" | PUT 要求每次都传完整对象。PATCH 才是客户端真正想要的。 |
| "等需要的时候我们再给 API 做版本管理" | 没有版本管理的破坏性变更会破坏消费者。从一开始就为可扩展性设计。 |
| "没人用那个未文档化的行为" | Hyrum 定律:只要能被观察到,就会有人依赖它。把每一个公共行为都当作一种承诺。 |
| "我们可以同时维护两个版本" | 多个版本会使维护成本成倍增加,并产生菱形依赖问题。优先遵循单版本原则。 |
| "内部 API 不需要契约" | 内部消费者仍然是消费者。契约能防止耦合,并支持并行开发。 |

## 危险信号

- 根据不同条件返回不同形状的端点
- 不同端点之间不一致的错误格式
- 验证散落在内部代码各处,而不是集中在边界处
- 对现有字段的破坏性变更(类型变化、字段移除)
- 没有分页的列表端点
- REST URL 中出现动词(`/api/createTask`、`/api/getUsers`)
- 第三方 API 响应未经验证或净化就被使用

## 验证

设计完一个 API 之后:

- [ ] 每个端点都有带类型的输入和输出 schema
- [ ] 错误响应遵循单一一致的格式
- [ ] 验证只发生在系统边界处
- [ ] 列表端点支持分页
- [ ] 新字段是增量添加的且是可选的(向后兼容)
- [ ] 命名在所有端点上遵循一致的约定
- [ ] API 文档或类型与实现一起提交

## 限制

- 仅在任务明确匹配其上游来源和本地项目上下文时才使用此技能。
- 在应用变更之前验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例当作针对特定环境的测试、安全审查,或破坏性/高成本操作所需用户批准的替代品。
